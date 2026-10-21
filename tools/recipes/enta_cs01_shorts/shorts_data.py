"""Shorts from cs ep01 (Aly 2026-10-21: "حولي الفيديو ده ل shorts" — end = the full episode + QR, no CTA clip).
Per short: slug, head (headline, *word* = boxed), hook (a, b) = cold-open sentence (source sec, rough word edges -> edges.fit),
pieces [(a, b), ...] = the idea from its start. (a, b, 'x') = exact edges by hand. Order = posting order (strongest first)."""
IDEAS = {
    1: dict(slug='tester_eyes', head='ليه الشركة محتاجة *Tester* لو الـDeveloper شاطر؟', hook=(499.7, 507.6), pieces=[(469.9, 539.9)]),
    2: dict(slug='ai_replace', head='هل الـ*AI* هيستبدل الـTester؟', hook=(1603.8, 1613.58, 'x'), pieces=[(1549.4, 1634.1), (1644.7, 1652.2)]),
    3: dict(slug='boring', head='هل الـ*Testing* شغل ممل؟', hook=(240.8, 249.6), pieces=[(209.4, 283.4)]),
    4: dict(slug='production', head='ننزّل الـApp *من غير Testing* والناس تبلّغ؟', hook=(756.4, 765.2), pieces=[(711.8, 797.0)]),
    5: dict(slug='no_cs_degree', head='لازم تكون *خريج حاسبات* عشان تبقى Tester؟', hook=(1150.67, 1156.5, 'x'), pieces=[(1053.57, 1062.66, 'x'), (1137.6, 1168.2)]),
    6: dict(slug='junior_ai', head='الـ*AI* خد شغل الـJunior؟', hook=(1691.22, 1700.99, 'x'), pieces=[(1665.9, 1709.6), (1723.5, 1727.36, 'x')]),
    7: dict(slug='istqb', head='شهادة *ISTQB* مهمة ولا لأ؟', hook=(1488.4, 1490.1), pieces=[(1413.3, 1484.3), (1488.4, 1512.9)]),
    8: dict(slug='joker', head='الـTester لازم يكون *جوكر*', hook=(1312.4, 1317.9), pieces=[(1238.2, 1336.1)]),
    9: dict(slug='what_is_qc', head='يعني إيه *QC*؟ ببساطة', hook=(317.0, 322.4), pieces=[(291.1, 347.9), (417.9, 460.6)]),
    10: dict(slug='roadmap', head='تبدأ *Testing* منين؟', hook=(1183.1, 1185.9), pieces=[(1169.5, 1235.3)]),
    11: dict(slug='manual_automation', head='*Manual* ولا *Automation*؟', hook=(953.5, 959.1), pieces=[(913.12, 980.6, 'x')]),
    12: dict(slug='ai_bugs', head='الـ*AI* قلّل الـBugs؟', hook=(640.6, 646.2), pieces=[(541.1, 557.6), (595.5, 606.9), (610.4, 646.2)]),
    13: dict(slug='passion', head='حد بيدخل *Testing* عن شغف؟', hook=(191.2, 194.3), pieces=[(109.6, 194.3)]),
    14: dict(slug='api_testing', head='يعني إيه *API Testing*؟', hook=(985.3, 992.1), pieces=[(981.6, 1048.3)]),
    15: dict(slug='ai_advice', head='نصيحة لأي حد *خايف من الـAI*', hook=(1755.2, 1761.4), pieces=[(1729.0, 1775.9)]),
    16: dict(slug='requirements', head='إزاي تعرف الـ*صح* من الغلط؟', hook=(401.88, 411.93, 'x'), pieces=[(350.8, 415.9)]),
    17: dict(slug='predict_bug', head='الـTester بيعرف الـ*Bug* فين قبل ما يدوّر', hook=(1393.1, 1396.9), pieces=[(1373.42, 1403.3, 'x')]),
}
# Aly 2026-10-21: "مش مستاهلة عدد كتير… اهم و اقوى 5 شورتس مثلا او 3" -> the 5 strongest, best 3 first.
# key = posting number, 'idea' = number in IDEAS (words_NN.json + CAPS are keyed by the idea)
PICK = [1, 2, 5, 3, 4]
SHORTS = {i + 1: dict(IDEAS[k], idea=k) for i, k in enumerate(PICK)}
TOTAL = len(SHORTS)
