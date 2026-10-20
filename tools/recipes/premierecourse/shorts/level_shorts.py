# Final loudness of the rendered shorts (gain only, his voice is not processed):
#   body (before the CTA) -> -16 LUFS, CTA clip -> 1.5 dB UNDER the body (Aly 2026-10-18: "مش عايز صوتي في الـ CTA أعلى بكتير"),
#   true peak kept under -1 dB (whole short lowered if needed). DEESS = shorts where he asked for the harsh voice to be softened
#   (short 3): a gentle -4 dB high shelf at 6 kHz on the body only.
#   Video is re-encoded like Aly's own `ffmpeg -i in.mp4 out.mp4` (libx264 CRF 23 + AAC) to make the files small.
#   python level_shorts.py 01_green_screen 02_... (names in output/shorts/_raw)
import json, re, subprocess, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[2]
O = PROJ / 'output/shorts'
DEESS = {'03_fast_slow_freeze'}


def lufs(args):
    r = subprocess.run(['ffmpeg'] + args + ['-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True, errors='ignore').stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])


def peak(f):
    r = subprocess.run(['ffmpeg', '-i', str(f), '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True, errors='ignore').stderr
    return float(re.findall(r'max_volume: (-?[\d.]+)', r)[0])


for nm in sys.argv[1:]:
    no = int(nm[:2])
    p = json.load(open(PROJ / f'work/shorts/props_{no:02d}.json', encoding='utf-8'))
    ca = p['cta']['at']
    raw, out = O / '_raw' / f'{nm}.mp4', O / f'{nm}.mp4'
    body, cta = lufs(['-t', str(ca), '-i', str(raw)]), lufs(['-ss', str(ca + 0.3), '-i', str(raw)])
    trim = 0.0
    for _ in range(4):
        gb = -16 - body - trim
        gc = (-16 - 1.5) - cta - trim
        chain = [f"volume={gb:.2f}dB:enable='lt(t,{ca})'", f"volume={gc:.2f}dB:enable='gte(t,{ca})'"]
        if nm in DEESS:
            chain.insert(0, f"highshelf=f=6000:g=-4:enable='lt(t,{ca})'")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-af', ','.join(chain), '-c:a', 'aac',
                        '-movflags', '+faststart', str(out)], check=True)
        pk = peak(out)
        if pk <= -1.0: break
        trim += pk + 1.0
    print(nm, f'body {body:.1f} -> {-16 - trim:.1f} | cta {cta:.1f} -> {-17.5 - trim:.1f} | peak {pk:.1f}', '| de-essed' if nm in DEESS else '')
