from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from audit_edit_plan import uncovered_ranges


def srt_time(seconds: float) -> str:
    milliseconds = max(0, round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Transcribe project media with faster-whisper.")
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--model", default="small")
    parser.add_argument("--model-dir", type=Path, required=True)
    args = parser.parse_args()

    local_packages = Path(__file__).resolve().parents[1] / "tools" / "py"
    sys.path.insert(0, str(local_packages))
    os.environ.setdefault("HF_HOME", str(args.model_dir))

    from faster_whisper import WhisperModel

    args.output_dir.mkdir(parents=True, exist_ok=True)
    model = WhisperModel(
        args.model,
        device="cpu",
        compute_type="int8",
        download_root=str(args.model_dir),
    )

    media = sorted(p for p in args.input_dir.iterdir() if p.suffix.lower() in {".mp4", ".mov", ".mkv", ".wav", ".mp3"})
    for path in media:
        print(f"Transcribing: {path.name}", flush=True)
        segments_iter, info = model.transcribe(
            str(path),
            language="ar",
            beam_size=5,
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 350},
            word_timestamps=True,
            condition_on_previous_text=True,
        )
        segments = []
        for segment in segments_iter:
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
            print(f"  {item['start']:7.2f}-{item['end']:7.2f} {item['text']}", flush=True)

        payload = {
            "source": str(path.resolve()),
            "language": info.language,
            "language_probability": round(info.language_probability, 4),
            "duration": round(info.duration, 3),
            "segments": segments,
            "review_status": "unreviewed_machine_transcript_not_an_edit_decision",
            "untranscribed_ranges": uncovered_ranges(segments, float(info.duration)),
        }
        if payload["untranscribed_ranges"]:
            print("REVIEW REQUIRED: untranscribed ranges are NOT proof of silence: "
                  + json.dumps(payload["untranscribed_ranges"]), flush=True)
        stem = path.stem
        (args.output_dir / f"{stem}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        with (args.output_dir / f"{stem}.srt").open("w", encoding="utf-8-sig", newline="\n") as srt:
            for index, segment in enumerate(segments, start=1):
                srt.write(f"{index}\n{srt_time(segment['start'])} --> {srt_time(segment['end'])}\n{segment['text']}\n\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
