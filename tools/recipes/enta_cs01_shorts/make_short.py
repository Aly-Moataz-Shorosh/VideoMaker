"""Build one meet-short (vertical short from cs ep01): python make_short.py 1 [2 ...]
1. hook + pieces edges on the waveform (edges.py, never into the neighbouring word)
2. public/projects/entacs01s/vNN.mp4 = the Meet tiles strip (hook | 0.9 s rewind | pieces | tail) + his ORIGINAL audio
   (audio and video concatenated SEPARATELY, exact piece lengths: lip-sync lesson of newstage19)
   public/projects/entacs01s/rNN.mp4 = the same timeline from the approved long edit review_02 (boards / person + card)
3. cadres from the long edit's plan (board / card there) and from who is talking (two / one) -> work/shorts/props_NN.json
Captions: CAPS (caps.py, corrected text per piece) timed on work/shorts/words_NN.json (cap_words.py)."""
import json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE = Path(__file__).parent
P = HERE.parents[1]
ML = P.parents[2] / 'motion-library'
CODE = 'entacs01s'
PUB = ML / 'public' / 'projects' / CODE
SRC = P / 'input' / 'main video.mp4'
REVSRC = P / 'output' / 'review_02.mp4'
OUT = P / 'work' / 'shorts'
from shorts_data import SHORTS, TOTAL
from edges import fit
try:
    from caps import CAPS
except ImportError:
    CAPS = {}

LONG = json.load(open(P / 'work' / 'transcript.json', encoding='utf8'))
SPK = json.load(open(P / 'work' / 'speakers.json', encoding='utf8'))['words']   # [start, end, word, 'A'|'G'|'-']
PLAN = json.load(open(P / 'work' / 'plan.json', encoding='utf8'))
REW, TAIL, FADE = 0.9, 3.0, 0.025
CROP_Y = 282                      # strip of the Meet frame that holds both tiles (y 282..778)
STRIP = (1920, 496)
TILES = {k: [v[0], v[1] - CROP_Y, v[2], v[3]] for k, v in PLAN['meet'].items() if k in 'AG'}
FACE = {'A': [0.49, 0.55], 'G': [0.47, 0.40]}   # focus points from the long plan's zoom cues (zx, zy)


def mmss(s):
    return f'{int(s // 60)}:{int(s % 60):02d}'


def speaker(s):
    best, bd = None, 0.8
    for a, b, w, k in SPK:
        if k in 'AG':
            d = 0 if a <= s <= b else min(abs(s - a), abs(s - b))
            if d < bd:
                best, bd = k, d
    return best


def review_state(s):
    """what the long edit shows at source second s: ('board', None) / ('card', person in it) / None"""
    for c in PLAN['cues']:
        if c['t'].startswith('qa_') and c['src'] <= s < c['src'] + c['dur']:
            return ('board', None)
    sh = [c for c in PLAN['cues'] if c['t'] == 'shot' and c['src'] <= s]
    if sh and sh[-1]['props'].get('m') in ('GP', 'AP') and s < sh[-1]['src'] + sh[-1]['dur']:
        return ('card', sh[-1]['props']['m'][0])
    return None


def build(n):
    sh = SHORTS[n]
    allw = sorted((w['start'], w['end']) for sn in LONG['sentences'] for w in sn['words'])
    def nb(a, b):
        prev = max((e for s0, e in allw if e <= a + 0.05 and s0 < a - 0.05), default=None)
        nxt = min((s0 for s0, e in allw if s0 >= b + 0.05), default=None)
        return prev, nxt
    spans = [(r[0], r[1]) if len(r) > 2 else fit(r[0], r[1], *nb(r[0], r[1]))[:2] for r in [sh['hook']] + sh['pieces']]
    # whole frames per piece: picture (frames) and voice (samples) get the SAME length -> no drift
    spans = [(a, round(a + round((b - a) * 30) / 30, 4)) for a, b in spans]
    tl, t = [], 0.0
    hook = spans[0]
    tl.append((hook[0], hook[1], 0.0)); t = hook[1] - hook[0]
    rew_t = t; t += REW
    for a, b in spans[1:]:
        tl.append((a, b, t)); t += b - a
    dur = t + TAIL
    first = spans[1][0]
    if first > hook[0] - 0.5:
        first = hook[0]

    PUB.mkdir(parents=True, exist_ok=True)
    def cut(src, out, vf, audio):
        ins, fc, k = [], [], 0
        def seg(a, b):
            nonlocal k
            ins.extend(['-ss', f'{a:.3f}', '-t', f'{b - a + 0.2:.3f}', '-i', str(src)])
            d = b - a
            fc.append(f'[{k}:v]fps=30,{vf},setsar=1,setpts=PTS-STARTPTS,trim=end_frame={round(d * 30)},format=yuv420p[v{k}];')
            if audio:
                fc.append(f'[{k}:a]aresample=48000,atrim=0:{d:.4f},asetpts=PTS-STARTPTS,apad=whole_dur={d:.4f},'
                          f'afade=t=in:d={FADE},afade=t=out:st={d - FADE:.3f}:d={FADE}[a{k}];')
            k += 1
        seg(*hook)
        span = hook[1] - first
        ins.extend(['-ss', f'{first:.3f}', '-t', f'{span:.3f}', '-i', str(src)])
        # 27 frames spread over the span, played backwards at 30 fps (= REW s). Frame-exact with select/settb: the old
        # fps=27/span + fps=30 chain gave ZERO frames -> every picture after the hook ran 0.93 s ahead of the voice
        # (Aly 2026-10-21: "الصوت مش ماشي مع الصورة"; the end tpad hid it because the file length still matched)
        step = max(1, round(span * 60 / 27))
        fc.append(f"[{k}:v]select='not(mod(n\\,{step}))',{vf},setsar=1,reverse,settb=1/30,setpts=N,trim=end_frame={round(REW * 30)},format=yuv420p,"
                  f'eq=saturation=0.6:contrast=1.15[v{k}];')
        if audio:
            fc.append(f'anullsrc=r=48000:cl=stereo,atrim=duration={REW}[a{k}];')
        k += 1
        for a, b in spans[1:]:
            seg(a, b)
        fc.append(''.join(f'[v{i}]' for i in range(k)) + f'concat=n={k}:v=1:a=0[cv0];[cv0]tpad=stop_mode=clone:stop_duration={TAIL}[cv]')
        maps = ['-map', '[cv]']
        if audio:
            fc.append(';' + ''.join(f'[a{i}]' for i in range(k)) + f'concat=n={k}:v=0:a=1[ca0];[ca0]apad=pad_dur={TAIL}[ca]')
            maps += ['-map', '[ca]', '-ac', '2', '-c:a', 'aac', '-b:a', '192k']
        cmd = ['ffmpeg', '-v', 'error', '-y'] + ins + ['-filter_complex', ''.join(fc)] + maps + \
              ['-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-g', '30', '-t', f'{dur:.3f}', str(out)]
        subprocess.run(cmd, check=True)
    cut(SRC, PUB / f'v{n:02d}.mp4', f'crop={STRIP[0]}:{STRIP[1]}:0:{CROP_Y}', True)
    cut(REVSRC, PUB / f'r{n:02d}.mp4', 'scale=1080:608:flags=lanczos', False)

    def to_short(s, hook_=False):
        for a, b, st in (tl[:1] if hook_ else tl[1:]):
            if a - 0.05 <= s <= b + 0.05:
                return st + min(max(s, a), b) - a
        return None

    # ---- cadres: sample every 0.1 s of the short ----
    STEP = 0.1
    raw = []   # (t, state)
    for idx, (a, b, st) in enumerate(tl):
        for j in range(int((b - a) / STEP) + 1):
            s = a + j * STEP
            rs = review_state(s)
            sp = speaker(s)
            raw.append((st + j * STEP, rs, sp, idx == 0))
    shots, last = [], None
    def add(t0, m, who='A', zz=1.0):
        nonlocal last
        if last and last['m'] == m and last['who'] == who and last['z'] == zz:
            return
        last = {'t': round(t0, 2), 'm': m, 'who': who, 'z': zz}
        shots.append(last)
    # hook: the hook's speaker big, slow push inside the tile
    hs = max('AG', key=lambda k: sum(1 for x in raw if x[3] and x[2] == k))
    add(0, 'one', hs, 1.0)
    add(0.4, 'one', hs, 1.08)   # slow push in during the hook
    add(rew_t, 'two', 'A', 1.0)
    # pieces: review board / card runs (>= 1.5 s) win; elsewhere ~3.5 s blocks: speaker big when he talks the whole block,
    # every third block both (two) — "حركة التنقل حلوة جدا جدا"
    body = [x for x in raw if not x[3]]
    i, blk = 0, 0
    while i < len(body):
        t0, rs = body[i][0], body[i][1]
        j = i
        while j < len(body) and body[j][1] == rs and body[j][0] - body[j - 1 if j > i else j][0] < 0.5:
            j += 1
        run = body[j - 1][0] - t0
        if rs and run >= 1.5:
            who = rs[1] if rs[0] == 'card' else None
            if rs[0] == 'card':
                who = 'A' if who == 'G' else 'G'     # the long edit shows him + card -> the listener under it
                add(t0, 'card', who)
                i = j; continue
            # board: the speaker under it, switching when the speaker changes (>= 2 s)
            # (a gentle zoom change in that tile every ~4 s, so a long board never sits still)
            k0, zb = i, 1.0
            while k0 < j:
                sp = body[k0][2] or 'G'
                add(body[k0][0], 'board', sp, zb)
                k1 = k0
                while k1 < j and (body[k1][2] or sp) == sp and body[k1][0] - body[k0][0] < 4:
                    k1 += 1
                k0 = max(k1, k0 + 20)
                zb = 1.06 if zb == 1.0 else 1.0
            i = j; continue
        # tiles: block of 3.5 s (ends at the next review run)
        j = i
        while j < len(body) and body[j][0] - t0 < 3.5 and not (body[j][1] and j > i):
            j += 1
        sps = [x[2] for x in body[i:j] if x[2]]
        dom = max('AG', key=sps.count) if sps else 'A'
        share = sps.count(dom) / max(1, len(sps))
        if blk % 3 == 2 or share < 0.8:
            add(t0, 'two')
        else:
            prev_one = next((s for s in reversed(shots) if s['m'] == 'one' and s['who'] == dom), None)
            add(t0, 'one', dom, 1.0 if (prev_one and prev_one['z'] > 1) else 1.06)
        blk += 1
        i = j
    add(t - 0.01, 'two', 'A', 1.0)
    # shots shorter than 1.2 s flicker -> drop them
    clean = []
    for s in shots:
        if clean and s['t'] - clean[-1]['t'] < 1.2 and clean[-1]['t'] > rew_t + 0.01:
            clean[-1] = s if clean[-1]['m'] not in ('board', 'card') else clean[-1]
            continue
        clean.append(s)
    shots = clean

    # ---- notes of the long edit (enta_note) -> taped strips in the short ----
    notes = []
    for c in PLAN['cues']:
        if c['t'] == 'enta_note':
            s0 = to_short(c['src'])
            if s0 is not None:
                notes.append({'t': round(s0, 2), 'd': round(min(c['dur'], 4.5), 2), 'text': c['props']['text'], 'accent': c['props'].get('accent', 'orange')})

    # ---- captions ----
    words = []
    wj = json.load(open(OUT / f"words_{sh['idea']:02d}.json", encoding='utf8'))
    cap = CAPS.get(sh['idea']) or [' '.join(w['w'] for w in p_['words']) for p_ in wj]
    for i, (pc, text) in enumerate(zip(wj, cap)):
        a, b, st = tl[i]
        src_words = pc['words']
        if text.startswith('@L '):
            text = text[3:]
            src_words = [w for sn in LONG['sentences'] for w in sn['words']]
        ws = [w for w in src_words if w['end'] > a - 0.2 and w['start'] < b + 0.2]
        if not ws:
            continue
        cum, pos = [], 0
        for w in ws:
            cum.append((pos, w['start'], pos + len(w['w']), w['end'])); pos += len(w['w']) + 1
        tot = pos
        def t_at(fr_):
            x = fr_ * tot
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

    # ---- sfx: tape on the rewind, whoosh ONLY when the cadre itself moves (two / one / board / card, or another person),
    # NEVER on a zoom inside the same cadre (Aly 2026-10-21: "sfx على كل زوم ان و زوم اوت over… خليها لما الكدر نفسه بنحركه
    # مش زوم"), pop on notes, riser before the end card ----
    sfx = [{'t': round(rew_t - 0.05, 2), 'file': 'sfx/tape.wav', 'vol': 0.5}]
    for a_, b_ in zip(shots[1:], shots[2:]):
        if (a_['m'], a_['who'] if a_['m'] != 'two' else '') != (b_['m'], b_['who'] if b_['m'] != 'two' else ''):
            sfx.append({'t': max(0, round(b_['t'] - 0.06, 2)), 'file': f"sfx/whoosh_{1 + int(b_['t'] * 10) % 3}.wav", 'vol': 0.12 if b_['m'] in ('two', 'one') else 0.2})
    for nt in notes:
        sfx.append({'t': nt['t'], 'file': f"sfx/pop_{1 + int(nt['t'] * 10) % 3}.wav", 'vol': 0.22})
    sfx.append({'t': round(dur - 3.4, 2), 'file': 'sfx/riser.wav', 'vol': 0.2})

    props = dict(duration=round(dur, 2), no=n, total=TOTAL, head=sh['head'], src=f'projects/{CODE}/v{n:02d}.mp4', rev=f'projects/{CODE}/r{n:02d}.mp4',
                 srcW=STRIP[0], srcH=STRIP[1], tiles=TILES, face=FACE, shots=shots, notes=notes, hookEnd=round(rew_t, 2),
                 rewind={'t': round(rew_t, 2), 'd': REW, 'from': mmss(hook[1]), 'to': mmss(first)},
                 thumb=f'projects/{CODE}/thumb.jpg', qr=f'projects/{CODE}/qr.png', len='30:23', words=words, sfx=sfx)
    json.dump(props, open(OUT / f'props_{n:02d}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    json.dump({'segs': [{'a': a, 'b': b, 'st': st} for a, b, st in tl], 'dur': dur}, open(OUT / f'tl_{n:02d}.json', 'w'))
    print(f'short {n}: {dur:.1f} s, {len(shots)} shots, {len(notes)} notes, {len(words)} words, pieces {[(round(a, 2), round(b, 2)) for a, b in spans]}')


if __name__ == '__main__':
    for n in map(int, sys.argv[1:]):
        build(n)
