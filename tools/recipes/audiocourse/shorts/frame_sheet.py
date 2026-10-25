# Contact sheet of session frames (for picking crops / click points): python frame_sheet.py <out.jpg> t1 t2 ...
# Frames at 640 px with a grid every 100 px of the 1280x720 source (numbers = source coordinates).
# CROP=x,y,w (source px) env = zoom into that region (grid every 20 px then).
import subprocess, sys, cv2, numpy as np
from pathlib import Path
PROJ = Path(__file__).resolve().parents[2]
out, ts = sys.argv[1], [float(t) for t in sys.argv[2:]]
src = PROJ.parents[1] / 'motion-library/public/projects/audio/course.mp4'
import os
CR = [int(v) for v in os.environ['CROP'].split(',')] if os.environ.get('CROP') else None
ims = []
for t in ts:
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', str(src), '-frames:v', '1', '-vf', 'scale=640:-1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
    if CR:
        r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', str(src), '-frames:v', '1', '-vf', f'crop={CR[2]}:{CR[2]*9//16}:{CR[0]}:{CR[1]},scale=640:360', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
        im = cv2.imdecode(np.frombuffer(r.stdout, np.uint8), 1); k = 640 / CR[2]
        for x in range((CR[0] // 20 + 1) * 20, CR[0] + CR[2], 20):
            cv2.line(im, (int((x - CR[0]) * k), 0), (int((x - CR[0]) * k), 359), (0, 90, 255), 1)
            if x % 40 == 0: cv2.putText(im, str(x), (int((x - CR[0]) * k) + 2, 355), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (0, 160, 255), 1)
        for y in range((CR[1] // 20 + 1) * 20, CR[1] + CR[2] * 9 // 16, 20):
            cv2.line(im, (0, int((y - CR[1]) * k)), (639, int((y - CR[1]) * k)), (0, 90, 255), 1)
            if y % 40 == 0: cv2.putText(im, str(y), (2, int((y - CR[1]) * k) - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (0, 160, 255), 1)
        cv2.putText(im, f'{t:.1f}', (8, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        ims.append(im); continue
    im = cv2.imdecode(np.frombuffer(r.stdout, np.uint8), 1)
    for x in range(100, 1280, 100):
        cv2.line(im, (x // 2, 0), (x // 2, 359), (0, 90, 255), 1)
        cv2.putText(im, str(x), (x // 2 + 2, 355), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (0, 160, 255), 1)
    for y in range(100, 720, 100):
        cv2.line(im, (0, y // 2), (639, y // 2), (0, 90, 255), 1)
        cv2.putText(im, str(y), (2, y // 2 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (0, 160, 255), 1)
    cv2.putText(im, f'{t:.1f}', (8, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    ims.append(im)
while len(ims) % 2: ims.append(np.zeros_like(ims[0]))
cv2.imwrite(out, np.vstack([np.hstack(ims[i:i + 2]) for i in range(0, len(ims), 2)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
