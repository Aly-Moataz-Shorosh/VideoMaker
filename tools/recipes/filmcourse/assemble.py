# Final video in ONE ffmpeg pass (h264_nvenc): every piece of work/pieces.json (teaser, pages, separator k, course chapter k ..., end)
# is its own input (-ss/-t, frame-accurate because it is re-encoded) and they are joined with the concat filter.
# The course audio goes in untouched (only resampled/encoded); no intro / outro (Aly review 1).
#   python assemble.py   -> output/film_making_course_full.mp4
import json, subprocess, sys, time
from pathlib import Path
W = Path(__file__).resolve().parent.parent
P = W.parent
SRC = P / 'input/2026-11-06 14-39-41.mp4'
OUT = P / 'output/film_making_course_full.mp4'
pieces = json.load(open(W / 'pieces.json'))
ins, fc = [], []
V = 'fps=60,scale=1920:1080,setsar=1,format=yuv420p'
A = 'aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo'
for i, p in enumerate(pieces):
    f = SRC if p['file'] == 'SRC' else W / p['file']
    ins += ['-ss', f"{p['ss']:.4f}", '-t', f"{p['t']:.4f}", '-i', str(f)]
    fc.append(f'[{i}:v]{V}[v{i}];[{i}:a]{A},apad=whole_dur={p["t"]:.4f}[a{i}]')
fc.append(''.join(f'[v{i}][a{i}]' for i in range(len(pieces))) + f'concat=n={len(pieces)}:v=1:a=1[v][a]')
scr = W / 'assemble_filter.txt'
scr.write_text(';\n'.join(fc), encoding='utf-8')
st = time.time()
subprocess.run(['ffmpeg', '-v', 'error', '-stats', '-y'] + ins + ['-filter_complex_script', str(scr), '-map', '[v]', '-map', '[a]',
                '-c:v', 'h264_nvenc', '-preset', 'p5', '-rc', 'vbr', '-cq', '24', '-b:v', '0', '-maxrate', '8M', '-bufsize', '16M', '-profile:v', 'high',
                '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', str(OUT)], check=True)
scr.unlink()
print('done', round(time.time() - st), 's', OUT)
