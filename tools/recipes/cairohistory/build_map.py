"""Cairo map data for src/cairo (Aly 2026-10-09: "الخرايط تكون دقيقة… زي ما انا راسمها بالظبط").
Aly's own Google Earth drawings (assets/kmz/islamic2.kml) + today's Nile (OSM riverbank, work/osm/water0.json) + main roads.
All coordinates -> local metres around (LON_C, LAT_C): x east, y north. Output: motion-library/src/cairo/data.json"""
import json, math, re, sys
from pathlib import Path
import numpy as np, cv2

W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
sys.stdout.reconfigure(encoding='utf-8')
LON_C, LAT_C = 31.245, 30.05
KX = math.cos(math.radians(LAT_C)) * 111320; KY = 110540


def xy(lon, lat):
    return [round((lon - LON_C) * KX, 1), round((lat - LAT_C) * KY, 1)]


# ---- Aly's KMZ layers
kml = open(P / 'assets/kmz/islamic2.kml', encoding='utf8').read()
layers = {}
for m in re.finditer(r'<Placemark[^>]*>(.*?)</Placemark>', kml, re.S):
    body = m.group(1)
    name = re.search(r'<name>(.*?)</name>', body).group(1).strip()
    kind = 'poly' if '<Polygon' in body else 'line' if '<LineString' in body else 'pt'
    co = re.search(r'<coordinates>(.*?)</coordinates>', body, re.S)
    if not co:
        continue
    pts = [xy(*map(float, c.split(',')[:2])) for c in co.group(1).split()]
    if not pts:
        continue
    key = name if name not in layers else name + '#' + kind
    layers[key] = {'kind': kind, 'pts': pts}
layers['العسكر#poly'] = layers.pop('Untitled Polygon')  # his unnamed polygon = al-Askar (label point sits inside it)
for k, v in layers.items():
    print(f'{v["kind"]:5} {len(v["pts"]):3}  {k}')

# ---- today's Nile from the OSM bank lines (components touching top/bottom edge = water; islands stay land)
LON0, LAT0, LON1, LAT1 = 31.16, 29.97, 31.32, 30.14
R = 5.0
KXm = math.cos(math.radians(30.05)) * 111320
Wd = int((LON1 - LON0) * KXm / R); Hd = int((LAT1 - LAT0) * KY / R)
px = lambda lon, lat: (int(round((lon - LON0) * KXm / R)), int(round((LAT1 - lat) * KY / R)))
m = np.zeros((Hd, Wd), np.uint8)
for e in json.load(open(W / 'osm/water0.json'))['elements']:
    cv2.polylines(m, [np.array([px(g['lon'], g['lat']) for g in e['geometry']], np.int32)], False, 255, 3)
n, lab, st, _ = cv2.connectedComponentsWithStats((m == 0).astype(np.uint8), connectivity=4)
water = np.zeros_like(m)
for i in range(1, n):
    x, y, w, h, a = st[i]
    if (y == 0 or y + h == Hd) and not (x == 0 or x + w == Wd) and a * R * R < 1.0e6 or a * R * R > 5e6 and (y == 0 or y + h == Hd) and not (x == 0 or x + w == Wd):
        water[lab == i] = 1  # main river (11.6 km2) + small channels; the 1.48 km2 piece is Dahab island -> land
water = cv2.dilate(water, np.ones((3, 3), np.uint8))
cs, hier = cv2.findContours(water, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
nile = []
for c in cs:
    if cv2.contourArea(c) < 40:
        continue
    c = cv2.approxPolyDP(c, 1.2, True)[:, 0, :]
    nile.append([xy(LON0 + (p[0] * R) / KXm, LAT1 - (p[1] * R) / KY) for p in c])
print('nile rings', len(nile), sum(len(r) for r in nile), 'pts')

# ---- main roads today (simplified)
roads = []
for e in json.load(open(W / 'osm/roads.json'))['elements']:
    pts = np.array([xy(g['lon'], g['lat']) for g in e['geometry']], np.float32)
    if len(pts) < 2:
        continue
    s = cv2.approxPolyDP(pts.reshape(-1, 1, 2), 12, False)[:, 0, :]
    roads.append({'k': e['tags'].get('highway', '')[0], 'pts': [[round(float(a), 1), round(float(b), 1)] for a, b in s]})
print('roads', len(roads), sum(len(r['pts']) for r in roads))

# ---- extra points: Aly's other KMZ (ALL.kmz / My Places) + Koubba palace (not in his files, OSM position)
EXTRA = {'مسجد السلطان حسن': (31.25606536266739, 30.03236779844737), 'مسجد الظاهر بيبرس': (31.26321122423474, 30.06196400742908),
         'الجامع الأزهر': (31.26255732918965, 30.04577681482311), 'قصر عابدين': (31.248544, 30.0422696), 'قصر القبة': (31.2813, 30.0869)}
for k, (lo, la) in EXTRA.items():
    layers[k] = {'kind': 'pt', 'pts': [xy(lo, la)]}

# ---- region (Nile -> Red Sea canals, short 3): km around (RLON, RLAT), x east, y north. Natural Earth 10m.
from shapely.geometry import Polygon, box
RLON, RLAT = 31.9, 30.25
RKX = math.cos(math.radians(RLAT)) * 111.32; RKY = 110.54
rxy = lambda lo, la: [round((lo - RLON) * RKX, 2), round((la - RLAT) * RKY, 2)]
BB = box(29.4, 28.6, 34.6, 32.0)
land = []
for ring in json.load(open(W / 'osm/land_eg.json')):
    g = Polygon(ring).buffer(0).intersection(BB).simplify(0.004)
    for q in (getattr(g, 'geoms', None) or [g]):
        if q.is_empty or q.area < 1e-4:
            continue
        land.append([rxy(*c) for c in q.exterior.coords])
rivers = {}
for ft in json.load(open(W / 'osm/ne_10m_rivers_lake_centerlines_eg.json'))['features']:
    nm = ft['properties'].get('name') or 'x'
    g = ft['geometry']; lines = g['coordinates'] if g['type'] == 'MultiLineString' else [g['coordinates']]
    for ln in lines:
        rivers.setdefault(nm, []).append([rxy(*c) for c in ln if 29.4 <= c[0] <= 34.6 and 28.6 <= c[1] <= 32.0])
lakes = [[rxy(*c) for c in ft['geometry']['coordinates'][0]] for ft in json.load(open(W / 'osm/ne_10m_lakes_eg.json'))['features']]
lakes.append([rxy(32.29 + 0.03 * math.cos(a / 8 * math.pi), 30.565 + 0.02 * math.sin(a / 8 * math.pi)) for a in range(16)])  # Lake Timsah
# ancient canals (approximate routes, as on the maps Aly showed: Zagazig -> Wadi Tumilat -> Timsah -> Bitter Lakes -> Suez)
CAN = {'sesostris': [(31.50, 30.59), (31.70, 30.56), (31.95, 30.55), (32.15, 30.55), (32.27, 30.56), (32.33, 30.47), (32.37, 30.38),
                     (32.42, 30.25), (32.47, 30.15), (32.53, 30.05), (32.55, 29.97)],
       'roman': [(31.230, 30.022), (31.28, 30.10), (31.36, 30.22), (31.44, 30.35), (31.50, 30.48), (31.58, 30.55)],
       'amr': [(31.230, 30.022), (31.262, 30.075), (31.33, 30.18), (31.42, 30.30), (31.50, 30.43), (31.60, 30.54), (31.70, 30.56)]}
canals = {k: [rxy(*c) for c in v] for k, v in CAN.items()}
RP = {'القاهرة': (31.235, 30.044), 'الزقازيق': (31.50, 30.59), 'السويس': (32.55, 29.97), 'البحيرات المرة': (32.37, 30.35),
      'الإسماعيلية': (32.27, 30.60), 'البحر الأحمر': (32.75, 29.45), 'البحر المتوسط': (31.6, 31.75), 'بلبيس': (31.56, 30.42)}
region = {'land': land, 'rivers': rivers, 'lakes': lakes, 'canals': canals, 'pts': {k: rxy(*v) for k, v in RP.items()}}
print('region land rings', len(land), sum(len(r) for r in land), 'rivers', {k: sum(len(x) for x in v) for k, v in rivers.items()})

# ---- generated decoration (deterministic): houses per city (inside HIS polygons), Mamluk suburbs, modern blocks, fields, palms
from shapely.geometry import Point, LineString
from shapely.ops import unary_union
rng = np.random.default_rng(7)
poly = lambda k: Polygon(layers[k]['pts']).buffer(0)
water_now = unary_union([Polygon(r).buffer(0) for r in nile if Polygon(r).area > 2e5])  # outer river rings
holes = [Polygon(r).buffer(0) for r in nile if Polygon(r).area <= 2e5]
water_now = water_now.difference(unary_union(holes))  # islands (Zamalek, Roda, ...) are land
old_water = poly('شط النيل قديما')
pt = lambda k: Point(layers[k]['pts'][0])
roda = next((Polygon(r).buffer(0) for r in nile if Polygon(r).buffer(0).contains(pt('جزيرة المنيل'))), None)
print('roda ring found', roda is not None, 'old water contains Roda point', old_water.contains(pt('جزيرة المنيل')), 'Zamalek', old_water.contains(pt('جزيرة الزمالك')))


def scatter(area, n_max, foot, hgt, avoid=None):
    a = area.area; sp = max(foot[1] * 1.05, math.sqrt(a / n_max))
    x0, y0, x1, y1 = area.bounds; out = []
    for gx in np.arange(x0, x1, sp):
        for gy in np.arange(y0, y1, sp):
            x, y = gx + rng.uniform(-0.35, 0.35) * sp, gy + rng.uniform(-0.35, 0.35) * sp
            if area.contains(Point(x, y)) and not (avoid is not None and avoid.contains(Point(x, y))):
                out.append([round(x), round(y), int(rng.uniform(*foot)), int(rng.uniform(*hgt)), int(rng.integers(0, 4))])
    return out

cities = {'fustat': poly('الفسطاط'), 'askar': poly('العسكر#poly'), 'qatai': poly('القطائع'), 'fatimid': poly('القاهرة الفاطمية')}
houses = {k: scatter(v.difference(old_water), 340, (34, 58), (14, 34)) for k, v in cities.items()}
houses['fatimid'] = scatter(cities['fatimid'], 420, (30, 50), (16, 40))
for k, v in houses.items():
    print('houses', k, len(v), 'km2', round(cities[k].area / 1e6, 2))
# Mamluk era: people live outside the walls -> a band round the Fatimid city (west to the Khalij, north, round the citadel)
khal = LineString(layers['الخليج / شارع بورسعيد']['pts'])
cit = poly('قلعة صلاح الدين الأيوبي')
band = unary_union([cities['fatimid'].buffer(900), cit.buffer(700), Point(*layers['مسجد السلطان حسن']['pts'][0]).buffer(600),
                    Point(*layers['مسجد الظاهر بيبرس']['pts'][0]).buffer(500)])
old_all = unary_union(list(cities.values()) + [old_water, cit])
houses['mamluk'] = scatter(band.difference(old_all), 380, (30, 52), (14, 32))
print('houses mamluk', len(houses['mamluk']))
# modern Cairo: everything on land within ~7 km (river + islands excluded except Zamalek/Roda which are built too)
view = box(-7000, -7500, 7000, 8000)
land_now = view.difference(water_now)
blocks = scatter(land_now.difference(unary_union(list(cities.values()))), 2600, (110, 170), (25, 95))
for b in blocks:
    b.append(int(math.hypot(b[0] - 300, b[1] + 300)))  # distance from the old core -> grow outward
print('modern blocks', len(blocks))
# fields + palms (historic countryside): west bank & north, near the river, outside the old water
west = view.intersection(water_now.buffer(3200)).difference(old_water).difference(water_now)
fields = []
for b in scatter(west.difference(unary_union(list(cities.values())).buffer(300)), 1100, (80, 140), (0, 1)):
    fields.append(b[:3] + [int(rng.integers(0, 5)), int(rng.uniform(-20, 20))])
palms = [[round(x), round(y)] for x, y, *_ in scatter(old_water.buffer(400).difference(old_water).difference(water_now), 260, (1, 2), (0, 1))]
print('fields', len(fields), 'palms', len(palms))
deco = {'houses': houses, 'blocks': blocks, 'fields': fields, 'palms': palms,
        'roda': [[round(x), round(y)] for x, y in roda.exterior.coords] if roda is not None else [],
        'islands': [[[round(x), round(y)] for x, y in h.exterior.coords] for h in holes if h.area > 5e4 and not (roda is not None and h.equals(roda))],
        'centroid': {k: [round(v.centroid.x), round(v.centroid.y)] for k, v in cities.items()} | {'citadel': [round(cit.centroid.x), round(cit.centroid.y)]}}

out = ROOT / 'motion-library/src/cairo/data.json'
json.dump({'center': [LON_C, LAT_C], 'layers': layers, 'nile': nile, 'roads': roads, 'region': region, 'deco': deco,
           'rorg': [round((RLON - LON_C) * KX), round((RLAT - LAT_C) * KY)]}, open(out, 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print(out, out.stat().st_size // 1024, 'KB')
