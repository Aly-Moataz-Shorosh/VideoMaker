import React from 'react';
import {AbsoluteFill, Easing, Img, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, img, lin, rnd, spr} from '../film/kit';

// "Glass studio" kit (lighting short, 2026-10-14). Technique from Aly's Behance reference (S.r. Seth portfolio 2026:
// SaaS animations = frosted glass cards on soft glowing gradients, words typing in grey -> white with ONE word in a pill,
// cursor clicks, toggles, a glowing light dot travelling on curves, podcast shorts with the speaker always on screen)
// but in HIS channel colours (docs/11, brand/theme.json): charcoal-navy, sky blue, royal blue, gold highlight.
export const G = {
  bg: '#0B0E14', bg2: '#14181F', navy: '#101A2E', royal: '#1F4E9F', blue: '#3BA9F5', gold: '#F5B83D', ink: '#FFFFFF',
  soft: '#C9D1DC', dim: '#7C8797', red: '#FF5A5F', green: '#35D07F',
  key: '#FFF4E0', back: '#FFB23F', fill: '#35E0F2', // the three lights of the video: white key, yellow back, cyan ambient
};
export const MONO = 'Consolas, "Courier New", monospace';

// ---------- background: charcoal-navy with two soft glowing orbs that drift + fine grain ----------
export const GlassBg: React.FC<{glow?: string}> = ({glow = G.blue}) => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const x = 30 + 18 * Math.sin(f / 90), y = 18 + 10 * Math.cos(f / 120);
  return (
    <AbsoluteFill style={{background: `linear-gradient(180deg, ${G.navy} 0%, ${G.bg} 55%, #07090D 100%)`}}>
      <AbsoluteFill style={{background: `radial-gradient(circle at ${x}% ${y}%, ${glow}55 0%, transparent 42%)`}} />
      <AbsoluteFill style={{background: `radial-gradient(circle at ${100 - x}% ${y + 20}%, ${G.royal}88 0%, transparent 48%)`}} />
      <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 120%, ${G.royal}40 0%, transparent 60%)`}} />
      <Img src={img(`bg/grain_${Math.floor(f / 2) % 3}.png`)} style={{position: 'absolute', width, height, opacity: 0.1, mixBlendMode: 'overlay'}} />
    </AbsoluteFill>
  );
};

export const GlassFx: React.FC = () => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, transparent 62%, rgba(3,6,12,0.45) 100%)'}} />
      <Img src={img(`bg/grain_${(Math.floor(f / 2) + 1) % 3}.png`)} style={{position: 'absolute', width, height, opacity: 0.07, mixBlendMode: 'overlay'}} />
    </AbsoluteFill>
  );
};

// ---------- his camera (ALWAYS on screen: the video is about light, the viewer must see the effect) ----------
// file = one continuous mp4 of the kept pieces (make_short.py builds it), keys = [{t, m}] layout changes in seconds.
// Modes: full (9:16 crop), low (big, lower part, graphics above), wide (the whole room 16:9 in the middle), mini (small
// corner card), hide (only where his source shows someone else's photo). Edges melt into the background (no hard box).
type R = {x: number; y: number; w: number; h: number; sx: number; sw: number; r: number; o: number; feather: number; sy?: number; sh?: number};
const MODES: Record<string, R> = {
  full: {x: 0, y: 0, w: 1080, h: 1920, sx: 656, sw: 607.5, r: 0, o: 1, feather: 0},
  low: {x: 0, y: 760, w: 1080, h: 1160, sx: 457, sw: 1005, r: 0, o: 1, feather: 0.16},
  wide: {x: 0, y: 690, w: 1080, h: 607.5, sx: 0, sw: 1920, r: 0, o: 1, feather: 0.12},
  mini: {x: 610, y: 1120, w: 420, h: 520, sx: 524, sw: 872, r: 46, o: 1, feather: 0},
  hide: {x: 640, y: 1180, w: 360, h: 446, sx: 524, sw: 872, r: 46, o: 0, feather: 0},
  // adobeaudition 2026-10-15: his webcam sits in the bottom-right corner of the screen recording -> crop that corner (sy/sh)
  corner: {x: 0, y: 1010, w: 1080, h: 610, sx: 1232, sw: 688, sy: 692, sh: 388, r: 0, o: 1, feather: 0.14},
  cmini: {x: 670, y: 1250, w: 360, h: 360, sx: 1440, sw: 380, sy: 692, sh: 380, r: 180, o: 1, feather: 0},
  // aftereffects-to-code 2026-10-16 (720p recording upscaled to 1080p): big webcam corner in his opening, then the small one
  lbig: {x: 160, y: 1110, w: 760, h: 570, sx: 1180, sw: 640, sy: 500, sh: 480, r: 50, o: 1, feather: 0},
  lmini: {x: 800, y: 1290, w: 240, h: 240, sx: 1670, sw: 200, sy: 850, sh: 200, r: 120, o: 1, feather: 0},
};
export const Cam: React.FC<{file: string; keys: {t: number; m: string}[]; len?: number}> = ({file, keys, len = 12}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  let i = 0;
  while (i + 1 < keys.length && f >= Math.round(keys[i + 1].t * fps)) i++;
  const cur = MODES[keys[i]?.m ?? 'low'];
  const prev = i > 0 ? MODES[keys[i - 1].m] : cur;
  const k = i > 0 ? lin(f, Math.round(keys[i].t * fps), Math.round(keys[i].t * fps) + len, 0, 1, Easing.inOut(Easing.cubic)) : 1;
  const m = (a: number, b: number) => a + (b - a) * k;
  const R = {x: m(prev.x, cur.x), y: m(prev.y, cur.y), w: m(prev.w, cur.w), h: m(prev.h, cur.h), sx: m(prev.sx, cur.sx), sw: m(prev.sw, cur.sw),
    r: m(prev.r, cur.r), o: m(prev.o, cur.o), fe: m(prev.feather, cur.feather), sy: m(prev.sy ?? 0, cur.sy ?? 0), sh: m(prev.sh ?? 1080, cur.sh ?? 1080)};
  const sc = Math.max(R.w / R.sw, R.h / R.sh); // source px -> screen px (cover)
  const vh = 1080 * sc;
  const top = -R.sy * sc + (R.h - R.sh * sc) / 2; // crop (sy..sy+sh) centred vertically inside the rect
  const mask = R.fe > 0.001 ? `linear-gradient(180deg, transparent 0%, #000 ${R.fe * 100}%, #000 ${100 - R.fe * 45}%, transparent 100%)` : undefined;
  const mini = R.r > 1;
  return (
    <div style={{position: 'absolute', left: R.x, top: R.y, width: R.w, height: R.h, opacity: R.o, borderRadius: R.r, overflow: 'hidden',
      WebkitMaskImage: mask, maskImage: mask, boxShadow: mini ? `0 30px 60px rgba(0,0,0,0.55), 0 0 0 3px rgba(255,255,255,${0.25 * R.o})` : undefined}}>
      <OffthreadVideo muted src={staticFile(file)} style={{position: 'absolute', left: -R.sx * sc + (R.w - R.sw * sc) / 2, top, width: 1920 * sc, height: vh}} />
    </div>
  );
};

// ---------- his REAL screen recording in a glass card (adobeaudition 2026-10-15): the same cam.mp4 (full 1920x1080 frame),
// cropped to a source rect that glides between keys, with a gold highlight box on every button he clicks (Aly rule: show WHERE).
// startFrom = timeline frame of the scene start (the scene Sequence restarts frame 0). keys/marks times = frames from scene start.
export type SKey = {t: number; sx: number; sy: number; sw: number};
export type SMark = {t: number; d: number; x: number; y: number; w: number; h: number; label?: string};
export const Screen: React.FC<{file: string; startFrom: number; w?: number; h?: number; keys: SKey[]; marks?: SMark[]}> = ({file, startFrom, w = 1000, h = 640, keys, marks = []}) => {
  const f = useCurrentFrame();
  let i = 0;
  while (i + 1 < keys.length && f >= keys[i + 1].t) i++;
  const a = keys[i], b = keys[Math.min(i + 1, keys.length - 1)];
  const k = b === a ? 0 : lin(f, b.t - 14, b.t, 0, 1, Easing.inOut(Easing.cubic));
  const sx = a.sx + (b.sx - a.sx) * k, sy = a.sy + (b.sy - a.sy) * k, sw = a.sw + (b.sw - a.sw) * k;
  const sc = w / sw;
  return (
    <Glass w={w + 24} h={h + 24} pad={12} r={38} glow={G.blue}>
      <div style={{position: 'relative', width: w, height: h, borderRadius: 28, overflow: 'hidden', background: '#1D1D1D'}}>
        <OffthreadVideo muted src={staticFile(file)} startFrom={startFrom} style={{position: 'absolute', left: -sx * sc, top: -sy * sc, width: 1920 * sc, height: 1080 * sc}} />
        {marks.map((m, j) => {
          if (f < m.t || f > m.t + m.d) return null;
          const p = spr(f, 30, m.t, 220, 14), o = 1 - lin(f, m.t + m.d - 6, m.t + m.d);
          const pad = 8;
          return (
            <div key={j} style={{position: 'absolute', left: (m.x - sx) * sc - pad, top: (m.y - sy) * sc - pad, width: m.w * sc + 2 * pad, height: m.h * sc + 2 * pad,
              border: `5px solid ${G.gold}`, borderRadius: 14, opacity: o, transform: `scale(${1.25 - 0.25 * p})`, boxShadow: `0 0 30px ${G.gold}AA, inset 0 0 20px ${G.gold}55`}}>
              {m.label ? <div style={{position: 'absolute', left: '50%', top: -62, transform: 'translateX(-50%)'}}><Pill text={m.label} font={EN} dir="ltr" size={34} /></div> : null}
              {m.w < 400 ? <Cursor x={m.w * sc / 2 + pad + 10} y={m.h * sc / 2 + pad + 6} s={0.6} click={m.t + 6} /> : null}
            </div>
          );
        })}
      </div>
    </Glass>
  );
};

// ---------- sound check card: his voice as bars (env = 0..1 per bar, precomputed from the real audio) + the noise floor band ----------
export const Sound: React.FC<{env: number[]; noise: number; label: string; color?: string; at?: number; w?: number; h?: number}> = ({env, noise, label, color = G.blue, at = 0, w = 960, h = 300}) => {
  const f = useCurrentFrame();
  const n = env.length, bw = w / n;
  const play = (f - at) / Math.max(1, n); // the playhead runs over the bars in n frames (one bar per frame)
  const head = Math.max(0, Math.min(1, play));
  return (
    <Glass w={w + 60} pad={30} r={40} glow={noise > 0.15 ? G.red : G.green}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', direction: 'rtl', marginBottom: 12}}>
        <Pill text={label} color={color} ink={color === G.gold ? '#14181F' : '#fff'} size={44} />
        <span style={{fontFamily: EN, fontWeight: 800, fontSize: 30, color: noise > 0.15 ? G.red : G.green, direction: 'ltr'}}>{noise > 0.15 ? 'NOISE ●' : 'CLEAN ✓'}</span>
      </div>
      <div style={{position: 'relative', width: w, height: h}}>
        <div style={{position: 'absolute', left: 0, right: 0, top: h / 2 - (h / 2) * noise, height: h * noise, background: `${G.red}33`, borderTop: noise > 0.02 ? `2px dashed ${G.red}` : undefined, borderBottom: noise > 0.02 ? `2px dashed ${G.red}` : undefined}} />
        {env.map((v, i) => {
          const lit = i / n <= head;
          const hh = Math.max(4, h * Math.max(v, noise * (0.6 + 0.4 * Math.abs(Math.sin(i * 1.7)))));
          return <div key={i} style={{position: 'absolute', left: i * bw + bw * 0.2, width: bw * 0.6, top: (h - hh) / 2, height: hh, borderRadius: bw, background: lit ? color : 'rgba(255,255,255,0.22)'}} />;
        })}
        <div style={{position: 'absolute', top: -10, bottom: -10, left: head * w, width: 4, background: '#fff', boxShadow: '0 0 16px #fff'}} />
      </div>
    </Glass>
  );
};

// Adobe Audition logo (vector: the product's own tile — dark navy square, lilac "Au").
export const AuLogo: React.FC<{s?: number}> = ({s = 1}) => (
  <div style={{width: 200 * s, height: 195 * s, borderRadius: 38 * s, background: '#00005B', border: `${6 * s}px solid #9999FF`, boxSizing: 'border-box',
    display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 20px 60px rgba(153,153,255,0.45)'}}>
    <span style={{fontFamily: EN, fontWeight: 700, fontSize: 110 * s, color: '#9999FF', letterSpacing: -2 * s}}>Au</span>
  </div>
);

// ---------- scene wrapper: soft blur + rise in, blur out (SaaS feel, no hard pops) ----------
export const GScene: React.FC<{children: React.ReactNode}> = ({children}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  const a = lin(f, 0, 10), b = lin(f, d - 8, d, 1, 0, Easing.in(Easing.cubic));
  const o = Math.min(a, b);
  return <AbsoluteFill style={{opacity: o, filter: o < 0.99 ? `blur(${(1 - o) * 14}px)` : undefined, transform: `translateY(${(1 - a) * 30}px)`}}>{children}</AbsoluteFill>;
};

// Appears at `at` (frames) with a soft spring + blur, optional exit.
export const In: React.FC<{at?: number; out?: number; x: number; y: number; children: React.ReactNode; from?: number; dy?: number; z?: number}> = ({at = 0, out, x, y, children, from = 0.86, dy = 40, z}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (f < at) return null;
  const p = spr(f, fps, at, 140, 18);
  const o = out === undefined ? 1 : 1 - lin(f, out, out + 8, 0, 1, Easing.in(Easing.cubic));
  if (o <= 0) return null;
  const v = Math.min(1, p * 1.3) * o;
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) translateY(${(1 - p) * dy}px) scale(${from + (1 - from) * p})`,
      opacity: v, filter: v < 0.98 ? `blur(${(1 - v) * 10}px)` : undefined, zIndex: z}}>{children}</div>
  );
};

// Frosted glass card.
export const Glass: React.FC<{w: number; h?: number; children?: React.ReactNode; pad?: number; r?: number; glow?: string; style?: React.CSSProperties}> = ({w, h, children, pad = 34, r = 40, glow, style}) => (
  <div style={{width: w, height: h, padding: pad, borderRadius: r, position: 'relative', boxSizing: 'border-box',
    background: 'linear-gradient(160deg, rgba(255,255,255,0.16) 0%, rgba(255,255,255,0.05) 100%)', backdropFilter: 'blur(26px)',
    border: '2px solid rgba(255,255,255,0.20)', boxShadow: `0 30px 70px rgba(0,0,0,0.45), inset 0 2px 0 rgba(255,255,255,0.18)${glow ? `, 0 0 70px ${glow}55` : ''}`, ...style}}>
    {children}
  </div>
);

// Pill (one highlighted word: gold, or a colour of light).
export const Pill: React.FC<{text: string; color?: string; ink?: string; size?: number; font?: string; dir?: 'rtl' | 'ltr'; glow?: boolean}> = ({text, color = G.gold, ink = '#14181F', size = 64, font = AR, dir = 'rtl', glow = true}) => (
  <span style={{display: 'inline-block', background: `linear-gradient(180deg, ${color} 0%, ${color}DD 100%)`, color: ink, fontFamily: font, fontWeight: 900, fontSize: size,
    padding: `${size * 0.06}px ${size * 0.36}px ${size * 0.12}px`, borderRadius: size, lineHeight: 1.25, direction: dir, whiteSpace: 'nowrap',
    boxShadow: glow ? `0 10px 40px ${color}77, inset 0 2px 0 rgba(255,255,255,0.5)` : undefined}}>{text}</span>
);

// Typed headline: words appear one by one (grey -> white); *word* = pill (gold), [word] = light-blue word.
export const Type: React.FC<{text: string; at?: number; size?: number; per?: number; color?: string; pill?: string; width?: number; dir?: 'rtl' | 'ltr'; font?: string; out?: number}> = ({text, at = 0, size = 76, per = 3, color = G.ink, pill = G.gold, width = 960, dir = 'rtl', font = AR, out}) => {
  const f = useCurrentFrame();
  if (f < at) return null;
  const o = out === undefined ? 1 : 1 - lin(f, out, out + 8);
  const words = text.split(' ');
  return (
    <div style={{width, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', alignItems: 'center', gap: `${size * 0.12}px ${size * 0.26}px`, direction: dir, opacity: o}}>
      {words.map((w, i) => {
        const t = at + i * per;
        const p = lin(f, t, t + 8), q = lin(f, t + 3, t + 14);
        if (f < t) return <span key={i} style={{fontFamily: font, fontWeight: 800, fontSize: size, opacity: 0}}>{w.replace(/[*[\]]/g, '')}</span>;
        const isPill = w.startsWith('*') && w.endsWith('*');
        const isBlue = w.startsWith('[') && w.endsWith(']');
        const clean = w.replace(/[*[\]]/g, '').replace(/_/g, ' ');
        const st: React.CSSProperties = {opacity: p, transform: `translateY(${(1 - p) * 18}px)`, filter: p < 0.98 ? `blur(${(1 - p) * 6}px)` : undefined, display: 'inline-block'};
        if (isPill) return <span key={i} style={{...st, transform: `${st.transform} scale(${0.7 + 0.3 * spr(f, 30, t, 200, 12)})`}}><Pill text={clean} color={pill} size={size * 0.92} font={font} dir={dir} /></span>;
        return (
          <span key={i} style={{...st, fontFamily: font, fontWeight: 800, fontSize: size, lineHeight: 1.25, color: isBlue ? G.blue : q < 1 ? mix(G.dim, color, q) : color,
            textShadow: '0 4px 24px rgba(0,0,0,0.5)'}}>{clean}</span>
        );
      })}
    </div>
  );
};
const hex = (c: string) => [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16));
export const mix = (a: string, b: string, t: number) => {
  const A = hex(a), B = hex(b);
  return `rgb(${A.map((v, i) => Math.round(v + (B[i] - v) * t)).join(',')})`;
};

// Top title holder (centred horizontally at y).
export const Top: React.FC<{text: string; at?: number; y?: number; size?: number; out?: number; width?: number}> = ({text, at = 2, y = 170, size = 76, out, width = 980}) => (
  <div style={{position: 'absolute', top: y, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Type text={text} at={at} size={size} out={out} width={width} /></div>
);

// Chapter chip: number + English name + Arabic name, glass pill with a coloured dot of that light.
export const Chip: React.FC<{n: string; en: string; ar: string; color: string; at?: number; y?: number}> = ({n, en, ar, color, at = 0, y = 92}) => {
  const f = useCurrentFrame();
  if (f < at) return null;
  const p = spr(f, 30, at, 160, 16);
  return (
    <div style={{position: 'absolute', top: y, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * -30}px)`}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 18, padding: '12px 30px 12px 14px', borderRadius: 60, direction: 'ltr',
        background: 'rgba(255,255,255,0.10)', border: '2px solid rgba(255,255,255,0.22)', backdropFilter: 'blur(20px)', boxShadow: `0 0 50px ${color}44`}}>
        <div style={{width: 58, height: 58, borderRadius: '50%', background: color, color: '#14181F', fontFamily: EN, fontWeight: 900, fontSize: 28,
          display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: `0 0 30px ${color}`}}>{n}</div>
        <span style={{fontFamily: EN, fontWeight: 800, fontSize: 38, color: G.ink}}>{en}</span>
        <span style={{fontFamily: AR, fontWeight: 700, fontSize: 36, color: G.soft}}>· {ar}</span>
      </div>
    </div>
  );
};

// iOS-like toggle that flips ON at frame `on` (glows in its light colour).
export const Toggle: React.FC<{on?: number; off?: number; color?: string; s?: number; start?: boolean}> = ({on, off, color = G.blue, s = 1, start = false}) => {
  const f = useCurrentFrame();
  let v = start ? 1 : 0;
  if (on !== undefined) v = lin(f, on, on + 8, start ? 1 : 0, 1);
  if (off !== undefined && f >= off) v = lin(f, off, off + 8, 1, 0);
  return (
    <div style={{width: 120 * s, height: 68 * s, borderRadius: 40 * s, position: 'relative', background: v > 0.5 ? color : 'rgba(255,255,255,0.18)',
      boxShadow: v > 0.5 ? `0 0 ${36 * s}px ${color}AA` : 'inset 0 2px 6px rgba(0,0,0,0.4)', transition: 'none'}}>
      <div style={{position: 'absolute', top: 6 * s, left: (6 + 52 * v) * s, width: 56 * s, height: 56 * s, borderRadius: '50%', background: '#fff', boxShadow: '0 4px 12px rgba(0,0,0,0.35)'}} />
    </div>
  );
};

// The "Light studio" panel (backbone of the short): one row per light, its toggle flips on its chapter.
export type Row = {id: string; en: string; ar: string; color: string; on?: number; off?: number; start?: boolean};
export const Studio: React.FC<{rows: Row[]; w?: number; focus?: string; title?: string}> = ({rows, w = 900, focus, title = 'Light Studio'}) => {
  const f = useCurrentFrame();
  return (
    <Glass w={w} pad={30} r={44}>
      <div style={{display: 'flex', alignItems: 'center', gap: 14, direction: 'ltr', marginBottom: 14}}>
        {['#FF5F57', '#FEBC2E', '#28C840'].map((c) => <div key={c} style={{width: 18, height: 18, borderRadius: '50%', background: c}} />)}
        <span style={{fontFamily: EN, fontWeight: 700, fontSize: 30, color: G.soft, marginLeft: 12}}>{title}</span>
      </div>
      {rows.map((r) => {
        const lit = r.on !== undefined && f >= r.on + 4 && !(r.off !== undefined && f >= r.off) || (r.start && !(r.off !== undefined && f >= r.off));
        const hi = focus === r.id;
        return (
          <div key={r.id} style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', direction: 'ltr', padding: '16px 18px', marginTop: 10, borderRadius: 26,
            background: hi ? 'rgba(255,255,255,0.12)' : 'rgba(255,255,255,0.04)', border: hi ? `2px solid ${r.color}88` : '2px solid transparent'}}>
            <div style={{display: 'flex', alignItems: 'center', gap: 20}}>
              <Bulb color={r.color} lit={lit} s={0.62} />
              <div>
                <div style={{fontFamily: EN, fontWeight: 800, fontSize: 38, color: lit ? G.ink : G.soft}}>{r.en}</div>
                <div style={{fontFamily: AR, fontWeight: 700, fontSize: 30, color: G.dim, direction: 'rtl', textAlign: 'left'}}>{r.ar}</div>
              </div>
            </div>
            <Toggle on={r.on} off={r.off} color={r.color} start={r.start} />
          </div>
        );
      })}
    </Glass>
  );
};

// ---------- icons (vector) ----------
export const Bulb: React.FC<{color?: string; lit?: boolean; s?: number}> = ({color = G.key, lit = true, s = 1}) => (
  <svg width={90 * s} height={90 * s} viewBox="0 0 90 90" style={{overflow: 'visible'}}>
    {lit ? <circle cx={45} cy={38} r={40} fill={color} opacity={0.28} style={{filter: 'blur(8px)'}} /> : null}
    <path d="M45 8 C27 8 16 21 16 36 C16 47 23 53 28 59 L30 66 L60 66 L62 59 C67 53 74 47 74 36 C74 21 63 8 45 8 Z" fill={lit ? color : 'rgba(255,255,255,0.15)'} stroke={lit ? '#fff' : 'rgba(255,255,255,0.4)'} strokeWidth={3} />
    <rect x={31} y={69} width={28} height={7} rx={3} fill="#9AA6B5" /><rect x={33} y={78} width={24} height={6} rx={3} fill="#7C8797" />
  </svg>
);

export const Cursor: React.FC<{x: number; y: number; s?: number; click?: number; ring?: string}> = ({x, y, s = 1, click, ring = G.gold}) => {
  const f = useCurrentFrame();
  const k = click === undefined ? -1 : f - click;
  const press = k >= 0 && k < 6 ? 0.85 : 1;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: 0, height: 0, zIndex: 20}}>
      {k >= 0 && k < 18 ? (
        <div style={{position: 'absolute', left: -60 * s, top: -60 * s, width: 120 * s, height: 120 * s, borderRadius: '50%', border: `${6 * s}px solid ${ring}`,
          transform: `scale(${0.3 + k / 10})`, opacity: 1 - k / 18}} />
      ) : null}
      <svg width={90 * s} height={115 * s} viewBox="0 0 22 28" style={{position: 'absolute', left: -4 * s, top: -4 * s, transform: `scale(${press})`, transformOrigin: '0 0',
        filter: 'drop-shadow(0 8px 12px rgba(0,0,0,0.45))'}}>
        <path d="M2,2 L2,22 L7.2,17.4 L10.6,25.4 L14,24 L10.7,16.2 L17.6,16 Z" fill="#fff" stroke="#14181F" strokeWidth={1.4} strokeLinejoin="round" />
      </svg>
    </div>
  );
};

// Glowing light dot (the motif: "you paint with light").
export const Orb: React.FC<{x: number; y: number; color?: string; r?: number; o?: number}> = ({x, y, color = G.key, r = 26, o = 1}) => (
  <div style={{position: 'absolute', left: x - r * 3, top: y - r * 3, width: r * 6, height: r * 6, opacity: o, pointerEvents: 'none'}}>
    <div style={{position: 'absolute', inset: 0, borderRadius: '50%', background: `radial-gradient(circle, ${color}AA 0%, ${color}33 30%, transparent 65%)`}} />
    <div style={{position: 'absolute', left: r * 2, top: r * 2, width: r * 2, height: r * 2, borderRadius: '50%', background: '#fff', boxShadow: `0 0 ${r}px ${color}, 0 0 ${r * 2.5}px ${color}`}} />
  </div>
);

// A sphere lit from angle `ang` (deg, 0 = from the right, 90 = from the top); hard = sharp terminator + sharp cast shadow.
export const Sphere: React.FC<{d?: number; ang?: number; hard?: number; flat?: number; color?: string; light?: string; shadow?: boolean}> = ({d = 300, ang = 135, hard = 0, flat = 0, color = '#4A6FA5', light = G.key, shadow = true}) => {
  const rad = (ang * Math.PI) / 180;
  const hx = 50 + 30 * Math.cos(rad), hy = 50 - 30 * Math.sin(rad);
  const soft = 1 - hard;
  // flat = 1 -> a 2D disc (no shading at all)
  const g = `radial-gradient(circle at ${hx}% ${hy}%, ${light} 0%, ${color} ${18 + 30 * soft}%, #0B1220 ${70 + 25 * soft - 10 * hard}%, #05080F 100%)`;
  const sx = -Math.cos(rad) * d * 0.45, sy = d * 0.48;
  return (
    <div style={{position: 'relative', width: d, height: d}}>
      {shadow ? <div style={{position: 'absolute', left: d * 0.1 + sx * (1 - flat), top: sy + d * 0.38, width: d * 0.8, height: d * 0.16, borderRadius: '50%', background: 'rgba(0,0,0,0.6)',
        filter: `blur(${2 + 22 * soft}px)`, opacity: 1 - flat}} /> : null}
      <div style={{position: 'absolute', inset: 0, borderRadius: '50%', background: color}} />
      <div style={{position: 'absolute', inset: 0, borderRadius: '50%', background: g, opacity: 1 - flat}} />
      <div style={{position: 'absolute', inset: 0, borderRadius: '50%', border: `${3 + 3 * flat}px solid rgba(255,255,255,${0.15 + 0.6 * flat})`}} />
    </div>
  );
};

// Simple vector bust (head + shoulders) lit from `ang`: front light = flat, side light = one cheek in shadow. edge = rim light colour.
export const Bust: React.FC<{w?: number; ang?: number; amount?: number; rim?: string; rimK?: number; tone?: string}> = ({w = 360, ang = 90, amount = 1, rim, rimK = 0, tone = '#C99A74'}) => {
  // ang: 90 = straight from the front (no shadow); 0 = light from screen right; 180 = from screen left
  const side = Math.cos((ang * Math.PI) / 180); // -1 left .. 1 right
  const dark = Math.abs(side) * amount;
  const dir = side >= 0 ? 'to left' : 'to right';
  const h = w * 1.2;
  const shade = `linear-gradient(${dir}, rgba(255,244,224,${0.25 * dark}) 0%, rgba(0,0,0,0) ${40 - 8 * dark}%, rgba(8,10,20,${0.8 * dark}) ${56}%, rgba(8,10,20,${0.9 * dark}) 100%)`;
  return (
    <div style={{position: 'relative', width: w, height: h}}>
      {rimK > 0 ? (
        <>
          <div style={{position: 'absolute', left: w * 0.27 - 6, top: -6, width: w * 0.46 + 12, height: w * 0.56 + 12, borderRadius: '48% 48% 46% 46%', background: rim, opacity: rimK, filter: 'blur(10px)'}} />
          <div style={{position: 'absolute', left: -6, top: w * 0.58 - 6, width: w + 12, height: h - w * 0.58 + 12, borderRadius: `${w * 0.45}px ${w * 0.45}px 0 0`, background: rim, opacity: rimK, filter: 'blur(12px)'}} />
        </>
      ) : null}
      {/* shoulders (hoodie) */}
      <div style={{position: 'absolute', left: 0, top: w * 0.58, width: w, height: h - w * 0.58, borderRadius: `${w * 0.45}px ${w * 0.45}px 0 0`, background: '#AEB7C4', overflow: 'hidden'}}>
        <div style={{position: 'absolute', inset: 0, background: shade}} />
      </div>
      {/* neck */}
      <div style={{position: 'absolute', left: w * 0.41, top: w * 0.46, width: w * 0.18, height: w * 0.16, background: tone, overflow: 'hidden'}}><div style={{position: 'absolute', inset: 0, background: shade}} /></div>
      {/* head */}
      <div style={{position: 'absolute', left: w * 0.27, top: 0, width: w * 0.46, height: w * 0.56, borderRadius: '48% 48% 46% 46%', background: tone, overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: 0, top: 0, width: '100%', height: '28%', background: '#1E1A18'}} />
        <div style={{position: 'absolute', left: '24%', top: '44%', width: '14%', height: '6%', borderRadius: 6, background: '#1E1A18'}} />
        <div style={{position: 'absolute', right: '24%', top: '44%', width: '14%', height: '6%', borderRadius: 6, background: '#1E1A18'}} />
        <div style={{position: 'absolute', left: '22%', bottom: 0, width: '56%', height: '24%', borderRadius: '0 0 46% 46%', background: '#3A302A', opacity: 0.55}} />
        <div style={{position: 'absolute', left: '46%', top: '50%', width: '8%', height: '16%', borderRadius: 8, background: 'rgba(0,0,0,0.12)'}} />
        <div style={{position: 'absolute', inset: 0, background: shade}} />
      </div>
    </div>
  );
};

// small helpers
export const Label: React.FC<{text: string; color?: string; size?: number; font?: string; dir?: 'rtl' | 'ltr'; w?: number}> = ({text, color = G.ink, size = 44, font = AR, dir = 'rtl', w}) => (
  <div style={{fontFamily: font, fontWeight: 800, fontSize: size, color, direction: dir, textAlign: 'center', width: w, lineHeight: 1.25, textShadow: '0 4px 20px rgba(0,0,0,0.5)'}}>{text}</div>
);
export const Mark: React.FC<{ok: boolean; s?: number}> = ({ok, s = 1}) => (
  <div style={{width: 76 * s, height: 76 * s, borderRadius: '50%', background: ok ? G.green : G.red, color: '#fff', fontFamily: EN, fontWeight: 900, fontSize: 44 * s,
    display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: `0 0 30px ${ok ? G.green : G.red}99`}}>{ok ? '✓' : '✕'}</div>
);
export {AR, EN, lin, spr, rnd};
