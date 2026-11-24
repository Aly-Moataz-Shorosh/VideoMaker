"""Hear-check of the final v10 file with Whisper: the kids' separators Aly flagged (v9 notes 1/7/15/17/51), «عود» (52) and the CTA (56).
Usage (project folder): python -X utf8 work/scripts/qa_audio_v10.py"""
import json, subprocess, pathlib
import numpy as np
from faster_whisper import WhisperModel
T = json.load(open("work/timeline_v10.json", encoding="utf-8")); P = T["pieces"] if isinstance(T, dict) else T
want = []
for p in P:
    if p["kind"] == "gap" and any(k in p["sep"][1] for k in ("OPEN", "الأفاتار", "على جهازك", "LLM", "الأغنية")): want.append(("kids " + p["sep"][1], p["t"], p["dur"]))
    if p.get("sids") and ("S055.4" in p["sids"] or "N56_cta" in p["sids"]): want.append((p["sids"][0], p["t"], 8))
m = WhisperModel(str(pathlib.Path.home() / "ai-models" / "faster-whisper-large-v3-turbo"), device="cpu", compute_type="int8")
for name, t, d in want:
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-t", str(d), "-i", "output/rough_cut_v10.mp4", "-ac", "1", "-ar", "16000",
                                      "-f", "f32le", "-"], capture_output=True).stdout, np.float32)   # numpy in (this av build has no metadata_errors)
    segs, _ = m.transcribe(a, language="ar", beam_size=5)
    print(f"{t:8.1f} {name}: {' '.join(s.text.strip() for s in segs)}")
