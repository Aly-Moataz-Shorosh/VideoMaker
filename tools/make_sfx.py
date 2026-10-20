"""Free sound-effects library, synthesized with numpy (no downloads, no licences) -> motion-library/public/sfx/<name>.wav
Made for the theodesy shorts (Aly 2026-10-08: "مفيش sound effects"); reusable in every project.
Run: python tools/make_sfx.py    (writes ~35 short wav files, 48 kHz mono, peak -3 dBFS)"""
import subprocess
from pathlib import Path
import numpy as np
from scipy.signal import lfilter

SR = 48000
OUT = Path(__file__).resolve().parent.parent / 'motion-library' / 'public' / 'sfx'
rng = np.random.default_rng(7)


def t(d): return np.arange(int(d * SR)) / SR
def noise(d): return rng.standard_normal(int(d * SR)).astype(np.float64)
def env(n, a=0.005, r=0.2, shape=4.0):
    x = np.arange(n) / SR
    e = np.minimum(1, x / max(a, 1e-4)) * np.exp(-shape * np.maximum(0, x - a) / max(r, 1e-4))
    return e


def biquad_bp(x, f0, q):
    """Band-pass (RBJ) with per-sample centre frequency f0 (array or float)."""
    if np.isscalar(f0):
        w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q); a0 = 1 + al
        return lfilter([al / a0, 0, -al / a0], [1, -2 * np.cos(w) / a0, (1 - al) / a0], x)
    f0 = np.broadcast_to(np.asarray(f0, float), x.shape)
    y = np.zeros_like(x); x1 = x2 = y1 = y2 = 0.0
    for i in range(len(x)):
        w = 2 * np.pi * f0[i] / SR; al = np.sin(w) / (2 * q); c = np.cos(w); a0 = 1 + al
        b0, b2, a1, a2 = al / a0, -al / a0, -2 * c / a0, (1 - al) / a0
        yi = b0 * x[i] + b2 * x2 - a1 * y1 - a2 * y2
        x2, x1, y2, y1 = x1, x[i], y1, yi; y[i] = yi
    return y


def lp(x, fc):  # one-pole low-pass
    a = np.exp(-2 * np.pi * fc / SR)
    return lfilter([1 - a], [1, -a], x)


def hp(x, fc): return x - lp(x, fc)


def save(name, x, rms_db=-18):
    x = np.asarray(x, float)
    x = x / (np.sqrt(np.mean(x ** 2)) + 1e-12) * 10 ** (rms_db / 20)
    pk = np.max(np.abs(x))
    if pk > 0.7: x *= 0.7 / pk
    fade = min(len(x), int(0.01 * SR)); x[-fade:] *= np.linspace(1, 0, fade)
    OUT.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f64le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'pcm_s16le', str(OUT / f'{name}.wav')],
                   input=x.astype(np.float64).tobytes(), check=True)
    print(name, round(len(x) / SR, 2), 's')


def sine_glide(f0, f1, d, curve=2.0):
    k = t(d) / d; f = f0 + (f1 - f0) * (1 - (1 - k) ** curve)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


# --- transitions -----------------------------------------------------------------------------------------------
for i, (d, fa, fb, fc) in enumerate([(0.55, 300, 2600, 500), (0.45, 500, 3500, 900), (0.7, 200, 1800, 300)], 1):
    n = noise(d); k = t(d) / d
    f = np.where(k < 0.45, fa + (fb - fa) * (k / 0.45) ** 1.5, fb + (fc - fb) * ((k - 0.45) / 0.55))
    e = np.sin(np.pi * np.clip(k, 0, 1)) ** 1.6
    save(f'whoosh_{i}', biquad_bp(n, f, 1.4) * e, -17)
n = noise(0.25); save('swish', biquad_bp(n, np.linspace(1200, 4500, len(n)), 1.2) * np.sin(np.pi * t(0.25) / 0.25) ** 2, -19)
n = noise(0.3); save('paper', biquad_bp(n, 2500, 0.7) * env(len(n), 0.02, 0.08), -20)
# riser + impact
d = 1.3; k = t(d) / d
save('riser', (biquad_bp(noise(d), 400 + 4000 * k ** 2, 2) * k ** 2 + 0.4 * sine_glide(180, 900, d) * k ** 3), -18)
d = 1.2; x = sine_glide(90, 32, d, 1.5) * env(int(d * SR), 0.003, 0.45, 3) + 0.6 * lp(noise(d), 900) * env(int(d * SR), 0.002, 0.08)
save('impact', x, -14)

# --- pops, clicks, ticks ---------------------------------------------------------------------------------------
for name, f0, f1 in (('pop_1', 650, 170), ('pop_2', 900, 260), ('pop_3', 520, 140)):
    d = 0.12; x = sine_glide(f0, f1, d, 3) * env(int(d * SR), 0.002, 0.05) + 0.25 * hp(noise(d), 3000) * env(int(d * SR), 0.0005, 0.006)
    save(name, x, -17)
d = 0.06; save('tick', hp(noise(d), 3500) * env(int(d * SR), 0.0003, 0.012) + 0.4 * np.sin(2 * np.pi * 2400 * t(d)) * env(int(d * SR), 0.0005, 0.01), -22)
d = 0.06; save('tock', hp(noise(d), 1500) * env(int(d * SR), 0.0003, 0.015) + 0.5 * np.sin(2 * np.pi * 1300 * t(d)) * env(int(d * SR), 0.0005, 0.015), -22)
d = 0.05; save('click', hp(noise(d), 2000) * env(int(d * SR), 0.0003, 0.008), -22)
# stamp / thud / door
d = 0.45; x = np.sin(2 * np.pi * 58 * t(d)) * env(int(d * SR), 0.002, 0.12) + 0.7 * lp(noise(d), 2500) * env(int(d * SR), 0.001, 0.03)
save('stamp', x, -14)
d = 0.8; x = np.sin(2 * np.pi * 45 * t(d)) * env(int(d * SR), 0.002, 0.2) + 0.5 * lp(noise(d), 1200) * env(int(d * SR), 0.001, 0.05)
x += 0.3 * sum(np.sin(2 * np.pi * f * t(d)) for f in (420, 677, 1043)) * env(int(d * SR), 0.004, 0.18)
save('door_slam', x, -14)
# good / bad
d = 0.8; save('ding', sum(a * np.sin(2 * np.pi * f * t(d)) for f, a in ((1318, 1), (2637, 0.4), (3951, 0.15))) * env(int(d * SR), 0.002, 0.35), -19)
d = 0.35; sq = np.sign(np.sin(2 * np.pi * 110 * t(d))); save('buzz_wrong', lp(sq, 1800) * env(int(d * SR), 0.005, 0.3, 1.5), -19)

# --- film / camera ---------------------------------------------------------------------------------------------
def clatter(d, rate=24, hum=110, harsh=1.0):
    n = int(d * SR); x = np.zeros(n)
    for k in np.arange(0, d, 1 / rate):
        i = int((k + rng.uniform(-0.002, 0.002)) * SR)
        if 0 <= i < n - 2000:
            c = hp(noise(0.03), 1500 + 1500 * harsh) * env(int(0.03 * SR), 0.0005, 0.006) * rng.uniform(0.7, 1)
            x[i:i + len(c)] += c
    x += 0.25 * np.sin(2 * np.pi * hum * t(d)) + 0.15 * np.sin(2 * np.pi * hum * 2 * t(d)) + 0.08 * lp(noise(d), 600)
    return x
save('projector', clatter(3.0, 24, 100, 0.6), -20)
save('camera_loud', clatter(2.5, 30, 140, 1.4) * 1.0, -13)
d = 0.25; x = np.zeros(int(d * SR))
for at, f in ((0, 3000), (0.075, 2200)):
    c = hp(noise(0.04), f) * env(int(0.04 * SR), 0.0004, 0.01); i = int(at * SR); x[i:i + len(c)] += c
save('shutter', x + 0.2 * biquad_bp(noise(d), 900, 1) * env(int(d * SR), 0.005, 0.08), -17)
d = 2.0; x = np.zeros(int(d * SR))
for k in np.sort(rng.uniform(0, d - 0.05, 22)):
    c = hp(noise(0.015), 2500) * env(int(0.015 * SR), 0.0003, 0.004) + 0.5 * np.sin(2 * np.pi * 180 * t(0.015)) * env(int(0.015 * SR), 0.0003, 0.006)
    i = int(k * SR); x[i:i + len(c)] += c * rng.uniform(0.6, 1)
save('typing', x, -20)
d = 0.35; x = np.zeros(int(d * SR))
for at in (0, 0.12):
    c = biquad_bp(noise(0.05), 5200, 3) * env(int(0.05 * SR), 0.0005, 0.012) + 0.4 * np.sin(2 * np.pi * 3300 * t(0.05)) * env(int(0.05 * SR), 0.0005, 0.02)
    i = int(at * SR); x[i:i + len(c)] += c
save('scissors', x, -17)
d = 0.4; save('tape', biquad_bp(noise(d), np.linspace(800, 5000, int(d * SR)), 2) * env(int(d * SR), 0.01, 0.25, 2), -19)
d = 1.0; sq = np.sign(np.sin(2 * np.pi * 190 * t(d))) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 14 * t(d))))
save('printer', lp(sq, 2500) * np.minimum(1, t(d) / 0.05) * np.minimum(1, (d - t(d)) / 0.05) + 0.2 * hp(noise(d), 3000), -21)
d = 1.4; k = t(d) / d
save('film_burn', biquad_bp(noise(d), 600 + 2500 * k, 0.8) * np.sin(np.pi * k) + sum(
    (hp(noise(0.01), 2000) * env(int(0.01 * SR), 0.0002, 0.003) if False else 0) for _ in range(1)), -17)
# crackle on top of the burn
x = np.zeros(int(1.4 * SR))
for k2 in rng.uniform(0, 1.35, 40):
    c = hp(noise(0.006), 2500) * env(int(0.006 * SR), 0.0002, 0.002); i = int(k2 * SR); x[i:i + len(c)] += c * rng.uniform(0.3, 1)
save('crackle', x, -21)

# --- nature / ambience -----------------------------------------------------------------------------------------
d = 4.0; k = t(d) / d
g = 0.6 + 0.4 * np.sin(2 * np.pi * 0.35 * t(d)) * np.sin(2 * np.pi * 0.11 * t(d) + 1)
save('wind', biquad_bp(noise(d), 350 + 250 * g, 0.9) * g * np.minimum(1, t(d) / 0.4) * np.minimum(1, (d - t(d)) / 0.4), -20)
d = 2.0; x = np.zeros(int(d * SR))
for k2 in np.sort(rng.uniform(0, d - 0.1, 30)):
    c = biquad_bp(noise(0.06), rng.uniform(1500, 4000), 1.5) * env(int(0.06 * SR), 0.004, 0.03); i = int(k2 * SR); x[i:i + len(c)] += c
save('rustle', x, -20)
d = 1.6; x = 0.15 * lp(noise(d), 1200)
for k2 in np.sort(rng.uniform(0, d - 0.1, 26)):
    f = rng.uniform(320, 950); c = sine_glide(f, f * 1.8, 0.04) * env(int(0.04 * SR), 0.001, 0.012); i = int(k2 * SR); x[i:i + len(c)] += c * 0.6
save('pour', x, -20)

# --- money / time ----------------------------------------------------------------------------------------------
d = 1.2; x = sum(a * np.sin(2 * np.pi * f * t(d)) for f, a in ((2093, 1), (2637, 0.8), (3136, 0.6), (4186, 0.3))) * env(int(d * SR), 0.002, 0.45)
x[:int(0.1 * SR)] += 0.8 * lp(noise(0.1), 1500) * env(int(0.1 * SR), 0.001, 0.03)
save('cash', x, -16)
d = 1.0; x = np.zeros(int(d * SR))
for k2 in np.sort(rng.uniform(0, 0.8, 8)):
    f = rng.uniform(3000, 6000); c = sum(np.sin(2 * np.pi * f * m * t(0.15)) / m for m in (1, 2.76, 5.4)) * env(int(0.15 * SR), 0.0005, 0.05)
    i = int(k2 * SR); x[i:i + len(c)] += c * rng.uniform(0.4, 1)
save('coins', x, -19)
# 4 ticks per second, 6 s (stopwatch)
d = 6.0; x = np.zeros(int(d * SR)); tk = hp(noise(0.03), 3000) * env(int(0.03 * SR), 0.0003, 0.008)
for j, k2 in enumerate(np.arange(0, d, 0.25)):
    i = int(k2 * SR); x[i:i + len(tk)] += tk * (1 if j % 2 else 0.7)
save('clock', x, -22)

# --- digital / ui ----------------------------------------------------------------------------------------------
d = 0.45; x = np.zeros(int(d * SR))
for k2 in np.arange(0, d - 0.05, 0.05):
    f = rng.choice([440, 660, 880, 1320, 1760]); c = np.sign(np.sin(2 * np.pi * f * t(0.04))) * env(int(0.04 * SR), 0.001, 0.02)
    i = int(k2 * SR); x[i:i + len(c)] += c
save('glitch', np.round(x * 6) / 6, -20)
save('swoop_up', sine_glide(260, 1600, 0.8, 1.2) * np.sin(np.pi * t(0.8) / 0.8) + 0.3 * biquad_bp(noise(0.8), np.linspace(500, 4000, int(0.8 * SR)), 2), -19)
save('swoop_down', sine_glide(1400, 220, 0.7, 1.2) * np.sin(np.pi * t(0.7) / 0.7), -19)
save('shh', biquad_bp(noise(0.7), 4200, 0.9) * np.sin(np.pi * t(0.7) / 0.7) ** 0.7, -20)
d = 0.5; save('magic', sum(np.sin(2 * np.pi * f * t(d)) * env(int(d * SR), 0.002 + 0.05 * j, 0.2) for j, f in enumerate((1568, 1976, 2349, 3136))), -21)

# --- music bits ------------------------------------------------------------------------------------------------
def piano(f, d=0.6):
    return sum(a * np.sin(2 * np.pi * f * m * t(d)) for m, a in ((1, 1), (2, 0.5), (3, 0.25), (4, 0.12))) * env(int(d * SR), 0.003, 0.25)
notes = [262, 330, 392, 523, 392, 440, 349, 392, 330, 262]
x = np.zeros(int(3.6 * SR))
for j, f in enumerate(notes):
    i = int(j * 0.3 * SR); p = piano(f); x[i:i + len(p)] += p; b = piano(f / 2, 0.5) * 0.4; x[i:i + len(b)] += b
save('piano_rag', x, -20)
d = 1.5; x = sum(np.sin(2 * np.pi * f * t(d) + 3 * np.sin(2 * np.pi * 5.5 * t(d)) / f * 50) for f in (440, 554, 659)) * env(int(d * SR), 0.15, 0.6, 2)
save('strings', x, -21)
