# On-screen proof: the EP1 YouTube page cropped to the player + title + description, upload date highlighted (no side suggestions).
import time, sys
from playwright.sync_api import sync_playwright
out = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=False, args=['--window-position=-2400,0'])
    pg = b.new_context(viewport={'width': 1280, 'height': 900}, locale='en-US', device_scale_factor=2).new_page()
    pg.goto('https://www.youtube.com/watch?v=fY2V1nY0u18', wait_until='domcontentloaded'); time.sleep(6)
    pg.evaluate("""() => { const v = document.querySelector('video'); if (v) v.pause();
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      while (w.nextNode()) { const n = w.currentNode; const i = n.nodeValue.indexOf('4/13/2018');
        if (i >= 0 && n.parentElement.offsetParent) { const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + 9);
          const m = document.createElement('mark'); m.style.cssText = 'background:#ffe066;outline:3px solid #e8590c;border-radius:3px'; r.surroundContents(m); break; } } }""")
    time.sleep(1)
    pg.screenshot(path=out, clip={'x': 12, 'y': 62, 'width': 882, 'height': 712})
    b.close()
print('ok', out)
