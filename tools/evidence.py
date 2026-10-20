"""Evidence for on-screen facts (Aly's sourcing rule): fetch the page, check the exact quote, take a highlighted screenshot.

Usage (one evidence.json per project, list of {id, claim, url, quote, shot?}):
  python tools/evidence.py fetch <evidence.json>            -> <dir>/ev_cache/<hash>.txt  (rendered page text)
  python tools/evidence.py find  <evidence.json> <id> <regex> ...   -> matching sentences of that row's page
  python tools/evidence.py check <evidence.json>            -> is every quote verbatim on its page?
  python tools/evidence.py shoot <evidence.json> <outdir>   -> PNG per row: quote highlighted + banner (claim | url | date)
Rendered with real Chrome (Playwright, images blocked). Never bypass a bot check: a page that refuses = use another source.
"""
import hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HL = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'highlight.js'), encoding='utf-8').read()
TEXT_JS = "() => { const r = document.querySelector('#mw-content-text') || document.querySelector('main') || document.body; return r.textContent; }"


def cache_of(evfile, url):
    d = os.path.join(os.path.dirname(os.path.abspath(evfile)), 'ev_cache'); os.makedirs(d, exist_ok=True)
    return os.path.join(d, hashlib.md5(url.encode()).hexdigest()[:12] + '.txt')


def browser(p):
    b = p.chromium.launch(channel='chrome', headless=os.environ.get('EV_HEADFUL') != '1', args=['--window-position=-2400,0'])
    ctx = b.new_context(viewport={'width': 1280, 'height': 900}, locale='en-US')
    ctx.route(re.compile(r'.*\.(png|jpe?g|gif|webp|svg)(\?.*)?$', re.I), lambda r: r.abort())
    return b, ctx


def load(pg, url):
    pg.goto(url, wait_until='domcontentloaded', timeout=60000)
    time.sleep(2.5)


def fetch(evfile):
    from playwright.sync_api import sync_playwright
    urls = sorted({e['url'] for e in json.load(open(evfile, encoding='utf-8'))})
    with sync_playwright() as p:
        b, ctx = browser(p); pg = ctx.new_page()
        for u in urls:
            f = cache_of(evfile, u)
            if os.path.exists(f) and os.path.getsize(f) > 500: continue
            try:
                load(pg, u); t = pg.evaluate(TEXT_JS)
                open(f, 'w', encoding='utf-8').write(u + '\n' + t); print(len(t), u, flush=True)
            except Exception as ex:
                print('ERR', u, str(ex)[:100], flush=True); pg.close(); pg = ctx.new_page()
        b.close()


def text_of(evfile, url):
    f = cache_of(evfile, url)
    return open(f, encoding='utf-8').read() if os.path.exists(f) else None


def present(t, quote):
    parts = [re.escape(x) for x in quote.split()]
    return bool(re.search(r'(?:\s|\[[^\]]{0,12}\]|[‎‏­])*'.join(parts), t, re.I))


def find(evfile, rid, pats):
    e = next(e for e in json.load(open(evfile, encoding='utf-8')) if e['id'] == rid)
    t = text_of(evfile, e['url']) or ''
    for s in re.split(r'(?<=[.!?])\s+|\n+', t):
        if any(re.search(p, s, re.I) for p in pats): print(' *', s.strip()[:400])


def check(evfile):
    bad = 0
    for e in json.load(open(evfile, encoding='utf-8')):
        t = text_of(evfile, e['url'])
        ok = None if t is None else present(t, e['quote'])
        bad += ok is not True
        print('OK ' if ok else ('NO PAGE' if ok is None else 'MISSING'), e['id'], '|', e['quote'][:80])
    print('missing:', bad)


def shoot(evfile, out):
    from playwright.sync_api import sync_playwright
    ev = json.load(open(evfile, encoding='utf-8')); os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b, ctx = browser(p); pg = ctx.new_page()
        for e in ev:
            e.setdefault('shot', e['id'] + '.png')
            try:
                load(pg, e['url'])
                if not pg.evaluate(HL, e['quote']):
                    e['status'] = 'NOT FOUND'; print(e['id'], 'NOT FOUND', flush=True); continue
                banner = f"{e['claim']} | {e['url']} | captured {time.strftime('%Y-%m-%d')}"
                pg.evaluate("(t)=>{const d=document.createElement('div');d.textContent=t;d.style.cssText='position:fixed;top:0;left:0;right:0;z-index:99999;background:#222;color:#fff;font:13px Arial;padding:6px 10px;direction:ltr;text-align:left';document.body.appendChild(d);}", banner)
                pg.screenshot(path=os.path.join(out, e['shot'])); e['status'] = 'ok'; print(e['id'], 'ok', flush=True)
            except Exception as ex:
                e['status'] = 'ERR ' + str(ex)[:80]; print(e['id'], e['status'], flush=True); pg.close(); pg = ctx.new_page()
        b.close()
    json.dump(ev, open(evfile, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('ok', sum(e.get('status') == 'ok' for e in ev), 'of', len(ev))


if __name__ == '__main__':
    cmd, f = sys.argv[1], sys.argv[2]
    {'fetch': lambda: fetch(f), 'check': lambda: check(f), 'find': lambda: find(f, sys.argv[3], sys.argv[4:]),
     'shoot': lambda: shoot(f, sys.argv[3])}[cmd]()
