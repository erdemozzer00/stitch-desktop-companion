// Local motion-review host. No startup registration or shell embedding.
using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.IO;
using System.Runtime.InteropServices;
using System.Windows.Forms;

internal static class Program
{
    [STAThread]
    private static void Main(string[] args)
    {
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);
        string root = AppDomain.CurrentDomain.BaseDirectory;
        string assets = Path.Combine(root, "assets");
        string carry = Directory.Exists(Path.Combine(root,"carry"))?Path.Combine(root,"carry"):null;
        bool probe = false, preview = false;
        foreach (string arg in args)
        {
            if (arg.StartsWith("--assets=")) assets = Path.GetFullPath(arg.Substring(9));
            if (arg == "--probe") probe = true;
            if (arg == "--preview") preview = true;
            if (arg.StartsWith("--carry=")) carry = Path.GetFullPath(arg.Substring(8));
        }
        try
        {
            string identity="Local\\StitchCompanion-"+System.Security.Principal.WindowsIdentity.GetCurrent().User.Value;
            using(var request=new System.Threading.EventWaitHandle(false,System.Threading.EventResetMode.AutoReset,identity+"-show"))
            using(var singleton=new System.Threading.Mutex(false,identity))
            {
                bool acquired;
                try{acquired=singleton.WaitOne(0);}catch(System.Threading.AbandonedMutexException){acquired=true;}
                if(!acquired){request.Set();return;}
                try
                {
            using (PetWindow pet = new PetWindow(assets, root, true, carry))
            using (Timer activation=new Timer())
            {
                activation.Interval=200;
                activation.Tick+=delegate{if(request.WaitOne(0)){pet.ShowPet();}};
                activation.Start();
                if (probe) pet.Shown += delegate { new ProbeWindow(pet).Show(); };
                if (preview) pet.Shown += delegate { pet.React(); };
                Application.Run(pet);
            }
                }
                finally{singleton.ReleaseMutex();}
            }
        }
        catch (Exception error)
        {
            File.AppendAllText(Path.Combine(root, "failure.log"), error + Environment.NewLine);
            MessageBox.Show(error.Message, "Stitch prototype could not start");
        }
    }
}

internal sealed class PetWindow : Form
{
    private readonly string statePath, logPath;
    private readonly Bitmap[] idle;
    private readonly Bitmap[] wave;
    private readonly Bitmap[] peace;
    private readonly Bitmap[] earLeft, earRight;
    private readonly Bitmap[] smile;
    private readonly NoseRegions nose;
    private readonly EarRegions ears;
    private readonly HandRegions hands;
    private ReactionKind pressedReaction;
    private readonly Bitmap[][] entries = new Bitmap[24][];
    private readonly MotionPlayback playback = new MotionPlayback();
    private readonly Timer timer = new Timer();
    private readonly Stopwatch clock = new Stopwatch();
    private readonly NotifyIcon tray;
    private readonly Icon trayIcon;
    private readonly ContextMenuStrip menu;
    private readonly CompanionUi controls;
    private ToolStripMenuItem hideCommand, showCommand;
    private readonly ToolStripMenuItem[] sizeCommands = new ToolStripMenuItem[3];
    private bool pressed, dragging, resourcesDisposed;
    private Point pointerStart, windowStart;
    private int side = 320;
    private Bitmap presented;
    private readonly CarryBank carryBank;
    private readonly CarryResponse carry = new CarryResponse();
    private PointF lastCarryOffset;
    private double lastCarryAngle = Double.NaN;
    internal int CharacterSize { get { return side; } }
    internal int ContentPadding { get { return carryBank == null ? 0 : CarrySurface.Padding(side); } }
    internal bool CarryEnabled { get { return carryBank != null; } }
    internal bool PointerBusy { get { return pressed || dragging; } }
    internal bool CanReact { get { return Visible && !dragging && !carry.Held && !playback.CarryReady && !playback.Reacting; } }
    internal Rectangle CharacterBounds { get { return new Rectangle(Left+ContentPadding,Top+ContentPadding,side,side); } }
    internal RemotePanel TrayPanel { get { return controls==null?null:controls.Panel; } }
    internal bool TrayVisible { get { return tray!=null && tray.Visible; } }
    internal void ToggleRemote(Point anchor) { if(controls!=null){controls.Toggle(anchor);Log("remote visible=" + TrayPanel.Visible);} }
    internal ContextMenuStrip OptionsMenu { get { return menu; } }
    internal bool ManualTicks { get; set; } // Direct-method smoke; ordinary launches use the timer.
    public int Reactions { get; private set; }
    public event Action Changed;

    public PetWindow(string assets, string output, bool createTray = true, string carryDirectory = null)
    {
        statePath = Path.Combine(output, "position.txt");
        logPath = Path.Combine(output, "events.log");
        idle = ReadClip(assets, "idle_", 96);
        wave = ReadClip(assets, "wave_", 45);
        // Old asset banks remain usable for the frozen baseline and comparisons.
        // A partially installed new bank must fail instead of silently changing input.
        if (File.Exists(Path.Combine(assets,"hands.csv")) || Directory.GetFiles(assets,"peace_*.png").Length!=0)
        {
            hands = new HandRegions(Path.Combine(assets,"hands.csv"));
            peace = ReadClip(assets,"peace_",60);
        }
        if (File.Exists(Path.Combine(assets,"ears.csv")) || Directory.GetFiles(assets,"ear_*.png").Length!=0)
        {
            if(hands==null) throw new InvalidDataException("Ear assets require hand assets.");
            ears = new EarRegions(Path.Combine(assets,"ears.csv"));
            earLeft = ReadClip(assets,"ear_left_",16);
            earRight = ReadClip(assets,"ear_right_",16);
        }
        if (File.Exists(Path.Combine(assets,"nose.csv")) || Directory.GetFiles(assets,"smile_*.png").Length!=0)
        {
            if(hands==null) throw new InvalidDataException("Smile assets require hand assets.");
            nose = new NoseRegions(Path.Combine(assets,"nose.csv"));
            smile = ReadClip(assets,"smile_",28);
        }
        for (int i = 0; i < entries.Length; i++) entries[i] = ReadClip(assets, "entry_" + i.ToString("00") + "_", 4);
        if (carryDirectory != null) carryBank = new CarryBank(carryDirectory);
        Text = "Stitch";
        AccessibleName = "Stitch masaüstü arkadaşı";
        FormBorderStyle = FormBorderStyle.None;
        ShowInTaskbar = false;
        StartPosition = FormStartPosition.Manual;
        TopMost = true;
        AutoScaleMode = AutoScaleMode.None;
        UpdateCanvasSize();
        Location = new Point(Screen.PrimaryScreen.WorkingArea.Right - side - ContentPadding - 40,
                             Screen.PrimaryScreen.WorkingArea.Bottom - side - ContentPadding - 40);
        LoadPosition();
        menu = new ContextMenuStrip();
        menu.Renderer=new PetMenuRenderer(); menu.Font=new Font("Segoe UI",10f);
        menu.BackColor=PetPalette.Top; menu.ForeColor=PetPalette.Text; menu.Padding=new Padding(5);
        menu.MinimumSize=new Size(188,0); menu.AccessibleName="Stitch seçenekleri";
        ToolStripMenuItem sizes=new ToolStripMenuItem("Boyut");
        string[] labels={"Küçük","Orta","Büyük"}; int[] values={240,320,400};
        for(int i=0;i<3;i++)
        {
            int selectedSize=values[i];
            sizeCommands[i]=new ToolStripMenuItem(labels[i],null,delegate{SetSize(selectedSize);});
            sizeCommands[i].Padding=new Padding(6,5,6,5); sizes.DropDownItems.Add(sizeCommands[i]);
        }
        sizes.DropDown.Renderer=menu.Renderer; sizes.DropDown.Font=menu.Font;
        sizes.DropDown.Padding=new Padding(5); menu.Items.Add(sizes);
        hideCommand=(ToolStripMenuItem)menu.Items.Add("Gizle", null, delegate { HidePet(); });
        showCommand=(ToolStripMenuItem)menu.Items.Add("Göster", null, delegate { ShowPet(); });
        menu.Items.Add(new ToolStripSeparator());
        menu.Items.Add("Çıkış", null, delegate { Close(); });
        foreach(ToolStripItem item in menu.Items)if(!(item is ToolStripSeparator))item.Padding=new Padding(6,6,12,6);
        menu.Opening+=delegate{PrepareMenu();};
        if (createTray)
        {
            controls=new CompanionUi(this,idle[0]);
            trayIcon=StitchIcon.Create(idle[0]);
            tray = new NotifyIcon { Icon = trayIcon, Text = "Stitch — kontroller", ContextMenuStrip = menu, Visible = true };
            tray.MouseClick += delegate(object sender,MouseEventArgs e) { if(e.Button==MouseButtons.Left)ToggleRemote(Cursor.Position); };
        }
        timer.Interval = 15;
        timer.Tick += delegate { if (!ManualTicks) Advance(); };
        Shown += delegate { clock.Restart(); timer.Start(); Advance(); Log("launched motion=phase03-appearance-400 ui=tray-remote panel=" + (TrayPanel!=null && TrayPanel.Visible) + " carry=" + CarryEnabled + " idle=" + idle.Length + " wave=" + wave.Length + " size=" + side + " location=" + Location); };
        Log("environment os=" + Environment.OSVersion + " screens=" + Screen.AllScreens.Length);
    }

    private static Bitmap ReadBitmap(string path)
    {
        using (Image source = Image.FromFile(path)) return new Bitmap(source);
    }
    private static Bitmap[] ReadClip(string assets, string prefix, int count)
    {
        Bitmap[] result = new Bitmap[count];
        for (int i = 0; i < count; i++) result[i] = ReadBitmap(Path.Combine(assets, prefix + (i + 1).ToString("0000") + ".png"));
        return result;
    }
    protected override bool ShowWithoutActivation { get { return true; } }
    protected override CreateParams CreateParams
    {
        get
        {
            CreateParams value = base.CreateParams;
            // Layered + tool window + no activation. NOT WS_EX_TRANSPARENT:
            // Windows routes alpha-zero pixels through, while the pet stays clickable.
            value.ExStyle |= 0x00080000 | 0x00000080 | 0x08000000;
            return value;
        }
    }
    protected override void WndProc(ref Message message)
    {
        if (message.Msg == 0x0021) { message.Result = new IntPtr(3); return; } // MA_NOACTIVATE
        base.WndProc(ref message);
    }
    protected override void OnMouseDown(MouseEventArgs e)
    {
        base.OnMouseDown(e);
        if (e.Button != MouseButtons.Left) return;
        PointerDownAt(Cursor.Position);
        Capture = true;
        Log("pointer-down foreground=" + Native.GetForegroundWindow());
    }
    protected override void OnMouseMove(MouseEventArgs e)
    {
        base.OnMouseMove(e);
        PointerMoveAt(Cursor.Position);
    }
    // The real event handlers and direct-method checks share these input paths.
    internal void PointerDownAt(Point pointer)
    {
        // Capture intent from the displayed pose. Idle may move before mouse-up;
        // a press during another reaction must not become a queued greeting.
        pressedReaction = CanReact ? ReactionAt(pointer) : ReactionKind.None;
        pressed = true; dragging = false;
        if(controls!=null)controls.Hide();
        pointerStart = pointer; windowStart = Location;
    }
    internal void PointerMoveAt(Point pointer)
    {
        if (!pressed) return;
        int dx = pointer.X - pointerStart.X, dy = pointer.Y - pointerStart.Y;
        Size threshold = SystemInformation.DragSize;
        bool starting = !dragging && (Math.Abs(dx) >= threshold.Width / 2 || Math.Abs(dy) >= threshold.Height / 2);
        if (starting) { dragging = true; pressedReaction = ReactionKind.None; }
        if (!dragging) return;
        // Move first. Neither pose transitions nor response smoothing gate location.
        Location = new Point(windowStart.X + dx, windowStart.Y + dy);
        if (starting && carryBank != null)
        {
            double now = clock.Elapsed.TotalSeconds;
            PointF grip = new PointF((pointerStart.X-windowStart.X-ContentPadding)/(float)side,
                                    (pointerStart.Y-windowStart.Y-ContentPadding)/(float)side);
            carry.Begin(now, pointerStart, grip);
            playback.BeginCarry(now);
            Log("carry-start entry=" + (playback.EntryOnly ? "idle-bridge" : playback.Reacting ? "finish-wave" : "regrab"));
        }
    }
    protected override void OnMouseUp(MouseEventArgs e)
    {
        base.OnMouseUp(e);
        if (e.Button != MouseButtons.Left || !pressed) return;
        PointerUp();
    }
    internal void PointerUp()
    {
        if (!pressed) return;
        bool wasDrag = dragging;
        ReactionKind reaction = pressedReaction;
        pressedReaction = ReactionKind.None;
        pressed = false;
        dragging = false;
        Capture = false;
        if (wasDrag) { carry.Release(); ClampPosition(); SavePosition(); Log("drag-ended location=" + Location); }
        else React(reaction);
    }
    protected override void OnMouseCaptureChanged(EventArgs e)
    {
        base.OnMouseCaptureChanged(e);
        if (!Capture && pressed)
        {
            CancelPointer();
        }
    }
    internal void CancelPointer()
    {
        pressedReaction = ReactionKind.None;
        pressed = dragging = false; carry.Release();
        Capture = false;
        ClampPosition(); SavePosition(); Log("drag-cancelled");
    }
    private ReactionKind ReactionAt(Point pointer)
    {
        if (hands == null) return ReactionKind.Wave;
        double x=(pointer.X-Left-ContentPadding)/(double)side;
        double y=(pointer.Y-Top-ContentPadding)/(double)side;
        // Invert the displayed carry transform, including its residual settling.
        double c=Math.Cos(carry.Angle), s=Math.Sin(carry.Angle);
        double dx=x-carry.Pivot.X-carry.Offset.X, dy=y-carry.Pivot.Y-carry.Offset.Y;
        x=c*dx+s*dy+carry.Pivot.X; y=-s*dx+c*dy+carry.Pivot.Y;
        if(x<0 || y<0 || x>=1 || y>=1) return ReactionKind.None;
        Bitmap frame=idle[playback.IdleIndex];
        if(frame.GetPixel((int)(x*frame.Width),(int)(y*frame.Height)).A<8) return ReactionKind.None;
        PointF point=new PointF((float)x,(float)y);
        ReactionKind hand=hands.At(playback.IdleIndex,point);
        if(hand!=ReactionKind.None) return hand;
        ReactionKind ear=ears==null ? ReactionKind.None : ears.At(playback.IdleIndex,point);
        if(ear!=ReactionKind.None) return ear;
        return nose!=null && nose.Contains(playback.IdleIndex,point) ? ReactionKind.Smile : ReactionKind.None;
    }
    public void React() { React(ReactionKind.Wave); }
    private void React(ReactionKind reaction)
    {
        if(reaction==ReactionKind.None || (reaction==ReactionKind.Peace && peace==null)
            || (reaction==ReactionKind.EarLeft && earLeft==null) || (reaction==ReactionKind.EarRight && earRight==null)
            || (reaction==ReactionKind.Smile && smile==null)) return;
        if (!Visible) { Log("hidden-reaction-ignored"); return; }
        if (carry.Held || playback.CarryReady || dragging) { Log("held-reaction-ignored"); return; }
        if (!playback.React(clock.Elapsed.TotalSeconds,reaction)) { Log("repeat-click-ignored"); return; }
        Reactions++; Advance(); Log("reaction-start count=" + Reactions + " gesture=" + reaction + " entry=" + playback.EntryBucket);
    }
    private void Advance()
    {
        AdvanceAt(clock.Elapsed.TotalSeconds, Cursor.Position);
    }
    internal void AdvanceAt(double now, Point pointer)
    {
        bool wasCarrying = carry.Active;
        if (!(pressed && !dragging)) carry.Update(now, pointer, side);
        if (playback.CarryReady && carry.CanResumeIdle(side))
        {
            playback.EndCarry(now);
            Log("carry-visual-end idle-resumed");
        }
        if (wasCarrying && !carry.Active)
        {
            // Commit re-grab compensation to window position at rest. Resetting
            // the offset without this would jump the displayed character.
            Location = new Point(Left+(int)Math.Round(carry.Offset.X*side), Top+(int)Math.Round(carry.Offset.Y*side));
            carry.Offset = PointF.Empty;
            playback.EndCarry(now);
            ClampPosition(); SavePosition(); Log("carry-settled");
        }
        bool wasReacting = playback.Reacting;
        playback.Advance(now);
        Bitmap current = CurrentFrame();
        if (current != presented || carry.Angle != lastCarryAngle || carry.Offset != lastCarryOffset)
        {
            Present(current); presented = current; lastCarryAngle = carry.Angle; lastCarryOffset = carry.Offset;
        }
        if (wasReacting && !playback.Reacting) Log(playback.CarryReady ? "entry-end carry-ready" : "reaction-end idle-resumed");
    }
    public void SetSize(int value)
    {
        if (pressed) CancelPointer();
        int oldPadding = ContentPadding;
        side = Math.Max(160, Math.Min(480, value));
        UpdateCanvasSize();
        Location = new Point(Left+oldPadding-ContentPadding, Top+oldPadding-ContentPadding);
        ClampPosition(); Present(CurrentFrame()); SavePosition(); Log("size=" + side);
        if(controls!=null)controls.RefreshState();
    }
    public void HidePet()
    {
        pressedReaction = ReactionKind.None;
        if(controls!=null)controls.Hide();
        timer.Stop(); clock.Reset(); playback.Reset(); carry.Reset(); presented = null; pressed = dragging = false;
        Capture = false; Hide(); Log("hidden");
    }
    public void ShowPet() { ClampPosition(); Show(); clock.Start(); timer.Start(); Present(CurrentFrame()); if(controls!=null)controls.RefreshState(); Log("shown"); }
    private void PrepareMenu()
    {
        hideCommand.Visible=Visible; showCommand.Visible=!Visible;
        int[] sizes={240,320,400};for(int i=0;i<3;i++)sizeCommands[i].Checked=side==sizes[i];
    }
    internal void ShowOptions(Point position)
    {
        PrepareMenu();
        Rectangle area=Screen.FromPoint(position).WorkingArea;Size wanted=menu.GetPreferredSize(Size.Empty);
        position.X=Math.Max(area.Left,Math.Min(position.X,area.Right-wanted.Width));
        position.Y=Math.Max(area.Top,Math.Min(position.Y,area.Bottom-wanted.Height));
        menu.Show(position);
    }
    private Bitmap CurrentFrame()
    {
        if (carryBank != null && playback.CarryReady) return carryBank.Frames[carry.FrameIndex];
        if (!playback.Reacting) return idle[playback.IdleIndex];
        return playback.ReactionIndex < 4 ? entries[playback.EntryBucket][playback.ReactionIndex]
            : (playback.Reaction==ReactionKind.Smile ? smile : playback.Reaction==ReactionKind.Peace ? peace : playback.Reaction==ReactionKind.EarLeft ? earLeft : playback.Reaction==ReactionKind.EarRight ? earRight : wave)[playback.ReactionIndex - 4];
    }
    private void ClampPosition()
    {
        int pad = ContentPadding;
        Rectangle area = Screen.FromRectangle(new Rectangle(Left+pad, Top+pad, side, side)).WorkingArea;
        Location = new Point(Math.Max(area.Left-pad, Math.Min(Left, area.Right-side-pad)),
                             Math.Max(area.Top-pad, Math.Min(Top, area.Bottom-side-pad)));
    }
    private void UpdateCanvasSize() { int width = side+2*ContentPadding; ClientSize = new Size(width, width); }
    private void LoadPosition()
    {
        try
        {
            if (!File.Exists(statePath)) return;
            string[] values = File.ReadAllText(statePath).Split(',');
            int x, y, size;
            if (values.Length != 3 || !Int32.TryParse(values[0], out x) || !Int32.TryParse(values[1], out y)
                || !Int32.TryParse(values[2], out size) || size < 160 || size > 480) return;
            side = size; UpdateCanvasSize(); Location = new Point(x, y);
            ClampPosition();
        }
        catch (IOException) { Log("settings-read-failed"); }
        catch (UnauthorizedAccessException) { Log("settings-read-denied"); }
    }
    private void SavePosition()
    {
        try { File.WriteAllText(statePath, Left + "," + Top + "," + side); }
        catch (IOException) { Log("settings-write-failed"); }
        catch (UnauthorizedAccessException) { Log("settings-write-denied"); }
    }
    public void Log(string text)
    {
        // Diagnostic storage must not crash the character or its settings fallback.
        try { File.AppendAllText(logPath, DateTime.UtcNow.ToString("o") + " " + text + Environment.NewLine); }
        catch (IOException error) { Debug.WriteLine(error); }
        catch (UnauthorizedAccessException error) { Debug.WriteLine(error); }
        if (Changed != null) Changed();
    }
    private void Present(Bitmap source, float scale = 1f)
    {
        if (!IsHandleCreated || !Visible) return;
        if (carryBank != null)
        {
            PointF correction = PointF.Empty;
            if (playback.CarryReady)
            {
                PointF anchor = carryBank.Anchors[carry.FrameIndex], neutral = carryBank.Anchors[22];
                correction = new PointF(neutral.X-anchor.X, neutral.Y-anchor.Y);
            }
            using (Bitmap surface = CarrySurface.Create(source, side, carry, correction))
                Native.Present(Handle, Location, surface);
            return;
        }
        using (Bitmap surface = SpriteSurface.Create(source, side, scale))
            Native.Present(Handle, Location, surface);
    }
    protected override void OnFormClosed(FormClosedEventArgs e)
    {
        SavePosition(); Log("closed"); base.OnFormClosed(e);
    }
    protected override void Dispose(bool disposing)
    {
        if (disposing && !resourcesDisposed)
        {
            resourcesDisposed = true;
            timer.Stop(); timer.Dispose();
            if(controls!=null)controls.Dispose();
            if (tray != null) { tray.Visible = false; tray.Dispose(); }
            if (trayIcon != null) trayIcon.Dispose();
            if (menu != null) { menu.Font.Dispose(); menu.Dispose(); }
            if (idle != null) foreach (Bitmap bitmap in idle) bitmap.Dispose();
            if (wave != null) foreach (Bitmap bitmap in wave) bitmap.Dispose();
            if (peace != null) foreach (Bitmap bitmap in peace) bitmap.Dispose();
            if (earLeft != null) foreach (Bitmap bitmap in earLeft) bitmap.Dispose();
            if (earRight != null) foreach (Bitmap bitmap in earRight) bitmap.Dispose();
            if (smile != null) foreach (Bitmap bitmap in smile) bitmap.Dispose();
            if (carryBank != null) carryBank.Dispose();
            foreach (Bitmap[] clip in entries) if (clip != null) foreach (Bitmap bitmap in clip) bitmap.Dispose();
        }
        base.Dispose(disposing);
    }
}

// Time is supplied by the host's monotonic clock; checks exercise the exact same player.
internal enum ReactionKind { None, Wave, Peace, EarLeft, EarRight, Smile }

internal sealed class NoseRegions
{
    private readonly PointF[][] regions=new PointF[96][];
    internal NoseRegions(string path)
    {
        string[] rows=File.ReadAllLines(path);
        if(rows.Length!=96)throw new InvalidDataException("Expected 96 nose regions.");
        for(int i=0;i<96;i++){
            string[] parts=rows[i].Split('|');
            if(parts.Length!=2 || Int32.Parse(parts[0],System.Globalization.CultureInfo.InvariantCulture)!=i)
                throw new InvalidDataException("Nose frame order mismatch.");
            regions[i]=EarRegions.Read(parts[1]);
        }
    }
    internal bool Contains(int frame,PointF point){return EarRegions.Contains(regions[frame],point);}
}

internal sealed class EarRegions
{
    private readonly PointF[][] left=new PointF[96][], right=new PointF[96][];
    internal EarRegions(string path)
    {
        string[] rows=File.ReadAllLines(path);
        if(rows.Length!=96)throw new InvalidDataException("Expected 96 ear regions.");
        for(int i=0;i<96;i++){
            string[] parts=rows[i].Split('|');
            if(parts.Length!=3 || Int32.Parse(parts[0],System.Globalization.CultureInfo.InvariantCulture)!=i)
                throw new InvalidDataException("Ear frame order mismatch.");
            left[i]=Read(parts[1]);right[i]=Read(parts[2]);
        }
    }
    internal static PointF[] Read(string value)
    {
        string[] vertices=value.Split(';');
        if(vertices.Length<3 || vertices.Length>256)throw new InvalidDataException("Invalid ear polygon.");
        PointF[] points=new PointF[vertices.Length];
        double area=0;
        for(int i=0;i<points.Length;i++){
            string[] xy=vertices[i].Split(',');if(xy.Length!=2)throw new InvalidDataException("Invalid ear vertex.");
            float x=Single.Parse(xy[0],System.Globalization.CultureInfo.InvariantCulture),y=Single.Parse(xy[1],System.Globalization.CultureInfo.InvariantCulture);
            if(!(x>=0 && x<=1 && y>=0 && y<=1))throw new InvalidDataException("Invalid ear coordinate.");
            points[i]=new PointF(x,y);
        }
        for(int i=0,j=points.Length-1;i<points.Length;j=i++)area+=points[j].X*points[i].Y-points[i].X*points[j].Y;
        if(Math.Abs(area)<.00001)throw new InvalidDataException("Empty ear polygon.");
        return points;
    }
    internal static bool Contains(PointF[] polygon,PointF p)
    {
        bool inside=false;
        for(int i=0,j=polygon.Length-1;i<polygon.Length;j=i++){
            PointF a=polygon[i],b=polygon[j];
            if((a.Y>p.Y)!=(b.Y>p.Y) && p.X<(b.X-a.X)*(p.Y-a.Y)/(b.Y-a.Y)+a.X)inside=!inside;
        }
        return inside;
    }
    internal ReactionKind At(int frame,PointF p)
    {
        if(Contains(left[frame],p))return ReactionKind.EarLeft;
        if(Contains(right[frame],p))return ReactionKind.EarRight;
        return ReactionKind.None;
    }
}

internal sealed class HandRegions
{
    private readonly RectangleF[] wave=new RectangleF[96], peace=new RectangleF[96];
    internal HandRegions(string path)
    {
        string[] rows=File.ReadAllLines(path);
        if(rows.Length!=96) throw new InvalidDataException("Expected 96 idle hand regions.");
        for(int i=0;i<96;i++)
        {
            string[] values=rows[i].Split(',');
            if(values.Length!=9 || Int32.Parse(values[0],System.Globalization.CultureInfo.InvariantCulture)!=i)
                throw new InvalidDataException("Hand region frame order mismatch.");
            wave[i]=Read(values,1);peace[i]=Read(values,5);
            if(peace[i].Right>=wave[i].Left) throw new InvalidDataException("Hand regions overlap.");
        }
    }
    private static RectangleF Read(string[] values,int start)
    {
        float[] b=new float[4];
        for(int i=0;i<4;i++)
        {
            b[i]=Single.Parse(values[start+i],System.Globalization.CultureInfo.InvariantCulture);
            if(!(b[i]>=0 && b[i]<=1)) throw new InvalidDataException("Invalid hand region coordinate.");
        }
        if(b[2]<=b[0] || b[3]<=b[1]) throw new InvalidDataException("Empty hand region.");
        return RectangleF.FromLTRB(b[0],b[1],b[2],b[3]);
    }
    internal ReactionKind At(int frame,PointF point)
    {
        if(wave[frame].Contains(point))return ReactionKind.Wave;
        if(peace[frame].Contains(point))return ReactionKind.Peace;
        return ReactionKind.None;
    }
}

internal sealed class MotionPlayback
{
    public int IdleIndex { get; private set; }
    public int ReactionIndex { get; private set; }
    public int EntryBucket { get; private set; }
    public bool Reacting { get; private set; }
    internal ReactionKind Reaction { get; private set; }
    internal bool CarryReady { get; private set; }
    internal bool EntryOnly { get; private set; }
    private bool carryRequested;
    private double idleStart, reactionStart;
    public void Reset() { idleStart = reactionStart = 0; IdleIndex = ReactionIndex = EntryBucket = 0; Reaction=ReactionKind.None; Reacting = CarryReady = EntryOnly = carryRequested = false; }
    internal void BeginCarry(double now)
    {
        carryRequested = true;
        if (Reacting || CarryReady) return;
        Reaction=ReactionKind.None;
        EntryBucket = ((IdleIndex+2)/4)%24;
        reactionStart = now; ReactionIndex = 0; Reacting = EntryOnly = true;
    }
    internal void EndCarry(double now)
    {
        carryRequested = false;
        if (CarryReady) { CarryReady = false; IdleIndex = 0; idleStart = now; }
    }
    public bool React(double now,ReactionKind reaction=ReactionKind.Wave)
    {
        if (reaction==ReactionKind.None || Reacting || carryRequested || CarryReady) return false;
        Reaction=reaction;
        // Use the last displayed idle frame, not a future timer sample.
        EntryBucket = ((IdleIndex + 2) / 4) % 24;
        reactionStart = now; ReactionIndex = 0; Reacting = true;
        return true;
    }
    public void Advance(double now)
    {
        if (CarryReady) return;
        if (Reacting)
        {
            ReactionIndex = (int)((now - reactionStart) * 24);
            int length = EntryOnly ? 4 : Reaction==ReactionKind.Smile ? 32 : Reaction==ReactionKind.Peace ? 64 : (Reaction==ReactionKind.EarLeft || Reaction==ReactionKind.EarRight) ? 20 : 49;
            if (ReactionIndex < length) return;
            Reacting = false;
            Reaction=ReactionKind.None;
            EntryOnly = false;
            idleStart = reactionStart + length / 24.0;
            if (carryRequested) { CarryReady = true; IdleIndex = 0; return; }
        }
        IdleIndex = (int)((now - idleStart) * 24) % 96;
    }
}

internal static class SpriteSurface
{
    internal static Bitmap Create(Bitmap source, int side, float scale = 1f)
    {
        Bitmap surface = new Bitmap(side, side, PixelFormat.Format32bppPArgb);
        try
        {
            using (Graphics graphics = Graphics.FromImage(surface))
            {
                graphics.CompositingMode = CompositingMode.SourceCopy;
                graphics.InterpolationMode = InterpolationMode.HighQualityBicubic;
                graphics.PixelOffsetMode = PixelOffsetMode.HighQuality;
                float inset = side * (1f - scale) / 2f;
                graphics.DrawImage(source, inset, inset, side * scale, side * scale);
            }
            return surface;
        }
        catch { surface.Dispose(); throw; }
    }
}

internal static class Native
{
    [StructLayout(LayoutKind.Sequential)] private struct Pair { public int X, Y; public Pair(int x, int y) { X = x; Y = y; } }
    [StructLayout(LayoutKind.Sequential, Pack = 1)] private struct Blend { public byte Operation, Flags, Alpha, Format; }
    [DllImport("user32.dll")] internal static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")] private static extern IntPtr GetDC(IntPtr window);
    [DllImport("user32.dll")] private static extern int ReleaseDC(IntPtr window, IntPtr dc);
    [DllImport("gdi32.dll")] private static extern IntPtr CreateCompatibleDC(IntPtr dc);
    [DllImport("gdi32.dll")] private static extern IntPtr SelectObject(IntPtr dc, IntPtr bitmap);
    [DllImport("gdi32.dll")] private static extern bool DeleteObject(IntPtr value);
    [DllImport("gdi32.dll")] private static extern bool DeleteDC(IntPtr dc);
    [DllImport("user32.dll", SetLastError = true)] private static extern bool UpdateLayeredWindow(IntPtr window, IntPtr screenDC,
        ref Pair location, ref Pair size, IntPtr memoryDC, ref Pair source, int key, ref Blend blend, int flags);
    internal static void Present(IntPtr window, Point location, Bitmap bitmap)
    {
        IntPtr screen = GetDC(IntPtr.Zero), memory = CreateCompatibleDC(screen), handle = IntPtr.Zero, previous = IntPtr.Zero;
        try
        {
            handle = bitmap.GetHbitmap(Color.FromArgb(0));
            previous = SelectObject(memory, handle);
            Pair position = new Pair(location.X, location.Y), size = new Pair(bitmap.Width, bitmap.Height), origin = new Pair(0, 0);
            Blend blend = new Blend { Alpha = 255, Format = 1 };
            if (!UpdateLayeredWindow(window, screen, ref position, ref size, memory, ref origin, 0, ref blend, 2))
                throw new Win32Exception(Marshal.GetLastWin32Error());
        }
        finally
        {
            if (previous != IntPtr.Zero) SelectObject(memory, previous);
            if (handle != IntPtr.Zero) DeleteObject(handle);
            if (memory != IntPtr.Zero) DeleteDC(memory);
            if (screen != IntPtr.Zero) ReleaseDC(IntPtr.Zero, screen);
        }
    }
}

// A controlled window behind the pet. It is excluded from ordinary launches.
internal sealed class ProbeWindow : Form
{
    private readonly PetWindow pet;
    private readonly Label status = new Label();
    private int cornerClicks, bodyClicks;
    public ProbeWindow(PetWindow value)
    {
        pet = value; Text = pet.CarryEnabled ? "Stitch - taşıma denemesi" : "Stitch - kısa kontrol"; StartPosition = FormStartPosition.CenterScreen;
        AutoScaleMode = AutoScaleMode.None; ClientSize = new Size(740, 510); BackColor = Color.WhiteSmoke;
        Button corner = Add("Boş köşe", 390, 95, delegate { cornerClicks++; pet.Log("probe-corner-click count=" + cornerClicks); });
        corner.Size = new Size(90, 30);
        Button body = Add("Alttaki düğme", 485, 240, delegate { bodyClicks++; pet.Log("probe-body-click count=" + bodyClicks); });
        body.Size = new Size(100, 30);
        Add("Test için hizala", 20, 20, delegate { Align(); });
        Add("Göster", 20, 70, delegate { pet.ShowPet(); });
        Add("Gizle", 20, 120, delegate { pet.HidePet(); });
        Add("Küçük", 20, 170, delegate { pet.SetSize(240); });
        Add("Büyük", 20, 220, delegate { pet.SetSize(400); });
        Add("El salla", 20, 270, delegate { pet.React(); });
        Add("Stitch'i kapat", 20, 320, delegate { pet.Close(); Close(); });
        Label help = new Label { Text = "1. Boş köşe: sayaç artmalı.\r\n2. Stitch'in gövdesi: yalnız tepki artmalı.\r\n3. Sürükle; boyut ve gizlemeyi dene.", AutoSize = false };
        help.SetBounds(230, 20, 490, 65); Controls.Add(help);
        status.SetBounds(20, 395, 700, 100); Controls.Add(status);
        pet.Changed += UpdateStatus;
        FormClosed += delegate { pet.Changed -= UpdateStatus; };
        Shown += delegate { Align(); };
    }
    private Button Add(string text, int x, int y, EventHandler click)
    {
        Button button = new Button { Text = text, Location = new Point(x, y), Size = new Size(180, 36) };
        button.Click += click; Controls.Add(button); return button;
    }
    private void Align()
    {
        pet.SetSize(320); pet.Location = PointToScreen(new Point(385-pet.ContentPadding, 95-pet.ContentPadding)); pet.ShowPet();
        pet.Log("probe-aligned foreground=" + Native.GetForegroundWindow()); UpdateStatus();
    }
    private void UpdateStatus()
    {
        status.Text = "Boş köşe: " + cornerClicks + " | Alttaki düğme: " + bodyClicks + " | Tepki: " + pet.Reactions
            + "\r\nGörünür: " + (pet.Visible ? "Evet" : "Hayır") + " | Konum: " + pet.Location + " | Boyut: " + pet.Width
            + "\r\nSağ tık: menü. Saat yanındaki Stitch bilgi simgesine çift tık: geri getir."
            + "\r\nBu panelin X düğmesi yalnız paneli kapatır; Stitch açık kalır.";
    }
}
