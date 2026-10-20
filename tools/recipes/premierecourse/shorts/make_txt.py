# Title + description + pinned comment beside every short (Aly's job deliverable).  python make_txt.py 6 7 ...
import json, sys
from pathlib import Path
import shorts_data as SD

PROJ = Path(__file__).resolve().parents[2]
CH = {c['n']: c for c in json.load(open(PROJ / 'work/chapters.json', encoding='utf-8'))}
URL = 'https://youtu.be/D4fqs2c0DfY'
T = {  # no: (3 titles, description lines)
    6: (['لوّن الفيديو كله مرة واحدة 🎨', 'Adjustment Layer في Premiere ببساطة', 'إفكت واحد على كل الكليبات؟'],
        ['Adjustment Layer = طبقة فاضية فوق الكليبات: أي إفكت تحطه عليها بيتطبق على كل اللي تحتها.',
         'New Item ← Adjustment Layer ← اسحبها فوق ← حط الإفكت.. وتغيّر مرة واحدة بدل كل كليب.']),
    7: (['لون الفيلم بـ Tint 🎬', 'خلي الفيديو بتاعك إحساسه سقعة وخوف', 'Tint في Premiere: لونين بس'],
        ['Tint بيصبغ الفيديو بلونين: Map Black To للغامق و Map White To للفاتح.', 'حطه على Adjustment Layer عشان الفيديو كله يبقى لون واحد.']),
    8: (['Lens Flare على فيديوك ✨', 'ليه الـ Lens Flare مش بيظهر؟', 'Black Video + Screen = Lens Flare'],
        ['الـ Lens Flare مش بيشتغل على طبقة شفافة: حطه على Black Video واعمل Blend mode = Screen.', 'File ← New ← Black Video.']),
    9: (['ترانزيشن في ثانية: Ctrl + D ⚡', 'Fade in و Fade out من غير Keyframes', 'أسرع ترانزيشن في Premiere'],
        ['Ctrl + D = Default transition على الكليب.', 'أو Right click ← Apply Default Transitions.']),
    10: (['ليه حركتك شكلها روبوت؟ 🤖', 'Linear و Hold و Bezier.. الفرق بالرسم', 'Ease In و Ease Out ببساطة'],
         ['Linear = نفس الخطوة كل فريم · Hold = واقف وفجأة ينط · Bezier = يبدأ بالراحة ويسرع ويهدى.',
          'Ease In = يهدى وهو داخل على الكيفريم · Ease Out = يبدأ بالراحة وهو خارج منه (المصدر: Adobe helpx).',
          'Right click على الكيفريم ← Temporal Interpolation.']),
    11: (['اتحكم في سرعة الحركة بالـ Graph 📈', 'الجراف السري جوه Effect Controls', 'سريع في الأول وهادي في الآخر'],
         ['افتح الجراف من السهم جنب Scale أو Position.', 'ارفع الكيرف في الأول = يطلع بسرعة ويهدى.. أو العكس.']),
    12: (['حرّك أي حاجة بـ Keyframes 🎯', 'غيّرت Scale ومفيش حركة؟ ده السبب', 'أول Animation ليك في Premiere'],
         ['دوس على الساعة (Stopwatch) جنب Scale = أول Keyframe.', 'روح لفريم تاني وغيّر = Keyframe جديد.. والبرنامج يعمل الحركة بينهم.']),
    13: (['Ripple ولا Rolling؟ ✂', 'اقص من غير ما تسيب فراغ', 'الفرق بين Ripple Edit و Rolling Edit'],
         ['Ripple Edit: يقص ويقفل الفراغ لوحده.', 'Rolling Edit: يطوّل كليب ويقصّر اللي جنبه في نفس الوقت.']),
    14: (['خد الحتة اللي عايزها بس: I و O 🎯', 'Insert ولا Overwrite؟', 'أسرع طريقة تحط بيها حتة في التايم لاين'],
         ['I = بداية الحتة · O = نهايتها.', ', = Insert (يزق اللي بعده) · . = Overwrite (يكتب فوقه).']),
    15: (['Slip ولا Slide؟ 🎞', 'غيّر اللي جوه الكليب من غير ما تحركه', 'أدوات Slip و Slide في Premiere'],
         ['Slip: نفس المكان على التايم لاين.. بس جزء تاني من الكليب.', 'Slide: الكليب نفسه بيتحرك ويقصّر اللي جنبه ويطوّل التاني.']),
    16: (['ألوان الأفلام في Premiere 🎨', 'Color workspace في دقيقة', 'Shadow tint و Highlight tint'],
         ['Window ← Workspaces ← Color.', 'Shadow tint و Highlight tint = لون الغامق والفاتح.. و Creative ← Look فيها ألوان جاهزة.']),
    17: (['اكتب على الفيديو في Premiere ✍', 'Shadow و Stroke و Background للكتابة', 'الكتابة في Premiere: القديم والجديد'],
         ['في الكورس (2018): Legacy Title بـ Shadow و Background و Outer Stroke.']),
    18: (['Slideshow في ثواني 📸', 'رص الصور كلها بدوسة واحدة', 'Automate to Sequence'],
         ['علّم على الصور ← Automate to Sequence ← Selection Order.', 'Apply Default Video Transition = ترانزيشن بين كل صورة.']),
    19: (['Transitions صح 🔀', 'مكان الترانزيشن بيفرق!', 'متعتمدش على الترانزيشن الجاهز'],
         ['Effects ← Video Transitions.', 'مكانه: على الأول ولا في النص بيغيّر الشكل.. و Set Selected as Default Transition يخليه هو بتاع Ctrl + D.']),
    20: (['Effects جاهزة بسحبة ✨', 'Presets في Premiere', 'Filmstocks: ألوان أفلام جاهزة'],
         ['Effects ← Presets ← Blurs واسحبه على الكليب.', 'Lumetri Presets ← Filmstocks = ألوان جاهزة.']),
    21: (['الصوت يمين وشمال: Pan 🎧', 'Mute و Solo و Pan في دقيقة', 'خلّي الصوت جاي من ناحية'],
         ['M = Mute (اكتم التراك) · S = Solo (اسمعه لوحده).', 'Audio Clip Mixer ← Pan يمين أو شمال.. حط السماعة وجرّب.']),
    22: (['علّي ووطّي الصوت بـ Keyframes 🔊', 'Keyframes على الصوت', 'Level في Effect Controls'],
         ['Effect Controls ← Volume ← Level: Keyframe واطي وبعدين عالي.', 'Linear = بالتدريج · Hold = فجأة.']),
    23: (['Audio Gain في دوسة 🔈', 'علّي الصوت كله مرة واحدة', 'ليه -42 و +42 = صفر؟'],
         ['Audio Gain: تعلّي (+) أو توطّي (-) الكليب كله.', 'Adjust Gain by بيزوّد على اللي موجود: -42 وبعدين +42 = يرجع صفر.']),
    24: (['رتّب الزحمة بـ Nest 📦', 'كل الكليبات في كليب واحد', 'Nest في Premiere'],
         ['علّم على الكليبات ← Right click ← Nest = Sequence واحدة.', 'إفكت واحد أو Keyframes على الكل مرة واحدة.']),
    25: (['المقص: Razor ✂', 'C = Razor', 'اقص وشيل الحتة في ثانيتين'],
         ['C = Razor (المقص) · V = Selection.', 'اختار الحتة ← Delete.']),
    26: (['المغناطيس: Snap 🧲', 'ليه القص بيتشد لوحده؟', 'S = Snap'],
         ['Snap بيشد القص والكليبات للمكان الصح.', 'S تقفله وتفتحه.']),
    27: (['سرّع وبطّأ بسحبة: Rate Stretch ⏩', 'R = Rate Stretch', 'Speed/Duration بالحساب'],
         ['R = Rate Stretch: اسحب لجوه = أسرع · لبره = أبطأ.', 'أو Right click ← Speed/Duration.. وخد بالك من الـ Frame rate.']),
    28: (['طلّع الفيديو: Export 📤', 'Ctrl + M = Export', 'H.264: جودة حلوة وحجم صغير'],
         ['File ← Export ← Media (Ctrl + M).', 'Format: H.264 · Output Name = مكان الحفظ.']),
    29: (['يعني إيه Resolution؟ 🖼', 'SD و HD و 4K', 'ليه الصورة بتوضح؟'],
         ['نفس المساحة.. بيكسلز أكتر = صورة أوضح.', 'HD = 1920 × 1080.']),
    30: (['يعني إيه Frame rate؟ 🎞', 'الفيديو = صور ورا بعض', 'fps يعني إيه؟'],
         ['الفيديو مجموعة صور ورا بعض.. وعدد الصور في الثانية = fps.', 'فريمات أكتر = حركة أنعم وتقدر تعمل Slow motion.']),
    31: (['يعني إيه Keyframe؟ 🔑', 'البرنامج بيحرك لوحده إزاي؟', 'Keyframe و Graph'],
         ['Keyframe = نقطة بتحفظ المكان في فريم معيّن.. والبرنامج يعمل الحركة بين نقطتين.', 'الجراف بيخلي الحركة واقعية: تبدأ بالراحة وتسرع وتهدى.']),
    32: (['يعني إيه Timeline؟ ⏱', 'خط الزمن في المونتاج', 'فوق الثواني وتحت الـ Layers'],
         ['Timeline = خط الزمن: كذا حاجة بتحصل في نفس الوقت.', 'في Premiere: فوق الثواني وتحت الـ Layers.']),
    33: (['يعني إيه Sequence؟ 📦', 'Sequence = Composition', 'فكرة الـ Function في المونتاج'],
         ['زي الـ Function في البرمجة: تعملها مرة وتستخدمها كتير.', 'Composition في After Effects = Sequence في Premiere.']),
    34: (['تشريح الـ Timeline 🔍', 'العين و Mute و Add Tracks', 'الفيديو فوق والأوديو تحت'],
         ['الفيديو فوق والأوديو تحت.. العين تخفي التراك و M تكتمه.', 'Right click ← Add Tracks = تراكات زيادة.']),
    35: (['سجّل صوتك جوه Premiere 🎙', 'Voice-over من غير برنامج تاني', 'ليه فيه صدى؟'],
         ['زرار المايك (Voice-over record) جنب التراك.', 'الصدى بييجي من السماعة جنب المايك.. استخدم سماعة ودن.']),
    36: (['الـ Paste هيتحط فين؟ 📋', 'V1 و A1 في Premiere', 'Track Targeting ببساطة'],
         ['Ctrl + V بيحط على أول تراك متعلّم.', 'من الـ Source: اسحب أيقونة الفيلم = صورة بس · الموجة = صوت بس.']),
    37: (['Insert من غير ما يقطع: Sync Lock 🔒', 'ليه الـ Insert بيقطع التراكات التانية؟', 'Sync Lock في Premiere'],
         ['اقفل Sync Lock على التراكات اللي مش عايزها تتأثر.', 'Insert بعدها = اللي تحت سليم.']),
    38: (['حرّك الصوت لوحده + Markers 🔗', 'Linked Selection', 'كومنت على التايم لاين'],
         ['اقفل Linked Selection عشان تحرك الصوت لوحده.', 'M = Add Marker.. و Right click ← Clear Markers.']),
    39: (['زُق كل الكليبات مرة واحدة: A ⏭', 'Track Select Forward', 'V و A و Shift + A'],
         ['A = Track Select Forward: يختار كل اللي بعده.', 'Shift + A = كل اللي قبله.']),
    40: (['اعمل Sequence صح 🎬', 'Ctrl + N = Sequence جديدة', 'Sequence بنفس إعدادات الفيديو'],
         ['File ← New ← Sequence (Ctrl + N) واختار 1080 و fps.', 'أو اسحب الفيديو على أيقونة New Item = Sequence بنفس إعداداته.']),
    41: (['دخّل ملفاتك في Premiere 📁', 'Import و Import Folder', 'الـ Project = مكتبة'],
         ['Double click في الـ Project أو Ctrl + I = Import.', 'Import Folder = فولدر كامل.. أو اسحب من الويندوز.']),
    42: (['أول مرة تفتح Premiere 👋', 'New Project و Panels', 'كبّر أي Panel'],
         ['New Project ← الاسم والمكان.', 'كل مربع = Panel.. والأزرق = اللي شغال.']),
    43: (['رتّب شكل البرنامج: Workspaces 🧩', 'Editing و Color', 'اعمل الـ Workspace بتاعك'],
         ['Workspace = ترتيب البانلز: Editing للمونتاج و Color للألوان.', 'Edit Workspaces = اعمل ترتيبك.']),
    44: (['اختصارات الكورس كلها ⌨', 'أهم اختصارات Premiere', 'احفظهم ووفّر وقت'],
         ['Ctrl + N · Ctrl + C/V · I / O · , / . · V · C · A · Ctrl + D · Ctrl + Z · Ctrl + M']),
}
NEWL = {k: f"⚡ وفي Premiere 2026: {v['title']} — {v['how']}" for k, v in SD.NEW.items() if v.get('kind') != 'same'}
ORDER = [p.split() for p in open(PROJ / 'work/shorts/render_list.txt', encoding='utf-8').read().split('"') if p.strip()]
NAME = {int(n): nm for n, nm in ORDER}

for n in map(int, sys.argv[1:]):
    sp = SD.SHORTS[n]
    titles, desc = T[n]
    at = CH[sp['chapter']]['time']
    lines = ['العناوين المقترحة:'] + [f'{i + 1}) {t}' for i, t in enumerate(titles)] + ['', 'الوصف:'] + desc
    if sp.get('new') in NEWL:
        lines.append(NEWL[sp['new']])
    lines += ['', f'ده جزء من كورس Premiere الكامل (مجانا) — الحتة دي في الكورس عند {at}', f'📺 الكورس الكامل: {URL}',
              '💬 اكتب "كورس" في كومنت ويوصلك اللينك على طول', '', '#بريمير #مونتاج #Premiere #كورس_بريمير #علي_شرش', '',
              'الكومنت المثبت:', f'الكورس الكامل (3 ساعات، مجانا): {URL} — الحتة دي عند {at} 🎬 السلسلة دي {n:02d} من 44']
    (PROJ / f'output/shorts/{NAME[n]}.txt').write_text('\n'.join(lines), encoding='utf-8')
    print(NAME[n])
