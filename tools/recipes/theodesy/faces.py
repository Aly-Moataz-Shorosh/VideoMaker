"""(raw clips are HLG HDR -> tonemapped hable, close to his final look)
Aly's face moments per short (source seconds in final.mp4) -> clean cut-outs from the RAW clips (no overlays).
1. find each window in the raw clips by audio cross-correlation (both halves must agree = no jump cut inside),
2. face x via haar on the middle frame, 3. crop a 1080x1080 square around him, 4. tools/matte.py -> alpha webm.
Writes motion-library/public/projects/<code>/aly_<short>_<k>.webm + work/faces.json. Run: python faces.py [short ...]"""
import glob, json, subprocess, sys, os
from pathlib import Path
import math
import numpy as np, cv2
W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
sys.stdout.reconfigure(encoding='utf-8')
CODE = P.name
PUB = ROOT / 'motion-library' / 'public' / 'projects' / CODE; PUB.mkdir(parents=True, exist_ok=True)
IN = Path(glob.glob(str(P / 'input' / '*Odesy'))[0])
FACES = {
    1: [[46.55, 50.6], [595.9, 600.4], [618.5, 623.09]],
    2: [[81.27, 85.3], [100.6, 103.0], [122.0, 126.86]],
    3: [[126.86, 131.0], [164.6, 167.7], [182.9, 187.3]],
    4: [[187.39, 191.5], [231.0, 234.3], [252.8, 256.59]],
    5: [[256.59, 262.5], [315.8, 320.0], [338.5, 341.87]],
    6: [[341.87, 345.8], [360.0, 363.6], [386.2, 389.81]],
    7: [[389.81, 395.0], [407.9, 413.0], [455.0, 460.0]],
    8: [[460.0, 464.5], [522.6, 527.5], [550.27, 553.52]],
    9: [[623.09, 627.5], [658.5, 662.2], [694.5, 699.61]],
    10: [[716.55, 721.5], [765.0, 768.5], [785.0, 790.15]],
}
SR = 4000
def audio(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(r, np.int16).astype(np.float32) / 32768
final = audio(IN / 'final.mp4')
RAWS = sorted(IN.glob('20260718_*.mp4'))
raw = {p: audio(p) for p in RAWS}
def grade(crop_bgr, target=0.44, sat=1.35):
    """Car clips look washed out next to the home clips (Aly 2026-10-08): black/white points from the crop,
    gamma so his face lands at `target`, more saturation and a bit of contrast."""
    a = crop_bgr[..., ::-1].astype(float) / 255
    y = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    lo, hi = np.percentile(y, 1.5), np.percentile(y, 99.5)
    m = (y[300:700, 350:750].mean() - lo) / (hi - lo)
    g = math.log(target) / math.log(min(0.95, max(0.05, m)))
    lv = ':'.join(f'{c}imin={lo:.3f}:{c}imax={hi:.3f}' for c in 'rgb')
    return f',colorlevels={lv},eq=gamma={1 / g:.3f}:saturation={sat}:contrast=1.06'


def locate(a, b):
    """-> (raw path, raw start sec, score) for final[a:b]."""
    q = final[int(a * SR):int(b * SR)]; q = (q - q.mean()) / (q.std() + 1e-9)
    best = (None, 0, -1)
    for p, r in raw.items():
        n = 1 << int(np.ceil(np.log2(len(r) + len(q))))
        c = np.fft.irfft(np.fft.rfft(r, n) * np.conj(np.fft.rfft(q, n)), n)[:len(r) - len(q)]
        cs = np.concatenate([[0.0], np.cumsum(r.astype(np.float64) ** 2)])  # window energy via cumulative sum (convolve was minutes)
        e = np.sqrt(np.maximum(cs[len(q):len(q) + len(c)] - cs[:len(c)], 0)) + 1e-9
        c = c / e / np.sqrt(len(q)); k = int(np.argmax(c))
        if c[k] > best[2]: best = (p, k / SR, float(c[k]))
    return best
out = json.load(open(W / 'faces.json', encoding='utf8')) if (W / 'faces.json').exists() else {}
todo = [int(x) for x in sys.argv[1:]] or list(FACES)
for n in todo:
    res = []
    for k, (a, b) in enumerate(FACES[n]):
        m = (a + b) / 2
        p1, s1, c1 = locate(a, m); p2, s2, c2 = locate(m, b)
        ok = p1 == p2 and abs((s2 - s1) - (m - a)) < 0.06
        if not ok:  # jump cut inside: keep the longer consistent half
            print(f'  short {n} win {k}: cut inside ({p1.name if p1 else None} {s1:.2f} / {p2.name if p2 else None} {s2:.2f}) -> half')
            if c2 > c1: a, p1, s1 = m, p2, s2
            else: b = m
        rs = s1
        fr = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{rs + (b - a) / 2:.2f}', '-i', str(p1), '-frames:v', '1', '-vf', 'zscale=t=linear:npl=150,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
        img = cv2.imdecode(np.frombuffer(fr, np.uint8), cv2.IMREAD_COLOR); h, w = img.shape[:2]
        fs = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(
            cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 1.1, 6, minSize=(int(h * 0.12),) * 2)
        f = max(fs, key=lambda r: r[2]) if len(fs) else None
        cx = int(f[0] + f[2] / 2) if f is not None else int(w * (0.46 if p1.name < '20260718_165' else 0.5))
        fy = int(f[1] + f[3] / 2) if f is not None else h // 3
        x0 = max(0, min(w - h, cx - h // 2))
        gr = grade(img[:, x0:x0 + h]) if p1.name < '20260718_165' else ''  # car clips only
        name = f'aly_{n}_{k}.webm'
        tmp = W / f'tmp_crop_{n}_{k}.mp4'
        if not (PUB / name).exists():
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{rs:.3f}', '-i', str(p1), '-t', f'{b - a:.3f}', '-vf', f'zscale=t=linear:npl=150,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,crop={h}:{h}:{x0}:0{gr},fps=30',
                            '-an', '-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast', str(tmp)], check=True)
            subprocess.run([sys.executable, str(ROOT / 'tools' / 'matte.py'), str(tmp), '0', f'{b - a:.3f}', str(PUB / name)], check=True)
            tmp.unlink()
        res.append({'src': round(a, 3), 'end': round(b, 3), 'file': f'projects/{CODE}/{name}', 'raw': p1.name, 'rawStart': round(rs, 3),
                    'score': round(c1, 2), 'face': [round((cx - x0) / h, 3), round(fy / h, 3)], 'faceW': round(float(f[2]) / h, 3) if f is not None else 0, 'grade': gr})
        print(n, k, res[-1], flush=True)
    out[str(n)] = res
    json.dump(out, open(W / 'faces.json', 'w', encoding='utf8'), indent=1)
