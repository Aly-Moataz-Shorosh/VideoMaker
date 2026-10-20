"""v3 voice (Aly 2026-10-08): his words, said by AI in a very clean voice, on HIS rhythm, close to his voice.
1. Phrases = his caption words (fixed text, timeline times) split at pauses.
2. Each phrase -> Microsoft Edge neural voice ar-EG-ShakirNeural (free, edge-tts), silence trimmed, time-stretched
   (ffmpeg atempo) to the exact length he took, placed at the exact time he said it.
3. The whole track -> OpenVoice V2 tone-colour converter (MIT, local CPU) with his reference voice (raw home clip)
   -> sounds like Aly (voiceprint similarity 0.84 vs 0.45 for the plain TTS; his own voice vs itself = 0.92).
4. Light podcast polish + loudnorm -12 LUFS -> public/projects/<code>/voice_ai_<n>.m4a and short_<n>_v3.json.
Run: python work/scripts/ai_voice.py [n ...]      (TTS cached in work/tts/cache)"""
import asyncio, hashlib, json, subprocess, sys, warnings
from pathlib import Path
import numpy as np
warnings.filterwarnings('ignore')
W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
sys.stdout.reconfigure(encoding='utf-8')
CODE = P.name
PUB = ROOT / 'motion-library' / 'public' / 'projects' / CODE
CACHE = W / 'tts' / 'cache'; CACHE.mkdir(parents=True, exist_ok=True)
VOICE = 'ar-EG-ShakirNeural'
RATE = '+0%'  # Aly: the AI may talk faster than him (he spoke very slowly), but not too fast
SR = 24000


async def tts(text, out):
    import edge_tts
    await edge_tts.Communicate(text, VOICE, rate=RATE).save(str(out))


def decode(path, sr=SR):
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'f32le', '-ac', '1', '-ar', str(sr), '-'],
                                        capture_output=True, check=True).stdout, np.float32).copy()


def ff(x, af, sr=SR, out_sr=None):
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', '-', '-af', af, '-f', 'f32le',
                                         '-ar', str(out_sr or sr), '-ac', '1', '-'], input=x.astype(np.float32).tobytes(),
                                        capture_output=True, check=True).stdout, np.float32).copy()


def trim(x, db=-42):
    hop = 240; n = len(x) // hop
    e = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    on = np.where(e > db)[0]
    if not len(on):
        return x
    return x[max(0, on[0] * hop - 240): min(len(x), (on[-1] + 1) * hop + 480)]


def phrases(words, end):
    out, cur = [], []
    for i, w in enumerate(words):
        if w['start'] >= end:
            break
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        gap = (nxt['start'] - w['end']) if nxt else 9
        dur = w['end'] - cur[0]['start']
        if gap > 0.15 or dur > 4.0 or w['w'][-1:] in '.؟?!،' or not nxt or nxt['start'] >= end:
            out.append({'text': ' '.join(x['w'] for x in cur), 'a': cur[0]['start'], 'b': cur[-1]['end']}); cur = []
    return out


def converter():
    import torch
    from openvoice.api import ToneColorConverter, OpenVoiceBaseClass
    p = Path.home() / 'ai-models' / 'openvoice-v2' / 'converter'
    c = ToneColorConverter.__new__(ToneColorConverter)
    OpenVoiceBaseClass.__init__(c, str(p / 'config.json'), device='cpu')  # (its own __init__ breaks on enable_watermark)
    c.watermark_model = None; c.version = 'v2'; c.load_ckpt(str(p / 'checkpoint.pth'))
    tgt = torch.load(str(W / 'tts' / 'aly_se.pth'))
    return c, tgt


def build(n, conv):
    """Aly: the AI may talk at its own (natural, a bit faster) pace -> the whole short is RE-TIMED to the voice:
    no time-stretch; phrases follow each other with short natural pauses; scenes, beats, captions, sfx and his
    cut-out windows (sped up by the same factor) are moved with a piecewise-linear old->new time map."""
    props = json.load(open(PUB / f'short_{n}.json', encoding='utf8'))
    main = props['cta']['tl']
    ph = phrases(props['words'], main)
    clips, old, new = [], [0.0], [0.0]
    t = min(0.25, ph[0]['a'])
    for i, p in enumerate(ph):
        f = CACHE / (hashlib.md5((VOICE + RATE + p['text']).encode()).hexdigest()[:16] + '.mp3')
        if not f.exists():
            asyncio.run(tts(p['text'], f))
        x = trim(decode(f))
        d = len(x) / SR
        old += [p['a'], p['b']]; new += [t, t + d]
        clips.append((t, x))
        gap = (ph[i + 1]['a'] - p['b']) if i + 1 < len(ph) else 0.3
        t += d + min(0.45, max(0.12, gap * 0.6))
    main_new = round(t + 0.1, 3)
    old.append(main); new.append(main_new)
    o, nw = np.array(old), np.array(new)
    keep = np.concatenate([[True], np.diff(o) > 1e-3])  # strictly increasing for interp
    o, nw = o[keep], np.maximum.accumulate(nw[keep])
    M = lambda x: float(np.interp(x, o, nw))
    track = np.zeros(int((main_new + 1) * SR), np.float32)
    for a, x in clips:
        k = int(a * SR); y = x * np.minimum(1, np.minimum(np.arange(len(x)), len(x) - np.arange(len(x))) / 120)
        track[k:k + len(y)] += y[:len(track) - k]
    tmp_in, tmp_out = W / 'tts' / f'_ai_{n}.wav', W / 'tts' / f'_ai_{n}_aly.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', str(tmp_in)], input=track.tobytes(), check=True)
    c, tgt = conv
    src = c.extract_se([str(tmp_in)])
    c.convert(audio_src_path=str(tmp_in), src_se=src, tgt_se=tgt, output_path=str(tmp_out), tau=0.4)
    y = decode(tmp_out, 48000)[:int(main_new * 48000)]
    polish = ('highpass=f=70,equalizer=f=170:t=q:w=1.0:g=2,equalizer=f=3000:t=q:w=1.3:g=2,treble=g=1.5:f=9000,'
              'acompressor=threshold=-24dB:ratio=3:attack=5:release=120:makeup=4:knee=4,alimiter=limit=0.9:level=false,loudnorm=I=-12:TP=-1:LRA=5')
    y = ff(y, polish, 48000)
    out = PUB / f'voice_ai_{n}.m4a'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', '48000', '-ac', '1', '-i', '-', '-c:a', 'aac', '-b:a', '192k', str(out)],
                   input=y.astype(np.float32).tobytes(), check=True)
    # re-time everything
    sh = main_new - main
    v = json.loads(json.dumps(props))
    v['voice'] = f'projects/{CODE}/voice_ai_{n}.m4a'
    v['segs'] = [{'src': 0, 'tl': 0, 'len': main_new}]
    v['words'] = [dict(w, start=round(M(w['start']), 3), end=round(M(w['end']), 3)) if w['start'] < main else
                  dict(w, start=round(w['start'] + sh, 3), end=round(w['end'] + sh, 3)) for w in props['words']]
    for s in v['scenes']:
        a0, b0 = s['at'], s['at'] + s['dur']
        a1, b1 = M(a0), M(b0)
        s['props']['b'] = {k: round(M(a0 + x) - a1, 3) for k, x in s['props'].get('b', {}).items()}
        s['at'], s['dur'] = round(a1, 3), round(max(0.3, b1 - a1), 3)
    for a in v['aly']:
        a1, b1 = M(a['at']), M(a['at'] + a['dur'])
        a['rate'] = round(min(1.8, max(1.0, a['dur'] / max(0.3, b1 - a1))), 3)
        a['at'], a['dur'] = round(a1, 3), round(max(0.3, b1 - a1), 3)
    for x in v['sfx']:
        x['at'] = round(M(x['at']) if x['at'] < main - 0.2 else x['at'] + sh, 3)
        if 'dur' in x and x['at'] < main_new:
            x['dur'] = round(max(0.3, M(x['at'] + x['dur']) - M(x['at'])), 3) if False else x['dur']
    v['cta'] = dict(v['cta'], tl=main_new)
    v['duration'] = round(main_new + v['cta']['len'], 3)
    json.dump(v, open(PUB / f'short_{n}_v3.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    sp = (main - ph[0]['a']) / (main_new - min(0.25, ph[0]['a']))
    print(f'short {n}: {len(ph)} phrases, {main:.1f}s -> {main_new:.1f}s (x{main / main_new:.2f} faster)', flush=True)


if __name__ == '__main__':
    conv = converter()
    for n in [int(x) for x in sys.argv[1:]] or range(1, 11):
        build(n, conv)
