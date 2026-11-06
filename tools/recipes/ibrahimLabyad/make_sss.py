"""Shot -> Scene -> Sequence board (HTML + PNG) from props.json."""
import json, html
from pathlib import Path
W = Path(__file__).resolve().parents[1]; O = W.parent / 'output'
p = json.load(open(W / 'props.json', encoding='utf-8'))
DESC = {'PRE': 'إبراهيم لوحده على السطح بالليل', 'TI': 'إبراهيم على الترابيزة', 'TF': 'فارس بيتكلم', 'TW': 'الترابيزة (واسعة)',
        'A': 'إبراهيم بيهجم على الحارة', 'P': 'إبراهيم بيشرب/بيسف برشام', 'N': 'نرجس', 'K': 'قطع اللسان في الحارة المولعة',
        'TT': 'اللسان على المنضدة', 'R': 'السطح وقت الفجر', 'M': 'الفلوس في الحفرة', 'MB': 'عشري على الموتوسيكل'}
COL = {'55': '#4C9BE8', '56': '#F2A93B', 'add': '#E5559A', 'x': '#7D8590'}
G = [((1, 2), 'x', 'مش في السيناريو', 'سطح بالليل وإبراهيم لوحده بيشرب — مش مكتوب في مشهد 55.'),
     ((3, 16), '55', 'مشهد 55 · بهو الجلوس · ص 97 و 98', 'فارس بيسأل إبراهيم ساب معلمه ليه، ويقوله إنه اختاره عشان «ماليش سيد». بعدين «ليا شرطين»: مالكش حماية، وفزورة الأسد والضبع. (J-Cut · Shot / Reverse Shot)'),
     ((17, 64), 'cross', 'مشهد 55 (الصوت) + مشهد 56 (الصورة) · Cross-Cutting', 'فارس بيكمل حكاية الأسد والضبع، والصورة بتروح للحارة: إبراهيم بالمولوتوف والسنجة، البرشام، ونرجس. (Sound Bridge · Hidden Cut · Pacing)'),
     ((65, 89), 'add', 'إضافة الفيلم · تجسيد «لسان آدمي» · ص 99', '«لا يقدر يقتله ولا يقدر يسيبه»: قطع اللسان في الحارة المولعة متقطع مع وش إبراهيم على الترابيزة. (Jump Cut · Flash Cut)'),
     ((90, 92), '55', 'مشهد 55 · آخره · ص 99', 'إبراهيم بيحط اللسان على المنضدة. الصوت بيختفي ونقط مية. فارس بيبتسم. (Fade to Silence · SFX)'),
     ((93, 98), '56', 'مشهد 56 · Photo Montage · ص 99 لـ 101', 'صوت عشري: «إبراهيم فضل يشرب ويشرب…» على صور: السطوح، الفلوس في الحفرة، وعشري على الموتوسيكل. (V.O. · Crane · Top Shot · Jump Cuts · Tracking)')]
import re
def fix(x):
    tail = ''
    m = re.search(r'\(([A-Za-z][^)]*)\)\s*$', x)
    if m:
        tail = '<br><bdi dir="ltr" class="en">' + m.group(1) + '</bdi>'; x = x[:m.start()].rstrip()
    x = re.sub(r'(V\.O\.|[A-Za-z][A-Za-z\-]*(?: [A-Z][A-Za-z\-]*)*)', lambda k: '<bdi dir="ltr">' + k.group(0) + '</bdi>', x)
    return x + tail
rows = []
for (a, b), sc, title, ar in G:
    items = ''.join(f"<li><span class='n' style='background:{COL[s['scene']]}'>{s['n']}</span><b>{html.escape(s['size'])}</b> · {html.escape(s['move'])}"
                    f"{(' · ' + html.escape(s['extra'])) if s['extra'] else ''}<i>{DESC[s['place']]}</i></li>" for s in p['shots'][a - 1:b])
    c = COL.get(sc, '#fff')
    border = f"border-color:{c}" if sc != 'cross' else "border-image:linear-gradient(90deg,#4C9BE8,#F2A93B) 1"
    rows.append(f"<div class='row'><div class='shots' style='{border}'><div class='h'>SHOTS {a}–{b}</div><ul>{items}</ul></div>"
                f"<div class='arr'>→</div><div class='scene' style='{border}'><div class='h2'>{fix(title)}</div><p>{fix(ar)}</p></div></div>")
doc = f"""<!doctype html><html lang="ar"><meta charset="utf-8"><title>Shot Scene Sequence</title><style>
@font-face{{font-family:Cairo;src:url('../../../motion-library/public/fonts/Cairo.ttf')}}
@font-face{{font-family:Montserrat;src:url('../../../motion-library/public/fonts/Montserrat.ttf')}}
body{{margin:0;background:#0D1015;color:#EDEFF2;font-family:Cairo,Montserrat;width:1800px}}
.top{{display:flex;justify-content:space-between;align-items:end;padding:30px 40px 10px}}
.top h1{{font-size:38px;margin:0}} .cols{{display:grid;grid-template-columns:1000px 60px 420px 60px 220px;padding:0 40px;font-family:Montserrat;font-weight:900;font-size:26px;letter-spacing:3px;color:#9AA4B2}}
.wrap{{display:grid;grid-template-columns:1560px 220px;padding:0 0 40px 40px;gap:0}}
.row{{display:grid;grid-template-columns:1000px 60px 420px;align-items:center;margin:14px 0}}
.shots,.scene{{border:3px solid;border-radius:12px;background:#141920;padding:14px 18px}}
.h{{font-family:Montserrat;font-weight:900;font-size:18px;color:#9AA4B2;margin-bottom:6px}}
ul{{list-style:none;margin:0;padding:0;columns:2;column-gap:28px;direction:ltr}}
li{{font-family:Montserrat;font-size:15px;line-height:1.75;break-inside:avoid;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
li i{{font-style:normal;font-family:Cairo;color:#9AA4B2;margin-left:8px;font-size:15px}}
.n{{display:inline-block;min-width:30px;text-align:center;border-radius:4px;color:#0D1015;font-weight:900;margin-right:8px}}
.arr{{text-align:center;font-size:40px;color:#5B6573}} .scene{{direction:rtl}} .en{{font-family:Montserrat;font-size:15px;color:#9AA4B2}} .h2{{font-weight:800;font-size:22px}}
.scene p{{font-size:18px;color:#D9DEE5;margin:6px 0 0;line-height:1.6}}
.seq{{display:flex;align-items:center}} .seqbox{{border:3px solid #EDEFF2;border-radius:12px;padding:18px;direction:rtl;font-size:21px;line-height:1.6;background:#141920}}
.legend{{padding:0 40px 30px;font-family:Montserrat;font-size:16px;display:flex;gap:26px}} .legend span{{display:inline-block;width:20px;height:12px;border-radius:3px;margin-right:6px}}
</style><body>
<div class="top"><h1>Shot → Scene → Sequence · إبراهيم الأبيض (2009)</h1><div style="font-family:Montserrat;color:#C8A27A;font-weight:700;font-size:22px">Aly Shorosh</div></div>
<div class="cols"><div>SHOT (98)</div><div></div><div style="text-align:right">SCENE</div><div></div><div style="text-align:right">SEQUENCE</div></div>
<div class="wrap"><div>{''.join(rows)}</div><div class="seq"><div class="arr">→</div><div class="seqbox"><b>إبراهيم بيدخل عالم فارس</b><br>الاتفاق ← الامتحان (اللسان) ← الفلوس بتكتر.<br><span style="color:#9AA4B2;font-size:17px">من الكلام على الترابيزة لحد مونتاج عشري.</span></div></div></div>
<div class="legend"><div><span style="background:#4C9BE8"></span>Sc 55 بهو الجلوس</div><div><span style="background:#F2A93B"></span>Sc 56 Photo Montage</div><div><span style="background:#E5559A"></span>Film addition (مش مكتوبة كمشهد)</div><div><span style="background:#7D8590"></span>Not in script</div><div style="color:#9AA4B2">Shot sizes &amp; moves: StudioBinder definitions · Script: V10 (shooting draft)</div></div>
</body></html>"""
(O / 'shot_scene_sequence.html').write_text(doc, encoding='utf-8')
print('ok')
