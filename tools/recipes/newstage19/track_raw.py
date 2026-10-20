"""Where is Aly on the stage? OpenCV HOG person detector on the RAW hall camera (static, 1280x720, HLG), 4 samples/s over a range.
Writes work/track.json {t: [cx, top, bottom]} (720p px).  python track.py <a_sec> <b_sec>  (default whole lecture)"""
import json, sys
from pathlib import Path
import cv2
P = Path(__file__).resolve().parents[2]
a = float(sys.argv[1]) if len(sys.argv) > 1 else 0
b = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
out = P / 'work' / 'track_raw.json'
data = json.load(open(out)) if out.exists() else {}
hog = cv2.HOGDescriptor(); hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cap = cv2.VideoCapture(str(P / 'input' / '20260908_103633.mp4'))
cap.set(cv2.CAP_PROP_POS_MSEC, a * 1000)
fps = cap.get(cv2.CAP_PROP_FPS); step = max(1, round(fps / 4)); i = 0
t0 = a
while True:
    ok = cap.grab()
    if not ok: break
    t = t0 + i / fps; i += 1
    if t > b: break
    if (i - 1) % step: continue
    ok, fr = cap.retrieve()
    roi = fr[60:420]  # stage band (heads of the audience below are not him)
    rects, w = hog.detectMultiScale(roi, winStride=(8, 8), padding=(8, 8), scale=1.05)
    best = None
    for (x, y, ww, hh), s in zip(rects, w):
        if hh < 110: continue
        if best is None or s > best[1]: best = ((x + ww / 2, y + 60, y + 60 + hh), float(s))
    if best: data[f'{t:.2f}'] = [round(v) for v in best[0]]
json.dump(data, open(out, 'w'))
print(len(data), 'detections')
