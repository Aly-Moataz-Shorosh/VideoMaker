"""English transcript with word times (tools/transcribe.py is Arabic-only).
Usage: python transcribe_en.py <media> <out_dir>"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding='utf-8')
media, out = sys.argv[1], Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', media, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                     capture_output=True, check=True).stdout
audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
model = WhisperModel(str(Path.home() / 'ai-models' / 'faster-whisper-large-v3-turbo'), device='cpu',
                     compute_type='int8', cpu_threads=10)
segs, _ = model.transcribe(audio, language='en', word_timestamps=True, beam_size=5,
                           initial_prompt='Garrett Warren, stunt coordinator, Avatar, James Cameron, Pandora, '
                                          'Na\'vi, banshee, motion capture, Grand Egyptian Museum.',
                           vad_filter=True, vad_parameters={'min_silence_duration_ms': 400, 'speech_pad_ms': 200},
                           condition_on_previous_text=False)
sents = []
for i, s in enumerate(segs, 1):
    ws = [{'w': w.word.strip(), 'start': round(w.start, 2), 'end': round(w.end, 2), 'p': round(w.probability, 2)}
          for w in (s.words or []) if w.word.strip()]
    sents.append({'id': f'S{i:03d}', 'start': round(s.start, 2), 'end': round(s.end, 2), 'text': s.text.strip(), 'words': ws})
    print(f'S{i:03d} {s.start:7.2f}-{s.end:7.2f} {s.text.strip()}', flush=True)
(out / 'transcript.json').write_text(json.dumps({'sentences': sents}, ensure_ascii=False, indent=1), encoding='utf-8')
(out / 'sents_timed.txt').write_text('\n'.join(f"{s['id']} {s['start']:.2f}-{s['end']:.2f} {s['text']}" for s in sents),
                                     encoding='utf-8')
