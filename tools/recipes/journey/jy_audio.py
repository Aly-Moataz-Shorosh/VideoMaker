"""Audio helpers for the Journey series (one source video per short, ep = '08', '33', '37'...).
fit(ep, a, b, prev, nxt) = range edges on the WAVEFORM (never inside a word; same rule as graphictablet/edges.py).
voice(ep, segs) = his original audio of the kept pieces, GAIN ONLY (per sentence to one level), never cleaned."""
import glob, json, subprocess
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parents[2]
SR = 48000
TARGET = -14.0
_cache = {}
# His CLEAN voice files (no music / no film audio under it) from F:\..\Aly Shorosh NEW, aligned to his published video by
# envelope cross-correlation: voice_t = video_t + off, piecewise where his edit cut the recording (list of (video_from, off)).
VOICE = {
    '08': ('assets/his/6-vectors FIXED.mp3', [(0, -4.15)]),
    '32': ('assets/his/oz_audio/e1 orginal v1.mp3', [(0.0, -30.16), (60.27, -29.87), (65.71, -29.17), (79.58, 24.5)]),
    '34': ('assets/his/oz_audio/e3 orginal v1.mp3', [(0.0, 12.67), (12.29, 25.11), (42.66, 60.71), (74.21, 64.86), (87.14, 72.7), (111.84, 133.5), (124.72, 153.31), (130.65, 154.42), (145.77, 161.96)]),
    # Aly 2026-10-23: chapters 4 and 5 (shorts 35-40) keep the PUBLISHED sound WITH its music (the cleaned voice sounded uneven/bad)
    '_35': ('assets/his/oz_audio/e4 orginal v1.mp3', [(0.0, 277.13), (9.8, 0.03), (25.84, 0.91), (31.5, 27.28), (40.5, 39.55), (62.25, 58.61), (72.07, 75.21), (82.5, 91.23), (127.71, 129.23), (137.15, 150.74), (162.5, 188.86), (181.16, 193.47), (186.21, 242.23), (202.71, 248.66), (211.58, 260.0), (216.29, 295.66)]),
    '_36': ('assets/his/oz_audio/e5 orginal v1.mp3', [(0.0, 12.08), (28.65, 49.96), (44.52, 59.95), (49.7, 94.5), (82.55, 98.65), (96.69, 105.73), (106.75, 151.44), (123.04, 196.34), (127.85, 237.49), (138.35, 247.43), (152.09, 268.83), (159.92, 298.76), (171.17, 338.69), (184.54, 389.49), (208.72, 398.61), (213.04, 402.58), (218.97, 407.61), (225.21, 411.99), (231.1, 498.22), (241.62, 502.66), (250.7, 513.54), (256.71, 517.16), (261.0, 523.13), (267.05, 572.81)]),
    '33': ('assets/his/oz_audio/e2 orginal v1.mp3', [(0, -8.44), (42.39, 98.24), (87.24, 98.42), (108.30, 166.46), (117.60, 166.18), (139.15, 189.26), (153.34, 193.88)]),
}
# the other هو ايه episodes whose clean voice matches the episode with ONE offset (align_huwa.py); edited ones keep the video audio
for _ep, _v in json.load(open(P / 'work' / 'huwa_voice.json', encoding='utf8')).items():
    VOICE.setdefault(_ep, (_v['file'], [(0, _v['off'])]))


def src(ep):
    return Path(glob.glob(str(P / 'input' / f'{ep}_*.mp4'))[0])


def transcript(ep):
    return json.load(open(P / 'work' / 'tr' / ep / 'transcript.json', encoding='utf8'))


def _db(ep):
    if ('db', ep) not in _cache:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(src(ep)), '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True, check=True).stdout
        a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
        _cache[('db', ep)] = 20 * np.log10(np.sqrt(np.convolve(a ** 2, np.ones(160) / 160, 'same')[::160]) + 1e-9)
    return _cache[('db', ep)]


def fit(ep, a, b, prev=None, nxt=None):
    db = _db(ep)

    def thr(t):
        i = int(t * 100)
        return max(-45.0, float(np.percentile(db[max(0, i - 300):i + 300], 15)) + 12)
    th_a, th_b = thr(a), thr(b)
    i = int(a * 100); lo = int(max(a - 0.6, (prev - 0.1) if prev else 0) * 100)
    while i > lo and db[i - 1] > th_a:
        i -= 1
    start = (lo + int(np.argmin(db[lo:int(a * 100) + 1]))) / 100 if (i == lo and db[lo] > th_a) else max(lo, i - 6) / 100
    j = int(b * 100); quiet = 0
    hi = int(min(b + 1.2, (nxt + 0.3) if nxt else b + 1.2) * 100)
    while j < hi and quiet < 15:
        quiet = quiet + 1 if db[j] <= th_b else 0
        j += 1
    if quiet >= 15:
        end = min(hi, j - quiet + 8) / 100
    else:
        k0 = int((b - 0.05) * 100); end = (k0 + int(np.argmin(db[k0:hi]))) / 100
    return round(start, 2), round(end, 2), f'[{a:.2f}->{start:.2f} {db[int(start * 100)]:.0f}dB | {b:.2f}->{end:.2f} {db[int(end * 100)]:.0f}dB{"" if quiet >= 15 else " DIP"}]'


def _pcm(path):
    if ('pcm', str(path)) not in _cache:
        _cache[('pcm', str(path))] = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-vn', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                                                                 capture_output=True, check=True).stdout, np.float32).copy()
    return _cache[('pcm', str(path))]


def take(ep, a, n):
    """n samples of his voice for video time a.. (clean voice file when we have it, else the video's own audio)"""
    if ep not in VOICE:
        x = _pcm(src(ep)); return x[int(a * SR):int(a * SR) + n].copy()
    f, mp = VOICE[ep]; x = _pcm(P / f)
    out = np.zeros(n, np.float32); i = 0
    while i < n:
        t = a + i / SR
        k = max(j for j, (t0, _) in enumerate(mp) if t0 <= t + 1e-6)
        nxt = mp[k + 1][0] if k + 1 < len(mp) else 1e9
        m = min(n - i, int(round((nxt - t) * SR)) or n - i)
        s0 = int(round((t + mp[k][1]) * SR))
        lo = max(0, -s0)  # this part of the video has no raw take before it (silence here; _patch fills it from the video)
        chunk = x[max(0, s0):max(0, s0 + m)][:m - lo]
        out[i + lo:i + lo + len(chunk)] = chunk; i += m
    return _patch(ep, a, out)


def _env(x):
    h = SR // 100; k = len(x) // h
    return np.log(np.sqrt((x[:k * h].reshape(k, h) ** 2).mean(1)) + 1e-4)


def _patch(ep, a, v):
    """Safety net (Oz chapters, many edit cuts): every 1.5 s window where the clean voice does NOT follow the published audio
    (envelope correlation < 0.55 while something is said) is replaced by the published audio itself, at the same loudness,
    with 40 ms fades -> never a wrong word from a wrong piece of the raw take."""
    if not ep.startswith('3'):  # هو ايه episodes use one constant offset, checked by align_huwa.py
        return v
    vid = _pcm(src(ep))[int(a * SR):int(a * SR) + len(v)]
    if len(vid) < len(v):
        return v
    ea, eb = _env(vid), _env(v)
    bad = np.zeros(len(ea), bool)
    for s in range(0, len(ea) - 150, 75):
        x, y = ea[s:s + 150], eb[s:s + 150]
        if y.max() < np.log(1e-3) and x.mean() > np.log(3e-3):  # clean take has NOTHING here but the video speaks (quietly): ch1 opening, Aly 2026-10-23
            bad[s:s + 150] = True; continue
        if max(x.std(), y.std()) < 0.3:
            continue
        if y.std() < 0.3 or np.corrcoef(x, y)[0, 1] < 0.55:
            bad[s:s + 150] = True
    if not bad.any():
        return v
    h = SR // 100
    mask = np.repeat(bad.astype(np.float32), h)[:len(v)]
    mask = np.concatenate([mask, np.zeros(len(v) - len(mask), np.float32)])
    f = int(0.04 * SR); mask = np.convolve(mask, np.ones(f) / f, 'same')
    good = v[mask < 0.01]; g = (np.sqrt((good ** 2).mean()) / max(1e-6, np.sqrt((vid[mask > 0.99] ** 2).mean()))) if len(good) and (mask > 0.99).any() else 1.0
    if not np.isfinite(g) or g < 0.05:  # nothing usable around to match: the video sound as it is (level() evens it later)
        g = 1.0
    return (v * (1 - mask) + vid * g * mask).astype(np.float32)


def _speech_db(x):
    hop = SR // 100; n = len(x) // hop
    if n == 0:
        return None
    fr = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    loud = fr[fr > np.percentile(fr, 85) - 20]
    return float(10 * np.log10(np.mean(10 ** (loud / 10)))) if len(loud) else None


def level(x, cuts):
    edges = [0] + [c for c in cuts if 0.4 * SR < c < len(x) - 0.4 * SR] + [len(x)]
    g = np.ones(len(x), np.float32); gains = []
    for a, b in zip(edges[:-1], edges[1:]):
        r = _speech_db(x[a:b]); gains.append(1.0 if r is None else 10 ** (np.clip(TARGET - r, -10, 16) / 20))
    for k, (a, b) in enumerate(zip(edges[:-1], edges[1:])):
        g[a:b] = gains[k]
    if len(edges) > 2:
        ramp = int(0.06 * SR); g = np.convolve(g, np.ones(ramp) / ramp, 'same').astype(np.float32)
    return x * g, [round(float(20 * np.log10(v)), 1) for v in gains]


def voice(ep, segs, tail, out):
    """segs = [{'src','len'}] -> wav of the pieces in order + `tail` seconds of silence (end card)"""
    bounds = sorted({s['words'][0]['start'] for s in transcript(ep)['sentences'] if s['words']})
    parts, log = [], []
    fade = int(0.012 * SR)
    for s in segs:
        a = s['src']; x = take(ep, a, int(round(s['len'] * SR)))
        # his published mix (music under the voice): ONE gain for the whole piece, never per sentence (the music would pump)
        y, gs = level(x, [int((t - a) * SR) for t in bounds if a < t < a + s['len']] if ep in VOICE else [])
        y[:fade] *= np.linspace(0, 1, fade); y[-fade:] *= np.linspace(1, 0, fade)
        parts.append(y); log.append(gs)
    parts.append(np.zeros(int(tail * SR), np.float32))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'pcm_s16le', str(out)],
                   input=np.concatenate(parts).astype(np.float32).tobytes(), check=True)
    return log
