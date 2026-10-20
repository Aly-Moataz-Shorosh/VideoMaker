"""Aly's face moments per short (source seconds in the YouTube video) -> cut-outs for the film-short composition.
Source = his published video (1080p, no raw clips this time). Desk shots only (screen-recording parts have a tiny cam).
1. face x via haar on the middle frame, 2. 1080x1080 square around him, 3. tools/matte.py -> alpha webm.
Writes motion-library/public/projects/<code>/aly_<short>_<k>.webm + work/faces.json. Run: python faces.py [short ...]"""
import json, subprocess, sys
from pathlib import Path
import numpy as np, cv2
W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
sys.stdout.reconfigure(encoding='utf-8')
CODE = P.name
PUB = ROOT / 'motion-library' / 'public' / 'projects' / CODE
SRC = P / 'input' / 'vSaO0bRnfz8.mp4'
FACES = {
    1: [[797.4, 799.5], [835.9, 840.9], [556.3, 559.4]],
    2: [[805.2, 809.5], [41.1, 43.6]],
    4: [[148.7, 156.5]],
    8: [[75.6, 81.1], [791.3, 794.5], [901.2, 903.7]],
}
casc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def frame(t):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', str(SRC), '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1080, 1920, 3)


out = json.load(open(W / 'faces.json', encoding='utf8')) if (W / 'faces.json').exists() else {}
for n in [int(x) for x in sys.argv[1:]] or sorted(FACES):
    res = []
    for k, (a, b) in enumerate(FACES[n]):
        g = cv2.cvtColor(frame((a + b) / 2), cv2.COLOR_BGR2GRAY)
        fs = sorted(casc.detectMultiScale(g, 1.1, 6, minSize=(90, 90)), key=lambda r: -r[2])
        fx, fy, fw = (fs[0][0] + fs[0][2] / 2, fs[0][1] + fs[0][3] / 2, fs[0][2]) if len(fs) else (960, 400, 0)
        x0 = int(min(1920 - 1080, max(0, fx - 540)))
        tmp = W / f'_sq_{n}_{k}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.2f}', '-t', f'{b - a:.2f}', '-i', str(SRC), '-an', '-vf', f'crop=1080:1080:{x0}:0,fps=30',
                        '-c:v', 'libx264', '-crf', '14', str(tmp)], check=True)
        name = f'aly_{n}_{k}.webm'
        subprocess.run([sys.executable, str(ROOT / 'tools' / 'matte.py'), str(tmp), '0', f'{b - a:.2f}', str(PUB / name), '--fps', '30'], check=True)
        tmp.unlink()
        res.append({'src': a, 'end': b, 'file': f'projects/{CODE}/{name}', 'face': [round((fx - x0) / 1080, 3), round(fy / 1080, 3)],
                    'faceW': round(fw / 1080, 3) if fw else 0})
        print(n, k, res[-1], flush=True)
    out[str(n)] = res
    json.dump(out, open(W / 'faces.json', 'w', encoding='utf8'), indent=1)
