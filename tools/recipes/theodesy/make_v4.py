"""v4 (Aly 2026-10-09): his cut-out the whole short (aly_full_<n>.webm from faces_full.py), his ORIGINAL voice with no
processing at all (audio of final.mp4 as is), the original CTA clip, the same scenes + sound effects (lower, because the
raw voice is ~7 dB quieter than the podcast version). -> public/projects/<code>/short_<n>_v4.json
Render: V=v4 sh work/scripts/render.sh <n>
Run: python work/scripts/make_v4.py <n ...>"""
import glob, json, subprocess, sys
from pathlib import Path
import numpy as np, cv2
W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
CODE = P.name
PUB = ROOT / 'motion-library' / 'public' / 'projects' / CODE
SRC = glob.glob(str(P / 'input' / '*Odesy' / 'final.mp4'))[0]
orig = PUB / 'voice_original.m4a'
if not orig.exists():  # untouched audio stream of his final edit
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-vn', '-c:a', 'copy', str(orig)], check=True)
FF = json.load(open(W / 'faces_full.json', encoding='utf8'))


def face_of(webm, dur):
    """median haar face (x, y, width) over a few frames of the cut-out, as fractions of the 1080 square."""
    det = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    hits = []
    for t in np.linspace(1, dur - 1, 9):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-c:v', 'libvpx-vp9', '-ss', f'{t:.2f}', '-i', str(webm), '-frames:v', '1',
                              '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], capture_output=True).stdout
        if len(raw) < 1080 * 1080 * 4:
            continue
        a = np.frombuffer(raw, np.uint8).reshape(1080, 1080, 4).astype(float)
        rgb = a[..., :3] * (a[..., 3:] / 255) + 128 * (1 - a[..., 3:] / 255)
        g = cv2.cvtColor(rgb.astype(np.uint8), cv2.COLOR_RGB2GRAY)
        fs = det.detectMultiScale(g, 1.1, 6, minSize=(110, 110))
        if len(fs):
            x, y, w, h = max(fs, key=lambda r: r[2])
            hits.append(((x + w / 2) / 1080, (y + h / 2) / 1080, w / 1080 * 1.05))
    return [round(float(np.median([h[i] for h in hits])), 3) for i in range(3)] if hits else [0.5, 0.3, 0.32]


for n in [int(x) for x in sys.argv[1:]]:
    v = json.load(open(PUB / f'short_{n}.json', encoding='utf8'))
    full = FF[str(n)]
    main = v['cta']['tl']
    v['voice'] = f'projects/{CODE}/voice_original.m4a'
    v['aly'] = [{'file': full['file'], 'at': 0, 'dur': round(main, 3), 'from': 0, 'mode': 'full',
                 'face': face_of(ROOT / 'motion-library' / 'public' / full['file'], full['dur'])}]
    v['layout'] = 'v4'
    v['capBottom'] = 0.035
    v['sfxGain'] = 0.9
    v['cta'] = dict(v['cta'], file=f'projects/{CODE}/cta.mp4')
    v['ctaVol'] = 0.75  # plain gain so the original CTA clip sits at the level of his original voice
    json.dump(v, open(PUB / f'short_{n}_v4.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(n, 'face', v['aly'][0]['face'])
