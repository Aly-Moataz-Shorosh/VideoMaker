"""Align his CLEAN voice file of every هو ايه episode to the published episode (envelope cross-correlation).
Prints one offset per episode (voice_t = video_t + off) and the 3 s window check (all windows must agree; else the edit cut it).
Writes work/huwa_voice.json -> used by jy_audio.VOICE."""
import glob, json, subprocess, sys
from pathlib import Path
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
P = Path(__file__).resolve().parents[2]
V = P / 'assets' / 'his' / 'huwa_voice'
FILES = {'02': 'software app.mp3', '03': 'plugins & addons.mp3', '04': 'opensource.mp3', '05': '3- eco system FIXED.mp3', '06': '4- adobe FIXED.mp3',
         '07': '5-pixels FIXED.mp3', '08': '6-vectors FIXED.mp3', '09': '7-compositing FIXED.mp3', '10': '8-photo editing FIXED.mp3',
         '11': '9-mock up FIXED.mp3', '12': '10-RGB & CYMK FIXED.mp3', '13': '12-resolution FIXED.mp3', '14': '13-modeling FIXED.mp3',
         '15': '14-materials FIXED.mp3', '16': '15-lighting FIXED.mp3', '17': '16- 3D sculpting FIXED.mp3', '18': '17-rendering FIXED.mp3',
         '19': '18-rigging FIXED.mp3', '20': '19-animating FIXED.mp3', '21': '20-physics FIXED.mp3', '22': '21-simulations FIXED mp3.mp3',
         '23': '22-THIS - keying and rotoscoping FIXED.mp3', '24': '23-matte painting FIXED.mp3', '25': '24-cgi FIXED.mp3', '26': '25-vfx FIXED.mp3',
         '27': '26-SFX FIXED.mp3', '28': '27-motion tracking FIXED.mp3', '29': '28-video editing FIXED.mp3', '30': '29-video compositing FIXED.mp3',
         '31': '30-node based vs layer based FIXED.mp3'}


def env(f, sr=8000):
    a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'], capture_output=True).stdout, np.int16).astype(np.float32)
    h = sr // 100; n = len(a) // h
    return np.log(np.sqrt((a[:n * h].reshape(n, h) ** 2).mean(1)) + 1)


out = {}
for ep, fn in FILES.items():
    a = env(glob.glob(str(P / 'input' / f'{ep}_*.mp4'))[0]); b = env(V / fn)
    an = (a - a.mean()) / a.std(); bn = (b - b.mean()) / b.std()
    c = np.correlate(an, bn, 'full'); k = int(np.argmax(c)) - (len(b) - 1)  # video index = voice index + k
    off = -k / 100
    # window check
    bad = []
    for t in range(3, int(len(a) / 100) - 4, 3):
        s = t * 100; seg = a[s:s + 300]; o = s + int(round(off * 100)); w = b[o:o + 300]
        if o < 0 or len(w) < 300 or seg.std() < 0.2:
            continue
        cc = np.corrcoef(seg, w)[0, 1]
        if cc < 0.6:
            bad.append((t, round(float(cc), 2)))
    out[ep] = {'file': f'assets/his/huwa_voice/{fn}', 'off': round(off, 2)}
    print(ep, fn, 'off', round(off, 2), 'weak windows:', bad[:6])
json.dump(out, open(P / 'work' / 'huwa_voice.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
