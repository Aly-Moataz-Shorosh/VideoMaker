"""Approximate on-screen boxes of v5 items (shared by the overlap check and the auto-resolver)."""
def tw(text, size): return len(str(text or "")) * size * 0.60 + 48
def boxes(d, end):
    k = d["k"]; x, y = d.get("x"), d.get("y")
    if x is None: return []
    sc = d.get("scale", 1)
    if k == "node":
        w = d.get("w"); bx = []
        top = y
        if d.get("src"):
            h = w / d.get("ar", 16 / 9); bx.append((x - w / 2, y - h / 2, x + w / 2, y + h / 2)); top = y + h / 2
        elif d.get("logo"):
            s = d.get("s", 110); bx.append((x - s / 2, y - s / 2, x + s / 2, y + s / 2)); top = y + s / 2
        if d.get("label"):
            sz = d.get("size", 30); lw = tw(d["label"], sz) + (sz * 1.4 if d.get("emo") else 0); lh = sz * 1.6
            if d.get("src") or d.get("logo"): bx.append((x - lw / 2, top + 6, x + lw / 2, top + 6 + lh)); top += lh + 6
            else: bx.append((x - lw / 2, y - lh / 2, x + lw / 2, y + lh / 2)); top = y + lh / 2
        if d.get("sub"):
            sz = d.get("size", 30) * 0.72; lw = tw(d["sub"], sz); bx.append((x - lw / 2, top + 4, x + lw / 2, top + 4 + sz * 1.5))
        return bx
    if k == "pic":
        w = d.get("w", 420) * sc; h = w / d.get("ar", 16 / 9); b = [(x - w / 2, y - h / 2, x + w / 2, y + h / 2)]
        if d.get("cap"): cw = tw(d["cap"], d.get("capSize", 32) * sc); b.append((x - cw / 2, y + h / 2 - 10, x + cw / 2, y + h / 2 + 45 * sc))
        return b
    if k == "logo": s = d.get("s", 200) * sc; return [(x - s / 2, y - s / 2, x + s / 2, y + s / 2)]
    if k in ("text", "chip"):
        sz = d.get("size", 48) * sc; w = tw(d.get("text"), sz) + (sz * 1.3 if d.get("emo") else 0); return [(x - w / 2, y - sz * 0.9, x + w / 2, y + sz * 0.9)]
    if k == "num": sz = d.get("size", 120) * sc; w = len(str(int(d.get("to", 0)))) * sz * 0.62 + 20; return [(x - w / 2, y - sz * 0.6, x + w / 2, y + sz * 0.6)]
    if k == "typed": w = d.get("w", 560); n = str(d.get("text", "")).count("\n") + 1; return [(x - w / 2, y, x + w / 2, y + n * d.get("size", 24) * 1.45 + 30)]
    if k == "wave": return [(x - d["w"] / 2, y - d["h"] / 2, x + d["w"] / 2, y + d["h"] / 2)]
    if k == "bar": return [(x - 70, d["base"] - d["h"] - 120, x + 70, d["base"] + 110)]
    if k == "scan": w = d["w"]; h = w / d.get("ar", 16 / 9); return [(x - w / 2, y - h / 2, x + w / 2, y + h / 2 + (50 if d.get("text") else 0))]
    return []
def inter(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0]); h = min(a[3], b[3]) - max(a[1], b[1])
    return w * h if w > 0 and h > 0 else 0
