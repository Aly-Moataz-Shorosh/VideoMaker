# Shorts series from the audio course "أسرار الصوت" (Aly 2026-10-26: all of them, CTA like the Premiere series; pilot 3 first).
# Key = posting number = course order (Aly review 1, plan: خطة_الشورتس.md). One source = the session recording (1280x720).
# piece: a/b = his sentence (source seconds, fitted on the waveform later); show = 'screen' (his recording, 'crop' or zoom keys 'zoom'),
# an animation name, or 'big:line|sub'; step = step chip text; kw = [(EN, AR, offset)]; key = (keys, AR, offset); labels = [(word, pill)];
# clicks = [(abs src time, x, y)] gold click marks (read from frame_sheet.py, 1280x720 space); bars = his voice as bars (a sound demo plays).
TOTAL = 31
URL = 'https://youtu.be/2XVRSnTuZJQ'
CTA_FILE = None  # Aly records a new CTA for this course (2026-10-26); until then the end card (thumbnail + QR) closes every short
CTA_WORD = 'صوت'
END_D = 4.5

# crops in the 1280x720 recording (card 1016x840 -> height = sw * 0.827)
ESS = dict(sx=1000, sy=50, sw=280)       # Premiere: Essential Sound panel (Dialogue / Preset / Loudness)
ESS_Z = dict(sx=1010, sy=110, sw=270)    # Premiere: Essential Sound preset list close
PR_TL = dict(sx=290, sy=140, sw=700)     # Premiere: source monitor + timeline clips
PR_ALL = dict(sx=140, sy=30, sw=880)       # Premiere: whole screen (the demo plays)
PR_SRC = dict(sx=140, sy=40, sw=500)     # Premiere: source monitor (big green waveform)
EFX = dict(sx=0, sy=150, sw=280)         # Premiere: Effects ← Audio Effects ← Special ← GuitarSuite
AU_WAVE = dict(sx=300, sy=40, sw=760)    # Audition: the waveform editor
AU_SEL = dict(sx=160, sy=40, sw=560)     # Audition: left part of the waveform (his selection of silence)
AU_MENU = dict(sx=80, sy=20, sw=560)     # Audition: Effects menu + Noise Reduction submenu
AU_DLG = dict(sx=380, sy=110, sw=540)    # Audition: Noise Reduction (process) dialog

# Aly review 1 (2026-10-26): numbers = COURSE ORDER (chapter order, not "most impressive first": "عايز الريلز بترتيب الكورس"),
# no screen without motion while he talks (reel 2), Fluent pictures instead of emoji newer than Emoji 12 (the saw was an empty box),
# click boxes the size of the clicked word, zoom follows the mouse through menus, short hook (before -> after first).
AU_TOP = dict(sx=40, sy=0, sw=440)       # Audition: menu bar (Effects) + top of the Effects menu
AU_MID = dict(sx=80, sy=150, sw=440)     # Audition: Effects menu around Noise Reduction / Restoration
AU_SUB = dict(sx=200, sy=170, sw=420)    # Audition: Noise Reduction submenu (Capture / process)
EFF = (115, 22, 44, 14)                  # menu bar "Effects" (x, y, w, h of the word)
NRR = (188, 257, 106, 14)                # "Noise Reduction / Restoration"
CNP = (361, 257, 74, 14)                 # "Capture Noise Print"
NRP = (375, 272, 100, 14)                # "Noise Reduction (process)..."
SHORTS = {
    # review 4 (2026-10-26): "26 و 27 يبقوا ريل واحد" + "27 مفيهاش صوت الانفجار" -> ONE reel for chapter 25: the phone voice, then the
    # explosion; the explosion is HEARD (in the demo, the plain sound he plays, the result from outside). Series = 31 shorts.
    26: dict(no=26, chapter=25, at='1:25:55', title='صوتك *تليفون*.. وفجأة انفجار', pieces=[
        dict(a=5019.9, b=5029.7, raw=True, crop=PR_ALL, bars=True, lab=[(0.2, 'النتيجة', 'telephone_receiver', 2.6), (5.6, 'انفجار', 'collision', 2.0)]),
        dict(a=5010.6, b=5016.6, crop=PR_ALL, labels=[('استخدمتش', 'من غير برامج تانية', 'cross_mark'), ('اسوات', 'أصوات تانية', 'speaker_high_volume')]),
        dict(a=5150.45, b=5156.7, crop=PR_SRC, labels=[('آلو', 'صوتي الأصلي', 'studio_microphone')]),
        dict(a=5193.6, b=5211.7, step='Essential Sound ← Dialogue', crop=ESS, clicks=[(5209.4, 1065, 150)], kw=[('Dialogue', 'صوت بني آدم بيتكلم', 9.0)]),
        dict(a=5217.4, b=5230.05, step='Preset ← From the Telephone', crop=ESS, clicks=[(5217.6, 1150, 162)], labels=[('التليفون', 'From the Telephone', 'telephone_receiver')]),
        dict(a=5145.2, b=5148.7, raw=True, crop=PR_ALL, bars=True, lab=[(0.1, 'صوت الانفجار', 'collision', 2.2)]),
        dict(a=5303.85, b=5309.9, show='BoomScene', anim=dict(mode='plan', boom=0.5)),
        dict(a=5327.25, b=5345.9, step='C = اقطع الصوت عند الكلمة', crop=PR_TL, key=(['C'], 'المقص', 4.0)),
        dict(a=5346.8, b=5370.5, step='Effects ← Special ← GuitarSuite', crop=dict(sx=0, sy=40, sw=700),
             zoom=[(5356.0, EFX), (5363.3, dict(sx=0, sy=90, sw=760)), (5364.9, dict(sx=360, sy=380, sw=440))],
             clicks=[(5363.25, 81, 328, 62, 12), (5364.0, 700, 553, 70, 16)], kw=[('GuitarSuite', 'إفكت بيدوّش الصوت', 10.0)]),
        dict(a=5385.15, b=5404.9, step='حط صوت الانفجار على نفس اللحظة', crop=PR_TL, lab=[(17.2, 'انفجار', 'collision', 1.6)]),
        dict(a=5412.5, b=5441.5, step='Essential Sound ← SFX ← Explosion', crop=ESS, kw=[('SFX', 'مؤثر صوتي', 17.0)]),
        dict(a=5442.0, b=5453.0, raw=True, crop=PR_ALL, bars=True, lab=[(3.6, 'الانفجار من برّه', 'house', 2.6)]),
        dict(a=5453.0, b=5459.5, show='BoomScene', anim=dict(mode='outside')),
    ]),
    28: dict(no=28, chapter=28, at='1:44:04', title='شيل *الدوشة* بكليكة واحدة', pieces=[
        # review 1: "الهوك محتاج يكون اقوى و اسرع" -> the noise itself first, then what it is, then the clean result, then "one click"
        dict(a=6341.45, b=6345.6, raw=True, crop=AU_WAVE, bars=True, lab=[(0.1, 'قبل', 'loudspeaker', 3.6)]),
        dict(a=6348.79, b=6354.1, crop=AU_WAVE, bars=True, labels=[('منشار', 'منشار', 'carpentry_saw'), ('عربيات', 'عربيات', 'automobile'), ('هوا', 'هوا', 'wind_face')]),
        dict(a=6317.05, b=6319.4, raw=True, crop=AU_WAVE, bars=True, lab=[(0.1, 'بعد', 'muted_speaker', 2.1)]),
        dict(a=6323.38, b=6325.68, crop=AU_WAVE, labels=[('نويز', 'مفيش دوشة', 'check_mark_button')]),
        dict(a=6354.45, b=6356.33, crop=AU_WAVE, lab=[(0.2, 'بكليكة واحدة', 'sparkles', 1.7)]),
        dict(a=6143.5, b=6160.6, step='علّم على حتة دوشة بس (مش بتتكلم فيها)', crop=AU_SEL, clicks=[(6160.0, 370, 300)]),
        dict(a=6161.1, b=6177.6, step='Effects ← Capture Noise Print', crop=AU_TOP, zoom=[(6165.2, AU_MID), (6168.6, AU_SUB)],
             clicks=[(6163.7, *EFF), (6167.4, *NRR), (6170.5, *CNP)], kw=[('Noise Print', 'بصمة الدوشة', 11.0)]),
        dict(a=6267.3, b=6280.2, step='Ctrl + A = علّم على الصوت كله', crop=AU_WAVE, key=(['Ctrl', 'A'], 'تحديد الكل', 9.0)),
        dict(a=6280.5, b=6305.3, step='Noise Reduction (process) ← Apply', crop=AU_TOP, zoom=[(6282.4, AU_MID), (6284.6, AU_SUB), (6287.4, AU_DLG)],
             clicks=[(6281.0, *EFF), (6283.2, *NRR), (6286.3, *NRP), (6293.5, 760, 536, 40, 14)]),
        dict(a=6440.7, b=6450.7, show='NoisePrint'),
    ]),
}

_P4 = [
    dict(a=1327.65, b=1332.8, show='Wave3D'),
    dict(a=1334.0, b=1351.8, show='Ripple3D'),
    dict(a=1351.8, b=1359.9, show='Molecules3D'),
    dict(a=1361.0, b=1382.2, show='Molecules3D', anim=dict(bar=True)),
    dict(a=1382.35, b=1395.95, show='big:طب ده إزاي هنلقطه|في الكمبيوتر؟ بالمايك.. وبالسماعة', ico='mic'),
    dict(a=1396.15, b=1418.4, show='Mic3D'),
    dict(a=1418.4, b=1430.9, show='Mic3D'),
    dict(a=1441.35, b=1457.15, show='Speaker3D'),
]

# 07 = the BLENDER version (Aly review 1: "4b احسن بكتير"; not remade, only the series number/frame changes).
# From now on: 3D in Blender, rendered at the whole phone size 1080x1920 (BlenderClip full=True).
def _bc(name, *tags):
    return dict(file=f'projects/audio/b3d/{name}.webm', tags=[dict(text=t, y=y, at=at, c=c) for t, y, at, c in tags])
SHORTS[7] = dict(no=7, chapter=6, at='23:33', title='الصوت فعلا *موجة*', pieces=[
    dict(_P4[0], show='BlenderClip', anim=_bc('b_wave', ('الصوت = موجة', 790, 12, None))),
    dict(_P4[1], show='BlenderClip', anim=_bc('b_ripple', ('الموجة مش حاجة بتمسكها.. دي حركة المية', 790, 50, None))),
    dict(_P4[2], show='BlenderClip', anim=_bc('b_air', ('ذرات الهوا بتخبط في بعض.. لحد ما توصلك', 790, 14, None))),
    dict(_P4[3], show='BlenderClip', anim=_bc('b_bar', ('الحديدة بتخبط الهوا.. والهوا يزق اللي جنبه', 790, 14, None))),
    _P4[4],
    dict(_P4[5], show='BlenderClip', anim=_bc('b_mic1', ('الدايفرام: حاجة هشة بتتهز مع الموجة', 60, 10, 'gold'), ('وحركته بتتسجل على الكمبيوتر', 880, 75, None))),
    dict(_P4[6], show='BlenderClip', anim=_bc('b_mic2', ('الدايفرام: حاجة هشة بتتهز مع الموجة', 60, 10, 'gold'), ('وحركته بتتسجل على الكمبيوتر', 880, 75, None))),
    dict(_P4[7], show='BlenderClip', anim=_bc('b_speaker', ('السماعة بتعمل نفس الاهتزازات في الهوا', 790, 12, None))),
])

# hand-corrected captions per piece (filled after caption_words.py; never words he didn't say)
CAP = {
    26: ['',
        'ما استخدمتش أي إفكت برا.. استخدمت الصوت بتاعي وجبت شوية أصوات تانية وظبطت حاجات',
        'وسجلت الصوت بتاعي العادي خالص اللي هو ده.. آلو، سلام عليكم.. أنا اسمي علي معتز',
        'فهنخش على اللي اسمها Audio وهدوس عليها.. هيجيلي بقى: ده Dialogue ولا موسيقى ولا Sound_Effect ولا صوت محيط؟ فهقوله إن ده Dialogue.. يعني ده صوت بني آدم بيتكلم.. فهدوس على Dialogue وبعد كده هختار من الحاجات الجاهزة',
        'فهدوس على Preset وأقول له From_the_Telephone.. فأنا عايز كأني بكلم في التليفون.. فهدوس وأجرب.. فبقيت كأني بتكلم في التليفون',
        'وده صوت انفجار عادي',
        'عايز بقى إن أنا أخلي الصوت فجأة يدوش.. كأن فيه انفجار حصل.. فالصوت بتاعي يبوظ',
        'نخلي الصوت يتدمر بقى.. نخلي مثلا هنا هقطع، دوست C.. الكلام القطع ده مونتاج خدناه.. فأنا عايز بقى أخلي الباقي ده لحد مثلا هنا.. إن الصوت بقى خلاص الخط فصل.. فأنا كده عايز الكلام ده',
        'عايز الجزء ده يكون صوت الفون.. والجزء ده يكون هنج.. فهعملها إزاي؟ من البانل اللي اسمها Effects.. هخش وأنا بستكشف كده وبدور على إفكت أستخدمه.. أجرب أجرب أجرب لحد ما ألاقي حاجة كويسة.. هو الإفكت GuitarSuite ده اللي أنا عايزه.. فآخده وأحطه كده.. وأجرب بقى.. هو ده اللي احنا سمعناه',
        'ندخل بقى الأصوات اللي عندي.. فهدخل صوت الانفجار نفسه.. فآخد الأوديو بتاعه وأحطه.. وأقرب بقى شوية كده.. وأخلي صوت الانفجار ييجي بالظبط أول ما الصوت بتاعي يتغير.. حس إن أول ما صوت الانفجار جه.. الصوت اتغير',
        'حلو قوي.. الصوت بتاع الانفجار عالي قوي ومش طبيعي.. فأنا عايز أخليه كأنه جاي من بعيد.. كأن الانفجار حصل من بعيد.. فهدوس على الأوديو بتاعي وأخش في البانل تاني.. وأقوله ده إيه؟ Dialogue؟ لأ.. Music؟ لأ.. Sound_Effect؟ أه.. فهدوس على Sound_Effect.. وأختار بقى Explosion.. بس أنا عايزه From_outside.. عايزه يكون صوت جاي من برا.. كأني أنا جوا روم',
        'تعالوا نجرب بقى نسمع كده تاني.. بس نسمع الانفجار لوحده',
        'صوته بقى واطي جدا.. بس برضه عامل فيه صدى صوت.. فكأنه انفجار برا وأنا قافل الشبابيك'],
    28: ['',
        'فيه صوت واحد بيعمل.. اللي هو منشار بيعمل صوت عالي قوي ده.. وفيه صوت عربيات وفيه صوت هوا',
        '',
        'مفيش أي نويز.. أنا مش سامع أي دوشة',
        'فكل ده اتشال بكليكاية واحدة',
        'فهاجي هنا.. فحلو، الحتة دي فاضية.. أنا ما بتكلمش فيها.. فإذن هو ده النويز.. هو ده الإزعاج.. هو ده الوش اللي وراه.. عايز أشيله من الخلفية خالص.. فهعمل إيه؟ علّمت عليها',
        'وهقوم عامل Effect.. وهاجي عند Noise_Reduction.. كل شغلنا بالـ Effect.. وهقوله Capture_Noise_Print.. القط البرينتة دي بتاعت النويز.. دي الباترن بتاعت النويز.. ده شكل النويز اللي بيجي لنا',
        'أنا عايز أشيل بقى النويز ده من الفيديو كله.. فعملت زوم آوت وهعلّم بقى على البتاع كله.. هدوس Ctrl_A.. فكده أنا علمت عليه كله.. أبيض يعني متعلم عليه.. فكده أنا علمت على الفيديو كله',
        'وبعد كده هدوس Effect.. بعد كده Noise_Reduction.. بعد كده Noise_Reduction_Process.. فهنا أنا ممكن نلعب بس احنا كده هنخش في تفاصيل قوي.. فدوس Apply على طول وهو هيظبط لك الحوار.. فكده هو شال صوت الخلفية من الأوديو بتاعي كله.. ولو خدتوا بالكم الويف شكلها اتغير',
        'فاللي بيحصل: أنا بسجل شوية صوت فاضي.. أنا ما بتكلمش فيه.. بس المايك شغال وبيسجل صوت.. فهو بيسجل كده صوت اللي في الخلفية بس'],
    7: ['الصوت عبارة عن إيه؟ كلنا آخد نفسه يا جماعة.. هو عبارة عن Wave',
        'الصوت مش عبارة عن حاجة موجودة في الحقيقة.. قد ما هي تأثير الحاجة دي.. يعني انت لو جبت طوبة ورميتها في مية.. فهي بتعمل موجة.. الموجة دي مش حاجة فيزيكال بتمسكها.. بس هي تأثير إن المية لما بتتحرك بالشكل ده بتعمل موجة',
        'فهو الصوت عبارة عن إن الموليكيولز.. الذرات اللي في الهوا بتخبط في بعض وبتعمل موجة لحد ما توصل لك',
        'فلو أنا مسكت مثلا حديدة وخبطتها بعصاية.. هتعمل الصوت اللي هو "طين" ده.. فاللي هيحصل إنها هتقوم مخبطة الموليكيولز بالطريقة دي.. بدل ما هي كل واحدة جنب التانية عادي.. هيبعدوا عن بعض ويزقوا واحدة تانية.. ويبعدوا عن بعض ويزقوا واحدة تانية.. فده اللي اسمه Wave',
        'طب احنا ده إزاي هنلقطه في الكمبيوتر؟ احنا عايزين نعمل زي اللي عملناه في الفيديو.. عايزين كاميرا وعايزين شاشة.. إزاي بقى نقدر نلقط ده جوا الكمبيوتر؟ فبنعمله عن طريق المايك وعن طريق السماعة',
        'المايك بيبقى فيه حاجة كده اسمها Diaphragm.. الدايفرام ده هو حاجة بتهتز مع الصوت.. حاجة هشة شوية.. مش حاجة مثلا زي حجر.. لو وقع عليه صوت مش هيتحرك.. هي بتتحرك مع الويفز بتاعة الصوت.. فاللي بيحصل إن لما حاجة بتطلع صوت',
        'الموليكيولز تخبط في بعض ويبقى فيه موجة في الهوا.. تخبط في الدايفرام ده وتحركه بطريقة ما.. فلما بيتحرك بتتسجل الحركة بتاعته على الكمبيوتر',
        'لما تيجي انت عايز تسمع الصوت ده.. الكمبيوتر مش سامعه.. الكمبيوتر انت سيفت فيه الويف اللي دخلت له.. فاللي بيحصل إن السماعة بتعمل اهتزازات في الجو.. هتعمل نفس الويف اللي دخلت لها.. بتطلع نفس الويف اللي جات لها.. انت بقى تيجي تسمع الويف دي'],
}

# 07 v2 (Aly 2026-10-26 "حطها في الفيديو و اعمله نسخة"): the same short with the 3D re-rendered at the WHOLE phone size (full=True, under
# the band and captions), the stone falling from far above, a complete mic on a stand + laptop and a complete speaker; the mic-icon card
# while he talks became picture rows (camera -> computer -> screen / mic -> computer -> speaker). 07 v1 stays as it is.
def _bf(name, *tags):
    return dict(_bc(name, *tags), full=True)
SHORTS[107] = dict(no=7, tag='07v2', chapter=6, at='23:33', title='الصوت فعلا *موجة*', pieces=[
    dict(_P4[0], show='BlenderClip', anim=_bf('p_wave', ('الصوت = موجة', 1170, 12, None))),
    dict(_P4[1], show='BlenderClip', anim=_bf('p_ripple', ('الموجة مش حاجة بتمسكها.. دي حركة المية', 1170, 70, None))),
    dict(_P4[2], show='BlenderClip', anim=_bf('p_air', ('ذرات الهوا بتخبط في بعض.. لحد ما توصلك', 1170, 14, None))),
    dict(_P4[3], show='BlenderClip', anim=_bf('p_bar', ('الحديدة بتخبط الهوا.. والهوا يزق اللي جنبه', 1170, 14, None))),
    dict(_P4[4], show='IdeaRows', anim=dict(rows=[
        dict(at=0.3, y=470, pics=['desktop_computer', 'red_question_mark'], tag='إزاي ندخّل الصوت الكمبيوتر؟', c='#8B5CF6'),
        dict(at=4.4, y=770, pics=['video_camera', 'desktop_computer', 'television'], tag='الصورة: كاميرا ← شاشة'),
        dict(at=11.4, y=1070, pics=['studio_microphone', 'desktop_computer', 'speaker_high_volume'], tag='الصوت: مايك ← سماعة')])),
    dict(_P4[5], show='BlenderClip', anim=_bf('p_mic1', ('الدايفرام: حاجة هشة بتتهز مع الموجة', 330, 10, 'gold'), ('وحركته بتتسجل على الكمبيوتر', 1170, 75, None))),
    dict(_P4[6], show='BlenderClip', anim=_bf('p_mic2', ('الدايفرام: حاجة هشة بتتهز مع الموجة', 330, 10, 'gold'), ('وحركته بتتسجل على الكمبيوتر', 1170, 75, None))),
    dict(_P4[7], show='BlenderClip', anim=_bf('p_speaker', ('السماعة بتعمل نفس الاهتزازات في الهوا', 1170, 12, None))),
])
CAP[107] = CAP[7]

# the rest of the series (2026-10-27): series_data.py
import series_data as _S
SHORTS.update(_S.SHORTS); CAP.update(_S.CAP)

# batch 6: 03 + 04 with the films he played (Aly 2026-10-27)
import series_data6 as _S6
SHORTS.update(_S6.SHORTS); CAP.update(_S6.CAP)

# review 2026-10-27: icon rows -> his real screen / material
import series_data7 as _S7
_S7.patch(SHORTS, CAP)

# review 2026-10-27 (2): 19-23 rebuilt with the sound examples heard + his pointing
import series_data8 as _S8
SHORTS.update(_S8.SHORTS); CAP.update(_S8.CAP)

# review 2026-10-27 (3): 08 + 09 = Blender explainers
import series_data9 as _S9
_S9.patch(SHORTS, CAP)

# review 2026-10-29: 01 (silence hook, whole sentences) + 19 (العار example, the no-music video longer)
import series_data10 as _S10
_S10.patch(SHORTS, CAP)
