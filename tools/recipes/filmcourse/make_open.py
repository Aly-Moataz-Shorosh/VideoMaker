# Film-making course (2026-11-06): his ~5-year-old course, recorded today (1:22:57, 1080p60) as ONE YouTube video.
# v2 (Aly review 1): NO intro / outro ("انا مش عايز انترو ولا اوترو"), chapter separators like the older courses.
# Final = teaser (his clips) -> opening pages (Claude's coverage, reasons, parts, timestamps)
#         -> [separator 4 s + chapter as-is] x 32 -> separator 'what to learn next' -> ending (missing topics + his videos).
# Only the added pieces are rendered by Remotion (teaser, pages, seps, end); assemble.sh joins them with the untouched course.
#   python make_open.py   -> work/props_{teaser,pages,seps,end}.json, work/pieces.json, work/chapters.json
import json, subprocess, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent.parent
ML = PROJ.parent.parent / 'motion-library'
PUB = 'projects/filmcourse/'
SRC = PROJ / 'input/2026-11-06 14-39-41.mp4'
SRC_LEN = 4977.45
FPS = 30
SEP = 4.0
MUSIC = PUB + 'music/lofi_coffee_shop.mp3'  # Pixabay, no Content ID (approved in the premiere + audio courses)
AN = json.load(open(PROJ / 'work/analysis.json'))
sys.path.insert(0, str(HERE))
import film_data as D


def g30(t): return round(round(t * 30) / 30, 4)   # Remotion pieces end on a 30 fps frame
def g60(t): return round(round(t * 60) / 60, 4)   # course cut points on a 60 fps frame


def fmt(t):
    t = int(t)
    return f'{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}' if t >= 3600 else f'{t // 60}:{t % 60:02d}'


TR = json.load(open(PROJ / 'work/transcript.json', encoding='utf-8'))
WORDS = sorted((w['start'], w['end']) for s in TR['sentences'] for w in s['words'])


def quiet_near(t):
    """Cut in the gap right BEFORE the chapter's first word (word times), at its quietest 100 ms -> never inside a word."""
    if t <= 0: return 0.0
    # gaps between words (ends can overlap the next start in Whisper times -> gap = max end so far .. next start)
    gaps, mx = [], 0.0
    for a, b in WORDS:
        if a > mx + 0.02 and t - 2.0 <= a <= t + 0.1: gaps.append((mx, a))
        mx = max(mx, b)
    r = np.array(AN['rms'])
    if not gaps:  # fast talk, no pause: cut on the word boundary where the sound is lowest
        starts = [a for a, _ in WORDS if t - 2.0 <= a <= t + 0.2]
        a = min(starts, key=lambda a: r[max(0, int(a * 10) - 1):int(a * 10) + 1].mean())
        return round(np.floor(a * 60) / 60, 4)
    lo, hi = max(gaps, key=lambda g: (g[1] - g[0]) - 0.15 * abs(g[1] - t))
    cand = [k for k in range(int(np.ceil(lo * 10)), int(hi * 10)) if k / 10 + 0.1 <= hi]
    bt = min(cand, key=lambda k: r[k]) / 10 + 0.05 if cand else (lo + hi) / 2
    bt = min(max(bt, lo), hi)
    return round(np.floor(bt * 60 + 1e-6) / 60, 4) if np.floor(bt * 60) / 60 >= lo else round(np.ceil(bt * 60) / 60, 4)


def thumb(s, name):
    out = ML / 'public' / PUB / 'thumbs' / name
    out.parent.mkdir(exist_ok=True)
    if not out.exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(s), '-i', str(SRC), '-frames:v', '1', '-vf', 'scale=960:540', '-q:v', '2', str(out)], check=True)
    return PUB + 'thumbs/' + name


def dump(name, props):
    for p in props.get('parts', []): p['from'] = p.pop('from_')
    for m in props.get('music', []): m['from'] = m.pop('from_')
    for k in ('parts', 'keys', 'cues', 'huds', 'sfx', 'scenes'): props.setdefault(k, [])
    json.dump(dict(fps=FPS, **props), open(PROJ / f'work/props_{name}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def teaser_file():
    # Teaser pieces cut once into ONE small 30 fps file (the 1.8 GB source never goes into public/)
    out = ML / 'public' / PUB / 'teaser.mp4'
    segs, t = [], 0.0
    for a, b, *_ in D.TEASER: segs.append((t, a, b)); t += b - a
    key = json.dumps(D.TEASER)
    stamp = out.with_suffix('.json')
    if not out.exists() or not stamp.exists() or stamp.read_text(encoding='utf-8') != key:
        fc = ''.join(f'[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=1276:720[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];' for i, (_, a, b) in enumerate(segs))
        fc += ''.join(f'[v{i}][a{i}]' for i in range(len(segs))) + f'concat=n={len(segs)}:v=1:a=1[v][a]'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(SRC), '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                        '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-c:a', 'aac', '-b:a', '256k', str(out)], check=True)
        stamp.write_text(key, encoding='utf-8')
    return segs, t


def main():
    segs, tl = teaser_file()
    teaser_len = g30(tl + 0.6)
    pages_len = g30(sum(d for _, d, _ in D.OPEN) + D.PARTS_SEC + D.STAMP_SEC * len(D.STAMP_PAGES))
    # chapters: cut on the quietest point near each start; timeline = teaser + pages + (sep + chapter) ...
    chs = []
    for i, (pi, s, ar, en, ico) in enumerate(D.CH):
        chs.append(dict(n=i + 1, part=pi, src=quiet_near(s), ar=ar, en=en, ico=ico))
    for i, c in enumerate(chs):
        c['end'] = chs[i + 1]['src'] if i + 1 < len(chs) else SRC_LEN
    t = teaser_len + pages_len
    for c in chs:
        c['sep'] = round(t, 4); c['t'] = round(t + SEP, 4); t = c['t'] + (c['end'] - c['src'])
    course_end = round(t, 4)
    TOTAL = len(chs) + 1

    # ---- teaser (his own audio, as recorded; calm music very low under it)
    cues, keys, parts = [], [], []
    tt = 0.3
    marks = [round(tt + sum(b - a for _, a, b in segs[:i]), 3) for i in range(len(segs) + 1)]
    cues.append(dict(t=0, d=teaser_len, k='TeaserHead', p=dict(text='هتشوف في الكورس ده', sub='لقطات من جوه الكورس', marks=marks)))
    for i, ((st, a, b), (_, _, cap, app)) in enumerate(zip(segs, D.TEASER)):
        parts.append(dict(at=round(tt, 3), from_=round(st, 3), to=round(st + b - a, 3), rate=1, file=PUB + 'teaser.mp4'))
        keys.append(dict(t=round(tt, 3), m='teaser'))
        c = [c for c in chs if c['src'] <= a + 0.01][-1]
        cues.append(dict(t=round(tt, 3), d=round(b - a, 3), k='TeaserCap', p=dict(text=cap, app=app, n=i + 1, total=len(segs), at=fmt(c['t'] + a - c['src']))))
        tt += b - a
    keys.append(dict(t=round(tt, 3), m='hide'))
    dump('teaser', dict(duration=teaser_len, parts=parts, keys=keys, cues=cues,
                        music=[dict(t=0, d=teaser_len, file=MUSIC, from_=20, vol=0.06, fade=0.4)]))

    # ---- opening pages (music only)
    scenes, tt = [], 0.0
    for k, d, p in D.OPEN:
        scenes.append(dict(t=tt, d=d, k=k, p=p)); tt += d
    pr = []
    for pi, (title, sub, ico, col) in enumerate(D.PARTS):
        cs = [c for c in chs if c['part'] == pi]
        nxt = [c for c in chs if c['part'] > pi]
        b = nxt[0]['sep'] if nxt else course_end
        pr.append(dict(title=title, sub=sub, ico=ico, c=col, time=f"{fmt(cs[0]['sep'])} – {fmt(b)}", count=len(cs) + (1 if pi == len(D.PARTS) - 1 else 0)))
    scenes.append(dict(t=tt, d=D.PARTS_SEC, k='OParts', p=dict(title=D.PARTS_TITLE, parts=pr))); tt += D.PARTS_SEC
    groups = []
    for pi, (title, sub, ico, col) in enumerate(D.PARTS):
        items = [dict(time=fmt(c['sep']), ar=c['ar'], ico=c['ico']) for c in chs if c['part'] == pi]
        if pi == len(D.PARTS) - 1: items.append(dict(time=fmt(course_end), ar=D.EXTRA[0], ico=D.EXTRA[2]))
        groups.append(dict(title=f'{pi + 1}. {title}', c=col, items=items))
    for g in D.STAMP_PAGES:
        scenes.append(dict(t=tt, d=D.STAMP_SEC, k='OStampsParts', p=dict(groups=[groups[i] for i in g]))); tt += D.STAMP_SEC
    dump('pages', dict(duration=pages_len, scenes=scenes, keys=[dict(t=0, m='hide')],
                       music=[dict(t=0, d=pages_len, file=MUSIC, from_=0, vol=0.14, fade=1.2)]))

    # ---- all separators back to back (4 s each) in ONE render; assemble.sh cuts sep k at k*SEP
    scenes, music = [], []
    for c in chs + [dict(n=TOTAL, part=len(D.PARTS) - 1, ar=D.EXTRA[0], en=D.EXTRA[1], ico=D.EXTRA[2], src=None)]:
        k = c['n'] - 1
        pt = D.PARTS[c['part']]
        th = thumb(c['src'] + (8 if c['n'] == 1 else 3), f"ch{c['n']:02d}.jpg") if c['src'] is not None else PUB + 'pics/premiere_course_thumb.jpg'
        scenes.append(dict(t=k * SEP, d=SEP, k='Sep', p=dict(n=c['n'], total=TOTAL, ep=c['part'] + 1, title=c['ar'], en=c['en'], ico=c['ico'],
                                                       thumb=th, part=pt[0], partN=c['part'] + 1, partC=pt[3])))
        music.append(dict(t=k * SEP, d=SEP, file=MUSIC, from_=8 + (c['n'] * 7) % 90, vol=0.14, fade=0.8))
    dump('seps', dict(duration=TOTAL * SEP, scenes=scenes, keys=[dict(t=0, m='hide')], music=music))

    # ---- ending (Claude: what to study next + his videos)
    scenes, tt = [], 0.0
    for k, d, p in D.END:
        scenes.append(dict(t=tt, d=d, k=k, p=p)); tt += d
    end_len = g30(tt)
    dump('end', dict(duration=end_len, scenes=scenes, keys=[dict(t=0, m='hide')],
                     music=[dict(t=0, d=end_len, file=MUSIC, from_=40, vol=0.12, fade=1.2)]))

    # ---- the cut list for assemble.sh (in timeline order)
    pieces = [dict(file='render/teaser.mp4', ss=0, t=teaser_len), dict(file='render/pages.mp4', ss=0, t=pages_len)]
    for c in chs:
        pieces.append(dict(file='render/seps.mp4', ss=(c['n'] - 1) * SEP, t=SEP))
        pieces.append(dict(file='SRC', ss=c['src'], t=round(c['end'] - c['src'], 4)))
    pieces.append(dict(file='render/seps.mp4', ss=(TOTAL - 1) * SEP, t=SEP))
    pieces.append(dict(file='render/end.mp4', ss=0, t=end_len))
    json.dump(pieces, open(PROJ / 'work/pieces.json', 'w'), indent=1)
    total = course_end + SEP + end_len
    json.dump(dict(teaser=teaser_len, pages=pages_len, total=round(total, 3),
                   chapters=[dict(n=c['n'], part=c['part'] + 1, time=fmt(c['sep']), sep=c['sep'], src=c['src'], ar=c['ar'], en=c['en']) for c in chs]
                   + [dict(n=TOTAL, part=len(D.PARTS), time=fmt(course_end), sep=course_end, ar=D.EXTRA[0])]),
              open(PROJ / 'work/chapters.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('teaser', teaser_len, 'pages', pages_len, 'first chapter', fmt(chs[0]['sep']), 'course ends', fmt(course_end), 'total', fmt(total))


if __name__ == '__main__':
    main()
