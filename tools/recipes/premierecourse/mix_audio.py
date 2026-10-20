# Build the course soundtrack straight from props_full.json with ffmpeg (Remotion's audio pass needed > 15 GB temp and
# filled the disk). Same mix as the composition: his voice untouched (only rate-1 pieces; x4 pieces are muted), music with
# linear fade in/out, sfx. Output: output/full/audio.m4a, then joins the video chunks -> output/premiere_course_full.mp4
#   python mix_audio.py
import json, subprocess, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[2]
PUBDIR = PROJ.parent.parent / 'motion-library' / 'public'
P = json.load(open(PROJ / 'work/props_full.json', encoding='utf-8'))
TOTAL = P['duration']
ins, fil, labels = [], [], []


def add_input(path, ss, t):
    ins.extend(['-ss', f'{ss:.3f}', '-t', f'{t:.3f}', '-i', path])
    return len(ins) // 6 - 1


for p in P['parts']:
    if p.get('rate', 1) > 1.01: continue
    d = p['to'] - p['from']
    i = add_input(p['file'], p['from'], d)
    ms = int(round(p['at'] * 1000))
    fil.append(f'[{i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,adelay={ms}|{ms}[a{i}]'); labels.append(f'[a{i}]')
for m in P['music']:
    i = add_input(m['file'], m.get('from', 0), m['d'])
    fd = max(0.05, m.get('fade', 1))
    ms = int(round(m['t'] * 1000))
    fil.append(f'[{i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,volume={m.get("vol", 0.12)},'
               f'afade=t=in:d={fd:.2f},afade=t=out:st={max(0, m["d"] - fd):.3f}:d={fd:.2f},adelay={ms}|{ms}[a{i}]'); labels.append(f'[a{i}]')
for s in P['sfx']:
    i = add_input(s['file'], 0, 3)
    ms = int(round(s['t'] * 1000))
    fil.append(f'[{i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,volume={s.get("vol", 0.25)},adelay={ms}|{ms}[a{i}]'); labels.append(f'[a{i}]')
fil.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0:duration=longest,apad,atrim=0:{TOTAL:.3f}[out]')
script = PROJ / 'work/mix_filter.txt'
script.write_text(';\n'.join(fil), encoding='utf-8')
out = PROJ / 'output/full/audio.m4a'
cmd = ['ffmpeg', '-v', 'error', '-y'] + ins + ['-filter_complex_script', str(script), '-map', '[out]', '-c:a', 'aac', '-b:a', '192k', str(out)]
print(len(labels), 'audio inputs', flush=True)
subprocess.run(cmd, cwd=PUBDIR, check=True)
print('audio ok', out, flush=True)

full = PROJ / 'output/full'
lst = full / 'list.txt'
lst.write_text(''.join(f"file '{f.as_posix()}'\n" for f in sorted(full.glob('v_*.mp4'))), encoding='utf-8')
final = PROJ / 'output/premiere_course_full.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst), '-i', str(out), '-map', '0:v', '-map', '1:a', '-c', 'copy',
                '-movflags', '+faststart', str(final)], check=True)
print('JOINED', final)
