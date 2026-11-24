"""narration_v1.md -> timeline_v1.json + chapters_v1.txt + captions_v1.srt (ESTIMATED timing).
Estimate = words / WPS + GAP between segments. Replace with Whisper timings when the real voice exists
(tools/transcribe.py on the voice wav -> rerun with --whisper <json>)."""
import json, re, sys
from pathlib import Path

WPS = 2.2      # Egyptian Arabic narration, calm pace (words per second)
GAP = 0.4      # pause between segments
HERE = Path(__file__).resolve().parent.parent  # work/
src = HERE / "narration_v1.md"

chapters, cur, seg = [], None, None
for line in src.read_text(encoding="utf-8").splitlines():
    if line.startswith("## "):
        cid, title = [x.strip() for x in line[3:].split("|", 1)]
        cur = {"id": cid, "title": title, "segments": []}
        chapters.append(cur)
    elif line.startswith("### "):
        seg = {"id": line[4:].strip(), "text": ""}
        cur["segments"].append(seg)
    elif seg is not None and line.strip() and not line.startswith(">"):
        seg["text"] += (" " if seg["text"] else "") + line.strip()

t = 0.0
for ch in chapters:
    ch["start"] = round(t, 2)
    for s in ch["segments"]:
        m = re.match(r"\[MUSIC (\d+)\]", s["text"])
        words = s["text"].split()
        s["words"] = 0 if m else len(words)
        s["dur"] = float(m.group(1)) if m else round(len(words) / WPS, 2)
        s["start"] = round(t, 2)
        t += s["dur"] + GAP
        s["end"] = round(s["start"] + s["dur"], 2)
    ch["end"] = round(t, 2)
total = round(t, 2)

def mmss(x):
    x = int(x)
    return f"{x//3600}:{x%3600//60:02d}:{x%60:02d}" if x >= 3600 else f"{x//60}:{x%60:02d}"

(HERE / "timeline_v1.json").write_text(json.dumps({"wps": WPS, "gap": GAP, "total": total, "chapters": chapters},
                                                  ensure_ascii=False, indent=1), encoding="utf-8")
# YouTube chapters: first must be 0:00, each >= 10 s
lines = [f"{mmss(c['start'])} {c['title']}" for c in chapters]
(HERE / "chapters_v1.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

# captions: groups of <= 6 words, time split by word count inside each segment
def ts(x):
    ms = int(round(x * 1000))
    return f"{ms//3600000:02d}:{ms%3600000//60000:02d}:{ms%60000//1000:02d},{ms%1000:03d}"
srt, n = [], 0
for ch in chapters:
    for s in ch["segments"]:
        if not s["words"]:
            continue
        w = s["text"].split()
        per = s["dur"] / len(w)
        for i in range(0, len(w), 6):
            g = w[i:i+6]
            n += 1
            a = s["start"] + i * per
            b = a + len(g) * per
            srt.append(f"{n}\n{ts(a)} --> {ts(b)}\n{' '.join(g)}\n")
(HERE / "captions_v1.srt").write_text("\n".join(srt), encoding="utf-8")

words = sum(s["words"] for c in chapters for s in c["segments"])
print(f"chapters {len(chapters)}  segments {sum(len(c['segments']) for c in chapters)}  words {words}  total {mmss(total)} ({total}s)")
for c in chapters:
    print(f"  {mmss(c['start']):>6}  {c['id']:5} {c['end']-c['start']:6.1f}s  {c['title']}")
over = [s["id"] for c in chapters for s in c["segments"] if s["dur"] > 60 and s["words"]]
print("segments > 60 s:", over or "none")
