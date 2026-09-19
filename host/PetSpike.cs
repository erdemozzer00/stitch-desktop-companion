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
        bool probe = false, preview = false;
        foreach (string arg in args)
        {
            if (arg.StartsWith("--assets=")) assets = Path.GetFullPath(arg.Substring(9));
            if (arg == "--probe") probe = true;
            if (arg == "--preview") preview = true;
        }
        try
        {
            using (PetWindow pet = new PetWindow(assets, root))
            {
                if (probe) pet.Shown += delegate { new ProbeWindow(pet).Show(); };
                if (preview) pet.Shown += delegate { pet.React(); };
                Application.Run(pet);
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
    private readonly Bitmap[][] entries = new Bitmap[16][];
    private readonly MotionPlayback playback = new MotionPlayback();
    private readonly Timer timer = new Timer();
    private readonly Stopwatch clock = new Stopwatch();
    private readonly NotifyIcon tray;
    private readonly ContextMenuStrip menu;
    private bool pressed, dragging, resourcesDisposed;
    private Point pointerStart, windowStart;
    private int side = 320;
    private Bitmap presented;
    public int Reactions { get; private set; }
    public event Action Changed;

    public PetWindow(string assets, string output, bool createTray = true)
    {
        statePath = Path.Combine(output, "position.txt");
        logPath = Path.Combine(output, "events.log");
        idle = ReadClip(assets, "idle_", 96);
        wave = ReadClip(assets, "wave_", 45);
        for (int i = 0; i < entries.Length; i++) entries[i] = ReadClip(assets, "entry_" + i.ToString("00") + "_", 4);
        Text = "Stitch floating prototype";
        AccessibleName = "Stitch floating prototype";
        FormBorderStyle = FormBorderStyle.None;
        ShowInTaskbar = false;
        StartPosition = FormStartPosition.Manual;
        TopMost = true;
        AutoScaleMode = AutoScaleMode.None;
        ClientSize = new Size(side, side);
        Location = new Point(Screen.PrimaryScreen.WorkingArea.Right - side - 40,
                             Screen.PrimaryScreen.WorkingArea.Bottom - side - 40);
        LoadPosition();
        menu = new ContextMenuStrip();
        menu.Items.Add("El salla", null, delegate { React(); });
        menu.Items.Add("Küçük", null, delegate { SetSize(240); });
        menu.Items.Add("Orta", null, delegate { SetSize(320); });
        menu.Items.Add("Büyük", null, delegate { SetSize(400); });
        menu.Items.Add("Gizle", null, delegate { HidePet(); });
        menu.Items.Add("Göster", null, delegate { ShowPet(); });
        menu.Items.Add("Çıkış", null, delegate { Close(); });
        if (createTray)
        {
            tray = new NotifyIcon { Icon = SystemIcons.Information, Text = "Stitch - sağ tık: seçenekler", ContextMenuStrip = menu, Visible = true };
            tray.DoubleClick += delegate { ShowPet(); };
        }
        timer.Interval = 15;
        timer.Tick += delegate { Advance(); };
        Shown += delegate { clock.Restart(); timer.Start(); Advance(); Log("launched motion=phase03-v3 idle=" + idle.Length + " wave=" + wave.Length + " size=" + side + " location=" + Location); };
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
        pressed = true;
        dragging = false;
        pointerStart = Cursor.Position;
        windowStart = Location;
        Capture = true;
        Log("pointer-down foreground=" + Native.GetForegroundWindow());
    }
    protected override void OnMouseMove(MouseEventArgs e)
    {
        base.OnMouseMove(e);
        if (!pressed) return;
        Point pointer = Cursor.Position;
        int dx = pointer.X - pointerStart.X, dy = pointer.Y - pointerStart.Y;
        Size threshold = SystemInformation.DragSize;
        if (Math.Abs(dx) >= threshold.Width / 2 || Math.Abs(dy) >= threshold.Height / 2) dragging = true;
        if (dragging) Location = new Point(windowStart.X + dx, windowStart.Y + dy);
    }
    protected override void OnMouseUp(MouseEventArgs e)
    {
        base.OnMouseUp(e);
        if (e.Button == MouseButtons.Right) { menu.Show(Cursor.Position); return; }
        if (e.Button != MouseButtons.Left || !pressed) return;
        bool wasDrag = dragging;
        pressed = false;
        dragging = false;
        Capture = false;
        if (wasDrag) { ClampPosition(); SavePosition(); Log("drag-ended location=" + Location); }
        else React();
    }
    protected override void OnMouseCaptureChanged(EventArgs e)
    {
        base.OnMouseCaptureChanged(e);
        if (!Capture && pressed)
        {
            pressed = dragging = false;
            ClampPosition(); SavePosition(); Log("drag-cancelled");
        }
    }
    public void React()
    {
        if (!Visible) { Log("hidden-reaction-ignored"); return; }
        if (!playback.React(clock.Elapsed.TotalSeconds)) { Log("repeat-click-ignored"); return; }
        Reactions++; Advance(); Log("reaction-start count=" + Reactions + " entry=" + playback.EntryBucket);
    }
    private void Advance()
    {
        bool wasReacting = playback.Reacting;
        playback.Advance(clock.Elapsed.TotalSeconds);
        Bitmap current = CurrentFrame();
        if (current != presented) { Present(current); presented = current; }
        if (wasReacting && !playback.Reacting) Log("reaction-end idle-resumed");
    }
    public void SetSize(int value)
    {
        side = Math.Max(160, Math.Min(480, value));
        ClientSize = new Size(side, side);
        ClampPosition(); Present(CurrentFrame()); SavePosition(); Log("size=" + side);
    }
    public void HidePet()
    {
        timer.Stop(); clock.Reset(); playback.Reset(); presented = null; pressed = dragging = false;
        Capture = false; Hide(); Log("hidden");
    }
    public void ShowPet() { ClampPosition(); Show(); clock.Start(); timer.Start(); Present(CurrentFrame()); Log("shown"); }
    private Bitmap CurrentFrame()
    {
        if (!playback.Reacting) return idle[playback.IdleIndex];
        return playback.ReactionIndex < 4 ? entries[playback.EntryBucket][playback.ReactionIndex] : wave[playback.ReactionIndex - 4];
    }
    private void ClampPosition()
    {
        Rectangle area = Screen.FromRectangle(Bounds).WorkingArea;
        Location = new Point(Math.Max(area.Left, Math.Min(Left, area.Right - side)),
                             Math.Max(area.Top, Math.Min(Top, area.Bottom - side)));
    }
    private void LoadPosition()
    {
        try
        {
            if (!File.Exists(statePath)) return;
            string[] values = File.ReadAllText(statePath).Split(',');
            int x, y, size;
            if (values.Length != 3 || !Int32.TryParse(values[0], out x) || !Int32.TryParse(values[1], out y)
                || !Int32.TryParse(values[2], out size) || size < 160 || size > 480) return;
            side = size; ClientSize = new Size(side, side); Location = new Point(x, y);
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
            if (tray != null) { tray.Visible = false; tray.Dispose(); }
            if (menu != null) menu.Dispose();
            if (idle != null) foreach (Bitmap bitmap in idle) bitmap.Dispose();
            if (wave != null) foreach (Bitmap bitmap in wave) bitmap.Dispose();
            foreach (Bitmap[] clip in entries) if (clip != null) foreach (Bitmap bitmap in clip) bitmap.Dispose();
        }
        base.Dispose(disposing);
    }
}

// Time is supplied by the host's monotonic clock; checks exercise the exact same player.
internal sealed class MotionPlayback
{
    public int IdleIndex { get; private set; }
    public int ReactionIndex { get; private set; }
    public int EntryBucket { get; private set; }
    public bool Reacting { get; private set; }
    private double idleStart, reactionStart;
    public void Reset() { idleStart = reactionStart = 0; IdleIndex = ReactionIndex = EntryBucket = 0; Reacting = false; }
    public bool React(double now)
    {
        if (Reacting) return false;
        // Use the last displayed idle frame, not a future timer sample.
        EntryBucket = ((IdleIndex + 3) / 6) % 16;
        reactionStart = now; ReactionIndex = 0; Reacting = true;
        return true;
    }
    public void Advance(double now)
    {
        if (Reacting)
        {
            ReactionIndex = (int)((now - reactionStart) * 24);
            if (ReactionIndex < 49) return;
            Reacting = false;
            idleStart = reactionStart + 49.0 / 24;
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
        pet = value; Text = "Stitch - kısa kontrol"; StartPosition = FormStartPosition.CenterScreen;
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
        pet.SetSize(320); pet.Location = PointToScreen(new Point(385, 95)); pet.ShowPet();
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
