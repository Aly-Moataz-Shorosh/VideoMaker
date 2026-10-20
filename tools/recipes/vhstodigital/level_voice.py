"""Even voice level (Aly 2026-10-09: "الاصوات مش ثابتة… خلي كل اصواتي في كل المشاهد وكل الفيديوهات بنفس الدرجة اكنهم في مكان واحد").
GAIN ONLY — no EQ, no denoise, no compression (his rule: never "clean" his voice unless he asks).
Each kept piece is split at sentence boundaries; every part gets one gain so its speech RMS hits TARGET (60 ms ramps
between parts); the CTA clip the same; then the whole short gets one gain to -15 LUFS and a peak limit at -1 dBTP.
build(segs, cta, out): segs = [{'src','len'}] in source seconds, cta = (file, src, len) -> out .wav on the short's timeline."""
import json, subprocess
from pathlib import Path
import numpy as np

W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
SRC = P / 'input' / 'vSaO0bRnfz8.mp4'
SR = 48000
TARGET = -14.0  # dBFS RMS of the speech frames
_tr = json.load(open(W / 'transcript.json', encoding='utf8'))
_bounds = sorted({round(s['words'][0]['start'], 2) for s in _tr['sentences'] if s['words']})


def rd(path):
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-vn', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                                        capture_output=True, check=True).stdout, np.float32).copy()


_src = None


def speech_rms_db(x):
    hop = SR // 100
    n = len(x) // hop
    if n == 0:
        return None
    fr = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    loud = fr[fr > np.percentile(fr, 85) - 20]  # speech frames (ignore pauses)
    return float(10 * np.log10(np.mean(10 ** (loud / 10)))) if len(loud) else None


def level(x, cuts):
    """x = audio, cuts = sample positions that split it into parts (sentence starts). Returns x * gain curve."""
    edges = [0] + [c for c in cuts if 0.4 * SR < c < len(x) - 0.4 * SR] + [len(x)]
    g = np.ones(len(x), np.float32); gains = []
    for a, b in zip(edges[:-1], edges[1:]):
        r = speech_rms_db(x[a:b])
        gains.append(1.0 if r is None else 10 ** (np.clip(TARGET - r, -10, 10) / 20))
    for k, (a, b) in enumerate(zip(edges[:-1], edges[1:])):
        g[a:b] = gains[k]
    ramp = int(0.06 * SR)  # smooth the steps
    if len(edges) > 2:
        g = np.convolve(g, np.ones(ramp) / ramp, 'same').astype(np.float32)
    return x * g, [round(float(20 * np.log10(v)), 1) for v in gains]


def build(segs, cta, out):
    global _src
    if _src is None:
        _src = rd(SRC)
    parts, log = [], []
    fade = int(0.012 * SR)
    for s in segs:
        a, b = s['src'], s['src'] + s['len']
        x = _src[int(a * SR):int(b * SR)].copy()
        y, gs = level(x, [int((t - a) * SR) for t in _bounds if a < t < b])
        y[:fade] *= np.linspace(0, 1, fade); y[-fade:] *= np.linspace(1, 0, fade)
        parts.append(y); log.append(gs)
    c = rd(ROOT / 'motion-library' / 'public' / cta[0])[int(cta[1] * SR):int((cta[1] + cta[2]) * SR)]
    cy, cg = level(c, [])
    parts.append(cy); log.append(cg)
    mix = np.concatenate(parts)
    raw = out.with_suffix('.raw.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', str(raw)], input=mix.astype(np.float32).tobytes(), check=True)
    m = subprocess.run(['ffmpeg', '-i', str(raw), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(m.split('Integrated loudness:')[1].split('I:')[1].split('LUFS')[0])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', f'volume={-15 - I:.2f}dB,alimiter=limit=0.89:level=false',
                    '-c:a', 'pcm_s16le', str(out)], check=True)
    raw.unlink()
    return log, I
