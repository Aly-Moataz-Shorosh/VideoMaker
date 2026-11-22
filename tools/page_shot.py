"""Screenshot of an official page WITH its images (for showing a tool's site on screen; evidence.py blocks images for quotes).
Usage: python tools/page_shot.py <url> <out.png> [wait_s=5] [width=1600] [height=900]
Never bypass a bot check / login: if the page refuses, use another source."""
import sys, time
from playwright.sync_api import sync_playwright

url, out = sys.argv[1], sys.argv[2]
wait = float(sys.argv[3]) if len(sys.argv) > 3 else 5
w = int(sys.argv[4]) if len(sys.argv) > 4 else 1600
h = int(sys.argv[5]) if len(sys.argv) > 5 else 900
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    ctx = b.new_context(viewport={'width': w, 'height': h}, locale='en-US')
    pg = ctx.new_page()
    pg.goto(url, wait_until='domcontentloaded', timeout=60000)
    time.sleep(wait)
    for sel in ['button:has-text("Accept")', 'button:has-text("Reject")', 'button:has-text("Got it")']:   # cookie banners (decline when offered)
        try:
            if 'Reject' in sel and pg.locator(sel).first.is_visible(): pg.locator(sel).first.click(); break
        except Exception:
            pass
    pg.screenshot(path=out)
    print('ok', pg.url, out)
    b.close()
