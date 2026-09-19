using System;
using System.IO;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;

internal static class BuildShortcutIcon
{
    private static void Main(string[] args)
    {
        int[] sizes={16,20,24,32,48,64,128,256};
        byte[][] images=new byte[sizes.Length][];
        using(Image source=Image.FromFile(args[0]))
        {
            for(int i=0;i<sizes.Length;i++)
            using(Bitmap bitmap=new Bitmap(sizes[i],sizes[i],PixelFormat.Format32bppArgb))
            using(MemoryStream stream=new MemoryStream())
            {
                using(Graphics g=Graphics.FromImage(bitmap))
                {g.InterpolationMode=InterpolationMode.HighQualityBicubic;StitchIcon.DrawFace(g,source,new RectangleF(0,0,sizes[i],sizes[i]));}
                bitmap.Save(stream,ImageFormat.Png);images[i]=stream.ToArray();
                if(sizes[i]==256)bitmap.Save(Path.ChangeExtension(args[1],"png"),ImageFormat.Png);
            }
        }
        using(BinaryWriter writer=new BinaryWriter(File.Create(args[1])))
        {
            writer.Write((ushort)0);writer.Write((ushort)1);writer.Write((ushort)sizes.Length);
            int offset=6+16*sizes.Length;
            for(int i=0;i<sizes.Length;i++)
            {
                writer.Write((byte)(sizes[i]==256?0:sizes[i]));writer.Write((byte)(sizes[i]==256?0:sizes[i]));
                writer.Write((byte)0);writer.Write((byte)0);writer.Write((ushort)1);writer.Write((ushort)32);
                writer.Write(images[i].Length);writer.Write(offset);offset+=images[i].Length;
            }
            foreach(byte[] image in images)writer.Write(image);
        }
        // Framework Icon caps its selected size below 256. Validate each embedded
        // PNG and use the managed loader for supported selections instead.
        for(int i=0;i<sizes.Length;i++)using(MemoryStream bytes=new MemoryStream(images[i]))using(Image decoded=Image.FromStream(bytes))
        {if(decoded.Width!=sizes[i] || decoded.Height!=sizes[i])throw new Exception("Invalid icon image.");}
        foreach(int size in sizes)using(Icon icon=new Icon(args[1],new Size(size,size)))
        {if(size<256 && (icon.Width!=size || icon.Height!=size))throw new Exception("ICO resolution missing: "+size);}
        Console.WriteLine("ICO: eight PNG sizes verified (16 through 256); managed icon selection verified through 128.");
    }
}
