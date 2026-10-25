# Props for the `course` composition: his 2021 audio session (2:03 h, one file) as ONE course video.
#   python make_course.py review1    -> opening + part 1 + the separator into part 2 (Aly's first review)
#   python make_course.py full       -> whole course
# Rules (Aly 2026-10-24): nothing cut, nothing sped up, the session's audio NEVER touched (no level, no ducking, no sfx);
# calm music ONLY inside the added opening and the added chapter separators. Chapters grouped in PARTS (one broad category each).
# Side motion only where it explains; the screen stays full most of the time.
import json, re, subprocess, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent.parent
ML = PROJ.parent.parent / 'motion-library'
PUB = 'projects/audio/'
SRC = PUB + 'course.mp4'
FPS = 30
SEP = 4.0
SRC_LEN = 7385.93
MUSIC = PUB + 'music/lofi_coffee_shop.mp3'  # Pixabay, no Content ID (approved in the premiere course)
AN = json.load(open(PROJ / 'work/analysis.json'))

PARTS = [  # (title, sub, icon, colour)
    ('ليه الصوت مهم؟', 'الصوت والصمت، الصوت بيعمل إيه، أمثلة من الأفلام', 'ear', '#F5B83D'),
    ('الصوت الديجيتال', 'الصورة الديجيتال، الموجة، Hz، Sample rate، Bit depth', 'sine', '#3BA9F5'),
    ('المايكات', 'أنواع المايكات، اتجاه المايك، تختار أنهي مايك', 'mic', '#35D07F'),
    ('الصوت جوه الفيديو', 'الحوار، الصوت المحيط، الموسيقى، المؤثرات، Sync', 'music', '#FF6B5B'),
    ('عملي: Premiere Pro', 'صوت المايك، Sync، الإفكتات، Essential Sound', 'app', '#9999FF'),
    ('عملي: Adobe Audition', 'الموجة من قريب، شيل الدوشة، الإفكتات، التسجيل', 'wave', '#19B5A5'),
    ('أسئلة وختام', 'البودكاست والسماعات + تتعلم إيه بعد كده', 'ques', '#C9CED8'),
]
# Chapters: (part index, source start s, Arabic title, English, icon). A chapter ends where the next one starts.
CH = [
    (0, 0, 'الصوت = نص الفيديو', 'Sound & silence', 'ear'),
    (0, 328, 'الصوت بيعمل إيه؟', 'What sound does', 'wave'),
    (0, 474, 'أمثلة من الأفلام', 'Sound in films', 'film'),
    (0, 965, 'مصادر الصوت وتاريخه', 'Sources & history', 'music'),
    (1, 1084, 'الصورة الديجيتال', 'Digital video', 'grid'),
    (1, 1325, 'الصوت موجة', 'Sound is a wave', 'sine'),
    (1, 1464, 'الهيرتز Hz', 'Hertz', 'sine'),
    (1, 1566, 'Sample rate', 'Sample rate', 'bits'),
    (1, 1712, 'Bit depth', 'Bit depth', 'bits'),
    (2, 2320, 'أنواع المايكات', 'Dynamic · Condenser · Ribbon', 'mic'),
    (2, 2510, 'اتجاه المايك', 'Polar patterns', 'mic'),
    (2, 2735, 'تختار أنهي مايك؟', 'Which mic?', 'ques'),
    (2, 3462, 'أكتر من مايك', 'Multiple mics', 'mic'),
    (2, 3549, 'Pop filter', 'Pop filter & Dead cat', 'mic'),
    (3, 3626, 'أنواع الصوت الأربعة', 'Four kinds of sound', 'music'),
    (3, 3751, 'الموسيقى التصويرية', 'Score', 'music'),
    (3, 3953, 'الحوار', 'Dialogue', 'mic'),
    (3, 4076, 'الصوت المحيط', 'Ambience', 'ear'),
    (3, 4152, 'Sync الصوت مع الصورة', 'Sync', 'clap'),
    (4, 4404, 'صوت الكاميرا ولا المايك؟', 'Camera vs mic audio', 'cam'),
    (4, 4522, 'Sync بالتسقيفة', 'Clap sync', 'clap'),
    (4, 4584, 'Volume و Solo و Mute', 'Audio basics', 'knob'),
    (4, 4758, 'Audio effects', 'Audio effects', 'fx'),
    (4, 4824, 'Essential Sound', 'Essential Sound', 'app'),
    (4, 4991, 'تجربة: تليفون وانفجار', 'Phone & explosion', 'fx'),
    (5, 5762, 'شاشات Audition', 'Audition panels', 'app'),
    (5, 5944, 'الموجة من قريب', 'Samples up close', 'bits'),
    (5, 6068, 'شيل الدوشة', 'Noise reduction', 'wave'),
    (5, 6618, 'Presets والإفكتات', 'Presets & effects', 'fx'),
    (5, 6836, 'التسجيل والـ Export', 'Record & export', 'export'),
    (6, 7123, 'أسئلة: البودكاست والسماعات', 'Q&A', 'phones'),
]
EXTRA = ('تتعلم إيه بعد كده', 'What to learn next', 'flag')  # last chapter, made by Claude
TOTAL = len(CH) + 1
STAMP_SEC = 7.0
PARTS_SEC = 6.0  # Aly: opening pages short, whoever wants the details pauses


def fmt(t):
    t = int(t)
    return f'{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}' if t >= 3600 else f'{t // 60}:{t % 60:02d}'


def quiet_near(t, back=2.5, fwd=1.5):
    """Quietest 150 ms point near t, so a separator never cuts into a word."""
    if t <= 0: return 0.0
    r = np.array(AN['rms'])
    best, bt = None, t
    for i in range(max(1, int((t - back) * 10)), min(len(r) - 2, int((t + fwd) * 10))):
        v = r[i:i + 2].max()
        score = -v - abs(i / 10 - t) * 3
        if best is None or score > best: best, bt = score, i / 10 + 0.05
    return round(bt, 2)


def thumb(s, name):
    out = ML / 'public' / PUB / 'thumbs' / name
    if not out.exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(s + 2), '-i', str(ML / 'public' / SRC), '-frames:v', '1', '-vf', 'scale=960:540', '-q:v', '2', str(out)], check=True)
    return PUB + 'thumbs/' + name


# Cold open (Aly): ~13 s of the course's own best moments, his audio as recorded (cut only on word gaps), calm music under it.
TEASER = [  # (source from, to, caption, app, crop sx, sy, sw)
    (2386.35, 2390.15, 'تختار المايك الصح', None, None, None, None),
    (5284.05, 5287.05, 'صوتك يبقى تليفون', 'Premiere Pro', 240, 40, 960),
    (6027.0, 6031.05, 'تشوف الصوت نقطة نقطة', 'Audition', 280, 20, 760),
    (6323.3, 6325.55, 'تشيل الدوشة', 'Audition', 300, 60, 880),
]
OPEN = [  # (scene, seconds, props). Aly review 1: no "100% original" screen; proof frame small (it was pixelated).
    ('OProofFrame', 6.5, dict(img=PUB + 'pics/proof.png', box=[1203, 696, 40, 21],
        line1='الكورس ده متسجل *أونلاين* سنة 2021', line2='يوم 28 مارس 2021.. شرح لطلبة على Zoom',
        line3='بس المعلومات اللي فيه *لسه مفيدة جدا* لحد النهارده')),
    ('OCoverage', 9.0, None),  # props from coverage.py (Claude's opinion = coverage %, each yardstick with its source)
    ('ORecommend', 5.0, dict(q='ليه أنصحك بالكورس ده؟', rows=[  # Aly review 2: Claude's reasons, each one really in the session
        dict(head='بيبدأ من ليه الصوت مهم', sub='الصوت بيعمل إيه في الفيديو، بأمثلة من أفلام', ico='ear', c='#F5B83D'),
        dict(head='الصوت الديجيتال ببساطة', sub='الموجة، Hz، Sample rate، Bit depth', ico='sine', c='#3BA9F5'),
        dict(head='تختار المايك صح', sub='الأنواع، اتجاه المايك، Shotgun / Pop filter / Dead cat', ico='mic', c='#35D07F'),
        dict(head='عملي على فيديو حقيقي', sub='Premiere + Audition: تشيل الدوشة، Essential Sound، الإفكتات', ico='wave', c='#19B5A5'),
    ])),
]


def chapters():
    out = []
    for i, (pi, s, ar, en, ico) in enumerate(CH):
        out.append(dict(n=i + 1, part=pi, src=quiet_near(s), ar=ar, en=en, ico=ico))
    for i, c in enumerate(out):
        c['end'] = out[i + 1]['src'] if i + 1 < len(out) else SRC_LEN
    return out


def word_list():
    d = json.load(open(PROJ / 'work/transcript.json', encoding='utf-8'))
    return [(w['w'].strip(' .,?!،'), w['start']) for s in d['sentences'] for w in s['words'] if w['w'].strip()]


def build(mode):
    chs = chapters()
    parts_len = 7.0 + 2 * STAMP_SEC
    teaser_len = sum(b - a for a, b, *_ in TEASER) + 0.6
    t = teaser_len + sum(d for _, d, _ in OPEN) + PARTS_SEC + 2 * STAMP_SEC
    for c in chs:
        c['sep'] = t; c['t'] = t + SEP; t = c['t'] + (c['end'] - c['src'])
    end_course = t
    # part ranges for the map
    pr = []
    for pi, (title, sub, ico, col) in enumerate(PARTS):
        cs = [c for c in chs if c['part'] == pi]
        a = cs[0]['sep']; b = cs[-1]['t'] + cs[-1]['end'] - cs[-1]['src']
        pr.append(dict(title=title, sub=sub, ico=ico, c=col, time=f'{fmt(a)} – {fmt(b)}', count=len(cs) + (1 if pi == len(PARTS) - 1 else 0)))
    scenes, cues, keys, vids, huds, music = [], [], [], [], [], []
    import course_cards as K
    tt = 0.3
    marks = [round(tt + sum(b - a for a, b, *_ in TEASER[:i]), 3) for i in range(len(TEASER) + 1)]
    cues.append(dict(t=0, d=round(teaser_len, 3), k='TeaserHead', p=dict(text='هتشوف في الكورس ده', sub='لقطات من جوه الكورس', marks=marks)))
    for i, (a, b, cap, app, sx, sy, sw) in enumerate(TEASER):
        vids.append(dict(at=round(tt, 3), from_=a, to=b, rate=1, file=SRC))
        keys.append(dict(t=round(tt, 3), m='teaser', **(dict(sx=sx, sy=sy, sw=sw) if sw else {})))
        c = [c for c in chs if c['src'] <= a][-1]
        cues.append(dict(t=round(tt, 3), d=round(b - a, 3), k='TeaserCap', p=dict(text=cap, app=app, n=i + 1, total=len(TEASER), at=fmt(c['t'] + a - c['src']))))
        tt += b - a
    music.append(dict(t=0, d=round(teaser_len, 3), file=MUSIC, from_=20, vol=0.06, fade=0.4))
    tt = teaser_len
    words = word_list()
    import coverage as CV
    cover = dict(q='رأيي ككلود: الكورس ده بيغطي كام في المية؟', sub='قارنته بمراجع رسمية النهارده (2026).. والأداة اللي اتشرحت بتتحسب كاملة',
                 cards=CV.cards(), foot='هدف الكورس *الصوت للفيديو*.. مش إنك تتعلم البرنامجين كلهم')
    for k, d, p in OPEN:
        scenes.append(dict(t=tt, d=d, k=k, p=cover if k == 'OCoverage' else p)); tt += d
    scenes.append(dict(t=tt, d=PARTS_SEC, k='OParts', p=dict(title='الكورس *7 أجزاء*', parts=pr))); tt += PARTS_SEC
    groups = []
    for pi, (title, sub, ico, col) in enumerate(PARTS):
        items = [dict(time=fmt(c['sep']), ar=c['ar'], ico=c['ico']) for c in chs if c['part'] == pi]
        if pi == len(PARTS) - 1: items.append(dict(time=fmt(end_course), ar=EXTRA[0], ico=EXTRA[2]))
        groups.append(dict(title=f'{pi + 1}. {title}', c=col, items=items))
    scenes.append(dict(t=tt, d=STAMP_SEC, k='OStampsParts', p=dict(groups=groups[:3]))); tt += STAMP_SEC
    scenes.append(dict(t=tt, d=STAMP_SEC, k='OStampsParts', p=dict(groups=groups[3:]))); tt += STAMP_SEC
    music.append(dict(t=teaser_len, d=tt - teaser_len + 0.3, file=MUSIC, from_=0, vol=0.14, fade=1.2))

    def sep(c):
        pt = PARTS[c['part']]
        first = c['n'] == 1 or chs[c['n'] - 2]['part'] != c['part']
        scenes.append(dict(t=c['sep'], d=SEP, k='Sep', p=dict(n=c['n'], total=TOTAL, ep=c['part'] + 1, title=c['ar'], en=c['en'], ico=c['ico'],
            thumb=thumb(c['src'] + (8 if c['n'] == 1 else 0), f'ch{c["n"]:02d}.jpg'), part=pt[0], partN=c['part'] + 1, partC=pt[3])))
        music.append(dict(t=c['sep'], d=SEP + 0.3, file=MUSIC, from_=8 + (c['n'] * 7) % 90, vol=0.14, fade=0.8))
        keys.append(dict(t=round(c['t'] - 0.01, 3), m='full'))

    def chapter(c, upto=None):
        b = c['end'] if upto is None else c['src'] + upto
        vids.append(dict(at=round(c['t'], 3), from_=c['src'], to=round(b, 3), rate=1, file=SRC))
        huds.append(dict(t=c['t'], d=round(b - c['src'], 3), ep=c['part'] + 1, n=c['n'], total=TOTAL, title=c['ar']))

    seen = {}
    sel = chs if mode == 'full' else [c for c in chs if c['part'] == 0]
    for c in sel:
        sep(c); chapter(c)
        last = -9
        for w, s in words:
            if not (c['src'] <= s < c['end']): continue
            for pat, en, ar in K.GLOSS:
                if re.search(pat, w, re.I):
                    if s - seen.get(en, -9999) > 1200 and s - last > 5:
                        seen[en] = s; last = s
                        cues.append(dict(t=round(c['t'] + s - c['src'], 3), d=3.4, k='Kw', p=dict(en=en, ar=ar)))
                    break
        for s, d, k, p in K.CARDS.get(c['n'], []):
            if c['src'] <= s < c['end']:
                cues.append(dict(t=round(c['t'] + s - c['src'], 3), d=d, k=k, p=p))
    if mode == 'full':
        duration = end_course  # + extra chapter (added later)
    else:
        nx = chs[len(sel)]
        sep(nx); chapter(nx, upto=1.5)
        duration = nx['t'] + 1.5
    for p in vids: p['from'] = p.pop('from_')
    for m in music: m['from'] = m.pop('from_')
    props = dict(fps=FPS, duration=round(duration, 3), parts=vids, keys=keys, cues=sorted(cues, key=lambda q: q['t']), scenes=scenes, huds=huds, music=music, sfx=[])
    out = PROJ / f'work/props_{mode}.json'
    json.dump(props, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump([dict(n=c['n'], part=c['part'] + 1, time=fmt(c['sep']), ar=c['ar'], en=c['en'], src=c['src']) for c in chs] + [dict(n=TOTAL, time=fmt(end_course), ar=EXTRA[0])],
              open(PROJ / 'work/chapters.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(out, 'duration', fmt(duration), '| course length', fmt(end_course), '| cues', len(cues))


if __name__ == '__main__':
    sys.path.insert(0, str(HERE))
    build(sys.argv[1] if len(sys.argv) > 1 else 'review1')
