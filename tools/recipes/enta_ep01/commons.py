"""Search Wikimedia Commons and list / download pictures (free licences). Generic User-Agent only.
python commons.py search "<query>" [n]      -> prints title, size, licence
python commons.py get "<File:title>" <out.jpg> [width]"""
import json, sys, time, urllib.error, urllib.parse, urllib.request
UA = {'User-Agent': 'video-maker/1.0 (personal project)'}
API = 'https://commons.wikimedia.org/w/api.php?'
def fetch(url):  # polite: wait and retry on 429 (Wikimedia rate limit)
    for k in range(6):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(10 * (k + 1))
    raise SystemExit('rate limited: ' + url)
def call(**q):
    q.update(format='json')
    return json.loads(fetch(API + urllib.parse.urlencode(q)))
if sys.argv[1] == 'search':
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    r = call(action='query', generator='search', gsrsearch=sys.argv[2] + ' filetype:bitmap', gsrnamespace=6, gsrlimit=n,
             prop='imageinfo', iiprop='size|extmetadata', iiextmetadatafilter='LicenseShortName')
    for p in sorted(r.get('query', {}).get('pages', {}).values(), key=lambda p: p.get('index', 0)):
        ii = p['imageinfo'][0]
        print(p['title'], ii['width'], 'x', ii['height'], ii.get('extmetadata', {}).get('LicenseShortName', {}).get('value', ''))
else:
    w = int(sys.argv[4]) if len(sys.argv) > 4 else 1400
    r = call(action='query', titles=sys.argv[2], prop='imageinfo', iiprop='url', iiurlwidth=w)
    url = list(r['query']['pages'].values())[0]['imageinfo'][0]['thumburl']
    time.sleep(2)
    open(sys.argv[3], 'wb').write(fetch(url))
    print('ok', sys.argv[3])
