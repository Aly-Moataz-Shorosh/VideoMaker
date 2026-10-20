"""Second independent ASR pass for the raw reel source."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "projects/1-test 1/input/20261001_192249.mp4"
OUT = ROOT / "projects/1-test 1/work/short_v02/asr_independent"
MODEL = next((ROOT / "tools/models-direct/models--Systran--faster-whisper-base/snapshots").glob("*/model.bin")).parent

sys.path.insert(0, str(ROOT / "tools/py"))
os.environ["HF_HUB_OFFLINE"] = "1"
from faster_whisper import WhisperModel  # noqa: E402


def stamp(seconds: float) -> str:
    millis = round(seconds * 1000)
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    model = WhisperModel(str(MODEL), device="cpu", compute_type="int8")
    prompt = (
        "شرح عربي مصري لبرنامج DaVinci Resolve. المصطلحات: Ripple Delete Silence، "
        "Audio Transcription، Silence Threshold، Pre-Roll، Post-Roll، Minimum Strip، "
        "Crossfade، Timeline، Export XML، Premiere Pro."
    )
    iterator, info = model.transcribe(
        str(SOURCE), language="ar", beam_size=10, best_of=5,
        vad_filter=False, word_timestamps=True, condition_on_previous_text=False,
        initial_prompt=prompt, temperature=0,
    )
    segments = []
    for segment in iterator:
        item = {
            "start": round(segment.start, 3),
            "end": round(segment.end, 3),
            "text": segment.text.strip(),
            "words": [
                {
                    "start": round(word.start, 3) if word.start is not None else None,
                    "end": round(word.end, 3) if word.end is not None else None,
                    "word": word.word,
                    "probability": round(word.probability, 4),
                }
                for word in (segment.words or [])
            ],
        }
        segments.append(item)
        print(f"{item['start']:7.2f}-{item['end']:7.2f} {item['text']}", flush=True)
    payload = {
        "source": str(SOURCE),
        "model": str(MODEL),
        "language": info.language,
        "duration": round(info.duration, 3),
        "status": "independent_machine_transcript_requires_editorial_review",
        "segments": segments,
    }
    (OUT / "raw_second_pass.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (OUT / "raw_second_pass.srt").open("w", encoding="utf-8-sig", newline="\n") as handle:
        for number, item in enumerate(segments, 1):
            handle.write(f"{number}\n{stamp(item['start'])} --> {stamp(item['end'])}\n{item['text']}\n\n")


if __name__ == "__main__":
    main()
