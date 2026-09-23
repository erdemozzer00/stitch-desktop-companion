using System;
using System.Drawing;
using System.IO;
using System.Reflection;
using System.Windows.Forms;

internal static class EarChecks
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
                foreach(int size in new[]{240,320,400})for(int idle=0;idle<96;idle++)foreach(bool left in new[]{true,false})
                {
                    Reset(p,size,idle);int before=p.Reactions;
                    Point at=At(p,left?.205:.79,.24);Click(p,at);
                    var player=Field<MotionPlayback>(p,"playback");
                    Check(p.Reactions==before+1,"Ear missed size="+size+" idle="+idle);
                    Check(player.Reaction.ToString()==(left?"EarLeft":"EarRight"),"Wrong ear reaction");
                    Click(p,At(p,.33,.685));Check(p.Reactions==before+1,"Hand interrupted ear");
                    Click(p,At(p,left?.79:.205,.24));Check(p.Reactions==before+1,"Opposite ear interrupted reaction");
                    Reset(p,size,idle);before=p.Reactions;Point origin=p.Location;
                    at=At(p,left?.205:.79,.24);p.PointerDownAt(at);p.PointerMoveAt(new Point(at.X+30,at.Y+20));
                    Check(p.Location==new Point(origin.X+30,origin.Y+20),"Ear drag lag");
                    p.PointerUp();Check(p.Reactions==before,"Ear drag triggers reaction");
                }
                foreach(bool left in new[]{true,false})
                {
                    Reset(p,320,0);int before=p.Reactions;Point at=At(p,left?.205:.79,.24);
                    p.PointerDownAt(at);p.CancelPointer();p.PointerUp();Check(p.Reactions==before,"Cancelled ear press reacts");
                    Reset(p,320,0);p.PointerDownAt(at);p.SetSize(240);p.PointerUp();Check(p.Reactions==before,"Resize keeps ear intent");
                    Reset(p,320,0);Click(p,At(p,left?.205:.79,.24));
                    var player=Field<MotionPlayback>(p,"playback");
                    var kind=player.Reaction;
                    double start=Field<double>(player,"reactionStart");
                    p.AdvanceAt(start+8.01/24,Point.Empty);
                    var current=(Bitmap)typeof(PetWindow).GetMethod("CurrentFrame",BindingFlags.NonPublic|BindingFlags.Instance).Invoke(p,null);
                    Check(player.ReactionIndex==8 && player.Reaction==kind,"Ear frame selection state");
                    using(var source=Image.FromFile(Path.Combine(args[0],"assets",(left?"ear_left_":"ear_right_")+"0005.png")))
                    using(var expected=new Bitmap(source))
                        for(int py=0;py<400;py+=5)for(int px=0;px<400;px+=5)
                            Check(current.GetPixel(px,py)==expected.GetPixel(px,py),"Wrong ear bitmap/frame");
                    before=p.Reactions;p.PointerDownAt(At(p,left?.79:.205,.24));
                    p.AdvanceAt(start+21.0/24,Point.Empty);p.PointerUp();
                    Check(p.Reactions==before,"Busy ear press queued after completion");
                    foreach(int interrupt in new[]{1,7,17}){
                        var m=new MotionPlayback();Check(m.React(0,kind),"Ear start");m.Advance(interrupt/24.0);m.BeginCarry(interrupt/24.0);
                        Check(m.Reacting && m.Reaction==kind,"Carry resets ear");m.Advance(19.9/24);Check(m.Reacting,"Ear ends early");
                        m.Advance(20.1/24);Check(!m.Reacting && m.CarryReady,"Ear duration or carry handoff incorrect");
                    }
                    Reset(p,400,0);before=p.Reactions;
                    var carry=Field<CarryResponse>(p,"carry");carry.Angle=.1;carry.Pivot=new PointF(.5f,.6f);carry.Offset=new PointF(.09f,-.08f);
                    double x=left?.205:.79, y=.24;
                    Click(p,At(p,Math.Cos(.1)*(x-.5)-Math.Sin(.1)*(y-.6)+.59,Math.Sin(.1)*(x-.5)+Math.Cos(.1)*(y-.6)+.52));
                    Check(p.Reactions==before+1 && Field<MotionPlayback>(p,"playback").Reaction==kind,"Settling transform misroutes ear");
                }
                foreach(var point in new[]{new PointF(.5f,.24f),new PointF(.38f,.30f),new PointF(.62f,.30f),new PointF(.5f,.6f),new PointF(.02f,.02f)})
                {Reset(p,400,0);int before=p.Reactions;Click(p,At(p,point.X,point.Y));Check(p.Reactions==before,"Face/body/empty click reacts");}
                p.Close();
            }
            Console.WriteLine("EAR_CHECKS_PASS assertions="+count);return 0;
        }catch(Exception ex){Console.Error.WriteLine(ex);return 1;}
    }
}
