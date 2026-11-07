# Short 08 from his phone recording 20261107_075352 (Aly review 3, 2026-11-07): the WHOLE recording (only the silences out), a line
# splitting جمال الشكل / جمال المحتوى on top (BeautySplit), HIS VIDEO under it (rec08w.mp4 = portrait over blurred sides), a matching
# picture for each thing he names (no picture twice).   python make_f08.py   -> work/shorts/props_08.json
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_fshorts as M
import fs_data as SD

M.SRC = M.PROJ / 'input/20261107_075352.mp4'
M.VOICE = 'rec08_720.mp4'
M.DB_CACHE = 'work/rec_075352/db10.npy'
_t = json.load(open(M.PROJ / 'work/rec_075352/transcript.json', encoding='utf-8'))
W = [(w['w'].strip(), w['start'], w['end']) for s_ in _t['sentences'] for w in s_['words'] if w['w'].strip()]
M.EPW = W
M._db.clear()


def shift_all(anim, a):  # all times here are seconds of the recording (also < 100)
    o = json.loads(json.dumps(anim))
    for k in ('items', 'chips'):
        o[k] = [dict(x, t=round(x['t'] - a, 3)) for x in o.get(k, [])]
    return o
M.shift = shift_all


def at(word, after=0.0):
    for w, s, e in W:
        if s >= after and word in w: return round(s, 2)
    raise SystemExit(f'word not found: {word} after {after}')


S = 'projects/filmcourse/stills/'
I = lambda word, after, side, img, label: dict(t=at(word, after), side=side, img=S + img, label=label)
C = lambda word, after, side, text: dict(t=at(word, after), side=side, text=text)
items = [
    I('رقعة', 0, 'form', 'f08_thuluth.jpg', 'الخط العربي'), I('نسخ', 0, 'form', 'f08_naskh.jpg', 'خط النسخ'),
    I('الشعر', 0, 'content', 'f08_burda.jpg', 'بيوت شعر: البردة'), I('تورية', 0, 'content', 'f08_verses.jpg', 'تورية وجناس وقافية'),
    I('فيلا', 40, 'form', 'f08_fil2.jpg', 'الفيل الأزرق 2'),
    I('الكيف', 60, 'content', 'f08_keif.jpg', 'الكيف'), I('العار', 60, 'content', 'f08_aar.jpg', 'العار'),
    I('افوكاتو', 60, 'content', 'f08_avocato.jpg', 'الأفوكاتو'), I('سمك', 60, 'content', 'f08_samak.jpg', 'سمك لبن تمر هندي'),
    I('ضوءة', 125, 'form', 'aspect_ibrahim.jpg', 'ضوء حلو وكادر جميل'),
    I('حركة', 133, 'content', 'f08_move.jpg', 'حركة الكاميرا'), I('زاوية', 133, 'content', 'ex_low_angle.jpg', 'زاوية الكاميرا'),
    I('شخص', 138, 'content', 'f08_count.jpg', 'الكادر فيه كام شخص'), I('هتركز', 140, 'content', 'f08_focus.jpg', 'هتركز على إيه'),
    I('ترتيب', 148, 'content', 'f08_cut.jpg', 'ترتيب الكادرات والقطع'),
    I('زرق', 160, 'form', 'f08_fil.jpg', 'الفيل الأزرق'), I('وكيرة', 160, 'form', 'f08_kira.jpg', 'كيرة والجن'),
    I('والست', 160, 'form', 'f08_sett.jpg', 'الست'), I('والارهاب', 160, 'content', 'f08_kabab.jpg', 'الإرهاب والكباب'),
]
chips = [
    C('عادي', 20, 'content', 'كلام عادي'), C('منصقة', 25, 'content', 'كلام مسجوع'), C('الركيك', 30, 'content', 'شعر ركيك'),
    C('قوي', 35, 'content', 'شعر قوي وعميق'), C('جاهلي', 35, 'content', 'شعر جاهلي'), C('فلسفي', 38, 'content', 'شعر فلسفي فيه تورية'),
    C('هدف', 80, 'content', 'كل فيلم حسب هدفه'), C('grammar', 115, 'content', 'نحو وبلاغة.. في السينما كمان'),
    C('موسيقى', 155, 'content', '🎵 الموسيقى'),
]
anim = dict(items=items, chips=chips)
# pieces = the whole recording, cut only at silences longer than 0.6 s (Aly: "قصيت كتير.. حطه زي ما كان" + no silence at 1:44)
pieces, cur = [], [W[0][1], W[0][2]]
for w, s, e in W[1:]:
    if s - cur[1] > 0.6: pieces.append(cur); cur = [s, e]
    else: cur[1] = max(cur[1], e)
pieces.append(cur)
pieces = [p for p in pieces if p[1] - p[0] > 0.25]
B = L = None
SD.SHORTS[8] = dict(no=8, chapter=2, title='الجمال *نوعين*', at='2:40', chap=2, pieces=[
    dict(a=round(a, 2), b=round(b, 2), file='rec08w.mp4', crop=dict(sx=0, sy=0, sw=1280), under=True, ak='BeautySplit', anim=anim, nocam=True) for a, b in pieces])
SD.CAP[8] = []
print(len(pieces), 'pieces', round(sum(b - a for a, b in pieces), 1), 's of speech')
M.build(8)
