"""sheet2.py <out.jpg> <url> [t1 t2 ...]  -> frames at given seconds (or 12 evenly) in a 4-col sheet, no download."""
import io, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
out, url, ts = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3:]]
info = subprocess.run([sys.executable, '-m', 'yt_dlp', '--js-runtimes', 'node', '-f', 'b[height<=480]/bv[height<=480]/b', '-g',
                       '--print', 'duration', '--print', 'title', url], capture_output=True, text=True)
lines = info.stdout.strip().split('\n')
dur, title, src = (float(lines[0]) if lines[0] != 'NA' else 40.0), lines[1], lines[2]
if not ts: ts = [dur * (i + 0.5) / 12 for i in range(12)]
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
imgs = []
for t in ts:
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.1f}', '-i', src, '-frames:v', '1', '-vf', 'scale=-2:300',
                        '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, timeout=120)
    if r.stdout:
        im = Image.open(io.BytesIO(r.stdout)).convert('RGB'); ImageDraw.Draw(im).text((4, 4), f'{int(t)//60}:{int(t)%60:02d}', fill='yellow', font=font); imgs.append(im)
W = max(i.width for i in imgs); C = 4 if W < 300 else 3; R = (len(imgs) + C - 1) // C
sheet = Image.new('RGB', (W * C, 300 * R + 24), (20, 20, 20))
ImageDraw.Draw(sheet).text((4, 4), title[:90], fill='white', font=font)
for k, im in enumerate(imgs): sheet.paste(im, ((k % C) * W, 24 + (k // C) * 300))
sheet.save(out, quality=80); print(out, title, dur)
