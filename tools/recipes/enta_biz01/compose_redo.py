"""Compose the re-rendered video (render_redo.sh step 3): the old muted chunks (v_NN.mp4, in order) + the 'fix' overlay PNGs over the
whole timeline, then every new part p_NN.mp4 put over exactly its own frames. One ffmpeg pass, x264 CRF 18 (one generation over the
CRF 20 chunks). Usage: python -X utf8 compose_redo.py <old chunks dir> <redo dir> <redo_parts.json> <out.mp4>"""
import glob, json, os, subprocess, sys

old, d, parts_json, out = sys.argv[1:5]
parts = json.load(open(parts_json))
chunks = sorted(glob.glob(os.path.join(old, 'v_*.mp4')))
lst = os.path.join(d, 'old_list.txt')
open(lst, 'w').write(''.join(f"file '{c.replace(os.sep, '/')}'\n" for c in chunks))
# Remotion names the PNGs element-<frame> with a width that depends on the range -> one fixed width for ffmpeg's pattern
for f in glob.glob(os.path.join(d, 'fix', 'element-*.png')):
    os.replace(f, os.path.join(d, 'fix', '%06d.png' % int(os.path.basename(f)[8:-4])))
pngs = sorted(glob.glob(os.path.join(d, 'fix', '[0-9]*.png')))
assert pngs, 'no overlay frames'
first = int(os.path.basename(pngs[0])[:6])
assert int(os.path.basename(pngs[-1])[:6]) - first + 1 == len(pngs), 'overlay frames missing'
cmd = ['ffmpeg', '-v', 'error', '-stats', '-y', '-f', 'concat', '-safe', '0', '-i', lst,
       '-framerate', '30', '-start_number', str(first), '-i', os.path.join(d, 'fix', '%06d.png')]
for k, (a, b) in enumerate(parts):
    cmd += ['-itsoffset', f'{a / 30:.6f}', '-i', os.path.join(d, 'parts', f'p_{k:02d}.mp4')]
fl = ['[0:v][1:v]overlay=0:0:eof_action=pass:format=auto[b0]']
for k, (a, b) in enumerate(parts):
    fl.append(f"[b{k}][{k + 2}:v]overlay=0:0:eof_action=pass:enable='between(n,{a},{b})'[b{k + 1}]")
fl.append(f'[b{len(parts)}]format=yuv420p[v]')
cmd += ['-filter_complex', ';'.join(fl), '-map', '[v]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-r', '30', out]
print(len(chunks), 'old chunks,', len(pngs), 'overlay frames,', len(parts), 'new parts')
sys.exit(subprocess.call(cmd))
