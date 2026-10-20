"""Material for the review-2026-10-19 versions -> motion-library/public/projects/newstage19/media/
(cuts of the downloaded clips, crops of his slides, YouTube thumbnails, QR codes). Sources: work/web, work/slides, work/slide_media."""
import subprocess, urllib.request
from pathlib import Path
import qrcode
from PIL import Image
P = Path(__file__).resolve().parents[2]
WEB, SL, SM = P / 'work' / 'web', P / 'work' / 'slides', P / 'work' / 'slide_media'
OUT = P.parents[1] / 'motion-library' / 'public' / 'projects' / 'newstage19' / 'media'
OUT.mkdir(parents=True, exist_ok=True)
H = {'User-Agent': 'Mozilla/5.0'}


def cut(src, name, ss, t, vf='scale=1280:-2'):
    o = OUT / name
    if not o.exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(t), '-i', str(src), '-an', '-vf', vf + ',fps=30', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', str(o)], check=True)


def crop(src, name, box, size=None):
    im = Image.open(src).convert('RGB').crop(box)
    if size: im = im.resize(size, Image.LANCZOS)
    im.save(OUT / name, quality=92)


def thumb(vid, name):
    o = OUT / name
    if o.exists(): return
    for q in ('maxresdefault', 'hqdefault'):
        try:
            data = urllib.request.urlopen(urllib.request.Request(f'https://i.ytimg.com/vi/{vid}/{q}.jpg', headers=H)).read()
            if len(data) > 5000:
                o.write_bytes(data); return
        except Exception:
            pass


def qr(url, name):
    q = qrcode.QRCode(border=1, box_size=12); q.add_data(url); q.make(); q.make_image().save(OUT / name)


# --- clips (muted cuts) ---
cut(WEB / 'meme_c19.mp4', 'meme_c19.mp4', 7, 7, 'scale=720:-2')                 # 10: the meme, last part
cut(WEB / 'ibrahim_a.mp4', 'ibrahim_a.mp4', 0, 11)                              # 19
cut(WEB / 'ibrahim_b.mp4', 'ibrahim_b.mp4', 0, 12)
cut(WEB / 'plane_yt.mp4', 'plane_close.mp4', 19.8, 6.5)                         # 2nd review: the nicest flying shot                             # 28: his plane video
cut(WEB / 'plane_yt.mp4', 'plane_fleet.mp4', 53, 6)
cut(WEB / 'plane_game.mp4', 'plane_game.mp4', 44, 12)                           # 28: his plane game
cut(WEB / 'wingit.webm', 'wingit_cat.mp4', 86, 8)                               # 9: WING IT! (CC BY 4.0 Blender Studio)
cut(WEB / 'wingit.webm', 'wingit_blender.mp4', 201, 7)
cut(WEB / 'printer3d.webm', 'printer3d.mp4', 0, 12.4)                           # 26 (CC BY-SA 4.0 MDXDave)
cut(WEB / 'vr_job.webm', 'vr_headset.mp4', 12, 6)                               # 19 (CC BY-SA 3.0 Owlchemy Labs)
cut(WEB / 'vr_job.webm', 'vr_world.mp4', 18, 6)
cut(WEB / 'vr_job.webm', 'vr_office.mp4', 60, 6)
cut(WEB / 'ar_spider.webm', 'ar_spider.mp4', 0, 4, 'scale=-2:960')             # 19 (CC BY-SA 4.0)
cut(WEB / 'glasses.webm', 'glasses.mp4', 0, 8)                                  # 19 (CC BY 4.0)
for f in ['032_media3.mp4', '033_media4.mp4', '041_media5.mp4', '042_media6.mp4', '043_media7.mp4', '044_media8.mp4', '056_media13.mp4']:
    if not (OUT / f).exists():
        (OUT / f).write_bytes((SM / f).read_bytes())

# --- pictures ---
s105 = SL / 'slide_105.png'   # materials slide: the 5 balls on the top row (1920 export)
for cx, cy, nm in [(295, 310, 'glass'), (620, 318, 'melon'), (965, 318, 'gravel'), (1310, 318, 'grass'), (1650, 310, 'honey')]:
    crop(s105, f'ball_{nm}.jpg', (cx - 125, cy - 125, cx + 125, cy + 125))
crop(SL / 'slide_034.png', 'burger.jpg', (105, 255, 960, 822))
crop(SL / 'slide_034.png', 'duck_feast.jpg', (1142, 226, 1690, 852))
Image.open(SM / '062_image69.png').convert('RGB').save(OUT / 'bonto_logo.jpg', quality=92)
Image.open(SM / '062_image70.png').convert('RGB').save(OUT / 'bonto_game.jpg', quality=92)
crop(SL / 'slide_046.png', 'heart_ecg.jpg', (0, 150, 1920, 1080))
crop(SL / 'slide_047.png', 'qr_map.jpg', (0, 150, 1920, 1080))
crop(SL / 'slide_045.png', 'touch_voice.jpg', (0, 150, 1920, 1080))
for i, f in enumerate(['plane_1.jpg', 'plane_3.png', 'plane_5.png', 'plane_6.png']):
    Image.open(WEB / 'behance' / f).convert('RGB').save(OUT / f'behance_{i + 1}.jpg', quality=92)
Image.open(WEB / 'plane_design.jpg').convert('RGB').save(OUT / 'plane_design.jpg', quality=92)

# --- YouTube thumbnails ---
for vid in ['5C4KNFiJFjA', 'sCVcWyMtTL8', 'j48LtUkZRjU', 'IlKaB1etrik',                       # AE->code, plane, Brackeys playlist
            'Ag22uTUIvPo', 'owZdBNisOpA', '2_PwpcOQQyE', 'tCV5jp5jZsE', 'ssB6HYUIR4w', 'a6QAqmP51TQ',  # his "هو ايه" 3D episodes
            'gSewGtCDhHY', '8d4jkySoXe4', '10UXB0cT4Ss', 'PJTcdeSiDUI', 'H5oOZypINf0', 'Ps7A-UXx-5g',  # his AI videos
            'Ae9q7KsRbuI', 'uO5cvkzh3P0', 'zJvN8PDX1is', 'vO6SWG-jxvE', '8B05cy3UuSE', 'eVBJIUxv8N8']: # Two Minute Papers
    thumb(vid, f'yt_{vid}.jpg')

# --- QR codes ---
qr('https://youtu.be/5C4KNFiJFjA', 'qr_ae2code.png')
qr('https://youtu.be/sCVcWyMtTL8', 'qr_plane.png')
qr('https://youtube.com/playlist?list=PLPV2KyIb3jR53Jce9hP7G5xC4O9AgnOuL', 'qr_brackeys.png')
qr('https://youtube.com/playlist?list=PL--cO7twoKgmv68cLkVeOKKpra-cOINvy', 'qr_howayh.png')
qr('https://youtu.be/H5oOZypINf0', 'qr_ai_start.png')
qr('https://www.youtube.com/@TwoMinutePapers', 'qr_2mp.png')
print(len(list(OUT.iterdir())), 'files in', OUT)
