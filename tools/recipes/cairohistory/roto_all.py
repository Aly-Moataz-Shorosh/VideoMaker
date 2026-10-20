"""His cut-out for v2 (Aly 2026-10-09: "عايز اكون في الفيديو اكتر مش اول حتى بس"): in the screen recording he sits keyed in the
bottom-right corner (same place from 80 s to the end) -> square crop 470 px at (1385, 612) -> tools/matte.py -> one alpha webm per
kept range of every short: public/projects/<code>/roto_<start>.webm. Usage: python work/scripts/roto_all.py"""
import subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
PUB = ROOT / 'motion-library/public/projects' / P.name
SRC = P / 'input' / 'Vd0NUtDsUfk.mp4'
import ast, re
txt = open(Path(__file__).parent / 'make_shorts.py', encoding='utf8').read()
SPANS = ast.literal_eval(re.search(r'SPANS = (\{.*?\n\})', txt, re.S).group(1))
rng = sorted({(a, b) for v in SPANS.values() for a, b in v if a > 80})
# merge overlapping/near ranges
merged = []
for a, b in rng:
    if merged and a <= merged[-1][1] + 1.0:
        merged[-1][1] = max(merged[-1][1], b)
    else:
        merged.append([a, b])
tmp = W / 'roto_tmp'; tmp.mkdir(exist_ok=True)
for a, b in merged:
    a0, d = a - 1.0, b - a + 2.5
    out = PUB / f'roto_{a0:.2f}.webm'
    if out.exists():
        continue
    sq = tmp / 'sq.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a0:.2f}', '-i', str(SRC), '-t', f'{d:.2f}', '-vf', 'crop=470:470:1385:612,scale=540:540',
                    '-c:v', 'libx264', '-crf', '14', '-an', str(sq)], check=True)
    subprocess.run([sys.executable, str(ROOT / 'tools/matte.py'), str(sq), '0', f'{d:.2f}', str(out), '--fps', '30'], check=True, capture_output=True)
    print('roto', a0, d, flush=True)
print('done', len(merged))
