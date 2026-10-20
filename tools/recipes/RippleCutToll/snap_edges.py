# Move every keep edge to the quietest 20 ms point within +-0.25 s (cuts must land in real pauses, Aly 2026-10-06).
import sys, json, numpy as np
sys.path.insert(0, 'tools')
from transcribe import load_audio
P = 'projects/2026-10-06 shorts RippleCutToll/'
def snap(audio, ranges, win=0.25):
    sr = 16000; hop = sr // 50
    rms = np.sqrt(np.convolve(audio ** 2, np.ones(hop) / hop, 'same'))
    out = []
    for a, b in ranges:
        r = []
        for t in (a, b):
            i0, i1 = int((t - win) * sr), int((t + win) * sr)
            seg = rms[max(0, i0):i1:hop // 4]
            k = int(np.argmin(seg)); nt = max(0, i0) / sr + k * (hop // 4) / sr
            r.append(round(nt, 2)); print(f'{t:7.2f} -> {nt:7.2f}  level {20*np.log10(seg[k]+1e-9):6.1f} dB (at old edge {20*np.log10(rms[int(t*sr)]+1e-9):6.1f})')
        out.append(r)
    return out
if __name__ == '__main__':
    src, ranges = sys.argv[1], json.loads(sys.argv[2])
    print(json.dumps(snap(load_audio(P + src), ranges)))
