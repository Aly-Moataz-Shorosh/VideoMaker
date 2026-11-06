# Film-making course (2026-11-06): his ~5-year-old online session (1:22:57, 1080p60) as ONE YouTube video.
# Aly: NO separators (saves render time) -> only an OPENING and an ENDING are rendered; the course itself goes in untouched.
# Final = teaser (his clips) -> his intro sting -> opening pages (Claude's coverage, parts, timestamps) -> course as-is
#         -> ending (what's missing to study + his courses) -> his outro (alpha) over the frozen last page.
#   python make_open.py          -> work/props_teaser.json, props_pages.json, props_end.json, chapters.json, teaser.mp4 in public
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent.parent
ML = PROJ.parent.parent / 'motion-library'
PUB = 'projects/filmcourse/'
SRC = PROJ / 'input/2026-11-06 14-39-41.mp4'
SRC_LEN = 4977.45
FPS = 30
INTRO_LEN = 4.433  # brand/clips/genjutsu_intro_sting.mp4
MUSIC = PUB + 'music/lofi_coffee_shop.mp3'  # Pixabay, no Content ID (approved in the premiere + audio courses)
sys.path.insert(0, str(HERE))
import film_data as D


def fmt(t):
    t = int(t)
    return f'{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}' if t >= 3600 else f'{t // 60}:{t % 60:02d}'


def dump(name, props):
    for p in props.get('parts', []): p['from'] = p.pop('from_')
    for m in props.get('music', []): m['from'] = m.pop('from_')
    props.setdefault('parts', []); props.setdefault('keys', []); props.setdefault('cues', []); props.setdefault('huds', []); props.setdefault('sfx', [])
    json.dump(dict(fps=FPS, **props), open(PROJ / f'work/props_{name}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def teaser():
    # Cut the teaser pieces once into ONE small 30 fps file (the 1.8 GB source never goes into public/: Remotion copies public on every bundle)
    out = ML / 'public' / PUB / 'teaser.mp4'
    segs, t = [], 0.0
    for a, b, *_ in D.TEASER: segs.append((t, a, b)); t += b - a
    if not out.exists():
        fc = ''.join(f'[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=1276:720[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];' for i, (_, a, b) in enumerate(segs))
        fc += ''.join(f'[v{i}][a{i}]' for i in range(len(segs))) + f'concat=n={len(segs)}:v=1:a=1[v][a]'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(SRC), '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                        '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-c:a', 'aac', '-b:a', '256k', str(out)], check=True)
    return segs, t


def main():
    pages_len = sum(d for _, d, _ in D.OPEN) + D.PARTS_SEC + D.STAMP_SEC * len(D.STAMP_PAGES)
    segs, tl = teaser()
    teaser_len = tl + 0.6
    offset = teaser_len + INTRO_LEN + pages_len  # where the course starts in the final video
    chs = []
    for i, (pi, s, ar, en, ico) in enumerate(D.CH):
        chs.append(dict(n=i + 1, part=pi, src=s, t=offset + s, ar=ar, en=en, ico=ico))
    course_end = offset + SRC_LEN

    # ---- teaser (his own audio, as recorded; calm music very low under it)
    cues, keys, parts = [], [], []
    tt = 0.3
    marks = [round(tt + sum(b - a for _, a, b in segs[:i]), 3) for i in range(len(segs) + 1)]
    cues.append(dict(t=0, d=round(teaser_len, 3), k='TeaserHead', p=dict(text='هتشوف في الكورس ده', sub='لقطات من جوه الكورس', marks=marks)))
    for i, ((st, a, b), (_, _, cap, app)) in enumerate(zip(segs, D.TEASER)):
        parts.append(dict(at=round(tt, 3), from_=round(st, 3), to=round(st + b - a, 3), rate=1, file=PUB + 'teaser.mp4'))
        keys.append(dict(t=round(tt, 3), m='teaser'))
        c = [c for c in chs if c['src'] <= a + 0.01][-1]
        cues.append(dict(t=round(tt, 3), d=round(b - a, 3), k='TeaserCap', p=dict(text=cap, app=app, n=i + 1, total=len(segs), at=fmt(offset + a))))
        tt += b - a
    keys.append(dict(t=round(tt, 3), m='hide'))
    dump('teaser', dict(duration=round(teaser_len, 3), parts=parts, keys=keys, cues=cues, scenes=[],
                        music=[dict(t=0, d=round(teaser_len, 3), file=MUSIC, from_=20, vol=0.06, fade=0.4)]))

    # ---- opening pages (music only)
    scenes, tt = [], 0.0
    for k, d, p in D.OPEN:
        scenes.append(dict(t=tt, d=d, k=k, p=p)); tt += d
    pr = []
    for pi, (title, sub, ico, col) in enumerate(D.PARTS):
        cs = [c for c in chs if c['part'] == pi]
        nxt = [c for c in chs if c['part'] > pi]
        b = nxt[0]['t'] if nxt else course_end
        pr.append(dict(title=title, sub=sub, ico=ico, c=col, time=f"{fmt(cs[0]['t'])} – {fmt(b)}", count=len(cs)))
    scenes.append(dict(t=tt, d=D.PARTS_SEC, k='OParts', p=dict(title=D.PARTS_TITLE, parts=pr))); tt += D.PARTS_SEC
    groups = []
    for pi, (title, sub, ico, col) in enumerate(D.PARTS):
        items = [dict(time=fmt(c['t']), ar=c['ar'], ico=c['ico']) for c in chs if c['part'] == pi]
        if pi == len(D.PARTS) - 1: items.append(dict(time=fmt(course_end), ar=D.EXTRA[0], ico=D.EXTRA[2]))
        groups.append(dict(title=f'{pi + 1}. {title}', c=col, items=items))
    for g in D.STAMP_PAGES:
        scenes.append(dict(t=tt, d=D.STAMP_SEC, k='OStampsParts', p=dict(groups=[groups[i] for i in g]))); tt += D.STAMP_SEC
    assert abs(tt - pages_len) < 1e-6
    dump('pages', dict(duration=round(tt, 3), scenes=scenes, keys=[dict(t=0, m='hide')],
                       music=[dict(t=0, d=round(tt, 3), file=MUSIC, from_=0, vol=0.14, fade=1.2)]))

    # ---- ending (Claude: what to study next + his courses/videos)
    scenes, tt = [], 0.0
    for k, d, p in D.END:
        scenes.append(dict(t=tt, d=d, k=k, p=p)); tt += d
    dump('end', dict(duration=round(tt, 3), scenes=scenes, keys=[dict(t=0, m='hide')],
                     music=[dict(t=0, d=round(tt, 3), file=MUSIC, from_=40, vol=0.12, fade=1.2)]))

    json.dump(dict(teaser=round(teaser_len, 3), intro=INTRO_LEN, pages=round(pages_len, 3), offset=round(offset, 3), end=round(tt, 3),
                   chapters=[dict(n=c['n'], part=c['part'] + 1, time=fmt(c['t']), src=c['src'], ar=c['ar'], en=c['en']) for c in chs]
                   + [dict(n=len(chs) + 1, time=fmt(course_end), ar=D.EXTRA[0])]),
              open(PROJ / 'work/chapters.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('teaser', round(teaser_len, 1), 'pages', pages_len, 'course starts', fmt(offset), 'ends', fmt(course_end), 'end pages', tt)


if __name__ == '__main__':
    main()
