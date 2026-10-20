"""Where are the faces in a picture? -> object-position y (%) that keeps them in a cover-cropped card.
Usage: python tools/face_pos.py <img> [card_aspect w/h, default 1/0.62 = side_picture 16:9]
Prints faces (cx, cy, size px) and the best y% (side_picture panTo / portal worldPos). Needs opencv-python-headless<5."""
import sys
import cv2

img = cv2.imread(sys.argv[1]); aspect = float(sys.argv[2]) if len(sys.argv) > 2 else 1 / 0.62
g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY); h, w = g.shape
c = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
faces = c.detectMultiScale(g, 1.1, 6, minSize=(int(w * 0.03),) * 2)
print('faces', [(int(x + fw / 2), int(y + fh / 2), int(fw)) for x, y, fw, fh in faces])
win = min(h, w / aspect)  # visible height in source px when cover-cropped
if len(faces) and win < h:
    top = min(y for x, y, fw, fh in faces) - 0.25 * win  # some headroom above the highest face
    print('y% =', round(max(0, min(100, 100 * top / (h - win))), 1))
else:
    print('y% = 50 (no faces or nothing cropped)')
