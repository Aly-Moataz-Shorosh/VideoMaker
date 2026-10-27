"""Two-person interview, one mono mix: which voice is which (step before speakers.py).
MFCC(1..19) mean + median pitch per 0.5 s voiced window -> GMM with 2 clusters -> work/voiceclust.npz (T, X, lab).
ep01: Aly ~186 Hz, guest ~147 Hz; Aly asks the questions (check a few turns against the text).
Usage: python voices.py <video> <work_dir>"""
import subprocess, sys
import numpy as np, librosa
from sklearn.mixture import GaussianMixture

video, work = sys.argv[1], sys.argv[2]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', video, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
hop = 160
mf = librosa.feature.mfcc(y=a, sr=16000, n_mfcc=20, hop_length=hop, n_fft=512)
f0 = librosa.yin(a, fmin=70, fmax=350, sr=16000, frame_length=1024, hop_length=hop)
rms = librosa.feature.rms(y=a, frame_length=512, hop_length=hop)[0]
n = min(mf.shape[1], len(f0), len(rms)); mf, f0, rms = mf[:, :n], f0[:n], rms[:n]
Wn, thr = 50, np.percentile(rms, 40)
X, T = [], []
for i in range(n // Wn):
    s = slice(i * Wn, (i + 1) * Wn); v = rms[s] > thr
    if v.mean() < 0.5: continue
    X.append(np.r_[mf[1:, s][:, v].mean(1), np.median(f0[s][v]) / 50]); T.append(i * 0.5)
X, T = np.array(X), np.array(T)
lab = GaussianMixture(2, covariance_type='diag', random_state=0).fit_predict((X - X.mean(0)) / X.std(0))
print('pitch per cluster', [round(float(np.median(X[lab == k, -1] * 50))) for k in (0, 1)], 'windows', np.bincount(lab))
np.savez(f'{work}/voiceclust.npz', T=T, X=X, lab=lab)
