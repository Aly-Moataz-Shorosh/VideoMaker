"""PICTURE sync QC (Aly 2026-10-21: "الصوت مش ماشي مع الصورة"): for every piece, where is the picture of the short relative to the
source? Frame of the short at st+k vs source frames around a+k (60 fps, 1 s window) -> best match -> offset (s).
Audio is checked by qc_sync.py; both must be ~0, else the short is NOT delivered.
python qc_av.py <video|'strip'> N ...   video = output/shorts/NN_*.mp4 (default) | strip = public vNN.mp4 (before Remotion)"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
P = Path(__file__).resolve().parents[2]
SRC = P / 'input' / 'main video.mp4'
ML = P.parents[2] / 'motion-library'
TILE = (36, 290, 910, 470)   # guest tile in the source (moves the most); for the short we compare against the source strip crop


def frames(src, ss, t, fps, crop):
    x, y, w, h = crop
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{ss:.3f}', '-t', f'{t:.3f}', '-i', str(src), '-vf',
                        f'fps={fps},crop={w}:{h}:{x}:{y},scale=96:50,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(-1, 50, 96).astype(np.float32)


def offsets(vid, crop_short, segs):
    out = []
    for s in segs:
        if s['b'] - s['a'] < 3:
            continue
        for k in np.linspace(1.0, s['b'] - s['a'] - 1.0, 4):
            # 15 frames (0.5 s) of the short slid over the source at 60 fps: robust even when he sits still
            f = frames(vid, s['st'] + k, 0.5, 30, crop_short)[:15]
            ref = frames(SRC, s['a'] + k - 0.5, 1.6, 60, TILE)
            d = [((ref[j:j + 30:2][:len(f)] - f) ** 2).mean() for j in range(0, len(ref) - 30)]
            out.append(round(int(np.argmin(d)) / 60 - 0.5, 3))
    return out


if __name__ == '__main__':
    mode, bad = sys.argv[1], False
    for n in map(int, sys.argv[2:]):
        tl = json.load(open(P / 'work' / 'shorts' / f'tl_{n:02d}.json'))
        if mode == 'strip':
            vid, crop = ML / 'public' / 'projects' / 'entacs01s' / f'v{n:02d}.mp4', (36, 290 - 282, 910, 470)
        else:
            vid, crop = next((P / 'output' / 'shorts').glob(f'{n:02d}_*.mp4')), None
        if crop is None:
            print('final-video check needs a layout-aware crop; use strip'); continue
        o = offsets(vid, crop, tl['segs'])
        out = max(map(abs, o)) > 0.025
        bad |= out
        print(f'short {n} [{mode}]: picture offset ' + ' '.join(f'{x:+.3f}' for x in o) + (' <-- OUT OF SYNC' if out else ' ok'), flush=True)
    sys.exit(1 if bad else 0)
