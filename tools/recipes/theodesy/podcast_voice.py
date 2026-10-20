"""Podcast-style voice (Aly 2026-10-08: "not only noise — it doesn't sound like a podcast").
1. Facebook Denoiser dns64 (speech-trained, free, CPU) on the whole track at 16 kHz -> engine/room noise + echo gone.
2. Back to 48 kHz: the denoised voice below 7 kHz + the ORIGINAL highs (sibilance/air) above 6.5 kHz, gated by the
   denoised speech envelope (dns64 is 16 kHz only -> would sound dull without this).
3. Podcast chain (ffmpeg): rumble cut, warmth +, mud -, presence +, air +, de-esser, compressor, limiter, -14 LUFS.
Writes work/voice.m4a (same timing as final.mp4) + output/sample_podcast_{car,home}_{before,after}.m4a
Run: python work/scripts/podcast_voice.py"""
import glob, subprocess
from pathlib import Path
import numpy as np, torch
from denoiser import pretrained

W = Path(__file__).resolve().parents[1]; P = W.parent
SRC = glob.glob(str(P / 'input' / '*Odesy' / 'final.mp4'))[0]


def rd(path, sr):
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(sr), '-'],
                                        capture_output=True, check=True).stdout, np.float32).copy()


def ff_filter(x, sr, af):
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', '-', '-af', af,
                                         '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-'], input=x.astype(np.float32).tobytes(),
                                        capture_output=True, check=True).stdout, np.float32).copy()


# 1. denoise in 30 s chunks with 1 s overlap (cross-faded); cached in work/voice_dns16.npy
CACHE = W / 'voice_dns16.npy'
x16 = rd(SRC, 16000)
model = pretrained.dns64().eval()
CH, OV = 30 * 16000, 16000
out = np.zeros_like(x16); wsum = np.zeros_like(x16)
with torch.no_grad():
    for a in ([] if CACHE.exists() else range(0, len(x16), CH - OV)):
        seg = x16[a:a + CH]
        y = model(torch.from_numpy(seg)[None, None])[0, 0].numpy()[:len(seg)]
        w = np.ones(len(seg), np.float32)
        r = min(OV, len(seg))
        w[:r] = np.linspace(0, 1, r) if a else 1
        w[-r:] = np.minimum(w[-r:], np.linspace(1, 0, r)) if a + CH < len(x16) else w[-r:]
        out[a:a + len(seg)] += y * w; wsum[a:a + len(seg)] += w
        print(f'denoise {a / 16000:.0f}s / {len(x16) / 16000:.0f}s', flush=True)
d16 = np.load(CACHE) if CACHE.exists() else out / np.maximum(wsum, 1e-6)
np.save(CACHE, d16)

# 2. back to 48 kHz + gated original highs
SR = 48000
d48 = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', '16000', '-ac', '1', '-i', '-', '-af', 'aresample=48000:resampler=soxr',
                                    '-f', 'f32le', '-ar', '48000', '-ac', '1', '-'], input=d16.astype(np.float32).tobytes(),
                                   capture_output=True, check=True).stdout, np.float32).copy()
o48 = rd(SRC, SR)
n = min(len(d48), len(o48)); d48, o48 = d48[:n], o48[:n]
hop = 480  # 10 ms
env = np.sqrt(np.convolve(np.pad(d48 ** 2, (0, (-n) % hop)).reshape(-1, hop).mean(1), np.ones(5) / 5, 'same')) + 1e-9
g = np.clip((20 * np.log10(env) + 48) / 14, 0, 1)
g = np.repeat(g, hop)[:n]
hf = ff_filter(o48, SR, 'highpass=f=6500:poles=2,highpass=f=6500:poles=2') * g * 0.8
lo = ff_filter(d48, SR, 'lowpass=f=7200:poles=2')
mix = lo + hf

# 3. podcast chain
# Aly: "the voice is low and far" -> closer (warmth + presence, dns64 already removed the room echo), harder compression,
# louder master (-12 LUFS, typical for shorts/reels).
CHAIN = ('highpass=f=75,equalizer=f=160:t=q:w=1.0:g=3.5,equalizer=f=420:t=q:w=1.3:g=-3.5,equalizer=f=2800:t=q:w=1.3:g=3.5,'
         'equalizer=f=5000:t=q:w=1.5:g=1.5,treble=g=2.5:f=9500,deesser=i=0.6:m=0.5:f=0.5,'
         'acompressor=threshold=-28dB:ratio=4:attack=5:release=120:makeup=6:knee=4,'
         'acompressor=threshold=-12dB:ratio=2.5:attack=2:release=60:makeup=1,alimiter=limit=0.9:level=false,'
         'loudnorm=I=-12:TP=-1:LRA=5')
final = ff_filter(mix, SR, CHAIN)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'aac', '-b:a', '192k',
                str(W / 'voice.m4a')], input=final.astype(np.float32).tobytes(), check=True)
(P / 'output').mkdir(exist_ok=True)
for name, t in (('car', 95), ('home', 700)):
    for tag, src in (('before', SRC), ('after', str(W / 'voice.m4a'))):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-t', '15', '-i', src, '-vn', '-c:a', 'aac', '-b:a', '192k',
                        str(P / 'output' / f'sample_podcast_{name}_{tag}.m4a')], check=True)
print('voice.m4a done', round(n / SR, 1), 's')
