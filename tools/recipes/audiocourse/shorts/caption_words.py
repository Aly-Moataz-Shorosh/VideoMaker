# Captions for a short: re-transcribe EACH piece on its own (short clean clip + a prompt with the audio terms), word times moved to the
# short's timeline. Read words_<NN>.txt, then write the corrected lines in shorts_data.CAP (never words he didn't say).
#   python caption_words.py 1 2     -> work/shorts/words_<NN>.json + words_<NN>.txt
import json, subprocess, sys
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

PROJ = Path(__file__).resolve().parents[2]
SRC = PROJ / 'input/2021-03-28 20-26-18_1.mp4'
PROMPT = 'كورس الصوت بالمصري. Premiere, Audition, Essential Sound, Dialogue, Preset, From the Telephone, Podcast, Effects, GuitarSuite, Explosion, SFX, Noise Reduction, Capture Noise Print, sample rate, bit depth, mic.'
model = WhisperModel(str(Path.home() / 'ai-models' / 'faster-whisper-large-v3-turbo'), device='cpu', compute_type='int8', cpu_threads=10)


def pcm(a, b):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-to', str(b), '-i', str(SRC), '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


for no in map(int, sys.argv[1:]):
    props = json.load(open(PROJ / f'work/shorts/props_{no:02d}.json', encoding='utf-8'))
    words, lines = [], []
    for v in props['voice']:
        segs, _ = model.transcribe(pcm(v['from'], v['to']), language='ar', beam_size=5, temperature=0, word_timestamps=True, initial_prompt=PROMPT, vad_filter=False)
        ws = [dict(w=w.word.strip(), start=round(v['at'] + w.start, 2), end=round(v['at'] + w.end, 2)) for s in segs for w in s.words if w.word.strip()]
        words += ws
        lines.append(f"{v['at']:.1f}  " + ' '.join(w['w'] for w in ws))
    json.dump(words, open(PROJ / f'work/shorts/words_{no:02d}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    (PROJ / f'work/shorts/words_{no:02d}.txt').write_text('\n'.join(lines), encoding='utf-8')
    print(no, len(words), 'words')
