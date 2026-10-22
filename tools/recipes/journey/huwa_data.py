"""هو ايه terms 1..30 (playlist 02..31) as shorts, built the approved way (pilot 8, Aly 2026-10-23 "كدا فهمت زوقي"):
HIS episode motion (jy_clip, boxes found automatically, whole frame when his picture fills it) + key-word chips under it on his
words + outro (term + the next term). Times = seconds in his episode.  Short number = playlist position (order Aly asked for)."""
import glob, subprocess
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parents[2]
NEXT_AFTER_LAST = 'المجالات و ساحر أوز'
# ep: (English term on screen, end word to stop at (None = last word), chips [(t, text)])
TERMS = {
    '02': ('Software Application', None, [(6.7, '📱 برنامج على موبايل أو كمبيوتر'), (9.6, '🪟 ويندوز • ماك • لينكس'), (12.5, '🛠️ أدوات تحل مشكلة'),
                                       (18.5, '🏭 زي مكنة جديدة في مصنع'), (27.5, '💰 بفلوس ولا ببلاش'), (34.6, '🧱 فوق الـ Operating System')]),
    '03': ('Plugins & Add-ons', None, [(9.6, '🪖 البرنامج = الجندي'), (16.6, '🎯 سنايبر = إضافة'), (23.2, '✈️ طيارة = إضافة تانية'),
                                    (26.3, '🧩 Plugins / Add-ons'), (34.6, '➕ خدمة زيادة على البرنامج'), (41.5, '💰 بفلوس ولا ببلاش')]),
    '04': ('Open Source', None, [(13.2, '💻 البرنامج = كود'), (17.9, '📦 ملف exe.'), (26.5, '🔒 الكود مع التيم بس'), (30.0, '🔓 Open Source = مفتوح المصدر'),
                              (40.2, '👥 تقدر تشارك في تطويره'), (44.0, '🆓 غالبًا ببلاش')]),
    '05': ('Ecosystem', None, [(6.6, '🌿 النظام البيئي'), (15.6, '🐾 كائنات حية وغير حية'), (22.5, '⚖️ أي خلل يهدم النظام'), (33.2, '💻 في التكنولوجيا'),
                            (36.4, '🤝 برامج متعاونة'), (52.6, '🔁 ناتج برنامج يدخل للتاني')]),
    '06': ('Adobe', None, [(10.8, '🖼️ فوتوشوب'), (18.9, '🏢 شركة برامج جرافيك'), (21.6, '🧩 بلاجنز كتير'), (30.2, '🌿 Ecosystem'), (41.3, '📅 اشتراك مش شرا'),
                        (53.3, '☁️ مساحة على الكلاود')]),
    '07': ('Pixels & Raster', None, [(13.3, '🔍 زوم جامد = مربعات'), (19.6, '🟥 Pixels'), (30.3, '⬛ أصغر وحدة في الصورة'), (39.1, '🖼️ Raster / Bitmap'),
                                  (42.6, '📄 صيغ ملفات معينة')]),
    '09': ('Image Compositing', None, [(7.1, '🧩 Compositing = تركيب'), (12.6, '🖼️ صور • 3D • illustrations'), (15.8, '➡️ صورة واحدة'), (23.8, '📄 الناتج صورة Raster'),
                                    (30.7, '✏️ لو Vectors بس')]),
    '10': ('Photo Editing & Retouching', None, [(6.6, '✂️ تحرير الصور'), (11.1, '🧹 تشيل اللي مش عايزه'), (13.6, '💡 الإضاءة • 🎨 الألوان'), (17.3, '🌫️ بلور للخلفية'),
                                             (19.6, '✨ تشيل النمش')]),
    '11': ('Mockup', None, [(6.6, '👕 تيشيرت • 🧃 علبة عصير'), (12.2, '👤 تعرض شغلك لعميل'), (18.0, '👀 يتخيله وهو مطبوع'), (22.9, '📐 Mockup = تمبلت'),
                         (29.3, '⚡ في ثواني عرض أحسن'), (33.7, '💰 بفلوس ولا ببلاش')]),
    '12': ('RGB & CMYK', 'CMYK', [(6.8, '🔴🟢🔵 RGB'), (9.0, '🔵🟣🟡⚫ CMYK'), (15.8, '🖥️ RGB = كل ما هو ديجيتال'), (22.7, '🖨️ CMYK = الطباعة')]),
    '13': ('Resolution', None, [(7.3, '📺 HD'), (15.9, '📐 Resolution = عدد البيكسلز'), (24.4, '📏 الطول × العرض'), (28.4, '🔍 بيكسلز أكتر = تفاصيل أكتر'),
                             (37.6, '🌐 للنت: 72 PPI'), (48.9, '🖨️ للطباعة: 300 PPI')]),
    '14': ('3D Modeling', None, [(6.9, '🧊 Modeling'), (12.0, '🎓 Blender Guru'), (21.5, '🗿 شكل حقيقي ← 3D'), (30.8, '🎬 فيلم • 🎮 جيمينج • 🎨 ديزاين'),
                              (35.9, '✋ الطريقة المانوال')]),
    '15': ('Materials & Shaders', None, [(6.7, '🧱 Materials / Shaders'), (10.4, '🎨 اللون • النعومة • الخشونة'), (13.2, '🔍 الشفافية • الانعكاس'),
                                      (21.4, '🧊 تتحط على الموديل'), (31.6, '🛠️ برامج متخصصة')]),
    '16': ('Lighting', None, [(6.7, '💡 الإضاءة في الـ 3D'), (13.8, '🎥 مكان الكاميرا'), (15.5, '📸 زي التصوير في الواقع'), (17.5, '🔦 أنواع إضاءات كتير')]),
    '17': ('Sculpting', None, [(6.7, '🗿 Sculpting = النحت'), (9.6, '🧊 بعد الموديل'), (12.4, '✨ تفاصيل أكتر')]),
    '18': ('Rendering', None, [(6.7, '🖥️ Rendering'), (10.4, '🎞️ المنتج الأخير: صورة أو فيديو'), (16.7, '🎮 Real-time في الألعاب'), (25.1, '🎬 Render Engine للأفلام'),
                            (41.2, '💡 الضوء • 🎨 الخامات'), (48.5, '⚙️ Render Engines كتير')]),
    '19': ('Rigging', None, [(6.9, '🦴 Rigging'), (10.2, '2D • 3D'), (13.6, '🧍 الشخصيات'), (17.0, '🦴 عضم يحركها')]),
    '20': ('Animating', None, [(6.6, '🎨 رسمت الشخصيات'), (10.8, '🦴 عملت Rigging'), (14.5, '🎬 Animating = التحريك'), (17.9, '📚 مبادئ الأنيميشن')]),
    '21': ('2D / 3D Physics', None, [(6.7, '🍎 جاذبية • 💨 رياح'), (20.0, '🧮 البرنامج يحسبها'), (24.2, '⚙️ Physics Tools'), (32.0, '🧩 Newton لـ After Effects')]),
    '22': ('3D Simulations', None, [(6.7, '🧪 Simulations = محاكاة'), (13.1, '🎬 أنيميشن صعب من غيرها'), (21.0, '🌊 سوائل • 💨 دخان • 🔥 نار')]),
    '23': ('Keying & Rotoscoping', None, [(11.5, '🟩 Green Screen'), (14.8, '🎨 Keying = تشيل لون'), (23.4, '🟩🟦 بعيد عن لون البشرة'),
                                       (33.0, '✂️ Rotoscoping = قص صورة صورة'), (49.7, '⬛⬜ Track Matte')]),
    '24': ('Matte Painting', None, [(6.8, '✂️ بعد القص'), (20.8, '🏔️ Matte Painting'), (31.9, '🖼️ تحط الخلفية اللي عايزها'), (37.7, '🧩 صور • فيديوهات • 3D'),
                                 (44.7, '✨ VFX • Color Correction')]),
    '25': ('CGI', None, [(6.7, '💻 Computer Generated Imagery'), (14.2, '🎬 أفلام • 🎮 ألعاب • 📺 إعلانات'), (20.5, '🧊 أكتر في الـ 3D'), (27.7, '🧸 من Toy Story لـ Avatar')]),
    '26': ('Visual Effects', None, [(6.8, '✨ Visual Effects'), (10.8, '2D / 3D + مشهد حقيقي'), (14.6, '⚖️ CGI ≠ VFX'), (18.8, '🎥 أساسها تصوير حقيقي')]),
    '27': ('SFX & FX', None, [(6.7, '💥 Special Effects = في الحقيقة'), (19.1, '🔊 Sound Effects'), (22.5, '💻 Digital Effects'), (27.9, '💥 انفجار • 🔥 نار • 🌧️ مطر')]),
    '28': ('Motion & Object Tracking', None, [(6.7, '✨ Visual Effects'), (12.5, '🎥 الكاميرا بتتحرك'), (16.2, '🎯 Motion Tracking'), (20.7, '🧊 تحط موديل 3D'),
                                           (30.3, '✋ Object Tracking')]),
    '29': ('Video Editing', None, [(6.7, '🎞️ Video Editing = المونتاج'), (15.4, '🧩 ترتيب المشاهد والصور'), (19.8, '⏱️ على الخط الزمني'), (27.7, '🎂 فيديو عيد ميلاد'),
                                (33.9, '⭐ الإتقان مش سهل')]),
    '30': ('Video Compositing', None, [(8.7, '🎞️ Compositing في الفيديو'), (11.8, '🧩 تجميع عناصر'), (16.7, '📍 مكان واحد • ⏱️ وقت واحد'), (33.1, '⭐ أهم مهارة لـ VFX artist')]),
    '31': ('Layer Based vs Node Based', None, [(16.6, '2️⃣ طريقتين للشغل'), (20.8, '📚 Layer Based'), (25.1, '📚 طبقات فوق بعض'), (28.5, '🔗 Node Based'),
                                            (31.9, '🔗 كروت متوصلة')]),
}
WFIX_HUWA = {'لشان': 'علشان', 'بيقى': 'بقى', 'قدقة': 'بدقة', 'مكنا': 'مكنة', 'مشدس': 'مسدس', 'الإيكو': 'الإيكو', 'باكسيلا': 'بيكسلة', 'بيت': 'بيت',
             'التشخصيات': 'الشخصيات', 'لناوية': 'لو ناوي', 'عضم': 'عضم', 'بشاسم': 'بشرط', 'اخضره': 'أخضر', 'الكيينج': 'الكيينج', 'كرومة': 'كروما',
             'الكوبيدر': 'الكمبيوتر', 'المؤسرات': 'المؤثرات', 'المؤسلات': 'المؤثرات', 'تبنيجه': 'تدمجه', 'العلعاب': 'الألعاب', 'الافاتار': 'Avatar',
             'وخمايات': 'وخامات', 'النقومة.': 'النعومة.', 'الخشولة.': 'الخشونة.', 'الدق': 'الضوء', 'ونعكاسه.': 'وانعكاسه.', 'ماتيريالز': 'Materials',
             'مودلنج': 'Modeling', 'رندرينج': 'Rendering', 'ريجنج': 'Rigging', 'رزيليوشن': 'Resolution', 'بيكسلز': 'Pixels', 'ادوبي': 'Adobe',
             'موكب': 'Mockup', 'كم': '--', 'بوزدينك': 'Compositing', 'بوزدين': 'Compositing', 'ايكو': 'Eco', 'سيستم': 'System', 'سيجيوي': 'CGI', 'دكتنوهي': '--',
             'فسيكرافكس': 'Physics', 'فسيكس': '--', 'تعالواي': '--', 'ترايكينج': 'Tracking', 'إفكت': 'Effects', 'وديجيطال': 'وديجيتال', 'كيينغ': 'Keying',
             'روتوسكوبينغ': 'Rotoscoping', 'لير': 'Layer', 'مود': 'Node', 'بيست': 'Based', 'انهواي': '--', 'اشتركوا': '--'}


def _boxes(ep, t0, t1):
    """runs of his picture's bounding box (1920x1080) every 0.25 s; same rule as content_boxes.py"""
    src = glob.glob(str(P / 'input' / f'{ep}_*.mp4'))[0]
    W, H, STEP = 480, 270, 0.25
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t0), '-t', str(t1 - t0), '-i', src, '-vf', f'fps={1 / STEP},scale={W}:{H}',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.int16)
    bg = np.median(fr, axis=0)
    out = []
    for i, f in enumerate(fr):
        m = np.abs(f - bg).sum(2) > 45
        m[:int(H * 0.09)] = False; m[int(H * 0.91):] = False
        ys, xs = np.where(m)
        if len(xs) < 60:
            out.append(None); continue
        x0, x1 = np.percentile(xs, [1, 99]); y0, y1 = np.percentile(ys, [1, 99])
        out.append([int(x0 * 4), int(y0 * 4), int(x1 * 4), int(y1 * 4)])
    return [(t0 + i * STEP, b) for i, b in enumerate(out)]


FULL = [0, 98, 1920, 982]  # his letterbox: the picture between the black bars


def segments(ep, a, b):
    """his motion as clip segments [(start, box)] over [a, b]: small pictures zoomed, big ones = the whole frame; >= 2 s each"""
    runs = []
    for t, bx in _boxes(ep, a, b):
        if bx is not None and (bx[2] - bx[0] > 1400 or bx[3] - bx[1] > 780):
            bx = FULL
        if bx is not None:  # a little air around his picture
            bx = [max(0, bx[0] - 40), max(98, bx[1] - 30), min(1920, bx[2] + 40), min(982, bx[3] + 30)]
        if runs and (bx is None or runs[-1][1] is None or max(abs(p - q) for p, q in zip(bx, runs[-1][1])) < 90):
            if runs[-1][1] is None and bx is not None:
                runs[-1][1] = bx
            continue
        runs.append([t, bx])
    out = []
    for t, bx in runs:
        if bx is None:
            continue
        if out and t - out[-1][0] < 2.0:  # too short: grow the previous box instead of a new scene
            pb = out[-1][1]; out[-1][1] = [min(pb[0], bx[0]), min(pb[1], bx[1]), max(pb[2], bx[2]), max(pb[3], bx[3])]; continue
        out.append([max(a, t), bx])
    if not out:
        out = [[a, FULL]]
    out[0][0] = a - 0.2
    return out


def build_all():
    from jy_audio import transcript
    eps = sorted(TERMS)
    order = ['%02d' % n for n in range(2, 32)]
    shorts = {}
    for ep in eps:
        term, endw, chips = TERMS[ep]
        n = int(ep); k = n - 1  # term number
        ws = [w for s in transcript(ep)['sentences'] for w in s['words']]
        first = ws[0]['start']
        if endw:
            last = [w for w in ws if endw in w['w']][-1]['start']
        else:
            last = ws[-1]['start']
        nxt_ep = order[order.index(ep) + 1] if ep != '31' else None
        nxt = TERMS[nxt_ep][0] if nxt_ep in TERMS else ('Vectors' if nxt_ep == '08' else NEXT_AFTER_LAST)
        # outro starts at "ده كان هو ايه" (or 2.5 s before the last word)
        outro = next((w['start'] for i, w in enumerate(ws) if w['w'] in ('ده', 'دا', 'ذا') and i + 2 < len(ws) and 'كان' in ws[i + 1]['w'] and ws[i]['start'] > last - 6), last - 2.5)
        segs = segments(ep, first, outro)
        scenes = []
        for i, (t, bx) in enumerate(segs):
            cs = [dict(t=ct, text=tx) for ct, tx in chips if t <= ct < (segs[i + 1][0] if i + 1 < len(segs) else outro)]
            scenes.append(dict(t='jy_clip', at=round(t, 2), src=f'src_{ep}.mp4', box=bx, title=term, chips=cs))
        scenes.append(dict(t='huwa_outro', at=round(outro, 2), term=term, next=nxt, b=dict(next=round(min(last, outro + 1.2), 2))))
        shorts[n] = dict(ep=ep, sec='huwa', label=f'مصطلح {k} من 30', vid_title=f'هو ايه | {term}', slug=term.lower().replace(' & ', '_').replace(' / ', '_')
                         .replace(' ', '_').replace('/', '_'), pieces=[(first, last)], scenes=scenes, WFIX=WFIX_HUWA, real=[])
    return shorts
