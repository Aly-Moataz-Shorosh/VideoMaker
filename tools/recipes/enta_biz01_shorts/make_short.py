"""Build one meet-short (vertical short from biz ep01; copied from the cs ep01 recipe): python make_short.py 1 [2 ...]
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
CODE = 'entabiz01s'
PUB = ML / 'public' / 'projects' / CODE
SRC = P / 'input' / '2026-10-27 16-06-01.mp4'
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
CROP_Y = 282                      # strip of the Meet frame that holds both tiles (side by side from 187.5 s: y 288..814)
STRIP = (1920, 538)
SIDE = PLAN['meet']['phases'][-1]  # the side-by-side layout (every short is after it)
TILES = {k: [SIDE[k][0], SIDE[k][1] - CROP_Y, SIDE[k][2], SIDE[k][3]] for k in 'AG'}
FACE = {'A': [0.49, 0.44], 'G': [0.49, 0.48]}   # face centres of the long plan
# Meet UI in the raw strip, covered like the long edit: name tags, the crop button (blur), Karim's speaking dots (clean patch)
PATCHES = json.load(open(P / 'work' / 'patches.json'))['G2']
def masks_for(sec):
    pt = [q for q in PATCHES if q[0] <= sec][-1][1]
    return [dict(who='G', box=[30, 776 - CROP_Y, 110, 26], tag='كريم تامر'), dict(who='A', box=[978, 776 - CROP_Y, 110, 26], tag='علي شُرُش'),
            dict(who='A', box=[1858, 772 - CROP_Y, 40, 36]), dict(who='G', box=[908, 290 - CROP_Y, 44, 44], patch=pt.replace('entabiz01/', CODE + '/'))]


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
        if c['t'] == 'biz_free' and c['src'] <= s < c['src'] + c['dur']:
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

    # ---- real work of the guest's business on top (Courzerve short, Aly 2026-10-31): item = pic / posts / clip (cut from the
    # campaign video into the short's public folder); its own cadre 'work' (card on top, the speaker under it), wins over the
    # cadres it covers; after it the cadre that would be on then comes back ----
    work = []
    WEB = PUB.parents[1] / 'projects' / 'entabiz01' / 'web' / 'courzerve'
    if not WEB.exists():
        WEB = P / 'motion_public' / 'entabiz01' / 'web' / 'courzerve'
    (PUB / 'cz').mkdir(exist_ok=True)
    if sh.get('work') and not (PUB / 'cz' / 'logo.jpg').exists():
        (PUB / 'cz' / 'logo.jpg').write_bytes((WEB / 'logo.jpg').read_bytes())
    for wa, wb, it in sh.get('work', []):
        for hk in (True, False):
            s0, s1 = to_short(wa, hk), to_short(wb, hk)
            if s0 is None and s1 is None:
                continue
            seg = tl[0] if hk else next(x for x in tl[1:] if x[0] - 0.05 <= (wa if s0 is not None else wb) <= x[1] + 0.05)
            s0 = s0 if s0 is not None else seg[2]
            s1 = s1 if s1 is not None else seg[2] + seg[1] - seg[0]
            if s1 - s0 < 0.8:
                continue
            w = {'t': round(s0, 2), 'd': round(s1 - s0, 2), 'kind': it['kind'], 'label': it['label'], 'pos': it.get('pos', 'bottom')}
            if it['kind'] == 'clip':
                off = 0 if to_short(wa, hk) is not None else max(0, seg[0] - wa)   # the hook / a piece may start inside the item
                name = f"cz/c{it['cam']}_{it['frm'] + off:.1f}_{s1 - s0:.1f}.mp4"
                if not (PUB / name).exists():
                    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f"{it['frm'] + off:.2f}", '-t', f'{s1 - s0 + 0.6:.2f}', '-i', str(WEB / f"campaign_{it['cam']}.mp4"),
                                    '-an', '-vf', 'fps=30,scale=1052:-2:flags=lanczos', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', str(PUB / name)], check=True)
                w['src'] = f'projects/{CODE}/{name}'
            else:
                srcs = it.get('srcs') or [it['src']]
                for f in srcs:
                    if not (PUB / 'cz' / f).exists():
                        (PUB / 'cz' / f).write_bytes((WEB / f).read_bytes())
                w['srcs'] = [f'projects/{CODE}/cz/{f}' for f in srcs]
            work.append(w)
    work.sort(key=lambda w: w['t'])
    for w in work:
        a_, b_ = w['t'], w['t'] + w['d']
        at_end = [s for s in shots if s['t'] <= b_ + 0.01]
        back = dict(at_end[-1]) if at_end else {'m': 'two', 'who': 'A', 'z': 1.0}
        sp = [x[2] for x in raw if a_ <= (x[0] if not x[3] else x[0]) < b_ and x[2]]
        who = max('AG', key=sp.count) if sp else 'G'
        shots = [s for s in shots if not (a_ - 0.01 <= s['t'] <= b_ + 0.01)]
        shots.append({'t': round(a_, 2), 'm': 'work', 'who': who, 'z': 1.0})
        if not any(abs(o['t'] - b_) < 0.05 for o in work):          # next item starts right here -> no flash back
            back['t'] = round(b_, 2); shots.append(back)
        shots.sort(key=lambda s: s['t'])
    if work:   # a shot that is replaced within 0.4 s only flickers
        shots = [s for j, s in enumerate(shots) if j + 1 == len(shots) or shots[j + 1]['t'] - s['t'] >= 0.4 or s['t'] < 0.01]

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
        if (a_['m'], a_['who'] if a_['m'] != 'two' else '') != (b_['m'], b_['who'] if b_['m'] != 'two' else '') and b_['m'] != 'work':
            sfx.append({'t': max(0, round(b_['t'] - 0.06, 2)), 'file': f"sfx/whoosh_{1 + int(b_['t'] * 10) % 3}.wav", 'vol': 0.12 if b_['m'] in ('two', 'one') else 0.2})
    for w in work:
        sfx.append({'t': round(w['t'], 2), 'file': f"sfx/pop_{1 + int(w['t'] * 10) % 3}.wav", 'vol': 0.2})
    for nt in notes:
        sfx.append({'t': nt['t'], 'file': f"sfx/pop_{1 + int(nt['t'] * 10) % 3}.wav", 'vol': 0.22})
    sfx.append({'t': round(dur - 3.4, 2), 'file': 'sfx/riser.wav', 'vol': 0.2})

    props = dict(duration=round(dur, 2), no=n, total=TOTAL, head=sh['head'], src=f'projects/{CODE}/v{n:02d}.mp4', rev=f'projects/{CODE}/r{n:02d}.mp4',
                 srcW=STRIP[0], srcH=STRIP[1], tiles=TILES, face=FACE, shots=shots, notes=notes, hookEnd=round(rew_t, 2),
                 rewind={'t': round(rew_t, 2), 'd': REW, 'from': mmss(hook[1]), 'to': mmss(first)},
                 thumb=f'projects/{CODE}/thumb.jpg' if (PUB / 'thumb.jpg').exists() else '', qr=f'projects/{CODE}/qr.png' if (PUB / 'qr.png').exists() else '',
                 len='45:03', words=words, sfx=sfx, work=work, workLogo=(f'projects/{CODE}/cz/logo.jpg' if work else ''), tag='انت بتشتغل ايه · رواد الأعمال', masks=masks_for(sh['hook'][0]))
    json.dump(props, open(OUT / f'props_{n:02d}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    json.dump({'segs': [{'a': a, 'b': b, 'st': st} for a, b, st in tl], 'dur': dur}, open(OUT / f'tl_{n:02d}.json', 'w'))
    print(f'short {n}: {dur:.1f} s, {len(shots)} shots, {len(notes)} notes, {len(words)} words, pieces {[(round(a, 2), round(b, 2)) for a, b in spans]}')


if __name__ == '__main__':
    for n in map(int, sys.argv[1:]):
        build(n)
