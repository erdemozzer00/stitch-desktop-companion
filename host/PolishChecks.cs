using System;
using System.Diagnostics;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Windows.Forms;

internal static class PolishChecks
{
    private static int checks;
    private static void Check(bool value,string message){checks++;if(!value)throw new Exception(message);}
    private static double Luminance(Color c)
    {
        double[] v={c.R/255.0,c.G/255.0,c.B/255.0};
        for(int i=0;i<3;i++)v[i]=v[i]<=.04045?v[i]/12.92:Math.Pow((v[i]+.055)/1.055,2.4);
        return .2126*v[0]+.7152*v[1]+.0722*v[2];
    }
    [STAThread]private static int Main(string[] args)
    {
        try
        {
            Application.EnableVisualStyles();Application.SetCompatibleTextRenderingDefault(false);
            string root=args[0],outDir=Path.Combine(root,"ui-review");Directory.CreateDirectory(outDir);
            double minContrast=100,firstHandoff=0,oldTail=0;
            foreach(Color ink in new[]{PetPalette.Text,PetPalette.Muted})
            foreach(Color bg in new[]{PetPalette.Top,PetPalette.Bottom,PetPalette.Hover})
            { double ratio=(Luminance(ink)+.05)/(Luminance(bg)+.05);minContrast=Math.Min(minContrast,ratio);Check(ratio>=4.5,"Text contrast below 4.5:1"); }
            foreach(int side in new[]{240,320,400})
            {
                CarryResponse r=new CarryResponse();r.Begin(0,PointF.Empty,new PointF(.5f,.6f));
                for(int i=1;i<=120;i++)r.Update(i/120.0,new PointF(240*i/120f,120*i/120f),240);
                r.Release();double handoff=-1,finish=-1;
                MotionPlayback p=new MotionPlayback();p.BeginCarry(0);p.Advance(1);
                for(int i=1;i<=240;i++)
                {
                    double t=i/120.0;r.Update(1+t,new PointF(240,120),240);
                    if(handoff<0 && r.CanResumeIdle(side)) {handoff=t;p.EndCarry(1+t);}
                    p.Advance(1+t);
                    if(handoff>=0 && t>handoff+.09)Check(p.IdleIndex>0,"Idle still blocked by residual settling");
                    if(!r.Active){finish=t;break;}
                }
                Check(handoff>=0 && finish-handoff>.2,"Subvisible tail was not separated from idle");
                if(side==240){firstHandoff=handoff;oldTail=finish-handoff;}
            }
            Rectangle work=new Rectangle(-1920,40,1920,1040);
            foreach(Point position in new[]{new Point(-1920,40),new Point(-240,840),new Point(-1900,840),new Point(-260,50)})
            {
                Size size=new Size(180,46);Point p=CompanionUi.PlaceInWorkArea(new Rectangle(position,new Size(240,240)),size,work);
                Check(work.Contains(new Rectangle(p,size)),"Toolbar crosses work area edge");
            }
            Exception failure=null;
            using(PetWindow pet=new PetWindow(Path.Combine(root,"assets"),outDir,true,Path.Combine(root,"carry")))
            using(Timer steps=new Timer())
            {
                pet.ManualTicks=true;pet.SetSize(240);
                steps.Interval=250;int stage=0;
                steps.Tick+=delegate
                {
                    try
                    {
                        if(stage==0)
                        {
                            Check(pet.ControlBar.Visible,"Welcome controls not visible");
                            Check(pet.ControlBar.More.AccessibleName.Length>0,"More control lacks accessible name");
                            Capture(pet.ControlBar,Path.Combine(outDir,"toolbar.png"));
                            pet.ControlBar.Wave.PerformClick();Check(pet.Reactions==1,"Wave button did not invoke existing action");
                            pet.ControlBar.More.PerformClick();Check(pet.OptionsMenu.Visible,"More did not open options");
                        }
                        else if(stage==1)
                        {
                            Capture(pet.OptionsMenu,Path.Combine(outDir,"menu.png"));
                            foreach(ToolStripItem item in pet.OptionsMenu.Items)
                                if(item.Text=="Boyut")((ToolStripMenuItem)item).DropDownItems[2].PerformClick();
                            Check(pet.CharacterSize==400,"Size menu failed");
                            pet.OptionsMenu.Close();
                            Point grip=new Point(pet.CharacterBounds.Left+200,pet.CharacterBounds.Top+200);
                            pet.PointerDownAt(grip);Check(!pet.ControlBar.Visible,"Toolbar stayed visible during grab");
                            pet.CancelPointer();pet.HidePet();Check(!pet.Visible && !pet.ControlBar.Visible,"Hide orphaned toolbar");
                            pet.ShowOptions(Cursor.Position);
                        }
                        else
                        {
                            bool restored=false;
                            foreach(ToolStripItem item in pet.OptionsMenu.Items)if(item.Text=="Göster" && item.Available){item.PerformClick();restored=true;break;}
                            Check(restored && pet.Visible,"Hidden pet cannot be restored through menu");
                            pet.OptionsMenu.Close();steps.Stop();pet.Close();
                        }
                        stage++;
                    }
                    catch(Exception e){failure=e;steps.Stop();pet.Close();}
                };
                pet.Shown+=delegate{steps.Start();};Application.Run(pet);
            }
            if(failure!=null)throw failure;
            Console.WriteLine("{\"status\":\"PASS\",\"assertions\":"+checks+",\"min_text_contrast\":"+minContrast.ToString("F2",CultureInfo.InvariantCulture)
                +",\"release_idle_at_240_seconds\":"+firstHandoff.ToString("F3",CultureInfo.InvariantCulture)+",\"removed_near_static_tail_seconds\":"+oldTail.ToString("F3",CultureInfo.InvariantCulture)
                +",\"limits\":\"Real control renders and direct-method UI tests. Physical hover/keyboard, different DPI and user visual acceptance remain separate.\"}");
            return 0;
        }
        catch(Exception e){Console.Error.WriteLine(e);return 1;}
    }
    private static void Capture(Control control,string path)
    {
        using(Bitmap bitmap=new Bitmap(control.Width,control.Height))
        {control.DrawToBitmap(bitmap,control.ClientRectangle);bitmap.Save(path);}
    }
}
