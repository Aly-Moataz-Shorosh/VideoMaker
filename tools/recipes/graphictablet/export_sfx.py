"""Sound effects ONLY (no voice, no CTA clip audio) for every short, same timing and levels as the render
(Aly 2026-10-08: "export لل audio بتاع الاصوات بس… من غير صوتي") -> output/sfx_only/short_<n>_sfx.wav
Mixes the props' sfx list exactly like FilmShort.tsx: volume = min(1, vol * sfxGain), dur cut, loop, 6-frame fade out.
Run: python work/scripts/export_sfx.py"""
import json, subprocess
from pathlib import Path
import numpy as np

W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
PUBLIC = ROOT / 'motion-library' / 'public'
PUB = PUBLIC / 'projects' / P.name
SR = 48000
cache = {}


def load(f):
    if f not in cache:
        cache[f] = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(PUBLIC / f), '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                                                capture_output=True, check=True).stdout, np.float32).copy()
    return cache[f]


for tag, suf in (('', ''),):
    out_dir = P / 'output' / (tag or '') / 'sfx_only'
    out_dir.mkdir(parents=True, exist_ok=True)
    for n in sorted(int(p.stem.split('_')[1]) for p in PUB.glob('short_*.json') if p.stem.count('_') == 1):
        props = json.load(open(PUB / f'short_{n}{suf}.json', encoding='utf8'))
        mix = np.zeros(int(props['duration'] * SR) + SR, np.float32)
        gain = props.get('sfxGain', 1)
        for s in props['sfx']:
            x = load(s['file'])
            dur = s.get('dur', 3.0)
            L = int(dur * SR)
            if s.get('loop'):
                x = np.tile(x, L // len(x) + 1)
            x = x[:L].copy()
            fade = int(6 / 30 * SR)
            if len(x) >= L:
                x[-fade:] *= np.linspace(1, 0, fade)
            a = int(s['at'] * SR)
            x = x[:len(mix) - a] * min(1.0, s.get('vol', 0.5) * gain)
            mix[a:a + len(x)] += x
        mix = mix[:int(props['duration'] * SR)]
        peak = float(np.abs(mix).max())
        if peak > 0.98:
            mix *= 0.98 / peak
        out = out_dir / f'short_{n}_sfx.wav'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-ac', '2', '-c:a', 'pcm_s16le', str(out)],
                       input=mix.tobytes(), check=True)
        print(tag, out.name, f"{props['duration']:.1f}s", len(props['sfx']), 'sounds', f'peak {20 * np.log10(peak + 1e-9):.1f} dB')
