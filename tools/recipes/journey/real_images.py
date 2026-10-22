"""Real example pictures (Aly 2026-10-22: "موشن بس من غير صور مش نافع" — people must SEE the real thing).
Order he asked for: HIS own work first (assets/his/work), then pictures from HIS video (crops of frames where the example
is visible around him), then free Commons pictures (assets/commons, credits.json).
python work/scripts/real_images.py -> motion-library/public/projects/<code>/real/<name>.jpg (never upscaled)"""
import glob, shutil, subprocess
from pathlib import Path
from PIL import Image

P = Path(__file__).resolve().parents[2]
OUT = P.parents[1] / 'motion-library' / 'public' / 'projects' / P.name / 'real'
OUT.mkdir(parents=True, exist_ok=True)
W = P / 'assets' / 'his' / 'work'

# (name, video, second, crop box x0 y0 x1 y1 in 1920x1080) — the area of his video where the example is NOT behind him
FRAMES = [
    ('oz_ui', '33', 51, (420, 0, 1500, 370)), ('oz_brand1', '33', 66, (420, 0, 1500, 380)), ('oz_brand2', '33', 70, (420, 0, 1500, 380)),
    ('oz_stationery', '33', 74, (420, 0, 1500, 370)), ('oz_poster', '33', 82, (420, 0, 1500, 380)), ('oz_brochure', '33', 90, (100, 560, 640, 900)),
    ('oz_pack', '33', 97, (380, 440, 660, 850)), ('oz_social1', '33', 103, (420, 0, 1500, 420)), ('oz_social2', '33', 106, (420, 0, 1500, 380)),
    ('oz_photo1', '33', 110, (420, 0, 1500, 400)), ('oz_photo2', '33', 114, (300, 60, 1300, 400)), ('oz_illus', '33', 124, (420, 0, 1500, 400)),
    ('oz_paint', '33', 134, (420, 0, 1500, 380)),
]
# his own work
HIS = [('his_social', 'w06.png'), ('his_logo180', 'w09.png'), ('his_tshirt', 'w11.png'), ('his_cartoon', 'w14.png'), ('his_cartoon_full', 'w15.jpg'),
       ('his_manip', 'w18.jpg'), ('his_photo', 'w02.jpg'), ('his_photo_cover', 'w05.png'), ('his_grad_ui', 'w08.png'), ('his_pyramids', 'w17.jpg')]

for name, ep, t, box in FRAMES:
    src = glob.glob(str(P / 'input' / f'{ep}_*.mp4'))[0]
    tmp = OUT / f'{name}.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', src, '-frames:v', '1', str(tmp)], check=True)
    Image.open(tmp).convert('RGB').crop(box).save(OUT / f'{name}.jpg', quality=92); tmp.unlink()
for name, f in HIS:
    im = Image.open(W / f).convert('RGBA')
    if im.getbbox() != (0, 0) + im.size:
        im = im.crop(im.getbbox())
    im.thumbnail((1400, 1400))
    (im if name.startswith('his_cartoon') else im.convert('RGB')).save(OUT / (f'{name}.png' if name.startswith('his_cartoon') else f'{name}.jpg'), quality=92)
for f in (P / 'assets' / 'commons').glob('*.jpg'):
    im = Image.open(f).convert('RGB'); im.thumbnail((1400, 1400)); im.save(OUT / f'c_{f.stem}.jpg', quality=92)
print(sorted(x.name for x in OUT.iterdir()))
