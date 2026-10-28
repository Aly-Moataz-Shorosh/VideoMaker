"""Shorts from رواد الأعمال ep01 (Karim Tamer). Aly 2026-10-28 picked from my 3 lists: 3 (AI took two pillars), 5 (The Dip: push on or
throw the towel), 7 (how each business got its first customers), 18 (food business is not software) and, last, 1 (every business = its
own world). Per short: slug, head (*word* = boxed), hook (a, b) = cold-open sentence, pieces [(a, b), ...] (source sec, rough edges ->
edges.fit; (a, b, 'x') = exact by hand). Key = posting order."""
IDEAS = {
    3: dict(slug='ai_pillars', head='الـ*AI* شال عمودين من البيزنس', hook=(1743.5, 1750.8), pieces=[(1611.4, 1754.1)]),
    5: dict(slug='the_dip', head='تكمّل ولا *ترمي المنديل*؟', hook=(2198.5, 2210.0), pieces=[(673.7, 705.0), (2175.4, 2232.3)]),
    7: dict(slug='first_customers', head='أول *عميل* بيجي منين؟', hook=(2119.0, 2126.9), pieces=[(2064.1, 2143.0)]),
    18: dict(slug='food_business', head='بيزنس *الأكل* مش زي السوفتوير', hook=(1180.8, 1187.7), pieces=[(1167.0, 1259.5)]),
    1: dict(slug='worlds', head='كل بيزنس = *عالم* لوحده', hook=(706.2, 713.5), pieces=[(695.9, 793.0), (823.5, 830.3), (1115.8, 1134.8)]),
}
PICK = [3, 5, 7, 18, 1]   # posting order (Aly: the worlds one LAST)
SHORTS = {i + 1: dict(IDEAS[k], idea=k) for i, k in enumerate(PICK)}
TOTAL = len(SHORTS)
