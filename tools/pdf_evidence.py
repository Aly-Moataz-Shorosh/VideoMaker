"""Evidence from an official PDF (Aly's sourcing rule): check the quote is on that page, render the page with the quote highlighted.

Usage: python tools/pdf_evidence.py <evidence_pdf.json> <outdir>
Rows: {id, claim, pdf (local path, relative to the json), url (where the PDF lives online), page (1-based), quote}
Writes <outdir>/<id>.png (page image, quote boxed in yellow, banner: claim | url | page | date) and sets status per row.
"""
import json, os, re, sys, time
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')
ev_path, out = sys.argv[1], sys.argv[2]
base = os.path.dirname(os.path.abspath(ev_path))
rows = json.load(open(ev_path, encoding='utf-8'))
os.makedirs(out, exist_ok=True)
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 22)
norm = lambda s: re.sub(r'\s+', ' ', s.replace('\u2019', "'").replace('\u2013', '-')).strip()
docs = {}
for r in rows:
    pdf = docs.setdefault(r['pdf'], pdfium.PdfDocument(os.path.join(base, r['pdf'])))
    page = pdf[r['page'] - 1]
    tp = page.get_textpage()
    text = norm(tp.get_text_range())
    if norm(r['quote']) not in text:
        r['status'] = 'NOT FOUND'; print(r['id'], 'NOT FOUND'); continue
    sc = 2.0
    img = page.render(scale=sc).to_pil().convert('RGB')
    W, H = img.size
    over = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(over)
    # search the first 6 words (pdfium search works on short strings), box every char of the whole quote from there
    srch = tp.search(' '.join(r['quote'].split()[:6]), match_case=False)
    hit = srch.get_next()
    if hit:
        i0, n = hit
        n_all = len(r['quote'])
        for k in range(i0, min(i0 + n_all, tp.count_chars())):
            box = tp.get_charbox(k)
            if box and box[2] > box[0]:
                l, b_, rr, t = box
                d.rectangle([l * sc - 2, H - t * sc - 2, rr * sc + 2, H - b_ * sc + 2], fill=(255, 224, 102, 120))
    img = Image.alpha_composite(img.convert('RGBA'), over).convert('RGB')
    banner = Image.new('RGB', (W, 44), (34, 34, 34))
    ImageDraw.Draw(banner).text((10, 10), f"{r['claim']} | {r['url']} | page {r['page']} | captured {time.strftime('%Y-%m-%d')}", font=font, fill='white')
    full = Image.new('RGB', (W, H + 44)); full.paste(banner, (0, 0)); full.paste(img, (0, 44))
    full.save(os.path.join(out, r['id'] + '.png'))
    r['status'] = 'ok' if hit else 'ok (text found, box not drawn)'
    print(r['id'], r['status'])
json.dump(rows, open(ev_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
