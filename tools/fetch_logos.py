"""Tip 13 — tool logo library: get each tool's logo ONCE from its OFFICIAL site -> brand/logos-tools/<name>.<ext>
+ one line in brand/logos-tools/index.md (source page, file url, date). Skips names already in the folder.
Takes the site's own declared icon (apple-touch-icon > svg icon > biggest png icon). Logos = only to identify the tool.
Usage: python -I tools/fetch_logos.py   (edit SITES below)"""
import datetime, re, sys, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "brand" / "logos-tools"
UA = {"User-Agent": "Mozilla/5.0 (logo-library script)"}
SITES = {
    "heygen": "https://www.heygen.com", "elevenlabs": "https://elevenlabs.io", "higgsfield": "https://higgsfield.ai",
    "suno": "https://suno.com", "claude": "https://claude.com", "openai-codex": "https://developers.openai.com",
    "antigravity": "https://antigravity.google", "blender": "https://docs.blender.org", "remotion": "https://www.remotion.dev",
    "ffmpeg": "https://ffmpeg.org", "comfyui": "https://www.comfy.org", "capcut": "https://www.capcut.com",
    "kling": "https://klingai.com", "runway": "https://runwayml.com",
    # 2026-11-21 rough cut v3 (only the ones the first pass did not get)
    "seedance": "https://seed.bytedance.com", "bytedance": "https://www.bytedance.com", "gemini": "https://gemini.google.com",
    "qwen": "https://qwen.ai", "ollama": "https://ollama.com", "ltx": "https://ltx.studio", "firefly": "https://firefly.adobe.com",
    "luma": "https://lumalabs.ai", "youtube": "https://www.youtube.com", "warner": "https://www.wmg.com", "believe": "https://www.believe.com",
}


def get(url, n=3_000_000):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
        return r.read(n), r.headers.get("Content-Type", ""), r.geturl()


def icons(html, base):
    out = []
    for tag in re.findall(r"<link[^>]+>", html, re.I):
        rel = (re.search(r'rel=["\']([^"\']+)', tag, re.I) or [None, ""])[1].lower()
        href = (re.search(r'href=["\']([^"\']+)', tag, re.I) or [None, ""])[1]
        if "icon" not in rel or not href:
            continue
        size = re.search(r'sizes=["\'](\d+)x', tag, re.I)
        score = (3 if "apple-touch" in rel else 0) + (2 if href.split("?")[0].endswith(".svg") else 0) + (int(size[1]) / 1000 if size else 0)
        out.append((score, urllib.parse.urljoin(base, href)))
    out.sort(reverse=True)
    return [u for _, u in out] + [urllib.parse.urljoin(base, "/favicon.ico")]


def main():
    DIR.mkdir(parents=True, exist_ok=True)
    idx = DIR / "index.md"
    if not idx.exists():
        idx.write_text("# Tool logos (official sources only — Tip 13)\n| file | tool site | file url | date |\n|---|---|---|---|\n", encoding="utf-8")
    today = datetime.date.today().isoformat()
    for name, site in SITES.items():
        if list(DIR.glob(name + ".*")):
            print("have", name); continue
        try:
            html, _, final = get(site)
            for u in icons(html.decode("utf-8", "ignore"), final):
                try:
                    data, ct, _ = get(u, 2_000_000)
                except Exception:
                    continue
                ext = "svg" if ("svg" in ct or u.split("?")[0].endswith(".svg")) else "png" if "png" in ct else "ico" if "icon" in ct or u.endswith(".ico") else "jpg" if "jpeg" in ct else None
                if ext and len(data) > 200:
                    (DIR / f"{name}.{ext}").write_bytes(data)
                    with idx.open("a", encoding="utf-8") as f:
                        f.write(f"| {name}.{ext} | {site} | {u} | {today} |\n")
                    print("got", name, ext, len(data)); break
            else:
                print("NO ICON", name, file=sys.stderr)
        except Exception as e:
            print("FAIL", name, type(e).__name__, e, file=sys.stderr)


if __name__ == "__main__":
    main()
