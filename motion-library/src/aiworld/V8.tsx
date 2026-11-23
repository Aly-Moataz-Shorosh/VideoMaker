// «عالم الـ AI كله» rough cut v8 (Aly's 55 notes on v7, 2026-11-23): tree already drawn + arrow + 3 levels, face shots = circle over boards,
// small song logos + handles + watermark, talking face in the last map, handles as a separate layer (comp ai-world-v8-handles).
// Was: rough cut v7 (Aly's notes on v6, 2026-11-23): his FACE back between the boards (faces layer), MAP6 'me', tree tags
// with space + slower, avatar section opens full-frame then shrinks to the circle, song: whole logos + OUR subscribe_press + handles.
// Was: rough cut v6 (Aly's 50 notes on v5, 2026-11-22): + TREE-MAP separators (the whole video as a tree, done parts dimmed
// with ✓, the coming part lit), new order, more explaining scenes. Built on v5 (which was on v4): Same approved kit as v4 (enta Items), plus:
// - ONE continuous star background for the whole video (stars move on video time, never jump; note 6)
// - the opening glitch takes the WHOLE frame as a transition (picture sliced + shifted + the show's bars; note 1)
// - everything inside a safe area, a bit smaller (note 24)
// - explaining motion instead of lists (notes 25-33): DIAGRAM scenes = nodes that pop + edges that DRAW, live voice wave,
//   green price bars, side-by-side looping clips, OCR scan, detection boxes, typed code
// - sub-category breadcrumb + a small separator card at each new sub-category (note 18)
import React from 'react';
import {AbsoluteFill, Easing, Img, Loop, OffthreadVideo, Sequence, interpolate, random, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {fontCss} from '../blocks/theme';
import {Item} from '../enta/BoardBiz';
import {EntaGlitch} from '../enta/EntaPop';
import {E, Grain, stickerBorder} from '../enta/kit';
import {enter} from '../blocks/anim';
import {Rtl} from './V4';
import {SubscribePress} from '../templates/SubscribePress';

const gold = '#E9B949', navy = '#0B1430', ink = '#F3EEDF', green = '#3DDC84', greenDark = '#178A4C';
const S = (p?: string) => (p ? staticFile(p) : '');
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const isVid = (p?: string) => !!p && /\.(mp4|webm)$/.test(p);

const clip = z.object({src: z.string(), from: z.number(), dur: z.number(), skip: z.number().optional(), rate: z.number().optional(),
  circle: z.object({x: z.number(), y: z.number(), r: z.number()}).optional()});
const scene = z.object({k: z.string(), start: z.number(), dur: z.number(), title: z.string().optional(), items: z.array(z.record(z.string(), z.any())).default([]),
  clips: z.array(clip).default([]), url: z.string().optional(), fx: z.string().optional(), hud: z.number().optional(), glitch: z.array(z.number()).default([]),
  words: z.array(z.object({t: z.number(), w: z.string()})).default([]), fam: z.array(z.number()).default([])});
export const aiV8Schema = z.object({
  fps: z.number().default(25), duration: z.number().default(10), outW: z.number().default(1920),
  scenes: z.array(scene).default([]), hud: z.array(z.object({a: z.number(), b: z.number(), i: z.number()})).default([]),
  subs: z.array(z.object({a: z.number(), b: z.number(), name: z.string(), fam: z.number(), parent: z.string().optional()})).default([]),
  handles: z.boolean().default(false),
  caps: z.array(z.object({a: z.number(), b: z.number(), t: z.string()})).default([]),
  families: z.array(z.string()).default(['التوليد', 'الـ LLMs والـ agents', 'السكريبتات', 'الـ MCP', 'الـ skills', 'الإنسان']),
  faces: z.array(clip).default([]),
  sub: z.object({from: z.number(), dur: z.number()}).optional(),
});
type Scene = z.infer<typeof scene>;
type D = Record<string, any>;

// ---------- ONE background for the whole video: stars drift on VIDEO time, each star wraps alone off-screen (no jump) ----------
const StarField: React.FC = () => {
  const f = useCurrentFrame();
  const W = 23 * 92, drift = f * 0.22;
  const push = 1.035 + 0.025 * Math.sin(f / (25 * 18));
  const stars: React.ReactNode[] = [];
  for (let r = 0; r < 15; r++) for (let c = 0; c < 23; c++) {
    const k = r * 23 + c, x = (((c * 92 + (r % 2) * 46 + drift) % W) + W) % W - 98, y = r * 82 - 20, s = 1 + ((r * 7 + c) % 3) * 0.12;
    stars.push(
      <g key={k} transform={`translate(${x},${y}) rotate(${(k * 37) % 72}) scale(${s})`} opacity={0.3 + 0.2 * Math.sin(f / 40 + k)}>
        {[0, 72, 144, 216, 288].map((q) => <line key={q} x1={0} y1={0} x2={0} y2={-9} stroke={gold} strokeWidth={1.8} strokeLinecap="round" transform={`rotate(${q})`} />)}
      </g>);
  }
  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 90% at 50% 40%, #16245a 0%, ${navy} 55%, #050815 100%)`, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${push})`}}><svg width={1920} height={1080}>{stars}</svg></AbsoluteFill>
      <AbsoluteFill style={{background: 'radial-gradient(60% 50% at 50% 30%, rgba(255,159,67,.10), transparent 70%)'}} />
    </AbsoluteFill>
  );
};

// ---------- paper title: smaller, inside the safe area (note 24) ----------
const PaperTitle: React.FC<{text?: string; dur: number; at?: number}> = ({text, dur, at = 3}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  if (!text || f < at) return null;
  const p = enter(f, fps, at), o = interpolate(f, [dur * fps - 12, dur * fps - 2], [1, 0], clamp);
  return (
    <div style={{position: 'absolute', top: 128, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: o}}>
      <div style={{position: 'relative', background: E.paper, color: E.ink, fontFamily: 'Cairo', fontSize: 42, fontWeight: 900, padding: '6px 34px', borderRadius: 10,
        transform: `rotate(-1.2deg) scale(${p})`, ...stickerBorder(6), overflow: 'hidden'}}>
        <Grain opacity={0.3} seed={43} /><span style={{position: 'relative'}}><Rtl text={text} hi={E.orange} /></span>
      </div>
    </div>
  );
};

const ClipSeq: React.FC<{c: z.infer<typeof clip>; start: number}> = ({c, start}) => {
  const {fps} = useVideoConfig();
  return (
    <Sequence from={Math.round((c.from - start) * fps)} durationInFrames={Math.max(1, Math.round(c.dur * fps))}>
      <OffthreadVideo src={S(c.src)} muted playbackRate={c.rate ?? 1} startFrom={Math.round((c.skip || 0) * fps)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
    </Sequence>
  );
};

// ---------- full-frame glitch TRANSITION (note 1): the picture itself is sliced and pushed + the show's bars + a flash ----------
const GlitchCut: React.FC<{s: Scene; g: number}> = ({s, g}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const at = Math.round((g - s.start) * fps), k = f - at;
  if (k < -5 || k > 6) return null;
  const amt = 1 - Math.abs(k) / 6;
  const bands = 7;
  return (
    <AbsoluteFill>
      {Array.from({length: bands}).map((_, i) => {
        const r = (q: number) => random(`gl-${g}-${f}-${i}-${q}`);
        const top = (i / bands) * 100, h = 100 / bands;
        const dx = (r(1) - 0.5) * 260 * amt, tint = i % 3 === 0 ? 'hue-rotate(-40deg) saturate(2.2)' : i % 3 === 1 ? 'hue-rotate(160deg) saturate(1.8)' : 'contrast(1.4)';
        return (
          <AbsoluteFill key={i} style={{clipPath: `inset(${top}% 0 ${100 - top - h}% 0)`, transform: `translateX(${dx}px)`, filter: tint}}>
            {s.clips.map((c, j) => <ClipSeq key={j} c={c} start={s.start} />)}
          </AbsoluteFill>);
      })}
      <AbsoluteFill style={{background: '#fff', opacity: k === 0 ? 0.35 : 0, mixBlendMode: 'screen'}} />
      <EntaGlitch seed={Math.round(g * 10)} strength={1} previewBg="" />
      <EntaGlitch seed={Math.round(g * 10) + 7} strength={0.8} previewBg="" />
    </AbsoluteFill>
  );
};

// ---------- live voice wave (note 25): bars from the real voice envelope (props: env = values per frame of this scene) ----------
const Wave: React.FC<{d: D; f: number}> = ({d, f}) => {
  const env: number[] = d.env ?? [];
  const n = d.bars ?? 48, w = d.w ?? 760, h = d.h ?? 150;
  const p = enter(f, 25, d.at ?? 0), o = d.out !== undefined ? interpolate(f, [d.out, d.out + 10], [1, 0], clamp) : 1;
  if (f < (d.at ?? 0)) return null;
  const clean = d.mode === 'clean' ? interpolate(f, [d.cleanAt ?? 0, (d.cleanAt ?? 0) + 25], [1, 0], clamp) : 0;
  return (
    <div style={{position: 'absolute', left: d.x - w / 2, top: d.y - h / 2, width: w, height: h, display: 'flex', alignItems: 'center', gap: 4, opacity: Math.min(1, p * 1.5) * o,
      transform: `scale(${0.85 + 0.15 * p})`}}>
      {Array.from({length: n}).map((_, i) => {
        const fi = Math.max(0, Math.min(env.length - 1, f - Math.floor((n - 1 - i) * 0.6)));
        const v = env.length ? env[fi] : 0.3;
        const noise = clean * (0.25 + 0.25 * random(`n-${f}-${i}`));
        const hh = Math.max(6, (Math.min(1, v * (d.gain ?? 1)) * 0.92 + noise) * h);
        return <div key={i} style={{flex: 1, height: hh, borderRadius: 6, background: noise > 0.05 ? '#9aa3b8' : (d.color ?? gold),
          boxShadow: `0 0 14px ${(d.color ?? gold)}55`}} />;
      })}
    </div>
  );
};

// ---------- a diagram node: chip / logo / picture / looping clip with label; scales up while ACTIVE ----------
const Node: React.FC<{d: D; f: number}> = ({d, f}) => {
  const at = d.at ?? 0;
  if (f < at || (d.out !== undefined && f >= d.out + 10)) return null;
  const p = enter(f, 25, at), o = d.out !== undefined ? interpolate(f, [d.out, d.out + 10], [1, 0], clamp) : 1;
  const act = d.act ? interpolate(f, [d.act[0], d.act[0] + 10, d.act[1], d.act[1] + 10], [0, 1, 1, 0], clamp) : 0;
  const dim = d.dimAfter !== undefined ? interpolate(f, [d.dimAfter, d.dimAfter + 12], [1, 0.55], clamp) : 1;
  const w = d.w ?? 300;
  const mediaH = d.src ? w / (d.ar ?? 16 / 9) : d.logo ? (d.s ?? 110) : 0;
  const media = d.src ? (
    <div style={{position: 'relative', width: w, aspectRatio: d.ar ?? 16 / 9, borderRadius: 12, overflow: 'hidden', ...stickerBorder(6), background: '#0b1020',
      outline: d.good ? `5px solid ${gold}` : undefined}}>
      {isVid(d.src) ? (d.loop ? <Loop durationInFrames={Math.round((d.loopDur ?? 4) * 25)}><OffthreadVideo src={S(d.src)} muted startFrom={d.from ?? 0} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></Loop>
        : <Sequence from={at} layout="none"><OffthreadVideo src={S(d.src)} muted startFrom={d.from ?? 0} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></Sequence>)
        : <Img src={S(d.src)} style={{width: '100%', height: '100%', objectFit: d.fit ?? 'cover', objectPosition: d.pos ?? '50% 50%'}} />}
    </div>) : d.logo ? (
    <div style={{width: d.s ?? 110, height: d.s ?? 110, background: E.white, borderRadius: (d.s ?? 110) * 0.22, display: 'flex', alignItems: 'center', justifyContent: 'center',
      boxShadow: '0 10px 22px rgba(0,0,0,.45)'}}><Img src={S(d.logo)} style={{width: '72%', height: '72%', objectFit: 'contain'}} /></div>) : null;
  const label = d.label ? (
    <div style={{marginTop: media ? 10 : 0, background: d.bg ? (E as any)[d.bg] ?? d.bg : E.paper, color: E.ink, fontFamily: 'Cairo', fontWeight: 900, fontSize: d.size ?? 30,
      padding: '4px 18px', borderRadius: 40, whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', gap: 8, ...stickerBorder(4)}}>
      {d.emo ? <Img src={staticFile(`fluent/${d.emo}.png`)} style={{width: (d.size ?? 30) * 1.25, height: (d.size ?? 30) * 1.25}} /> : null}
      <Rtl text={d.label} hi={E.orange} /></div>) : null;
  const sub = d.sub ? <div style={{marginTop: 6, color: ink, fontFamily: 'Cairo', fontWeight: 700, fontSize: (d.size ?? 30) * 0.72, whiteSpace: 'nowrap', textShadow: '0 3px 10px rgba(0,0,0,.6)'}}>
    <Rtl text={d.sub} hi={gold} /></div> : null;
  return (
    <div style={{position: 'absolute', left: d.x, top: d.y,   /* (x, y) = centre of the picture/logo; labels hang under it */
      transform: `translate(-50%, ${mediaH ? `${-mediaH / 2}px` : '-50%'}) translateY(${(1 - p) * 30}px) scale(${(0.5 + 0.5 * p) * (1 + 0.12 * act)})`,
      transformOrigin: mediaH ? `50% ${mediaH / 2}px` : '50% 50%',
      opacity: Math.min(1, p * 1.6) * o * dim, display: 'flex', flexDirection: 'column', alignItems: 'center', zIndex: act > 0.5 ? 5 : 1}}>
      {media}{label}{sub}
    </div>
  );
};

// edges that DRAW themselves (stroke draw-on) + arrow head
const Edge: React.FC<{d: D; f: number}> = ({d, f}) => {
  const at = d.at ?? 0; if (f < at) return null;
  const k = interpolate(f, [at, at + (d.dur ?? 14)], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const o = d.out !== undefined ? interpolate(f, [d.out, d.out + 10], [1, 0], clamp) : 1;
  const [x1, y1, x2, y2] = d.pts; const mx = (x1 + x2) / 2 + (d.bend ?? 0), my = (y1 + y2) / 2 - Math.abs(d.bend ?? 0) * 0.3;
  const path = `M${x1},${y1} Q${mx},${my} ${x2},${y2}`; const L = Math.hypot(x2 - x1, y2 - y1) * 1.15;
  const ang = Math.atan2(y2 - my, x2 - mx) * 180 / Math.PI;
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', inset: 0, opacity: o}}>
      <path d={path} fill="none" stroke={d.color ?? gold} strokeWidth={d.wd ?? 4} strokeLinecap="round" strokeDasharray={`${L} ${L}`} strokeDashoffset={L * (1 - k)} />
      {d.arrow !== false && k > 0.95 ? <g transform={`translate(${x2},${y2}) rotate(${ang})`}><path d="M-16,-9 L0,0 L-16,9" fill="none" stroke={d.color ?? gold} strokeWidth={d.wd ?? 4} strokeLinecap="round" /></g> : null}
    </svg>
  );
};

// green price bars side by side (note 32): logo + plan + $ price, bar grows on its word, coins sfx in the audio stem
const PriceBar: React.FC<{d: D; f: number}> = ({d, f}) => {
  const at = d.at ?? 0; if (f < at) return null;
  const k = interpolate(f, [at, at + 18], [0, 1], {...clamp, easing: Easing.out(Easing.back(1.3))});
  const o = d.out !== undefined ? interpolate(f, [d.out, d.out + 10], [1, 0], clamp) : 1;
  const H = (d.h ?? 300) * k;
  return (
    <div style={{position: 'absolute', left: d.x - 70, top: d.base - H - 120, width: 140, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, fontFamily: 'Cairo'}}>
      <div style={{fontFamily: d.unit ? 'Cairo' : 'Montserrat', fontWeight: 900, fontSize: d.unit ? 32 : 40, color: green, textShadow: '0 4px 14px rgba(0,0,0,.6)', whiteSpace: 'nowrap', direction: 'rtl'}}>
        {d.unit ? `${Math.round((d.price ?? 0) * Math.min(1, k * 1.2))} ${d.unit}` : `$${Math.round((d.price ?? 0) * Math.min(1, k * 1.2))}`}</div>
      <div style={{width: 96, height: H, background: `linear-gradient(${green}, ${greenDark})`, borderRadius: '12px 12px 4px 4px', border: `3px solid ${E.white}`, marginTop: 6}} />
      <div style={{marginTop: 10, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4}}>
        {d.logo ? <div style={{width: 64, height: 64, background: E.white, borderRadius: 14, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <Img src={S(d.logo)} style={{width: '74%', height: '74%', objectFit: 'contain'}} /></div> : null}
        <div style={{color: ink, fontWeight: 900, fontSize: 24, whiteSpace: 'nowrap'}}><Rtl text={d.label ?? ''} /></div>
        {d.sub ? <div style={{color: 'rgba(243,238,223,.75)', fontWeight: 700, fontSize: 19, whiteSpace: 'nowrap'}}><Rtl text={d.sub} /></div> : null}
      </div>
    </div>
  );
};

// OCR scan / detection boxes over a picture
const Scan: React.FC<{d: D; f: number}> = ({d, f}) => {
  const at = d.at ?? 0; if (f < at) return null;
  const p = enter(f, 25, at), o = d.out !== undefined ? interpolate(f, [d.out, d.out + 10], [1, 0], clamp) : 1;
  const w = d.w ?? 620, hgt = w / (d.ar ?? 16 / 9);
  const k = interpolate(f, [at + 8, at + 50], [0, 1], clamp);
  return (
    <div style={{position: 'absolute', left: d.x - w / 2, top: d.y - hgt / 2, width: w, height: hgt, opacity: Math.min(1, p * 1.5) * o, transform: `scale(${0.9 + 0.1 * p})`}}>
      <div style={{position: 'absolute', inset: 0, borderRadius: 12, overflow: 'hidden', ...stickerBorder(6)}}>
        <Img src={S(d.src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        {d.mode === 'ocr' ? <div style={{position: 'absolute', left: 0, right: 0, top: `${k * 100}%`, height: 6, background: green, boxShadow: `0 0 24px ${green}`}} /> : null}
      </div>
      {(d.boxes ?? []).map((b: D, i: number) => {
        const bk = interpolate(f, [at + 10 + i * 8, at + 22 + i * 8], [0, 1], clamp);
        return bk > 0 ? <div key={i} style={{position: 'absolute', left: `${b.x}%`, top: `${b.y}%`, width: `${b.w}%`, height: `${b.h}%`, border: `4px solid ${b.c ?? green}`, borderRadius: 6,
          opacity: bk, transform: `scale(${1.15 - 0.15 * bk})`}}>
          <div style={{position: 'absolute', top: -34, left: -4, background: b.c ?? green, color: E.ink, fontFamily: 'Cairo', fontWeight: 900, fontSize: 20, padding: '1px 10px', borderRadius: 6, whiteSpace: 'nowrap'}}>
            <Rtl text={b.label} /></div></div> : null;
      })}
      {d.text ? <div style={{position: 'absolute', left: 0, right: 0, top: hgt + 16, textAlign: 'center', fontFamily: 'Consolas, monospace', color: green, fontSize: 26, direction: 'ltr'}}>
        {String(d.text).slice(0, Math.floor(String(d.text).length * k))}</div> : null}
    </div>
  );
};

// typed text block (prompt / code / words with times)
const Typed: React.FC<{d: D; f: number}> = ({d, f}) => {
  const at = d.at ?? 0; if (f < at) return null;
  const o = d.out !== undefined ? interpolate(f, [d.out, d.out + 10], [1, 0], clamp) : 1;
  const k = interpolate(f, [at, at + (d.dur ?? 40)], [0, 1], clamp), p = enter(f, 25, at);
  const txt = String(d.text ?? '');
  return (
    <div style={{position: 'absolute', left: d.x - (d.w ?? 560) / 2, top: d.y, width: d.w ?? 560, opacity: Math.min(1, p * 1.5) * o, background: 'rgba(8,14,36,.92)', borderRadius: 12,
      padding: '14px 20px', ...stickerBorder(5), fontFamily: 'Consolas, monospace', fontSize: d.size ?? 24, color: '#cfe3ff', direction: d.rtl ? 'rtl' : 'ltr', textAlign: d.rtl ? 'right' : 'left',
      whiteSpace: 'pre-wrap', lineHeight: 1.45}}>
      {d.head ? <span style={{color: E.mustard}}>{d.head} </span> : null}{txt.slice(0, Math.floor(txt.length * k))}
    </div>
  );
};

const Diagram: React.FC<{items: D[]}> = ({items}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{fontFamily: 'Cairo'}}>
      {items.filter((d) => d.k === 'edge').map((d, i) => <Edge key={'e' + i} d={d} f={f} />)}
      {items.filter((d) => d.k === 'wave').map((d, i) => <Wave key={'w' + i} d={d} f={f} />)}
      {items.filter((d) => d.k === 'bar').map((d, i) => <PriceBar key={'b' + i} d={d} f={f} />)}
      {items.filter((d) => d.k === 'scan').map((d, i) => <Scan key={'s' + i} d={d} f={f} />)}
      {items.filter((d) => d.k === 'typed').map((d, i) => <Typed key={'t' + i} d={d} f={f} />)}
      {items.filter((d) => d.k === 'node').map((d, i) => <Node key={'n' + i} d={d} f={f} />)}
      {items.filter((d) => !['edge', 'wave', 'bar', 'scan', 'typed', 'node', 'page', 'split', 'diff', 'line', 'circle', 'brand', 'subscribe'].includes(d.k)).map((d, i) => <Item key={'i' + i} d={{scale: 0.8, ...d}} f={f} />)}
    </AbsoluteFill>
  );
};

// ---------- his face in a small circle beside pages/motion (note 21) ----------
const FaceCircle: React.FC<{d: D; s: Scene}> = ({d, s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const at = d.at ?? 0; if (f < at) return null;
  const p = enter(f, fps, at), o = d.out !== undefined ? interpolate(f, [d.out, d.out + 10], [1, 0], clamp) : interpolate(f, [s.dur * fps - 12, s.dur * fps - 2], [1, 0], clamp);
  const r = d.r ?? 150;
  // v7 note 13: the section opens with HIM full frame, then the screen shrinks into the circle at the top
  const k = d.grow !== undefined ? interpolate(f, [d.grow, d.grow + 18], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)}) : 1;
  const L = (a: number, b: number) => a + (b - a) * k;
  const W = L(1920, r * 2), H = L(1080, r * 2);
  const hid = ((d.hide ?? []) as number[][]).reduce((m, [a0, b0]) => Math.min(m, 1 - interpolate(f, [a0 - 6, a0, b0, b0 + 6], [0, 1, 1, 0], clamp)), 1);   // v8 notes 13/14
  return (
    <div style={{position: 'absolute', left: L(0, d.x - r), top: L(0, d.y - r), width: W, height: H, borderRadius: L(0, r), overflow: 'hidden', border: `${L(0, 6)}px solid ${E.white}`,
      boxShadow: '0 14px 30px rgba(0,0,0,.55)', opacity: (d.grow !== undefined ? o : Math.min(1, p * 1.5) * o) * hid, transform: d.grow !== undefined ? undefined : `scale(${0.6 + 0.4 * p})`, zIndex: 3}}>
      <OffthreadVideo src={S(d.src)} muted startFrom={Math.round((d.skip ?? 0) * fps)} style={{position: 'absolute', width: L(1920, r * 3.6), height: L(1080, r * 3.6), objectFit: 'cover',
        left: L(0, -r * 0.8), top: L(0, -r * 0.38)}} />
    </div>
  );
};

// ---------- browser with a real page; page starts BELOW the bar (nothing cut, note 21), smaller (note 24) ----------
const Browser: React.FC<{s: Scene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const pages = s.items.filter((d) => d.k === 'page');
  const cur = [...pages].reverse().find((d) => f >= d.at) ?? pages[0];
  if (!cur) return null;
  const p = enter(f, fps, cur.at), o = interpolate(f, [(cur.out ?? s.dur * fps) - 10, cur.out ?? s.dur * fps], [1, 0], clamp);
  const W = cur.w ?? 1180, H = W * 0.56;
  return (
    <div style={{position: 'absolute', left: (cur.x ?? 960) - W / 2, top: (cur.y ?? 560) - H / 2, width: W, height: H + 44, borderRadius: 18, overflow: 'hidden', background: '#0e1220',
      boxShadow: '0 30px 80px rgba(0,0,0,.6)', ...stickerBorder(6), transform: `translateY(${(1 - p) * 50}px) scale(${0.92 + 0.08 * p})`, opacity: Math.min(1, p * 1.5) * o}}>
      <div style={{height: 44, background: '#1a2036', display: 'flex', alignItems: 'center', gap: 9, padding: '0 16px'}}>
        {['#FF5A6E', '#F5C451', '#4CD37A'].map((c) => <div key={c} style={{width: 13, height: 13, borderRadius: 7, background: c}} />)}
        <div style={{marginLeft: 18, flex: 1, height: 26, borderRadius: 13, background: '#0b0f1c', color: 'rgba(243,238,223,.7)', fontFamily: 'Montserrat', fontSize: 16,
          display: 'flex', alignItems: 'center', padding: '0 14px'}}>{cur.url ?? s.url ?? ''}</div>
      </div>
      <div style={{width: W, height: H, overflow: 'hidden'}}>
        <Img src={S(cur.src)} style={{width: '100%', height: '100%', objectFit: 'cover',
          objectPosition: cur.pos ?? `50% ${interpolate(f, [cur.at + 15, cur.out ?? s.dur * fps], [0, 100], {...clamp, easing: Easing.inOut(Easing.sin)})}%`}} />
      </div>
    </div>
  );
};

// text -> picture / picture -> same picture edited / clip pairs (kept from v4, smaller)
const Split: React.FC<{s: Scene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const out = interpolate(f, [s.dur * fps - 12, s.dur * fps - 2], [1, 0], clamp);
  const side = (d: D, i: number) => {
    const t0 = d.at ?? 0, p = enter(f, fps, t0);
    const typed = interpolate(f, [t0, t0 + 40], [0, 1], clamp), reveal = interpolate(f, [t0 + 45, t0 + 65], [0, 1], clamp);
    const wipe = interpolate(f, [t0 + 20, t0 + 60], [0, 1], clamp);
    return (
      <div key={i} style={{position: 'relative', width: 720, height: 405, borderRadius: 12, overflow: 'hidden', ...stickerBorder(6), background: '#0b1020',
        transform: `translateY(${(1 - p) * 50}px) rotate(${i ? 1 : -1}deg)`, opacity: f < t0 ? 0 : Math.min(1, p * 1.5)}}>
        {!d.src ? <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', background: E.paper, color: E.ink, fontFamily: 'Cairo',
          fontWeight: 900, fontSize: 52, padding: 40, textAlign: 'center'}}><Rtl text={d.cap ?? ''} hi={E.orange} /></div>
          : isVid(d.src) ? (d.loop ? <Loop durationInFrames={Math.round((d.loopDur ?? 5) * 25)}><OffthreadVideo src={S(d.src)} muted startFrom={3} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></Loop>
            : <Sequence from={t0} layout="none"><OffthreadVideo src={S(d.src)} muted startFrom={3} style={{width: '100%', height: '100%', objectFit: 'cover', opacity: d.prompt ? reveal : 1}} /></Sequence>)
          : <Img src={S(d.src)} style={{width: '100%', height: '100%', objectFit: 'cover', opacity: d.prompt ? reveal : 1}} />}
        {d.before ? <div style={{position: 'absolute', inset: 0, clipPath: `inset(0 0 0 ${wipe * 100}%)`}}>
          <Img src={S(d.before)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          <div style={{position: 'absolute', top: 0, bottom: 0, left: 0, width: 6, background: E.mustard}} /></div> : null}
        {d.prompt && reveal < 1 ? <div style={{position: 'absolute', inset: 0, background: `rgba(8,14,36,${0.93 - 0.9 * reveal})`, padding: 26, fontFamily: 'Consolas, monospace',
          fontSize: 22, lineHeight: 1.45, color: '#cfe3ff', direction: 'ltr', textAlign: 'left'}}><span style={{color: E.mustard}}>prompt › </span>
          {String(d.prompt).slice(0, Math.floor(String(d.prompt).length * typed))}</div> : null}
        {d.cap && d.src ? <div style={{position: 'absolute', bottom: 12, right: 12, background: E.paper, color: E.ink, fontFamily: 'Cairo', fontWeight: 900, fontSize: 26, padding: '3px 16px',
          borderRadius: 8, ...stickerBorder(4)}}><Rtl text={d.cap} hi={E.orange} /></div> : null}
      </div>);
  };
  return <AbsoluteFill style={{flexDirection: 'row-reverse', gap: 44, alignItems: 'center', justifyContent: 'center', paddingTop: 40, opacity: out}}>
    {s.items.filter((d) => d.k === 'split').map(side)}</AbsoluteFill>;
};

const Diffusion: React.FC<{s: Scene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const d = s.items.find((x) => x.k === 'diff'); if (!d) return null;
  const k = interpolate(f, [d.at ?? 0, s.dur * fps - 15], [0, 1], clamp), out = interpolate(f, [s.dur * fps - 6, s.dur * fps - 1], [1, 0], clamp);
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', paddingTop: 40, opacity: out}}>
      <div style={{position: 'relative', width: 1000, height: 562, borderRadius: 12, overflow: 'hidden', ...stickerBorder(6), background: navy}}>
        <Img src={S(d.src)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: `blur(${(1 - k) * 26}px)`}} />
        <Img src={S('projects/aiworld/v3/noise.png')} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: Math.pow(1 - k, 1.3)}} />
      </div>
      <div style={{position: 'absolute', top: 150, fontFamily: 'Montserrat', fontWeight: 900, color: E.mustard, fontSize: 34}}>step {Math.floor(k * 30)} / 30</div>
    </AbsoluteFill>
  );
};

const Lyr: React.FC<{s: Scene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const t = s.start + f / fps;
  const lines = s.items.filter((d) => d.k === 'line');
  const line = [...lines].reverse().find((d) => t >= d.t - 0.05);
  const words = line ? s.words.filter((w) => w.t >= line.t - 0.05 && w.t < line.end) : [];
  return (
    <AbsoluteFill>
      {s.clips.map((c, i) => <ClipSeq key={i} c={c} start={s.start} />)}
      <AbsoluteFill style={{background: 'linear-gradient(transparent 55%, rgba(5,8,21,.78))'}} />
      <div style={{position: 'absolute', bottom: 110, left: 160, right: 160, display: 'flex', flexWrap: 'wrap', gap: '6px 16px', justifyContent: 'center', direction: 'rtl', fontFamily: 'Cairo'}}>
        {words.map((w, i) => {
          const p = enter(f, fps, Math.round((w.t - s.start) * fps));
          const o = line ? interpolate(t, [line.end - 0.35, line.end - 0.05], [1, 0], clamp) : 1;
          return <bdi key={i} style={{fontSize: 62, fontWeight: 900, color: t >= w.t ? gold : 'rgba(243,238,223,.25)', transform: `translateY(${(1 - p) * 30}px)`, opacity: o,
            textShadow: '0 6px 26px rgba(0,0,0,.7)', display: 'inline-block'}}>{w.w}</bdi>;
        })}
      </div>
      <SongBrand s={s} />
    </AbsoluteFill>
  );
};

// the song (notes 49, 50): HIS logo the whole song — the face top-right, the name bottom-left (from pp 2.png) —
// and on «لسه شغلانة بني آدم» a subscribe button + the 4 platforms
const SongBrand: React.FC<{s: Scene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const b = s.items.find((d) => d.k === 'brand'); if (!b) return null;
  const pin = interpolate(f, [0, 15], [0, 1], clamp), pout = interpolate(f, [s.dur * fps - 15, s.dur * fps], [1, 0], clamp);
  const sub = s.items.find((d) => d.k === 'subscribe');
  const so = sub ? interpolate(f, [s.dur * fps - 12, s.dur * fps], [1, 0], clamp) : 0;
  return (
    <AbsoluteFill style={{opacity: pin * pout}}>
      <Img src={S(b.face)} style={{position: 'absolute', right: 96, top: 70, width: 62, filter: 'drop-shadow(0 4px 10px rgba(0,0,0,.6))'}} />
      {(() => { const spots = [[150, 150], [1610, 820], [150, 700], [1600, 260]]; const k = Math.floor(f / (fps * 9)) % spots.length; const [wx, wy] = spots[k];
        return <Img src={staticFile('brand/signature-calligraphy.png')} style={{position: 'absolute', left: wx, top: wy, width: 150, opacity: 0.1,
          filter: 'invert(1) brightness(1.4)'}} />; })()}
      {b.handles ? <div style={{position: 'absolute', left: 96, bottom: 46, display: 'flex', gap: 18, direction: 'ltr', alignItems: 'center', opacity: 0.9}}>
        {(b.handles as {logo: string; t: string}[]).map((h, i) => (
          <div key={i} style={{display: 'flex', alignItems: 'center', gap: 6}}>
            <Img src={S(h.logo)} style={{width: 22, height: 22, objectFit: 'contain'}} />
            <span style={{fontFamily: 'Montserrat', fontWeight: 700, fontSize: 18, color: ink, textShadow: '0 2px 6px rgba(0,0,0,.8)'}}>{h.t}</span></div>))}
      </div> : null}
      {sub && f >= sub.at + 20 ? (
        <div style={{position: 'absolute', left: 120, top: 400, display: 'flex', flexDirection: 'column', gap: 14, opacity: so, direction: 'ltr'}}>
          {(sub.logos as string[]).map((l, i) => {
            const q = interpolate(f, [sub.at + 22 + i * 5, sub.at + 32 + i * 5], [0, 1], clamp);
            return (
              <div key={i} style={{display: 'flex', alignItems: 'center', gap: 14, opacity: q, transform: `translateX(${(1 - q) * -40}px)`}}>
                <div style={{width: 58, height: 58, borderRadius: 16, background: E.paper, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 8px 18px rgba(0,0,0,.5)'}}>
                  <Img src={S(l)} style={{width: 40, height: 40, objectFit: 'contain'}} /></div>
                <div style={{fontFamily: 'Montserrat', fontWeight: 800, fontSize: 32, color: ink, textShadow: '0 3px 10px rgba(0,0,0,.8)'}}>{(sub.handles as string[])[i]}</div>
              </div>);
          })}
        </div>) : null}
    </AbsoluteFill>
  );
};

// the six families (map) — smaller and inside the safe area
const JetMap: React.FC<{s: Scene; families: string[]}> = ({s, families}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const parts = [[-390, 10], [-210, -175], [0, -40], [210, -175], [390, 10], [0, 175]];
  const X = (x: number) => 960 + x * 1.3, Y = (y: number) => 560 + y * 1.3;
  const out = interpolate(f, [s.dur * fps - 12, s.dur * fps - 2], [1, 0], clamp);
  const me = (s as D).me as string | undefined;
  if (me) {   // v7 note 21: HIS picture in the middle, the 6 parts around him (not the plane)
    const ring = [[-560, -170], [-620, 40], [-560, 250], [560, -170], [620, 40], [560, 250]];
    const pm = enter(f, fps, 0);
    return (
      <AbsoluteFill style={{opacity: out}}>
        <div style={{position: 'absolute', left: 960 - 190, top: 580 - 190, width: 380, height: 380, borderRadius: '50%', overflow: 'hidden', border: `8px solid ${E.white}`,
          boxShadow: '0 20px 50px rgba(0,0,0,.6)', transform: `scale(${0.7 + 0.3 * pm})`, opacity: Math.min(1, pm * 1.5)}}>
          {/\.mp4$/.test(me) ? <OffthreadVideo src={S(me)} muted startFrom={Math.round(((s as D).meSkip ?? 0) * fps)} style={{position: 'absolute', width: 380 * 1.8, height: 380 * 1.8, objectFit: 'cover', left: -380 * 0.4, top: -380 * 0.19}} />
            : <Img src={S(me)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />}</div>
        {ring.map(([x, y], i) => {
          const p = enter(f, fps, 6 + i * 4); const X = 960 - x, Y = 580 + y;
          return (
            <div key={i} style={{position: 'absolute', left: X, top: Y, transform: `translate(-50%,-50%) scale(${0.5 + 0.5 * p})`, opacity: Math.min(1, p * 1.5),
              background: E.paper, color: E.ink, borderRadius: 12, padding: '8px 20px', minWidth: 190, textAlign: 'center', ...stickerBorder(5), fontFamily: 'Cairo', boxShadow: '0 12px 24px rgba(0,0,0,.45)'}}>
              <div style={{fontFamily: 'Montserrat', fontWeight: 900, fontSize: 28, color: E.orange}}>{i + 1}</div>
              <div style={{fontWeight: 900, fontSize: 28, whiteSpace: 'nowrap'}}><Rtl text={families[i]} /></div>
            </div>);
        })}
      </AbsoluteFill>);
  }
  return (
    <AbsoluteFill style={{opacity: out}}>
      <svg width={1920} height={1080} viewBox="-740 -430 1480 830" style={{position: 'absolute', inset: 0}}>
        <path d="M0,-260 L60,-60 L380,40 L380,90 L60,60 L40,200 L120,250 L120,280 L0,260 L-120,280 L-120,250 L-40,200 L-60,60 L-380,90 L-380,40 L-60,-60 Z"
          fill="rgba(95,211,230,.10)" stroke="#5FD3E6" strokeOpacity={0.75} strokeWidth={3} strokeDasharray="12 8" />
      </svg>
      {parts.map(([x, y], i) => {
        const at = s.fam[i] !== undefined ? s.fam[i] : 0;
        const show = s.fam.length ? f >= at : true;
        const p = s.fam.length ? enter(f, fps, at) : 1, hot = s.hud === i;
        return (
          <div key={i} style={{position: 'absolute', left: X(x), top: Y(y), transform: `translate(-50%,-50%) scale(${0.5 + 0.5 * p})`, opacity: show ? 1 : 0.25,
            background: hot ? E.mustard : E.paper, color: E.ink, borderRadius: 12, padding: '8px 20px', minWidth: 190, textAlign: 'center', ...stickerBorder(5),
            fontFamily: 'Cairo', boxShadow: '0 12px 24px rgba(0,0,0,.45)'}}>
            <div style={{fontFamily: 'Montserrat', fontWeight: 900, fontSize: 28, color: E.orange}}>{i + 1}</div>
            <div style={{fontWeight: 900, fontSize: 28, whiteSpace: 'nowrap'}}><Rtl text={families[i]} /></div>
          </div>);
      })}
    </AbsoluteFill>
  );
};

// ---------- top strip: family + sub-category breadcrumb (note 18) ----------
const MiniHud: React.FC<{i: number; families: string[]; sub?: string}> = ({i, families, sub}) => (
  <div style={{position: 'absolute', top: 22, right: 26, display: 'flex', gap: 6, direction: 'rtl', fontFamily: 'Cairo', alignItems: 'center'}}>
    {families.map((n, k) => (
      <div key={k} style={{padding: '3px 12px', borderRadius: 8, fontSize: 19, fontWeight: 800, whiteSpace: 'nowrap',
        color: k === i ? E.ink : 'rgba(243,238,223,.7)', background: k === i ? E.mustard : 'rgba(8,14,36,.62)', border: `1px solid ${k === i ? E.white : 'rgba(233,185,73,.3)'}`}}>
        <Rtl text={k === i && sub ? `${n} › ${sub}` : n} /></div>
    ))}
  </div>
);

// ---------- separator = the MAP of the whole video as a tree (notes 3, 37): root → 6 families → their parts;
// parts already explained are dimmed with ✓, the coming one is lit (gold, pulsing, its branch draws itself), the rest wait ----------
const TreeMap: React.FC<{s: Scene; subs: {a: number; b: number; name: string; fam: number; parent?: string}[]; families: string[]; first: boolean}> = ({s, subs, families, first}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const cur = subs.findIndex((x) => Math.abs(x.a - s.start) < 0.05);
  const curFam = cur >= 0 ? subs[cur].fam : 0;
  const fin = interpolate(f, [0, 8], [0, 1], clamp), fout = interpolate(f, [s.dur * fps - 8, s.dur * fps], [1, 0], clamp);
  const colX = (i: number) => 1590 - i * 246;   // RTL: first family on the right
  const famY = 285, subY0 = 352, subH = 46;   // v7 note 16: space between every tag
  const grow = (_k: number) => 1;   // v8 note 3a: the tree is ALREADY drawn when the screen appears
  const draw = interpolate(f, [4, 26], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  void first;
  const pulse = 0.5 + 0.5 * Math.sin(f / 7);
  let k = 0;
  return (
    <AbsoluteFill style={{opacity: fin * fout, fontFamily: 'Cairo'}}>
      <AbsoluteFill style={{background: 'rgba(5,8,21,.55)'}} />
      <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
        {families.map((_, i) => {
          const lit = i === curFam;
          const L = Math.hypot(colX(i) - 960, famY - 190);
          return <path key={i} d={`M960,200 L${colX(i)},${famY - 28}`} stroke={lit ? gold : 'rgba(243,238,223,.35)'} strokeWidth={lit ? 4 : 2}
            strokeDasharray={lit ? `${L} ${L}` : undefined} strokeDashoffset={lit ? L * (1 - draw) : 0} fill="none" />;
        })}
      </svg>
      <div style={{position: 'absolute', left: 960, top: 165, transform: 'translate(-50%,-50%)', background: E.paper, color: E.ink, fontWeight: 900, fontSize: 34,
        padding: '4px 28px', borderRadius: 12, ...stickerBorder(5)}}><Rtl text="عالم الـ AI كله" /></div>
      {families.map((fam, i) => {
        const items = subs.map((x, j) => ({...x, j})).filter((x) => x.fam === i);
        const lit = i === curFam;
        return (
          <React.Fragment key={i}>
            <div style={{position: 'absolute', left: colX(i), top: famY, transform: `translate(-50%,-50%) scale(${lit ? 1.06 : 1})`, background: lit ? E.mustard : 'rgba(239,230,210,.9)',
              color: E.ink, fontWeight: 900, fontSize: 21, padding: '4px 12px', borderRadius: 10, whiteSpace: 'nowrap', ...stickerBorder(3), opacity: grow(k++)}}>
              <Rtl text={`${i + 1}. ${fam}`} /></div>
            {items.map((x, q) => {
              const done = x.j < cur, now = x.j === cur;
              const g = grow(k++);
              const child = !!x.parent;   // v8 note 26: sites are children of «مواقع التوليد»
              const ax = colX(i) + (child ? 14 : 0), ay = subY0 + q * subH;
              const arrowIn = interpolate(f, [6, 16], [0, 1], clamp), bob = Math.sin(f / 5) * 6;
              return (
                <React.Fragment key={q}>
                {now ? <svg width={1920} height={1080} style={{position: 'absolute', inset: 0, opacity: arrowIn}}>
                  {/* v8 note 3b: an arrow points at the part we enter */}
                  <path d={`M${ax + 150 + bob},${ay} L${ax + 92 + bob},${ay}`} stroke={gold} strokeWidth={6} strokeLinecap="round" />
                  <path d={`M${ax + 108 + bob},${ay - 14} L${ax + 90 + bob},${ay} L${ax + 108 + bob},${ay + 14}`} fill="none" stroke={gold} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" />
                </svg> : null}
                {child && q > 0 ? <div style={{position: 'absolute', left: colX(i) - 48, top: ay - subH + 14, width: 14, height: subH - 8, borderLeft: '2px solid rgba(233,185,73,.45)', borderBottom: '2px solid rgba(233,185,73,.45)', opacity: done ? 0.42 : 0.8}} /> : null}
                <div style={{position: 'absolute', left: ax, top: ay, transform: `translate(-50%,-50%) scale(${(now ? 1.08 + 0.04 * pulse : 1) * (child ? 0.88 : 1)})`,
                  opacity: g * (done ? 0.42 : 1), padding: '2px 12px', borderRadius: 18, fontSize: now ? 20 : 17, fontWeight: now ? 900 : 700, whiteSpace: 'nowrap',
                  background: now ? gold : done ? 'rgba(243,238,223,.18)' : 'rgba(8,14,36,.75)', color: now ? E.ink : ink,
                  border: `2px solid ${now ? E.white : 'rgba(233,185,73,.35)'}`, boxShadow: now ? `0 0 ${18 + 14 * pulse}px rgba(233,185,73,.8)` : undefined}}>
                  {done ? '✓ ' : ''}<Rtl text={x.name} /></div>
                </React.Fragment>);
            })}
          </React.Fragment>);
      })}
    </AbsoluteFill>
  );
};

const SubSep: React.FC<{name: string; fam: string}> = ({name, fam}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const p = enter(f, fps, 0), o = interpolate(f, [30, 40], [1, 0], clamp);
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', pointerEvents: 'none'}}>
      <div style={{transform: `translateY(${(1 - p) * -60}px) rotate(-2deg) scale(${0.7 + 0.3 * p})`, opacity: Math.min(1, p * 1.6) * o, background: E.paper, color: E.ink,
        fontFamily: 'Cairo', padding: '10px 40px', borderRadius: 12, ...stickerBorder(7), textAlign: 'center', boxShadow: '0 20px 40px rgba(0,0,0,.5)'}}>
        <div style={{fontSize: 26, fontWeight: 800, color: E.orange}}><Rtl text={fam} /></div>
        <div style={{fontSize: 52, fontWeight: 900}}><Rtl text={name} /></div>
      </div>
    </AbsoluteFill>
  );
};

const SceneView: React.FC<{s: Scene; families: string[]; subs: {a: number; b: number; name: string; fam: number; parent?: string}[]}> = ({s, families, subs}) => {
  const {fps} = useVideoConfig();
  const video = ['AV', 'CLIP', 'LYR'].includes(s.k);
  return (
    <AbsoluteFill>
      {(s.k === 'AV' || s.k === 'CLIP') ? <AbsoluteFill>{s.clips.map((c, i) => <ClipSeq key={i} c={c} start={s.start} />)}</AbsoluteFill> : null}
      {s.glitch.map((g, i) => <GlitchCut key={'g' + i} s={s} g={g} />)}
      {s.k === 'SEP' && <TreeMap s={s} subs={subs} families={families} first={subs.length > 0 && Math.abs(subs[0].a - s.start) < 0.05} />}
      {s.k === 'MAP6' && <JetMap s={s} families={families} />}
      {s.k === 'WEB' && <Browser s={s} />}
      {s.k === 'SPLIT' && <Split s={s} />}
      {s.fx === 'diffusion' && <Diffusion s={s} />}
      {s.k === 'LYR' && <Lyr s={s} />}
      {video && s.k !== 'LYR' && s.items.some((d) => d.k !== 'circle') ? <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(5,8,21,.35), transparent 30%, transparent 70%, rgba(5,8,21,.35))'}} /> : null}
      <Diagram items={s.items} />
      {s.items.filter((d) => d.k === 'circle').map((d, i) => <FaceCircle key={'c' + i} d={d} s={s} />)}
      {s.k !== 'LYR' && <PaperTitle text={s.title} dur={s.dur} at={s.items.find((d) => d.k === 'titleAt')?.at ?? 3} />}
      {void fps}
    </AbsoluteFill>
  );
};

// v7 notes 4 + 15: HIS face (the avatar, lip-synced: the clip second = the voice second) full frame between the boards
const FaceFade: React.FC<{dur: number; children: React.ReactNode}> = ({dur, children}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 4, dur - 4, dur], [0, 1, 1, 0], clamp);
  return <AbsoluteFill style={{opacity: o}}>{children}</AbsoluteFill>;
};
const FaceRing: React.FC<{c: z.infer<typeof clip>; dur: number}> = ({c, dur}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const {x, y, r} = c.circle!;
  const p = enter(f, fps, 0), o = interpolate(f, [dur - 8, dur], [1, 0], clamp);
  return (
    <div style={{position: 'absolute', left: x - r, top: y - r, width: r * 2, height: r * 2, borderRadius: '50%', overflow: 'hidden', border: `6px solid ${E.white}`,
      boxShadow: '0 14px 30px rgba(0,0,0,.55)', opacity: Math.min(1, p * 1.6) * o, transform: `scale(${0.6 + 0.4 * p})`, background: navy}}>
      <OffthreadVideo src={S(c.src)} muted startFrom={Math.round((c.skip || 0) * fps)} style={{position: 'absolute', width: r * 3.6, height: r * 3.6, objectFit: 'cover', left: -r * 0.8, top: -r * 0.38}} />
    </div>
  );
};
const FaceShot: React.FC<{c: z.infer<typeof clip>}> = ({c}) => {
  const {fps} = useVideoConfig();
  const dur = Math.max(1, Math.round(c.dur * fps));
  return (
    <Sequence from={Math.round(c.from * fps)} durationInFrames={dur}>
      {c.circle ? <FaceRing c={c} dur={dur} /> :
      <FaceFade dur={dur}><OffthreadVideo src={S(c.src)} muted startFrom={Math.round((c.skip || 0) * fps)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></FaceFade>}
    </Sequence>
  );
};

export const HandlesBadge: React.FC = () => (
  <div style={{position: 'absolute', right: 40, bottom: 26, display: 'flex', alignItems: 'center', gap: 12, direction: 'ltr', opacity: 0.85}}>
    <Img src={staticFile('projects/aiworld/v6/imgs/v7__logo_face_full.png')} style={{width: 34, filter: 'drop-shadow(0 2px 6px rgba(0,0,0,.6))'}} />
    {[['youtube.png', '@AlyShorosh'], ['tiktok.png', '@alyshorosh'], ['instagram.ico', '@alyshorosh'], ['facebook.png', 'aly.shorosh']].map(([l, t]) => (
      <div key={l} style={{display: 'flex', alignItems: 'center', gap: 5}}>
        <Img src={staticFile('projects/aiworld/v6/logos/' + l)} style={{width: 18, height: 18, objectFit: 'contain'}} />
        <span style={{fontFamily: 'Montserrat', fontWeight: 700, fontSize: 15, color: ink, textShadow: '0 2px 6px rgba(0,0,0,.85)'}}>{t}</span></div>))}
  </div>
);
// the handles alone on a transparent canvas = the separate layer for Premiere
export const HandlesLayer: React.FC<{outW: number; duration: number}> = () => {
  const {width} = useVideoConfig();
  return <AbsoluteFill><div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `scale(${width / 1920})`, transformOrigin: 'left top'}}><HandlesBadge /></div></AbsoluteFill>;
};

const Captions: React.FC<{caps: z.infer<typeof aiV8Schema>['caps']; t: number}> = ({caps, t}) => {
  const c = caps.find((x) => t >= x.a && t < x.b);
  if (!c) return null;
  const e_ = Math.min(0.12, (c.b - c.a) / 3), o = interpolate(t, [c.a, c.a + e_, c.b - e_, c.b], [0, 1, 1, 0], clamp);
  return (
    <div style={{position: 'absolute', left: 0, right: 0, bottom: 34, display: 'flex', justifyContent: 'center', opacity: o, fontFamily: 'Cairo'}}>
      <div style={{background: 'rgba(5,8,21,.72)', color: ink, fontWeight: 800, fontSize: 40, padding: '4px 24px', borderRadius: 12, maxWidth: 1400, textAlign: 'center'}}>
        <Rtl text={c.t} /></div>
    </div>
  );
};

export const AiWorldV8: React.FC<z.infer<typeof aiV8Schema>> = (p) => {
  const {width} = useVideoConfig(); const f = useCurrentFrame(); const t = f / p.fps;
  const h = p.hud.find((x) => t >= x.a && t < x.b);
  const sub = p.subs.find((x) => t >= x.a && t < x.b);
  return (
    <AbsoluteFill style={{background: navy, overflow: 'hidden'}}>
      <style>{fontCss}</style>
      <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `scale(${width / 1920})`, transformOrigin: 'left top'}}>
        <StarField />
        {p.scenes.map((s, i) => (
          <Sequence key={i} from={Math.round(s.start * p.fps)} durationInFrames={Math.max(1, Math.round(s.dur * p.fps))}>
            <SceneView s={s} families={p.families} subs={p.subs} />
          </Sequence>
        ))}

        {p.faces.map((c, i) => <FaceShot key={'f' + i} c={c} />)}
        {h && <MiniHud i={sub ? sub.fam : h.i} families={p.families} sub={sub?.name} />}
        <Captions caps={p.caps} t={t} />
        {p.handles ? <HandlesBadge /> : null}
      </div>
      {p.sub ? <Sequence from={Math.round(p.sub.from * p.fps)} durationInFrames={Math.round(p.sub.dur * p.fps)}>
        <SubscribePress pressAt={22} bellAt={36} signature={false} platform="youtube" x={0.24} y={0.24} previewBg="" /></Sequence> : null}
    </AbsoluteFill>
  );
};
