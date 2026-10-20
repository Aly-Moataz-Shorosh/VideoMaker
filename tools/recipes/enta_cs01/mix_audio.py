"""Soundtrack of the episode with ffmpeg: his edit's audio UNTOUCHED (Aly rule: never clean his voice) + every 'sfx' cue of
edit_<name>.json (public/sfx/<name>.wav at its volume). Usage: python mix_audio.py <edit.json> <out_dir> -> <out_dir>/audio.m4a"""
import json, subprocess, sys
from pathlib import Path

props, out = Path(sys.argv[1]), Path(sys.argv[2])
P = json.load(open(props, encoding='utf-8'))
PUB = props.parents[2]
ins, fil, labels = ['-i', str(PUB / P['source'])], ['[0:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a0]'], ['[a0]']
for c in P['cues']:
    if c['t'] != 'sfx': continue
    ins += ['-i', str(PUB / 'sfx' / f"{c['props']['name']}.wav")]
    i = len(labels); ms = int(round(c['at'] * 1000))
    fil.append(f"[{i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,volume={c['props'].get('volume', 0.5)},adelay={ms}|{ms}[a{i}]")
    labels.append(f'[a{i}]')
fil.append(''.join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{P['duration']:.3f}[out]")
script = out / 'mix_filter.txt'; script.write_text(';\n'.join(fil), encoding='utf-8')
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + ins + ['-filter_complex_script', str(script), '-map', '[out]', '-c:a', 'aac', '-b:a', '256k', str(out / 'audio.m4a')], check=True)
print(len(labels) - 1, 'sfx mixed ->', out / 'audio.m4a')
