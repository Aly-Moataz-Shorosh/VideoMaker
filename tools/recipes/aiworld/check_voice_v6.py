"""Listen to the v6 re-voices with Whisper (Arabic + English passes) so we know HOW a word was said (3D, قطعة, القاعدة).
Usage: python -X utf8 work/scripts/check_voice_v6.py file.wav [file.wav ...]"""
import subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

M = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
for f in sys.argv[1:]:
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    for lang in ("ar", "en"):
        s, _ = M.transcribe(a, language=lang, word_timestamps=True, vad_filter=False)
        print(f.split("/")[-1], lang, " ".join(f"{w.word.strip()}@{w.start:.2f}" for x in s for w in x.words))
