"""Turn transcript + plan into an editable edit (Mode 1: Claude edits everything).

Usage: python tools/build_edit.py projects/<code> [--plan work/plan.json] [--name review] [--vertical]
                                  [--render] [--overlays]
Reads : <proj>/input/<video>, <proj>/work/transcript.json, plan
Writes: motion-library/public/projects/<code>/{source.ext, edit_<name>.json, matte_<name>_<i>.webm}
        <proj>/output/<name>.mp4 (--render), <name>.xml (Premiere: File > Import), <name>.srt, overlays/ (--overlays)

plan (written by Claude, small):
{"cut": false,                      # false (default) = Aly already edited: keep everything as is
 "range": ["S010", "S025"],         # optional: only these sentences (shorts)
 "drop": ["S005"], "cut_words": [{"id": "S007", "from": 0, "to": 2}],   # only used when cut = true
 "fix": {"S011": "corrected caption text"},
 "quiet": [[114.4, 116.05]],        # source ranges with no captions/cues (his intro/outro clips)
 "video": "work/clean.mp4",         # optional: footage to use instead of the first file in input/ (same timing)
 "keep": [[13.6, 20.4], [33.0, 37.1]],   # optional: exact source ranges (s) in order -> overrides range/cut
 "append": [{"video": "input/cta.mp4", "transcript": "work/cta/transcript.json", "keep": [[1.6, 5.3]], "fit": "cover"}],
                                    # fit "cover" = clip already in the output aspect (vertical phone CTA in a 9:16 short)
 "cropX": 0.4, "vShift": 0.15,      # 9:16 only: speaker x in the 16:9 footage; lift footage so the face sits higher
 "roto": [{"start": 14.4, "file": "projects/<code>/roto_14.4.webm"}], "rotoScale": 0.62, "gShift": 0.3, "capBottom": 0.2,
                                    # 9:16 roto mode: speaker cut out (matte.py --fps 30) over a motion background
                                    # extra clips after the main part (e.g. CTA); cue anchor "A1:S001"
 "cues": [{"t": "keyword_pop", "at": "S003", "word": 1, "dur": 2.5, "props": {"text": "..."}},
          {"t": "zoom", "at": "S004", "dur": 1.5, "props": {"to": 1.2, "style": "punch"}}]}
"""
import json, os, subprocess, sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ML = ROOT / 'motion-library'
PAD_IN, PAD_OUT, MERGE_GAP = 0.06, 0.14, 0.30
SILENCE = 0.40  # pause between words longer than this is removed (like DaVinci ripple delete)
VIDEO_EXT = ('.mp4', '.mov', '.mkv', '.mxf')


def in_range(transcript, plan):
    ids = [x['id'] for x in transcript['sentences']]
    a, b = plan.get('range', [ids[0], ids[-1]])
    return set(ids[ids.index(a): ids.index(b) + 1])


def kept_runs(transcript, plan):
    keep = in_range(transcript, plan)
    if not plan.get('cut', False):  # Aly's own edit: one continuous run, no silence cutting
        return [[{**w, 'sid': s['id'], 'wi': i} for s in transcript['sentences'] if s['id'] in keep
                 for i, w in enumerate(s['words'])]]
    drop = set(plan.get('drop', [])) | {s['id'] for s in transcript['sentences'] if s['id'] not in keep}
    cuts = {}
    for c in plan.get('cut_words', []):
        cuts.setdefault(c['id'], set()).update(range(c['from'], c['to'] + 1))
    runs = []  # list of (start, end, [words])
    for s in transcript['sentences']:
        if s['id'] in drop:
            continue
        cur = []
        for i, w in enumerate(s['words']):
            if i in cuts.get(s['id'], ()):
                if cur:
                    runs.append(cur); cur = []
                continue
            if cur and w['start'] - cur[-1]['end'] > SILENCE:
                runs.append(cur); cur = []
            cur.append({**w, 'sid': s['id'], 'wi': i})
        if cur:
            runs.append(cur)
    return runs


def keep_segments(transcript, ranges, prefix=''):
    """plan.keep: exact source ranges [[a, b], ...] in play order; words inside each range go with it."""
    segs = []
    for a, b in ranges:
        ws = [{**w, 'sid': prefix + s['id'], 'wi': i} for s in transcript['sentences'] for i, w in enumerate(s['words'])
              if a - 0.05 <= w['start'] < b - 0.05]
        segs.append({'a': a, 'b': b, 'words': ws})
    return segs


def arg(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


def render_overlays(code, cues, edit_json, out_dir, fps=30, vertical=False):
    """One alpha .mov per graphic cue (same names as the XML) + one captions .mov. Zoom = camera move on V1 (no file)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    d = json.load(open(edit_json, encoding='utf8'))
    last = round(d['duration'] * fps) - 1
    for layer, jobs in (('motion', [{'out': str((out_dir / cue_name(code, i, c)).resolve()), 'a': round(c['at'] * fps),
                                     'b': min(round((c['at'] + c['dur']) * fps) - 1, last)}
                                    for i, c in enumerate(cues) if c['t'] not in ('zoom', 'sfx')]),
                        ('captions', [{'out': str((out_dir / f'{code}_captions.mov').resolve()), 'a': 0, 'b': last}])):
        props = edit_json.with_name(f'edit_{layer}.json'); jf = edit_json.with_name(f'jobs_{layer}.json')
        json.dump({**d, 'layer': layer}, open(props, 'w', encoding='utf8'), ensure_ascii=False)
        json.dump(jobs, open(jf, 'w', encoding='utf8'))
        subprocess.run(['node', 'overlays.mjs', 'edit-v' if vertical else 'edit', str(props.resolve()), str(jf.resolve())],
                       cwd=ML, check=True)


def apply_fixes(words, fix):
    """plan.fix = {"S011": "corrected text of the KEPT words"}. Caption text only; timing is spread over the
    kept words' time (1:1 if counts match, else proportional to character length)."""
    out, i = [], 0
    while i < len(words):
        sid = words[i]['sid']
        j = i
        while j < len(words) and words[j]['sid'] == sid:
            j += 1
        group = words[i:j]
        if sid in fix:
            new = fix[sid].split()
            if len(new) == len(group):
                group = [{**w, 'w': n} for w, n in zip(group, new)]
            elif new:
                a, b = group[0]['start'], group[-1]['end']
                tot = sum(len(n) + 1 for n in new); t = a; g = []
                for n in new:
                    d = (b - a) * (len(n) + 1) / tot
                    g.append({'w': n, 'start': round(t, 3), 'end': round(t + d, 3), 'sid': sid, 'wi': -1}); t += d
                group = g
        out += group
        i = j
    return out


def cue_name(code, i, c):
    return f"{code}_{i + 1:02d}_{c['t']}_{c['at']:07.2f}".replace('.', '-') + '.mov'


def build(proj: Path, render=False):
    code = proj.name
    name = arg('--name', 'review')
    vertical = '--vertical' in sys.argv
    tr = json.load(open(proj / 'work/transcript.json', encoding='utf8'))
    plan = json.load(open(proj / arg('--plan', 'work/plan.json'), encoding='utf8'))
    video = proj / plan['video'] if plan.get('video') else next(
        p for p in sorted((proj / 'input').iterdir()) if p.suffix.lower() in VIDEO_EXT)
    fps = 30

    # 1. segments in source time, merged when the gap is tiny (keeps natural flow).
    segs = []
    if plan.get('keep'):  # exact ranges chosen by Claude (Aly's edit has no silences; Whisper gaps = lost words)
        segs = keep_segments(tr, plan['keep'])
    for run in ([] if segs else kept_runs(tr, plan)):
        a, b = max(0, run[0]['start'] - PAD_IN), min(tr['duration'], run[-1]['end'] + PAD_OUT)
        if segs and a - segs[-1]['b'] < MERGE_GAP and run[0]['start'] >= segs[-1]['b'] - PAD_OUT:
            segs[-1]['b'] = b; segs[-1]['words'] += run
        else:
            if segs and a < segs[-1]['b']:
                a = segs[-1]['b']
            segs.append({'a': a, 'b': b, 'words': list(run)})
    if not plan.get('cut', False) and 'range' not in plan and 'keep' not in plan and segs:
        segs[0]['a'], segs[-1]['b'] = 0.0, tr['duration']
    main_end = len(segs)
    for k, ap in enumerate(plan.get('append', []), 1):  # extra clips (CTA ...) with their own source
        atr = json.load(open(proj / ap['transcript'], encoding='utf8'))
        for sg in keep_segments(atr, ap['keep'], prefix=f'A{k}:'):
            sg['video'] = proj / ap['video']; sg['fit'] = ap.get('fit'); segs.append(sg)
    tl = 0.0
    for s in segs:
        s['tl'] = tl; tl += s['b'] - s['a']
    duration = round(tl, 3)

    def to_tl(t):
        for s in segs[:main_end]:
            if s['a'] <= t <= s['b']:
                return s['tl'] + t - s['a']
        return None

    words = []
    for s in segs:
        for w in s['words']:
            words.append({'w': w['w'], 'start': round(s['tl'] + max(w['start'], s['a']) - s['a'], 3),
                          'end': round(s['tl'] + min(w['end'], s['b']) - s['a'], 3), 'sid': w['sid'], 'wi': w['wi']})
    for a, b in plan.get('quiet', []):  # Aly's intro/outro clips: no captions, no cues
        words = [w for w in words if not (a <= w['start'] < b)]
    full = {x['id']: len(x['words']) for x in tr['sentences']}
    for sid in {w['sid'] for w in words if w['sid'] in plan.get('fix', {}) and ':' not in w['sid']}:
        kept, nf = sum(w['sid'] == sid for w in words), len(plan['fix'][sid].split())
        if kept < full.get(sid, 0) and abs(nf - full[sid]) < abs(nf - kept):  # whole-sentence fix on a cut sentence
            print(f'WARN fix {sid} is for the whole sentence but only part is kept -> give the kept part only')
    raw_words = words  # cue anchors use original word indexes
    words = apply_fixes(words, plan.get('fix', {}))

    # 2. cues -> timeline seconds
    cues = []
    for c in plan.get('cues', []):
        if 'src' in c:  # anchor = main-video source second (must be inside a kept range)
            at = to_tl(c['src'])
        else:
            hit = next((w for w in raw_words if w['sid'] == c['at'] and w['wi'] >= c.get('word', 0)), None)
            at = hit['start'] if hit else None
        if at is None:
            print('WARN cue skipped (anchor dropped):', c); continue
        if any(a - 0.05 < at < b for a, b in plan.get('quiet', [])) or any(at < a < at + c.get('dur', 2.5) - 0.05 for a, b in plan.get('quiet', [])):
            print('WARN cue touches a quiet range (intro/outro):', c)
        cue = {'t': c['t'], 'at': round(at, 3), 'dur': c.get('dur', 2.5), 'props': dict(c.get('props', {}))}
        if c['t'] == 'portal_world':  # needs Aly cut out for exactly this source range
            seg = next(s for s in segs[:main_end] if s['tl'] <= cue['at'] < s['tl'] + s['b'] - s['a'])
            src = seg['a'] + cue['at'] - seg['tl']
            cue['dur'] = min(cue['dur'], seg['b'] - src)  # must stay inside one continuous segment
            cue['props'].update(cropX=plan.get('cropX', 0.5), vShift=plan.get('vShift', 0), footageStart=round(src, 3), matte=f'projects/{code}/matte_{name}_{int(src * 1000)}.webm',
                                footage=f'projects/{code}/source{video.suffix.lower()}')
            cue['_matte'] = (round(src, 3), round(cue['dur'], 3))
        cues.append(cue)

    # No two overlay graphics at once: a graphic ends when the next one starts (zoom/icon_pop may overlap).
    cues.sort(key=lambda c: c['at'])
    solo = [c for c in cues if c['t'] not in ('zoom', 'icon_pop', 'green_clip', 'sfx', 'enta_glitch', 'enta_stickers', 'enta_leak', 'enta_bubble', 'enta_note')]
    for a, b in zip(solo, solo[1:]):
        if a['at'] + a['dur'] > b['at'] - 0.1:
            a['dur'] = max(0.8, round(b['at'] - 0.1 - a['at'], 3))

    # 3. Remotion props + hard-linked source (no extra disk space on same drive)
    pub = ML / 'public' / 'projects' / code
    pub.mkdir(parents=True, exist_ok=True)
    src_pub = pub / ('source' + video.suffix.lower())
    if not src_pub.exists():
        try:
            os.link(video, src_pub)
        except OSError:
            import shutil; shutil.copy2(video, src_pub)
    for s in segs:
        if 'video' in s:  # appended clip -> its own public copy
            p = pub / ('app_' + s['video'].name)
            if not p.exists():
                try:
                    os.link(s['video'], p)
                except OSError:
                    import shutil; shutil.copy2(s['video'], p)
            s['pub'] = f'projects/{code}/{p.name}'
    edit = {'source': f'projects/{code}/{src_pub.name}', 'fps': fps, 'duration': duration, 'layer': 'all',
            'pack': plan.get('pack', 'charcoal'), 'cropX': plan.get('cropX', 0.5), 'vShift': plan.get('vShift', 0), 'roto': plan.get('roto', []), 'rotoScale': plan.get('rotoScale', 0.62),
            'gShift': plan.get('gShift', 0), 'capBottom': plan.get('capBottom', -1), 'captions': plan.get('captions', True),
            'segments': [{'src': round(s['a'], 3), 'tl': round(s['tl'], 3), 'len': round(s['b'] - s['a'], 3),
                          **({'source': s['pub']} if 'pub' in s else {}), **({'fit': s['fit']} if s.get('fit') else {})} for s in segs],
            'words': [{k: w[k] for k in ('w', 'start', 'end')} for w in words], 'cues': cues}
    for c in cues:
        if c['t'] == 'cta_endcard' and c['props'].get('qrUrl'):
            import qrcode, hashlib
            qn = 'qr_' + hashlib.md5(c['props']['qrUrl'].encode()).hexdigest()[:8] + '.png'
            qrcode.make(c['props']['qrUrl'], border=2).save(pub / qn)
            c['props']['qr'] = f'projects/{code}/{qn}'
    for i, c in enumerate(cues):
        if '_matte' in c:
            m = pub / Path(c['props']['matte']).name  # keyed by source time (stable after sorting)
            if not m.exists():
                subprocess.run([sys.executable, str(ROOT / 'tools/matte.py'), str(video), str(c['_matte'][0]), str(c['_matte'][1]), str(m)], check=True)
            del c['_matte']
    ej = pub / f'edit_{name}.json'
    json.dump(edit, open(ej, 'w', encoding='utf8'), ensure_ascii=False)

    out = proj / 'output'
    out.mkdir(exist_ok=True)
    write_srt(words, out / f'{name}.srt')
    write_xml(video, segs, cues, fps, duration, out / f'{name}.xml', code, vertical)
    kept = sum(s['b'] - s['a'] for s in segs)
    print(f'{len(segs)} segments, {kept:.1f}s kept of {tr["duration"]:.1f}s, {len(cues)} cues -> {ej}')
    if '--overlays' in sys.argv:
        render_overlays(code, cues, ej, out / 'overlays', fps, vertical)
    if render:
        subprocess.run(['npx', 'remotion', 'render', 'edit-v' if vertical else 'edit', str((out / f'{name}.mp4').resolve()),
                        f'--props={ej.resolve()}', '--crf=23'],
                       cwd=ML, check=True, shell=os.name == 'nt')


def write_srt(words, path, max_words=6):
    def ts(t):
        ms = int(round(t * 1000)); return f'{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}'
    lines, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        gap = words[i + 1]['start'] - w['end'] if i + 1 < len(words) else 9
        if len(cur) >= max_words or gap > 0.45:
            lines.append(cur); cur = []
    path.write_text('\n'.join(f"{i}\n{ts(l[0]['start'])} --> {ts(l[-1]['end'])}\n{' '.join(w['w'] for w in l)}\n"
                              for i, l in enumerate(lines, 1)), encoding='utf8')


def write_xml(video, segs, cues, fps, duration, path, code, vertical=False):
    """FCP7 XML (xmeml v4) — Premiere: File > Import. V1+A1/A2 = kept speech (zoom cues = V1 split into scaled
    pieces), V2 = motion overlays, V3 = captions overlay. 9:16: footage scaled to fill the height (centered crop)."""
    f = lambda s: int(round(s * fps))
    W, H = (1080, 1920) if vertical else (1920, 1080)
    base = 100 * 1920 / 1080 if vertical else 100.0
    rate = f'<rate><timebase>{fps}</timebase><ntsc>FALSE</ntsc></rate>'
    url = lambda p: 'file://localhost/' + Path(p).resolve().as_posix().replace(' ', '%20')
    files, fdefs = {}, {}

    def fileref(p):
        if p not in files:
            files[p] = f'src{len(files)}'
            return (f'<file id="{files[p]}"><name>{escape(Path(p).name)}</name><pathurl>{escape(url(p))}</pathurl>{rate}'
                    f'<media><video><samplecharacteristics><width>1920</width><height>1080</height></samplecharacteristics></video>'
                    f'<audio><channelcount>2</channelcount></audio></media></file>')
        return f'<file id="{files[p]}"/>'

    def scale_at(t):  # zoom level at timeline time (piecewise constant = punch cuts)
        z = 1.0
        for c in cues:
            if c['t'] == 'zoom' and c['at'] <= t < c['at'] + c['dur']:
                z = max(z, c['props'].get('to', 1.18))
        return z

    zb = sorted({x for c in cues if c['t'] == 'zoom' for x in (f(c['at']), f(c['at'] + c['dur']))})
    v1, a1, a2 = [], [], []
    for i, s in enumerate(segs):
        src = s.get('video', video)
        st, en, si = f(s['tl']), f(s['tl'] + s['b'] - s['a']), f(s['a'])
        cuts = [st] + [x for x in zb if st < x < en] + [en]
        for k, (p, q) in enumerate(zip(cuts, cuts[1:])):
            sc = base * scale_at((p + q) / 2 / fps)
            motion = (f'<filter><effect><name>Basic Motion</name><effectid>basic</effectid><effectcategory>motion</effectcategory>'
                      f'<effecttype>motion</effecttype><mediatype>video</mediatype><parameter><parameterid>scale</parameterid>'
                      f'<name>Scale</name><valuemin>0</valuemin><valuemax>1000</valuemax><value>{sc:.2f}</value></parameter></effect></filter>')
            v1.append(f'<clipitem id="v{i}_{k}"><name>{escape(Path(src).name)}</name>{rate}<start>{p}</start><end>{q}</end>'
                      f'<in>{si + p - st}</in><out>{si + q - st}</out>{fileref(src)}{motion}</clipitem>')
        for trk, ch in ((a1, 1), (a2, 2)):
            trk.append(f'<clipitem id="a{ch}_{i}"><name>{escape(Path(src).name)}</name>{rate}<start>{st}</start><end>{en}</end>'
                       f'<in>{si}</in><out>{si + en - st}</out>{fileref(src)}<sourcetrack><mediatype>audio</mediatype>'
                       f'<trackindex>{ch}</trackindex></sourcetrack></clipitem>')

    def ov(cid, name, st, en):
        p = path.parent / 'overlays' / name
        return (f'<clipitem id="{cid}"><name>{name}</name>{rate}<start>{st}</start><end>{en}</end><in>0</in><out>{en - st}</out>'
                f'<file id="f_{cid}"><name>{name}</name><pathurl>{escape(url(p))}</pathurl>{rate}</file></clipitem>')
    v2 = [ov(f'm{i}', cue_name(code, i, c), f(c['at']), min(f(c['at'] + c['dur']), f(duration)))
          for i, c in enumerate(cues) if c['t'] not in ('zoom', 'sfx')]
    v3 = [ov('cap', f'{code}_captions.mov', 0, f(duration))]
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n'
           f'<xmeml version="4"><sequence id="seq"><name>{escape(code)}_{path.stem}</name>'
           f'<duration>{f(duration)}</duration>{rate}<media><video><format><samplecharacteristics><width>{W}</width><height>{H}</height>'
           f'{rate}</samplecharacteristics></format><track>{"".join(v1)}</track><track>{"".join(v2)}</track><track>{"".join(v3)}</track></video>'
           f'<audio><track>{"".join(a1)}</track><track>{"".join(a2)}</track></audio></media></sequence></xmeml>')
    path.write_text(xml, encoding='utf8')


if __name__ == '__main__':
    build(Path(sys.argv[1]).resolve(), '--render' in sys.argv)
