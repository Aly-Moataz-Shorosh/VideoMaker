# Soundtrack straight from props with ffmpeg. The session's audio pieces go in UNTOUCHED (no volume, no filter, no fade:
# Aly 2026-10-24 "متلعبش في الصوت"); music only where props put it (opening + separators). Then mux with the muted video.
#   python mix_audio.py <props.json> <video_muted.mp4> <out.mp4>
import json, subprocess, sys
from pathlib import Path

PUB = Path(__file__).resolve().parents[4] / 'motion-library' / 'public'
P = json.load(open(sys.argv[1], encoding='utf-8'))
ins, fil, labels = [], [], []


def inp(path, ss, t):
    ins.extend(['-ss', f'{ss:.3f}', '-t', f'{t:.3f}', '-i', path])
    return len(ins) // 6 - 1


for p in P['parts']:
    i = inp(p['file'], p['from'], p['to'] - p['from'])
    ms = int(round(p['at'] * 1000))
    fil.append(f'[{i}:a]adelay={ms}|{ms}[a{i}]'); labels.append(f'[a{i}]')
for m in P['music']:
    i = inp(m['file'], m.get('from', 0), m['d'])
    fd = max(0.05, m.get('fade', 1)); ms = int(round(m['t'] * 1000))
    fil.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={m.get("vol", 0.12)},afade=t=in:d={fd:.2f},'
               f'afade=t=out:st={max(0, m["d"] - fd):.3f}:d={fd:.2f},adelay={ms}|{ms}[a{i}]'); labels.append(f'[a{i}]')
fil.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0:duration=longest,apad,atrim=0:{P["duration"]:.3f}[out]')
scr = Path(sys.argv[3]).with_suffix('.filter.txt'); scr.write_text(';\n'.join(fil), encoding='utf-8')
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + ins + ['-i', sys.argv[2], '-filter_complex_script', str(scr), '-map', f'{len(ins) // 6}:v', '-map', '[out]',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', sys.argv[3]], cwd=PUB, check=True)
scr.unlink()
print('ok', sys.argv[3])
