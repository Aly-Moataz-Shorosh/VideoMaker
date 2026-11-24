"""Note 49: the bill — only numbers read from the accounts (2026-11-23) + plan prices read on the pricing pages (work/site_tours_v1.md).
HeyGen 574 (2026-11-20) -> 130 = 444 (2026-11-24, after the v11 batch) · Higgsfield 3000.35 -> 1912.5 = 1087.85 · ElevenLabs used 15,425 this month, 6,228 before the video
(39,468 limit - 33,240 left on 11-20) = 9,197 · Suno 40 (8 takes) · overage 0 everywhere. Usage (project folder): python -X utf8 work/scripts/make_bill_v10.py"""
import json
rows = [["heygen.ico", "استخدمت 444 كريدت من 600 في HeyGen ـ اشتراك Creator بـ 29$ في الشهر"],
        ["higgsfield.png", "استخدمت حوالي 1088 كريدت في Higgsfield ـ اشتراك Ultra"],
        ["elevenlabs.png", "استخدمت 9197 حرف في ElevenLabs ـ اشتراك Starter بـ 6$ في الشهر"],
        ["suno.png", "استخدمت 40 كريدت في Suno = 8 نسخ للأغنية ـ اشتراك Pro بـ 10$ في الشهر"],
        ["claude.svg", "الاشتراك الشهري في Claude ـ الخطط بتبدأ من 20$"]]
json.dump({"title": "فاتورة الفيديو ده (لحد 24 نوفمبر 2026)", "rows": rows,
           "total": "كله جوه الاشتراكات الشهرية.. ومفيش ولا دولار زيادة"}, open("work/bill_v10.json", "w", encoding="utf-8"), ensure_ascii=False)
print("bill ok")
