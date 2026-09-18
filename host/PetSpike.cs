// Phase 02 feasibility prototype. No startup registration or shell embedding.
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
    private readonly Bitmap idle;
    private readonly Bitmap[] wave;
    private readonly Timer timer = new Timer();
    private readonly Stopwatch clock = new Stopwatch();
    private readonly NotifyIcon tray;
    private readonly ContextMenuStrip menu;
    private bool pressed, dragging, reacting;
    private Point pointerStart, windowStart;
    private int side = 320, frame = -1;
    public int Reactions { get; private set; }
    public event Action Changed;

    public PetWindow(string assets, string output)
    {
        statePath = Path.Combine(output, "position.txt");
        logPath = Path.Combine(output, "events.log");
        idle = ReadBitmap(Path.Combine(assets, "idle.png"));
        string[] paths = Directory.GetFiles(assets, "wave_*.png");
        Array.Sort(paths, StringComparer.Ordinal);
        wave = Array.ConvertAll(paths, ReadBitmap);
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
        menu.Items.Add("Kucuk", null, delegate { SetSize(240); });
        menu.Items.Add("Orta", null, delegate { SetSize(320); });
        menu.Items.Add("Buyuk", null, delegate { SetSize(400); });
        menu.Items.Add("Gizle", null, delegate { HidePet(); });
        menu.Items.Add("Goster", null, delegate { ShowPet(); });
        menu.Items.Add("Cikis", null, delegate { Close(); });
        tray = new NotifyIcon { Icon = SystemIcons.Information, Text = "Stitch - sag tik: secenekler", ContextMenuStrip = menu, Visible = true };
        tray.DoubleClick += delegate { ShowPet(); };
        timer.Interval = 15;
        timer.Tick += delegate { Advance(); };
        Shown += delegate { Present(idle); Log("launched size=" + side + " frames=" + wave.Length + " location=" + Location); };
        Log("environment os=" + Environment.OSVersion + " screens=" + Screen.AllScreens.Length);
    }

    private static Bitmap ReadBitmap(string path)
    {
        using (Image source = Image.FromFile(path)) return new Bitmap(source);
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
        if (reacting) { Log("repeat-click-ignored"); return; }
        reacting = true; Reactions++; frame = -1;
        clock.Restart(); timer.Start(); Advance(); Log("reaction-start count=" + Reactions);
    }
    private void Advance()
    {
        int index = (int)(clock.Elapsed.TotalSeconds * 24);
        int count = wave.Length == 0 ? 18 : wave.Length;
        if (index >= count)
        {
            reacting = false; timer.Stop(); clock.Stop(); frame = -1;
            Present(idle); Log("reaction-end"); return;
        }
        if (index == frame) return;
        frame = index;
        // Initial static-asset spike uses a small visual response, not a claimed wave.
        Present(wave.Length == 0 ? idle : wave[index], wave.Length == 0 ? 0.97f : 1f);
    }
    public void SetSize(int value)
    {
        side = Math.Max(160, Math.Min(480, value));
        ClientSize = new Size(side, side);
        ClampPosition(); Present(CurrentFrame()); SavePosition(); Log("size=" + side);
    }
    public void HidePet()
    {
        timer.Stop(); clock.Reset(); reacting = false; frame = -1; pressed = dragging = false;
        Capture = false; Hide(); Log("hidden");
    }
    public void ShowPet() { ClampPosition(); Show(); Present(CurrentFrame()); Log("shown"); }
    private Bitmap CurrentFrame() { return reacting && wave.Length > 0 && frame >= 0 ? wave[frame] : idle; }
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
        File.AppendAllText(logPath, DateTime.UtcNow.ToString("o") + " " + text + Environment.NewLine);
        if (Changed != null) Changed();
    }
    private void Present(Bitmap source, float scale = 1f)
    {
        if (!IsHandleCreated || !Visible) return;
        using (Bitmap surface = new Bitmap(side, side, PixelFormat.Format32bppPArgb))
        {
            using (Graphics graphics = Graphics.FromImage(surface))
            {
                graphics.CompositingMode = CompositingMode.SourceCopy;
                graphics.InterpolationMode = InterpolationMode.HighQualityBicubic;
                graphics.PixelOffsetMode = PixelOffsetMode.HighQuality;
                float inset = side * (1f - scale) / 2f;
                graphics.DrawImage(source, inset, inset, side * scale, side * scale);
            }
            Native.Present(Handle, Location, surface);
        }
    }
    protected override void OnFormClosed(FormClosedEventArgs e)
    {
        SavePosition(); timer.Stop(); timer.Dispose(); tray.Visible = false; tray.Dispose(); menu.Dispose();
        idle.Dispose(); foreach (Bitmap bitmap in wave) bitmap.Dispose();
        Log("closed"); base.OnFormClosed(e);
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
        pet = value; Text = "Stitch host probe"; StartPosition = FormStartPosition.CenterScreen;
        AutoScaleMode = AutoScaleMode.None; ClientSize = new Size(740, 510); BackColor = Color.WhiteSmoke;
        Button corner = Add("Transparent corner", 390, 95, delegate { cornerClicks++; pet.Log("probe-corner-click count=" + cornerClicks); });
        corner.Size = new Size(90, 30);
        Button body = Add("Covered body", 485, 240, delegate { bodyClicks++; pet.Log("probe-body-click count=" + bodyClicks); });
        body.Size = new Size(100, 30);
        Add("Align pet for test", 20, 20, delegate { Align(); });
        Add("Show pet", 20, 70, delegate { pet.ShowPet(); });
        Add("Hide pet", 20, 120, delegate { pet.HidePet(); });
        Add("Small", 20, 170, delegate { pet.SetSize(240); });
        Add("Large", 20, 220, delegate { pet.SetSize(400); });
        Add("Reaction", 20, 270, delegate { pet.React(); });
        Add("Exit prototype", 20, 320, delegate { pet.Close(); Close(); });
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
        status.Text = "Corner clicks: " + cornerClicks + " | Covered body clicks: " + bodyClicks + " | Pet reactions: " + pet.Reactions
            + "\r\nPet visible: " + pet.Visible + " | Position: " + pet.Location + " | Size: " + pet.Width
            + "\r\nClick pet to react; drag it; right click for menu. Tray double click restores it.";
    }
}
