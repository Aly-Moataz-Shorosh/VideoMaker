# One pass over the 720p session recording (2 fps, 320 px): screen change per sample + audio level per 0.1 s.
# Writes work/analysis.json. Also writes contact sheets work/sheets/sheet_NNN.jpg (one frame every 10 s, 6x5 per sheet, time printed).
#   python analyze.py
import json, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

PROJ = Path(__file__).resolve().parents[2]
SRC = PROJ / 'input/2021-03-28 20-26-18_1.mp4'
W, H, FPS = 320, 180, 2
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(SRC), '-vf', f'fps={FPS},scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
prev, dif, frames, i = None, [], [], 0
while True:
    b = p.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    a = np.frombuffer(b, np.uint8).reshape(H, W, 3)
    g = a.mean(2)
    dif.append(round(float(np.abs(g - prev).mean()), 2) if prev is not None else 0)
    prev = g
    if i % (10 * FPS) == 0: frames.append((i / FPS, Image.fromarray(a.copy())))
    i += 1
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(SRC), '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
n = len(x) // 1600
rms = 20 * np.log10(np.sqrt((x[: n * 1600].reshape(n, 1600) ** 2).mean(1)) + 1e-9)
json.dump(dict(fps=FPS, diff=dif, rms_step=0.1, rms=[round(float(v), 1) for v in rms]), open(PROJ / 'work/analysis.json', 'w'))
for k in range(0, len(frames), 30):
    sheet = Image.new('RGB', (W * 6, H * 5), 'black')
    d = ImageDraw.Draw(sheet)
    for j, (t, im) in enumerate(frames[k:k + 30]):
        x0, y0 = (j % 6) * W, (j // 6) * H
        sheet.paste(im, (x0, y0))
        d.rectangle((x0, y0, x0 + 60, y0 + 14), fill='black'); d.text((x0 + 2, y0 + 1), f'{int(t // 60)}:{int(t % 60):02d}', fill='yellow')
    sheet.save(PROJ / f'work/sheets/sheet_{k // 30:03d}.jpg', quality=80)
print('samples', len(dif), 'sheets', (len(frames) + 29) // 30)
