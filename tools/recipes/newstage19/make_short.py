"""Build one stage-short: python make_short.py 1 [2 ...]
1. edges of the hook + pieces on the waveform (edges.py)
2. the short's own mp4 = hook, rewind (frames of the whole span played backwards, 0.9 s, silent), pieces; 25 ms audio fades
   -> motion-library/public/projects/newstage19/sNN.mp4
3. captions from CAP (corrected text) timed on words_NN.json (cap_words.py), cues + beats mapped to the short timeline, sfx
   -> work/shorts/props_NN.json
"""
import json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE = Path(__file__).parent
P = HERE.parents[1]
ML = P.parents[1] / 'motion-library'
PUB = ML / 'public' / 'projects' / 'newstage19'
SRC = P / 'input' / 'Main new.mp4'
OUT = P / 'work' / 'shorts'
from shorts_data import SHORTS, TOTAL
from caps import CAPS
from edges import fit

LONG = json.load(open(P / 'work' / 'transcript.json', encoding='utf8'))
REW = 0.9   # rewind length (s)
TAIL = 1.6  # quiet end so the big badge can land
FADE = 0.025


def mmss(s):
    return f'{int(s // 60)}:{int(s % 60):02d}'


def build(n):
    sh = SHORTS[n]
    # never run into the neighbouring word (e.g. "اللي بعده" after the last sentence): give fit() the previous word's end
    # and the next word's start from the long transcription
    allw = sorted((w['start'], w['end']) for sn in LONG['sentences'] for w in sn['words'])
    def nb(a, b):
        prev = max((e for s0, e in allw if e <= a + 0.05 and s0 < a - 0.05), default=None)
        nxt = min((s0 for s0, e in allw if s0 >= b + 0.05), default=None)
        return prev, nxt
    # (a, b, 'x') = exact edges set by hand on the waveform (speech runs on without a gap: fit() clipped "الفن", "بحثية")
    spans = [(r[0], r[1]) if len(r) > 2 else fit(r[0], r[1], *nb(r[0], r[1]))[:2] for r in [sh['hook']] + sh['pieces']]
    # timeline: (src_a, src_b, short_t)
    tl, t = [], 0.0
    hook = spans[0]
    tl.append((hook[0], hook[1], 0.0)); t = hook[1] - hook[0]
    rew_t = t; t += REW
    for a, b in spans[1:]:
        tl.append((a, b, t)); t += b - a
    dur = t + TAIL

    # ---- the mp4: hook | rewind | pieces | tail (last frame held) ----
    PUB.mkdir(parents=True, exist_ok=True)
    out = PUB / f's{n:02d}.mp4'
    first = spans[1][0]
    if first > hook[0] - 0.5:  # the pieces continue after the hook (shorts 12, 18): rewind back over the hook itself
        first = hook[0]
    ins, fc, k = [], [], 0
    def seg(a, b):
        nonlocal k
        ins.extend(['-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', str(SRC)])
        d = b - a
        fc.append(f'[{k}:v]fps=30,scale=1280:720,setsar=1,format=yuv420p[v{k}];'
                  f'[{k}:a]aresample=48000,atrim=0:{d:.4f},asetpts=PTS-STARTPTS,apad=whole_dur={d:.4f},'
                  f'afade=t=in:d={FADE},afade=t=out:st={d - FADE:.3f}:d={FADE}[a{k}];')  # exact length: extra AAC samples drifted lip-sync 0.28 s
        k += 1
    seg(*hook)
    # rewind: from the hook back to the first piece; 27 frames picked over the span, reversed
    span = hook[1] - first
    ins.extend(['-ss', f'{first:.3f}', '-t', f'{span:.3f}', '-i', str(SRC)])
    fc.append(f'[{k}:v]fps={27 / span:.5f},scale=1280:720,setsar=1,reverse,setpts=N/(30*TB),fps=30,trim=duration={REW},format=yuv420p,'
              f'eq=saturation=0.6:contrast=1.15[v{k}];anullsrc=r=48000:cl=stereo,atrim=duration={REW}[a{k}];')
    k += 1
    for a, b in spans[1:]:
        seg(a, b)
    # concat, then hold the last frame + silence for the tail
    # bleeps (insults he wants hidden): silence those source ranges in the short's audio (a beep sfx is added in props)
    bl = []
    tcur = hook[1] - hook[0] + REW
    for a, b in spans[1:]:
        for x0, x1 in sh.get('bleep', []):
            if a <= x0 < b:
                bl.append((round(tcur + x0 - a, 3), round(tcur + min(x1, b) - a, 3)))
        tcur += b - a
    mute = ''.join(f",volume=enable='between(t,{x0},{x1})':volume=0" for x0, x1 in bl)
    # audio and video joined SEPARATELY: a joint concat padded every piece's audio to its (frame-rounded) video length ->
    # the voice drifted up to 0.28 s late by the end (Aly 2026-10-19: "صوتي مش ماشي مع الصورة")
    fc.append(''.join(f'[v{i}]' for i in range(k)) + f'concat=n={k}:v=1:a=0[cv0];' + ''.join(f'[a{i}]' for i in range(k)) + f'concat=n={k}:v=0:a=1[ca0];'
              f'[cv0]tpad=stop_mode=clone:stop_duration={TAIL}[cv];[ca0]apad=pad_dur={TAIL}{mute}[ca]')
    cmd = ['ffmpeg', '-v', 'error', '-y'] + ins + ['-filter_complex', ''.join(fc), '-map', '[cv]', '-map', '[ca]', '-ac', '2',
                                                   '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-g', '30', '-c:a', 'aac', '-b:a', '192k', str(out)]
    subprocess.run(cmd, check=True)

    def to_short(s, hook=False, after=0.0):
        # the hook repeats source seconds of a later piece: cues map into the pieces unless they are hook cues
        for a, b, st in (tl[:1] if hook else tl[1:]):
            if a - 0.3 <= s <= b + 0.3 and st + b - a >= after:
                return st + min(max(s, a), b) - a
        return None

    # ---- captions ----
    words = []
    wj = json.load(open(OUT / f'words_{n:02d}.json', encoding='utf8'))
    cap = CAPS.get(n) or sh.get('cap') or [' '.join(w['w'] for w in p['words']) for p in wj]
    for i, (p, text) in enumerate(zip(wj, cap)):
        a, b, st = tl[i]
        src_words = p['words']
        if text.startswith('@L '):  # piece re-transcription was garbage -> timings from the long pass (transcript.json)
            text = text[3:]
            src_words = [w for sn in LONG['sentences'] for w in sn['words']]
        ws = [w for w in src_words if w['end'] > a - 0.2 and w['start'] < b + 0.2]
        if not ws:
            continue
        # cumulative char position of whisper words -> time
        cum, pos = [], 0
        for w in ws:
            cum.append((pos, w['start'], pos + len(w['w']), w['end'])); pos += len(w['w']) + 1
        tot = pos
        def t_at(fr):
            x = fr * tot
            for c0, t0, c1, t1 in cum:
                if x <= c1:
                    return t0 + (t1 - t0) * max(0, min(1, (x - c0) / max(1, c1 - c0)))
            return cum[-1][3]
        toks = text.split()
        tl_len = sum(len(x.replace('*', '')) + 1 for x in toks)
        c = 0
        for tok in toks:
            w = tok.replace('*', ''); hl = '*' in tok
            s0 = t_at(c / tl_len); s1 = t_at((c + len(w)) / tl_len); c += len(w) + 1
            s0, s1 = max(a, min(b, s0)), max(a, min(b, s1))
            words.append({'w': w, 'start': round(st + s0 - a, 2), 'end': round(st + max(s1, s0 + 0.12) - a, 2), **({'hl': True} if hl else {})})

    # ---- cues ----
    cues = []
    cs = sh['cues']
    # a cue whose props have '_hook': True plays inside the hook (cold open), cut at the rewind
    ishook = [i == 0 or bool(c[2].get('_hook')) for i, c in enumerate(cs)]
    starts = [to_short(c[0], hook=ishook[i]) for i, c in enumerate(cs)]
    for i, (s, kind, props, beats) in enumerate(cs):
        t0 = starts[i]
        if t0 is None:
            print('cue outside the pieces', s, kind); continue
        # a scene ends where the NEXT scene in TIME starts (any position in the list; appended cues overlapped in 10 / 11 v4)
        nxt = [starts[j] for j in range(len(cs)) if j != i and starts[j] is not None and starts[j] > t0 + 0.01 and cs[j][1] != 'hall']
        t1 = min(nxt) if nxt else dur
        if ishook[i]:
            t1 = min(t1, rew_t)
        p = dict(props)
        if beats:
            p['b'] = {k: round(to_short(v, hook=ishook[i], after=t0) - t0, 2) for k, v in beats.items()
                      if to_short(v, hook=ishook[i], after=t0) is not None}  # a beat in a cut gap is dropped
        p.pop('_hook', None)
        cues.append({'t': round(t0, 2), 'd': round(t1 - t0, 2), 'k': kind, 'p': p})

    # slide videos used by 'clip' cues -> public
    import shutil
    for c in cues:
        if c['k'] == 'clip':
            (PUB / 'media').mkdir(exist_ok=True)
            src = P / 'work' / 'slide_media' / c['p']['file']
            if not (PUB / 'media' / src.name).exists():
                shutil.copy(src, PUB / 'media' / src.name)

    # ---- sfx ----
    sfx = [{'t': round(rew_t - 0.05, 2), 'file': 'sfx/tape.wav', 'vol': 0.5}]
    for c in cues[1:]:
        sfx.append({'t': max(0, c['t'] - 0.08), 'file': f"sfx/whoosh_{1 + int(c['t'] * 10) % 3}.wav", 'vol': 0.22})
        for name, v in c['p'].get('b', {}).items():
            fx = {'cash': 'sfx/cash.wav', 'card': 'sfx/pop_2.wav', 'walk': 'sfx/swish.wav', 'hurt': 'sfx/buzz_wrong.wav', 'good': 'sfx/ding.wav',
                  'ma': 'sfx/buzz_wrong.wav', 'mb': 'sfx/ding.wav', 'go': 'sfx/tick.wav', 'go2': 'sfx/impact.wav',
                  'shake': 'sfx/rustle.wav', 'squeeze': 'sfx/pour.wav'}.get(name)
            if fx:
                sfx.append({'t': round(c['t'] + v, 2), 'file': fx, 'vol': 0.3})
        for name, v in c['p'].get('b', {}).items():
            if name[:1] in 'sr' and name[1:].isdigit():  # flow steps / list rows
                sfx.append({'t': round(c['t'] + v, 2), 'file': f'sfx/pop_{1 + int(name[1:]) % 3}.wav', 'vol': 0.25})
        if c['k'] in ('atm', 'atm3d') and c['p'].get('mode') == 'wrong':
            sfx.append({'t': round(c['t'] + c['p']['b']['walk'] + 1.2, 2), 'file': 'sfx/buzz_wrong.wav', 'vol': 0.3})
        if c['k'] == 'big':
            sfx.append({'t': round(c['t'] + 0.1, 2), 'file': 'sfx/pop_1.wav', 'vol': 0.25})
    sfx.append({'t': round(dur - 2.6, 2), 'file': 'sfx/riser.wav', 'vol': 0.2})
    for x0, x1 in bl:
        sfx.append({'t': x0, 'file': 'sfx/bleep.wav', 'vol': 0.35})

    # ---- v2 (Aly 2026-10-19): he fills the screen the whole short -> the camera follows him, zoom in/out per piece ----
    trk = {float(k): v[0] for k, v in json.load(open(P / 'work' / 'track.json')).items()}
    tks = sorted(trk)
    import bisect
    def cx_at(s):
        i = bisect.bisect_left(tks, s)
        near = [tks[j] for j in (i - 1, i) if 0 <= j < len(tks) and abs(tks[j] - s) < 1.5]
        return trk[min(near, key=lambda x: abs(x - s))] if near else None
    track = []
    for idx, (a, b, st) in enumerate(tl):
        raw, last = [], None
        for k in range(int((b - a) / 0.25) + 1):
            v = cx_at(a + k * 0.25); last = v if v is not None else last; raw.append(last)
        raw = [v if v is not None else next((x for x in raw if x is not None), 640) for v in raw]
        sm = [sum(raw[max(0, i - 4):i + 5]) / len(raw[max(0, i - 4):i + 5]) for i in range(len(raw))]  # ~2 s moving average
        track += [[round(st + k * 0.25, 2), round(v)] for k, v in enumerate(sm)]
        if idx == 0:
            rew_cx = sm[-1]
    track.sort()
    zoom = [[0, 1.0], [round(rew_t - 0.2, 2), 1.32], [round(rew_t + REW, 2), 1.0]]
    for i, (a, b, st) in enumerate(tl[1:]):
        z = 1.0 if i % 2 == 0 else 1.18
        zoom += [[round(st + 0.001, 3), z], [round(st + b - a - 0.001, 3), z + 0.06]]
    for t0, z in sh.get('punch', []):  # extra punch-ins on a word: (src_sec, zoom)
        s0 = to_short(t0)
        zoom += [[round(s0 - 0.25, 2), None], [round(s0, 2), z], [round(s0 + 1.6, 2), z], [round(s0 + 1.9, 2), None]]
    zoom.sort(key=lambda x: x[0])
    for i, kz in enumerate(zoom):  # None = keep the base curve value there
        if kz[1] is None:
            prev = next(x[1] for x in reversed(zoom[:i]) if x[1] is not None)
            kz[1] = prev

    # ---- pop-out moments: (src_sec, dur) -> his cut-out of the same window, he steps out of a square card ----
    for j, (t0, d) in enumerate(sh.get('pops', [])):
        s0 = to_short(t0)
        cx = next(v for tt, v in track if tt >= s0)
        ch = 705; cw = ch * 9 / 16; cy = max(0, min(720 - ch, 170 - 430 * ch / 1920)) + ch / 2  # = win(1) in stage/kit.tsx
        x0 = max(0, min(1280 - cw, cx - cw / 2))
        crop = P / 'work' / f'pop_{n:02d}_{j}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s0:.3f}', '-t', f'{d:.3f}', '-i', str(out), '-an', '-vf',
                        f'crop={cw:.0f}:{ch}:{x0:.0f}:{cy - ch / 2:.0f},scale=540:960:flags=lanczos', '-c:v', 'libx264', '-crf', '14', str(crop)], check=True)
        webm = PUB / f'pop_{n:02d}_{j}.webm'
        if True:
            subprocess.run([sys.executable, str(P.parents[1] / 'tools' / 'matte.py'), str(crop), '0', f'{d:.3f}', str(webm), '--fps', '30'], check=True)
        cues.append({'t': round(s0, 2), 'd': round(d, 2), 'k': 'pop', 'p': {'matte': f'projects/newstage19/{webm.name}', 'cx': round(x0 + cw / 2), 'z': 1}})
        sfx.append({'t': round(s0, 2), 'file': 'sfx/swoop_up.wav', 'vol': 0.3})

    # timeline for cam.py (his full-screen camera from the RAW file)
    segs = [{'kind': 'seg', 'a': hook[0], 'b': hook[1], 'st': 0.0}, {'kind': 'rew', 'a': first, 'b': hook[1], 'st': round(rew_t, 3), 'd': REW}]
    segs += [{'kind': 'seg', 'a': a, 'b': b, 'st': st} for a, b, st in tl[1:]]
    segs.append({'kind': 'tail', 'st': round(t, 3), 'd': TAIL})
    json.dump({'segs': segs, 'zoom': zoom}, open(OUT / f'tl_{n:02d}.json', 'w'))

    props = dict(duration=round(dur, 2), no=n, total=TOTAL, head=sh['head'], src=f'projects/newstage19/s{n:02d}.mp4', hookEnd=round(rew_t, 2),
                 rewind={'t': round(rew_t, 2), 'd': REW, 'from': mmss(hook[1]), 'to': mmss(first)},
                 thumb='projects/newstage19/thumb.jpg', qr='projects/newstage19/qr.png', cues=cues, words=words, capsHide=[], sfx=sfx,
                 cam=f'projects/newstage19/cam_{n:02d}.mp4')
    # QC (Aly 2026-10-19 "متغلطش غلطات دي تاني"): two scenes on screen at once = stop, never render it
    shown = sorted([c for c in cues if c['k'] != 'hall'], key=lambda c: c['t'])
    bad = [(a['k'], a['t'], b['k'], b['t']) for a, b in zip(shown, shown[1:]) if a['t'] + a['d'] > b['t'] + 0.05]
    if bad:
        raise SystemExit(f'short {n}: overlapping scenes {bad}')
    json.dump(props, open(OUT / f'props_{n:02d}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'short {n}: {dur:.1f} s, {len(cues)} cues, {len(words)} words, pieces {[(round(a, 2), round(b, 2)) for a, b in spans]}')


if __name__ == '__main__':
    for n in map(int, sys.argv[1:]):
        build(n)
