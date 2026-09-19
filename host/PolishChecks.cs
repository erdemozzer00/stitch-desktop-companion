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
            foreach(Point position in new[]{new Point(-1920,40),new Point(-5,1100),new Point(-1900,1060),new Point(-260,0)})
            foreach(Size size in new[]{new Size(312,220),new Size(390,275),new Size(624,440)})
            {
                Point p=CompanionUi.PlaceInWorkArea(position,size,work);
                Check(work.Contains(new Rectangle(p,size)),"Remote crosses work area edge");
            }
            Exception failure=null;
            using(PetWindow pet=new PetWindow(Path.Combine(root,"assets"),outDir,true,Path.Combine(root,"carry")))
            using(Form outside=new Form())
            using(Timer steps=new Timer())
            {
                outside.Text="Stitch temporary focus check";outside.ShowInTaskbar=false;outside.Size=new Size(220,90);
                pet.ManualTicks=true;pet.SetSize(240);
                Point anchor=new Point(Screen.PrimaryScreen.WorkingArea.Right-100,Screen.PrimaryScreen.WorkingArea.Bottom+10);
                steps.Interval=300;int stage=0;
                steps.Tick+=delegate
                {
                    try
                    {
                        RemotePanel panel=pet.TrayPanel;
                        if(stage==0)
                        {
                            Check(pet.Visible && pet.TrayVisible,"Launch must show pet and tray icon");
                            Check(!panel.Visible,"Panel opened automatically on launch");
                            Check(panel.Controls.Count==6,"Unexpected extra commands");
                            foreach(Control c in panel.Controls)
                            {Check(c.Text!="El salla","Wave command must not appear in remote");Check(!String.IsNullOrEmpty(c.AccessibleName),"Unnamed remote control");}
                            foreach(ToolStripItem item in pet.OptionsMenu.Items)Check(item.Text!="El salla","Wave command still in tray fallback");
                            // Dispatch through the actual NotifyIcon event; not a physical shell click.
                            var field=typeof(PetWindow).GetField("tray",System.Reflection.BindingFlags.Instance|System.Reflection.BindingFlags.NonPublic);
                            var method=typeof(NotifyIcon).GetMethod("OnMouseClick",System.Reflection.BindingFlags.Instance|System.Reflection.BindingFlags.NonPublic);
                            method.Invoke(field.GetValue(pet),new object[]{new MouseEventArgs(MouseButtons.Left,1,0,0,0)});
                        }
                        else if(stage==1)
                        {
                            Check(panel.Visible,"Tray left-click handler did not show remote");
                            CheckTranslatedPaint(panel,outDir);
                            Check(panel.Owner==null && !panel.ShowInTaskbar,"Remote depends on pet visibility or has taskbar button");
                            Capture(panel,Path.Combine(outDir,"tray-remote-visible.png"));
                            for(int i=0;i<3;i++)
                            {panel.SizeButtons[i].PerformClick();Check(pet.CharacterSize==240+80*i,"Remote size failed");Check(panel.SizeButtons[i].Selected,"Size selection state is stale");}
                            pet.ToggleRemote(anchor);Check(!panel.Visible,"Second tray activation must close");
                            pet.ToggleRemote(anchor);Check(panel.Visible,"Explicit reopen failed");
                            var key=typeof(RemotePanel).GetMethod("ProcessCmdKey",System.Reflection.BindingFlags.Instance|System.Reflection.BindingFlags.NonPublic);
                            object[] keyArgs={new Message(),Keys.Escape};Check((bool)key.Invoke(panel,keyArgs),"Escape not consumed");
                            Check(!panel.Visible,"Escape did not dismiss");
                            Point grip=new Point(pet.CharacterBounds.Left+200,pet.CharacterBounds.Top+200);
                            pet.PointerDownAt(grip);pet.PointerUp();Check(pet.Reactions==1,"Character click no longer waves");
                            Check(!panel.Visible,"Character click opened controls");
                        }
                        else if(stage==2)pet.ToggleRemote(anchor);
                        else if(stage==3){Check(panel.Visible,"Remote not ready for deactivate test");outside.Show();outside.Activate();}
                        else if(stage==4)
                        {
                            Check(!panel.Visible,"Activation of another native window did not dismiss remote");
                            outside.Hide();pet.ToggleRemote(anchor);
                        }
                        else if(stage==5)
                        {
                            Check(panel.Visible,"Remote reopen after deactivate failed");
                            panel.VisibilityButton.PerformClick();Check(!pet.Visible && !panel.Visible && pet.TrayVisible,"Hide must keep only tray access");
                        }
                        else if(stage==6)pet.ToggleRemote(anchor);
                        else if(stage==7)
                        {
                            Check(panel.Visible && panel.VisibilityButton.Text=="Göster","Hidden pet cannot access remote");
                            Capture(panel,Path.Combine(outDir,"tray-remote-hidden.png"));
                            panel.VisibilityButton.PerformClick();Check(pet.Visible && !panel.Visible,"Restore must not auto-open remote");
                        }
                        else if(stage==8)
                        {
                            pet.ToggleRemote(anchor);Check(panel.Visible,"Remote reopen failed");
                            Point grip=new Point(pet.CharacterBounds.Left+200,pet.CharacterBounds.Top+200),before=pet.Location;
                            pet.PointerDownAt(grip);Check(!panel.Visible,"Grab left remote visible");
                            pet.PointerMoveAt(new Point(grip.X+80,grip.Y+30));
                            Check(pet.Location==new Point(before.X+80,before.Y+30),"Drag no longer immediately follows pointer");pet.PointerUp();
                            pet.HidePet();pet.ShowOptions(anchor);
                        }
                        else if(stage==9)
                        {
                            bool restored=false;
                            foreach(ToolStripItem item in pet.OptionsMenu.Items)if(item.Text=="Göster" && item.Available){item.PerformClick();restored=true;break;}
                            Check(restored && pet.Visible,"Hidden pet cannot be restored through fallback menu");
                            pet.OptionsMenu.Close();pet.ToggleRemote(anchor);
                        }
                        else
                        {
                            Check(panel.Visible,"Remote must be open before exit");steps.Stop();panel.ExitButton.PerformClick();
                            Check(pet.IsDisposed,"Remote exit did not close the pet");
                            Check(panel.IsDisposed,"Remote was not disposed on app exit");
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
                +",\"limits\":\"Real control renders and direct-method UI tests. Tray handler and native deactivate tested; physical shell input, keyboard navigation, other DPI and user acceptance remain separate.\"}");
            return 0;
        }
        catch(Exception e){Console.Error.WriteLine(e);return 1;}
    }
    private static void Capture(Control control,string path)
    {
        using(Bitmap bitmap=new Bitmap(control.Width,control.Height))
        {control.DrawToBitmap(bitmap,control.ClientRectangle);bitmap.Save(path);}
    }
    // Repainting a transparent child supplies an offset/clipped Graphics. Drawing
    // must stay within that target, including GDI text (not just GDI+ geometry).
    private static void CheckTranslatedPaint(RemotePanel panel,string directory)
    {
        foreach(Control control in panel.Controls)
        using(Bitmap bitmap=new Bitmap(control.Width+180,control.Height+100))
        using(Graphics g=Graphics.FromImage(bitmap))
        {
            Color sentinel=Color.Magenta;g.Clear(sentinel);
            g.TranslateTransform(160,80);g.SetClip(control.ClientRectangle);
            var paint=control.GetType().GetMethod("OnPaint",System.Reflection.BindingFlags.NonPublic|System.Reflection.BindingFlags.Instance);
            paint.Invoke(control,new object[]{new PaintEventArgs(g,control.ClientRectangle)});
            int escaped=0;
            for(int y=0;y<bitmap.Height;y++)for(int x=0;x<bitmap.Width;x++)
                if(!new Rectangle(160,80,control.Width,control.Height).Contains(x,y) && bitmap.GetPixel(x,y).ToArgb()!=sentinel.ToArgb())escaped++;
            bitmap.Save(Path.Combine(directory,"translated-"+control.TabIndex+".png"));
            Check(escaped==0,"Button repaint escaped translated clip: "+control.AccessibleName+" pixels="+escaped);
        }
    }
}
