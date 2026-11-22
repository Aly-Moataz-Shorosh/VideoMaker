"""Garrett Warren @ UTH Festival 2026 (GEM) — reel plan. All times = SOURCE seconds (input/20261120_194608.mp4).
Edges measured on the waveform (crowd floor ~ -31 dB):
  hook 112.77 (quiet -35 after "So") .. 119.10 (after "hire you."),  main 3.74 (quiet before "Hit me") .. 121.43 (applause, faded).
Captions: words from ElevenLabs Scribe (work/el_words.json), fixed by ear + sources:
  "John Landis" -> Jon Landau (Avatar producer, died 2024: NPR, evidence.json 'landau'); "the rook for where" -> the rookery where.
"""
FPS = 30
HOOK = (112.77, 119.10)
MAIN = (3.74, 121.43)
REW_F = 27   # 0.9 s rewind

HEAD = 'إزاي بيتخيّلوا *Avatar* أثناء التصوير من غير مؤثرات؟'
TAG = 'UTH FESTIVAL 2026'
TAG_AR = 'المتحف المصري الكبير'

# (src start, src end, English as said (fixed), Egyptian Arabic)
PHRASES = [
    (3.84, 4.12, 'Hit me.', 'قول سؤالك.'),
    (5.08, 6.02, 'I got a simple question.', 'عندي سؤال بسيط.'),
    (7.10, 8.42, 'Of course, as an amazing stuntman,', 'أكيد، وانت stuntman عظيم كده،'),
    (9.50, 10.84, 'for example, in Avatar,', 'مثلًا في Avatar،'),
    (11.02, 12.70, 'while you were preparing the fight scenes and stuntman,', 'وانت بتحضّر مشاهد الأكشن والستانتس،'),
    (12.74, 15.58, "of course, it's different from how the outcome came in the movie.", 'أكيد ده مختلف عن اللي طلع في الفيلم في الآخر.'),
    (15.98, 18.64, 'How do you visualize it, or how do you visualize the whole scene', 'إزاي بتتخيّله؟ إزاي بتتخيّل المشهد كله'),
    (19.28, 22.46, 'with no effects, no special effects, no VFX, et cetera?', 'من غير أي مؤثرات، لا مؤثرات خاصة ولا VFX ولا غيره؟'),
    (22.86, 26.30, 'So we have already this 3D world', 'بص، إحنا عندنا أصلًا العالم الـ 3D ده'),
    (26.36, 28.70, 'that James Cameron has built in the computer.', 'اللي James Cameron بناه على الكمبيوتر.'),
    (29.14, 32.80, 'We go into these suits, these motion capture suits.', 'بنلبس البدل دي، بدل الـ motion capture.'),
    (33.46, 35.12, "If Jon Landau was alive, he'd kill me.", 'لو Jon Landau كان عايش كان قتلني.'),
    (35.26, 35.98, 'So sorry, Jon.', 'آسف جدًا يا Jon.'),
    (36.28, 37.48, "It's performance capture.", 'اسمها performance capture.'),
    (37.92, 39.28, 'Anyways, we go on stage,', 'المهم، بنطلع على الستيدج،'),
    (40.08, 41.98, '150 cameras see us wherever we go,', '150 كاميرا شايفانا في أي حتة نروحها،'),
    (42.34, 45.42, 'and you see the world on the TV screen.', 'وانت بتشوف العالم ده على شاشة التلفزيون.'),
    (45.74, 47.38, 'So I can literally be sitting here walking,', 'يعني أنا ممكن أبقى هنا بمشي عادي،'),
    (47.72, 50.12, "and on the TV screen you'd see Pandora,", 'وعلى الشاشة تشوف Pandora،'),
    (50.48, 51.54, 'the floating mountains,', 'الجبال الطايرة،'),
    (51.92, 54.62, 'you know, the rookery where the Ikran is.', 'والمكان اللي عايش فيه الـ Ikran.'),
    (56.00, 59.88, 'We can visualize because we have it visualized for us, you know?', 'إحنا بنقدر نتخيّل لأن الصورة جاهزة قدامنا.'),
    (60.62, 62.52, "And look, I've got a great imagination.", 'وبص، أنا خيالي واسع جدًا.'),
    (62.96, 65.10, 'You know, I can definitely concoct anything you want,', 'وأقدر أألّف أي حاجة تطلبها،'),
    (65.48, 68.40, "but when it comes to James Cameron's imagination and Pandora,", 'بس لما نيجي لخيال James Cameron وعالم Pandora،'),
    (69.20, 70.78, 'that trumps me all day long.', 'ده بيكسبني في أي وقت.'),
    (70.84, 72.68, "So that's how I would visualize it.", 'فكده بقدر أتخيّله.'),
    (73.06, 75.24, 'Then what I do when I create a fight scene', 'وبعدين، لما بعمل مشهد أكشن'),
    (75.26, 76.84, "is I do what's called pre-vis.", 'بعمل حاجة اسمها pre-vis.'),
    (77.42, 79.74, 'I get all my friends together, we all get a space,', 'بجمع صحابي كلهم، ونجيب مكان،'),
    (80.00, 80.94, 'and we do a fight scene.', 'ونعمل مشهد الخناقة.'),
    (81.46, 85.54, 'And we come up with four or five versions.', 'ونطلع بـ 4 أو 5 نسخ.'),
    (86.16, 87.64, 'I do the one version I think he wants,', 'نسخة أنا شايف إنه عايزها،'),
    (88.12, 89.44, 'I do the one version I want,', 'ونسخة أنا اللي عايزها،'),
    (90.02, 91.96, 'and I do a bunch of different riffs', 'وشوية تنويعات تانية'),
    (92.36, 95.08, 'of things that might be just jack squat no good.', 'ممكن تطلع ملهاش أي لازمة.'),
    (95.46, 97.60, "You know, because I need to give him stuff that he doesn't like,", 'لأني لازم أديله حاجات مش هتعجبه،'),
    (97.80, 98.22, 'remember?', 'فاكرين؟'),
    (98.94, 99.94, "And so that's how I do it.", 'ودي طريقتي.'),
    (100.04, 103.94, 'I film it with an iPhone or a Canon R5 real fast.', 'بصوّرها بسرعة بـ iPhone أو Canon R5.'),
    (104.42, 107.30, 'I slap it together on my computer on Adobe Premiere,', 'وأركّبها على الكمبيوتر بـ Adobe Premiere،'),
    (108.08, 108.96, 'and I go to him.', 'وأروح له.'),
    (109.36, 112.36, "And trust me, man, it's the greatest thing you'll ever see in your life, you know?", 'وصدقني، دي أعظم حاجة ممكن تشوفها في حياتك.'),
    (112.48, 114.24, 'So go shoot some pre-vis,', 'فروح صوّر pre-vis،'),
    (114.72, 116.48, "show the world, and say, \"Hey, I'm good.\"", 'ورّيها للعالم وقول: أنا شاطر.'),
    (116.48, 118.96, "'Cause if your pre-vis is good, I'll hire you.", 'لأن لو الـ pre-vis بتاعك حلو… هشغّلك.'),
]
HOOK_PHRASES = [
    (112.90, 114.24, 'Go shoot some pre-vis,', 'روح صوّر pre-vis،'),
    (114.72, 116.48, "show the world, and say, \"Hey, I'm good.\"", 'ورّيها للعالم وقول: أنا شاطر.'),
    (116.48, 118.96, "'Cause if your pre-vis is good, I'll hire you.", 'لأن لو الـ pre-vis بتاعك حلو… هشغّلك.'),
]

F = 'projects/uth/film/'
# scenes in the tray (src start, src end, kind, props). Every picture on its word.
CUES = [
    (3.74, 7.05, 'event', {}),
    (7.05, 15.70, 'who', {'pic': F + 'pc_232.jpg'}),
    (15.90, 22.70, 'vs', {'a': F + 'pc_123.jpg', 'al': 'اللي بيتصوّر', 'b': F + 'pc_230.jpg', 'bl': 'اللي بيطلع في الفيلم', 'bAt': 1.2}),
    (22.86, 28.90, 'pic', {'file': F + 'pc_345.jpg', 'label': 'العالم الـ 3D على الكمبيوتر', 'face': F + 'c_cameron.jpg', 'faceAt': 3.6, 'faceLabel': 'James Cameron'}),
    (29.00, 33.20, 'pic', {'file': F + 'pc_10.jpg', 'label': 'بدل الـ motion capture'}),
    (33.30, 36.15, 'person', {'file': F + 'c_landau.jpg', 'name': 'Jon Landau', 'sub': 'منتج أفلام Avatar', 'note': 'اتوفّى سنة 2024'}),
    (36.15, 37.85, 'term', {'file': F + 'pc_180.jpg', 'term': 'Performance capture', 'def': 'الجسم + الوش + التمثيل'}),
    (37.85, 42.20, 'count', {'file': F + 'pc_203.jpg', 'n': 150, 'unit': 'كاميرا', 'at': 2.2}),
    (42.20, 45.60, 'pic', {'file': F + 'pc_5.jpg', 'label': 'العالم على شاشة التلفزيون'}),
    (45.60, 49.50, 'pic', {'file': F + 'pc_338.jpg', 'label': 'بيمشي في الاستوديو…'}),
    (49.50, 50.42, 'pic', {'file': F + 'pc_230.jpg', 'label': 'Pandora', 'cut': True}),
    (50.42, 51.85, 'pic', {'file': F + 'tr_34.jpg', 'label': 'الجبال الطايرة', 'cut': True}),
    (51.85, 55.60, 'pic', {'file': F + 'pc_400.jpg', 'label': 'الـ Ikran', 'cut': True}),
    (55.80, 60.50, 'pic', {'file': F + 'pc_336.jpg', 'label': 'الصورة جاهزة قدامهم'}),
    (60.55, 65.25, 'emo', {'items': [['brain', 'خيال'], ['light_bulb', 'أفكار'], ['sparkles', '']], 'title': 'خياله واسع'}),
    (65.40, 71.00, 'crown', {'face': F + 'c_cameron.jpg', 'pic': F + 'tr_34.jpg', 'name': 'خيال James Cameron', 'at': 3.6}),
    (73.00, 77.30, 'term', {'file': '', 'term': 'Pre-vis', 'full': 'Previsualization', 'def': 'نسخة تجريبية بسيطة من المشهد قبل التصوير الحقيقي', 'at': 2.3}),
    (77.40, 81.25, 'emo', {'items': [['people_hugging', 'صحابه'], ['martial_arts_uniform', 'مشهد خناقة']], 'beats': [0, 2.6]}),
    (81.40, 98.40, 'versions', {'at': 2.25, 'c1': 4.8, 'c2': 6.7, 'riffs': 9.5, 'bad': 12.3, 'dislike': 14.8, 'face': F + 'c_cameron.jpg'}),
    (99.90, 104.25, 'gear', {'beats': [1.1, 2.3]}),
    (104.30, 108.00, 'logo', {'file': 'logos/premiere-pro-official.png', 'label': 'Adobe Premiere', 'emo': 'laptop'}),
    (108.00, 109.30, 'person', {'file': F + 'c_cameron.jpg', 'name': 'James Cameron', 'sub': 'مخرج Avatar'}),
    (109.30, 112.45, 'emo', {'items': [['star-struck', ''], ['glowing_star', ''], ['fireworks', '']], 'title': 'أعظم حاجة هتشوفها'}),
    (112.50, 119.10, 'hire', {'at': 4.0}),
]
HOOK_CUES = [
    (112.77, 119.10, 'hire', {'at': 3.75, 'hook': True}),
]
SFX = 'sfx/'
