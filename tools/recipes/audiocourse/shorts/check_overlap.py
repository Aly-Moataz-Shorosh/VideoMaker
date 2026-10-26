# No two shorts may share a hook or a piece of content (Aly 2026-10-26: "مشنفعش فيديوهين يكونو نفس الهوك او نفس المحتوى").
#   python check_overlap.py  -> prints every source range used by two shorts (versions of the same short, keys >= 100, are skipped)
from itertools import combinations
import shorts_data as SD
R = {n: [(pc['a'], pc['b']) for pc in sp['pieces'] if 'a' in pc] for n, sp in SD.SHORTS.items() if n < 100}
bad = 0
for x, y in combinations(R, 2):
    for a1, b1 in R[x]:
        for a2, b2 in R[y]:
            if min(b1, b2) - max(a1, a2) > 0.3:
                bad += 1; print(f'overlap: short {x} {a1}-{b1}  <->  short {y} {a2}-{b2}')
print('ok' if not bad else f'{bad} overlaps', '| shorts', sorted(R))
