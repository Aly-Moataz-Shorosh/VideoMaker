"""v10 note 7: REAL word times of the voice track (Whisper large-v3-turbo, word timestamps) -> work/whisper_words_v11.json.
Logos / items «on their word» use these, never the script-order guesses. Usage (project folder): python -X utf8 work/scripts/whisper_words_v11.py"""
import json, subprocess, pathlib, numpy as np
from faster_whisper import WhisperModel
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "output/audio_stems_v11/voice_full_timeline.wav", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                 capture_output=True).stdout, np.float32)
m = WhisperModel(str(pathlib.Path.home() / "ai-models" / "faster-whisper-large-v3-turbo"), device="cpu", compute_type="int8")
segs, _ = m.transcribe(a, language="ar", beam_size=5, word_timestamps=True, vad_filter=True, condition_on_previous_text=False)
out = [{"w": w.word.strip(), "a": round(w.start, 3), "b": round(w.end, 3)} for s in segs for w in s.words]
json.dump(out, open("work/whisper_words_v11.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(out), "words")
