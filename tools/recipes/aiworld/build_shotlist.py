"""timeline_v1.json -> shotlist_v1.csv + shotlist_v1.json (stage 4 of RUN_v9).
Shots <= 6 s; the WORLD changes at least every 20 s (rule: same place <= 25 s); every shot has 2-4 visual
events inside it (event every 1-2 s, listed in `events`). Types (docs/34): A real+lipsync, B generated Aly,
C Higgsfield B-roll, D 3D (Blender), E motion graphics (Remotion), F screen recording.
Cost = proposed bundle (cost_plan_v1.md): C 5s Kling 4.0 1080p = 16.25 (10 s = 32.5), flex C = Seedance 2.5 720p
5s = 35, D->look = Kling Omni Edit 5 s = 10, B = HeyGen (rate unknown: '?/s', measured by the 10 s test)."""
import csv, json, math, sys
from pathlib import Path

# usage: build_shotlist.py [version]  -> reads timeline_v<version>.json, writes shotlist_v<version>.*  (default 1)
# v2 = real voice timing (build_timeline_v2.py); B cost = measured HeyGen Avatar 6 Turbo 1080p ≈ 0.33 credit/s
V = sys.argv[1] if len(sys.argv) > 1 else "1"
W = Path(__file__).resolve().parent.parent
tl = json.loads((W / f"timeline_v{V}.json").read_text(encoding="utf-8"))

# per chapter: worlds (cycled every <=20 s), style, beats (type, what we see), transition INTO the chapter
P = {
 "C00": (["الأوضة بتتبني من نقط حوالين علي", "فراغ أسود + FREEZE"], "live action + HUD",
         [("B", "علي الـ AI بيتكلم، الكاميرا orbit 360"), ("D", "النقط بتتجمع أوضة وتتفكك"), ("E", "كارت «AI × بإشراف علي» + عدّاد 3 سنين → 28/أسبوع")], "fade من أسود + glitch"),
 "C01": (["قمرة طيارة حربية", "الطيارة exploded view في الهوا"], "cinematic 3D + HUD",
         [("C", "dolly من بره القمرة لجوه، علي قاعد"), ("E", "HUD بيعرض الـ 6 عيلات واحدة واحدة"), ("D", "الطيارة بتتفكك 6 قطع، كل قطعة عليها اسم عيلة")], "whip pan"),
 "C02": (["معمل high-tech", "noise بيتحول لصورة"], "cinematic 3D + 2D cartoon",
         [("B", "علي في المعمل رافع قطعة «التوليد»"), ("E", "3 كروت: موديل ≠ أداة ≠ workflow"), ("E", "دوشة → صورة خطوة بخطوة (diffusion)")], "zoom-through من عين علي"),
 "C02a": (["جاليري صور بتطير"], "2D cartoon + HUD",
          [("C", "صور بتتولد وتطير حواليه"), ("E", "before/after: inpaint / outpaint / remove bg / upscale"), ("E", "نفس الشخصية في 4 صور (consistency)")], "portal"),
 "C02b": (["قاهرة 1897 بالألوان", "شاشة start/end frame"], "live action cinematic",
          [("C", "علي ماشي في قاهرة 1897 (steadicam)"), ("E", "start frame → end frame بيتملا"), ("C", "نفس الحركة بستايل تاني (video-to-video)")], "shatter زي الإزاز"),
 "C02c": (["وشه wireframe", "split قبل/بعد"], "HUD + live action",
          [("D", "وش علي بيتفكك mesh ويتبني"), ("E", "split: صورة → حركة over / lipsync / twin"), ("B", "علي الـ AI بيتكلم بلغة تانية (dubbing)")], "morph على حركة إيده"),
 "C02d": (["waveform 3D بيلف حواليه"], "cinematic 3D",
          [("D", "waveform 3D بيلف ويتحول لكلمات"), ("E", "كروت: TTS / clone / STS / design / SFX / stems"), ("B", "علي بيتكلم والموجة طالعة من بقه")], "الأرض بتتقلب"),
 "C02e": (["نوتات بتطير وتتجمع"], "2D cartoon",
          [("E", "نوتات بتتجمع جملة مزيكا"), ("F", "Suno: الكورس بيتحول كورال (سكرين)")], "wipe بنوتة مزيكا"),
 "C02f": (["hologram كوبري قصر النيل", "Blender رمادي ↔ النتيجة"], "cinematic 3D",
          [("D", "الكوبري بيتبني قطعة قطعة والشمس بتغرب"), ("D", "blockout رمادي"), ("C", "نفس اللقطة بعد التوليد (before/after wipe)")], "particles بتتبني مكان"),
 "C02g": (["كلمات بتتقطع لحروف"], "HUD",
          [("E", "كل كلمة عليها timestamp بالمللي ثانية (Whisper)"), ("E", "OCR بيقرا لافتة + وصف صورة")], "glitch scan"),
 "C29": (["متصفح عملاق (HeyGen)", "متصفح (ElevenLabs)", "متصفح (Higgsfield)", "متصفح (Suno)", "قاعة تحكم (Claude/Codex)", "خريطة العالم (الصيني)", "كانفاس nodes (ComfyUI)", "رف أدوات مجانية"],
         "screen + HUD", [("F", "سكرين الموقع بيكبر وعلي جنبه"), ("E", "كارت المعلومة + المصدر"), ("B", "علي الـ AI جوه الموقع"), ("F", "flex shot من الأداة نفسها")], "الشاشة بتكبر وبندخل فيها"),
 "C03": (["قاعة تحكم، كود بينزل زي المطر"], "toy 3D (شخصيات أصلية)",
         [("C", "لعب الأدوات على مكتب بتشتغل مع بعض"), ("E", "كود بيتكتب → فيديو بيطلع جنبه"), ("B", "علي في قاعة التحكم، FREEZE على سطر كود")], "FREEZE bullet-time"),
 "C04": (["لوحة After Effects عملاقة"], "HUD",
         [("F", "سكريبت قص الصمت شغال"), ("E", "اللوحة بتبني نفسها")], "slide بالتايملاين"),
 "C05": (["أسلاك نور بين قطع الطيارة"], "cinematic 3D",
         [("D", "سلك MCP بيوصل لوجو ويولّعه"), ("E", "Claude في النص و4 أدوات حواليه"), ("C", "الأسلاك بتنور الطيارة كلها")], "سلك نور بيشد الكاميرا"),
 "C06": (["كتب بتطير وبتتفتح"], "2D cartoon",
         [("E", "كراسة SKILL.md بتتفتح وتطلع رسومات"), ("C", "علي بياخد قدرة من كل كتاب")], "صفحة كتاب بتتقلب"),
 "C065": (["شاشة الكالندر FREEZE", "داشبوردات حقيقية بتطير", "الطيارة بتتركب"], "HUD + live action",
          [("E", "28 فيديو بيطيروا ويترصوا في جدول"), ("E", "عدّاد المشاهدات لحد 474K"), ("F", "سكرين الداشبوردات (اليوزرات متغطية)"), ("B", "علي الـ AI بيحكي")], "zoom-out من الكالندر"),
 "C07": (["المعمل: الطيارة بتتجمّع", "سكرينات الأدوات كشاشات في المعمل"], "screen + HUD",
         [("F", "سكرين الخطوة الحقيقية"), ("E", "كارت الخطوة + الأمر/اللينك"), ("D", "قطعة بتتركب في الطيارة"), ("B", "علي بيشاور على الشاشة")], "قطعة بتتركب وبتقفل الكادر"),
 "C075": (["لوح Tips بأرقام"], "HUD",
          [("E", "كارت رقم التريك + before/after"), ("F", "سكرين التريك"), ("E", "split قبل/بعد")], "كارت بيتقلب"),
 "C08": (["خزنة + فاتورة hologram"], "cinematic 3D + HUD",
         [("C", "low-angle hero قدام الخزنة"), ("E", "الفاتورة بتتملا سطر سطر، الأرقام عدّادات"), ("E", "المجموع بينفجر")], "باب الخزنة بيتفتح"),
 "C09": (["FREEZE طويل"], "live action",
         [("B", "الـ twin بيبص لضل علي الحقيقي"), ("C", "بيسلّمه آخر قطعة في الطيارة"), ("E", "قائمة دور الإنسان")], "كل حاجة بتقف"),
 "C095": (["شاشة يوتيوب بالـ label"], "HUD + screen",
          [("F", "مكان الـ label تحت المشغل / على الشورت"), ("E", "C2PA / SynthID كعلامة مستخبية بتنور"), ("B", "علي الـ AI بيقول القرار")], "label بيتحط على الكادر"),
 "C10": (["ستوديو مزيكا متولّد"], "2D cartoon",
         [("F", "Suno: الكلمات + الستايل"), ("E", "beat grid والمونتاج بيتقص عليه")], "سلك Suno MCP"),
 "C11": (["كل العوالم ورا بعض على الإيقاع"], "mix",
         [("C", "مونتاج على الـ beat من كل العوالم"), ("E", "كلمات الأغنية kinetic"), ("D", "الطيارة متركّبة بتطير")], "cut على الـ beat"),
 "C12": (["الطيارة طالعة من المعمل", "الثمبنيلز حوالين علي FREEZE"], "live action + HUD",
         [("E", "الثمبنيلز بتطير وتقف بأسمائها"), ("B", "علي بيلف للكاميرا"), ("C", "drone pull-out كبير")], "drone pull-out"),
}
TOOL = {"A": "HeyGen lipsync", "B": "HeyGen twin (look a7e1bb9b + ref c7e371d6)", "C": "Higgsfield Kling 4.0",
        "D": "Blender (EEVEE) blockout", "E": "Remotion (alpha)", "F": "screen recording / screenshot"}
FLEX = {"C00", "C02b", "C02f", "C05", "C08", "C12"}   # Seedance 2.5 flex shots (one per chapter)

rows, n = [], 0
for ch in tl["chapters"]:
    worlds, style, beats, trans = P[ch["id"]]
    t0, t1 = ch["start"], ch["end"] - tl["gap"]
    k = max(1, math.ceil((t1 - t0) / 6.0))
    d = (t1 - t0) / k
    flex_done = False
    for i in range(k):
        n += 1
        s = t0 + i * d
        typ, what = beats[i % len(beats)]
        world = worlds[int((s - t0) // 20) % len(worlds)]
        paid, cost, tool = "free", 0.0, TOOL[typ]
        if typ == "C":
            paid = "paid"
            if ch["id"] in FLEX and not flex_done:
                tool, cost, flex_done = "Higgsfield Seedance 2.5 720p (flex)", 35.0, True
            else:
                cost = 16.25 if d <= 5.5 else 32.5
        elif typ == "B":
            paid, cost = "paid", (None if V == "1" else f"HeyGen {d / 3:.1f}")
        rows.append({"n": n, "chapter": ch["id"], "start": round(s, 2), "dur": round(d, 2), "type": typ,
                     "style": style, "world": world, "what": what,
                     "transition": trans if i == 0 else ("world change: morph/match cut" if i and int((s - t0) // 20) != int((s - d - t0) // 20) else "cut on event"),
                     "tool": tool, "free_paid": paid, "cost": "HeyGen ?/s" if cost is None else cost,
                     "events": "zoom/push + object fly-in + sfx hit" if typ != "E" else "card pop + counter + ui click"})

with open(W / f"shotlist_v{V}.csv", "w", encoding="utf-8-sig", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    wr.writeheader(); wr.writerows(rows)
(W / f"shotlist_v{V}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")

from collections import Counter
c = Counter(r["type"] for r in rows)
hig = sum(r["cost"] for r in rows if isinstance(r["cost"], float))
bsec = sum(r["dur"] for r in rows if r["type"] == "B")
print(f"shots {len(rows)}  types {dict(c)}  Higgsfield {hig:.1f} credits  avatar(B) {bsec/60:.1f} min")
# checks
long = [r for r in rows if r["dur"] > 6.01]
print("shots > 6 s:", len(long))
