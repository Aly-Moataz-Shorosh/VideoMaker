"""Titles + description + pinned comment beside every short, in Aly's notepad format (2026-10-21):
العناوين (3, the strongest first: a question or a sentence with !, 15-60 letters) / الوصف (1-2 lines + link) / hashtags /
الكومنت المثبت / ترتيب النشر: N من TOTAL. Written to output/ and output/v2/.  Run: python work/scripts/write_meta.py"""
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / 'output'
URL = 'https://youtu.be/Uc47QvWaocs'
TAGS = '#جرافيك_تابلت #GraphicTablet #رسم_ديجيتال #علي_شرش'
ORDER = [6, 3, 5, 2, 7]  # posting order = the order Aly picked them ("6+3+5+2+7")
META = {
    6: (['قبل ما تشتري جرافيك تابلت شوف ده!', 'إزاي تختار أول جرافيك تابلت ليك؟', '9 حاجات تفرق في اختيار التابلت!'],
        'اعرف محتاجه ليه، وشوف الحاجات اللي بتفرق، واختار الأنسب من المتاح قدامك.'),
    3: (['إزاي تكتب بقلم على الكمبيوتر؟', 'تابلت بشاشة ولا من غير شاشة؟', 'الشاشة كلها جوه المستطيل ده!'],
        'نوعين الجرافيك تابلت: بشاشة بترسم عليها على طول، ومن غير شاشة أرخص وبتاخد على إحساسه بسرعة.'),
    5: (['اكتب المعادلات بإيدك وتتحول لوحدها!', 'إزاي تكتب الماث على الكمبيوتر بالقلم؟', 'ده اللي يخلّيك تحب الماث!'],
        'بالجرافيك تابلت تكتب المعادلة بإيدك في Word وتتحول لمعادلة مكتوبة، من غير كود ولا مواقع.'),
    2: (['إزاي كنت بذاكر أيام الثانوية العامة؟', 'حوّلت قصة الإنجليزي لخريطة!', 'طريقتي في المذاكرة على السبورة!'],
        'كنت بذاكر على سبورة كبيرة وبلخّص بالرسم، وكنت عايز أعمل كده على الكمبيوتر… فكان الحل القلم.'),
    7: (['أول مرة يمسك جرافيك تابلت!', 'اشتريت الجرافيك تابلت بتاعي منين؟', 'فتحت علبة تابلت Huion HS610!'],
        'من الشراء لفتح العلبة لأول رسمة على تابلت Huion HS610 (مواصفاته: https://www.huion.com/pen_tablet/HS/HS610.html).'),
}
PIN = f'الفيديو الكامل عن أهمية الجرافيك تابلت: {URL}\nأو امسح الـ QR اللي في آخر الفيديو'

for i, n in enumerate(ORDER):
    titles, desc = META[n]
    for t in titles[:1]:  # the strongest title: a question or with !, 15-60 letters
        assert 15 <= len(t) <= 60 and ('؟' in t or '!' in t), (n, t, len(t))
    # Aly's posting script finds the parts by these EXACT header words: العناوين: / الوصف: / الكومنت المثبت: / ترتيب النشر:
    txt = 'العناوين:\n' + '\n'.join(f'{k + 1}. {t}' for k, t in enumerate(titles))
    txt += f'\n\nالوصف:\n{desc}\n{URL}\n\n{TAGS}\n\nالكومنت المثبت:\n{PIN}\n\nترتيب النشر: {i + 1} من {len(ORDER)}\n'
    for d in (OUT, OUT / 'v2'):
        d.mkdir(exist_ok=True)
        (d / f'short_{n}.txt').write_text(txt, encoding='utf-8', newline='\n')
print('ok')
