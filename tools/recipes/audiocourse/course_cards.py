# Content over the screen for the audio course. Times = SOURCE seconds of the session.
# GLOSS: English term -> short Arabic meaning (auto: first time in a chapter, >= 4 s apart). Regex covers Whisper's Arabic spellings.
# CARDS: manual cards per chapter number: (source s, seconds, kind, props). Outside facts only with a checked source (Aly's rule).
GLOSS = [
    (r'^(ال)?(كنتراست|contrast)', 'Contrast', 'الفرق بين الفاتح والغامق'),
    (r'^(ال)?(اوتبوت|الاوتبوت|output)', 'Output', 'الناتج النهائي'),
    (r'^(ال)?(ساسبينس|suspense)', 'Suspense', 'تشويق'),
    (r'^(ال)?(موشن|motion)$', 'Motion picture', 'الصورة المتحركة = الأفلام'),
    (r'^(ديجيتال|الديجيتال|digital)', 'Digital', 'متخزن أرقام على الكمبيوتر'),
    (r'^(ال)?(سنسور|sensor)', 'Sensor', 'الحساس اللي بيلقط الضوء في الكاميرا'),
    (r'^(ال)?(بيكسل|بيكسلز|البيكسلز|pixel)', 'Pixel', 'أصغر نقطة في الصورة'),
    (r'^(ال)?(فريم|الفريمل|فريمز|frame)', 'Frame rate', 'عدد الصور في الثانية'),
    (r'^(ال)?(ريزيليوشن|ريزوليوشن|الريزيليوشن|resolution)', 'Resolution', 'عدد البيكسلز في الصورة'),
    (r'^(ال)?(ويف|ويفز|الويفز|wave)', 'Wave', 'موجة'),
    (r'^(ال)?(موليكيولز|الموليكيولز|molecules)', 'Molecules', 'جزيئات الهوا'),
    (r'^(ال)?(دايفرام|ديافرام|الديافرام|الدايافران|diaphragm)', 'Diaphragm', 'الغشا اللي بيتهز جوه المايك'),
    (r'^(ال)?(هيردز|هيرتز|الهيرتز|hz)', 'Hz', 'عدد الموجات في الثانية'),
    (r'^(ال)?(سايكل|سايكلز|cycle)', 'Cycle', 'موجة كاملة: فوق وتحت'),
    (r'^(كوانتيزيشن|quantization)', 'Quantization', 'تحويل الموجة لأرقام'),
    (r'^(ال)?(سامبل|السامبل|sample)', 'Sample rate', 'عدد اللقطات من الموجة في الثانية'),
    (r'^(ديبس|dips|depth)', 'Bit depth', 'عدد الدرجات المتاحة لكل لقطة'),
    (r'^(ال)?(ديناميك|دايناميك|الديناميك|dynamic)$', 'Dynamic mic', 'مايك قوي وحساسيته قليلة'),
    (r'^(ال)?(كندنسور|كوندنسور|الكندنسور|كوندينسور|كوندنسر|كندنسر|condenser)', 'Condenser mic', 'مايك حساس جدا'),
    (r'^(ال)?(ريبون|ribbon)', 'Ribbon mic', 'مايك بشريحة رفيعة جدا'),
    (r'^(ال)?(بولاريتي|بولارتي|البولاريتي|polar)', 'Polar pattern', 'المايك بيسمع من أنهي اتجاه'),
    (r'^(كاردويد|كارديويد|كاردويت|cardioid)', 'Cardioid', 'بيسمع من قدام وشوية من الجناب'),
    (r'^(ال)?(شوت|شوتجن|الشوتجان|shotgun)', 'Shotgun mic', 'بيسمع من قدام بس ولمسافة أبعد'),
    (r'^(ال)?(امني|اومني|omni)', 'Omni', 'بيسمع من كل الاتجاهات'),
    (r'^(انترفيرنس|interference)', 'Interference tube', 'الأنبوبة المخرّمة في الشوت جن'),
    (r'^(ال)?(بوب|pop)$', 'Pop filter', 'بيقلل هوا الحروف زي "ب"'),
    (r'^(ديد|dead)$', 'Dead cat', 'فرو بيمنع صوت الهوا برا'),
    (r'^(ال)?(امبيانس|الامبيانس|ambience)', 'Ambience', 'الصوت المحيط'),
    (r'^(ديالوج|الديالوج|dialogue)', 'Dialogue', 'الحوار'),
    (r'^(ال)?(سينك|sync)', 'Sync', 'الصوت ماشي مع الصورة بالظبط'),
    (r'^(ال)?(نويز|النويز|noise)', 'Noise', 'الدوشة اللي في الخلفية'),
    (r'^(ميوت|ميوتا|mute)', 'Mute', 'كتم الصوت'),
    (r'^(ال)?(سولو|الصولو|solo)', 'Solo', 'اسمع ده بس'),
    (r'^(ال)?(فوليوم|الفوليوم|volume)', 'Volume', 'علو الصوت'),
    (r'^(ال)?(كيفريم|كيف|keyframe)', 'Keyframe', 'نقطة بتحفظ القيمة في لحظة'),
    (r'^(ال)?(افكت|افكتات|الافكتات|effect)', 'Effect', 'إفكت: تأثير على الصوت'),
    (r'^(ال)?(ورك|work)$', 'Workspace', 'ترتيب شاشات البرنامج'),
    (r'^(ال)?(بانل|بانيل|panel)', 'Panel', 'شاشة جوه البرنامج'),
    (r'^(ال)?(بريسيت|presets?)', 'Preset', 'إعدادات جاهزة'),
    (r'^(ال)?(امبليتيود|amplitude)', 'Amplitude', 'علو الموجة'),
    (r'^(ستيريو|stereo)', 'Stereo', 'صوت لسماعتين: يمين وشمال'),
    (r'^(مونو|mono)$', 'Mono', 'صوت قناة واحدة'),
    (r'^(ال)?(اكسبورت|export)', 'Export', 'تطلّع الملف النهائي'),
    (r'^(ريفيرب|reverb|ايكو|echo)', 'Reverb', 'صدى الصوت في المكان'),
    (r'^(ميكسر|mixer)', 'Mixer', 'شاشة التحكم في كل التراكات'),
]

CARDS = {
    1: [
        (32.5, 7.5, 'Chip', dict(kind='weak', text='50% ولا 90%؟ أرقام بتتقال كتير.. ومالهاش مصدر موثوق (معلومة ضعيفة المصدر)', size=30, y=880)),
    ],
    3: [
        (493.0, 6.5, 'Chip', dict(kind='tip', text='صوت الفيديو مكانش واصل للطلبة في الأول.. واتحلت بعد ثواني', size=30, y=880)),
        (629.0, 6.0, 'Chip', dict(kind='tip', text='هنا اجتماع Zoom اتقفل.. ورجعنا كملنا', size=30, y=880)),
        (686.0, 8.0, 'FilmTag', dict(title='Mickey, Donald, Goofy: The Three Musketeers', year='2004', note='الموسيقى كنوع من الكوميديا')),
        (722.0, 8.0, 'FilmTag', dict(title='The King of Comedy', year='1982', note='الموسيقى بتوصل معنى')),
        (787.0, 8.0, 'FilmTag', dict(title='The Wrestler', year='2008', note='الصوت بيحكي اللي في دماغه')),
        (888.0, 8.0, 'FilmTag', dict(title='Raging Bull', year='1980', note='بنسمع اللي هو سامعه بس')),
    ],
}

# Concept animations (left column; make_course puts the screen in 'side' while they play). Times = the second he says it.
ANIMS = {'PixelNums', 'MolWave', 'MicChain', 'HzAnim', 'SampleAnim', 'BitAnim', 'MicTypes', 'PolarAnim', 'FourSounds', 'SyncAnim',
         'NoisePrint', 'StereoAnim', 'HeadMonitor'}
CARDS.update({
    5: [(1142.0, 10.0, 'PixelNums', {})],                       # 19:02 "كل بيكسل رقم".. 3D array R G B
    6: [(1351.0, 11.0, 'MolWave', {}), (1395.0, 12.0, 'MicChain', {})],  # 22:31 molecules, 23:15 diaphragm -> computer -> speaker
    7: [(1481.0, 12.0, 'HzAnim', {})],                          # 24:41 cycles per second = Hz
    8: [(1613.0, 14.0, 'SampleAnim', {}), (1653.0, 7.0, 'SampleAnim', dict(mode='min'))],  # 26:53 snapshots, 27:33 minimum 2
    9: [(2042.0, 15.0, 'BitAnim', {})],                         # 34:02 0/1 vs many values
    10: [(2368.0, 16.0, 'MicTypes', {})],                       # 39:28 dynamic / condenser / ribbon
    11: [(2572.0, 15.0, 'PolarAnim', {})],                      # 42:52 omni / cardioid / shotgun
    15: [(3630.0, 14.0, 'FourSounds', {})],                     # 60:30 dialogue, ambience, music, sfx
    19: [(4159.0, 10.0, 'SyncAnim', {})],                       # 69:19 sync
    28: [(6163.0, 7.0, 'NoisePrint', {})],                      # 102:43 capture noise print
    30: [(6919.0, 10.0, 'StereoAnim', {})],                     # 115:19 stereo / mono
    31: [(7199.0, 12.0, 'HeadMonitor', {})],                    # 119:59 headphones in podcasts
})
