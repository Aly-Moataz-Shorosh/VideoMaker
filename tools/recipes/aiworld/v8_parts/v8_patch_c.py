
# note 43: skills explained simply + «you don't write it yourself: tell Claude to turn the finished work into a skill»
k1 = T8("الـ", 781.4); kB = T8("بتتبني", 791.6); kW = T8("وأهميتها", 796.0); kIn = T8("في", 802.2); kEx = T8("ومثال:", 811.2); kOpen = T8("وده", 819.7); kEnd = T8("خليني", 833.2)
spec8(k1 - 0.1, kEnd - 0.15, "الـ skill = كراسة خبرة", k1, outs([
    N(T8("ملف", 783.0), 1400, 430, "ملف SKILL.md: الخطوات + القواعد + أمثلة", src=P6 + "claude_skill_row.jpg", w=440, size=20),
    N(kB, 820, 360, "بتتبني إزاي؟", size=24),
    N(T8("بتكتب", 792.2), 820, 460, "اللي بتعمله كل مرة.. واللي اتعلمته من غلطاتك", size=19),
    N(kW, 820, 600, "ليه مهمة؟ مش بيبدأ من الصفر كل مرة", emo="light_bulb", size=20),
    N(T8("بأسلوبك،", 800.2), 820, 700, "بيشتغل بأسلوبك.. وبيقراها بس لما يحتاجها", size=18)], kIn - 0.15) + outs([
    N(kIn, 1450, 330, "مش لازم تكتبها بنفسك", emo="sparkles", size=24, bg="mustard"),
    TY(kIn + 0.4, 1450, 420, "«حوّل الشغل ده لـ skill واحفظ المعرفة»", w=420, rtl=True, head="بعد ما تخلص شات أو فيديو:", size=19, dur=16),
    E(kIn + 1.6, 1450, 560, 1450, 610),
    N(kIn + 1.8, 1450, 700, "الـ skill اتحفظت ✓", src=P6 + "claude_skill_row.jpg", w=380, size=20, good=True),
    N(kIn + 2.6, 760, 520, "المرة الجاية بيبدأ من هنا", emo="repeat_button", size=22),
    N(T8("ChatGPT", 809.2), 760, 700, "ChatGPT و Codex: Skills بنفس الفكرة", logo=LG("chatgpt.png"), size=18)], kEx - 0.15) + outs([
    N(kEx, 1300, 470, "الـ video maker بتاعنا", src="../../styles/16 journey-series/cover.jpg", w=420, size=22, sub="skill فيها كل اللي عجب علي"),
    N(T8("غلطة", 817.2), 700, 400, "كل غلطة اتسجلت.. متتكررش", emo="no_entry", size=20),
    N(T8("وعشرين", 818.1), 700, 560, "20 ستايل برقم", emo="artist_palette", size=22)], kOpen - 0.15) + [
    N(kOpen, 960, 330, "معيار مفتوح", size=26),
    N(T8("Claude", 822.8), 1400, 520, logo=LG("claude.svg"), label="Claude Code", size=20), N(T8("وCodex،", 823.6), 960, 520, logo=LG("openai-codex.png"), label="Codex", size=20),
    N(T8("Antigravity", 824.4), 520, 520, logo=LG("antigravity.png"), label="Antigravity", size=20),
    N(T8("أمثلة:", 826.3), 960, 760, "skill بتكتب السكريبت بأسلوب صاحب القناة", emo="writing_hand", size=20)])
# notes 46/47: the real experience — no PDF crops: real course thumbs side by side, the styles wall, what the publisher / IG automation DO
import glob as _g
r1 = T8("خليني", 833.2); rBuilt = T8("اللي", 849.8); rVM = T8("video", 855.4); rSk = T8("skill", 861.1); rPub = T8("publisher", 864.2); rIG = T8("أوتوميشن", 869.3)
rOld = T8("والفيديوهات", 873.4); rRes = T8("والنتيجة", 879.2); rLes = T8("والدروس؟", 893.3); rEnd = T8("الموجة.", 906.8) + 1.0
covers = sorted(_g.glob("../../styles/[01]*/cover.jpg"))[:20]
plats = ["youtube.png", "instagram.ico", "facebook.png", "tiktok.png"]
spec8(r1 - 0.1, rLes - 0.1, "تجربة حقيقية بالأرقام", r1, outs([
    N(T8("software", 837.7), 1460, 330, "software tester full-time", emo="technologist", size=22),
    N(T8("وقت", 840.3), 1460, 430, "المونتاج والموشن: مفيش وقت", emo="hourglass_not_done", size=20),
    num(T8("تلات", 841.2), 1460, 650, 3, "سنين من غير فيديو"),
    *[N(T8("كورسات", 844.1) + i * 0.25, 1100 - i * 300, 360, None, src=PI + f, w=270) for i, f in enumerate(["p26_1.png", "p26_2.png", "p26_3.png"])],
    N(T8("كورسات", 844.1) + 0.8, 800, 500, "3 كورسات متسجلة على الرف", size=20),
    N(T8("الإنترو", 848.2), 800, 700, "إنترو «انت بتشتغل إيه؟» جاهز من 2023", src=PI + "p27_1.png", w=360, size=18)], rBuilt - 0.15) + outs([
    N(rBuilt, 960, 250, "اللي اتبنى بـ Claude Code.. على الجهاز", logo=LG("claude.svg"), size=22),
    *[N(rVM + 0.1 * i, 1640 - (i % 5) * 130, 380 + (i // 5) * 80, None, src=f, w=120) for i, f in enumerate(covers)],
    N(rVM + 0.4, 1380, 720, "1. video maker: 20 ستايل برقم", size=20)], rSk - 0.15) + outs([
    N(rSk, 1400, 420, "2. skill السكريبت بنفس الأسلوب", src=P6 + "claude_skill_row.jpg", w=380, size=20),
    N(rPub, 700, 300, "3. publisher: فيديو واحد ← يتجدول على 4 منصات", emo="calendar", size=20),
    *[N(rPub + 0.5 + i * 0.15, 520 + i * 120, 420, logo=LG(f), size=16) for i, f in enumerate(plats)],
    num(T8("تمنية", 865.4), 700, 560, 28, "فيديو في الأسبوع"),
    N(rIG, 1400, 680, "4. أوتوميشن إنستجرام", logo=LG("instagram.ico"), size=20),
    TY(rIG + 0.4, 1400, 770, "كومنت: «كلمة»  ←  رسالة فيها اللينك ✓", w=420, rtl=True, size=18, dur=14)], rOld - 0.15) + outs([
    N(rOld, 1400, 470, "كورس واحد ساعتين", src=CH + "thumb_2XVRSnTuZJQ.jpg" if os.path.exists(CH + "thumb_2XVRSnTuZJQ.jpg") else PI + "p26_3.png", w=420, size=20),
    E(rOld + 1.0, 1170, 470, 1000, 470),
    *[N(T8("واحد", rOld + 2) + i * 0.15, 560 + (i % 3) * 120, 400 + (i // 3) * 220, None, src=PI + f, w=100, ar=9 / 16) for i, f in enumerate(["p07_2.png", "p07_7.png", "p07_9.png", "p07_10.png", "p07_13.png", "p07_14.png"])],
    num(T8("شورت.", rOld + 3), 680, 820, 31, "شورت")], rRes - 0.15) + [
    num(T8("أربعمية", 883.4), 1440, 430, 474, "ألف مشاهدة في آخر شهر"),
    *[N(rRes + 1.0 + i * 0.15, 1290 + i * 105, 580, logo=LG(f), size=16) for i, f in enumerate(plats)],
    N(T8("Genjutsu", 887.0), 640, 470, "ريل واحد: 253K على فيسبوك", src=V8 + "genjutsu_reel.mp4", w=480, loop=10, size=20),
    N(T8("وشورت", 890.0), 1440, 760, "شورت كل يوم + فيديو يوتيوب كل أسبوع", emo="calendar", size=20)])
spec8(rLes - 0.1, rEnd, "الدروس", rLes, [
    N(T8("بتتكرر", 894.8), 1440, 450, "أي حاجة بتتكرر ← تتأتمت", emo="repeat_button", size=24),
    N(T8("السكريبتات،", 898.0), 960, 600, "الـ AI يكتب السكريبت.. والسكريبت هو اللي يشتغل (أوفر)", emo="money_with_wings", size=22),
    N(T8("ego:", 902.8), 480, 450, "مفيش مكان للـ ego", emo="person_bowing", size=24),
    N(T8("فاركب", 906.2), 960, 800, "اركب الموجة", emo="water_wave", size=30, bg="mustard")])
# notes 48/50: step by step SIMPLE — one big picture per step, «خطوة N من 11» + a progress bar, desktop app only (no PowerShell / no code)
sa = T8("تعالى", 910.3)
steps = [T8("خطوة", 920.5 + 0)]
for af in (922.5, 926.6, 931.4, 943.1, 947.4, 954.6, 959.5, 964.1, 976.0, 985.3): steps.append(T8("خطوة", af))
send = T8("بالظبط.", 989.8) + 1.4
def stepbar(i, t, o):
    return [N(t, 960, 232, f"خطوة {i} من 11", size=26, bg="mustard", out=o)] + \
           [N(t + 0.05, 1460 - j * 100, 300, str(j + 1) + (" ✓" if j < i - 1 else ""), size=16, out=o, bg=("mustard" if j == i - 1 else None), dim=(t + 0.3 if j > i - 1 else None)) for j in range(11)]
vis = [
    N(steps[0] + 0.2, 960, 560, "اشترك في Claude (Pro)", logo=LG("claude.svg"), size=30),
    N(steps[1] + 0.2, 960, 560, "نزّل Claude Desktop وافتح تبويب Code", src=P6 + "claude_new_chat.jpg", w=720, ar=1120 / 380, size=24),
    N(steps[2] + 0.2, 960, 560, "حسابات: ElevenLabs · HeyGen · Higgsfield · Suno", emo="key", size=26),
    N(steps[3] + 0.2, 960, 580, "Settings ← Connectors ← Add custom connector ← Connect", src=V8 + "connectors_ui.mp4", w=560, ar=1020 / 794, loop=4.6, size=20),
    N(steps[4] + 0.2, 960, 560, "الـ digital twin: كليب قصير ليك + فيديو موافقة", src=V7 + "real_room_take_6s.mp4", w=620, loop=6, size=22),
    N(steps[5] + 0.2, 960, 560, "look جوه الستوديو نفسه ✓", src=GEN + "avatar_015_C02.mp4", w=620, loop=4, size=22, good=True),
    N(steps[6] + 0.2, 960, 560, "فولدر للمشروع.. وجواه ملف بقواعدك", emo="file_folder", size=30),
    TY(steps[7] + 0.2, 960, 460, "عايز ريل 30 ثانية:\nالنسخة الـ AI بتعرّف بنفسها،\nستايل سينمائي، مزيكا هادية", w=640, head="البرومبت", size=26, dur=35, rtl=True),
    N(steps[8] + 0.2, 960, 560, "Claude بيولّد بالترتيب.. وانت بتتفرج", src=V8 + "claude_session_2x.mp4", w=640, ar=1280 / 1004, loop=10, size=22),
    N(steps[9] + 0.2, 960, 560, "المراجعة: الاسم · الصوت · الحركة ← اتصلحوا ✓", emo="magnifying_glass_tilted_left", size=26),
    N(steps[10] + 0.2, 960, 560, "export.. وتكلفة الريل على الشاشة", emo="film_frames", size=28)]
items = outs([N(sa + 1.0, 960, 420, "ريل 30 ثانية: النسخة الـ AI بتعرّف بنفسها", emo="clapper_board", size=28),
              *[N(T8(w_, 915.3 + i * 0.6), 1500 - i * 220, 620, w_.rstrip("،."), size=20) for i, w_ in enumerate(["وش،", "وصوت،", "وستوديو،", "ولقطة", "وكابشن،", "ومزيكا."])]], steps[0] - 0.15)
for i in range(11):
    o = (steps[i + 1] - 0.15) if i + 1 < 11 else None
    items += stepbar(i + 1, steps[i], o) + [dict(vis[i], **({"out_t": o} if o else {}))]
spec8(sa - 0.1, send, "خطوة بخطوة: ريل 30 ثانية", sa, items)
