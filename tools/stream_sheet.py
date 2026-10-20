"""Study a public YouTube video WITHOUT downloading it: grab N frames from the stream, save one small sheet.

Usage: python tools/stream_sheet.py <name> <youtube_id> [<youtube_id> ...]
Writes references/style-sheets/<name>.jpg only.
"""
import io, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / 'references' / 'style-sheets'
N, TW = 8, 230


def main():
    name, ids = sys.argv[1], sys.argv[2:]
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 14)
    rows = []
    for vid in ids:
        info = subprocess.run([sys.executable, '-m', 'yt_dlp', '-f', 'b[height<=360]/bv[height<=360]', '-g', '--print', 'duration',
                               '--print', 'title', f'https://www.youtube.com/watch?v={vid}'], capture_output=True, text=True).stdout.split('\n')
        dur, title, url = float(info[0]), info[1], info[2]
        imgs = []
        for i in range(N):
            t = dur * (i + 0.5) / N
            r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.1f}', '-i', url, '-frames:v', '1', '-vf', f'scale={TW}:-2',
                                '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, timeout=90)
            if r.stdout:
                imgs.append(Image.open(io.BytesIO(r.stdout)).convert('RGB'))
        h = max(i.height for i in imgs)
        row = Image.new('RGB', (TW * N + 150, h + 4), (30, 30, 30))
        d = ImageDraw.Draw(row)
        d.text((4, 4), title[:20], fill='white', font=font)
        for j, im in enumerate(imgs):
            row.paste(im, (150 + j * TW, 2))
        rows.append(row)
        print(vid, title, len(imgs))
    sheet = Image.new('RGB', (TW * N + 150, sum(r.height for r in rows)))
    y = 0
    for r in rows:
        sheet.paste(r, (0, y)); y += r.height
    sheet.save(OUT / f'{name}.jpg', quality=80)


if __name__ == '__main__':
    main()
