# Titles + description + tags + pinned comment beside every short (Aly's format: starts with 'العناوين:', no YouTube link line,
# no posting order).  python make_txt.py 1 2 ...   -> output/shorts/<name>.txt (name = the mp4 next to it)
import sys
from pathlib import Path
import shorts_data as SD

PROJ = Path(__file__).resolve().parents[2]
T = {  # no: (3 titles, description lines, extra tags)
    1: (['صوتك يبقى تليفون في ثانية 📞', 'From the Telephone في Premiere', 'إزاي تعمل صوت مكالمة تليفون؟'],
        ['صوتك العادي يتحول لصوت مكالمة تليفون من جوه Premiere، من غير أي برنامج تاني.',
         'Essential Sound ← Dialogue ← Preset ← From the Telephone.. وجرّب Podcast و In a Large Room.'], ['From the Telephone', 'Essential Sound']),
    2: (['انفجار.. وصوتك يتغير معاه 💥', 'صوت مكتوم بعد الانفجار في Premiere', 'GuitarSuite و Explosion في Premiere'],
        ['أول ما الانفجار يحصل الصوت يدوش ويتكتم: اقطع بـ C عند الكلمة، وحط GuitarSuite (Effects ← Special).',
         'صوت الانفجار نفسه: Essential Sound ← SFX ← Explosion.. وخليه جاي من برا.'], ['GuitarSuite', 'SFX', 'Explosion']),
    3: (['شيل الدوشة بكليكة واحدة 🔇', 'Noise Reduction في Adobe Audition', 'منشار وعربيات وهوا.. اتشالوا كلهم'],
        ['علّم على حتة فيها دوشة بس ← Effects ← Noise Reduction ← Capture Noise Print.',
         'Ctrl + A ← Noise Reduction (process) ← Apply.. والبرنامج يشيل الدوشة من الصوت كله.'], ['Noise Reduction', 'Capture Noise Print', 'Adobe Audition']),
    4: (['الصوت فعلا موجة 🌊', 'المايك بيسمع إزاي؟ الدايفرام', 'الصوت بيوصل لودنك إزاي؟'],
        ['الصوت = ذرات الهوا بتخبط في بعض وبتعمل موجة لحد ما توصلك، زي الطوبة لما تقع في المية.',
         'المايك فيه Diaphragm بيتهز مع الموجة وحركته بتتسجل.. والسماعة بتعمل نفس الاهتزازات تاني.'], ['Diaphragm', 'Sound wave']),
}
BASE_TAGS = ['كورس الصوت', 'الصوت للفيديو', 'أسرار الصوت', 'مونتاج', 'Aly Shorosh']

for n in map(int, sys.argv[1:]):
    titles, desc, tags = T[n]
    spec = SD.SHORTS[n]
    mp4 = sorted((PROJ / 'output/shorts').glob(f'{n:02d}_*.mp4'))
    name = mp4[0].stem if mp4 else f'{n:02d}'
    txt = ['العناوين:', *titles, '', 'الوصف:', *desc, '',
           f'ده جزء من كورس "أسرار الصوت" الكامل على القناة (نظري + عملي، Premiere و Audition).. الفصل {spec["chapter"]}.',
           f'الكورس الكامل: {SD.URL}', '', 'الوسوم:', ', '.join(tags + BASE_TAGS), '', 'كومنت مثبت:',
           f'الكورس الكامل في الوصف 👆 وده الفصل {spec["chapter"]} منه.. عايز شورت عن إيه بعد كده؟']
    (PROJ / f'output/shorts/{name}.txt').write_text('\n'.join(txt), encoding='utf-8')
    print(name)
