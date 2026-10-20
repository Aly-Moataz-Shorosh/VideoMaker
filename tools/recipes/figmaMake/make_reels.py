"""6 VERTICAL reels (9:16) from Aly's figmaMake edit + his CTA clip (Aly 2026-10-08).
Cues come from the long-video plan (work/plan.json, same source seconds), clipped to each reel's ranges and
re-laid for 9:16, plus reel-specific cues. Footage: crop centered on Aly (cropX 0.40) and lifted (vShift 0.15) so his
face sits at the top and graphics go on his chest (0.38-0.68), captions below. Every reel ends with his vertical
CTA clip (work/cta_9x16.mp4, +8.5 dB) + comment_cta.
Run: python work/scripts/make_reels.py -> work/reel_<n>.json ; build: tools/build_edit.py <proj> --plan work/reel_<n>.json --name reel_<n> --vertical"""
import json, sys
from pathlib import Path
import numpy as np

W = Path(__file__).resolve().parents[1]
P = W.parent
sys.path.insert(0, str(P.parents[1] / 'tools'))
from transcribe import load_audio

PJ = 'projects/2026-10-07 youtube figmaMake/'
MAIN = 'input/figma video after edit.mp4'
long_plan = json.load(open(W / 'plan.json', encoding='utf8'))
BIG = ('egypt_crowd', 'judge_scene', 'portal_world', 'phone_tour')
# ROTO MODE (Aly 2026-10-08, reviewing reel_1: "no black strip; rotoscope me the whole video, motion graphics
# everywhere, make me smaller; the phone screen was hidden and too big"): Aly = cut-out (roto_*.webm, 30 fps)
# standing at the bottom (rotoScale 0.62), GrainBg behind, all recordings BIG in the top area, other graphics
# lifted by gShift, captions on his chest. Face sits at ~(0.5, 0.64).
ROTO = [{'start': 14.4, 'file': PJ + 'roto_14.4.webm'}, {'start': 154.1, 'file': PJ + 'roto_154.1.webm'},
        {'start': 228.0, 'file': PJ + 'roto_228.0.webm'}, {'start': 265.0, 'file': PJ + 'roto_265.0.webm'},
        {'start': 466.3, 'file': PJ + 'roto_466.3.webm'}]
PHONE = [900, 140, 500, 880]  # Quizzer phone frame in rec3/5/6
FACE = {'x': 0.5, 'y': 0.64}  # face position in the 9:16 output (zoom origin)

REELS = {
    1: [[14.62, 75.55]],  # starts in the quiet tail before 'فمثلا' (+3-frame fade) — Aly: 'مثلا' got cut  # edges = measured dips (his edit has almost no pauses)
    2: [[154.35, 196.63], [466.53, 469.85]],  # end before the short 'بس' after 'المشروع'
    3: [[228.12, 244.96], [303.2, 323.22]],
    4: [[265.19, 323.22]],
    5: [[323.22, 391.69]],
    6: [[391.69, 437.8]],  # no clean pause around 401-404 -> keep whole
}

audio = load_audio(str(P / MAIN))
SR, HOP = 16000, 320
rms = np.sqrt(np.convolve(audio ** 2, np.ones(HOP) / HOP, 'same'))


def snap(t, win=0.03):
    """Cut edge -> quietest point within ±win (cuts land in real pauses, never inside a phrase)."""
    i0, i1 = int((t - win) * SR), int((t + win) * SR)
    seg = rms[max(0, i0):i1:80]
    k = int(np.argmin(seg)); nt = max(0, i0) / SR + k * 80 / SR
    db = 20 * np.log10(seg[k] + 1e-9)
    if db > -30:
        print(f'  !! edge {t:.2f} -> {nt:.2f} still loud ({db:.0f} dB)')
    return round(nt, 2)


def tour(at, end):
    """Every Figma Make page from the real recordings, splash first (Aly: all pages + the splash)."""
    rec = lambda n: PJ + f'rec{n}.mp4'
    pages = [(rec(3), 105.0, False, 'Splash'), (rec(3), 1, True, 'Login'), (rec(5), 13, True, 'Create Account'),
             (rec(3), 26, True, 'Instructor'), (rec(3), 51, True, 'المواد والامتحانات'), (rec(3), 63, True, 'تعديل امتحان'),
             (rec(3), 76, True, 'سؤال اختياري'), (rec(3), 89, True, 'سؤال مقالي'), (rec(5), 19, True, 'Student'),
             (rec(3), 126, True, 'مراجعة الإجابات'), (rec(3), 138, True, 'النتيجة'), (rec(6), 18.5, True, 'تصميم تاني')]
    step = (end - at) / len(pages)
    return {'t': 'phone_tour', 'src': at, 'dur': round(end - at, 2), 'props': {
        'title': 'كل صفحات *Figma Make*',
        'pages': [{'src': s, 'start': st, 'still': still, 'label': lab, 'at': int(round(i * step * 30))}
                  for i, (s, st, still, lab) in enumerate(pages)]}}


def extra(n):
    c = []
    if n == 2:  # "want to know more about the project? tell me in the comments" -> graduation photo behind him
        c.append({'t': 'side_picture', 'src': 466.65, 'dur': 3.15, 'props': {
            'src': PJ + 'grad2.jpg', 'caption': 'عايزين تعرفوا أكتر عن المشروع؟ 💬', 'side': 'right', 'fit': 'cover', 'tilt': 3}})
    if n in (3, 4):
        c.append(tour(303.5, 320.9))
    if n == 6:  # the design inside Figma Make before exporting
        c.append({'t': 'screen_ui', 'src': 391.7, 'dur': 2.0, 'props': {
            'src': PJ + 'rec6.mp4', 'start': 18.5, 'still': False, 'crop': [0, 30, 1920, 1010], 'title': 'الديزاين *جوه Figma*',
            'tag': 'Figma Make', 'logo': 'logos/figma.svg', 'marks': [], 'accent': 'gold'}})
    return c


def drop(n, c):
    if c['t'] in ('subscribe_press', 'green_clip'):
        return True
    if n in (3, 4) and c['t'] in ('screen_ui', 'keyword_pop', 'icon_pop') and 303.4 <= c['src'] < 320.8:
        return True  # replaced by the phone tour
    if n == 2 and c['src'] >= 460:
        return True  # replaced by the portal scene
    if n == 6 and c['t'] == 'keyword_pop' and c['src'] < 391.7:
        return True
    return False


def vertical(c):
    """Re-lay a 16:9 cue for 9:16 roto mode."""
    p = c['props']
    if c['t'] == 'portal_world':  # no portals: the phone screenshot behind him was hidden + huge -> real phone card
        c['t'] = 'screen_ui'
        c['props'] = {'src': PJ + 'rec3.mp4', 'start': 1, 'still': True, 'crop': PHONE, 'title': p.get('title', ''),
                      'tag': 'Quizzer', 'logo': 'logos/figma.svg', 'marks': [], 'accent': 'gold', 'split': True}
        return c
    if c['t'] == 'zoom':
        p.update(FACE)
    elif c['t'] == 'icon_pop':
        p.update(x=0.84, y=0.85, size=120)  # lifted by gShift 0.3 -> beside his head
    elif c['t'] == 'screen_ui':
        cw, ch = p['crop'][2], p['crop'][3]
        w = min(0.9 * 1080, 0.27 * 1920 * cw / ch)  # card fits the chest zone
        p.update(width=round(w / 1080, 3), top=0.385)  # card ends <= 0.655, above the captions
    return c


def fill(cues, ranges, max_gap=2.6):
    big = [(c['src'], c['src'] + c['dur']) for c in cues if c['t'] in BIG]
    out, k = [], 0
    for a, b in ranges:
        starts = sorted([a] + [c['src'] for c in cues if a <= c['src'] < b] + [b])
        for s, e in zip(starts, starts[1:]):
            t = s + max_gap
            while e - t > 0.6:
                st = ['push', 'punch', 'out'][k % 3]; d = 1.6 if st == 'punch' else 2.4
                if not any(t < y and t + d > x for x, y in big) and t + d <= b:
                    k += 1
                    out.append({'t': 'zoom', 'src': round(t, 2), 'dur': d, 'props': {
                        'style': st, 'to': {'punch': 1.2, 'push': 1.12, 'out': 1.18}[st], **FACE}})
                t += max_gap
    return out


# Sentences cut by a reel edge: the long-video fix is for the WHOLE sentence -> give the kept part only
# (a whole-sentence fix on a partial sentence put the video's opening words on reel 1, 2026-10-08).
PARTIAL = {
    1: {'S001': 'فمثلا احنا في مصر 120 مليون بني آدم كام مليون منهم هيبقى يعرف يعمل الحوار ده. فالمنافسة بقت عالية جدا. فدلوقتي اللي يفرقك عن اي حد تاني مش انك بتعرف تكتب كود بس. طبعا في حاجات كتير جدا تفرقك ان',
        'S012': 'اكبر بعدد اكبر بسرعة سريعة جدا.'},
    2: {'S028': 'الهدف بتاعنا بقى في الامتحانات احنا كمان نعمل AI يقدر', 'S039': 'صريحة مش هنخش في تفاصيل المشروع',
        'S104': 'ولو'},
    3: {'S047': 'انا وانا في الكلية فتحت',
        'G3': 'بعد ما Figma خلص قدرنا نوصل للـ Quality دي. نقدر نخش من هنا على الـ Instructor او',
        'S068': 'وتصميم ينفع كبداية لابليكيشن ينزل السوق'},
    4: {'S055': 'Figma من اشهر برامج الـ UI UX', 'S068': 'وتصميم ينفع كبداية لابليكيشن ينزل السوق'},
    5: {'S068': 'طيب لو لاحظت ان', 'S087': 'الديزاين بتاعك كامل.'},
    6: {'S087': 'طب خلصت الديزاين بتاعك. تقدر من هنا', 'S098': 'بتاعك وتبتدي تبني عليه زي ما انت عايز.'},
}
tr = json.load(open(W / 'transcript.json', encoding='utf8'))
fix = dict(long_plan['fix'])
fix['A1:S001'] = 'لو عايز نسخة الفيديو على اليوتيوب اكتب في كومنت يوتيوب وهو هيبعتلك اللينك على طول'
for n, ranges in REELS.items():
    print(f'reel {n}')
    ranges = [[snap(a), snap(b)] for a, b in ranges]
    ex = extra(n)
    cues = []
    for c in long_plan['cues'] + ex:
        if c not in ex and drop(n, c):
            continue
        for a, b in ranges:
            s, e = c['src'], c['src'] + c['dur']
            if a <= s < b - 0.4 or (s < a < e and a - s < 0.6):
                c2 = json.loads(json.dumps(c))
                c2['src'] = round(max(s, a), 2)
                c2['dur'] = round(min(e, b) - c2['src'], 2)
                if c2['dur'] >= 0.7:
                    cues.append(vertical(c2))
                break
    cues += fill(cues, ranges)
    cues.sort(key=lambda c: c['src'])
    # Aly 2026-10-08: screen recordings much BIGGER, him smaller, and vary big/small "زي ما متعودين":
    # back-to-back recordings = one group; groups alternate split (big, top half) / card (small). Tour always big.
    groups, last = [], None
    for c in cues:
        if c['t'] == 'screen_ui':
            if last is not None and c['src'] - (last['src'] + last['dur']) < 0.6:
                groups[-1].append(c)
            else:
                groups.append([c])
            last = c
        elif c['t'] == 'phone_tour':
            c['props']['split'] = True
    for g in groups:  # roto mode: every recording big in the top area (he is small at the bottom)
        for c in g:
            c['props']['split'] = True
    spans = [(c['src'], c['src'] + c['dur']) for c in cues if c['props'].get('split')]
    cues = [c for c in cues if not (c['t'] == 'icon_pop' and any(a <= c['src'] < b for a, b in spans))]
    # CTA: his vertical comment-keyword clip, card on top (his face is low in that framing), punches on the keyword
    cues += [{'t': 'comment_cta', 'at': 'A1:S001', 'word': 7, 'dur': 4.82, 'props': {
                'title': 'اكتب في *كومنت*', 'keyword': 'يوتيوب', 'dm': 'ده لينك الفيديو كامل 🎬', 'typeAt': 49, 'sendAt': 80,
                'dmAt': 105, 'top': 0.02}},
             {'t': 'zoom', 'at': 'A1:S001', 'word': 7, 'dur': 1.2, 'props': {'to': 1.12, 'style': 'punch', 'x': 0.5, 'y': 0.5}},
             {'t': 'zoom', 'at': 'A1:S001', 'word': 13, 'dur': 1.2, 'props': {'to': 1.15, 'style': 'punch', 'x': 0.5, 'y': 0.5}}]
    rfix = dict(fix)
    for snt in tr['sentences']:  # partial sentence: never use the whole-sentence fix
        kept = [w for w in snt['words'] if any(a - 0.05 <= w['start'] < b - 0.05 for a, b in ranges)]
        if kept and len(kept) < len(snt['words']):
            rfix.pop(snt['id'], None)
            if snt['id'] in PARTIAL[n]:
                rfix[snt['id']] = PARTIAL[n][snt['id']]
            else:
                print('  !! partial sentence without text:', snt['id'], ' '.join(w['w'] for w in kept))
    plan = {'cut': False, 'video': MAIN, 'pack': 'charcoal', 'cropX': 0.4, 'vShift': 0, 'roto': ROTO, 'rotoScale': 0.62, 'gShift': 0.3, 'capBottom': 0.17, 'keep': ranges, 'fix': rfix,
            'append': [{'video': 'work/cta_9x16.mp4', 'transcript': 'work/cta/transcript.json', 'keep': [[7.06, 12.01]], 'fit': 'cover'}],
            'cues': cues}
    json.dump(plan, open(W / f'reel_{n}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    srcs = sorted(c['src'] for c in cues if 'src' in c)
    holes = [(a, round(b - a, 1)) for a, b in zip(srcs, srcs[1:]) if b - a > 3.0 and not any(x <= a < x + d for x, d in
             [(c['src'], c['dur']) for c in cues if c.get('t') in BIG])]
    print(f'  {ranges} = {sum(b - a for a, b in ranges):.1f}s + CTA 4.95s | {len(cues)} cues | holes>3s: {holes}')
