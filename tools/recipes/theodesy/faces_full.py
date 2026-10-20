"""v4 (Aly 2026-10-09): his cut-out visible for the WHOLE short. For every short range, rebuild his edit from the RAW
clips (no overlays): 0.5 s windows located in the raw clips by audio correlation, jump cuts refined to 20 ms, gaps that
are not in any raw clip (inserted sounds) hold the previous segment. Pieces are tonemapped (HLG -> SDR), car clips get
ONE grade per raw clip (no flicker), cropped to a fixed 1080 square per clip, joined in timeline order and matted
(tools/matte.py) -> public/projects/<code>/aly_full_<n>.webm + work/faces_full.json.
Run: python work/scripts/faces_full.py [n ...]"""
import glob, json, math, subprocess, sys
from pathlib import Path
import numpy as np, cv2
W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
sys.stdout.reconfigure(encoding='utf-8')
CODE = P.name
PUB = ROOT / 'motion-library' / 'public' / 'projects' / CODE
IN = Path(glob.glob(str(P / 'input' / '*Odesy'))[0])
TM = 'zscale=t=linear:npl=150,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p'
SR = 4000
R = {int(k): v for k, v in json.load(open(W / 'ranges.json')).items()}
R[1][2][1] = 622.28; R[3][0][1] = 187.3; R[4][0][1] = R[5][0][0] = 256.42; R[9][0][0] = 622.28  # same overrides as make_shorts


def audio(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(r, np.int16).astype(np.float32) / 32768


final = audio(IN / 'final.mp4')
RAWS = sorted(IN.glob('20260718_*.mp4'))
raw = {p: audio(p) for p in RAWS}
cums = {p: np.concatenate([[0.0], np.cumsum(r.astype(np.float64) ** 2)]) for p, r in raw.items()}


def nc(q, p, off):
    """normalised correlation of final chunk q with raw clip p at sample offset off."""
    r = raw[p]
    if off < 0 or off + len(q) > len(r):
        return -1
    s = r[off:off + len(q)]
    return float(np.dot(q - q.mean(), s - s.mean()) / (np.linalg.norm(q - q.mean()) * np.linalg.norm(s - s.mean()) + 1e-9))


def search(q):
    best = (None, 0, -1.0)
    qn = (q - q.mean()) / (q.std() + 1e-9)
    for p, r in raw.items():
        n = 1 << int(np.ceil(np.log2(len(r) + len(qn))))
        c = np.fft.irfft(np.fft.rfft(r, n) * np.conj(np.fft.rfft(qn, n)), n)[:len(r) - len(qn)]
        cs = cums[p]
        e = np.sqrt(np.maximum(cs[len(qn):len(qn) + len(c)] - cs[:len(c)], 0)) + 1e-9
        c = c / e / np.sqrt(len(qn)); k = int(np.argmax(c))
        if c[k] > best[2]:
            best = (p, k, float(c[k]))
    return best


def segments(a, b, win=0.5):
    """[(final_start, final_end, raw_path|None, delta)] where raw_time = final_time + delta."""
    wins, prev = [], None
    t = a
    while t < b - 0.05:
        e = min(b, t + win)
        q = final[int(t * SR):int(e * SR)]
        hit = None
        if prev and prev[0]:
            off = int((t + prev[1]) * SR)
            if nc(q, prev[0], off) > 0.8:
                hit = prev
        if not hit:
            p, k, c = search(q)
            hit = (p, k / SR - t) if c > 0.6 else (None, 0)
        wins.append((t, e, hit)); prev = hit if hit[0] else prev
        t = e
    # merge equal neighbours, refine boundaries to 20 ms
    segs = []
    for t, e, h in wins:
        if segs and (h[0] is None or (segs[-1][2] == h[0] and abs(segs[-1][3] - h[1]) < 0.04)):
            segs[-1][1] = e
            continue
        if segs and h[0]:
            pa, da = segs[-1][2], segs[-1][3]
            best, bt = -9, t
            for x in np.arange(t - win, t + 0.001, 0.02):  # boundary that best explains both sides (0.25 s each)
                qa = final[int((x - 0.25) * SR):int(x * SR)]; qb = final[int(x * SR):int((x + 0.25) * SR)]
                sc = nc(qa, pa, int((x - 0.25 + da) * SR)) + nc(qb, h[0], int((x + h[1]) * SR))
                if sc > best: best, bt = sc, x
            segs[-1][1] = bt; t = bt
        segs.append([t, e, h[0], h[1]])
    if segs and segs[0][2] is None:  # leading unknown -> use the next segment
        nxt = next((s for s in segs if s[2]), None)
        if nxt: segs[0][2], segs[0][3] = nxt[2], nxt[3]
    return segs


GRADE = {}


def grade_for(p):
    """one grade per car clip (from its middle frame), none for the home clip."""
    if p.name >= '20260718_165':
        return ''
    if p not in GRADE:
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout)
        fr = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{dur / 2:.1f}', '-i', str(p), '-frames:v', '1', '-vf', TM + f',crop=1080:1080:{X0[p.name]}:0',
                             '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
        a = cv2.imdecode(np.frombuffer(fr, np.uint8), cv2.IMREAD_COLOR)[..., ::-1].astype(float) / 255
        y = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
        lo, hi = np.percentile(y, 1.5), np.percentile(y, 99.5)
        m = (y[300:700, 350:750].mean() - lo) / (hi - lo)
        g = math.log(0.44) / math.log(min(0.95, max(0.05, m)))
        lv = ':'.join(f'{c}imin={lo:.3f}:{c}imax={hi:.3f}' for c in 'rgb')
        GRADE[p] = f',colorlevels={lv},eq=gamma={1 / g:.3f}:saturation=1.35:contrast=1.06'
    return GRADE[p]


X0 = {'20260718_161737.mp4': 343, '20260718_162713.mp4': 343, '20260718_164103.mp4': 343, '20260718_165537.mp4': 420, '20260718_170136.mp4': 420}
out = json.load(open(W / 'faces_full.json', encoding='utf8')) if (W / 'faces_full.json').exists() else {}
tmp = W / 'tmp_full'; tmp.mkdir(exist_ok=True)
for n in [int(x) for x in sys.argv[1:]] or range(1, 11):
    pieces, info = [], []
    for a, b in R[n]:
        for s in segments(a, b):
            info.append([round(s[0], 3), round(s[1], 3), s[2].name if s[2] else None, round(s[3], 3)])
    # pieces, frame-exact on the 30 fps timeline
    tl = 0.0; k = 0
    for fa, fb, name, d in info:
        p = IN / name
        f0, f1 = round(tl * 30), round((tl + fb - fa) * 30)
        nfr = f1 - f0; tl += fb - fa
        if nfr <= 0:
            continue
        piece = tmp / f'p{k:04d}.mp4'; k += 1
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{fa + d:.3f}', '-i', str(p), '-frames:v', str(nfr), '-an',
                        '-vf', TM + f',crop=1080:1080:{X0[name]}:0' + grade_for(p) + ',fps=30', '-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast',
                        '-pix_fmt', 'yuv420p', str(piece)], check=True)
        pieces.append(piece)
    lst = tmp / 'list.txt'
    lst.write_text('\n'.join(f"file '{x.name}'" for x in pieces), encoding='utf8')
    joined = tmp / f'joined_{n}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c', 'copy', str(joined)], check=True)
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(joined)], capture_output=True, text=True).stdout)
    webm = PUB / f'aly_full_{n}.webm'
    subprocess.run([sys.executable, str(ROOT / 'tools' / 'matte.py'), str(joined), '0', f'{dur:.3f}', str(webm)], check=True)
    for x in pieces + [lst, joined]:
        x.unlink()
    unknown = sum(1 for s in info if s[2] is None)
    out[str(n)] = {'file': f'projects/{CODE}/aly_full_{n}.webm', 'dur': round(dur, 3), 'segments': info}
    json.dump(out, open(W / 'faces_full.json', 'w', encoding='utf8'), indent=1)
    print(f'short {n}: {len(info)} pieces ({unknown} not in raw), {dur:.1f}s -> {webm.name}', flush=True)
