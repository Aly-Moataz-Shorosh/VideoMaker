"""Final pass (gain only, his voice untouched): whole short -16 LUFS, true peak <= -1 dB, compressed like Aly's
`ffmpeg -i in out` (x264 CRF 23 + AAC; shorts are always compressed). output/shorts/_raw/NN.mp4 -> output/shorts/NN_<slug>.mp4"""
import re, subprocess, sys
from pathlib import Path
from shorts_data import SHORTS
P = Path(__file__).resolve().parents[2]


def lufs(f):
    r = subprocess.run(['ffmpeg', '-i', str(f), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True, errors='ignore').stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])


def peak(f):
    r = subprocess.run(['ffmpeg', '-i', str(f), '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True, errors='ignore').stderr
    return float(re.findall(r'max_volume: (-?[\d.]+)', r)[0])


for n in map(int, sys.argv[1:]):
    raw = P / 'output' / 'shorts' / '_raw' / f'{n:02d}.mp4'
    out = P / 'output' / 'shorts' / f"{n:02d}_{SHORTS[n]['slug']}.mp4"
    tmp = out.with_suffix('.tmp.mp4')
    L, trim = lufs(raw), 0.0
    for _ in range(4):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-af', f'volume={-16 - L - trim:.2f}dB',
                        '-c:a', 'aac', '-movflags', '+faststart', str(tmp)], check=True)
        pk = peak(tmp)
        if pk <= -1.0: break
        trim += pk + 1.0
    tmp.replace(out)
    print(out.name, f'{L:.1f} -> {-16 - trim:.1f} LUFS, peak {pk:.1f}')
