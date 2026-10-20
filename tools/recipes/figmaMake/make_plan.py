"""figmaMake (youtube, Aly's own edit, 8:18): motion-only plan. All anchors = source seconds (no cutting).
Aly is on the LEFT (face x~0.4) -> graphics on the RIGHT. Intro 114.45-116.0 and outro 473.2-end: nothing.
Density: an event at least every ~3 s (zooms fill the holes automatically, see fill()).
Run: python work/scripts/make_plan.py  -> work/plan.json"""
import json
from pathlib import Path

W = Path(__file__).resolve().parents[1]
PJ = 'projects/2026-10-07 youtube figmaMake/'
QUIET = [[114.4, 116.05], [473.15, 498.5]]
cues = []


def add(t, at_, dur, **props):
    cues.append({'t': t, 'src': round(at_, 2), 'dur': round(dur, 2), 'props': props})


def kw(src, dur, text, tag=''):
    add('keyword_pop', src, dur, text=text, side='right', tag=tag)


def zoom(src, dur, style='punch', to=None):
    add('zoom', src, dur, style=style, to=to or {'punch': 1.22, 'push': 1.14, 'out': 1.2}[style], x=0.38, y=0.38)


def icon(src, dur, i, x=0.62, y=0.24):
    add('icon_pop', src, dur, icon=i, x=x, y=y, size=130)


def steps(src, dur, items, stagger):
    add('steps_list', src, dur, items=items, stagger=stagger, side='right')


def pic(src, dur, path, caption, fit='cover', pan=(50, 50)):
    add('side_picture', src, dur, src=path, caption=caption, side='right', fit=fit, tilt=3, panFrom=pan[0], panTo=pan[1])


def logo(src, dur, path, caption):
    pic(src, dur, path, caption, fit='contain')


PHONE = [900, 140, 500, 880]  # Quizzer phone frame in rec2/3/5/6


def screen(src, dur, rec, start, crop, title='', still=False, hw=None, marks=(), crop2=None, moveAt=0, tag='Figma Make',
           logo_='logos/figma.svg'):
    tall = crop[3] / crop[2] > 1.2
    w = hw or (0.25 if tall else 0.46)
    p = dict(src=PJ + f'rec{rec}.mp4', start=start, still=still, crop=crop, title=title, tag=tag, logo=logo_,
             hx=0.97 - w / 2 - 0.01, hw=w, htop=0.16 if tall else 0.2, marks=list(marks), accent='gold')
    if crop2:
        p.update(crop2=crop2, moveAt=moveAt, moveDur=24)
    add('screen_ui', src, dur, **p)


def flow(src, dur, items, packet='', title='', arrows=True):
    add('logo_flow', src, dur, items=[{'logo': l, 'label': t, 'at': a} for l, t, a in items], packet=packet, title=title,
        side='right', arrows=arrows)


def portal(src, dur, world, title, back=None):
    add('portal_world', src, dur, world=PJ + world, title=title, accent='gold', wipeIn=0,
        wipeBack=back if back is not None else int(dur * 30) - 16, shrink=0.95, alyX=0)


def green(src, name, dx=0.0, dy=0.0, dur=8.0, start=0.0):
    add('green_clip', src, dur, src=PJ + f'gs_{name}.webm', dx=dx, dy=dy, start=start, volume=0.6)


f = lambda s: int(round(s * 30))  # seconds -> frames inside a cue

# ---------- 0:00 hook ----------
zoom(0.0, 1.6, 'push')
logo(1.3, 1.9, 'brand/video-blog-badge.png', '')
kw(3.3, 2.6, 'عالم *الـAI*')
zoom(4.6, 1.1)
kw(6.0, 1.5, 'كل الناس *تقدر*')
icon(7.5, 1.4, '📱', 0.66, 0.3); icon(8.7, 1.4, '🌐', 0.78, 0.3); icon(9.9, 1.6, '💻', 0.9, 0.3)
zoom(7.3, 3.5, 'push')
kw(11.1, 3.6, 'معرفة *بسيطة* بالبرمجة', tag='+ AI')
zoom(12.4, 1.2)
# 0:15 Egypt map (Aly's idea): 120M -> laptops -> jump (competition) -> one stands out -> map closes like a book
s0 = 14.9
add('egypt_crowd', s0, 25.5 - s0, count=120, peopleAt=f(16.0 - s0), laptopAt=f(17.5 - s0), jumpAt=f(19.8 - s0),
    heroAt=f(21.6 - s0), closeAt=f(24.3 - s0), title1='*120 مليون* مصري', title2='كام مليون *بيبرمج*؟',
    title3='المنافسة *عالية*', title4='إيه اللي *يفرقك*؟')
zoom(25.4, 2.0, 'out')
steps(27.3, 4.6, ['Architecture صح', 'كود نضيف', 'وألف حاجة تانية'], 38)
icon(32.4, 1.4, '✋'); zoom(32.5, 1.6)
kw(34.9, 3.9, 'اللي *بيبيع* 💰')
zoom(38.9, 2.6, 'push')
kw(41.4, 4.0, 'يفضلوا *يستخدموه*')
steps(45.6, 3.2, ['🔒 آمن', '✅ جيد', '⚡ سريع'], 22)
kw(49.0, 3.0, 'السر = *السهولة*')
zoom(51.2, 1.0)
kw(52.2, 3.8, 'خدمة *رائعة* ⭐')
steps(56.1, 4.4, ['واجهة سيئة', 'معقدة', 'صعبة', 'مش مريحة'], 27)
icon(60.5, 1.5, '🚫'); zoom(60.5, 1.3)
portal(61.8, 9.0, 'w_student.jpg', 'واجهة *ممتازة* + تجربة *مثالية*')
add('bar_chart', 71.0, 4.6, title='هيوصل لكام واحد؟', unit='%', side='right',
    items=[{'label': 'واجهة وحشة', 'value': 15}, {'label': 'واجهة سهلة', 'value': 90}])
# UI/UX said 3 ways = SAME thing (Aly's note @1:20)
s1 = 75.7
add('same_word', s1, 83.3 - s1, words=[{'text': 'UI / UX', 'at': 0}, {'text': 'User Interface & Experience', 'at': f(76.9 - s1)},
    {'text': 'واجهة وتجربة المستخدم', 'at': f(78.6 - s1)}], mergeAt=f(81.0 - s1), tag='كلهم نفس الحاجة', side='right')
zoom(82.2, 1.2)
kw(83.6, 3.6, 'تصمم *واجهة* لبرنامجك')
kw(87.4, 3.6, 'تدفع لـ*ديزاينر*؟ 💸')
zoom(91.0, 1.3)
kw(92.6, 2.7, 'تعملها *بنفسك*؟')
icon(96.4, 1.5, '😬'); zoom(95.4, 3.0, 'push')
green(98.4, 'youtube_1', dur=7.8)
steps(98.6, 4.3, ['مش فنان 🎨', 'مش مهنتك', 'مش دارسه 📚'], 27)
kw(103.0, 2.0, 'علم *كبير*')
zoom(104.4, 1.2)
flow(105.2, 7.2, [('logos/claude.svg', 'Claude', 0), ('logos/figma.svg', 'Figma Make', 60)], packet='Prompt',
     title='تصميم *محترم* بالـAI')
icon(112.6, 1.3, '✨'); zoom(112.6, 1.4)
# --- intro 114.45-116.0: nothing ---
zoom(116.3, 1.4)
kw(117.4, 2.6, 'هنعمل *إيه*؟')
kw(120.2, 2.6, 'اللي *عملناه* قبل كده')
zoom(123.0, 1.6)
portal(125.3, 5.0, 'grad2.jpg', 'مشروع *التخرج* — جامعة حلوان')
pic(130.4, 3.8, PJ + 'grad1.jpg', 'ذكريات التخرج 🎓', pan=(100, 0))  # tall photo, face at the top (tools/face_pos.py)
kw(134.3, 2.8, '*AI* بيصحح الامتحانات')
zoom(135.2, 1.6, 'push')
icon(139.1, 1.5, '🤔'); zoom(139.1, 1.2)
screen(140.4, 7.3, 3, 75, PHONE, title='اختيار من *متعدد*', tag='MCQ', logo_='logos/figma.svg')
zoom(146.0, 2.0, 'push')
add('counter', 148.0, 3.8, value=17, from_=0, suffix='/20', label='تصحيح أوتوماتيك', side='right')
zoom(151.4, 1.2)
kw(152.8, 3.6, 'سهلة و*منتشرة*')
kw(156.5, 4.6, 'هدفنا: *AI* يصحح *المقالي* ✍️')
# 2:41 Aly's idea: cat & dog (China x2 + USA agree) -> Egypt university -> two doctors, two different marks
s2 = 161.3
add('judge_scene', s2, 187.0 - s2, photosAt=f(164.0 - s2), aiAt=f(161.7 - s2), chinaAt=f(168.6 - s2), usaAt=f(169.8 - s2),
    pointAt=f(172.3 - s2), egyptAt=f(173.8 - s2), uniLabel='جامعة', chips=[{'text': 'نفس الجامعة', 'at': f(177.6 - s2)},
    {'text': 'نفس القسم', 'at': f(178.9 - s2)}, {'text': 'نفس المادة', 'at': f(180.0 - s2)}],
    splitAt=f(180.7 - s2), grade1='7/10', grade1At=f(183.5 - s2), grade2='6/10', grade2At=f(185.2 - s2))
zoom(187.0, 1.0)
steps(187.4, 5.0, ['معقدة أكتر', 'أكبر', 'فنية أكتر', 'تفاصيل أكتر'], 30)
icon(192.6, 1.4, '🤯'); zoom(192.4, 2.4, 'push')
zoom(195.0, 1.4)
kw(196.6, 2.6, 'خلاصة *المشروع*')
screen(199.3, 4.7, 0, 9, [350, 150, 1210, 680], title='مدرسين و*طلاب*', tag='Quizzer', hw=0.5)
screen(204.0, 4.4, 3, 25, PHONE, title='المواد', tag='Quizzer')
screen(208.4, 4.6, 3, 50, PHONE, title='امتحانات و*أسئلة*', tag='Quizzer')
kw(213.3, 3.0, 'مقالي *أو* اختيارات')
green(214.2, 'instagram_1', dur=7.8)  # native side (left) — never mirror/shift these
zoom(216.3, 1.2)
kw(217.6, 2.0, 'و*الطلاب* كمان')
screen(219.7, 3.4, 3, 112, PHONE, title='يختاروا *امتحان*', tag='Quizzer')
screen(223.1, 3.4, 3, 37, PHONE, title='*الدرجات*', tag='Quizzer')
zoom(226.5, 1.2)
kw(227.0, 2.0, 'لو حد *مبتدئ*؟')
logo(229.1, 2.8, 'logos/adobe-xd.svg', 'Adobe XD')
screen(232.0, 4.0, 0, 47.6, [740, 200, 440, 680], title='النتيجة *وقتها*', tag='Adobe XD', logo_='logos/adobe-xd.svg')
icon(236.3, 1.5, '😅')
screen(236.0, 3.7, 0, 53, [740, 200, 440, 680], title='', tag='Adobe XD', logo_='logos/adobe-xd.svg')
screen(239.8, 4.6, 0, 58.2, [600, 110, 720, 860], title='كانت *بتفي بالغرض*', tag='Adobe XD', logo_='logos/adobe-xd.svg')
zoom(244.4, 1.6)
# 4:10 his presentation animation (rec0 0-45 s)
screen(246.4, 9.4, 0, 0.5, [350, 150, 1210, 680], title='*الانيميشن* اللي قدمنا بيه', tag='Graduation 2019', hw=0.55)
icon(253.0, 1.4, '😂', 0.6, 0.22)
zoom(255.8, 1.4)
kw(256.6, 3.3, 'من غير *المانوال*')
zoom(260.0, 3.0, 'push')
logo(264.3, 2.4, 'logos/figma.svg', 'Figma')
kw(266.6, 3.2, 'أشهر برنامج *UI/UX*')
flow(270.0, 2.2, [('logos/claude.svg', 'Claude', 0), ('logos/chatgpt.svg', 'ChatGPT', 14)], arrows=False)
screen(272.2, 3.5, 1, 0.2, [560, 0, 800, 1040], still=True, title='اكتب لـ*Claude* هنا', tag='Claude', logo_='logos/claude.svg',
       marks=[{'x': 580, 'y': 950, 'w': 760, 'h': 50, 'from': 4, 'to': 55, 'label': 'هنا بتكتب'},
              {'x': 700, 'y': 10, 'w': 630, 'h': 190, 'from': 55, 'to': 105, 'label': 'اشرحله برنامجك'}], hw=0.3)
screen(275.7, 4.0, 1, 2.0, [560, 0, 800, 1040], title='الـ*Prompt* اللي طلع', tag='Claude', logo_='logos/claude.svg', hw=0.3)
flow(279.8, 4.8, [('logos/claude.svg', 'Claude', 0), ('logos/figma.svg', 'Figma Make', 100)], packet='Prompt',
     title='عايز *Prompt*')
screen(284.8, 3.9, 2, 45.6, [1180, 0, 740, 320], title='Figma *Make* من هنا', hw=0.42,
       marks=[{'x': 1700, 'y': 42, 'w': 94, 'h': 40, 'from': 20, 'to': 117, 'label': 'Make'}])
screen(288.8, 5.6, 2, 58.0, [560, 240, 840, 420], title='الصق الـ*Prompt* هنا',
       marks=[{'x': 620, 'y': 330, 'w': 690, 'h': 260, 'from': 10, 'to': 168, 'label': 'Ctrl + V'}])
screen(294.5, 6.8, 2, 81.5, [560, 240, 840, 420], title='اختار الموديل و*ابعت*',
       marks=[{'x': 1070, 'y': 528, 'w': 150, 'h': 44, 'from': 4, 'to': 110, 'label': 'الموديل'},
              {'x': 1250, 'y': 528, 'w': 46, 'h': 46, 'from': 110, 'to': 204, 'label': 'إرسال'}])
kw(301.4, 2.2, 'استخدمت *Sonnet*')
# 5:03-5:20 what Figma Make built
screen(303.6, 2.8, 3, 0.5, PHONE, title='النتيجة 🔥', tag='Quizzer')
screen(306.4, 2.8, 3, 25, PHONE, title='Instructor', tag='Quizzer')
screen(309.2, 2.5, 3, 50, PHONE, title='*الامتحانات*', tag='Quizzer')
screen(311.7, 2.4, 3, 37, PHONE, title='*الدرجات*', tag='Quizzer')
screen(314.1, 3.4, 3, 112, PHONE, title='أحلى *بكتير*', tag='Quizzer')
zoom(316.0, 1.4)
screen(317.5, 3.0, 3, 137, PHONE, title='*راضي* بيه', tag='Quizzer')
kw(320.5, 3.0, 'ينفع *ينزل السوق* 🚀')
screen(323.6, 4.4, 4, 2, [0, 150, 800, 800], title='الـ*Credits* خلصت', marks=[{'x': 20, 'y': 790, 'w': 350, 'h': 80, 'from': 20}],
       hw=0.42)
s3 = 328.1
add('credits_drain', s3, 340.3 - s3, from_=30, drainAt=0, emptyAt=f(330.2 - s3),
    options=[{'text': '💸 تدفع فلوس', 'at': f(335.6 - s3)}, {'text': '⏳ تستنى يوم يومين', 'at': f(336.5 - s3)}], side='right')
zoom(331.8, 1.3); zoom(334.3, 1.4)
kw(340.4, 3.6, 'النسخة *الفري* = Prompt واحد')
green(341.0, 'youtube_3', dur=7.8)
icon(344.4, 1.4, '🤔'); zoom(344.4, 1.3)
steps(346.0, 3.6, ['شاشة', 'زرار', 'أي حاجة'], 20)
kw(349.7, 2.4, 'مش محتاج *تدفع* ❌')
screen(352.2, 4.0, 5, 31.6, [300, 20, 800, 520], title='خانة *الكود*',
       marks=[{'x': 474, 'y': 44, 'w': 38, 'h': 36, 'from': 20, 'to': 80, 'label': '+'},
              {'x': 484, 'y': 108, 'w': 112, 'h': 32, 'from': 80, 'to': 120, 'label': 'Files'}])
screen(356.2, 3.3, 5, 41.2, [300, 200, 900, 560], title='اختار *الصفحة*',
       marks=[{'x': 400, 'y': 462, 'w': 230, 'h': 26, 'from': 20, 'to': 99, 'label': 'student.tsx'}])
flow(359.6, 4.0, [('logos/figma.svg', 'الكود', 0), ('logos/chatgpt.svg', 'ChatGPT / Claude', 50)], packet='Code')
steps(363.7, 4.8, ['➕ زود زرار', '↔ انقل زرار', '🎨 غير لون'], 30)
screen(368.6, 4.4, 5, 83, [800, 180, 700, 260], title='اعمله *Simple* أكتر', tag='Claude', logo_='logos/claude.svg')
flow(373.0, 3.2, [('logos/chatgpt.svg', 'ChatGPT', 0), ('logos/figma.svg', 'Figma Make', 40)], packet='New Code')
screen(376.2, 4.8, 6, 8.6, [300, 20, 1000, 620], title='الصق الكود + *Ctrl+S*',
       marks=[{'x': 400, 'y': 462, 'w': 230, 'h': 26, 'from': 0, 'to': 40, 'label': 'نفس الفايل'},
              {'x': 640, 'y': 70, 'w': 640, 'h': 540, 'from': 40, 'to': 144, 'label': 'Ctrl+A  Ctrl+V  Ctrl+S'}])
screen(381.0, 2.6, 6, 13.6, [300, 20, 800, 520], title='*Preview* و Refresh',
       marks=[{'x': 395, 'y': 42, 'w': 110, 'h': 34, 'from': 0, 'to': 45, 'label': 'Preview'},
              {'x': 444, 'y': 94, 'w': 32, 'h': 32, 'from': 45, 'to': 78, 'label': 'Refresh'}])
screen(383.6, 2.5, 6, 21, PHONE, title='الدزاين *الجديد* ✨', tag='Quizzer')
add('counter', 386.1, 3.6, value=0, from_=30, suffix=' Prompts', label='من غير ما تدفع', side='right')
zoom(389.0, 1.2)
kw(390.2, 3.4, 'خلصت؟ *Export* 📦')
screen(393.7, 3.9, 7, 8.6, [1300, 0, 620, 420], title='*Download* code', hw=0.42,
       marks=[{'x': 1820, 'y': 78, 'w': 44, 'h': 36, 'from': 0, 'to': 36, 'label': '⋯'},
              {'x': 1698, 'y': 176, 'w': 154, 'h': 32, 'from': 36, 'to': 117, 'label': 'Download code'}])
screen(397.6, 3.6, 7, 26.8, [380, 100, 1460, 780], title='المشروع *كامل*', hw=0.5)
zoom(401.4, 2.6, 'push')
kw(404.2, 3.0, 'الكود *بتاعك* 100%')
icon(407.3, 1.5, '📁'); zoom(407.4, 1.4)
kw(409.0, 2.9, 'موبايل *أو* ويب')
kw(411.4, 2.2, 'الـ*AI Tool* بتاعتك')
flow(413.6, 5.0, [('logos/claude.svg', 'Claude Code', 12), ('logos/openai.svg', 'Codex', 42),
                  ('logos/githubcopilot.svg', 'Copilot', 69), ('logos/cursor.svg', 'Cursor', 93)], arrows=False)
zoom(415.2, 3.0, 'push')
flow(418.8, 7.6, [('logos/figma.svg', 'Figma Code', 0), ('logos/claude.svg', 'Claude', 45), ('logos/supabase.svg', 'Backend', 195)],
     packet='Code', title='*اربطه* بالباك إند')
flow(426.5, 7.0, [('logos/nextdotjs.svg', 'Next.js', 48), ('logos/angular.svg', 'Angular', 102), ('logos/flutter.svg', 'Flutter', 141)],
     arrows=False, title='يحوّله لأي *Framework*')
kw(434.0, 3.8, 'وتبني *عليه* 🧱')
kw(438.0, 3.0, 'دي طريقة *Figma Make*')
icon(441.3, 1.4, '⚠️'); zoom(441.3, 1.4)
add('bar_chart', 443.4, 5.6, title='الكواليتي', unit='%', side='right',
    items=[{'label': 'Figma Make', 'value': 60}, {'label': 'ديزاينر محترف', 'value': 100}])
zoom(450.5, 1.2)
kw(451.9, 3.2, 'الطريقة *السريعة* ⚡')
kw(455.3, 3.6, 'أسهل من *المانوال*')
logo(459.2, 2.3, 'logos/supabase.svg', 'اربطه بالكود')
green(461.4, 'youtube_2', dur=7.8)
kw(461.6, 4.2, 'نربطه بالـ*Database*؟')
zoom(464.0, 1.4)
kw(466.0, 3.7, 'قولولي في *الكومنتات* 💬')
add('subscribe_press', 470.0, 3.1, platform='youtube', x=0.76, y=0.42, pressAt=f(472.4 - 470.0), bellAt=f(472.7 - 470.0))
# --- outro 473.2-end: nothing ---


def fill(cues, max_gap=2.6):
    """Zoom fillers: no stretch longer than max_gap without a new visual event (graphic start or zoom)."""
    big = [(c['src'], c['src'] + c['dur']) for c in cues if c['t'] in ('egypt_crowd', 'judge_scene', 'portal_world')]
    starts = sorted([c['src'] for c in cues] + [b for a, b in QUIET])
    out, k = [], 0
    for a, b in zip(starts, starts[1:]):
        t = a + max_gap
        while b - t > 0.6:
            st = ['push', 'punch', 'out'][k % 3]
            d = 1.6 if st == 'punch' else 2.4
            if not any(t < y and t + d > x for x, y in big + [tuple(q) for q in QUIET]):
                k += 1
                out.append({'t': 'zoom', 'src': round(t, 2), 'dur': d,
                            'props': {'style': st, 'to': {'punch': 1.2, 'push': 1.12, 'out': 1.18}[st], 'x': 0.38, 'y': 0.38}})
            t += max_gap
    return out


fillers = fill(cues)
cues += fillers
for c in cues:  # 'from' is a python keyword -> from_
    if 'from_' in c['props']:
        c['props']['from'] = c['props'].pop('from_')
cues.sort(key=lambda c: c['src'])
fix = json.load(open(W / 'fix.json', encoding='utf8'))
plan = {'cut': False, 'video': 'input/figma video after edit.mp4', 'pack': 'charcoal', 'quiet': QUIET, 'fix': fix, 'cues': cues}
json.dump(plan, open(W / 'plan.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
for c in cues:
    for a, b in QUIET:
        if c['src'] < b and c['src'] + c['dur'] > a:
            print('!! overlaps quiet', c['t'], c['src'])
print(len(cues), 'cues', len(fillers), 'filler zooms')
