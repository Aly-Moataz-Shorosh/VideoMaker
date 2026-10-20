# Build props for the `course` composition (premiere pro course, 2026-10-16).
#   python make_course.py <part>     part = "ch1" (opening + chapter 1 + the separator to chapter 2, for Aly's first review)
# Writes work/props_<part>.json + work/chapters.json (final timeline time of every chapter = the description timestamps).
# Rules (Aly): nothing is cut from his course; boring waits play x4 with a note (FF); music only under the timestamps and the
# chapter separators; sfx minimal; the screen recording is visible the whole course (full / side modes).
import json, subprocess, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent.parent
PUB = 'projects/premiere/'
FPS = 25
SEP = 4.0  # separator length (s)
EP_LEN = {1: 4483.05, 2: 3214.43, 3: 2798.68}

# Chapters: (episode, source start s, Arabic title, English, icon). A chapter ends where the next one starts.
CH = [
    (1, 0, 'الفيديو و Frame rate', 'Frames & FPS', 'film'),
    (1, 130.9, 'Resolution و 4K', 'Resolution', 'grid'),
    (1, 264, 'يعني إيه Timeline؟', 'Timeline', 'timeline'),
    (1, 464, 'يعني إيه Keyframe؟', 'Keyframes', 'key'),
    (1, 732, 'Composition و Sequence', 'Sequences', 'seq'),
    (1, 940, 'أول مرة تفتح Premiere', 'New Project & Panels', 'app'),
    (1, 1096, 'إزاي تدخل ملفاتك', 'Import', 'import'),
    (1, 1280, 'أول Sequence', 'New Sequence', 'gear'),
    (1, 1404, 'Slow motion بالحساب', 'Frame rate math', 'slow'),
    (1, 1709, 'Sequence من الكليب', 'Sequence from clip', 'seq'),
    (1, 1820, 'تشريح الـ Timeline', 'Timeline controls', 'timeline'),
    (1, 2184, 'تسجيل Voice over', 'Voice-over', 'mic'),
    (1, 2258, 'V1 و A1', 'Source patching', 'patch'),
    (1, 2558, 'التقطيع بـ I و O', 'Insert & Overwrite', 'io'),
    (1, 2841, 'Insert من غير ما يقطع', 'Sync lock', 'lock'),
    (1, 3012, 'Linked selection و Markers', 'Linked selection', 'link'),
    (1, 3205, 'Selection و Track select', 'Selection tools', 'arrow'),
    (1, 3302, 'Razor: المقص', 'Razor tool', 'razor'),
    (1, 3437, 'Ripple و Rolling', 'Ripple & Rolling edit', 'ripple'),
    (1, 3780, 'تسريع وتبطيء', 'Rate stretch', 'rate'),
    (1, 3849, 'Slip و Slide', 'Slip & Slide', 'slip'),
    (1, 4158, 'Snap: المغناطيس', 'Snap', 'magnet'),
    (1, 4241, 'زيادة Tracks', 'Add tracks', 'plus'),
    (1, 4280, 'Export: طلّع الفيديو', 'Export', 'export'),
    (2, 0, 'تنظيم الـ Bins', 'Bins', 'folder'),
    (2, 110, 'Keyframes جوه Premiere', 'Effect Controls', 'watch'),
    (2, 509, 'Linear و Hold و Bezier', 'Keyframe interpolation', 'curve'),
    (2, 1015, 'Blending modes', 'Blend modes', 'blend'),
    (2, 1352, 'Ease in و Ease out', 'Easing', 'curve'),
    (2, 1545, 'Default transition', 'Ctrl + D', 'fade'),
    (2, 1855, 'Transitions', 'Transitions', 'trans'),
    (2, 2130, 'Effects', 'Effects & presets', 'fx'),
    (2, 2364, 'Mask', 'Masks', 'mask'),
    (2, 2790, 'الكتابة', 'Titles', 'text'),
    (2, 2992, 'Slideshow في ثواني', 'Automate to sequence', 'slides'),
    (2, 3116, 'Nest', 'Nest', 'nest'),
    (3, 0, 'الصوت: Mute و Solo و Pan', 'Audio basics', 'wave'),
    (3, 436, 'Keyframes على الصوت', 'Audio keyframes', 'pan'),
    (3, 781, 'Audio gain', 'Audio gain', 'knob'),
    (3, 830, 'Adjustment layer', 'Adjustment layer', 'layers'),
    (3, 1223, 'Tint: صبغة اللون', 'Tint', 'drop'),
    (3, 1434, 'تصحيح الألوان', 'Color workspace', 'wheel'),
    (3, 1688, 'Speed و Frame hold', 'Speed & Frame hold', 'freeze'),
    (3, 2073, 'File > New', 'Bars, matte, black video', 'newfile'),
    (3, 2365, 'Green screen', 'Ultra Key', 'green'),
    (3, 2674, 'Workspaces', 'Workspaces', 'windows'),
]
EXTRA = ('اللي ناقصك تتعلمه', 'What to learn next', 'flag')  # chapter 47, made by Claude (Aly's request)
TOTAL = len(CH) + 1
# Fast-forward waits (source s, x4, with a note). Filled per chapter as they are reviewed.
FF = {}  # {ep: [(from, to, note)]}

OPEN = [  # (scene, seconds, props)
    ('OProof', 7.5, dict(img=PUB + 'pics/proof_ep1_2018.png', line1='الكورس ده أنا عامله سنة *2018*', line2='اترفع على يوتيوب يوم 13 أبريل 2018.. يعني من 8 سنين')),
    ('OName', 7.0, dict(line1='من ساعتها الدنيا اتغيرت.. حتى الاسم!', line2='بس في الأساس هو *نفس* البرنامج', src='Adobe helpx (v26.0 – Jan 2026) · PetaPixel')),
    ('OLine', 6.5, dict(line1='و *أغلب* الأدوات لسه هي هي.. يعني الكورس ده', big='More than enough', line2='كفاية جدا إنك تبدأ مونتاج من الصفر')),
    ('OMeter', 12.0, dict(title='الكورس ده مغطي اد إيه؟', sub='قارنته ببريمير 2026 (نسخة 26.5 – سبتمبر 2026).. والنسبة بتفرق حسب انت بتقارن بإيه:', rings=[
        dict(v=1.0, head='كل مواضيع المونتاج', text='9 من 9 مواضيع في دروس Adobe الرسمية', src='adobe.com/learn', miss='ناقص: ولا موضوع'),
        dict(v=0.81, head='أدوات امتحان Adobe', text='29 من 36 نقطة تقنية في منهج الامتحان', src='certifiedprofessional.adobe.com', miss='ناقص: Text-Based Editing، Captions، Auto Reframe، Safe margins، المراجعة قبل الـ Export'),
        dict(v=0.71, head='كل حاجة في البرنامج', text='34 من 48 قسم مونتاج في دليل Premiere', src='helpx.adobe.com', miss='ناقص كمان: AI، Color mode، Multi-camera، Proxy، Motion Graphics Templates، Essential Sound'),],
        note='مستبعد: الجمهور وحقوق الملكية والـ Accessibility (22% من منهج الامتحان) + الإعدادات والتسطيب والشغل الجماعي')),
    ('OWhy', 11.0, dict(title='ليه النسبة بتفرق؟', foot='وكل الناقص ده هقولك عليه في *آخر* فصل', rows=[
        dict(ico='grid', c='#35D07F', head='المواضيع: 100%', text='الكورس شرح كل موضوع أساسي: الـ Timeline، التقطيع، الـ Keyframes، الإفكتات، الصوت، الألوان، الـ Export'),
        dict(ico='gear', c='#F5B83D', head='أدوات الامتحان: 81%', text='الامتحان بيعد أدوات بالتفصيل، وفيه أدوات مش في الكورس: Text-Based Editing، Captions، Auto Reframe'),
        dict(ico='fx', c='#3BA9F5', head='البرنامج كله: 71%', text='البرنامج زاد من 2018 لـ 2026: أدوات AI، Color mode، Captions، Multi-camera، Proxy', src='Adobe')])),
    ('OChanged', 10.0, dict(title='إيه اللي اتغير أو بقى أسهل من 2018؟', foot='هتلاقي علامة ⚡ في وقتها جوه الكورس',
        tiles=[dict(ico='app', en='Premiere', old='Premiere Pro', neu='Premiere 26', ar='الاسم بس اللي اتغير (يناير 2026)', src='Adobe helpx'),
               dict(ico='text', en='Titles', old='Legacy Title', neu='Essential Graphics', ar='الكتابة بقت بأدوات جديدة (من نسخة 23.0)', src='Adobe blog'),
               dict(ico='mask', en='Masks', old='frame by frame', neu='Object Mask', ar='الماسك بيلاقي الحاجة ويتتبعها لوحده', src='Adobe helpx')])),
    ('OVerdict', 9.0, dict(q='رأيي ككلود بعد ما اتفرجت على الكورس كله:', yes='اتفرج عليه', l1='لو بتبدأ مونتاج من الصفر: الأساسيات هنا *قوية* جدا',
        l2='ولو عارف حاجات: اقفز للفصل اللي محتاجه من الـ timestamps', l3='واللي ناقص.. هقولك عليه في *آخر* الكورس', sign='— Claude')),
    ('OLine', 5.0, dict(line1='عايز تشوف الكورس بالمونتاج القديم بتاع 2018؟', big='', line2='لينك الـ playlist الأصلية في الوصف ⬇')),
]
STAMP_SEC = 9.0  # one timestamps page per episode
EP_TITLE = {1: 'الأساسيات', 2: 'الحركة والإفكتات', 3: 'الصوت والألوان'}


def dur_of(ep, a, b):
    """Timeline length of source range a..b (x4 inside FF ranges)."""
    d = b - a
    for (x, y, _) in FF.get(ep, []):
        o = max(0, min(b, y) - max(a, x))
        d -= o * 0.75
    return d


def chapter_ranges():
    out = []
    for i, (ep, s, ar, en, ico) in enumerate(CH):
        nxt = CH[i + 1] if i + 1 < len(CH) and CH[i + 1][0] == ep else None
        out.append(dict(n=i + 1, ep=ep, src=s, end=nxt[1] if nxt else EP_LEN[ep], ar=ar, en=en, ico=ico))
    return out


def fmt(t):
    t = int(t)
    return f'{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}' if t >= 3600 else f'{t // 60}:{t % 60:02d}'


def timeline():
    """Final position of every chapter: opening, then [Sep + chapter] x N, then the extra chapter."""
    t = sum(d for _, d, _ in OPEN) + STAMP_SEC * 3
    chs = chapter_ranges()
    for c in chs:
        c['sep'] = t
        c['t'] = t + SEP
        t = c['t'] + dur_of(c['ep'], c['src'], c['end'])
    return chs, t


def thumb(ep, s, name):
    out = PROJ.parent.parent / 'motion-library/public' / PUB / 'thumbs' / name
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(s + 1.5), '-i', str(PROJ / f'input/ep{ep}.mp4'), '-frames:v', '1', '-q:v', '2', str(out)], check=True)
        autocrop(out)
    return PUB + 'thumbs/' + name


def autocrop(path):
    # Many of his slides are small pictures on black: zoom the thumbnail onto the content (16:9 box, never upscaled past 2x).
    from PIL import Image
    im = Image.open(path).convert('RGB')
    W, H = im.size
    a = np.asarray(im.convert('L'))[20:H - 34, :W - 160]  # skip title bar, taskbar, "Activate Windows" corner
    ys, xs = np.where(a > 40)
    if len(xs) > 50:
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min() + 20, ys.max() + 20
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        w = max(x1 - x0 + 60, (y1 - y0 + 60) * 16 / 9, W / 2)
        w = min(w, W); h = w * 9 / 16
        l = min(max(0, cx - w / 2), W - w); t = min(max(0, cy - h / 2), H - h)
        im = im.crop((int(l), int(t), int(l + w), int(t + h)))
    im.resize((960, 540), Image.LANCZOS).save(path, quality=90)


def build(part):
    chs, end_all = timeline()
    json.dump([dict(n=c['n'], ep=c['ep'], time=fmt(c['sep']), ar=c['ar'], en=c['en'], src=c['src']) for c in chs], open(PROJ / 'work/chapters.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    scenes, cues, keys, parts, huds, music, sfx = [], [], [], [], [], [], []
    t = 0.0
    for k, d, p in OPEN:
        scenes.append(dict(t=t, d=d, k=k, p=p)); t += d
    music_from = t
    for ep in (1, 2, 3):
        items = [dict(time=fmt(c['sep']), ar=c['ar'], ico=c['ico']) for c in chs if c['ep'] == ep]
        if ep == 3:
            items.append(dict(time=fmt(end_all), ar=EXTRA[0], ico=EXTRA[2]))
        nums = [c['n'] for c in chs if c['ep'] == ep] + ([TOTAL] if ep == 3 else [])
        scenes.append(dict(t=t, d=STAMP_SEC, k='OStamps', p=dict(range=f'الفصول {nums[0]} – {nums[-1]}', title=EP_TITLE[ep], items=items))); t += STAMP_SEC
    music.append(dict(t=0, d=t + 0.3, file=PUB + 'music/lofi_coffee_shop.mp3', from_=0, vol=0.14, fade=1.2))  # Aly: music under the whole opening

    def sep(c, nxt_thumb):
        scenes.append(dict(t=c['sep'], d=SEP, k='Sep', p=dict(n=c['n'], total=TOTAL, ep=c['ep'], title=c['ar'], en=c['en'], ico=c['ico'], thumb=nxt_thumb)))
        music.append(dict(t=c['sep'], d=SEP + 0.3, file=PUB + 'music/lofi_coffee_shop.mp3', from_=8 + (c['n'] * 7) % 90, vol=0.14, fade=0.8))
        sfx.append(dict(t=c['sep'] + 0.05, file='sfx/whoosh_2.wav', vol=0.18))

    if part == 'ch1':
        c1, c2 = chs[0], chs[1]
        sep(c1, thumb(1, 0, 'ch01.jpg'))
        T = c1['t']  # timeline second of source 0
        parts.append(dict(at=T, from_=0, to=c1['end'], rate=1, file=PUB + 'ep1.mp4'))
        huds.append(dict(t=T, d=c1['end'], ep=1, n=1, total=TOTAL, title=c1['ar']))
        L = lambda s, m, **crop: keys.append(dict(t=T + s, m=m, **crop))
        Q = lambda s, d, k, **p: cues.append(dict(t=T + s, d=d, k=k, p=p))
        # layout (source seconds): slides change at 41.1 / 43.8 / 73.7 / 92.4 / 103.7 / 114.6 / 129.2
        L(0, 'full'); L(1.0, 'side')
        L(43.9, 'side', sx=230, sy=130, sw=820)        # Muybridge horse, cropped
        L(73.8, 'side')                                # 9 vs 6 fps runners (whole slide)
        L(92.5, 'side', sx=270, sy=150, sw=740)        # gymnast strobe
        L(103.8, 'side', sx=318, sy=192, sw=640)       # fps bars
        L(114.7, 'side', sx=318, sy=180, sw=640)       # 10 fps run frames
        L(129.3, 'side')
        # left column + chips + words
        Q(1.2, 41.5, 'Agenda', ep=1, title=EP_TITLE[1], items=[dict(ico=c['ico'], ar=c['ar']) for c in chs if c['ep'] == 1][:7])
        Q(8.5, 3.0, 'Kw', en='Training', ar='تدريب / كورس')
        Q(9.8, 3.4, 'Kw', en='Premiere', ar='برنامج المونتاج بتاع Adobe', y=930)
        Q(13.6, 6.0, 'Chip', kind='tip', text='الكورس كان 3 حلقات.. وهنا اتجمعوا في فيديو واحد: 47 فصل')
        Q(44.2, 14.0, 'Flip')
        Q(58.5, 12.5, 'Fig', n='1.1', title='The Horse in Motion · Muybridge, 1878', sub='من أوائل الصور اللي قسّمت الحركة لصور ورا بعض', img=PUB + 'pics/muybridge.jpg', src='National Gallery of Art')
        Q(71.3, 7.0, 'Chip', kind='weak', text='12 صورة في الثانية: رقم تقريبي.. معلومة ضعيفة المصدر', y=90)
        Q(78.2, 3.2, 'Kw', en='Frame', ar='صورة واحدة من الفيديو')
        Q(78.4, 8.0, 'Def', term='Frame', ar='فريم', text='صورة واحدة من الصور اللي الفيديو متكون منها')
        Q(86.6, 17.0, 'FpsRace', note='كل ما الصور تزيد في الثانية.. الحركة تبقى أنعم')
        Q(101.7, 3.0, 'Kw', en='Slow motion', ar='الحركة البطيئة')
        Q(101.9, 7.0, 'Chip', kind='later', text='الـ Slow motion بالحساب في الفصل 9', y=90)
        Q(104.0, 13.5, 'Def', term='FPS', ar='فريم في الثانية', text='Frame rate يعني عدد الفريمات اللي بتظهر في الثانية الواحدة، وعشان كده اسمه FPS', src='Adobe')
        Q(108.9, 3.0, 'Kw', en='FPS', ar='Frames per second')
        Q(112.0, 7.5, 'Chip', kind='tip', text='معلومة: الأفلام الصامتة كانت 16 صورة في الثانية، ولما الصوت دخل بقت 24 (Adobe)', y=90, size=28)
        Q(117.8, 3.0, 'Kw', en='Frames', ar='فريمات = صور')
        Q(120.8, 10.3, 'PerSecond', n=30)
        Q(123.2, 3.2, 'Kw', en='Frame per second', ar='فريم في الثانية')
        # end of the review render: separator to chapter 2 + 1 s of chapter 2
        sep(c2, thumb(1, c2['src'], 'ch02.jpg'))
        parts.append(dict(at=c2['t'], from_=c2['src'], to=c2['src'] + 1.5, rate=1, file=PUB + 'ep1.mp4'))
        keys.append(dict(t=c2['sep'] - 0.01, m='side'))
        keys.append(dict(t=c2['t'], m='full'))
        duration = c2['t'] + 1.5
    else:
        raise SystemExit('unknown part ' + part)

    for p in parts: p['from'] = p.pop('from_')
    for m in music: m['from'] = m.pop('from_')
    props = dict(fps=FPS, duration=round(duration, 3), parts=parts, keys=keys, cues=cues, scenes=scenes, huds=huds, music=music, sfx=sfx)
    out = PROJ / f'work/props_{part}.json'
    json.dump(props, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(out, 'duration', fmt(duration), '| final course length', fmt(end_all), '| chapters', TOTAL)


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else 'ch1')
