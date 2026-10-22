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
    '33': ('assets/his/oz_audio/e2 orginal v1.mp3', [(0, -8.44), (42.39, 98.24), (87.24, 98.42), (108.30, 166.46), (117.60, 166.18), (139.15, 189.26), (153.34, 193.88)]),
}


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
        s0 = int(round((t + mp[k][1]) * SR)); chunk = x[max(0, s0):s0 + m]
        out[i:i + len(chunk)] = chunk; i += m
    return out


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
        r = _speech_db(x[a:b]); gains.append(1.0 if r is None else 10 ** (np.clip(TARGET - r, -10, 10) / 20))
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
        y, gs = level(x, [int((t - a) * SR) for t in bounds if a < t < a + s['len']])
        y[:fade] *= np.linspace(0, 1, fade); y[-fade:] *= np.linspace(1, 0, fade)
        parts.append(y); log.append(gs)
    parts.append(np.zeros(int(tail * SR), np.float32))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'pcm_s16le', str(out)],
                   input=np.concatenate(parts).astype(np.float32).tobytes(), check=True)
    return log
