"""Split each kids take (28 shouted lines) into its 28 names by SILENCE (the lines are separated by pauses, a shout has none):
find quiet stretches, keep the 27 longest as the line breaks. Whisper of each piece is printed to check the order.
Writes kids_v10/take{i}_NN.wav + split.json. Usage (project folder): python -X utf8 work/scripts/kids_split_v10.py"""
import json, subprocess, pathlib
import numpy as np
D = "assets/ai/elevenlabs/kids_v10/"; SR = 48000; N = 28; HOP = 0.01
def load(f, sr):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
out = {}
for i in range(6):
    a = load(D + f"full_{i}.mp3", SR); h = int(HOP * SR)
    e = np.array([np.sqrt((a[k:k + h] ** 2).mean() + 1e-12) for k in range(0, len(a) - h, h)])
    th = max(0.012, 0.06 * np.percentile(e, 95)); loud = e > th
    # quiet runs between loud parts
    runs, k = [], 0
    while k < len(loud):
        if not loud[k]:
            j = k
            while j < len(loud) and not loud[j]: j += 1
            if k > 0 and j < len(loud): runs.append((j - k, k, j))
            k = j
        else: k += 1
    br = sorted(sorted(runs, reverse=True)[:N - 1], key=lambda r: r[1])
    first = int(np.argmax(loud)); last = len(loud) - int(np.argmax(loud[::-1]))
    bounds = [first] + [x for r in br for x in (r[1], r[2])] + [last]
    spans = []
    for k in range(N):
        s0 = max(0, bounds[2 * k] * HOP - 0.04); s1 = bounds[2 * k + 1] * HOP + 0.12
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", D + f"take{i}_{k:02d}.wav"],
                       input=a[int(s0 * SR): int(s1 * SR)].tobytes())
        spans.append(round(s1 - s0, 2))
    out[i] = spans; print(i, len(br), spans)
json.dump(out, open(D + "split.json", "w"), indent=1)
