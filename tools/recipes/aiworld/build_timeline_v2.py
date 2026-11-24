"""REAL timing from the generated voice (HeyGen voice_v1 + Whisper) -> timeline_v2.json, chapters_v2.txt, captions_v2.srt.
Chapters = the real wav files placed one after the other with GAP between them; C11 = [MUSIC 180].
Inside a chapter, each script word gets the time of the Whisper word it is aligned to (difflib);
unmatched script words are spread between their matched neighbours. Caption TEXT = the script (not Whisper).
Also writes work/voice_v1_timeline.wav = the narration placed on the timeline (silence for gaps + music part).
Same JSON shape as timeline_v1.json (chapters[].segments[] with start/end/dur/words) + chapters[].file.
Usage: python -X utf8 work/scripts/build_timeline_v2.py   (from the project folder)"""
import difflib, json, re, subprocess, sys
sys.path.insert(0, 'work/scripts')
from check_voice import norm  # noqa: E402  (runs check_voice once on import -> refreshes voice_check_v1.md)

GAP = 0.6
V1 = json.load(open('work/timeline_v1.json', encoding='utf-8'))
VOICE = {p['chapter']: p for p in json.load(open('assets/ai/heygen/voice_v1/voice_v1.json', encoding='utf-8'))['parts']}
TIM = {c['chapter']: c for c in json.load(open('work/voice_timing_v1.json', encoding='utf-8'))}

t = 0.0
for ch in V1['chapters']:
    ch['start'] = round(t, 3)
    music = re.match(r'\[MUSIC (\d+)\]', ch['segments'][0]['text'])
    if music:
        s = ch['segments'][0]
        s.update(start=round(t, 3), dur=float(music.group(1)), end=round(t + float(music.group(1)), 3), words=0)
        t += s['dur'] + GAP
        ch['end'] = round(t, 3)
        continue
    v, tm = VOICE[ch['id']], TIM[ch['id']]
    ch['file'] = 'assets/ai/heygen/' + v['file']
    # script words with their segment
    sw = [(s['id'], w) for s in ch['segments'] for w in s['text'].split()]
    a = [norm(w) for _, w in sw]
    hw = tm['words']
    b = [norm(w['w']) for w in hw]
    times = [None] * len(sw)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            times[blk.a + k] = (hw[blk.b + k]['s'], hw[blk.b + k]['e'])
    # fill gaps by spreading between known neighbours
    known = [i for i, x in enumerate(times) if x]
    edges = [(-1, (0.0, 0.0))] + [(i, times[i]) for i in known] + [(len(sw), (v['duration_s'], v['duration_s']))]
    for (i0, t0), (i1, t1) in zip(edges, edges[1:]):
        n = i1 - i0 - 1
        if n > 0:
            span = (t1[0] - t0[1]) / n
            for k in range(n):
                times[i0 + 1 + k] = (t0[1] + k * span, t0[1] + (k + 1) * span)
    for s in ch['segments']:
        idx = [i for i, (sid, _) in enumerate(sw) if sid == s['id']]
        s['start'] = round(t + times[idx[0]][0], 3)
        s['end'] = round(t + times[idx[-1]][1], 3)
        s['dur'] = round(s['end'] - s['start'], 3)
        s['words'] = len(idx)
        s['word_times'] = [[sw[i][1], round(t + times[i][0], 3), round(t + times[i][1], 3)] for i in idx]
    t += v['duration_s'] + GAP
    ch['end'] = round(t, 3)
total = round(t, 3)

def mmss(x):
    x = int(x)
    return f"{x // 60}:{x % 60:02d}"

def ts(x):
    ms = int(round(x * 1000))
    return f"{ms // 3600000:02d}:{ms % 3600000 // 60000:02d}:{ms % 60000 // 1000:02d},{ms % 1000:03d}"

json.dump({'source': 'voice_v1 + Whisper', 'gap': GAP, 'total': total, 'chapters': V1['chapters']},
          open('work/timeline_v2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open('work/chapters_v2.txt', 'w', encoding='utf-8').write(
    '\n'.join(f"{mmss(c['start'])} {c['title']}" for c in V1['chapters']) + '\n')
srt, n = [], 0
for c in V1['chapters']:
    for s in c['segments']:
        wt = s.get('word_times') or []
        for i in range(0, len(wt), 6):
            g = wt[i:i + 6]
            n += 1
            srt.append(f"{n}\n{ts(g[0][1])} --> {ts(g[-1][2])}\n{' '.join(w for w, _, _ in g)}\n")
open('work/captions_v2.srt', 'w', encoding='utf-8').write('\n'.join(srt))

# narration on the timeline (one wav, silence in gaps and in the music chapter)
inputs, filt = [], []
for c in V1['chapters']:
    if c.get('file'):
        k = len(inputs) // 2
        inputs += ['-i', c['file']]
        filt.append(f"[{k}:a]aformat=sample_rates=44100:channel_layouts=mono,adelay={int(c['start'] * 1000)}[a{k}]")
mix = ''.join(f'[a{k}]' for k in range(len(inputs) // 2))
filt.append(f"{mix}amix=inputs={len(inputs) // 2}:normalize=0,apad=whole_dur={total}[out]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(filt), '-map', '[out]',
                '-t', str(total), 'work/voice_v1_timeline.wav'], check=True)

print(f"total {mmss(total)} ({total}s), captions {n}")
for c in V1['chapters']:
    print(f"  {mmss(c['start']):>6}  {c['id']:5} {c['end'] - c['start']:6.1f}s  {c['title']}")
