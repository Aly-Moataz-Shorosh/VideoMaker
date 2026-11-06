# Data for make_open.py: chapters (source seconds, from transcript.json word times), teaser, Claude's coverage + what's missing.
# Yardsticks (checked 2026-11-06, screenshots in research/shots/): see COVER below. Rule (Aly, audio course): an explained topic counts
# fully, true numbers only, and what was left out is written on the card.
PUB = 'projects/filmcourse/'

PARTS = [  # (title, sub, icon, colour)
    ('يعني إيه Film making؟', 'الفيديو لغة: شكل ومحتوى، والفيلم ميكر الشاطر', 'film', '#F5B83D'),
    ('أنواع الصورة والفيديو', 'ثابت ومتحرك، 5 أنواع أنيميشن، المنصة، الأدوات مش عذر', 'layers', '#3BA9F5'),
    ('مراحل صناعة الفيلم', 'Pre-production، Production، Post، Discovery، الفريمات', 'timeline', '#35D07F'),
    ('لغة السينما', 'Visual literacy، المونتاج، السيناريو والتقسيم', 'text', '#FF6B5B'),
    ('الكاميرا', 'أحجام، Framing، 180، Composition، زوايا، فوكس، حركة', 'cam', '#9999FF'),
    ('تحليل مشاهد وختام', 'الصوت في المشهد، السلطة في الكادر، تشويق هيتشكوك', 'play', '#19B5A5'),
]
PARTS_TITLE = 'الكورس *6 أجزاء*'
# (part, source start s, Arabic title, English, icon). Starts = the first word of the sentence that opens the topic.
CH = [
    (0, 0, 'الكورس ده عن إيه', 'Intro', 'flag'),
    (0, 93.3, 'الفيديو لغة: شكل ومحتوى', 'Form & content', 'text'),
    (0, 260.6, 'الفيلم ميكر الشاطر محتاج إيه', 'The filmmaker', 'ques'),
    (0, 316.3, 'أمثلة: إزاي توظّف الأدوات', 'Examples', 'play'),
    (1, 457.4, 'عالم الجرافيكس: ثابت ومتحرك', 'Still & moving', 'layers'),
    (1, 571.3, 'أنواع الأنيميشن الخمسة', '5 animation types', 'slides'),
    (1, 681.0, 'الفيديو حسب المنصة + مثال إعلان', 'Platform', 'app'),
    (1, 767.2, 'الأدوات مش عذر', 'Tools are no excuse', 'green'),
    (2, 857.3, 'أدواتنا: سكريبت ومونتاج وكاميرا', 'The basics', 'cam'),
    (2, 894.7, 'Pre-production و Production و Post', 'Production stages', 'timeline'),
    (2, 1023.2, 'Discovery قبل التحضير', 'Discovery', 'flag'),
    (2, 1075.8, 'التحضير: مثال يوسف شاهين', 'Preparation', 'folder'),
    (2, 1157.5, 'الفريمات والـ Aspect ratio', 'Frames & aspect ratio', 'grid'),
    (3, 1242.8, 'جمال السينما', 'Cinema', 'film'),
    (3, 1366.8, 'السينما لغة مرئية: Visual literacy', 'Visual literacy', 'text'),
    (3, 1501.0, 'المونتاج: القطع ليه معنى', 'Editing', 'razor'),
    (3, 1975.1, 'السيناريو: Sequence و Scene و Shot', 'Script breakdown', 'seq'),
    (3, 2124.1, 'سكريبت إبراهيم الأبيض مع المشهد', 'Script vs scene', 'text'),
    (4, 2366.0, 'الكاميرا: جرامر اللقطة', 'Camera grammar', 'cam'),
    (4, 2393.6, 'أحجام اللقطات Shot sizes', 'Shot sizes', 'grid'),
    (4, 2531.6, 'Framing: POV و Single و Two shot', 'Framing', 'mask'),
    (4, 2606.4, 'قاعدة الـ 180 درجة و Insert', '180° rule', 'pan'),
    (4, 2864.5, 'Composition: قاعدة الأثلاث', 'Composition', 'grid'),
    (4, 3090.7, 'زوايا الكاميرا', 'Camera angles', 'cam'),
    (4, 3225.2, 'الفوكس: Depth of field و Split diopter', 'Focus', 'wheel'),
    (4, 3444.2, 'حركة الكاميرا: Tilt و Pan و Dolly zoom', 'Camera movement', 'pan'),
    (4, 3830.1, 'أدوات الكاميرا', 'Camera gear', 'gear'),
    (5, 4048.8, 'الإضاءة والصوت + تحليل مشاهد', 'Light, sound, breakdowns', 'ear'),
    (5, 4414.6, 'ملخص + الـ Sound effects في المشهد', 'Summary & SFX', 'music'),
    (5, 4555.8, 'السلطة في الكادر: مثال هاري بوتر', 'Power in the frame', 'play'),
    (5, 4682.8, 'التشويق عند هيتشكوك', 'Hitchcock suspense', 'watch'),
    (5, 4858.4, 'الختام: حب السينما', 'Outro', 'flag'),
]
EXTRA = ('تتعلم إيه بعد كده', 'What to learn next', 'flag')  # the ending pages (Claude)

# Cold open: his own words as recorded, cut only on word gaps (times = word starts/ends in transcript.json).
TEASER = [  # (from, to, caption, app)
    (182.0, 185.7, 'السينما لغة: شكل ومحتوى', None),
    (2427.0, 2429.8, 'أحجام اللقطات', 'Shot sizes'),
    (2606.4, 2608.6, 'الـ Framing وقاعدة الـ 180 درجة', None),
    (3398.5, 3403.2, 'عدسة بفوكسين', 'Split diopter'),
    (4588.4, 4591.4, 'تحليل مشهد: السلطة في الكادر', None),
]

# ---- Claude's coverage: each yardstick = an official course / textbook, one row per topic (1 = explained in the session)
COVER = [
    dict(head='كتاب Film Art', en='Bordwell & Thompson, Film Art: An Introduction (McGraw Hill) - chapters', src='Film Art · McGraw Hill',
         url='https://highered.mheducation.com/sites/0072484551/information_center_view0/table_of_contents.html', unit='موضوع',
         has='أقوى جزء: الكاميرا والمونتاج', miss='القصة، الـ Mise-en-scene، الصوت، أنواع الأفلام، التاريخ', items=[
             ('Film production (stages)', 1, '14:54'), ('Distribution and exhibition', 0, 'platform aspect ratio only (19:56)'),
             ('Film form (form vs content)', 1, '2:57'), ('Narrative form', 0, ''), ('Film genres', 0, ''),
             ('Animated film', 1, '9:31 five animation types'), ('Documentary and experimental film', 0, ''),
             ('Mise-en-scene', 0, ''), ('Cinematography', 1, '39:25 - 1:07:28'), ('Editing', 1, '25:01'),
             ('Sound in the cinema', 0, 'SFX shown in examples only (1:14:03); separate audio course'),
             ('Style and film analysis', 1, '1:07:28 - 1:21:00 scene breakdowns'), ('Film history', 0, ''),
         ]),
    dict(head='كورس UCLA للـ Filmmaking', en='UCLA Summer Institute, Digital Filmmaking sample syllabus - lecture topics', src='UCLA Summer · Syllabus',
         url='https://summer.ucla.edu/app/uploads/2021/12/Pre-College-Digital-Filmmaking-Sample-Syllabus-11.5.23.pdf', unit='درس',
         has='الكاميرا، الـ 180، شكل السكريبت، المونتاج', miss='كتابة القصة، الصوت، الإضاءة، الممثلين، الجدول', items=[
             ('Crew positions and set etiquette', 0, 'crew named only'), ('Narrative film and structure', 0, ''),
             ('Basics of camera', 1, '39:25'), ('Basics of sound', 0, 'separate audio course'), ('Lighting (grip: flags, bounce)', 0, 'named only 1:07:36'),
             ('Camera coverage, shot listing, 180 degree rule', 1, '43:26'), ('Screenwriting concepts', 0, ''),
             ('Screenwriting format', 1, '35:24 real script pages'), ('Pitching', 0, ''), ('Blocking and floorplans', 0, ''),
             ('Mise en scene', 0, ''), ('Editing concepts', 1, '25:01'), ('Auditions and directing the actor', 0, ''),
             ('Call sheets and shooting schedules', 0, ''), ('Editing audio and music', 0, ''),
         ]),
    dict(head='مراحل الإنتاج', en='Aberystwyth University, FM17620 Introduction to Film Production - course content', src='Aberystwyth University',
         url='https://www.aber.ac.uk/en/modules/deptfuture/FM17620/AB1/', unit='مرحلة',
         has='من الفكرة للتصوير للمونتاج', miss='التمويل، الميزانية، الجدول، التسليم', items=[
             ('Stages of production', 1, '14:54'), ('Development', 1, '17:03 Discovery'), ('Financing', 0, ''), ('Scheduling', 0, ''),
             ('Budgeting', 0, ''), ('Pre production', 1, '14:54, 17:55'), ('Production', 1, '14:54'), ('Post production', 1, '15:55'), ('Delivery', 0, ''),
         ]),
]
for c in COVER:
    c['n'] = sum(x[1] for x in c['items']); c['of'] = len(c['items']); c['v'] = round(c['n'] / c['of'], 4)
CARDS = [dict(head=c['head'], v=c['v'], n=c['n'], of=c['of'], unit=c['unit'], has=c['has'], miss=c['miss'], src=c['src']) for c in COVER]

OPEN = [  # (scene, seconds, props) - after his intro sting
    ('OCoverage', 9.0, dict(q='رأيي ككلود: الكورس ده بيغطي كام في المية؟', sub='قارنته بكتاب ومنهجين رسميين في الـ Film making.. والموضوع اللي اتشرح بيتحسب كامل',
                            cards=CARDS, foot='هو قال بنفسه: ده *Introduction* مش كورس Film making كامل')),
    ('ORecommend', 6.0, dict(q='ليه أنصحك بالكورس ده؟', rows=[  # every reason = something really in the session
        dict(head='السينما لغة', sub='الشكل والمحتوى، بأمثلة زي الكيف والفيل الأزرق', ico='text', c='#F5B83D'),
        dict(head='جرامر الكاميرا كله', sub='أحجام، Framing، 180، زوايا، فوكس، حركة.. بمشاهد من أفلام', ico='cam', c='#9999FF'),
        dict(head='من الفكرة للشاشة', sub='Discovery، Pre-production، Production، Post', ico='timeline', c='#35D07F'),
        dict(head='تتعلم تحلل مشهد', sub='سكريبت إبراهيم الأبيض، هاري بوتر، تشويق هيتشكوك', ico='play', c='#19B5A5'),
    ])),
]
PARTS_SEC = 6.0
STAMP_SEC = 8.0
STAMP_PAGES = [(0, 1, 2), (3, 4, 5)]

END = [
    ('ONextA', 14.0, dict(
        course=dict(title='كورس المونتاج: Premiere Pro كامل', sub='الخطوة الجاية زي ما قال في الكورس', thumb=PUB + 'pics/premiere_course_thumb.jpg', qr=PUB + 'qr/premiere_course.png'),
        rows=[dict(head='القصة وبناءها', sub='Narrative، الـ 3 فصول، Logline', src='Film Art + UCLA'),
              dict(head='الـ Mise-en-scene', sub='الديكور، الملابس، التمثيل، الإضاءة في الكادر', src='Film Art'),
              dict(head='الصوت في الفيلم', sub='الحوار، المزيكا، المؤثرات.. كورس الصوت على القناة', src='Film Art'),
              dict(head='إدارة الممثل و Blocking', sub='تحرّك الممثل والكاميرا في المشهد', src='UCLA'),
              dict(head='الميزانية والجدول', sub='Budget، Shooting schedule، Call sheet', src='Aberystwyth + UCLA'),
              dict(head='أنواع الأفلام وتاريخ السينما', sub='Genres، الوثائقي، مدارس السينما', src='Film Art')],
        foot='الترشيحات دي من Claude.. من المراجع اللي قارنت بيها الكورس')),
    ('ONextVideos', 14.0, dict(title='فيديوهات من القناة تكمّل بيها', foot='امسح الـ QR بالموبايل.. أو اللينكات في الوصف', vids=[
        dict(title='كورس الصوت للفيديو', why='الصوت نص الفيلم.. من الأساسيات للبرامج', thumb=PUB + 'pics/audio_course_thumb.jpg', qr=PUB + 'qr/audio_course.png', c='#19B5A5'),
        dict(title='تظبيط الإضاءة لفيديوهات اليوتيوب', why='الإضاءة اللي اتذكرت بسرعة في الكورس', thumb=PUB + 'pics/yt_o7QYL5qIY84.jpg', qr=PUB + 'qr/yt_o7QYL5qIY84.png', c='#35D07F'),
        dict(title='هو ايه | SFX & FX', why='المؤثرات الصوتية والبصرية ببساطة', thumb=PUB + 'pics/yt_oi9vWEbEwqI.jpg', qr=PUB + 'qr/yt_oi9vWEbEwqI.png', c='#F5B83D'),
        dict(title='طريقة سهلة وسريعة لتحسين صوت الفيديو', why='صوتك يبقى أنضف في دقايق', thumb=PUB + 'pics/yt_IjVlRDHEBSY.jpg', qr=PUB + 'qr/yt_IjVlRDHEBSY.png', c='#3BA9F5'),
    ])),
]
OUTRO_LEN = 33.3
LINKS = dict(premiere='https://youtu.be/D4fqs2c0DfY', audio='https://youtu.be/2XVRSnTuZJQ', lighting='https://youtu.be/o7QYL5qIY84',
             sfx='https://youtu.be/oi9vWEbEwqI', voice='https://youtu.be/IjVlRDHEBSY')
