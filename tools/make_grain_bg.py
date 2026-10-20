"""Grainy / stippled motion-graphics background textures (Aly 2026-10-08: "noise/grain like these references" —
risograph-style dotted shading, not a faint noise). Writes PNG layers that Edit's GrainBg moves/cycles:
  base.png     two-blue gradient with stippled (dithered) shading
  blob_1..4    big soft shapes whose edges dissolve into dots (parallax layers)
  grain_0..2   strong speckle overlay (light + dark dots), cycled every 2 frames = film "boil"
Usage: python tools/make_grain_bg.py <out_dir> [w h] [--main #1D5C96 --dark #0A2442 --light #3E86C9]"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
W, H = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 and sys.argv[2].isdigit() else (1080, 1920)
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
hexc = lambda h: np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32)
MAIN, DARK, LIGHT = hexc(arg('--main', '#1D5C96')), hexc(arg('--dark', '#0A2442')), hexc(arg('--light', '#3E86C9'))
GOLD = hexc('#F5B83D')
rng = np.random.default_rng(7)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)


def stipple(p):
    """p in 0..1 -> dotted mask (each pixel on with probability p): the grainy-gradient look."""
    return (rng.random(p.shape, dtype=np.float32) < np.clip(p, 0, 1)).astype(np.float32)


def save(rgb, a, name):
    Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.clip(a * 255, 0, 255)]).astype(np.uint8)).save(out / name, optimize=True)


# base: main blue, darker toward the bottom-right with stippled transition, lighter dotted glow top-left
t = np.clip((xx / W * 0.35 + yy / H * 0.85) - 0.2, 0, 1)
dark = stipple(t ** 1.3)[..., None]
glow = stipple(np.clip(1 - np.hypot(xx / W - 0.25, yy / H - 0.18) * 2.2, 0, 1) ** 1.5 * 0.85)[..., None]
base = MAIN * (1 - dark) + DARK * dark
base = base * (1 - glow) + LIGHT * glow
Image.fromarray(base.astype(np.uint8)).save(out / 'base.png', optimize=True)

# blobs: circles / waves with a dotted shadow side (light from top-left)
specs = [  # (cx, cy, r, color, shade color)
    (0.85, 0.22, 0.42, LIGHT * 1.25, MAIN), (0.08, 0.62, 0.36, DARK, MAIN), (0.7, 0.86, 0.3, MAIN * 0.8 + LIGHT * 0.2, DARK),
    (0.93, 0.6, 0.05, GOLD, GOLD * 0.6)]
for i, (cx, cy, r, col, sh) in enumerate(specs, 1):
    d = np.hypot((xx / W - cx) * W / H, yy / H - cy) / r  # 0 at center, 1 at edge (in height units)
    inside = (d < 1).astype(np.float32)
    edge = stipple(np.clip((1.05 - d) / 0.05, 0, 1)) * (d >= 1 - 0.02)  # dotted rim dissolving outward
    shade = stipple(np.clip(((xx / W - cx) * 0.8 + (yy / H - cy)) / r + 0.2, 0, 1) ** 1.2)  # dotted shadow side
    rgb = (col * (1 - shade[..., None]) + sh * shade[..., None]) * np.ones((H, W, 1), np.float32)
    save(rgb, np.maximum(inside, edge) * (0.9 if i < 4 else 0.85), f'blob_{i}.png')

# grain overlay: dense light + dark speckles (strong, visible like the references)
for k in range(3):
    r1 = rng.random((H, W), dtype=np.float32)
    light, darkd = (r1 < 0.07).astype(np.float32), (r1 > 0.93).astype(np.float32)
    rgb = np.where(light[..., None] > 0, 235, 4) * np.ones((H, W, 3), np.float32)
    save(rgb, (light * 0.55 + darkd * 0.45), f'grain_{k}.png')
print('textures ->', out)
