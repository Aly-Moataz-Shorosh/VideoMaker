"""Projector crops of the RAW camera at given Main-new seconds, labelled, in one sheet (to see which slide/video was shown).
python proj_sheet.py out.jpg 1166 1170 1180 ..."""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
P = Path(__file__).resolve().parents[2]
OFF = -88.01
out, ts = sys.argv[1], [float(x) for x in sys.argv[2:]]
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 22)
tiles = []
for t in ts:
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t + OFF:.2f}', '-i', str(P / 'input' / '20260908_103633.mp4'), '-frames:v', '1',
                        '-vf', 'crop=520:300:545:5,scale=416:240', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    im = Image.frombytes('RGB', (416, 240), b)
    ImageDraw.Draw(im).text((6, 4), f'{t:.0f}', fill=(255, 255, 0), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
    tiles.append(im)
c = 5
r = (len(tiles) + c - 1) // c
s = Image.new('RGB', (c * 420, r * 244))
for i, im in enumerate(tiles):
    s.paste(im, ((i % c) * 420, (i // c) * 244))
s.save(P / 'work' / out, quality=82)
print(out)
