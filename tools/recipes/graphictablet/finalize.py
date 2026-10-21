"""Final pass (gain only, his voice untouched): whole short -16 LUFS with a transparent peak limiter (same level in every short),
compressed like Aly's `ffmpeg -i in out` (x264 CRF 23 + AAC). output/_raw/short_N.mp4 -> output/short_N.mp4"""
import re, subprocess, sys
from pathlib import Path
P = Path(__file__).resolve().parents[2]


def lufs(f):
    r = subprocess.run(['ffmpeg', '-i', str(f), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True, errors='ignore').stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])


for n in map(int, sys.argv[1:]):
    raw = P / 'output' / '_raw' / f'short_{n}.mp4'
    out = P / 'output' / f'short_{n}.mp4'
    L, trim = lufs(raw), 0.0
    for _ in range(4):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-c:v', 'libx264', '-crf', '23', '-preset', 'medium',
                        '-af', f'volume={-16 - L - trim:.2f}dB,alimiter=limit=0.84:attack=2:release=50:level=disabled',
                        '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(out)], check=True)
        got = lufs(out)
        if abs(got + 16) <= 0.3:
            break
        trim += got + 16
    print(f'short {n}: raw {L:.1f} -> {got:.1f} LUFS, {out.stat().st_size / 1e6:.1f} MB')
