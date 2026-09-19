// Opt-in Phase 04 trial. No physics engine or eye-closure assets.
using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Globalization;
using System.IO;

internal sealed class CarryBank : IDisposable
{
    internal readonly Bitmap[] Frames = new Bitmap[45];
    internal readonly PointF[] Anchors = new PointF[45];
    internal CarryBank(string directory)
    {
        try
        {
            string[] lines = File.ReadAllLines(Path.Combine(directory, "anchors.csv"));
            if (lines.Length != 45) throw new InvalidDataException("Carry anchor count must be 45.");
            for (int y = 0; y < 5; y++) for (int x = 0; x < 9; x++)
            {
                int i = y * 9 + x;
                string name = "bank_" + x + "_" + y + ".png";
                string[] values = lines[i].Split(',');
                if (values.Length != 3 || values[0] != name) throw new InvalidDataException("Carry anchor order mismatch.");
                float ax = Single.Parse(values[1], CultureInfo.InvariantCulture);
                float ay = Single.Parse(values[2], CultureInfo.InvariantCulture);
                if (!(ax >= 0 && ax <= 1 && ay >= 0 && ay <= 1)) throw new InvalidDataException("Invalid carry anchor.");
                Anchors[i] = new PointF(ax, ay);
                using (Image image = Image.FromFile(Path.Combine(directory, name)))
                {
                    if ((image.Width != 240 && image.Width != 400) || image.Height != image.Width)
                        throw new InvalidDataException("Carry bank must be square 240px or 400px.");
                    Frames[i] = new Bitmap(image);
                }
            }
        }
        catch { Dispose(); throw; }
    }
    public void Dispose() { foreach (Bitmap frame in Frames) if (frame != null) frame.Dispose(); }
}

// Time/input supplied by the host; the accepted Python replay is an independent oracle.
internal sealed class CarryResponse
{
    internal double Angle, Vertical;
    private double bodyVelocity, ear, earVelocity, verticalVelocity, vx, vy, lastTime;
    private PointF previousPointer;
    internal bool Held { get; private set; }
    internal bool Active { get; private set; }
    internal PointF Pivot = new PointF(.5f, .6f), Offset;
    internal double Horizontal { get { return Clamp((ear-Angle)/.07 + .2*Angle/.18); } }
    internal bool CanResumeIdle(int size)
    {
        // Resume breathing once the authored bank is neutral and the remaining
        // global turn is subpixel. Keep integrating that turn independently.
        double horizontalSpeed=(earVelocity-bodyVelocity)/.07+.2*bodyVelocity/.18;
        return !Held && FrameIndex == 22 && Math.Abs(Angle)*size < .25
            && Math.Abs(bodyVelocity)*size < 3 && Math.Abs(horizontalSpeed)<1
            && Math.Abs(verticalVelocity)<1;
    }
    internal int FrameIndex { get { return (int)Math.Floor((Clamp(Vertical)+1)*2+.5)*9 + (int)Math.Floor((Horizontal+1)*4+.5); } }

    internal static double Clamp(double value) { return Math.Max(-1, Math.Min(1, value)); }
    private static void Spring(ref double value, ref double velocity, double target, double omega, double dt)
    {
        double delta = value-target, j = velocity+omega*delta, decay = Math.Exp(-omega*dt);
        value = target+(delta+j*dt)*decay;
        velocity = (velocity-omega*j*dt)*decay;
    }
    internal PointF Map(PointF point)
    {
        double c = Math.Cos(Angle), s = Math.Sin(Angle), x = point.X-Pivot.X, y = point.Y-Pivot.Y;
        return new PointF((float)(c*x-s*y+Pivot.X+Offset.X), (float)(s*x+c*y+Pivot.Y+Offset.Y));
    }
    internal void Begin(double now, PointF pointer, PointF displayedGrip)
    {
        // Invert the current transform before changing its pivot. Re-grab preserves
        // the entire displayed affine transform, not just its center point.
        double c = Math.Cos(Angle), s = Math.Sin(Angle);
        double x = displayedGrip.X-Pivot.X-Offset.X, y = displayedGrip.Y-Pivot.Y-Offset.Y;
        PointF sourceGrip = new PointF((float)(c*x+s*y+Pivot.X), (float)(-s*x+c*y+Pivot.Y));
        Pivot = sourceGrip;
        Offset = new PointF(displayedGrip.X-sourceGrip.X, displayedGrip.Y-sourceGrip.Y);
        previousPointer = pointer; lastTime = now; vx = vy = 0;
        Held = Active = true;
    }
    internal void Release() { Held = false; }
    internal void Update(double now, PointF pointer, int size)
    {
        if (!Active) return;
        double elapsed = now-lastTime;
        if (elapsed <= 0) return;
        // Resume stalls and teleports must not create an unbounded input impulse.
        double dt = Math.Min(elapsed, .05);
        double rawX = elapsed > .25 ? 0 : (pointer.X-previousPointer.X)/elapsed/size;
        double rawY = elapsed > .25 ? 0 : (pointer.Y-previousPointer.Y)/elapsed/size;
        double smoothing = 1-Math.Exp(-dt/.045);
        vx += (Math.Max(-12, Math.Min(12, rawX))-vx)*smoothing;
        vy += (Math.Max(-12, Math.Min(12, rawY))-vy)*smoothing;
        if (!Held) vx = vy = 0;
        double goal = Math.Max(-.18, Math.Min(.18, vx*.16));
        if (Math.Abs(vx) < .025) goal = 0;
        Spring(ref Angle, ref bodyVelocity, goal, 26, dt);
        Spring(ref ear, ref earVelocity, Angle, 16, dt);
        double yGoal = Math.Abs(vy) < .025 ? 0 : Clamp(-vy*.9);
        Spring(ref Vertical, ref verticalVelocity, yGoal, 22, dt);
        previousPointer = pointer; lastTime = now;
        if ((!Held || (Math.Abs(vx)<.025 && Math.Abs(vy)<.025))
            && Math.Abs(Angle)<.0001 && Math.Abs(bodyVelocity)<.002
            && Math.Abs(ear)<.0001 && Math.Abs(earVelocity)<.002
            && Math.Abs(Vertical)<.0001 && Math.Abs(verticalVelocity)<.002)
        {
            Angle = Vertical = bodyVelocity = ear = earVelocity = verticalVelocity = 0;
            Active = Held;
        }
    }
    internal void Reset()
    {
        Held = Active = false;
        Angle = Vertical = bodyVelocity = ear = earVelocity = verticalVelocity = vx = vy = 0;
        Offset = PointF.Empty; Pivot = new PointF(.5f, .6f);
    }
}

internal static class CarrySurface
{
    internal static int Padding(int side) { return (int)Math.Ceiling(side*.35); }
    internal static Bitmap Create(Bitmap source, int side, CarryResponse response, PointF anchorCorrection)
    {
        int pad = Padding(side);
        Bitmap surface = new Bitmap(side+2*pad, side+2*pad, PixelFormat.Format32bppPArgb);
        try
        {
            using (Graphics graphics = Graphics.FromImage(surface))
            {
                graphics.CompositingMode = CompositingMode.SourceCopy;
                graphics.InterpolationMode = InterpolationMode.HighQualityBicubic;
                graphics.PixelOffsetMode = PixelOffsetMode.HighQuality;
                double c = Math.Cos(response.Angle), s = Math.Sin(response.Angle);
                PointF origin = response.Map(anchorCorrection);
                if (response.Angle == 0)
                    graphics.DrawImage(source, pad+origin.X*side, pad+origin.Y*side, (float)side, (float)side);
                else
                {
                    // GDI+ uses row-vector elements: x'=m11*x+m21*y+dx.
                    using (Matrix transform = new Matrix((float)c, (float)s, (float)-s, (float)c,
                        pad+origin.X*side, pad+origin.Y*side))
                        graphics.Transform = transform;
                    graphics.DrawImage(source, 0f, 0f, (float)side, (float)side);
                }
            }
            return surface;
        }
        catch { surface.Dispose(); throw; }
    }
}
