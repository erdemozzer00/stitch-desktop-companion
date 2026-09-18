// Component checks on the real host code; no mouse injection or desktop acceptance claim.
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Runtime.InteropServices;
using System.Windows.Forms;

internal static class HostChecks
{
    private static int assertions;
    private static readonly List<string> cases = new List<string>();

    [STAThread]
    private static int Main(string[] args)
    {
        try
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            string assets = args[0], scratch = args[1];
            Directory.CreateDirectory(scratch);
            using (Bitmap idle = new Bitmap(Path.Combine(assets, "idle.png")))
            {
                foreach (int size in new[] { 240, 320, 400 })
                using (Bitmap surface = SpriteSurface.Create(idle, size))
                {
                    Assert(surface.PixelFormat == PixelFormat.Format32bppPArgb, "Expected premultiplied surface");
                    Assert(surface.GetPixel(size / 2, size / 2).A == 255, "Body must remain opaque");
                    for (int i = 0; i < size; i++)
                        Assert(surface.GetPixel(i, 0).A == 0 && surface.GetPixel(i, size - 1).A == 0
                            && surface.GetPixel(0, i).A == 0 && surface.GetPixel(size - 1, i).A == 0, "Resize clipped alpha boundary");
                    CheckPremultiplied(surface);
                }
                using (Bitmap surface = SpriteSurface.Create(idle, 320))
                {
                    Assert(surface.GetPixel(50, 15).A == 0, "Probe corner center must be transparent");
                    Assert(surface.GetPixel(150, 160).A == 255, "Probe body center must be opaque");
                }
            }
            cases.Add("Three output sizes preserve alpha and premultiplied pixels; manual probe targets have the intended alpha");

            string settings = Path.Combine(scratch, "settings");
            Directory.CreateDirectory(settings);
            Point saved;
            using (PetWindow pet = new PetWindow(assets, settings, false))
            {
                Assert(!pet.Visible, "Component window must remain hidden");
                pet.React(); pet.React();
                Assert(pet.Reactions == 0, "A hidden character must not start an invisible reaction");
                pet.HidePet(); pet.React();
                Assert(pet.Reactions == 0, "Hide must continue to suppress reactions");
                pet.SetSize(1); Assert(pet.Width == 160, "Minimum size bound");
                pet.SetSize(10000); Assert(pet.Width == 480, "Maximum size bound");
                Rectangle area = Screen.PrimaryScreen.WorkingArea;
                pet.Location = new Point(area.Left + 30, area.Top + 30);
                pet.SetSize(240); saved = pet.Location;
                Assert(!pet.Visible, "Resizing hidden character must not show it");
            }
            using (PetWindow restored = new PetWindow(assets, settings, false))
            {
                Assert(restored.Width == 240 && restored.Location == saved, "Saved geometry did not round trip");
            }
            cases.Add("Hidden reaction guard, size bounds and saved geometry round trip through the real host");

            File.WriteAllText(Path.Combine(settings, "position.txt"), "not,a,position");
            using (PetWindow invalid = new PetWindow(assets, settings, false))
                Assert(invalid.Width == 320, "Malformed settings must use the default size");
            File.WriteAllText(Path.Combine(settings, "position.txt"), "-99999,-99999,240");
            using (PetWindow recovered = new PetWindow(assets, settings, false))
            {
                Rectangle area = Screen.FromRectangle(recovered.Bounds).WorkingArea;
                Assert(area.Contains(recovered.Bounds), "Off-screen saved position was not recovered");
            }
            cases.Add("Malformed and off-screen settings fall back to usable geometry");

            string unavailableLog = Path.Combine(scratch, "unavailable-log");
            Directory.CreateDirectory(Path.Combine(unavailableLog, "events.log"));
            using (PetWindow pet = new PetWindow(assets, unavailableLog, false))
            {
                pet.Log("Expected diagnostic write failure");
                pet.SetSize(240);
                Assert(File.Exists(Path.Combine(unavailableLog, "position.txt")), "Logging failure interrupted settings write");
                pet.Dispose(); // The outer using also disposes it: cleanup must be idempotent.
            }
            cases.Add("An unavailable diagnostic log does not abort host creation or settings changes; repeated disposal succeeds");
            Console.WriteLine("{\"status\":\"PASS\",\"assertions\":" + assertions + ",\"cases\":["
                + String.Join(",", cases.ConvertAll(value => "\"" + value + "\""))
                + "],\"limits\":\"Component and pixel checks only. No native clicks, menu operation, desktop composition, or visual motion acceptance.\"}");
            return 0;
        }
        catch (Exception error) { Console.Error.WriteLine(error); return 1; }
    }

    private static void Assert(bool value, string message)
    {
        assertions++;
        if (!value) throw new Exception(message);
    }

    private static void CheckPremultiplied(Bitmap surface)
    {
        BitmapData data = surface.LockBits(new Rectangle(Point.Empty, surface.Size), ImageLockMode.ReadOnly, PixelFormat.Format32bppPArgb);
        try
        {
            byte[] pixels = new byte[data.Stride * data.Height];
            Marshal.Copy(data.Scan0, pixels, 0, pixels.Length);
            int translucent = 0;
            bool valid = true;
            for (int i = 0; i < pixels.Length; i += 4)
            {
                byte alpha = pixels[i + 3];
                if (alpha > 0 && alpha < 255) translucent++;
                valid &= pixels[i] <= alpha && pixels[i + 1] <= alpha && pixels[i + 2] <= alpha;
            }
            Assert(translucent > 0 && valid, "Soft edges must be premultiplied without bright RGB in zero-alpha pixels");
        }
        finally { surface.UnlockBits(data); }
    }
}
