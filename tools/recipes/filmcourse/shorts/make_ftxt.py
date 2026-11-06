# Titles + description (one #hashtag line inside it) + pinned comment beside every short, in Aly's format (starts with 'العناوين:',
# then 'الوصف:', then 'الكومنت المثبت:'; no YouTube link line, no posting order — his reels-publisher bulk.py reads these headings).
#   python make_ftxt.py 5 15 20   -> output/shorts/<name>.txt (name = the mp4 next to it)
import sys
from pathlib import Path
import fs_data as SD

PROJ = Path(__file__).resolve().parents[2]
T = {
    5: (['كروما من طرحة أمي 🎬', 'الأدوات مش عذر: أول كروما عملتها كانت طرحة', 'من سلم السرير لاستوديو.. الأدوات بتتغير والغاية لأ'],
        ['أول كروما عملتها، من حوالي 15 سنة: طرحة أمي الخضرا، وراها طرحة سودا، متعلقة على سلم السرير، والكاميرا القديمة جوه علبة جزمة على كرسي.. وبعدين Crop.',
         'وبعدها السطح، والاستوديو، والتابلت.. الأدوات بتساعدك بس، متبقاش مقيد بيها.'],
        ['كروما', 'Green screen']),
    15: (['زاوية الكاميرا بتغير المعنى 🎥', 'ليه الدحيح بنبصله من فوق؟', 'High angle و Low angle و Dutch angle ببساطة'],
         ['لما الكاميرا فوق وبتبص على المقدم من فوق، مش بيحسسك إنه بيعلّمك من فوق.. ولو هو اللي بيبص لنا من فوق واحنا تحت، هنحس بنظرة استعلاء.',
          'Overhead shot بيورينا المكان، Dutch angle (الكادر المايل) بيدي توهان وقلق، و Ground level بيخليك تسأل: مين اللي جاي؟'],
         ['Camera angle', 'زوايا الكاميرا']),
    20: (['نزلت سلمة.. وطلعت سلمة ⬆️', 'السلطة في الكادر: مشهد من Harry Potter', 'إزاي المخرج بينقل السلطة من شخصية لشخصية؟'],
         ['في مشهد من Harry Potter and the Order of the Phoenix (2007): الأطول في الكادر ليه السلطة.. وكل ما واحدة تطلع سلمة، السلطة تتنقل لها.',
          'وفي الآخر: نزلت سلمة وطلعت، Push in بالكاميرا وزوم، الموسيقى تعلى، والتانية تخرج من الكادر.. ده لغة السينما.'],
         ['السلطة في الكادر', 'لغة السينما']),
}
HASH_BASE = ['فيلم_ميكينج', 'صناعة_الأفلام', 'تصوير', 'مونتاج', 'AlyShorosh', 'Shorts']

for n in map(int, sys.argv[1:]):
    titles, desc, tags = T[n]
    spec = SD.SHORTS[n]
    mp4 = sorted((PROJ / 'output/shorts').glob(f'{n:02d}_*.mp4'))
    name = mp4[0].stem if mp4 else f'{n:02d}'
    tg = list(dict.fromkeys('#' + '_'.join(x.split()) for x in tags[:2] + HASH_BASE))
    txt = ['العناوين:', *titles, '', 'الوصف:', *desc, '',
           f'ده جزء من كورس "مقدمة في صناعة الأفلام Film making" الكامل على القناة.. الفصل {spec["chapter"]}.',
           '', ' '.join(tg), '', 'الكومنت المثبت:',
           f'الكورس الكامل على القناة 👆 وده الفصل {spec["chapter"]} منه.. عايز شورت عن إيه بعد كده؟']
    (PROJ / f'output/shorts/{name}.txt').write_text('\n'.join(txt), encoding='utf-8')
    print(name)
