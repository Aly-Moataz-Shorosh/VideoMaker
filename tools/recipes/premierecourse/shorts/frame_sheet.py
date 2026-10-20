# Contact sheet of episode frames (for picking crops): python frame_sheet.py <ep> <out.jpg> t1 t2 ...
import subprocess, sys, cv2, numpy as np
from pathlib import Path
PROJ = Path(__file__).resolve().parents[2]
ep, out, ts = sys.argv[1], sys.argv[2], [float(t) for t in sys.argv[3:]]
src = PROJ.parents[1] / f'motion-library/public/projects/premiere/ep{ep}.mp4'
ims = []
for t in ts:
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', str(src), '-frames:v', '1', '-vf', 'scale=640:-1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
    im = cv2.imdecode(np.frombuffer(r.stdout, np.uint8), 1)
    cv2.putText(im, f'{t:.1f}', (8, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    ims.append(im)
while len(ims) % 3: ims.append(np.zeros_like(ims[0]))
cv2.imwrite(out, np.vstack([np.hstack(ims[i:i + 3]) for i in range(0, len(ims), 3)]), [cv2.IMWRITE_JPEG_QUALITY, 80])
