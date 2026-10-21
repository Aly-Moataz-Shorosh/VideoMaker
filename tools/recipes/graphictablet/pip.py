"""Find when the picture-in-picture insert (box x66-872, y314-766 of 1920x1080) is on screen: a straight edge at its right + bottom side."""
import subprocess, sys
import numpy as np
src = sys.argv[1]; W, H, FPS = 480, 270, 10
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'fps={FPS},scale={W}:{H},format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
v = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
x = 218; y0, y1 = 82, 188
edge = np.abs(v[:, y0:y1, x - 1] - v[:, y0:y1, x + 1])
eb = np.abs(v[:, 191, 20:215] - v[:, 193, 20:215])
score = np.median(edge, 1) + 0.5 * np.median(eb, 1)
on = score > 6
runs, s = [], None
for i, o in enumerate(list(on) + [False]):
    if o and s is None: s = i
    if not o and s is not None:
        if i - s >= 5: runs.append((s / FPS, i / FPS))
        s = None
print(' '.join(f'{a:.1f}-{b:.1f}' for a, b in runs))
np.save('pip_score.npy', score)
