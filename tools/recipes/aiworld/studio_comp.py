"""Put Aly (cut out of the HeyGen avatar with RVM, his pixels untouched by any AI) into a generated EMPTY studio plate,
with light that belongs to the room (Aly 2026-11-21: "حاسس اني مقصوص").
Per frame:  edge refine -> colour/contrast transfer toward the plate -> directional key from the plate's bright side
            -> rim light in the plate's colours -> light wrap -> soft shadow on the chair/wall -> same grain on both.
comp(fg_rgba[H,W,4] float 0-1, plate_rgb[H,W,3] float 0-1, seed) -> rgb float 0-1
Usage (stills): python -X utf8 work/scripts/studio_comp.py <matte.png> <plate.png> <out.png>"""
import sys
import numpy as np
from PIL import Image, ImageFilter

def _blur(x, r):
    if x.ndim == 2:
        return np.asarray(Image.fromarray((np.clip(x, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255
    return np.stack([_blur(x[..., c], r) for c in range(x.shape[2])], -1)

def _lab_stats(rgb, w):
    w = w / (w.sum() + 1e-6)
    m = (rgb * w[..., None]).sum((0, 1)); s = np.sqrt((((rgb - m) ** 2) * w[..., None]).sum((0, 1))) + 1e-6
    return m, s

def comp(fg, plate, seed=0, key_strength=0.10, rim=0.55, wrap=0.30, shadow=0.35, grade=0.35,
         feather=0.8, erode=0.6, target=None, lightmap=None):
    """target = (mean, std) of HOW HE SHOULD LOOK in this room (from the generated still of him in it) -> his colours
    go there instead of toward the room average. lightmap[H,W,3] = low-frequency light of the generated version
    divided by his real frame (the 'mix': his real face, the generated light)."""
    H, W = plate.shape[:2]
    rgb, a = fg[..., :3], fg[..., 3]
    # 1. edges: tiny shrink + light feather (Aly 2026-11-21: not a high feather)
    a_er = np.minimum(a, 1 - _blur((a < 0.98).astype(np.float32), 1.2) * erode)
    a2 = _blur(a_er, feather) if feather > 0 else a_er
    # 2. colour + contrast toward the plate (partial: his skin stays his skin) or toward the generated him
    pm, ps = _lab_stats(plate, np.ones((H, W), np.float32))
    fm, fs = _lab_stats(rgb, a)
    if target is not None:
        tm, ts = target
        tgt = (rgb - fm) / fs * (fs + (ts - fs) * grade) + (fm + (tm - fm) * grade)
    else:
        tgt = (rgb - fm) / fs * (fs + (ps - fs) * grade * 0.5) + (fm + (pm - fm) * grade)
    rgb2 = np.clip(tgt, 0, 1)
    if lightmap is not None:
        rgb2 = np.clip(rgb2 * lightmap, 0, 1)
    # 2b. light swap: the cold window light of his real room (blue on one cheek) becomes the room's own light colour
    cool = np.clip((rgb2[..., 2] - rgb2[..., 0]) * 4, 0, 1) * a
    lumv = rgb2.mean(-1, keepdims=True)
    tone = pm / (pm.mean() + 1e-6)
    rgb2 = rgb2 * (1 - 0.7 * cool[..., None]) + np.clip(lumv * tone, 0, 1) * 0.7 * cool[..., None]
    # 3. directional key: which side of the room is brighter (lamps / softbox) -> gentle gain across his body
    lum = plate.mean(-1)
    left, right = lum[:, : W // 3].mean(), lum[:, -W // 3:].mean()
    side = np.clip((left - right) * 4, -1, 1)          # +1 = light from the left
    xs = np.linspace(1, -1, W)[None, :]                 # +1 on the left edge
    ys = np.linspace(1, -1, H)[:, None] * 0.35           # a bit more light from above
    gain = 1 + key_strength * (side * xs + ys)
    rgb3 = np.clip(rgb2 * gain[..., None], 0, 1)
    # 4. rim light: thin band inside his outline, coloured by the blurred plate, stronger on the bright side
    band = np.clip(a2 - _blur(a2, 9) * 1.0, 0, 1) * 2.5
    band *= np.clip(0.55 + 0.45 * side * xs, 0.1, 1)
    room = _blur(plate, 40)
    rgb4 = 1 - (1 - rgb3) * (1 - np.clip(band[..., None] * rim, 0, 1) * room * 1.6)   # screen
    # 5. light wrap: the room's light bleeding onto his edges
    edge = np.clip((1 - _blur(a2, 14)) * a2 * 2.0, 0, 1)[..., None]
    rgb5 = rgb4 * (1 - wrap * edge) + room * wrap * edge
    # 6. soft shadow of him on the chair / wall behind (offset away from the key side, very soft)
    dx = int(-side * 40); dy = 18
    sh = np.roll(np.roll(_blur(a2, 30), dy, 0), dx, 1)
    bg = plate * (1 - shadow * sh[..., None] * (1 - a2[..., None]))
    out = rgb5 * a2[..., None] + bg * (1 - a2[..., None])
    # 7. the same fine grain over everything (sensor noise ties the two layers together)
    g = np.random.default_rng(seed).normal(0, 0.012, (H, W, 1)).astype(np.float32)
    return np.clip(out + g, 0, 1)

def load_plate(path, W, H, dof=1.6):
    p = Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(dof))
    return np.asarray(p).astype(np.float32) / 255

if __name__ == "__main__":
    fg = np.asarray(Image.open(sys.argv[1]).convert("RGBA")).astype(np.float32) / 255
    H, W = fg.shape[:2]
    out = comp(fg, load_plate(sys.argv[2], W, H))
    Image.fromarray((out * 255).astype(np.uint8)).save(sys.argv[3])
    print("ok", sys.argv[3])
