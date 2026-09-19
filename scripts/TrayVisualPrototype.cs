// Static design review only. No host reference, message loop, tray or input handlers.
using System;
using System.IO;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Drawing.Text;

internal static class TrayVisualPrototype
{
    static readonly Color White = Color.FromArgb(246,243,250);
    static readonly Color Muted = Color.FromArgb(181,174,194);
    static Image stitch;
    static Color C(int r,int g,int b) { return Color.FromArgb(r,g,b); }
    static GraphicsPath Round(float x,float y,float w,float h,float r)
    {
        var p=new GraphicsPath(); float d=r*2;
        p.AddArc(x,y,d,d,180,90); p.AddArc(x+w-d,y,d,d,270,90);
        p.AddArc(x+w-d,y+h-d,d,d,0,90); p.AddArc(x,y+h-d,d,d,90,90); p.CloseFigure(); return p;
    }
    static void Box(Graphics g,float x,float y,float w,float h,float r,Color fill)
    { using(var p=Round(x,y,w,h,r))using(var b=new SolidBrush(fill))g.FillPath(b,p); }
    static void Text(Graphics g,string s,float x,float y,float size,Color ink,bool bold=false)
    {
        using(var f=new Font("Segoe UI",size,bold?FontStyle.Bold:FontStyle.Regular,GraphicsUnit.Pixel))
        using(var b=new SolidBrush(ink))g.DrawString(s,f,b,x,y,StringFormat.GenericTypographic);
    }
    static void Center(Graphics g,string s,RectangleF r,float size,Color ink)
    {
        using(var f=new Font("Segoe UI",size,FontStyle.Regular,GraphicsUnit.Pixel))
        using(var b=new SolidBrush(ink))using(var sf=new StringFormat { Alignment=StringAlignment.Center,LineAlignment=StringAlignment.Center })
            g.DrawString(s,f,b,r,sf);
    }
    static void Line(Graphics g,Color c,float x,float y,float xx,float yy,float width=1)
    { using(var p=new Pen(c,width) { StartCap=LineCap.Round,EndCap=LineCap.Round })g.DrawLine(p,x,y,xx,yy); }
    static void Glyph(Graphics g,string s,float x,float y,float size,Color ink)
    {
        using(var f=new Font("Segoe MDL2 Assets",size,FontStyle.Regular,GraphicsUnit.Pixel))
        using(var b=new SolidBrush(ink))g.DrawString(s,f,b,x,y,StringFormat.GenericTypographic);
    }
    static void Face(Graphics g,float x,float y,float size)
    {
        // Aspect-preserving viewport of the accepted frame; source PNG is never modified.
        float h=size*164f/292f;
        g.DrawImage(stitch,new RectangleF(x,y+(size-h)/2,size,h),new RectangleF(55,30,292,164),GraphicsUnit.Pixel);
    }
    static void ActionIcon(Graphics g,string kind,float x,float y,Color ink)
    {
        var state=g.Save();g.TranslateTransform(x,y);
        using(var pen=new Pen(ink,1.25f) { StartCap=LineCap.Round,EndCap=LineCap.Round,LineJoin=LineJoin.Round })
        using(var p=new GraphicsPath())
        {
            p.AddBezier(1,9,5,2,13,2,17,9);p.AddBezier(17,9,13,16,5,16,1,9);g.DrawPath(pen,p);
            g.DrawEllipse(pen,6.5f,6.5f,5,5);
            if(kind=="hide")g.DrawLine(pen,1,1,17,17);
        }
        g.Restore(state);
    }
    static void Panel(Graphics g,float x,float y,bool hidden=false)
    {
        var state=g.Save(); g.TranslateTransform(x,y);
        for(int i=14;i>0;i--)
            Box(g,-i/2f,4-i/3f,312+i,220+i/1.5f,16+i/3f,Color.FromArgb(3,0,0,0));
        using(var p=Round(.5f,.5f,311,219,16))
        using(var b=new LinearGradientBrush(new Rectangle(0,0,312,220),C(24,21,31),C(40,29,49),65f))
        using(var edge=new Pen(Color.FromArgb(30,230,222,247))) { g.FillPath(b,p);g.DrawPath(edge,p); }
        Face(g,20,18,38); Text(g,"Stitch",70,20,19,White,true);
        Text(g,hidden?"Gizli":"Masaüstünde",70,45,12,Muted);
        Line(g,Muted,278,26,286,34);Line(g,Muted,286,26,278,34);
        Text(g,"Boyut",20,80,12,Muted);
        Box(g,16,102,280,38,8,C(20,17,26));
        Box(g,19,105,90,32,6,C(66,54,79));
        Center(g,"Küçük",new RectangleF(19,105,90,32),13,White);
        Center(g,"Orta",new RectangleF(111,105,90,32),13,Muted);
        Center(g,"Büyük",new RectangleF(203,105,90,32),13,Muted);
        Line(g,Color.FromArgb(24,230,222,247),20,160,292,160);
        ActionIcon(g,hidden?"show":"hide",24,179,White);
        Text(g,hidden?"Göster":"Gizle",51,179,13,White);
        Glyph(g,"\uE7E8",225,181,16,Muted);Text(g,"Çıkış",249,179,13,Muted);
        g.Restore(state);
    }
    static Bitmap Canvas(int w,int h,out Graphics g)
    {
        var b=new Bitmap(w,h,PixelFormat.Format32bppArgb); g=Graphics.FromImage(b);
        g.SmoothingMode=SmoothingMode.AntiAlias;g.InterpolationMode=InterpolationMode.HighQualityBicubic;
        g.PixelOffsetMode=PixelOffsetMode.HighQuality;g.TextRenderingHint=TextRenderingHint.AntiAliasGridFit;return b;
    }
    static void Desktop(string path,bool open)
    {
        Graphics g;using(var b=Canvas(1280,800,out g))using(g)
        {
            using(var bg=new LinearGradientBrush(new Rectangle(0,0,1280,800),C(26,29,39),C(44,39,54),30f))g.FillRectangle(bg,0,0,1280,800);
            Text(g,"STITCH / KONTROL PANELİ",56,48,12,Muted);
            Text(g,open?"Kontroller bir tık uzağında.":"Sadece Stitch.",56,79,32,White,true);
            Text(g,open?"Tray ikonuna tıkla. Panelden yönet.":"Panel kapalıyken masaüstünde yalnızca karakter kalır.",58,128,15,Muted);
            Text(g,"GÖRSEL PROTOTİP · UYGULAMAYA ENTEGRE EDİLMEDİ",58,169,10,Muted);
            g.DrawImage(stitch,new Rectangle(228,420,280,280));
            if(open)Panel(g,932,516);
            using(var bar=new SolidBrush(C(20,20,24)))g.FillRectangle(bar,0,752,1280,48);
            Glyph(g,"\uE70E",1063,770,12,Muted);
            if(open)Box(g,1092,757,40,38,6,C(48,43,56));
            Face(g,1099,765,26);
            Glyph(g,"\uE839",1143,769,16,Muted);Text(g,"21:08",1195,759,12,White);Text(g,"19.09.2026",1174,778,11,Muted);
            b.Save(path,ImageFormat.Png);
        }
    }
    static void Main(string[] args)
    {
        Directory.CreateDirectory(args[1]);
        using(stitch=Image.FromFile(args[0]))
        {
            Desktop(Path.Combine(args[1],"desktop-open.png"),true);
            Desktop(Path.Combine(args[1],"desktop-closed.png"),false);
            Graphics g;using(var b=Canvas(1408,604,out g))using(g)
            {
                g.Clear(C(18,18,24));g.ScaleTransform(2,2);
                Text(g,"GÖRÜNÜR",26,16,10,Muted);Text(g,"GİZLİ",374,16,10,Muted);
                Panel(g,22,48,false);Panel(g,370,48,true);
                b.Save(Path.Combine(args[1],"panel-states-2x.png"),ImageFormat.Png);
            }
            using(var b=Canvas(720,176,out g))using(g)
            {
                g.Clear(C(24,24,29));Text(g,"TRAY İKONU / GERÇEK PİKSEL BOYUTLARI",24,20,12,Muted);
                int x=32;foreach(int size in new[]{16,20,24,32})
                { Face(g,x,64,size);Text(g,size+" px",x,110,12,Muted);x+=90; }
                using(var light=new SolidBrush(C(237,237,240)))g.FillRectangle(light,404,52,284,94);
                x=424;foreach(int size in new[]{16,20,24,32}){Face(g,x,74,size);x+=65;}
                b.Save(Path.Combine(args[1],"tray-icon-sizes.png"),ImageFormat.Png);
            }
        }
        Console.WriteLine("Static prototype rendered. No running application was modified.");
    }
}
