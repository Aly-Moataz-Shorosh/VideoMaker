# Re-transcribe only the kept ranges with an English-terms prompt (first pass dropped Clip/Threshold/...).
import json, sys
sys.path.insert(0, 'tools')
from transcribe import load_audio
from faster_whisper import WhisperModel
from pathlib import Path
P = Path('projects/2026-10-06 shorts RippleCutToll')
KEEP = json.load(open(P / 'work/plan.json', encoding='utf8'))['keep']
m = WhisperModel(str(Path.home() / 'ai-models/faster-whisper-large-v3-turbo'), device='cpu', compute_type='int8', cpu_threads=10)
a = load_audio(str(P / 'input/delete_silence_edit.mp4'))
PR = 'DaVinci Resolve: Clip, Audio Operations, Ripple Delete Silence, Threshold, Pre head, Post tail, Minimum to strip, Cross fade audio. فيديو باللهجة المصرية.'
sents = []
for k, (s, e) in enumerate(KEEP, 1):
    segs, _ = m.transcribe(a[int((s - 1.5) * 16000):int((e + 1.0) * 16000)], language='ar', word_timestamps=True,
                           initial_prompt=PR, beam_size=5, condition_on_previous_text=False)
    ws = [{'w': w.word.strip(), 'start': round(s - 1.5 + w.start, 2), 'end': round(s - 1.5 + w.end, 2), 'p': round(w.probability, 2)}
          for sg in segs for w in sg.words if w.word.strip()]
    ws = [w for w in ws if s <= (w['start'] + w['end']) / 2 < e]  # word midpoint inside the range
    sents.append({'id': f'K{k:02d}', 'start': s, 'end': e, 'text': ' '.join(w['w'] for w in ws), 'words': ws})
    print(f'K{k:02d} {s}-{e} ({len(ws)}w): ' + ' '.join(f"{i}:{w['w']}" for i, w in enumerate(ws)))
full = json.load(open(P / 'work/transcript_full.json', encoding='utf8'))
json.dump({'duration': full['duration'], 'sentences': sents, 'note': 'kept ranges only; full = transcript_full.json'},
          open(P / 'work/transcript.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
