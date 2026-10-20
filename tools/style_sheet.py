"""Study helper (read-only on sources): one contact-sheet row per video + dominant colors.

Usage: python tools/style_sheet.py <group_name> <list.txt>   (list: "label|path" per line)
Writes references/style-sheets/<group>.jpg (small) and appends palettes to references/style-sheets/palettes.json
Sources are only READ (ffmpeg fast seek, 6 frames). Nothing is written next to them.
"""
import json, subprocess, sys, io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'references' / 'style-sheets'
N, TW = 6, 230


def dur(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0


def frame(p, t):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', p, '-frames:v', '1', '-vf', f'scale={TW}:-2',
                        '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
    return Image.open(io.BytesIO(r.stdout)).convert('RGB') if r.stdout else None


def palette(imgs, k=6):
    w = sum(i.width for i in imgs)
    strip = Image.new('RGB', (w, max(i.height for i in imgs)))
    x = 0
    for i in imgs:
        strip.paste(i, (x, 0)); x += i.width
    q = strip.resize((w // 3, strip.height // 3)).quantize(k, method=Image.Quantize.MEDIANCUT)
    pal, cnt = q.getpalette(), sorted(q.getcolors(), reverse=True)
    tot = sum(c for c, _ in cnt)
    return [('#%02X%02X%02X' % tuple(pal[i * 3:i * 3 + 3]), round(100 * c / tot)) for c, i in cnt]


def main():
    group, lst = sys.argv[1], sys.argv[2]
    OUT.mkdir(parents=True, exist_ok=True)
    rows, pals = [], {}
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 14)
    for line in Path(lst).read_text(encoding='utf8').splitlines():
        if '|' not in line:
            continue
        label, p = [x.strip() for x in line.split('|', 1)]
        d = dur(p)
        if d <= 0:
            print('skip', label); continue
        imgs = [f for f in (frame(p, d * (i + 0.5) / N) for i in range(N)) if f]
        if not imgs:
            continue
        pal = palette(imgs)
        pals[f'{group}/{label}'] = {'path': p, 'duration': round(d, 1), 'palette': pal}
        h = max(i.height for i in imgs)
        row = Image.new('RGB', (TW * N + 150, h + 4), (30, 30, 30))
        dr = ImageDraw.Draw(row)
        dr.text((4, 4), label[:18], fill='white', font=font)
        dr.text((4, 22), f'{d:.0f}s', fill='#aaa', font=font)
        for j, (hx, pc) in enumerate(pal[:5]):
            dr.rectangle([4 + j * 28, 44, 28 + j * 28, 68], fill=hx)
        for j, im in enumerate(imgs):
            row.paste(im, (150 + j * TW, 2))
        rows.append(row)
    sheet = Image.new('RGB', (TW * N + 150, sum(r.height for r in rows)), (0, 0, 0))
    y = 0
    for r in rows:
        sheet.paste(r, (0, y)); y += r.height
    sheet.save(OUT / f'{group}.jpg', quality=80)
    pj = OUT / 'palettes.json'
    allp = json.loads(pj.read_text(encoding='utf8')) if pj.exists() else {}
    allp.update(pals)
    pj.write_text(json.dumps(allp, ensure_ascii=False, indent=1), encoding='utf8')
    print(group, len(rows), 'rows')


if __name__ == '__main__':
    main()
