// Small contextual controls. No web runtime or custom input engine.
using System;
using System.Runtime.InteropServices;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Windows.Forms;

internal static class PetPalette
{
    internal static readonly Color Top = Color.FromArgb(24,21,31);
    internal static readonly Color Bottom = Color.FromArgb(40,29,49);
    internal static readonly Color Text = Color.FromArgb(246,243,250);
    internal static readonly Color Muted = Color.FromArgb(181,174,194);
    internal static readonly Color Hover = Color.FromArgb(53,43,65);
    internal static readonly Color Border = Color.FromArgb(49,43,59);
    internal static GraphicsPath Round(RectangleF rect, float radius)
    {
        GraphicsPath path = new GraphicsPath(); float d=radius*2;
        path.AddArc(rect.X,rect.Y,d,d,180,90); path.AddArc(rect.Right-d,rect.Y,d,d,270,90);
        path.AddArc(rect.Right-d,rect.Bottom-d,d,d,0,90); path.AddArc(rect.X,rect.Bottom-d,d,d,90,90);
        path.CloseFigure(); return path;
    }
    internal static void Panel(Graphics g, Rectangle rect, float radius)
    {
        g.SmoothingMode=SmoothingMode.AntiAlias;
        using(GraphicsPath path=Round(new RectangleF(.5f,.5f,rect.Width-1,rect.Height-1),radius))
        using(LinearGradientBrush fill=new LinearGradientBrush(rect,Top,Bottom,70f))
        using(Pen edge=new Pen(Border)) { g.FillPath(fill,path); g.DrawPath(edge,path); }
    }
}

internal sealed class PetMenuRenderer : ToolStripProfessionalRenderer
{
    internal PetMenuRenderer() { RoundedEdges=false; }
    protected override void OnRenderToolStripBackground(ToolStripRenderEventArgs e)
    {
        using(LinearGradientBrush fill=new LinearGradientBrush(e.AffectedBounds,PetPalette.Top,PetPalette.Bottom,70f))
            e.Graphics.FillRectangle(fill,e.AffectedBounds);
    }
    protected override void OnRenderImageMargin(ToolStripRenderEventArgs e) { }
    protected override void OnRenderToolStripBorder(ToolStripRenderEventArgs e)
    {
        using(Pen pen=new Pen(PetPalette.Border)) e.Graphics.DrawRectangle(pen,0,0,e.ToolStrip.Width-1,e.ToolStrip.Height-1);
    }
    protected override void OnRenderMenuItemBackground(ToolStripItemRenderEventArgs e)
    {
        if(!e.Item.Selected || !e.Item.Enabled)return;
        e.Graphics.SmoothingMode=SmoothingMode.AntiAlias;
        using(GraphicsPath path=PetPalette.Round(new RectangleF(4,1,e.Item.Width-8,e.Item.Height-2),6))
        using(Brush fill=new SolidBrush(PetPalette.Hover))e.Graphics.FillPath(fill,path);
    }
    protected override void OnRenderItemText(ToolStripItemTextRenderEventArgs e)
    {
        e.TextColor=e.Item.Enabled?PetPalette.Text:PetPalette.Muted; base.OnRenderItemText(e);
    }
    protected override void OnRenderArrow(ToolStripArrowRenderEventArgs e) { e.ArrowColor=PetPalette.Muted; base.OnRenderArrow(e); }
    protected override void OnRenderSeparator(ToolStripSeparatorRenderEventArgs e)
    {
        using(Pen pen=new Pen(PetPalette.Border))e.Graphics.DrawLine(pen,14,e.Item.Height/2,e.Item.Width-14,e.Item.Height/2);
    }
    protected override void OnRenderItemCheck(ToolStripItemImageRenderEventArgs e)
    {
        Rectangle r=e.ImageRectangle;
        using(Pen pen=new Pen(PetPalette.Text,1.7f))
            e.Graphics.DrawLines(pen,new[]{new Point(r.Left+3,r.Top+r.Height/2),new Point(r.Left+6,r.Bottom-4),new Point(r.Right-2,r.Top+3)});
    }
}

// Native Button keeps keyboard, focus and accessibility semantics; only paint changes.
internal sealed class RemoteButton : Button
{
    private bool hover;
    internal bool Selected;
    internal string Symbol;
    internal RemoteButton()
    {
        SetStyle(ControlStyles.UserPaint|ControlStyles.AllPaintingInWmPaint|ControlStyles.OptimizedDoubleBuffer|ControlStyles.Opaque,true);
        BackColor=PetPalette.Top;ForeColor=PetPalette.Text;FlatStyle=FlatStyle.Flat;
        FlatAppearance.BorderSize=0;Cursor=Cursors.Hand;TabStop=true;AccessibleRole=AccessibleRole.PushButton;
    }
    protected override void OnMouseEnter(EventArgs e){hover=true;Invalidate();base.OnMouseEnter(e);}
    protected override void OnMouseLeave(EventArgs e){hover=false;Invalidate();base.OnMouseLeave(e);}
    protected override void OnPaintBackground(PaintEventArgs e) { }
    protected override void OnPaint(PaintEventArgs e)
    {
        Graphics g=e.Graphics;g.SmoothingMode=SmoothingMode.None;float s=Height/32f;
        // ButtonBase does not reliably erase a custom transparent button on each
        // native hover repaint. Own every pixel instead of reusing that buffer.
        if(Symbol==null)
        {using(Brush b=new SolidBrush(Color.FromArgb(20,17,26)))g.FillRectangle(b,ClientRectangle);}
        else
        {
            Rectangle surface=Parent==null?ClientRectangle:new Rectangle(-Left,-Top,Parent.Width,Parent.Height);
            using(LinearGradientBrush b=new LinearGradientBrush(surface,PetPalette.Top,PetPalette.Bottom,70f))g.FillRectangle(b,ClientRectangle);
        }
        g.SmoothingMode=SmoothingMode.AntiAlias;
        if(Selected || hover)
            using(GraphicsPath p=PetPalette.Round(new RectangleF(1,1,Width-2,Height-2),6*s))
            using(Brush b=new SolidBrush(Selected?Color.FromArgb(66,54,79):PetPalette.Hover))g.FillPath(b,p);
        Color ink=Enabled?ForeColor:PetPalette.Muted;
        Rectangle text=ClientRectangle;
        if(Symbol!=null)
        {
            GraphicsState state=g.Save();g.TranslateTransform(8*s,(Height-18*s)/2);g.ScaleTransform(s,s);
            using(Pen pen=new Pen(ink,1.2f){StartCap=LineCap.Round,EndCap=LineCap.Round,LineJoin=LineJoin.Round})
            {
                if(Symbol=="close"){g.DrawLine(pen,5,5,13,13);g.DrawLine(pen,13,5,5,13);}
                else if(Symbol=="exit"){g.DrawArc(pen,2,2,14,14,310,280);g.DrawLine(pen,9,0,9,9);}
                else using(GraphicsPath p=new GraphicsPath())
                {
                    p.AddBezier(1,9,5,2,13,2,17,9);p.AddBezier(17,9,13,16,5,16,1,9);g.DrawPath(pen,p);
                    g.DrawEllipse(pen,6.5f,6.5f,5,5);if(Symbol=="hide")g.DrawLine(pen,1,1,17,17);
                }
            }
            g.Restore(state);text.X=(int)(34*s);text.Width-=text.X;
        }
        TextRenderer.DrawText(g,Text,Font,text,ink,TextFormatFlags.VerticalCenter|TextFormatFlags.NoPadding|TextFormatFlags.PreserveGraphicsClipping|TextFormatFlags.PreserveGraphicsTranslateTransform|
            (Symbol==null?TextFormatFlags.HorizontalCenter:TextFormatFlags.Left));
        if(Focused && ShowFocusCues)
            using(GraphicsPath p=PetPalette.Round(new RectangleF(2,2,Width-5,Height-5),5*s))
            using(Pen pen=new Pen(Color.FromArgb(197,178,227)))g.DrawPath(pen,p);
    }
}

internal static class StitchIcon
{
    [DllImport("user32.dll")] private static extern bool DestroyIcon(IntPtr handle);
    internal static void DrawFace(Graphics g,Image source,RectangleF target)
    {
        float h=target.Width*164f/292f;
        g.DrawImage(source,new RectangleF(target.X,target.Y+(target.Height-h)/2,target.Width,h),
            new RectangleF(source.Width*55f/400,source.Height*30f/400,source.Width*292f/400,source.Height*164f/400),GraphicsUnit.Pixel);
    }
    internal static Icon Create(Image source)
    {
        int size=Math.Max(16,SystemInformation.SmallIconSize.Width);
        using(Bitmap b=new Bitmap(size,size))
        {
            using(Graphics g=Graphics.FromImage(b)){g.InterpolationMode=InterpolationMode.HighQualityBicubic;DrawFace(g,source,new RectangleF(0,0,size,size));}
            IntPtr h=b.GetHicon();
            try{using(Icon borrowed=Icon.FromHandle(h))return (Icon)borrowed.Clone();}
            finally{DestroyIcon(h);}
        }
    }
}

internal sealed class RemotePanel : Form
{
    private readonly PetWindow pet;
    private readonly Image face; // Borrowed from the pet; disposed by the pet after this form.
    private readonly float scale;
    private readonly Font titleFont,labelFont;
    internal readonly RemoteButton[] SizeButtons=new RemoteButton[3];
    internal readonly RemoteButton VisibilityButton=new RemoteButton(),ExitButton=new RemoteButton(),DismissButton=new RemoteButton();
    internal event Action DismissedByDeactivation;
    internal RemotePanel(PetWindow owner,Image source)
    {
        pet=owner;face=source;
        FormBorderStyle=FormBorderStyle.None;ShowInTaskbar=false;TopMost=true;StartPosition=FormStartPosition.Manual;
        AutoScaleMode=AutoScaleMode.None;Text="Stitch kontrolleri";AccessibleName=Text;BackColor=PetPalette.Top;
        using(Graphics g=Graphics.FromHwnd(IntPtr.Zero))scale=g.DpiX/96f;
        ClientSize=new Size(Px(312),Px(220));Font=new Font("Segoe UI",9.75f);
        titleFont=new Font("Segoe UI",14.25f,FontStyle.Bold);labelFont=new Font("Segoe UI",9f);
        SetStyle(ControlStyles.AllPaintingInWmPaint|ControlStyles.OptimizedDoubleBuffer,true);
        string[] labels={"Küçük","Orta","Büyük"};int[] sizes={240,320,400};
        for(int i=0;i<3;i++)
        {
            int value=sizes[i];RemoteButton b=new RemoteButton();b.Text=labels[i];b.AccessibleName="Boyut: "+labels[i];b.TabIndex=i;
            b.Click+=delegate{pet.SetSize(value);RefreshState();};SizeButtons[i]=b;Add(b,19+i*92,105,90,32);
        }
        VisibilityButton.TabIndex=3;VisibilityButton.Click+=delegate{Hide();if(pet.Visible)pet.HidePet();else pet.ShowPet();};Add(VisibilityButton,16,172,124,32);
        ExitButton.Text="Çıkış";ExitButton.AccessibleName="Stitch'ten çık";ExitButton.Symbol="exit";ExitButton.ForeColor=PetPalette.Muted;
        ExitButton.TabIndex=4;ExitButton.Click+=delegate{pet.Close();};Add(ExitButton,216,172,80,32);
        DismissButton.Symbol="close";DismissButton.AccessibleName="Paneli kapat";DismissButton.TabIndex=5;
        DismissButton.Click+=delegate{Hide();};Add(DismissButton,264,14,32,32);
        using(GraphicsPath p=PetPalette.Round(new RectangleF(0,0,Width,Height),16*scale))Region=new Region(p);
        RefreshState();
    }
    private int Px(float value){return (int)Math.Round(value*scale);}
    private void Add(Control control,int x,int y,int w,int h){control.SetBounds(Px(x),Px(y),Px(w),Px(h));Controls.Add(control);}
    internal void RefreshState()
    {
        VisibilityButton.Text=pet.Visible?"Gizle":"Göster";VisibilityButton.AccessibleName="Stitch'i "+VisibilityButton.Text;
        VisibilityButton.Symbol=pet.Visible?"hide":"show";
        int[] sizes={240,320,400};
        for(int i=0;i<3;i++)
        {
            SizeButtons[i].Selected=pet.CharacterSize==sizes[i];
            SizeButtons[i].AccessibleDescription=SizeButtons[i].Selected?"Seçili boyut":"";SizeButtons[i].Invalidate();
        }
        VisibilityButton.Invalidate();Invalidate();
    }
    protected override CreateParams CreateParams
    {get{CreateParams p=base.CreateParams;p.ExStyle|=0x80;p.ClassStyle|=0x00020000;return p;}}
    protected override void OnPaintBackground(PaintEventArgs e)
    {
        Graphics g=e.Graphics;PetPalette.Panel(g,ClientRectangle,16*scale);
        g.InterpolationMode=InterpolationMode.HighQualityBicubic;
        StitchIcon.DrawFace(g,face,new RectangleF(Px(20),Px(18),Px(38),Px(38)));
        TextRenderer.DrawText(g,"Stitch",titleFont,new Point(Px(70),Px(18)),PetPalette.Text,TextFormatFlags.NoPadding|TextFormatFlags.PreserveGraphicsClipping|TextFormatFlags.PreserveGraphicsTranslateTransform);
        TextRenderer.DrawText(g,pet.Visible?"Masaüstünde":"Gizli",labelFont,new Point(Px(70),Px(45)),PetPalette.Muted,TextFormatFlags.NoPadding|TextFormatFlags.PreserveGraphicsClipping|TextFormatFlags.PreserveGraphicsTranslateTransform);
        TextRenderer.DrawText(g,"Boyut",labelFont,new Point(Px(20),Px(80)),PetPalette.Muted,TextFormatFlags.NoPadding|TextFormatFlags.PreserveGraphicsClipping|TextFormatFlags.PreserveGraphicsTranslateTransform);
        using(GraphicsPath p=PetPalette.Round(new RectangleF(Px(16),Px(102),Px(280),Px(38)),8*scale))
        using(Brush b=new SolidBrush(Color.FromArgb(20,17,26)))g.FillPath(b,p);
        using(Pen p=new Pen(PetPalette.Border))g.DrawLine(p,Px(20),Px(160),Px(292),Px(160));
    }
    protected override void OnDeactivate(EventArgs e)
    {
        base.OnDeactivate(e);
        if(Visible){Hide();if(DismissedByDeactivation!=null)DismissedByDeactivation();}
    }
    protected override bool ProcessCmdKey(ref Message msg,Keys keyData)
    {if(keyData==Keys.Escape){Hide();return true;}return base.ProcessCmdKey(ref msg,keyData);}
    protected override void OnFormClosing(FormClosingEventArgs e)
    {if(e.CloseReason==CloseReason.UserClosing){e.Cancel=true;Hide();}base.OnFormClosing(e);}
    protected override void Dispose(bool disposing)
    {
        if(disposing){titleFont.Dispose();labelFont.Dispose();Font.Dispose();if(Region!=null)Region.Dispose();}
        base.Dispose(disposing);
    }
}

internal sealed class CompanionUi : IDisposable
{
    internal readonly RemotePanel Panel;
    private DateTime dismissedAt=DateTime.MinValue;
    internal CompanionUi(PetWindow owner,Image face)
    {
        Panel=new RemotePanel(owner,face);
        Panel.DismissedByDeactivation+=delegate{dismissedAt=DateTime.UtcNow;};
    }
    internal void Toggle(Point anchor)
    {
        if(Panel.Visible){Panel.Hide();return;}
        // Clicking the same tray icon first deactivates this form. Do not reopen it
        // on that click's mouse-up. A later intentional click opens it normally.
        if((DateTime.UtcNow-dismissedAt).TotalMilliseconds<200)return;
        Panel.RefreshState();Panel.Location=PlaceInWorkArea(anchor,Panel.Size,Screen.FromPoint(anchor).WorkingArea);
        // Independent of the pet's visibility/ownership. Explicit tray click may activate.
        Panel.Show();Panel.Activate();Panel.SizeButtons[0].Select();
    }
    internal void Hide(){Panel.Hide();}
    internal void RefreshState(){Panel.RefreshState();}
    internal static Point PlaceInWorkArea(Point anchor,Size panel,Rectangle area)
    {
        int x=anchor.X-panel.Width+24,y=anchor.Y-panel.Height-12;
        if(y<area.Top+8)y=anchor.Y+12;
        return new Point(Math.Max(area.Left+8,Math.Min(x,area.Right-panel.Width-8)),
            Math.Max(area.Top+8,Math.Min(y,area.Bottom-panel.Height-8)));
    }
    public void Dispose(){Panel.Dispose();}
}
