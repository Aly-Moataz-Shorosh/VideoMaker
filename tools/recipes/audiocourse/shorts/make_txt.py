# Titles + description + tags + pinned comment beside every short (Aly's format: starts with 'العناوين:', no YouTube link line,
# no posting order, Aly 2026-10-21).  python make_txt.py 1 2 ...   -> output/shorts/<name>.txt (name = the mp4 next to it)
import sys
from pathlib import Path
import shorts_data as SD

PROJ = Path(__file__).resolve().parents[2]
T = {  # no: (3 titles, description lines, extra tags)
    26: (['صوتك تليفون.. وفجأة انفجار 💥', 'From the Telephone و GuitarSuite في Premiere', 'إزاي تعمل صوت مكالمة وانفجار من برّه؟'],
        ['صوتك العادي يتحول لمكالمة تليفون من جوه Premiere: Essential Sound ← Dialogue ← Preset ← From the Telephone.',
         'وبعدين انفجار: اقطع بـ C، حط GuitarSuite (Effects ← Special) على الجزء اللي بعد الانفجار، وصوت الانفجار من Essential Sound ← SFX ← Explosion وخليه جاي من برّه.'],
        ['From the Telephone', 'GuitarSuite', 'Explosion', 'Essential Sound']),
    28: (['شيل الدوشة بكليكة واحدة 🔇', 'Noise Reduction في Adobe Audition', 'منشار وعربيات وهوا.. اتشالوا كلهم'],
        ['علّم على حتة فيها دوشة بس ← Effects ← Noise Reduction ← Capture Noise Print.',
         'Ctrl + A ← Noise Reduction (process) ← Apply.. والبرنامج يشيل الدوشة من الصوت كله.'], ['Noise Reduction', 'Capture Noise Print', 'Adobe Audition']),
    7: (['الصوت فعلا موجة 🌊', 'المايك بيسمع إزاي؟ الدايفرام', 'الصوت بيوصل لودنك إزاي؟'],
        ['الصوت = ذرات الهوا بتخبط في بعض وبتعمل موجة لحد ما توصلك، زي الطوبة لما تقع في المية.',
         'المايك فيه Diaphragm بيتهز مع الموجة وحركته بتتسجل.. والسماعة بتعمل نفس الاهتزازات تاني.'], ['Diaphragm', 'Sound wave']),
}
import txt_series
T.update(txt_series.T)
HASH_BASE = ['أسرار الصوت', 'كورس الصوت', 'مونتاج', 'هندسة الصوت', 'AlyShorosh', 'Shorts']

for n in map(int, sys.argv[1:]):
    titles, desc, tags = T[n]
    spec = SD.SHORTS[n]
    mp4 = sorted((PROJ / 'output/shorts').glob(f'{n:02d}_*.mp4'))
    name = mp4[0].stem if mp4 else f'{n:02d}'
    # Aly 2026-10-30 "ليه مش حاتط هاشتاجز": a hashtag-only line INSIDE الوصف (reels-publisher bulk.split_tags takes it out
    # as the reel's hashtags; Instagram/TikTok use the first 5 -> the short's own 2 first). No separate 'الوسوم:' part
    # (not a heading his script knows: it ended up inside the description).
    tg = list(dict.fromkeys('#' + '_'.join(x.split()) for x in tags[:2] + HASH_BASE))
    txt = ['العناوين:', *titles, '', 'الوصف:', *desc, '',
           f'ده جزء من كورس "أسرار الصوت" الكامل على القناة (نظري + عملي، Premiere و Audition).. الفصل {spec["chapter"]}.',
           '', ' '.join(tg), '', 'الكومنت المثبت:',
           f'الكورس الكامل على القناة 👆 وده الفصل {spec["chapter"]} منه.. عايز شورت عن إيه بعد كده؟']
    (PROJ / f'output/shorts/{name}.txt').write_text('\n'.join(txt), encoding='utf-8')
    print(name)
