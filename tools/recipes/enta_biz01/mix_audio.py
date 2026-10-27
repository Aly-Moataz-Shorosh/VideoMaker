"""Soundtrack of the episode with ffmpeg: his edit's audio UNTOUCHED (Aly rule: never clean his voice) + every 'sfx' cue of
edit_<name>.json (public/sfx/<name>.wav at its volume). Usage: python mix_audio.py <edit.json> <out_dir> -> <out_dir>/audio.m4a
biz ep01 has ~1000 sfx cues: one ffmpeg input per cue made the Windows command line too long (WinError 206) -> each sound file is
an input ONCE, split (asplit) into as many copies as it is used, each copy delayed to its cue."""
import json, subprocess, sys
from collections import defaultdict
from pathlib import Path

props, out = Path(sys.argv[1]), Path(sys.argv[2])
P = json.load(open(props, encoding='utf-8'))
PUB = props.parents[2]
uses = defaultdict(list)
for c in P['cues']:
    if c['t'] == 'sfx': uses[c['props']['name']].append((c['at'], c['props'].get('volume', 0.5)))
ins, fil, labels = ['-i', str(PUB / P['source'])], ['[0:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a0]'], ['[a0]']
for i, (name, us) in enumerate(sorted(uses.items()), 1):
    ins += ['-i', str(PUB / 'sfx' / f'{name}.wav')]
    fil.append(f'[{i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,asplit={len(us)}' + ''.join(f'[s{i}_{k}]' for k in range(len(us))))
    for k, (at, vol) in enumerate(us):
        ms = int(round(at * 1000))
        fil.append(f'[s{i}_{k}]volume={vol},adelay={ms}|{ms}[x{i}_{k}]')
        labels.append(f'[x{i}_{k}]')
fil.append(''.join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{P['duration']:.3f}[out]")
script = out / 'mix_filter.txt'; script.write_text(';\n'.join(fil), encoding='utf-8')
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + ins + ['-filter_complex_script', str(script), '-map', '[out]', '-c:a', 'aac', '-b:a', '256k', str(out / 'audio.m4a')], check=True)
print(len(labels) - 1, 'sfx mixed from', len(uses), 'files ->', out / 'audio.m4a')
