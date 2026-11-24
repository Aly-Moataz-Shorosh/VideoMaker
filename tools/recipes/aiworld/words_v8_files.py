"""Word times for the FILE pieces of timeline v6 (re-voices + new narration): Whisper gives the times, the SCRIPT gives the text
(so captions say «قطعة» even when the voice file was written «أطعة», and «3D» stays 3D). Merges with the v2-part words → work/words_v8.json.
Usage (project folder): python -X utf8 work/scripts/words_v6_files.py"""
import json, re, subprocess
import numpy as np
from faster_whisper import WhisperModel

T = json.load(open("work/timeline_v8.json", encoding="utf-8")); W = json.load(open("work/_words_v8_v2part.json", encoding="utf-8"))
S = {s["id"]: s["t"] for s in json.load(open("work/sentences_v3.json", encoding="utf-8"))}
CAP = {"S003.5": "صور وفيديو وصوت ومزيكا و3D.", "S016.1": "الـ 3D دلوقتي ممكن يبدأ من صورة:", "S016.2": "تدي صورة لحاجة، يطلعلك موديل 3D تقدر تلف حواليه.",
       "S016.5": "وفيه طريقة اسمها Gaussian splats بتحول تصوير مكان حقيقي لمشهد 3D.",
       "S033.3": "Remotion للموشن، وthree.js للـ 3D، وffmpeg للقص والتجميع، وBlender بالبايثون، وWhisper للكلام.",
       "S005.4": "الأداة هي الموقع اللي بتكتب فيه، زي Higgsfield أو Magnific.", "S007.2": "كلام مكتوب يبقى صورة، وصورة تبقى صورة.",
       "S009.2": "كلام مكتوب يبقى فيديو، وصورة تبقى فيديو،", "S009.2b": "وأقوى حاجة:"}
nar = open("narration_v6_new.md", encoding="utf-8").read()
for k, h in (("N1", "### N1"), ("N2", "### N2"), ("N3", "### N3")):
    blk = nar.split(h, 1)[1].split("\n", 1)[1].split("\n###", 1)[0].split("\n## ", 1)[0].strip()
    CAP[k] = blk.replace(".mcp.json", "mcp.json").replace("/mcp", "mcp")
    if k == "N2":   # v8 note 41: that sentence was cut from the voice
        import re as _re; CAP[k] = _re.sub(r"وفي Claude Code:.*?وأمر mcp\.\s*", "", CAP[k])
M = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
for p in T["pieces"]:
    if p["kind"] != "file": continue
    sid = p["sids"][0]; text = CAP.get(sid) or S[sid]
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", str(p["a"]), "-to", str(p["b"]), "-i", p["f"], "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    segs, _ = M.transcribe(a, language="ar", word_timestamps=True, vad_filter=False, initial_prompt=text[:200])
    ww = [(w.start, w.end) for s_ in segs for w in s_.words]
    sw = text.split()
    for i, w in enumerate(sw):   # script word i takes the time of the whisper word at the same relative place
        j = min(len(ww) - 1, int(round(i * (len(ww) - 1) / max(1, len(sw) - 1)))) if ww else None
        st, en = ww[j] if ww else (i * (p["b"] - p["a"]) / len(sw), (i + 1) * (p["b"] - p["a"]) / len(sw))
        W.append({"w": w, "a": round(p["t"] + st, 3), "b": round(p["t"] + en, 3), "sid": sid})
    print(sid, len(sw), "script words /", len(ww), "heard")
W.sort(key=lambda w: w["a"])
json.dump(W, open("work/words_v8.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(W), "words")
