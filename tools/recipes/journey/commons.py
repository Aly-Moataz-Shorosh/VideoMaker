"""Free real-example pictures from Wikimedia Commons (license + author kept for the credits in the .txt).
python work/scripts/commons.py search "<query>"      -> list files with license
python work/scripts/commons.py get "<File:...>" name -> assets/commons/<name>.jpg (1600 px) + assets/commons/credits.json"""
import json, sys, urllib.error, urllib.parse, urllib.request
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
P = Path(__file__).resolve().parents[2]
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
API = 'https://commons.wikimedia.org/w/api.php?'


def get(url):
    import time
    for k in range(6):  # Commons answers 429 when asked too fast -> back off
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(5 * (k + 1))
    raise RuntimeError('Commons kept refusing (429)')


def call(**q):
    q['format'] = 'json'
    return json.loads(get(API + urllib.parse.urlencode(q)))


def info(titles):
    d = call(action='query', titles='|'.join(titles), prop='imageinfo', iiprop='url|size|extmetadata', iiurlwidth=1600)
    out = []
    for p in d['query']['pages'].values():
        ii = (p.get('imageinfo') or [{}])[0]; m = ii.get('extmetadata', {})
        g = lambda k: (m.get(k, {}).get('value') or '').replace('\n', ' ')
        out.append({'title': p['title'], 'w': ii.get('width'), 'h': ii.get('height'), 'thumb': ii.get('thumburl'), 'license': g('LicenseShortName'),
                    'artist': __import__('re').sub('<[^>]+>', '', g('Artist'))[:80], 'page': ii.get('descriptionurl')})
    return out


if sys.argv[1] == 'search':
    r = call(action='query', list='search', srnamespace=6, srlimit=12, srsearch=sys.argv[2] + ' filetype:bitmap')
    for x in info([s['title'] for s in r['query']['search']]):
        print(f"{x['w']}x{x['h']} | {x['license']} | {x['artist'][:30]} | {x['title']}")
else:
    x = info([sys.argv[2]])[0]
    d = P / 'assets' / 'commons'; d.mkdir(parents=True, exist_ok=True)
    (d / f'{sys.argv[3]}.jpg').write_bytes(get(x['thumb']))
    cf = d / 'credits.json'
    c = json.loads(cf.read_text(encoding='utf8')) if cf.exists() else {}
    c[sys.argv[3]] = x
    cf.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding='utf8')
    print('saved', sys.argv[3], x['license'], x['artist'])
