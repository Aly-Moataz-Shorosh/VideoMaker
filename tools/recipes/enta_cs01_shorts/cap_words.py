"""Re-transcribe every piece of a short alone (better words than the long pass) -> work/shorts/words_NN.json + .txt
The .txt is what I read to write the corrected caption text (CAP in shorts_data.py).
Usage: python cap_words.py 1 2 3"""
import json, sys
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
sys.stdout.reconfigure(encoding='utf-8')
HERE = Path(__file__).parent
P = HERE.parents[1]
sys.path.insert(0, str(P.parents[2] / 'tools'))
from transcribe import load_audio
from shorts_data import SHORTS
from edges import fit

PROMPT = 'حلقة بودكاست باللهجة المصرية عن Software Testing و QA و QC و Automation و API و Postman و ISTQB و AI و Developer و Bugs و Requirements. علي شرش وأيمن إسماعيل.'
OUT = P / 'work' / 'shorts'
OUT.mkdir(exist_ok=True)
cache = P / 'work' / 'audio16k.npy'
if cache.exists():
    audio = np.load(cache)
else:
    audio = load_audio(str(P / 'input' / 'main video.mp4')); np.save(cache, audio)
model = WhisperModel(str(Path.home() / 'ai-models' / 'faster-whisper-large-v3-turbo'), device='cpu', compute_type='int8', cpu_threads=10)

for n in map(int, sys.argv[1:]):
    sh = SHORTS[n]
    res, txt = [], []
    for i, (a, b, *x) in enumerate([sh['hook']] + sh['pieces']):
        s, e = (a, b) if x else fit(a, b)[:2]
        segs, _ = model.transcribe(audio[int(s * 16000):int(e * 16000)], language='ar', word_timestamps=True, initial_prompt=PROMPT,
                                   vad_filter=False, condition_on_previous_text=False, beam_size=5)
        ws = [{'w': w.word.strip(), 'start': round(s + w.start, 2), 'end': round(s + w.end, 2)} for g in segs for w in (g.words or []) if w.word.strip()]
        res.append({'piece': i, 'a': s, 'b': e, 'words': ws})
        txt.append(f"P{i} {s:.2f}-{e:.2f}: " + ' '.join(w['w'] for w in ws))
    json.dump(res, open(OUT / f'words_{n:02d}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    (OUT / f'words_{n:02d}.txt').write_text('\n'.join(txt), encoding='utf8')
    print(f'--- short {n}'); print('\n'.join(txt))
