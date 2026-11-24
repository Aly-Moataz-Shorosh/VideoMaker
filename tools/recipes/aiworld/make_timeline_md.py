"""shotlist_v1.json + timeline_v1.json -> output/rough_cut_v1_timeline.md (what is where in rough_cut_v1.mp4)."""
import json
from pathlib import Path
W = Path(__file__).resolve().parent.parent
tl = json.loads((W / "timeline_v1.json").read_text(encoding="utf-8"))
shots = json.loads((W / "shotlist_v1.json").read_text(encoding="utf-8"))
mm = lambda x: f"{int(x)//60}:{int(x)%60:02d}"
L = ["# rough_cut_v1 — التايملاين (720p، 25fps، " + mm(tl["total"]) + ")",
     "كل لقطة = كارت placeholder (حدود متقطعة = لقطة مدفوعة مطلوبة، خط عادي = مجاني). لقطات D في الطيارة/المعمل/الكوبري = Blender blockout الحقيقي.",
     "الكابشن = نص الـ narration بتوقيت تقديري (2.2 كلمة/ث). **مفيش صوت** (مفيش voice placeholder؛ الصوت الحقيقي = HeyGen بعد الموافقة).",
     "Layers شفافة جاهزة في `output/layers_alpha_v1/` (badge، families، counters، card_<chapter>).", ""]
for ch in tl["chapters"]:
    ss = [s for s in shots if s["chapter"] == ch["id"]]
    paid = sum(1 for s in ss if s["free_paid"] == "paid")
    L.append(f"## {mm(ch['start'])}–{mm(ch['end'])} {ch['id']} {ch['title']} ({len(ss)} لقطة، {paid} مدفوعة)")
    L.append("| # | من | ث | نوع | العالم | اللقطة | الأداة | تكلفة |")
    L.append("|---|---|---|---|---|---|---|---|")
    for s in ss:
        L.append(f"| {s['n']} | {mm(s['start'])} | {s['dur']} | {s['type']} | {s['world']} | {s['what']} | {s['tool']} | {s['cost']} |")
    L.append("")
(W.parent / "output" / "rough_cut_v1_timeline.md").write_text("\n".join(L), encoding="utf-8")
print("ok", len(shots))
