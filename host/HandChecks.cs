// Exercise the real layered-window input path with independent screen fixtures.
using System;
using System.Drawing;
using System.IO;
using System.Reflection;
using System.Windows.Forms;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Globalization;
using System.Collections.Generic;

internal static class HandChecks
{
    static int assertions;
    static void Check(bool condition,string message){assertions++;if(!condition)throw new Exception(message);}
    static T Field<T>(object value,string name){return (T)value.GetType().GetField(name,BindingFlags.NonPublic|BindingFlags.Instance).GetValue(value);}
    static Point At(PetWindow pet,double x,double y){return new Point(pet.Left+pet.ContentPadding+(int)Math.Round(x*pet.CharacterSize),pet.Top+pet.ContentPadding+(int)Math.Round(y*pet.CharacterSize));}
    static void Click(PetWindow pet,Point at){pet.PointerDownAt(at);pet.PointerUp();}
    static string Reaction(PetWindow pet){var p=Field<MotionPlayback>(pet,"playback");var property=p.GetType().GetProperty("Reaction",BindingFlags.Public|BindingFlags.NonPublic|BindingFlags.Instance);return property==null?"Wave":property.GetValue(p,null).ToString();}
    static void Reset(PetWindow pet,int size,int idle){pet.HidePet();pet.SetSize(size);pet.ShowPet();pet.AdvanceAt(idle/24.0+.001,Point.Empty);}
    [STAThread] static int Main(string[] args)
    {
        try
        {
            Application.EnableVisualStyles();Application.SetCompatibleTextRenderingDefault(false);
            string root=args[0],output=args[1];Directory.CreateDirectory(output);
            if(args.Length>2 && args[2]=="--measure"){Measure(root,output);return 0;}
            using(var pet=new PetWindow(Path.Combine(root,"assets"),output,false,Path.Combine(root,"carry")))
            {
                pet.ManualTicks=true;pet.Enabled=false;pet.Show();
                Reset(pet,320,0);int count=pet.Reactions;
                Click(pet,At(pet,.5,.6));Check(pet.Reactions==count,"Body click incorrectly starts a gesture");
                Click(pet,At(pet,.02,.02));Check(pet.Reactions==count,"Transparent corner starts a gesture");
                Reset(pet,400,0);count=pet.Reactions;
                Click(pet,At(pet,.695,.75));Check(pet.Reactions==count,"Empty pixel inside hand bounds starts a gesture");
                foreach(int size in new[]{240,320,400})for(int idle=0;idle<96;idle++)
                {
                    foreach(bool peace in new[]{false,true})
                    {
                        Reset(pet,size,idle);count=pet.Reactions;
                        Click(pet,At(pet,peace?.33:.655,peace?.685:.69));
                        Check(pet.Reactions==count+1,"Hand missed at size="+size+" idle="+idle);
                        Check(Reaction(pet)==(peace?"Peace":"Wave"),"Wrong hand gesture");
                        Click(pet,At(pet,peace?.655:.33,.69));
                        Check(pet.Reactions==count+1,"Repeated/opposite click interrupted reaction");
                    }
                }
                foreach(bool peace in new[]{false,true})
                {
                    Reset(pet,320,0);count=pet.Reactions;
                    Click(pet,At(pet,peace?.33:.655,.69));
                    var player=Field<MotionPlayback>(pet,"playback");
                    double start=Field<double>(player,"reactionStart");
                    pet.AdvanceAt(start+28.01/24,Point.Empty);
                    var current=(Bitmap)typeof(PetWindow).GetMethod("CurrentFrame",BindingFlags.NonPublic|BindingFlags.Instance).Invoke(pet,null);
                    using(Image png=Image.FromFile(Path.Combine(root,"assets",(peace?"peace":"wave")+"_0025.png")))
                    using(Bitmap expected=new Bitmap(png))
                        for(int y=0;y<400;y+=5)for(int x=0;x<400;x+=5)
                            Check(current.GetPixel(x,y)==expected.GetPixel(x,y),"Selected reaction renders wrong clip/frame");
                    // A press during a reaction must not be queued when it ends.
                    pet.PointerDownAt(At(pet,peace?.655:.33,.69));
                    pet.AdvanceAt(start+3,Point.Empty);pet.PointerUp();
                    Check(pet.Reactions==count+1,"Press during reaction queued a new greeting");

                    Reset(pet,320,0);count=pet.Reactions;
                    Point down=At(pet,peace?.33:.655,.69),location=pet.Location;
                    pet.PointerDownAt(down);pet.PointerMoveAt(new Point(down.X+30,down.Y-20));
                    Check(pet.Location==new Point(location.X+30,location.Y-20),"Drag did not follow first pointer move");
                    pet.PointerUp();Check(pet.Reactions==count,"Drag release started greeting");
                    Reset(pet,320,0);count=pet.Reactions;
                    pet.PointerDownAt(At(pet,peace?.33:.655,.69));pet.CancelPointer();pet.PointerUp();
                    Check(pet.Reactions==count,"Capture cancellation started greeting");

                    Reset(pet,320,0);count=pet.Reactions;
                    var carry=Field<CarryResponse>(pet,"carry");
                    carry.Angle=.1;carry.Pivot=new PointF(.5f,.6f);carry.Offset=new PointF(.09f,-.08f);
                    // Independent projected fixture: source (.655,.69) or (.33,.685),
                    // rotated 0.1 rad around (.5,.6), translated (+.09,-.08).
                    Click(pet,At(pet,peace?.412363:.735241,peace?.587604:.625025));
                    Check(pet.Reactions==count+1 && Reaction(pet)==(peace?"Peace":"Wave"),"Residual carry transform misroutes hand");

                    Reset(pet,320,0);count=pet.Reactions;
                    pet.PointerDownAt(At(pet,peace?.33:.655,.69));pet.SetSize(240);pet.PointerUp();
                    Check(pet.Reactions==count,"Resize retained armed hand click");
                }
                foreach(ReactionKind kind in new[]{ReactionKind.Wave,ReactionKind.Peace})
                foreach(int interrupt in new[]{1,20,40})
                {
                    var player=new MotionPlayback();int length=kind==ReactionKind.Peace?64:49;
                    Check(player.React(0,kind),"Gesture did not start");
                    player.Advance(interrupt/24.0);player.BeginCarry(interrupt/24.0);
                    Check(player.Reacting && player.Reaction==kind,"Drag resets active gesture");
                    Check(!player.React(.9,kind==ReactionKind.Wave?ReactionKind.Peace:ReactionKind.Wave),"Carry accepts overlapping gesture");
                    player.Advance((length-.1)/24.0);Check(player.Reacting,"Gesture ends too early");
                    player.Advance((length+.1)/24.0);Check(!player.Reacting && player.CarryReady,"Gesture does not hand over to carry");
                    player.EndCarry(3);Check(player.React(3.1,kind),"Settled carry cannot greet again");
                }
                pet.Close();
            }
            string partial=Path.Combine(output,"partial-assets");Directory.CreateDirectory(partial);
            foreach(string file in Directory.GetFiles(Path.Combine(root,"assets"),"*.png"))
                if(Path.GetFileName(file)!="peace_0001.png")File.Copy(file,Path.Combine(partial,Path.GetFileName(file)));
            bool rejected=false;
            try{using(var invalid=new PetWindow(partial,output,false)){}}
            catch(IOException){rejected=true;}
            Check(rejected,"Partial gesture bank silently falls back to legacy input");
            Console.WriteLine("{\"status\":\"PASS\",\"assertions\":"+assertions+",\"scope\":\"Native window direct-method checks, not physical mouse acceptance\"}");return 0;
        }catch(Exception error){Console.Error.WriteLine(error);return 1;}
    }
    [DllImport("user32.dll")] static extern int GetGuiResources(IntPtr process,int flags);
    static string Sample(string phase,Stopwatch watch,double cpuStart)
    {
        var process=Process.GetCurrentProcess();process.Refresh();
        return "{\"phase\":\""+phase+"\",\"elapsed_seconds\":"+watch.Elapsed.TotalSeconds.ToString("F3",CultureInfo.InvariantCulture)
            +",\"cpu_seconds\":"+(process.TotalProcessorTime.TotalSeconds-cpuStart).ToString("F3",CultureInfo.InvariantCulture)
            +",\"working_set\":"+process.WorkingSet64+",\"private_bytes\":"+process.PrivateMemorySize64
            +",\"managed_bytes\":"+GC.GetTotalMemory(false)+",\"gdi_objects\":"+GetGuiResources(process.Handle,0)+"}";
    }
    static void Measure(string root,string output)
    {
        var samples=new List<string>();
        using(var pet=new PetWindow(Path.Combine(root,"assets"),output,true,Path.Combine(root,"carry")))
        using(var timer=new Timer())
        {
            pet.SetSize(320);pet.Enabled=false;var watch=new Stopwatch();int stage=0;
            double cpuStart=Process.GetCurrentProcess().TotalProcessorTime.TotalSeconds;
            timer.Interval=50;
            timer.Tick+=delegate{
                if(stage==0 && watch.Elapsed.TotalSeconds>=2){samples.Add(Sample("idle",watch,cpuStart));Click(pet,At(pet,File.Exists(Path.Combine(root,"assets","hands.csv"))?.33:.655,.69));stage++;}
                if(stage==1 && watch.Elapsed.TotalSeconds>=3){samples.Add(Sample("gesture",watch,cpuStart));stage++;}
                if(stage==2 && watch.Elapsed.TotalSeconds>=6){samples.Add(Sample("idle_return",watch,cpuStart));timer.Stop();pet.Close();}
            };
            pet.Shown+=delegate{watch.Start();timer.Start();};Application.Run(pet);
        }
        Console.WriteLine("{\"samples\":["+String.Join(",",samples)+"],\"scope\":\"Six-second real host window/tray observation; not a sustained resource benchmark\"}");
    }
}
