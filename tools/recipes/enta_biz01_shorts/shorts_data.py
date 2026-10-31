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
}
PICK = [3, 5, 7, 18, 1]   # posting order (Aly: the worlds one LAST)
SHORTS = {i + 1: dict(IDEAS[k], idea=k) for i, k in enumerate(PICK)}
TOTAL = len(SHORTS)
