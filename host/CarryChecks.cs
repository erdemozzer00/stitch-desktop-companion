// Focused Phase 04 checks against the real controller, renderer and host paths.
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Runtime.InteropServices;
using System.Windows.Forms;

internal static class CarryChecks
{
    private static int assertions;
    private static void Check(bool condition, string message)
    {
        assertions++;
        if (!condition) throw new Exception(message);
    }
    private static double[] Row(string text) { return Array.ConvertAll(text.Split(','), x => Double.Parse(x, CultureInfo.InvariantCulture)); }
    [STAThread]
    private static int Main(string[] args)
    {
        try
        {
            Application.EnableVisualStyles(); Application.SetCompatibleTextRenderingDefault(false);
            string root = args[0], output = args[1]; Directory.CreateDirectory(output);
            if (args.Length > 2) { Smoke(root, output, args[2] == "--live-carry"); return 0; }
            TimelineChecks();
            double error = ReplayChecks(root);
            PixelChecks(root, output);
            using (PetWindow pet = new PetWindow(Path.Combine(root,"assets"),output,false,Path.Combine(root,"carry")))
            {
                pet.Location = new Point(200,200);
                Point start = new Point(400,400);
                pet.PointerDownAt(start); pet.PointerMoveAt(new Point(401,400));
                Check(pet.Location == new Point(200,200),"Sub-threshold move displaced window");
                pet.PointerMoveAt(new Point(440,380));
                Check(pet.Location == new Point(240,180),"First drag move did not follow pointer immediately");
                pet.AdvanceAt(.2,new Point(440,380));
                pet.PointerMoveAt(new Point(360,420));
                Check(pet.Location == new Point(160,220),"Reversal changed pointer offset");
                pet.CancelPointer(); pet.PointerMoveAt(new Point(900,900));
                Check(pet.Location == new Point(160,220),"Capture cancellation left drag armed");
                pet.PointerUp(); Check(pet.Reactions==0,"Cancel/release generated a wave");
                pet.HidePet(); pet.SetSize(240);
                Check(!pet.Visible && pet.CharacterSize==240,"Hidden resize made the pet visible");
            }
            Console.WriteLine("{\"status\":\"PASS\",\"assertions\":"+assertions+",\"python_replay_max_angle_error\":"+error.ToString("R",CultureInfo.InvariantCulture)
                +",\"limits\":\"Controller/state/pixel/direct-method checks; not physical mouse or visual acceptance.\"}");
            return 0;
        }
        catch(Exception error) { Console.Error.WriteLine(error); return 1; }
    }
    private static void TimelineChecks()
    {
        for(int phase=0;phase<96;phase++)
        {
            MotionPlayback p = new MotionPlayback(); double now=(phase+.1)/24;
            p.Advance(now); p.BeginCarry(now);
            Check(p.EntryOnly && p.ReactionIndex==0,"Idle must enter through existing bridge");
            Check(!p.React(now),"Carry accepted click-wave");
            p.Advance(now+3.1/24); Check(p.EntryOnly && p.ReactionIndex==3,"Entry skipped last frame");
            p.Advance(now+4.1/24); Check(p.CarryReady && !p.Reacting,"Idle bridge did not enter carry");
            p.EndCarry(now+.4); p.Advance(now+.4); Check(!p.CarryReady && p.IdleIndex==0,"Release did not return to idle neutral");
            p.Reset(); p.BeginCarry(0); p.EndCarry(.01); p.Advance(.2);
            Check(!p.CarryReady && !p.Reacting,"Quick release triggered wave or stuck carry");
        }
        // Every wave frame, plus each entry frame for all 24 buckets.
        for(int bucket=0;bucket<24;bucket++) for(int frame=0;frame<49;frame++)
        {
            if(bucket!=0 && frame>=4) continue;
            MotionPlayback p = new MotionPlayback(); double start=bucket*4/24.0;
            p.Advance(start); p.React(start); double now=start+(frame+.1)/24;
            p.Advance(now); p.BeginCarry(now);
            Check(p.ReactionIndex==frame && !p.EntryOnly,"Drag reset active wave/entry");
            p.Advance(start+48.1/24); Check(p.ReactionIndex==48,"Wave return was skipped");
            p.Advance(start+49.1/24); Check(p.CarryReady,"Wave endpoint failed to enter carry");
            p.EndCarry(start+3); p.Advance(start+3); Check(p.IdleIndex==0 && !p.CarryReady,"Carry exit failed");
            p.Reset(); p.React(0); p.Advance(.5); p.BeginCarry(.5); p.EndCarry(.6); p.Advance(.7);
            Check(p.Reacting && !p.CarryReady,"Quick wave drag interrupted greeting");
            p.Reset(); Check(!p.Reacting && !p.CarryReady,"Hide left carry state active");
        }
    }
    private static double ReplayChecks(string root)
    {
        string[] inputs=File.ReadAllLines(Path.Combine(root,"inputs.csv")), oracle=File.ReadAllLines(Path.Combine(root,"reference.csv"));
        CarryResponse r=new CarryResponse(); double[] first=Row(inputs[0]);
        r.Begin(0,new PointF((float)first[1],(float)first[2]),new PointF(.5f,.6f));
        double max=0;
        for(int i=0;i<inputs.Length;i++)
        {
            double[] row=Row(inputs[i]); if(row[0]>=6.65) r.Release();
            r.Update(row[0],new PointF((float)row[1],(float)row[2]),240);
            Check(Math.Abs(r.Angle)<=.180001 && r.FrameIndex>=0 && r.FrameIndex<45,"Unbounded response");
            if(i%5==0)
            {
                double[] expected=Row(oracle[i/5]);
                max=Math.Max(max,Math.Abs(r.Angle-expected[3]));
                Check(Math.Abs(r.Angle-expected[3])<.00011,"C# response differs from accepted Python trace");
                Check(Math.Abs(r.Vertical-expected[5])<.00011,"Vertical response differs from accepted trace");
            }
        }
        Check(!r.Active && r.Angle==0,"Release did not stop updating at rest");
        r.Begin(10,new PointF(0,0),new PointF(.3f,.2f)); r.Update(10.02,new PointF(100,30),240);
        PointF a=r.Map(new PointF(.2f,.4f)), b=r.Map(new PointF(.7f,.8f));
        r.Begin(10.021,new PointF(100,30),new PointF(.6f,.2f));
        Check(Distance(a,r.Map(new PointF(.2f,.4f)))<.000001 && Distance(b,r.Map(new PointF(.7f,.8f)))<.000001,"Re-grab changed affine pose");
        r.Update(20,new PointF(10000,-10000),240); Check(Math.Abs(r.Angle)<.18,"Resume gap caused unbounded impulse");
        r.Release(); for(int i=1;i<=120;i++)r.Update(20+i/120.0,new PointF(10000,-10000),240);
        Check(!r.Active,"Stall/release did not settle");
        r.Begin(22,new PointF(0,0),new PointF(.5f,.6f)); r.Update(22.02,new PointF(30,0),240);
        for(int i=1;i<=180;i++)r.Update(22.02+i/120.0,new PointF(30,0),240);
        Check(r.Held && r.Active && r.Angle==0 && r.Vertical==0 && r.FrameIndex==22,"Held rest would redraw indefinitely");
        return max;
    }
    private static double Distance(PointF a, PointF b) { return Math.Sqrt((a.X-b.X)*(a.X-b.X)+(a.Y-b.Y)*(a.Y-b.Y)); }
    private static void PixelChecks(string root, string output)
    {
        PointF[] grips={new PointF(.5f,.6f),new PointF(.5f,.25f),new PointF(.15f,.3f),new PointF(.4f,.88f)};
        using(Bitmap marker=new Bitmap(240,240))
        {
            using(Graphics g=Graphics.FromImage(marker))g.FillRectangle(Brushes.White,117,141,7,7);
            foreach(PointF grip in grips) foreach(double angle in new[]{-.18,.18})
            {
                CarryResponse r=new CarryResponse();r.Pivot=grip;r.Angle=angle;
                PointF expected=r.Map(new PointF(.5f,.6f));
                using(Bitmap surface=CarrySurface.Create(marker,240,r,PointF.Empty))
                    Check(surface.GetPixel(CarrySurface.Padding(240)+(int)Math.Round(expected.X*240),
                        CarrySurface.Padding(240)+(int)Math.Round(expected.Y*240)).A>240,"GDI+ rendered position differs from transform");
            }
        }
        using(CarryBank bank=new CarryBank(Path.Combine(root,"carry")))
        foreach(int size in new[]{240,320,400})
        foreach(PointF grip in grips)
        foreach(double angle in new[]{-.18,0,.18})
        foreach(int index in new[]{0,4,8,18,22,26,36,40,44})
        {
            CarryResponse r=new CarryResponse(); r.Pivot=grip; r.Angle=angle;
            Check(Distance(r.Map(grip),grip)<.000001,"Rotation displaced selected grip");
            using(Bitmap surface=CarrySurface.Create(bank.Frames[index],size,r,PointF.Empty))
            {
                int n=surface.Width;
                for(int i=0;i<n;i++) Check(surface.GetPixel(i,0).A==0 && surface.GetPixel(i,n-1).A==0
                    && surface.GetPixel(0,i).A==0 && surface.GetPixel(n-1,i).A==0,"Transformed alpha clipped");
                if(size==240 && grip==grips[0] && index==22)
                    surface.Save(Path.Combine(output,"native-angle-"+angle.ToString("F2",CultureInfo.InvariantCulture)+".png"));
            }
        }
    }
    [DllImport("user32.dll")] private static extern int GetGuiResources(IntPtr process, int flags);
    private static string Sample(string name, Stopwatch wall, double cpuStart)
    {
        Process p=Process.GetCurrentProcess(); p.Refresh();
        double cpu=p.TotalProcessorTime.TotalSeconds-cpuStart;
        return "{\"phase\":\""+name+"\",\"elapsed_seconds\":"+wall.Elapsed.TotalSeconds.ToString("F3",CultureInfo.InvariantCulture)
            +",\"cpu_seconds\":"+cpu.ToString("F3",CultureInfo.InvariantCulture)+",\"working_set\":"+p.WorkingSet64
            +",\"private_bytes\":"+p.PrivateMemorySize64+",\"managed_bytes\":"+GC.GetTotalMemory(false)
            +",\"gdi_objects\":"+GetGuiResources(p.Handle,0)+"}";
    }
    private static void Smoke(string root,string output,bool enabled)
    {
        List<string> samples=new List<string>();
        using(PetWindow pet=new PetWindow(Path.Combine(root,"assets"),output,false,enabled?Path.Combine(root,"carry"):null))
        using(Timer ticks=new Timer())
        {
            pet.ManualTicks=true; pet.Enabled=false; pet.SetSize(240);
            Stopwatch watch=new Stopwatch(); double cpuStart=Process.GetCurrentProcess().TotalProcessorTime.TotalSeconds;
            int step=0,round=0; Point origin=Point.Empty,initialWindow=Point.Empty; bool began=false;
            string[] inputs=File.ReadAllLines(Path.Combine(root,"inputs.csv"));
            ticks.Interval=16;
            ticks.Tick+=delegate
            {
                double now=watch.Elapsed.TotalSeconds;
                if(now<2) { pet.AdvanceAt(now,Point.Empty); return; }
                if(!began)
                {
                    samples.Add(Sample("idle",watch,cpuStart));
                    origin=new Point(pet.Left+pet.ContentPadding+120,pet.Top+pet.ContentPadding+145);
                    initialWindow=pet.Location; pet.PointerDownAt(origin); began=true;
                }
                int index=Math.Min(1020,step*2); double[] row=Row(inputs[index]);
                Point pointer=new Point(origin.X+(int)Math.Round(row[1]-200),origin.Y+(int)Math.Round(row[2]-270));
                if(row[0]<6.65) pet.PointerMoveAt(pointer); else pet.PointerUp();
                pet.AdvanceAt(now,pointer); step++;
                if(index<1020)return;
                samples.Add(Sample("drag_round_"+round,watch,cpuStart)); round++;
                if(round<2) { step=0; pet.Location=initialWindow; pet.PointerDownAt(origin); return; }
                pet.PointerDownAt(origin); pet.PointerMoveAt(new Point(origin.X+30,origin.Y)); pet.CancelPointer();
                pet.HidePet(); pet.SetSize(400); pet.ShowPet(); pet.AdvanceAt(0,origin);
                pet.SetSize(320); pet.ShowPet(); pet.AdvanceAt(.1,origin);
                Check(pet.Reactions==0,"Synthetic drag generated click wave");
                samples.Add(Sample("after_hide_resize_show",watch,cpuStart));
                ticks.Stop(); pet.Close();
            };
            pet.Shown+=delegate { watch.Start(); ticks.Start(); };
            Application.Run(pet);
        }
        Console.WriteLine("{\"status\":\"PASS\",\"carry_enabled\":"+(enabled?"true":"false")+",\"samples\":["+String.Join(",",samples)
            +"],\"limits\":\"Visible Windows layered-window direct-method replay. No physical input, menu/tray acceptance or desktop screenshots. CPU samples are cumulative, not percentages.\"}");
    }
}
