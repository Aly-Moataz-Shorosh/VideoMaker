"""Re-transcribe stretches Whisper skipped/hallucinated (speech present) and splice them into transcript.json
as new sentences G1, G2 ... Usage: python fill_gaps.py <video> <transcript.json> a-b [a-b ...]"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'tools'))
sys.stdout.reconfigure(encoding='utf-8')
from transcribe import load_audio
from faster_whisper import WhisperModel

video, tp, ranges = sys.argv[1], sys.argv[2], [tuple(map(float, r.split('-'))) for r in sys.argv[3:]]
tr = json.load(open(tp, encoding='utf8'))
model = WhisperModel(str(Path.home() / 'ai-models' / 'faster-whisper-large-v3-turbo'), device='cpu', compute_type='int8', cpu_threads=10)
audio = load_audio(video)
prompt = 'فيديو يوتيوب باللهجة المصرية عن Figma Make و Claude و ChatGPT و UI UX ومشروع التخرج في جامعة حلوان.'
for k, (a, b) in enumerate(ranges, 1):
    segs, _ = model.transcribe(audio[int(a * 16000):int(b * 16000)], language='ar', word_timestamps=True, vad_filter=False,
                               initial_prompt=prompt, condition_on_previous_text=False, beam_size=5)
    ws = [{'w': w.word.strip(), 'start': round(a + w.start, 2), 'end': round(a + w.end, 2), 'p': round(w.probability, 2)}
          for s in segs for w in (s.words or []) if w.word.strip()]
    for s in tr['sentences']:
        s['words'] = [w for w in s['words'] if not (a <= w['start'] < b)]
    tr['sentences'].append({'id': f'G{k}', 'start': a, 'end': b, 'text': ' '.join(w['w'] for w in ws), 'words': ws})
    print(f'G{k} {a}-{b}:', ' '.join(f"{w['start']:.1f}|{w['w']}" for w in ws))
tr['sentences'] = sorted([s for s in tr['sentences'] if s['words']], key=lambda s: s['words'][0]['start'])
json.dump(tr, open(tp, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
