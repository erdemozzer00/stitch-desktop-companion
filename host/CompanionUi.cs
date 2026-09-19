// Small contextual controls. No web runtime or custom input engine.
using System;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Windows.Forms;

internal static class PetPalette
{
    internal static readonly Color Top = Color.FromArgb(31,24,44);
    internal static readonly Color Bottom = Color.FromArgb(48,32,61);
    internal static readonly Color Text = Color.FromArgb(248,245,252);
    internal static readonly Color Muted = Color.FromArgb(198,187,210);
    internal static readonly Color Hover = Color.FromArgb(72,52,88);
    internal static readonly Color Border = Color.FromArgb(91,72,108);
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

internal sealed class PetCommandButton : Button
{
    private bool hover;
    internal bool More;
    internal PetCommandButton()
    {
        SetStyle(ControlStyles.UserPaint|ControlStyles.AllPaintingInWmPaint|ControlStyles.OptimizedDoubleBuffer|ControlStyles.SupportsTransparentBackColor,true);
        BackColor=Color.Transparent; ForeColor=PetPalette.Text; FlatStyle=FlatStyle.Flat;
        FlatAppearance.BorderSize=0; Cursor=Cursors.Hand; TabStop=true;
        AccessibleRole=AccessibleRole.PushButton;
    }
    protected override void OnMouseEnter(EventArgs e) { hover=true; Invalidate(); base.OnMouseEnter(e); }
    protected override void OnMouseLeave(EventArgs e) { hover=false; Invalidate(); base.OnMouseLeave(e); }
    protected override void OnPaint(PaintEventArgs e)
    {
        e.Graphics.SmoothingMode=SmoothingMode.AntiAlias;
        if((hover || Focused) && Enabled)
        using(GraphicsPath path=PetPalette.Round(new RectangleF(1,1,Width-2,Height-2),9))
        using(Brush fill=new SolidBrush(PetPalette.Hover))e.Graphics.FillPath(fill,path);
        Color ink=Enabled?PetPalette.Text:PetPalette.Muted;
        if(More)
        {
            using(Brush fill=new SolidBrush(ink))for(int i=-1;i<=1;i++)e.Graphics.FillEllipse(fill,Width/2f+i*7-1.5f,Height/2f-1.5f,3,3);
        }
        else TextRenderer.DrawText(e.Graphics,Text,Font,ClientRectangle,ink,TextFormatFlags.HorizontalCenter|TextFormatFlags.VerticalCenter|TextFormatFlags.NoPadding);
        if(Focused && ShowFocusCues)ControlPaint.DrawFocusRectangle(e.Graphics,Rectangle.Inflate(ClientRectangle,-4,-4),ink,PetPalette.Top);
    }
}

internal sealed class CommandBar : Form
{
    internal readonly PetCommandButton Wave=new PetCommandButton(), More=new PetCommandButton();
    private readonly ToolTip tips=new ToolTip();
    internal CommandBar(Action wave, Action more)
    {
        FormBorderStyle=FormBorderStyle.None; ShowInTaskbar=false; TopMost=true;
        StartPosition=FormStartPosition.Manual; AutoScaleMode=AutoScaleMode.None;
        BackColor=PetPalette.Top; Text="Stitch kontrolleri"; AccessibleName=Text;
        float scale;
        using(Graphics g=Graphics.FromHwnd(IntPtr.Zero))scale=g.DpiX/96f;
        ClientSize=new Size((int)Math.Round(180*scale),(int)Math.Round(46*scale));
        Font=new Font("Segoe UI",10f,FontStyle.Regular);
        Wave.Text="El salla"; Wave.AccessibleName="Stitch el sallasın"; Wave.TabIndex=0;
        More.More=true; More.AccessibleName="Stitch seçenekleri"; More.TabIndex=1;
        Wave.SetBounds((int)(5*scale),(int)(5*scale),(int)(120*scale),Height-(int)(10*scale));
        More.SetBounds((int)(130*scale),(int)(5*scale),Width-(int)(135*scale),Height-(int)(10*scale));
        Wave.Click+=delegate{wave();}; More.Click+=delegate{more();};
        Controls.Add(Wave); Controls.Add(More);
        tips.SetToolTip(More,"Boyut, gizle ve çıkış");
        using(GraphicsPath path=PetPalette.Round(new RectangleF(0,0,Width,Height),15*scale))Region=new Region(path);
        SetStyle(ControlStyles.AllPaintingInWmPaint|ControlStyles.OptimizedDoubleBuffer,true);
    }
    protected override bool ShowWithoutActivation { get { return true; } }
    protected override CreateParams CreateParams { get { CreateParams p=base.CreateParams;p.ExStyle|=0x80;return p; } }
    protected override void OnPaintBackground(PaintEventArgs e) { PetPalette.Panel(e.Graphics,ClientRectangle,15*Width/180f); }
    protected override bool ProcessCmdKey(ref Message msg,Keys keyData)
    {
        if(keyData==Keys.Escape){Hide();return true;}return base.ProcessCmdKey(ref msg,keyData);
    }
    protected override void Dispose(bool disposing)
    {
        if(disposing) { tips.Dispose(); Font.Dispose(); if(Region!=null)Region.Dispose(); }
        base.Dispose(disposing);
    }
}

internal sealed class CompanionUi : IDisposable
{
    private readonly PetWindow pet;
    private readonly ContextMenuStrip menu;
    internal readonly CommandBar Bar;
    private readonly Timer timer=new Timer();
    private readonly Stopwatch clock=Stopwatch.StartNew();
    private double keepUntil;
    internal CompanionUi(PetWindow owner, ContextMenuStrip options)
    {
        pet=owner;menu=options;
        Bar=new CommandBar(pet.React,delegate{pet.ShowOptions(new Point(Bar.Left,Bar.Bottom+5));});
        timer.Interval=100;timer.Tick+=delegate{Update();};timer.Start();
    }
    internal void Reveal()
    {
        if(!pet.Visible || pet.PointerBusy)return;
        keepUntil=clock.Elapsed.TotalSeconds+.8; Place(); if(!Bar.Visible)Bar.Show(pet);
    }
    internal void Welcome() { Reveal(); keepUntil=clock.Elapsed.TotalSeconds+3; }
    internal void Hide() { Bar.Hide(); }
    internal static Point PlaceInWorkArea(Rectangle character,Size bar,Rectangle area)
    {
        int x=character.Left+(character.Width-bar.Width)/2;
        int y=character.Bottom+6;
        if(y+bar.Height>area.Bottom-8)y=character.Top-bar.Height-6;
        return new Point(Math.Max(area.Left+8,Math.Min(x,area.Right-bar.Width-8)),
            Math.Max(area.Top+8,Math.Min(y,area.Bottom-bar.Height-8)));
    }
    private void Place()
    {
        Rectangle body=pet.CharacterBounds;
        // The sprite canvas has a transparent footer; use the visible feet band.
        body.Height=(int)Math.Ceiling(body.Height*.94);
        Bar.Location=PlaceInWorkArea(body,Bar.Size,Screen.FromRectangle(body).WorkingArea);
    }
    private void Update()
    {
        if(!pet.Visible || pet.PointerBusy) { Bar.Hide(); return; }
        Bar.Wave.Enabled=pet.CanReact;
        if(!Bar.Visible)return;
        Place();
        Rectangle bridge=Rectangle.Union(pet.CharacterBounds,Bar.Bounds);
        bridge.Inflate(6,6);
        if(menu.Visible || Bar.ContainsFocus || bridge.Contains(Cursor.Position))keepUntil=clock.Elapsed.TotalSeconds+.8;
        if(clock.Elapsed.TotalSeconds>keepUntil)Bar.Hide();
    }
    public void Dispose() { timer.Stop();timer.Dispose();Bar.Dispose(); }
}
