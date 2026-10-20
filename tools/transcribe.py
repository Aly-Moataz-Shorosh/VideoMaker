"""Transcribe Aly's video (Egyptian Arabic) with word timestamps, free & local (faster-whisper, CPU).

Usage: python tools/transcribe.py <media> <work_dir> [--model large-v3-turbo] [--prompt 'Figma, Claude']
Writes: transcript.json  {duration, sentences:[{id,start,end,text,words:[{w,start,end,p}]}], gaps:[...]}
        sentences.txt    "S001 text" per line  (this is what the LLM reads — no timestamps)
Gap check: any silence-free stretch the model skipped (>4 s with audio energy) is listed so text is never
silently lost (Codex v01 lost 115 s this way).
"""
import json, subprocess, sys, time
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

PROMPT = 'فيديو يوتيوب باللهجة المصرية. علي شرش بيشرح. Premiere, DaVinci, After Effects, AI.'


def load_audio(path, sr=16000):
    # Decode with ffmpeg ourselves (PyAV inside faster-whisper breaks with some av versions).
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def audio_energy(a, sr=16000):
    win = sr // 10  # 100 ms
    n = len(a) // win
    rms = np.sqrt((a[: n * win].reshape(n, win) ** 2).mean(1))
    return rms, len(a) / sr


def main():
    sys.stdout.reconfigure(encoding='utf-8')  # Windows console is cp1252 -> Arabic print crashed
    media, work = sys.argv[1], Path(sys.argv[2])
    model_name = sys.argv[sys.argv.index('--model') + 1] if '--model' in sys.argv else 'large-v3-turbo'
    global PROMPT
    if '--prompt' in sys.argv:  # extra terms for this video (English names Whisper should spell)
        PROMPT = PROMPT + ' ' + sys.argv[sys.argv.index('--prompt') + 1]
    work.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    # Windows blocks HF cache symlinks -> download once into a plain folder (C:, E: is nearly full).
    local = Path.home() / 'ai-models' / f'faster-whisper-{model_name}'
    if not (local / 'model.bin').exists():
        from huggingface_hub import snapshot_download
        repo = 'mobiuslabsgmbh/faster-whisper-large-v3-turbo' if model_name == 'large-v3-turbo' else f'Systran/faster-whisper-{model_name}'
        snapshot_download(repo, local_dir=str(local))
    model = WhisperModel(str(local), device='cpu', compute_type='int8', cpu_threads=10)
    audio = load_audio(media)
    segs, info = model.transcribe(audio, language='ar', word_timestamps=True, initial_prompt=PROMPT,
                                  vad_filter=True, vad_parameters={'min_silence_duration_ms': 400, 'speech_pad_ms': 200},
                                  condition_on_previous_text=False, beam_size=5)
    sentences = []
    for i, s in enumerate(segs, 1):
        words = [{'w': w.word.strip(), 'start': round(w.start, 2), 'end': round(w.end, 2), 'p': round(w.probability, 2)}
                 for w in (s.words or []) if w.word.strip()]
        sentences.append({'id': f'S{i:03d}', 'start': round(s.start, 2), 'end': round(s.end, 2),
                          'text': s.text.strip(), 'words': words})
        print(f'S{i:03d} {s.start:7.1f} {s.text.strip()[:70]}', flush=True)

    # Second pass: re-transcribe weak stretches (mean word prob < 0.55) without VAD/prompt; keep if better.
    def mean_p(ws):
        return sum(w['p'] for w in ws) / max(1, len(ws))
    redo = 0
    for k, sn in enumerate(sentences):
        if mean_p(sn['words']) >= 0.55 or sn['end'] - sn['start'] < 1:
            continue
        a, b = int(sn['start'] * 16000), int(sn['end'] * 16000)
        alt, _ = model.transcribe(audio[a:b], language='ar', word_timestamps=True, vad_filter=False,
                                  condition_on_previous_text=False, beam_size=5, temperature=[0.0, 0.2, 0.4])
        ws, txt = [], []
        for seg in alt:
            txt.append(seg.text.strip())
            ws += [{'w': w.word.strip(), 'start': round(sn['start'] + w.start, 2), 'end': round(sn['start'] + w.end, 2),
                    'p': round(w.probability, 2)} for w in (seg.words or []) if w.word.strip()]
        if ws and mean_p(ws) > mean_p(sn['words']) + 0.1:
            sn.update(words=ws, text=' '.join(txt), redo=True); redo += 1
        if mean_p(sn['words']) < 0.55:
            sn['lowConfidence'] = True  # plan step: treat text as unreliable, decide by context/time only
    print(f'second pass improved {redo} sentences')

    # Gap check: loud stretches (> 4 s) not covered by any sentence.
    rms, dur = audio_energy(audio)
    covered = np.zeros(len(rms), bool)
    for s in sentences:
        covered[int(s['start'] * 10): int(s['end'] * 10) + 1] = True
    loud = rms > max(0.02, np.percentile(rms, 60) * 0.6)
    gaps, start = [], None
    for k, (l, c) in enumerate(zip(loud, covered)):
        if l and not c:
            start = k if start is None else start
        elif start is not None:
            if (k - start) / 10 > 4:
                gaps.append({'start': start / 10, 'end': k / 10})
            start = None
    json.dump({'media': str(media), 'model': model_name, 'duration': round(dur, 2), 'sentences': sentences, 'gaps': gaps},
              open(work / 'transcript.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    (work / 'sentences.txt').write_text('\n'.join(f"{s['id']}{' [?]' if s.get('lowConfidence') else ''} {s['text']}"
                                                  for s in sentences), encoding='utf8')
    print(f'\n{len(sentences)} sentences, {dur:.0f}s audio, {time.time() - t0:.0f}s wall. GAPS (>4s loud, untranscribed): {gaps or "none"}')


if __name__ == '__main__':
    main()
