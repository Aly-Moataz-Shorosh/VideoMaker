# Caption text = the corrected sentence written in full; timing comes from Whisper words by alignment
# (difflib on normalized tokens). Unmatched corrected words (e.g. English terms Whisper dropped) are spread
# over the time between their matched neighbours. Run after retranscribe_keep.py.
import json, re, difflib

TEXT = {
 'K01': 'أصعب بروسيس وأصعب مرحلة في مونتاج الفيديوهات هي إن انت تشيل السكتات أغلب فيديوهاتنا مليانة سكتات',
 'K02': 'دلوقتي برنامج DaVinci Resolve بتاع المونتاج النسخة المجانية فيه tool جديدة بقالها كم أسبوع أو كم شهر رائع جدًا '
        'بتشيل كل السكتات اللي في الفيديو بتاعك بطريقة سريعة جدًا عشان تعمل ده أول حاجة اخش على موقع DaVinci Resolve '
        'ونزّل النسخة المجانية بعد كده افتح البرنامج وخد الفيديو بتاعك حطه في البرنامج',
 'K03': 'بعد كده دوس فوق على كلمة Clip ثم دوس على Audio Operations ومن Audio Operations دوس على Ripple Delete Silence '
        'هيطلع لك popup أو منيو صغيرة كده فيها كذا option أول حاجة هي Threshold وهي إن انت بتتحكم بتقوله إيه هو الصمت '
        'عشان تشيل الصمت لازم تعرف الصمت فانت هتقوله أي حاجة تحت -20 dB مثلًا ده أنا باعتبره صمت',
 'K04': 'فبالتالي أي حاجة فوق -20 dB هيعتبرها كلام وهياخدها معاه بعد كده عندنا Pre و Post Tail ببساطة شديدة انت بتقول '
        'للبرنامج لما تقص بقى الحتة اللي فيها الكلام خد لي قبلها كام فريم وخد لي بعدها كام فريم علشان ما يبقاش الكلام '
        'كأنه مقصوص جدًا أنا ساعات الصراحة بحب أعملها 0 أو 3 أو رقم صغير جدًا لأني عايز الفيديوهات بتاعتي تبقى سريعة '
        'على قد ما أقدر بعد كده عندك Minimum Strip ده عبارة عن انت بتقول له الحد الأدنى من الصمت اللي يتشال لازم يكون 5 فريم',
 'K05': 'بعد كده آخر حاجة Cross fade audio ودي ببساطة شديدة إن هو بيخلي الصوت اللي خارج من المشهد اللي فات والمشهد '
        'اللي جاي يخش في بعض حاجة بسيطة فمبيبقاش فيه صوت القطعة اللي بين كل مشهد ومشهد',
 'K06': 'بس في الأغلب هتلاقي وهي On بيبقى صوتها ألطف',
}


def norm(w):
    w = re.sub(r'[ً-ْ.,!?؟]', '', w.lower())
    return w.translate(str.maketrans('أإآىة', 'اااىه'))


t = json.load(open('transcript.json', encoding='utf8'))
for s in t['sentences']:
    if s['id'] not in TEXT:
        continue
    src = s['words']; new = TEXT[s['id']].split()
    times = [None] * len(new)
    sm = difflib.SequenceMatcher(None, [norm(w['w']) for w in src], [norm(w) for w in new], autojunk=False)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            times[b + k] = (src[a + k]['start'], src[a + k]['end'])
    # fill unmatched runs between known neighbours
    i = 0
    while i < len(new):
        if times[i]:
            i += 1; continue
        j = i
        while j < len(new) and not times[j]:
            j += 1
        t0 = times[i - 1][1] if i else s['start']
        t1 = times[j][0] if j < len(new) else max(t0 + 0.3 * (j - i), s['words'][-1]['end'] if s['words'] else t0)
        if t1 <= t0:
            t1 = t0 + 0.25 * (j - i)
        d = (t1 - t0) / (j - i)
        for k in range(i, j):
            times[k] = (round(t0 + (k - i) * d, 3), round(t0 + (k - i + 1) * d, 3))
        i = j
    s['words'] = [{'w': w, 'start': a, 'end': b, 'p': 1.0} for w, (a, b) in zip(new, times)]
    s['text'] = ' '.join(new)
    miss = sum(1 for k in range(len(new)) if not any(b <= k < b + n for _, b, n in sm.get_matching_blocks()))
    print(s['id'], f'{len(new)} words, {miss} timed by interpolation')
json.dump(t, open('transcript.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
