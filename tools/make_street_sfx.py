"""Cinematic street sound effects for the audio-course short 02 Blender scene (Aly 2026-10-27: "sound effects بشكل سينمائي").
Synthesized (free, no Content ID): city ambience, another car passing, the gold car's engine (loud, slows down, idles), wind,
brake squeal, car door, suspense drone.  python tools/make_street_sfx.py  -> motion-library/public/sfx/street_*.wav
Times follow the scene in tools/blender/sound_scenes.py ('street'): isolation 15.5 s, stop 29.2-31.4 s, door 35.2 s, attention 37.3 s.
"""
import subprocess
from pathlib import Path
import numpy as np
from scipy.signal import lfilter, butter

SR = 48000
OUT = Path(__file__).resolve().parents[1] / 'motion-library/public/sfx'
rng = np.random.default_rng(3)
t_ = lambda d: np.arange(int(d * SR)) / SR
noise = lambda d: rng.standard_normal(int(d * SR))


def bp(x, lo, hi, o=2):
    b, a = butter(o, [lo / (SR / 2), hi / (SR / 2)], 'band'); return lfilter(b, a, x)


def lp(x, fc, o=2):
    b, a = butter(o, fc / (SR / 2)); return lfilter(b, a, x)


def hp(x, fc, o=2):
    b, a = butter(o, fc / (SR / 2), 'high'); return lfilter(b, a, x)


def ramp(n, pts):
    """piecewise-linear gain over time: pts = [(sec, gain), ...]"""
    s, g = zip(*pts); return np.interp(np.arange(n) / SR, s, g)


def save(name, x, peak=0.7):
    x = np.asarray(x, float); x = x / (np.max(np.abs(x)) + 1e-12) * peak
    f = int(0.02 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f64le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'pcm_s16le', str(OUT / f'{name}.wav')],
                   input=x.tobytes(), check=True)
    print(name, round(len(x) / SR, 2), 's')


# 1. city: traffic rumble + crowd murmur + footsteps + one far horn; fades out on "هعزل كل الأصوات" (15.5 -> 17.5)
d = 17.5; n = int(d * SR); tt = t_(d)
rumble = lp(noise(d), 160) * (1 + 0.3 * np.sin(2 * np.pi * 0.13 * tt))
murmur = bp(noise(d), 350, 1600) * (0.6 + 0.4 * lp(np.abs(noise(d)), 3) * 6)
steps = np.zeros(n)
for k in range(int(d * 3.2)):
    i = int(rng.uniform(0, d - 0.1) * SR); L = int(0.05 * SR)
    steps[i:i + L] += bp(noise(0.05), 1500, 4000)[:L] * np.exp(-np.arange(L) / (0.008 * SR)) * rng.uniform(0.3, 1)
horn = np.zeros(n); h0 = int(6.0 * SR); hd = t_(0.45)
horn[h0:h0 + len(hd)] = (np.sin(2 * np.pi * 415 * hd) + 0.8 * np.sin(2 * np.pi * 523 * hd)) * np.minimum(1, hd / 0.02) * np.minimum(1, (0.45 - hd) / 0.05)
city = 1.0 * rumble / np.std(rumble) + 0.6 * murmur / np.std(murmur) + 1.5 * steps + 0.25 * lp(horn, 2500)
save('street_city', city * ramp(n, [(0, 0), (0.6, 1), (15.5, 1), (17.5, 0)]), 0.6)

# 2. the other car passes (left lane) and is gone on "ما أسمعش صوت العربية التانية" (plays 18.0 -> 23.6)
d = 5.6; n = int(d * SR); tt = t_(d)
g = np.exp(-((tt - 2.6) / 1.2) ** 2)
f = 55 + 12 * np.tanh((tt - 2.6) * 2)  # doppler: higher coming, lower going
eng = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(4 * np.pi * np.cumsum(f) / SR)
car2 = (lp(eng, 500) + 1.2 * bp(noise(d), 200, 1200) * (0.5 + g)) * g
save('street_car2', car2 * ramp(n, [(0, 1), (5.0, 1), (5.6, 0)]), 0.6)

# 3. the gold car's engine: quiet, then LOUD ("وصوت العربية عالي" 28.3), slows down (29.2-31.4), idles, fades after the door
d = 40.0; n = int(d * SR); tt = t_(d)
f = np.interp(tt, [0, 29.2, 31.4, 40], [46, 46, 26, 24])
ph = 2 * np.pi * np.cumsum(f) / SR
saw = sum(np.sin(k * ph) / k for k in range(1, 9))
engine = lp(saw, 420) + 0.4 * lp(noise(d), 300) * (1 + 0.5 * np.sin(ph))
save('street_engine', engine * ramp(n, [(0, 0), (1.0, 0.35), (28.3, 0.35), (29.0, 1.0), (31.4, 0.7), (36.5, 0.5), (40, 0)]), 0.7)

# 4. wind: the only thing left in the street ("كل الأصوات صوت هوا" 27.2), soft to the end
d = 26.0; n = int(d * SR); tt = t_(d)
fc = 600 + 350 * np.sin(2 * np.pi * 0.11 * tt) + 200 * np.sin(2 * np.pi * 0.23 * tt + 1)
wind = sum(bp(noise(d), lo, lo * 1.6) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * tt + lo)) for lo in (250, 450, 800))
save('street_wind', wind * ramp(n, [(0, 0), (1.5, 1), (24, 1), (26, 0)]), 0.5)

# 5. brake: tyre hiss + squeal (2.7 kHz with vibrato)
d = 1.7; n = int(d * SR); tt = t_(d)
sq = np.sin(2 * np.pi * np.cumsum(2700 + 60 * np.sin(2 * np.pi * 9 * tt)) / SR) + 0.4 * np.sin(2 * np.pi * np.cumsum(5420 + 90 * np.sin(2 * np.pi * 9 * tt)) / SR)
brake = 0.5 * sq * ramp(n, [(0, 0), (0.15, 1), (1.2, 0.8), (1.6, 0)]) + 0.8 * hp(noise(d), 1800) * ramp(n, [(0, 0), (0.05, 1), (1.3, 0.3), (1.7, 0)])
save('street_brake', brake, 0.65)

# 6. door: latch clicks, hinge creak, a soft thump
d = 1.5; n = int(d * SR); door = np.zeros(n)
for at, amp in ((0.0, 1.0), (0.05, 0.7)):
    i = int(at * SR); L = int(0.03 * SR); door[i:i + L] += bp(noise(0.03), 2000, 6000)[:L] * np.exp(-np.arange(L) / (0.004 * SR)) * amp
tt = t_(1.0); i = int(0.12 * SR)
creak = bp(noise(1.0) * (1 + np.sign(np.sin(2 * np.pi * np.cumsum(28 + 20 * tt) / SR))), 700, 1500) * np.sin(np.pi * tt) * 0.6
door[i:i + len(creak)] += creak
i = int(0.02 * SR); L = int(0.25 * SR); door[i:i + L] += lp(noise(0.25), 150)[:L] * np.exp(-np.arange(L) / (0.05 * SR)) * 3
save('street_door', door, 0.7)

# 7. suspense drone under "يلفت انتباهي".. "الساسبنس" (37.3 -> end), swells
d = 16.5; n = int(d * SR); tt = t_(d)
drone = sum(np.sin(2 * np.pi * f0 * tt + k) * a for k, (f0, a) in enumerate([(55, 1), (82.4, 0.6), (110.3, 0.35), (164.8, 0.15)]))
drone = drone * (1 + 0.15 * np.sin(2 * np.pi * 0.4 * tt)) + 0.2 * bp(noise(d), 100, 400)
save('street_drone', drone * ramp(n, [(0, 0), (3, 0.5), (11, 0.8), (15.5, 1), (16.5, 0)]), 0.6)
