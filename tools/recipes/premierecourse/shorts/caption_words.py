# Captions for a short: re-transcribe EACH piece on its own (short clean clip + a prompt with the Premiere terms), word times
# moved to the short's timeline. Then the per-short fix map (shorts_data.FIX[no]) corrects words before they reach the screen.
#   python caption_words.py 1 2     -> work/shorts/words_<NN>.json (+ words_<NN>.txt for reading)
import json, subprocess, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shorts_data as SD

PROJ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJ.parents[1] / 'tools'))
from faster_whisper import WhisperModel

PROMPT = 'كورس Premiere بالمصري. Premiere, Effects, Video Effects, Keying, Ultra Key, Key Color, Effect Controls, Opacity, Blend Mode, Multiply, layer, sequence, timeline, keyframe, green screen, slow motion, frame.'
local = Path.home() / 'ai-models' / 'faster-whisper-large-v3-turbo'
model = WhisperModel(str(local), device='cpu', compute_type='int8', cpu_threads=10)


def pcm(ep, a, b):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-to', str(b), '-i', str(PROJ / f'input/ep{ep}.mp4'), '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


for no in map(int, sys.argv[1:]):
    props = json.load(open(PROJ / f'work/shorts/props_{no:02d}.json', encoding='utf-8'))
    spec = SD.SHORTS[no]
    words, lines = [], []
    for v in props['voice']:
        a, b = v['from'], v['to']
        segs, _ = model.transcribe(pcm(int(v['file'].split('ep')[-1][0]), a, b), language='ar', beam_size=5, temperature=0, word_timestamps=True, initial_prompt=PROMPT, vad_filter=False)
        ws = [dict(w=w.word.strip(), start=round(v['at'] + w.start, 2), end=round(v['at'] + w.end, 2)) for s in segs for w in s.words if w.word.strip()]
        words += ws
        lines.append(f"{v['at']:.1f}  " + ' '.join(w['w'] for w in ws))
    json.dump(words, open(PROJ / f'work/shorts/words_{no:02d}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    (PROJ / f'work/shorts/words_{no:02d}.txt').write_text('\n'.join(lines), encoding='utf-8')
    print(no, len(words), 'words')
