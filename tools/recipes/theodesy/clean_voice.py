"""Remove the car's steady engine/AC noise from Aly's voice (car part only; home part is clean) -> work/voice.m4a.
noisereduce stationary mode with a noise profile from the quietest frames of the car part."""
import glob, subprocess, sys
import numpy as np, noisereduce as nr
from pathlib import Path
W = Path(__file__).resolve().parents[1]
v = glob.glob(str(W.parent / 'input' / '*Odesy' / 'final.mp4'))[0]
SR = 48000
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', v, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
a = np.frombuffer(raw, np.float32).copy()
hop = SR // 10
e = 20 * np.log10(np.sqrt((a[:len(a) // hop * hop].reshape(-1, hop) ** 2).mean(1)) + 1e-9)
# car/home boundary: rolling 10th-percentile floor drops from ~-22 to ~-34 dB
fl = np.array([np.percentile(e[max(0, i - 50):i + 50], 10) for i in range(len(e))])
b = int(np.argmax((np.arange(len(fl)) > 5000) & (fl < -29))) * hop if len(sys.argv) < 2 else int(float(sys.argv[1]) * SR)
print('car part ends at', round(b / SR, 2))
car = a[:b]
q = e[:b // hop] < np.percentile(e[:b // hop], 8)
noise = np.concatenate([car[i * hop:(i + 1) * hop] for i in np.where(q)[0]])
clean = nr.reduce_noise(y=car, sr=SR, y_noise=noise, stationary=True, prop_decrease=0.85, n_fft=2048)
out = np.concatenate([clean, a[b:]]).astype(np.float32)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-af',
                'highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', str(SR), '-c:a', 'aac', '-b:a', '192k', str(W / 'voice.m4a')],
               input=out.tobytes(), check=True)
def pct(x, t):
    s = x[int(t * SR):int((t + 40) * SR)]; w = s[:len(s) // 4800 * 4800].reshape(-1, 4800)
    ee = 20 * np.log10(np.sqrt((w ** 2).mean(1)) + 1e-9); return [round(float(np.percentile(ee, p)), 1) for p in (10, 50, 90)]
print('car before', pct(a, 80), 'after', pct(out, 80))
