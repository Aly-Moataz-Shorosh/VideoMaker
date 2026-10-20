"""Round webcam clips (NO roto, the screen recording stays behind him) for v2 of shorts 4/5/6 (Aly 2026-10-09: "عايز زي السكرين شوت
دايرة كدا من غير روتو سكوب… حلوة للخرايط خاصة ان الشاشة باينة ورايا"). One square clip per merged range, same ranges as roto_all.py:
public/projects/<code>/camr_<start>.mp4 (crop 450 px around his face in the bottom-right corner, 480 px out)."""
import ast, re, subprocess
from pathlib import Path
W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
PUB = ROOT / 'motion-library/public/projects' / P.name
SRC = P / 'input' / 'Vd0NUtDsUfk.mp4'
txt = open(Path(__file__).parent / 'make_shorts.py', encoding='utf8').read()
SPANS = ast.literal_eval(re.search(r'SPANS = (\{.*?\n\})', txt, re.S).group(1))
rng = sorted({(a, b) for v in SPANS.values() for a, b in v if a > 80})
merged = []
for a, b in rng:
    if merged and a <= merged[-1][1] + 1.0:
        merged[-1][1] = max(merged[-1][1], b)
    else:
        merged.append([a, b])
need = {(a, b) for n in (4, 5, 6) for a, b in SPANS[n]}
for a, b in merged:
    if not any(a <= x and y <= b for x, y in need):
        continue
    a0, d = a - 1.0, b - a + 2.5
    out = PUB / f'camr_{a0:.2f}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a0:.2f}', '-i', str(SRC), '-t', f'{d:.2f}', '-vf', 'crop=450:450:1381:630,scale=480:480',
                    '-c:v', 'libx264', '-crf', '17', '-an', str(out)], check=True)
    print('cam', a0, round(d, 1))
