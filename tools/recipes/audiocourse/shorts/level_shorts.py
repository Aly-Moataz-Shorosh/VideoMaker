# Final loudness of the rendered shorts (gain only, his voice is not processed): body (before the end card) -> -16 LUFS, peak <= -1 dB.
# When his CTA clip is in (shorts_data.CTA_FILE), the CTA goes 1.5 dB UNDER the body (Aly 2026-10-18, Premiere series).
# Video re-encoded like Aly's own `ffmpeg -i in out` (libx264 CRF 23 + AAC) to keep shorts small.
#   python level_shorts.py 01_phone 02_explosion   (names in output/shorts/_raw)
import json, re, subprocess, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[2]
O = PROJ / 'output/shorts'


def lufs(args):
    r = subprocess.run(['ffmpeg'] + args + ['-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True, errors='ignore').stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])


def peak(f):
    r = subprocess.run(['ffmpeg', '-i', str(f), '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True, errors='ignore').stderr
    return float(re.findall(r'max_volume: (-?[\d.]+)', r)[0])


for nm in sys.argv[1:]:
    p = json.load(open(PROJ / f'work/shorts/props_{int(nm[:2]):02d}.json', encoding='utf-8'))
    ea = p['end']['at']
    raw, out = O / '_raw' / f'{nm}.mp4', O / f'{nm}.mp4'
    body = lufs(['-t', str(ea), '-i', str(raw)])
    cta = lufs(['-ss', str(p['cta']['at'] + 0.3), '-i', str(raw)]) if p.get('cta') else None
    trim = 0.0
    for _ in range(4):
        chain = [f"volume={-16 - body - trim:.2f}dB" + (f":enable='lt(t,{p['cta']['at']})'" if cta is not None else '')]
        if cta is not None: chain.append(f"volume={-17.5 - cta - trim:.2f}dB:enable='gte(t,{p['cta']['at']})'")
        tmp = out.with_suffix('.part.mp4')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-af', ','.join(chain), '-c:a', 'aac', '-b:a', '192k',
                        '-movflags', '+faststart', str(tmp)], check=True)
        pk = peak(tmp)
        if pk <= -1.0: break
        trim += pk + 1.0
    tmp.replace(out)  # written in one go (a half-written mp4 he might open = "broken file")
    print(nm, f'body {body:.1f} -> {-16 - trim:.1f} LUFS | peak {pk:.1f}' + (f' | cta {cta:.1f}' if cta is not None else ''))
