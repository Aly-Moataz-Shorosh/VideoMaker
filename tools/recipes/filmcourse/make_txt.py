# output/film_making_course_full.txt (titles + description with timestamps + pinned comment) and research/coverage.xlsx
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
PROJ = HERE.parent.parent
sys.path.insert(0, str(HERE))
import film_data as D

C = json.load(open(PROJ / 'work/chapters.json', encoding='utf-8'))
L = ['العناوين:',
     'مقدمة في صناعة الأفلام Film making: إزاي السينما بتتكلم بلغة الصورة',
     'Introduction to Film making: من الفكرة للسيناريو للكاميرا وتحليل المشاهد',
     'اتعلم لغة السينما: أحجام اللقطات، الزوايا، الفوكس، وحركة الكاميرا بأمثلة من أفلام',
     'قبل ما تصوّر أي فيديو: مراحل صناعة الفيلم ولغة الكاميرا ببساطة',
     'كورس Film making للمبتدئين: الفيديو لغة.. اتعلم تتكلمها',
     '',
     'الوصف:',
     'الفيديو مش بس أدوات.. الفيديو لغة ليها شكل ومحتوى. الكورس ده مقدمة في صناعة الأفلام (Introduction to Film making)،',
     'اتشرح من حوالي 5 سنين، وأنا سجلته من جديد النهارده بنفس الملفات.',
     '',
     'هتتعلم فيه:',
     '- يعني إيه Film making، والفيلم ميكر الشاطر محتاج إيه',
     '- أنواع الصورة والفيديو والأنيميشن الخمسة',
     '- مراحل صناعة الفيلم: Discovery، Pre-production، Production، Post-production',
     '- لغة السينما: المونتاج، السيناريو وتقسيمه Sequence و Scene و Shot (مع سكريبت إبراهيم الأبيض)',
     '- جرامر الكاميرا: أحجام اللقطات، Framing، قاعدة الـ 180 درجة، Composition، الزوايا، الفوكس و Split diopter، حركة الكاميرا و Dolly zoom',
     '- تحليل مشاهد: الصوت في المشهد، السلطة في الكادر، والتشويق عند هيتشكوك',
     '',
     '0:00 لقطات من الكورس',
     f"{int(C['teaser'] + C['intro']) // 60}:{int(C['teaser'] + C['intro']) % 60:02d} رأي Claude: الكورس بيغطي كام في المية + الفهرس",
     '']
by = {}
for ch in C['chapters']:
    by.setdefault(ch.get('part'), []).append(ch)
for pi, (title, *_rest) in enumerate(D.PARTS):
    L.append(f'الجزء {pi + 1}: {title}')
    L += [f"{c['time']} {c['ar']}" for c in by[pi + 1]]
    L.append('')
last = C['chapters'][-1]
L += ['ترشيحات', f"{last['time']} {last['ar']}", '']
L += ['رأي Claude (قارنت الكورس بكتاب ومنهجين رسميين، والموضوع اللي اتشرح بيتحسب كامل):']
for c in D.COVER:
    L.append(f"- {c['head']}: {round(c['v'] * 100)}% ({c['n']} من {c['of']}) | ناقص: {c['miss']} | المصدر: {c['en']} {c['url']}")
L += ['الكورس نفسه بيقول إنه Introduction مش كورس Film making كامل.. وأقوى جزء فيه الكاميرا والمونتاج.', '',
      'تذاكر إيه بعد كده (ترشيحات Claude من نفس المراجع):']
nxt = [p for k, _, p in D.END if k == 'ONextA'][0]
L += [f"- {r['head']}: {r['sub']} ({r['src']})" for r in nxt['rows']]
L += ['', 'فيديوهات تكمّل بيها:',
      f"كورس Premiere Pro الكامل (المونتاج): {D.LINKS['premiere']}",
      f"كورس الصوت للفيديو: {D.LINKS['audio']}",
      f"تظبيط الإضاءة لفيديوهات اليوتيوب: {D.LINKS['lighting']}",
      f"هو ايه | SFX & FX: {D.LINKS['sfx']}",
      f"طريقة سهلة وسريعة لتحسين صوت الفيديو: {D.LINKS['voice']}",
      '',
      'مقاطع الأفلام والفيديوهات اللي في الكورس لأصحابها، ومعروضة للشرح والتحليل بس.',
      '',
      '#فيلم_ميكينج #صناعة_الأفلام #لغة_السينما #Film_making #Cinematography #تصوير #مونتاج #Aly_Shorosh',
      '',
      'الكومنت المثبت:',
      'الكورس متقسم 6 أجزاء والتايم ستامبس في الوصف.. ابدأ من اللي محتاجه. وقولي في الكومنتات: أنهي مشهد في فيلم مصري شايف إن لغة الكاميرا فيه عبقرية؟',
      '']
out = PROJ / 'output/film_making_course_full.txt'
out.write_text('\n'.join(L), encoding='utf-8')
print(out)

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
wb = Workbook(); ws = wb.active; ws.title = 'Coverage'
ws.append(['Yardstick', 'Topic', 'Covered', 'Where in the course (source min:sec)', 'Source'])
for c in ws[1]: c.font = Font(bold=True)
for c in D.COVER:
    ws.append([f"{c['en']}: {c['n']}/{c['of']} = {round(c['v'] * 100)}%", '', '', '', c['url']]); ws.cell(ws.max_row, 1).font = Font(bold=True)
    for name, ok, where in c['items']:
        ws.append(['', name, 'yes' if ok else 'no', where, ''])
        ws.cell(ws.max_row, 3).fill = PatternFill('solid', fgColor='C8F0D0' if ok else 'F8D0C8')
for col, w in zip('ABCDE', (60, 50, 10, 46, 90)): ws.column_dimensions[col].width = w
wb.save(PROJ / 'output/تغطية_كورس_فيلم_ميكينج.xlsx')
