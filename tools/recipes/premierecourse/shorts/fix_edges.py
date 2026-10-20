# Snap piece edges to whole sentences (Aly 2026-10-18: no half-sentences at the start/end of a piece).
# Rules: (short, piece, kind, word) — kind: a_at = start at that word, b_end = end after that word, b_before = end before it.
# The word is searched near the current edge (closest occurrence within 4 s). Prints old -> new and the new text.
import json, sys
import shorts_data as SD
W = {}
for e in (1, 2, 3):
    t = json.load(open(f'../ep{e}/transcript.json', encoding='utf-8'))
    W[e] = [(w['w'].strip(), w['start'], w['end']) for s in t['sentences'] for w in s['words'] if w['w'].strip()]
RULES = [
    (1, 4, 'b_before', 'عشان'), (4, 2, 'a_at', 'تعمل'), (4, 3, 'b_end', 'الاخر'), (5, 8, 'a_at', 'مفروض'),
    (6, 5, 'b_end', 'كلهم'), (10, 6, 'b_end', 'in'), (12, 3, 'b_end', 'Scale'), (14, 6, 'b_end', 'هنا'),
    (15, 2, 'a_at', 'هنعرض'), (16, 4, 'b_end', 'معين'), (18, 0, 'b_end', 'بينهم'), (18, 5, 'a_at', 'وهنا'),
    (18, 5, 'b_end', 'صورة'), (18, 7, 'b_end', 'مضيف'), (19, 0, 'b_end', 'ايه'), (19, 1, 'b_end', 'ترانزيشنز'),
    (19, 3, 'b_end', 'فيديو'), (21, 4, 'b_end', '3'), (23, 3, 'b_end', 'هنا'), (24, 0, 'b_before', 'انت'),
    (24, 3, 'b_end', 'كده'), (24, 4, 'a_at', 'فالنست'), (24, 4, 'b_end', 'كسو.'), (26, 1, 'b_end', 'عليه'),
    (27, 4, 'b_end', 'rate'), (31, 0, 'b_end', 'ديت'), (31, 2, 'b_end', 'ده'), (31, 5, 'b_before', 'بحيس'),
    (35, 3, 'b_end', 'دي'), (36, 1, 'b_end', 'V1.'), (36, 2, 'a_at', 'فهو'), (36, 2, 'b_end', 'V3'),
    (36, 3, 'b_end', 'تو؟'), (39, 2, 'a_at', 'لكنها'), (39, 2, 'b_end', 'ده'), (40, 1, 'b_end', 'ان'),
    (44, 0, 'b_end', 'ان'), (41, 3, 'b_before', 'انا'), (42, 2, 'b_end', 'دلوقتي.'), (43, 2, 'a_at', 'دي'),
    (43, 2, 'b_end', 'الفوتشوب.'), (44, 1, 'b_before', 'لو'), (44, 9, 'b_before', 'عشان'),
]
out = {}
for n, i, kind, word in RULES:
    sp = SD.SHORTS[n]; pc = sp['pieces'][i]; ep = pc.get('ep', sp['ep'])
    a, b = out.get((n, i), (pc['a'], pc['b']))
    edge = a if kind == 'a_at' else b
    cand = [w for w in W[ep] if w[0] == word and abs(w[1] - edge) < 4]
    if not cand: print('NOT FOUND', n, i, kind, word); continue
    w = min(cand, key=lambda w: abs(w[1] - edge))
    if kind == 'a_at': a = round(w[1] - 0.05, 2)
    elif kind == 'b_end': b = round(w[2] + 0.02, 2)
    else: b = round(w[1] - 0.03, 2)
    out[(n, i)] = (a, b)
for (n, i), (a, b) in out.items():
    sp = SD.SHORTS[n]; pc = sp['pieces'][i]; ep = pc.get('ep', sp['ep'])
    txt = ' '.join(w[0] for w in W[ep] if a - 0.05 <= w[1] < b - 0.2)
    print(f"{n}.{i} {pc['a']}-{pc['b']} -> {a}-{b} | {txt}")
json.dump({f'{n}.{i}': v for (n, i), v in out.items()}, open('../shorts/edge_fixes.json', 'w'), indent=0)
