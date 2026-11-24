"""timeline_v1.json + shotlist_v1.json -> props_rough_v1.json for Remotion `ai-world-rough` (25 fps, 16:9)."""
import json
from pathlib import Path
W = Path(__file__).resolve().parent.parent
tl = json.loads((W / "timeline_v1.json").read_text(encoding="utf-8"))
shots = json.loads((W / "shotlist_v1.json").read_text(encoding="utf-8"))
caps = []
for ch in tl["chapters"]:
    for s in ch["segments"]:
        if not s["words"]:
            continue
        w = s["text"].split(); per = s["dur"] / len(w)
        for i in range(0, len(w), 6):
            g = w[i:i + 6]
            caps.append({"a": round(s["start"] + i * per, 2), "b": round(s["start"] + (i + len(g)) * per, 2), "t": " ".join(g)})
chs = [{"id": c["id"], "title": c["title"], "start": c["start"], "end": c["end"]} for c in tl["chapters"]]
for s in shots:
    s["cost"] = str(s["cost"])
props = {"fps": 25, "duration": tl["total"], "shots": shots, "caps": caps, "chapters": chs}
(W / "props_rough_v1.json").write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")
print("props", len(shots), "shots", len(caps), "caps", tl["total"], "s")
