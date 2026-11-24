"""Reach batch analyzer (Homus optimization loop) — ratios, course points, outliers.

Usage:
  python reach_batch.py --template batch.csv          # write an empty CSV to fill
  python reach_batch.py batch.csv [--xlsx out.xlsx]   # analyse a filled CSV (UTF-8)

CSV columns (only title + views are required; empty cells = unknown):
  title, views, likes, comments, shares, saves, follows, full_watches, rewatches, retention, type, format, hook, length, notes

Outputs a markdown report on stdout (+ an xlsx when --xlsx is given):
  - per 1,000 views: likes, comments, shares, saves, follows
  - saves/likes and shares/likes ratios (Homus: ratios > numbers)
  - course points model (like 1, comment 2, share 3, full watch 4, rewatch 5) per 1,000 views — a teaching model, not platform data
  - outlier group by a composite of views and engagement: top 20% positive, bottom 20% negative, the rest core
  - averages per type (A/B/C), format and hook, so patterns show up
"""
import csv
import sys
import statistics as st

COLS = ["title", "views", "likes", "comments", "shares", "saves", "follows", "full_watches",
        "rewatches", "retention", "type", "format", "hook", "length", "notes"]
NUM = ["views", "likes", "comments", "shares", "saves", "follows", "full_watches", "rewatches", "retention"]
POINTS = {"likes": 1, "comments": 2, "shares": 3, "full_watches": 4, "rewatches": 5}


def num(v):
    v = (v or "").strip().replace(",", "").replace("%", "")
    if not v:
        return None
    try:
        return float(v)
    except ValueError:
        return None


def per_k(x, views):
    return None if x is None or not views else 1000.0 * x / views


def ratio(a, b):
    return None if a is None or not b else a / b


def fmt(x, d=1):
    return "-" if x is None else f"{x:.{d}f}"


def rank_pct(values, x):
    vals = sorted(v for v in values if v is not None)
    if x is None or not vals:
        return None
    return sum(1 for v in vals if v <= x) / len(vals)


def load(path):
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if not (r.get("title") or "").strip():
                continue
            d = {k: (r.get(k) or "").strip() for k in COLS}
            for k in NUM:
                d[k] = num(r.get(k))
            rows.append(d)
    return rows


def analyse(rows):
    for r in rows:
        v = r["views"]
        for k in ["likes", "comments", "shares", "saves", "follows"]:
            r[k + "_pk"] = per_k(r[k], v)
        r["saves_per_like"] = ratio(r["saves"], r["likes"])
        r["shares_per_like"] = ratio(r["shares"], r["likes"])
        pts = [POINTS[k] * r[k] for k in POINTS if r[k] is not None]
        r["points_pk"] = per_k(sum(pts), v) if pts else None
        eng = [r[k] for k in ["comments", "shares", "saves"] if r[k] is not None]
        r["eng_pk"] = per_k(sum(eng), v) if eng else None
    views = [r["views"] for r in rows]
    eng = [r["eng_pk"] for r in rows]
    for r in rows:
        a, b = rank_pct(views, r["views"]), rank_pct(eng, r["eng_pk"])
        parts = [p for p in (a, b) if p is not None]
        r["score"] = sum(parts) / len(parts) if parts else None
    scored = sorted((r for r in rows if r["score"] is not None), key=lambda r: r["score"], reverse=True)
    n = len(scored)
    k = max(1, round(n * 0.2)) if n >= 5 else 1
    for i, r in enumerate(scored):
        r["group"] = "positive" if i < k else ("negative" if i >= n - k else "core")
    return rows


def group_avgs(rows, key):
    out = {}
    for r in rows:
        g = r.get(key) or "-"
        out.setdefault(g, []).append(r)
    res = []
    for g, rs in out.items():
        def avg(f):
            vals = [x[f] for x in rs if x.get(f) is not None]
            return st.mean(vals) if vals else None
        res.append((g, len(rs), avg("views"), avg("shares_pk"), avg("saves_pk"), avg("comments_pk")))
    return sorted(res, key=lambda t: -(t[2] or 0))


def report(rows):
    L = ["# Reach batch report", "", f"Videos: {len(rows)} · points model = Homus course model (like 1, comment 2, share 3, "
         "full watch 4, rewatch 5), not platform data.", "",
         "| group | title | views | likes/1k | comments/1k | shares/1k | saves/1k | follows/1k | saves/like | shares/like | points/1k |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    order = {"positive": 0, "core": 1, "negative": 2}
    for r in sorted(rows, key=lambda r: (order.get(r.get("group"), 3), -(r["views"] or 0))):
        L.append(f"| {r.get('group', '-')} | {r['title']} | {fmt(r['views'], 0)} | {fmt(r['likes_pk'])} | {fmt(r['comments_pk'])} | "
                 f"{fmt(r['shares_pk'])} | {fmt(r['saves_pk'])} | {fmt(r['follows_pk'])} | {fmt(r['saves_per_like'], 2)} | "
                 f"{fmt(r['shares_per_like'], 2)} | {fmt(r['points_pk'], 0)} |")
    for key, name in [("type", "type (A/B/C)"), ("format", "format"), ("hook", "hook type")]:
        if any(r.get(key) for r in rows):
            L += ["", f"## Averages by {name}", "", "| value | videos | avg views | shares/1k | saves/1k | comments/1k |",
                  "|---|---|---|---|---|---|"]
            for g, c, v, sh, sa, co in group_avgs(rows, key):
                L.append(f"| {g} | {c} | {fmt(v, 0)} | {fmt(sh)} | {fmt(sa)} | {fmt(co)} |")
    L += ["", "## Next (fill by hand)", "- Patterns: topics / hooks / formats / delivery / CTA",
          "- Comment research: questions / objections / confusion / demand",
          "- 3 hypotheses → next 10 videos, each with ONE test variable"]
    return "\n".join(L)


def write_xlsx(rows, path):
    from openpyxl import Workbook
    from openpyxl.styles import PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "batch"
    head = ["group", "title", "type", "format", "hook", "views", "likes/1k", "comments/1k", "shares/1k", "saves/1k",
            "follows/1k", "saves/like", "shares/like", "points/1k", "notes"]
    ws.append(head)
    fill = {"positive": PatternFill("solid", fgColor="C6EFCE"), "negative": PatternFill("solid", fgColor="FFC7CE")}
    for r in rows:
        ws.append([r.get("group"), r["title"], r["type"], r["format"], r["hook"], r["views"], r["likes_pk"], r["comments_pk"],
                   r["shares_pk"], r["saves_pk"], r["follows_pk"], r["saves_per_like"], r["shares_per_like"], r["points_pk"], r["notes"]])
        if r.get("group") in fill:
            for c in ws[ws.max_row]:
                c.fill = fill[r["group"]]
    wb.save(path)


def main(argv):
    if len(argv) >= 2 and argv[0] == "--template":
        with open(argv[1], "w", encoding="utf-8-sig", newline="") as f:
            csv.writer(f).writerow(COLS)
        print("template written:", argv[1])
        return
    if not argv:
        print(__doc__)
        return
    rows = analyse(load(argv[0]))
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(report(rows))
    if "--xlsx" in argv:
        write_xlsx(rows, argv[argv.index("--xlsx") + 1])


if __name__ == "__main__":
    main(sys.argv[1:])
