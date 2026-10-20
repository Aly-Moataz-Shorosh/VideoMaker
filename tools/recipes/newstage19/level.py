"""Final pass (gain only, his voice untouched): whole short -16 LUFS, true peak <= -1 dB; video re-encoded like Aly's own
`ffmpeg -i in out` (x264 CRF 18 slow + AAC: Aly 2026-10-19 "اعمل الجودة احسن ما يمكن"). output/_raw/short_NN.mp4 -> output/NN_<slug>.mp4.   python level.py 1 2"""
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
    raw = P / 'output' / '_raw' / f'short_{n:02d}.mp4'
    VER = 'v3'  # v1 small hall card, v2 browser-upscaled edit (both rejected 2026-10-19); v3 = RAW camera, 3D emoji, face blur
    (P / 'output' / VER).mkdir(exist_ok=True)
    out = P / 'output' / VER / f"{n:02d}_{SHORTS[n]['slug']}.mp4"
    tmp = out.with_suffix('.tmp.mp4')
    L, trim = lufs(raw), 0.0
    for _ in range(4):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-af', f'volume={-16 - L - trim:.2f}dB',
                        '-c:a', 'aac', '-movflags', '+faststart', str(tmp)], check=True)
        pk = peak(tmp)
        if pk <= -1.0: break
        trim += pk + 1.0
    tmp.replace(out)  # whole file at once (never a half-written mp4 he might open)
    print(out.name, f'{L:.1f} -> {-16 - trim:.1f} LUFS, peak {pk:.1f}')
