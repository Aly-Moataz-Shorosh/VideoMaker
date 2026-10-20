"""Labelled frame sheet of any clip: python clip_sheet.py <video> <out.jpg> <step_sec> [cols]"""
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont
src, out, step = sys.argv[1], sys.argv[2], float(sys.argv[3])
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 6
d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 18)
tiles, t = [], 0.3
while t < d:
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', src, '-frames:v', '1', '-vf', 'scale=240:-2', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
    if b:
        import io
        im = Image.open(io.BytesIO(b)).convert('RGB')
        ImageDraw.Draw(im).text((4, 2), f'{t:.0f}', fill=(255, 255, 0), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
        tiles.append(im)
    t += step
w, h = tiles[0].size
r = (len(tiles) + cols - 1) // cols
s = Image.new('RGB', (cols * (w + 4), r * (h + 4)))
for i, im in enumerate(tiles):
    s.paste(im.resize((w, h)), ((i % cols) * (w + 4), (i // cols) * (h + 4)))
s.save(out, quality=80)
print(out, len(tiles))
