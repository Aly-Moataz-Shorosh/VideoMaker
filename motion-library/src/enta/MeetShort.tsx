import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {fontCss} from '../blocks/theme';
import {Badge, Caps, Frame, Pal, Rewind} from '../stage/kit';
import {AR, EN, spr} from '../film/kit';
import {E, Grain, Hi, Tape} from './kit';
import {MeetBg} from './Meet';

// Vertical shorts from an ONLINE episode (cs ep01, Aly 2026-10-21): style 14 (calm dark bg, webcam tiles, cadre switching)
// turned 9:16. Headline + captions like the lecture shorts (style 13: hook sentence first, rewind, then the idea), the full
// episode thumbnail + QR on the side and big at the end (no CTA clip). Props from the episode's work/scripts/make_short.py.
//   src = the short's own strip of the Meet recording (both tiles, hook | rewind | pieces | tail, with his audio)
//   rev = the same timeline cut from the approved long edit (review_02, 1080x608): used where it shows a board or a card
// Cadres (shots): two = both stacked (Aly top) · one = the speaker big · board / card = the long edit's board (or person + card)
// on top and `who` under it (board: the speaker; card: the listener). Zoom only inside a tile, <= 1.08 (style 14 rule).
const shot = z.object({t: z.number(), m: z.enum(['two', 'one', 'board', 'card', 'work']), who: z.enum(['A', 'G']).default('A'), z: z.number().default(1)});
export const meetShortSchema = z.object({
  duration: z.number().default(5),
  no: z.number().default(1),
  total: z.number().default(17),
  tag: z.string().default('انت بتشتغل ايه · حاسبات'),
  head: z.string().default(''),
  src: z.string().default(''),
  rev: z.string().default(''),
  srcW: z.number().default(1920),
  srcH: z.number().default(496),
  tiles: z.record(z.string(), z.array(z.number())).default({A: [961, 8, 910, 470], G: [12, 8, 910, 470]}),
  face: z.record(z.string(), z.array(z.number())).default({A: [0.5, 0.5], G: [0.47, 0.4]}),
  shots: z.array(shot).default([]),
  notes: z.array(z.object({t: z.number(), d: z.number(), text: z.string(), accent: z.string().default('orange')})).default([]),
  hookEnd: z.number().default(0),
  rewind: z.object({t: z.number(), d: z.number(), from: z.string(), to: z.string()}).nullable().default(null),
  thumb: z.string().default(''),
  qr: z.string().default(''),
  len: z.string().default('30:23'),
  words: z.array(z.object({w: z.string(), start: z.number(), end: z.number(), hl: z.boolean().optional()})).default([]),
  sfx: z.array(z.object({t: z.number(), file: z.string(), vol: z.number().default(0.3)})).default([]),
  // Meet UI in the raw strip covered like in the long edit (biz ep01 2026-10-28): tag = our paper name tag, patch = a clean crop
  // (Meet's speaking dots), neither = a soft blur. box = strip px [x, y, w, h]
  masks: z.array(z.object({who: z.enum(['A', 'G']), box: z.array(z.number()), tag: z.string().optional(), patch: z.string().optional()})).default([]),
  // the guest's REAL work on top while he names it (biz ep01 Courzerve short, Aly 2026-10-31): clip = a cut of their campaign video,
  // pic = one design, posts = several designs fanned out; label = paper chip (*word* = highlighted); cadre 'work' = card on top + speaker under
  work: z.array(z.object({t: z.number(), d: z.number(), kind: z.enum(['clip', 'pic', 'posts']), label: z.string().default(''), pos: z.enum(['bottom', 'top']).default('bottom'),
    src: z.string().optional(), srcs: z.array(z.string()).optional()})).default([]),
  workLogo: z.string().default(''),
});
type Props = z.infer<typeof meetShortSchema>;
type Shot = z.infer<typeof shot>;
type R = {x: number; y: number; w: number; h: number; o: number};

export const PAL: Pal = {box: E.paper, boxInk: E.orange, bar: [E.orange, E.mustard, E.blue], now: E.mustard, hl: E.orange};
const TOP = 392, BOT = 1516, CAP = 1532, BLEND = 12, END = 3.2;
const smooth = (x: number) => x * x * (3 - 2 * x);
const lerp = (a: R, b: R, k: number): R => ({x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, w: a.w + (b.w - a.w) * k, h: a.h + (b.h - a.h) * k, o: a.o + (b.o - a.o) * k});
const REV: R = {x: 0, y: TOP, w: 1080, h: 608, o: 1};

// where each person's tile sits in a cadre (Aly top / guest bottom, like Aly left / guest right in the long video)
const rectOf = (s: Shot, p: 'A' | 'G'): R => {
  const half = (BOT - TOP - 8) / 2;
  const two = p === 'A' ? {x: 0, y: TOP, w: 1080, h: half, o: 1} : {x: 0, y: TOP + half + 8, w: 1080, h: half, o: 1};
  const away = {...two, y: p === 'A' ? TOP - half - 80 : 1920 + 40, o: 0};
  if (s.m === 'two') return two;
  if (s.who !== p) return away;
  if (s.m === 'one') return {x: 0, y: TOP + (BOT - TOP - 820) / 2, w: 1080, h: 820, o: 1};
  return {x: 0, y: TOP + 608 + 10, w: 1080, h: BOT - TOP - 618, o: 1}; // under the board / card
};

export const MeetShort: React.FC<Props> = (p) => {
  const {duration, no, total, tag, head, src, rev, srcW, srcH, tiles, face, shots, notes, hookEnd, rewind, thumb, qr, len, words, sfx, masks, work, workLogo} = p;
  const {fps} = useVideoConfig();
  const now = useCurrentFrame();
  const fr = (s: number) => Math.round(s * fps);
  const D = fr(duration);
  // current + previous shot -> blend
  let i = -1;
  for (let k = 0; k < shots.length; k++) if (fr(shots[k].t) <= now) i = k;
  const cur: Shot = shots[i] ?? {t: 0, m: 'two', who: 'A', z: 1};
  const prev: Shot = i > 0 ? shots[i - 1] : cur;
  const since = i >= 0 ? now - fr(cur.t) : 999;
  const k = smooth(Math.min(1, since / BLEND));
  const kz = smooth(Math.min(1, since / (BLEND * 2.5)));
  const isRev = (s: Shot) => s.m === 'board' || s.m === 'card' || s.m === 'work';
  const isLong = (s: Shot) => s.m === 'board' || s.m === 'card';
  const revK = (isLong(prev) ? 1 - k : 0) + (isLong(cur) ? k : 0);
  const workK = (prev.m === 'work' ? 1 - k : 0) + (cur.m === 'work' ? k : 0);
  const wk = [...work].reverse().find((w) => now >= fr(w.t) - 2 && now < fr(w.t + w.d) + BLEND);

  const tile = (pp: 'A' | 'G') => {
    const r = lerp(rectOf(prev, pp), rectOf(cur, pp), k);
    if (r.o <= 0.01) return null;
    const t = tiles[pp], [fx, fy] = face[pp];
    const zz = (prev.who === pp || prev.m === 'two' ? prev.z : 1) + ((cur.who === pp || cur.m === 'two' ? cur.z : 1) - (prev.who === pp || prev.m === 'two' ? prev.z : 1)) * kz;
    const s = Math.max(r.w / t[2], r.h / t[3]) * zz;
    const left = Math.min(-t[0] * s, Math.max(r.w - (t[0] + t[2]) * s, r.w / 2 - (t[0] + fx * t[2]) * s));
    const top = Math.min(-t[1] * s, Math.max(r.h - (t[1] + t[3]) * s, r.h * 0.45 - (t[1] + fy * t[3]) * s));
    return (
      <div key={pp} style={{position: 'absolute', left: r.x + 14, top: r.y, width: r.w - 28, height: r.h, opacity: r.o, borderRadius: 22, overflow: 'hidden',
        boxShadow: '0 22px 50px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.06)', background: '#0c0d11'}}>
        <OffthreadVideo src={staticFile(src)} muted style={{position: 'absolute', left: left - 14, top, width: srcW * s, height: srcH * s, maxWidth: 'none'}} />
        {masks.filter((m) => m.who === pp).map((m, j) => {
          const L = left - 14 + m.box[0] * s, T = top + m.box[1] * s, w = m.box[2] * s, h = m.box[3] * s;
          if (m.tag) return <div key={j} style={{position: 'absolute', left: L - 6, top: T + h / 2, transform: 'translateY(-50%) rotate(-2deg)', background: '#EFE6D2', color: '#1C2030',
            fontWeight: 900, fontFamily: AR, fontSize: Math.max(16, h * 0.95), padding: `${h * 0.12}px ${h * 0.5}px`, borderRadius: 6, whiteSpace: 'nowrap', border: '3px solid #FBF7EE',
            boxShadow: '0 4px 10px rgba(0,0,0,.4)', direction: 'rtl'}}>{m.tag}</div>;
          if (m.patch) return <Img key={j} src={staticFile(m.patch)} style={{position: 'absolute', left: L, top: T, width: w, height: h,
            maskImage: 'radial-gradient(circle, black 55%, transparent 72%)', WebkitMaskImage: 'radial-gradient(circle, black 55%, transparent 72%)'}} />;
          return <div key={j} style={{position: 'absolute', left: L, top: T, width: w, height: h, borderRadius: h / 2, backdropFilter: 'blur(7px)', WebkitBackdropFilter: 'blur(7px)'}} />;
        })}
      </div>
    );
  };

  // the bottom note of the long video, as a taped paper strip on the seam between the tiles (or under the big tile)
  const nt = notes.find((n) => now >= fr(n.t) && now < fr(n.t + n.d));
  const note = () => {
    if (!nt || isRev(cur)) return null;
    const a = now - fr(nt.t), b = fr(nt.t + nt.d) - now;
    const q = smooth(Math.min(1, a / 9, b / 9));
    const y = cur.m === 'one' ? TOP + (BOT - TOP + 820) / 2 - 40 : (TOP + BOT) / 2 - 46;
    const acc = (E as Record<string, string>)[nt.accent] ?? E.orange;
    return (
      <div style={{position: 'absolute', left: 0, right: 0, top: y, display: 'flex', justifyContent: 'center', opacity: q, transform: `translateY(${(1 - q) * 40}px)`}}>
        <div style={{position: 'relative', background: E.paper, color: E.ink, padding: '10px 30px 14px', borderRadius: 8, fontFamily: AR, fontSize: 46, fontWeight: 900,
          maxWidth: 960, textAlign: 'center', direction: 'rtl', border: `6px solid ${E.white}`, boxShadow: '0 12px 26px rgba(0,0,0,.5)', overflow: 'hidden',
          transform: `rotate(${-1.5 + (1 - q) * 4}deg)`}}>
          <Grain opacity={0.28} seed={51} />
          <span style={{position: 'relative'}}><Hi text={nt.text} color={acc} /></span>
          <Tape w={110} rot={-12} style={{top: -24, right: -26}} />
        </div>
      </div>
    );
  };

  return (
    <AbsoluteFill style={{background: '#121419'}}>
      <style>{fontCss}</style>
      <MeetBg frame={now} />
      {tile('A')}
      {tile('G')}
      {revK > 0.01 && rev ? (
        <div style={{position: 'absolute', left: REV.x + 14, top: REV.y + (1 - revK) * -40, width: REV.w - 28, height: REV.h - 16, opacity: revK, borderRadius: 22,
          overflow: 'hidden', boxShadow: '0 22px 50px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.08)'}}>
          <OffthreadVideo src={staticFile(rev)} muted style={{position: 'absolute', left: -14, top: -8, width: 1080, height: 608, maxWidth: 'none'}} />
        </div>
      ) : null}
      {workK > 0.01 && wk ? (
        <div style={{position: 'absolute', left: REV.x + 14, top: REV.y + (1 - workK) * -40, width: REV.w - 28, height: REV.h - 16, opacity: workK, borderRadius: 22,
          overflow: 'hidden', boxShadow: '0 22px 50px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.08)', background: '#0c0d11'}}>
          <Sequence key={wk.t} from={fr(wk.t)} layout="none"><WorkCard w={wk} logo={workLogo} /></Sequence>
        </div>
      ) : null}
      {note()}
      {rewind ? <Sequence from={fr(rewind.t)} durationInFrames={fr(rewind.d)} layout="none"><Rewind dur={fr(rewind.d)} from={rewind.from} to={rewind.to} /></Sequence> : null}
      <Caps words={words} top={CAP} pal={PAL} />
      <Frame no={no} total={total} head={head} dur={D} hookEnd={fr(hookEnd)} tag={tag} pal={PAL} />
      {thumb ? <Badge thumb={thumb} qr={qr} at={fr(hookEnd + (rewind?.d ?? 0))} big={D + 999} label="الحلقة كاملة" sub="على قناتي في يوتيوب" len={len} y0={TOP + 18}
        hide={Math.max(revK, workK, Math.min(1, (now - (D - fr(END))) / 8))} /> : null}
      {thumb ? <Sequence from={D - fr(END)} layout="none"><EndCard thumb={thumb} qr={qr} len={len} /></Sequence> : null}
      {src ? <Audio src={staticFile(src)} /> : null}
      {sfx.map((s, j) => <Sequence key={'x' + j} from={fr(s.t)} durationInFrames={fr(2.5)} layout="none"><Audio src={staticFile(s.file)} volume={s.vol} /></Sequence>)}
    </AbsoluteFill>
  );
};

// one piece of the guest's real work (W x H = the card on top), its label chip bottom-right, the brand logo top-left
const CW = 1052, CH = 592;
const WorkCard: React.FC<{w: Props['work'][number]; logo: string}> = ({w, logo}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = spr(f, fps, 0, 150, 16);
  const srcs = w.srcs ?? [];
  const body = () => {
    if (w.kind === 'clip' && w.src) return <OffthreadVideo src={staticFile(w.src)} muted style={{position: 'absolute', inset: 0, width: CW, height: CH, objectFit: 'cover'}} />;
    if (w.kind === 'pic' && srcs[0]) return (
      <>
        <Img src={staticFile(srcs[0])} style={{position: 'absolute', inset: -40, width: CW + 80, height: CH + 80, objectFit: 'cover', filter: 'blur(28px) brightness(.55)'}} />
        <Img src={staticFile(srcs[0])} style={{position: 'absolute', left: '50%', top: '47%', maxWidth: CW - 120, maxHeight: CH - 150, borderRadius: 14,
          border: `6px solid ${E.white}`, boxShadow: '0 18px 40px rgba(0,0,0,.55)', transform: `translate(-50%, -50%) scale(${0.9 + 0.1 * a + f * 0.0006})`}} />
      </>
    );
    // posts: fanned out one by one, a slow drift
    const n = srcs.length, size = n > 4 ? 300 : 340, gap = (CW - 120 - size) / Math.max(1, n - 1);
    const per = Math.max(3, Math.min(7, Math.round((w.d * fps * 0.45) / n)));
    return (
      <>
        <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 40%, #3D5BA6 0%, #1E2C55 70%)'}} />
        {srcs.map((s, j) => {
          const q = spr(f, fps, j * per, 170, 14);
          const rot = ((j % 2 ? 1 : -1) * (4 + (j * 3) % 5)) * (1 - 0.3 * q);
          return <Img key={j} src={staticFile(s)} style={{position: 'absolute', left: 60 + j * gap - f * 0.15, top: (CH - 70 - size) / 2 + (j % 2 ? 22 : -10) + (1 - q) * 160,
            width: size, height: size, objectFit: 'cover', borderRadius: 10, border: `6px solid ${E.white}`, boxShadow: '0 16px 34px rgba(0,0,0,.55)',
            opacity: q, transform: `rotate(${rot}deg) scale(${0.85 + 0.15 * q})`}} />;
        })}
      </>
    );
  };
  return (
    <AbsoluteFill style={{opacity: Math.min(1, f / 4 + 0.2)}}>
      {body()}
      {logo ? <div style={{position: 'absolute', left: 18, ...(w.pos === 'top' ? {bottom: 16} : {top: 16}), display: 'flex', alignItems: 'center', gap: 10, background: 'rgba(12,13,17,.72)', borderRadius: 40,
        padding: '6px 16px 6px 6px', opacity: a}}>
        <Img src={staticFile(logo)} style={{width: 44, height: 44, borderRadius: 22}} />
        <span style={{fontFamily: EN, fontWeight: 900, fontSize: 24, color: E.white, letterSpacing: 1}}>COURZERVE</span></div> : null}
      {w.label ? <div style={{position: 'absolute', right: 22, ...(w.pos === 'top' ? {top: 18} : {bottom: 20}), maxWidth: CW - 80, background: E.paper, color: E.ink, borderRadius: 10, padding: '6px 22px 10px',
        fontFamily: AR, fontWeight: 900, fontSize: 40, direction: 'rtl', boxShadow: '0 10px 24px rgba(0,0,0,.5)', border: `5px solid ${E.white}`,
        transform: `translateY(${(1 - spr(f, fps, 5, 170, 15)) * (w.pos === 'top' ? -90 : 90)}px) rotate(-1.2deg)`}}><Hi text={w.label} color={E.orange} /></div> : null}
    </AbsoluteFill>
  );
};

// end of every short (Aly 2026-10-21: "في الآخر نخلي الراجل يشوف الحلقة" — the episode itself + QR, no CTA clip of his)
const EndCard: React.FC<{thumb: string; qr: string; len: string}> = ({thumb, qr, len}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = spr(f, fps, 0, 140, 16), b = spr(f, fps, 6, 160, 14), c = spr(f, fps, 12, 180, 14);
  return (
    <AbsoluteFill style={{background: `rgba(10,11,15,${0.86 * Math.min(1, f / 8)})`, direction: 'rtl', alignItems: 'center'}}>
      <div style={{position: 'absolute', top: 430, fontFamily: AR, fontWeight: 900, fontSize: 76, color: E.white, opacity: a, transform: `translateY(${(1 - a) * 30}px)`}}>
        شوف <span style={{background: E.paper, color: E.orange, borderRadius: 14, padding: '0 18px 6px'}}>الحلقة كاملة</span></div>
      <div style={{position: 'absolute', top: 560, width: 940, transform: `scale(${0.85 + 0.15 * b}) rotate(${(1 - b) * -3}deg)`, opacity: b}}>
        <Img src={staticFile(thumb)} style={{width: 940, height: 529, objectFit: 'cover', borderRadius: 22, display: 'block', border: `8px solid ${E.white}`,
          boxShadow: '0 26px 60px rgba(0,0,0,.6)'}} />
        <div style={{position: 'absolute', left: 22, bottom: 22, background: '#FF0033', borderRadius: 10, padding: '2px 14px', fontFamily: EN, fontWeight: 900, fontSize: 34, color: '#fff', direction: 'ltr'}}>▶ {len}</div>
      </div>
      <div style={{position: 'absolute', top: 1150, display: 'flex', alignItems: 'center', gap: 30, opacity: c, transform: `translateY(${(1 - c) * 40}px)`}}>
        <div style={{background: '#fff', padding: 12, borderRadius: 18}}><Img src={staticFile(qr)} style={{width: 230, height: 230, display: 'block'}} /></div>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 50, color: E.white, lineHeight: 1.35}}>على قناتي في يوتيوب<br />
          <span style={{color: E.mustard, fontSize: 40}}>امسح الكود · أو اللينك في الوصف</span></div>
      </div>
    </AbsoluteFill>
  );
};
