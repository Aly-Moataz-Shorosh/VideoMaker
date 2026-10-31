"""Shorts from رواد الأعمال ep01 (Karim Tamer). Aly 2026-10-28 picked from my 3 lists: 3 (AI took two pillars), 5 (The Dip: push on or
throw the towel), 7 (how each business got its first customers), 18 (food business is not software) and, last, 1 (every business = its
own world). Per short: slug, head (*word* = boxed), hook (a, b) = cold-open sentence, pieces [(a, b), ...] (source sec, rough edges ->
edges.fit; (a, b, 'x') = exact by hand). Key = posting order."""
IDEAS = {
    3: dict(slug='ai_pillars', head='الـ*AI* شال عمودين من البيزنس', hook=(1743.5, 1750.8), pieces=[(1611.4, 1754.1)]),
    5: dict(slug='the_dip', head='لازم تبقى *الأول* في عالمك؟', hook=(805.65, 811.45, 'x'), pieces=[(673.7, 705.0), (801.2, 823.0)]),   # v2 (Aly 2026-10-30): his cake reply, no 'ماتقاوحش'
    7: dict(slug='first_customers', head='أول *عميل* بيجي منين؟', hook=(2119.0, 2126.9), pieces=[(2064.1, 2143.0)]),
    18: dict(slug='food_business', head='بيزنس *الأكل* مش زي السوفتوير', hook=(1180.8, 1187.7), pieces=[(1167.0, 1259.5)]),
    1: dict(slug='worlds', head='كل بيزنس = *عالم* لوحده', hook=(1119.62, 1125.0, 'x'), pieces=[(706.2, 793.0), (823.5, 830.3), (1115.8, 1134.8), (1511.4, 1529.7)]),   # v2: every 'world' moment, no Dip part; v3 hook = the NEW world (Aly: the hook must not be the sentence the short starts with)
    # Aly 2026-10-31: "شورت ليها علاقة ب courzerve يكون باين فيها امثلة من شغل courzerve" -> the story + the lesson, and REAL Courzerve work
    # (their posts + campaign videos from Behance) on top while he names it. work = (src a, src b, item): pic / posts / clip (campaign N, from sec)
    21: dict(slug='courzerve', head='قصة *Courzerve*… واتقفلت', hook=(491.30, 499.12, 'x'), pieces=[(307.79, 336.40, 'x'), (342.6, 362.98), (457.85, 545.3)],
             work=[(307.9, 312.9, dict(kind='pic', src='cz_banner.jpg', label='هنا بدأت *Courzerve*')),
                   (318.5, 322.4, dict(kind='pic', src='logo.jpg', label='*Cour*se + Rese*rve* = Courzerve')),
                   (348.9, 356.3, dict(kind='posts', srcs=['cz_web.jpg', 'cz_android.jpg', 'cz_post_4.jpg', 'cz_post_8.jpg'], label='كورسات *Software Engineering*')),
                   (356.5, 362.95, dict(kind='clip', cam=1, frm=30.0, label='بعد الكورونا: الكورس *Live* على Zoom')),
                   (457.9, 462.6, dict(kind='clip', cam=3, frm=21.5, label='نعرف نكتب *Code*… ونعمل *Website*')),
                   (488.2, 493.2, dict(kind='clip', cam=3, frm=100.0, label='الويبسايت بتاع *Courzerve*')),
                   (493.2, 496.6, dict(kind='clip', cam=1, frm=77.6, label='تحجز معاد الكورس من الـ*Calendar*')),
                   (496.6, 499.1, dict(kind='clip', cam=2, frm=102.5, label='فورم تسجيل، ورسايل *SMS*، و*Mail*')),
                   (517.6, 520.3, dict(kind='posts', srcs=['cz_post_1.jpg', 'cz_post_5.jpg', 'cz_post_7.jpg', 'cz_post_3.jpg', 'cz_post_6.jpg'], label='الأول: *صور* بس')),
                   (520.3, 525.4, dict(kind='clip', cam=2, frm=110.0, label='بعدين: فيديوهات الـ*Instructors* في ستوديو', pos='top')),
                   (525.4, 530.3, dict(kind='clip', cam=3, frm=119.5, label='كاميرا، و*Backdrop*، ومونتاج… على *يوتيوب*', pos='top'))]),
}
PICK = [3, 5, 7, 18, 1, 21]   # posting order (Aly: the worlds one LAST of the first five; 21 = Courzerve, added 2026-10-31)
SHORTS = {i + 1: dict(IDEAS[k], idea=k) for i, k in enumerate(PICK)}
TOTAL = len(SHORTS)
