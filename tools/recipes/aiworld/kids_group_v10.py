"""Kids GROUP v10 (Aly v9 notes 1/7/15/17/51: v9 = 3 voices + pitch-shifted delayed COPIES of the same take = echo / chorus).
Now: only DIFFERENT performances (3 kid voices x 2 takes each = 6 real takes), each trimmed to its own shout, aligned on its own onset with a small
natural random spread (0-70 ms, never a copy of the same take), different gains, spread left/right in stereo; the cheer comes AFTER the shout.
Usage: python kids_group_v10.py out.wav cheer.mp3 take1.mp3 take2.mp3 ...   (prints the shout length)"""
import subprocess, sys, random
import numpy as np
SR = 48000
def load(f):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).copy()
def trim(x):
    w = int(.01 * SR); e = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, "same")); on = np.where(e > 0.03 * e.max())[0]
    return x[max(0, on[0] - int(.015 * SR)): on[-1] + int(.08 * SR)]
out_f, cheer_f, takes = sys.argv[1], sys.argv[2], sys.argv[3:]
random.seed(len(takes) * 7 + sum(map(ord, out_f)))
T = [trim(load(f)) for f in takes]
pans = np.linspace(-0.7, 0.7, len(T)); random.shuffle(pans := list(pans))
speech = max(len(x) for x in T) + int(0.08 * SR)
L = speech + int(1.3 * SR)
out = np.zeros((L, 2), np.float32)
for x, pan in zip(T, pans):
    d = int(random.uniform(0, 0.07) * SR); g = random.uniform(0.7, 1.0) / np.abs(x).max()
    l, r = np.sqrt((1 - pan) / 2), np.sqrt((1 + pan) / 2); n = min(len(x), L - d)
    out[d:d + n, 0] += x[:n] * g * l; out[d:d + n, 1] += x[:n] * g * r
c = load(cheer_f); s = int(speech * 0.8); n = min(len(c), L - s)
out[s:s + n] += (c[:n] * 0.28)[:, None]
out /= np.abs(out).max() / 0.89
f = int(.01 * SR); out[:f] *= np.linspace(0, 1, f)[:, None]; out[-int(.5 * SR):] *= np.linspace(1, 0, int(.5 * SR))[:, None]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", out_f], input=out.tobytes())
print(round(speech / SR, 2))
