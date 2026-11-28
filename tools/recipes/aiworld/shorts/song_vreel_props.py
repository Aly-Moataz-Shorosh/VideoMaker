"""The whole song as a vertical reel (Aly 2026-11-28) -> props for comp ai-world-vsong (VSong11.tsx): work/shorts/vsong_props.json.
Song = the v11 LYR scene (1389.73 -> 1580.20). Clips: 9:16 versions from shorts/vertical_clips.json (made for the 14 shorts) +
assets/ai/higgsfield/reframe_song/out (the 28 rest, Higgsfield reframe 720p; windows shorts/reframe_windows_song.json, cut from 0).
Lyrics = one whole line at a time. End card 8 s: thumbnail + length 27:24 + QR youtu.be/4HLjkQdDnDE.  Run from work/."""
import json, os, re, shutil, subprocess
PUB = '../../../motion-library/public/'; DST = 'projects/aiworld/shorts/v916/'; RS = '../assets/ai/higgsfield/reframe_song/'
dur = lambda f: float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
P = json.load(open('props_v11.json', encoding='utf-8'))
L = [s for s in P['scenes'] if s['k'] == 'LYR'][0]
V = json.load(open('shorts/vertical_clips.json'))
for src in json.load(open('shorts/reframe_windows_song.json')):
    n = os.path.basename(src); o = RS + 'out/' + n
    if not os.path.exists(o): continue
    shutil.copy(o, PUB + DST + n)
    V[src] = [DST + n, 0.0, round(dur(o) / dur(RS + 'src/' + n), 4)]
clips, miss = [], []
for c in L['clips']:
    c = dict(c)
    if c['src'] in V:
        nsrc, s0, k = (V[c['src']] + [1.0])[:3]
        c['src'] = nsrc; c['skip'] = max(0.0, round((c.get('skip', 0) - s0) * k, 3)); c['rate'] = round(c.get('rate', 1) * k, 4)
    else: miss.append(c['src'].split('/')[-1])
    clips.append(c)
lines = []
for d in [d for d in L['items'] if d['k'] == 'line']:
    txt = ' '.join(w['w'] for w in L['words'] if d['t'] - 0.05 <= w['t'] < d['end'])
    txt = re.sub(r'"([^"]+)"', r'«\1»', txt)                    # straight quotes flip in RTL -> Arabic quotes
    txt = re.sub(r'(^|\s)(و|لل|ال|بال)ـ?\s+(?=[A-Za-z])', lambda m: m.group(1) + m.group(2) + ('' if m.group(2) == 'و' else 'ـ') + ' ', txt)   # glue the prefix to the English after it (drawn as one block in VSong11)
    lines.append(dict(t=round(d['t'], 3), end=round(d['end'], 3), text=txt))
sub = [d for d in L['items'] if d['k'] == 'subscribe'][0]
END = 8.0
# the song's loudness per frame (0..1, smoothed) -> the lyric line pulses / floats with the music (Aly review 1: «يتحرك مع الأغنية شوية»)
import numpy as np
raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(L['start']), '-t', str(L['dur']), '-i', '../output/rough_cut_v11.mp4', '-vn', '-ac', '1', '-ar', '8000',
                      '-f', 's16le', '-'], capture_output=True, check=True).stdout
a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768; n = int(L['dur'] * 25); hop = 8000 // 25
rms = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2) + 1e-9) for i in range(n)])
db = 20 * np.log10(rms); lo, hi = np.percentile(db, 10), np.percentile(db, 98)
e = np.clip((db - lo) / (hi - lo), 0, 1)
fast = np.convolve(e, np.ones(3) / 3, 'same'); slow = np.convolve(e, np.ones(25) / 25, 'same')
env = [round(float(x), 3) for x in np.clip((fast - slow) * 2.2 + 0.5, 0, 1)]   # beats above the running level
props = dict(fps=25, start=L['start'], songDur=round(L['dur'], 3), duration=round(L['dur'] + END, 3), clips=clips, lines=lines, env=env,
             title='أغنية كاملة اتعملت بالـ AI', face='projects/aiworld/v6/imgs/v7__logo_face_full.png', sign='brand/signature-calligraphy.png',
             sub=dict(at=round(L['start'] + sub['at'] / 25, 3), logos=sub['logos'], handles=sub['handles']),
             end=dict(thumb='projects/aiworld/shorts/thumb_final.jpg', qr='projects/aiworld/shorts/qr_full.png', line1='الأغنية دي من فيديو كامل',
                      line2='عالم الـ AI كله في فيديو واحد.. والفيديو نفسه معمول بالـ AI', length='27:24'))
json.dump(props, open('shorts/vsong_props.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(f"{props['duration']}s, {len(clips)} clips, {len(lines)} lines, still 16:9: {len(miss)} {miss}")
