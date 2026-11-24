"""Collect the 9:16 clips (Higgsfield reframes in assets/ai/higgsfield/reframe_v11/out, HeyGen twin in assets/ai/heygen/vertical_v11),
copy them to motion-library/public/projects/aiworld/shorts/v916/ and write work/shorts/vertical_clips.json:
{v11 src: [9:16 file, source second where it starts, length factor k]}. Run from work/."""
import json, os, shutil, subprocess
A = '../assets/ai/'; PUB = '../../../motion-library/public/'; DST = 'projects/aiworld/shorts/v916/'
os.makedirs(PUB + DST, exist_ok=True)
dur = lambda f: float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
W = json.load(open('shorts/reframe_windows.json'))
out = {}
for src, (lo, hi) in W.items():
    name = os.path.basename(src)
    f = A + 'higgsfield/reframe_v11/out/' + (name if name != 'ex_generated.mp4' else 'ex_generated5.mp4')
    if not os.path.exists(f): print('missing', name); continue
    shutil.copy(f, PUB + DST + name)
    out[src] = [DST + name, lo, round(dur(f) / dur(A + 'higgsfield/reframe_v11/src/' + (name if name != 'ex_generated.mp4' else 'ex_generated5.mp4')), 4)]
tw = A + 'heygen/vertical_v11/twin_175_178_9x16.mp4'
if os.path.exists(tw):
    shutil.copy(tw, PUB + DST + 'twin_175_178.mp4')
    out['projects/aiworld/v6/avatar_gen/avatar_175_C095.mp4'] = [DST + 'twin_175_178.mp4', 0.0, 1.0]
    out['projects/aiworld/v6/avatar_gen/avatar_178_C095.mp4'] = [DST + 'twin_175_178.mp4', -5.95, 1.0]
json.dump(out, open('shorts/vertical_clips.json', 'w'), indent=1)
print(len(out), 'vertical clips mapped')
