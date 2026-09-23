using System;
using System.Drawing;
using System.IO;
using System.Reflection;
using System.Windows.Forms;

internal static class SmileChecks
{
    static int count;
    static void Check(bool ok,string message){count++;if(!ok)throw new Exception(message);}
    static T Field<T>(object p,string n){return (T)p.GetType().GetField(n,BindingFlags.NonPublic|BindingFlags.Instance).GetValue(p);}
    static Point At(PetWindow p,double x,double y){return new Point(p.Left+p.ContentPadding+(int)Math.Round(x*p.CharacterSize),p.Top+p.ContentPadding+(int)Math.Round(y*p.CharacterSize));}
    static void Reset(PetWindow p,int size,int idle){p.HidePet();p.SetSize(size);p.ShowPet();p.AdvanceAt(idle/24.0+.001,Point.Empty);}
    static void Click(PetWindow p,Point at){p.PointerDownAt(at);p.PointerUp();}
    [STAThread] static int Main(string[] args)
    {
        try{
            Application.EnableVisualStyles();Application.SetCompatibleTextRenderingDefault(false);
            Directory.CreateDirectory(args[1]);
            using(var p=new PetWindow(Path.Combine(args[0],"assets"),args[1],false,Path.Combine(args[0],"carry")))
            {
                p.ManualTicks=true;p.Enabled=false;p.Show();
                // Independent screen fixtures selected from rendered nose/neighboring features.
                foreach(int size in new[]{240,320,400})for(int idle=0;idle<96;idle++){
                    foreach(double x in new[]{.445,.485,.525}){
                        Reset(p,size,idle);int before=p.Reactions;Click(p,At(p,x,.35));
                        Check(p.Reactions==before+1,"Nose missed size="+size+" idle="+idle);
                        Check(Field<MotionPlayback>(p,"playback").Reaction==ReactionKind.Smile,"Wrong nose action");
                        Click(p,At(p,x,.35));Click(p,At(p,.655,.69));Click(p,At(p,.205,.24));
                        Check(p.Reactions==before+1,"Busy smile reset/interrupted");
                    }
                    foreach(var point in new[]{new PointF(.38f,.32f),new PointF(.60f,.32f),new PointF(.485f,.43f),new PointF(.49f,.25f),new PointF(.5f,.6f),new PointF(.02f,.02f)}){
                        Reset(p,size,idle);int before=p.Reactions;Click(p,At(p,point.X,point.Y));
                        Check(p.Reactions==before,"Neighboring eye/mouth/body/empty region reacts");
                    }
                    Reset(p,size,idle);int previous=p.Reactions;Point down=At(p,.485,.35),origin=p.Location;
                    p.PointerDownAt(down);p.PointerMoveAt(new Point(down.X+30,down.Y-20));
                    Check(p.Location==new Point(origin.X+30,origin.Y-20),"Nose drag lags pointer");
                    p.PointerUp();Check(p.Reactions==previous,"Nose drag starts smile");
                }
                Reset(p,320,0);int beforeCancel=p.Reactions;p.PointerDownAt(At(p,.485,.35));p.CancelPointer();p.PointerUp();
                Check(p.Reactions==beforeCancel,"Cancelled nose press reacts");
                Reset(p,320,0);p.PointerDownAt(At(p,.485,.35));p.SetSize(240);p.PointerUp();
                Check(p.Reactions==beforeCancel,"Resize retains armed smile");
                Reset(p,320,0);Click(p,At(p,.485,.35));
                var player=Field<MotionPlayback>(p,"playback");double start=Field<double>(player,"reactionStart");
                foreach(int frame in new[]{1,8,12,22,28}){
                    p.AdvanceAt(start+(frame+3+.01)/24,Point.Empty);
                    var actual=(Bitmap)typeof(PetWindow).GetMethod("CurrentFrame",BindingFlags.NonPublic|BindingFlags.Instance).Invoke(p,null);
                    using(var image=Image.FromFile(Path.Combine(args[0],"assets","smile_"+frame.ToString("0000")+".png")))
                    using(var expected=new Bitmap(image))
                        for(int y=0;y<400;y+=5)for(int x=0;x<400;x+=5)
                            Check(actual.GetPixel(x,y)==expected.GetPixel(x,y),"Wrong smile bitmap/frame");
                }
                int beforeBusy=p.Reactions;p.PointerDownAt(At(p,.485,.35));p.AdvanceAt(start+33.0/24,Point.Empty);p.PointerUp();
                Check(p.Reactions==beforeBusy,"Busy press queued after smile");
                Reset(p,400,0);beforeBusy=p.Reactions;
                var carry=Field<CarryResponse>(p,"carry");carry.Angle=.1;carry.Pivot=new PointF(.5f,.6f);carry.Offset=new PointF(.09f,-.08f);
                Click(p,At(p,Math.Cos(.1)*(-.015)-Math.Sin(.1)*(-.25)+.59,Math.Sin(.1)*(-.015)+Math.Cos(.1)*(-.25)+.52));
                Check(p.Reactions==beforeBusy+1 && Field<MotionPlayback>(p,"playback").Reaction==ReactionKind.Smile,"Residual carry transform misroutes nose");
                p.Close();
            }
            foreach(int interrupt in new[]{1,12,27}){
                var m=new MotionPlayback();Check(m.React(0,ReactionKind.Smile),"Smile starts");m.Advance(interrupt/24.0);m.BeginCarry(interrupt/24.0);
                Check(m.Reacting && m.Reaction==ReactionKind.Smile,"Carry resets smile");
                Check(!m.React(1,ReactionKind.Wave),"Overlap allowed");m.Advance(31.9/24);Check(m.Reacting,"Smile ends early");
                m.Advance(32.1/24);Check(!m.Reacting && m.CarryReady,"Smile duration or carry handoff");
            }
            string partial=Path.Combine(args[1],"partial");Directory.CreateDirectory(partial);
            foreach(string file in Directory.GetFiles(Path.Combine(args[0],"assets")))
                if(Path.GetFileName(file)!="smile_0028.png")File.Copy(file,Path.Combine(partial,Path.GetFileName(file)));
            bool rejected=false;try{using(var invalid=new PetWindow(partial,args[1],false)){}}catch(IOException){rejected=true;}
            Check(rejected,"Partial smile bank accepted");
            if(args.Length>2)using(var old=new PetWindow(Path.Combine(args[2],"assets"),args[1],false)){
                old.ManualTicks=true;old.Show();Click(old,At(old,.485,.35));Check(old.Reactions==0,"Legacy bank nose changed");
                Click(old,At(old,.655,.69));Check(old.Reactions==1,"Legacy bank wave broken");old.Close();
            }
            Console.WriteLine("SMILE_CHECKS_PASS assertions="+count);return 0;
        }catch(Exception error){Console.Error.WriteLine(error);return 1;}
    }
}
