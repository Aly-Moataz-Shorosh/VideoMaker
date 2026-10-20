import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, OffthreadVideo, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

// "Darkroom collage" kit for the film-story shorts (theodesy, 2026-10-08).
// Look (from Aly's references): cut-out B&W photos on grey paper, halftone, film grain + dust, hand-drawn red marker
// scribbles, big kinetic words, light beams. Colors: darkroom black, silver paper, safelight red, Kodak yellow.
export const K = {
  ink: '#0E0D0C', ink2: '#1A1917', paper: '#E4E2DC', paper2: '#C9C6BE', white: '#F5F3EF', dim: '#8C8880',
  red: '#E5232B', yellow: '#FFC21A', cyan: '#3FC7DA', sand: '#B89A6A',
};
export const AR = 'Cairo', EN = 'Montserrat', OLD = 'Amiri';

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const ease = Easing.bezier(0.22, 1, 0.36, 1);
export const smooth = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
export const lin = (f: number, a: number, b: number, from = 0, to = 1, e: (x: number) => number = ease) =>
  interpolate(f, [a, b], [from, to], {...clamp, easing: e});
export const spr = (f: number, fps: number, delay = 0, stiff = 170, damp = 13) =>
  spring({frame: f - delay, fps, config: {damping: damp, stiffness: stiff, mass: 0.7}});
export const rnd = (seed: number) => {
  const x = Math.sin(seed * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};
export const sec = (fps: number, s: number | undefined, d = 0) => Math.round((s ?? d) * fps);
export const img = (p: string) => staticFile(p);

// Beats: props.b = {name: seconds from scene start} -> frame number (fallback d seconds).
export const useBeats = (b: Record<string, number> = {}) => {
  const {fps} = useVideoConfig();
  return (k: string, d = 0) => Math.round((b[k] ?? d) * fps);
};

// Scene-level in/out: fast scale+fade in, quick out. Every scene is wrapped (no hard pops).
export const Scene: React.FC<{children: React.ReactNode; bg?: string; inF?: number; outF?: number; push?: number}> = ({children, bg, inF = 7, outF = 6, push = 0.04}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  const a = Math.min(lin(f, 0, inF), lin(f, d - outF, d, 1, 0, Easing.in(Easing.cubic)));
  const s = 1 + push * (1 - lin(f, 0, inF + 4)) + 0.025 * (f / Math.max(1, d)); // slow push-in during the scene
  return (
    <AbsoluteFill style={{opacity: a, background: bg, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${s})`}}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};

// Background used under everything: warm black, faint paper texture, slow red/yellow light leak.
export const FilmBg: React.FC<{tint?: string}> = ({tint = K.red}) => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const x = 50 + 30 * Math.sin(f / 90), y = 30 + 20 * Math.cos(f / 120);
  return (
    <AbsoluteFill style={{background: K.ink}}>
      <AbsoluteFill style={{background: `radial-gradient(circle at ${x}% ${y}%, ${tint}38 0%, transparent 45%)`}} />
      <AbsoluteFill style={{background: `radial-gradient(circle at ${100 - x}% ${85 - y / 2}%, ${K.yellow}18 0%, transparent 40%)`}} />
      <Halftone color="#ffffff" size={18} dot={0.12} opacity={0.035} />
      <Img src={img(`bg/grain_${Math.floor(f / 2) % 3}.png`)} style={{position: 'absolute', width, height, opacity: 0.25}} />
    </AbsoluteFill>
  );
};

// Film look on top of everything: grain, dust specks, a hairline scratch now and then, flicker, vignette.
export const FilmFx: React.FC<{strength?: number}> = ({strength = 1}) => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const k = Math.floor(f / 2);
  const specks = Array.from({length: 7}, (_, i) => {
    const r = rnd(k * 13 + i);
    if (r > 0.45) return null;
    return <circle key={i} cx={rnd(k * 7 + i * 3) * width} cy={rnd(k * 5 + i * 11) * height} r={1.5 + rnd(k + i * 17) * 4}
      fill={rnd(k * 3 + i) > 0.5 ? '#000' : '#fff'} opacity={0.35 + rnd(i + k) * 0.4} />;
  });
  const scratch = rnd(Math.floor(f / 5) * 31) > 0.82;
  const sx = rnd(Math.floor(f / 5) * 9) * width;
  const flick = 0.035 * (rnd(f * 3.3) - 0.5);
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <Img src={img(`bg/grain_${k % 3}.png`)} style={{position: 'absolute', width, height, opacity: 0.32 * strength, mixBlendMode: 'overlay'}} />
      <svg width={width} height={height} style={{position: 'absolute'}}>
        {specks}
        {scratch ? <line x1={sx} y1={0} x2={sx + 14} y2={height} stroke="#fff" strokeWidth={1.4} opacity={0.18} /> : null}
      </svg>
      <AbsoluteFill style={{background: `rgba(${flick > 0 ? '255,255,255' : '0,0,0'},${Math.abs(flick)})`}} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, transparent 55%, rgba(0,0,0,0.55) 100%)'}} />
    </AbsoluteFill>
  );
};

export const Halftone: React.FC<{color?: string; size?: number; dot?: number; opacity?: number; style?: React.CSSProperties}> = ({color = '#000', size = 12, dot = 0.3, opacity = 0.25, style}) => (
  <AbsoluteFill style={{opacity, backgroundImage: `radial-gradient(circle, ${color} ${dot * 100}%, transparent ${dot * 100 + 2}%)`,
    backgroundSize: `${size}px ${size}px`, ...style}} />
);

// Torn-paper polygon (stable per seed) as CSS clip-path.
export const torn = (seed: number, n = 26, j = 1.2) => {
  const pts: string[] = [];
  const edge = (i: number, t: number) => (rnd(seed * 31 + i) - 0.5) * j + (t ? 0 : 0);
  for (let i = 0; i <= n; i++) pts.push(`${(i / n) * 100}% ${Math.abs(edge(i, 0))}%`);
  for (let i = 0; i <= n; i++) pts.push(`${100 - Math.abs(edge(i + 50, 0))}% ${(i / n) * 100}%`);
  for (let i = n; i >= 0; i--) pts.push(`${(i / n) * 100}% ${100 - Math.abs(edge(i + 100, 0))}%`);
  for (let i = n; i >= 0; i--) pts.push(`${Math.abs(edge(i + 150, 0))}% ${(i / n) * 100}%`);
  return `polygon(${pts.join(',')})`;
};

// Pop: spring scale + small rotation in at `at`, optional out at `out` (frames, scene-relative).
export const Pop: React.FC<{at?: number; out?: number; x: number; y: number; rot?: number; from?: number; children: React.ReactNode;
  drift?: number; z?: number; origin?: string}> = ({at = 0, out, x, y, rot = 0, from = 0.3, children, drift = 0, z, origin = '50% 50%'}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, at);
  const o = out === undefined ? 1 : 1 - lin(f, out, out + 7, 0, 1, Easing.in(Easing.cubic));
  if (f < at) return null;
  const s = (from + (1 - from) * p) * (0.6 + 0.4 * o);
  const dy = drift * (f - at);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) translate(0px, ${dy}px) rotate(${rot * (1.6 - 0.6 * p)}deg) scale(${s})`,
      opacity: Math.min(1, p * 1.6) * o, zIndex: z, transformOrigin: origin}}>
      {children}
    </div>
  );
};

// Paper card with torn edges + grain; children inside.
export const Paper: React.FC<{w: number; h: number; seed?: number; color?: string; children?: React.ReactNode; pad?: number; shadow?: boolean}> = ({w, h, seed = 1, color = K.paper, children, pad = 0, shadow = true}) => (
  <div style={{width: w, height: h, position: 'relative', filter: shadow ? 'drop-shadow(0 18px 30px rgba(0,0,0,0.55))' : undefined}}>
    <div style={{position: 'absolute', inset: 0, background: color, clipPath: torn(seed), padding: pad, overflow: 'hidden'}}>
      <Img src={img('bg/grain_1.png')} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: 0.5, mixBlendMode: 'multiply'}} />
      <div style={{position: 'relative', width: '100%', height: '100%'}}>{children}</div>
    </div>
  </div>
);

// Cut-out photo: B&W (default) with paper border, halftone hint, shadow.
export const Photo: React.FC<{src: string; w: number; h: number; bw?: boolean; border?: number; pos?: string; seed?: number; tone?: string;
  zoom?: number; fit?: 'cover' | 'contain'}> = ({src, w, h, bw = true, border = 14, pos = '50% 50%', seed = 3, tone, zoom = 1, fit = 'cover'}) => (
  <Paper w={w} h={h} seed={seed} color={K.white}>
    <div style={{position: 'absolute', inset: border, overflow: 'hidden', background: '#111'}}>
      <Img src={img(src)} style={{width: '100%', height: '100%', objectFit: fit, objectPosition: pos, transform: `scale(${zoom})`,
        filter: bw ? 'grayscale(1) contrast(1.25) brightness(1.05)' : 'contrast(1.08) saturate(1.05)'}} />
      {tone ? <AbsoluteFill style={{background: tone, mixBlendMode: 'multiply', opacity: 0.55}} /> : null}
      <Halftone color="#000" size={7} dot={0.22} opacity={0.12} />
    </div>
  </Paper>
);

// Real footage inside a torn paper frame (B&W optional). start = seconds into the clip.
export const Clip: React.FC<{src: string; w: number; h: number; start?: number; bw?: boolean; pos?: string; zoom?: number; seed?: number; border?: number;
  rate?: number; vol?: number}> = ({src, w, h, start = 0, bw = false, pos = '50% 50%', zoom = 1, seed = 5, border = 12, rate = 1, vol = 0}) => {
  const {fps} = useVideoConfig();
  return (
    <Paper w={w} h={h} seed={seed} color={K.white}>
      <div style={{position: 'absolute', inset: border, overflow: 'hidden', background: '#000'}}>
        <OffthreadVideo src={img(src)} startFrom={Math.round(start * fps)} playbackRate={rate} volume={vol}
          style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: pos, transform: `scale(${zoom})`,
            filter: bw ? 'grayscale(1) contrast(1.2)' : 'contrast(1.05)'}} />
      </div>
    </Paper>
  );
};

// Kinetic Arabic title. "*word*" = yellow highlight, "_word_" = red marker box. Words pop one by one.
export const Title: React.FC<{text: string; at?: number; size?: number; color?: string; stagger?: number; width?: number; align?: 'center' | 'right' | 'left';
  font?: string; lh?: number; dir?: 'rtl' | 'ltr'; stroke?: boolean}> = ({text, at = 0, size = 96, color = K.white, stagger = 3, width = 940, align = 'center', font = AR, lh = 1.25, dir = 'rtl', stroke = false}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  // "*a b*" / "_a b_" may span several words: mark every word inside the markers.
  const words: {t: string; hi: boolean; box: boolean}[] = [];
  let mode = '';
  for (const raw of text.split(' ')) {
    let w = raw;
    const open = !mode && (w.startsWith('*') || w.startsWith('_')) ? w[0] : '';
    if (open) {mode = open; w = w.slice(1);}
    const cur = mode;
    const m = mode ? w.match(mode === '*' ? /^(.*)\*([!؟?.,،:…]*)$/ : /^(.*)_([!؟?.,،:…]*)$/) : null; // closing marker, maybe before punctuation
    if (m) {w = m[1] + m[2]; mode = '';}
    words.push({t: w, hi: cur === '*', box: cur === '_'});
  }
  return (
    <div style={{width, direction: dir, textAlign: align, lineHeight: lh, fontFamily: font, fontWeight: 900, fontSize: size, color}}>
      {words.map(({t, hi, box}, i) => {
        const p = spr(f, fps, at + i * stagger, 220, 14);
        return (
          <span key={i} style={{display: 'inline-block', margin: `0 ${size * 0.12}px`, opacity: Math.min(1, p * 2),
            transform: `translateY(${(1 - p) * size * 0.5}px) scale(${0.7 + 0.3 * p})`, color: hi ? K.yellow : box ? K.white : color,
            background: box ? K.red : undefined, padding: box ? `0 ${size * 0.16}px` : undefined, borderRadius: box ? 6 : undefined,
            WebkitTextStroke: stroke ? `${Math.max(3, size / 22)}px ${K.ink}` : undefined, paintOrder: 'stroke fill',
            textShadow: '0 6px 18px rgba(0,0,0,0.45)'}}>
            {t}
          </span>
        );
      })}
    </div>
  );
};

// Small paper label (like a museum tag).
export const Tag: React.FC<{text: string; color?: string; bg?: string; size?: number; font?: string; dir?: 'rtl' | 'ltr'}> = ({text, color = K.ink, bg = K.paper, size = 44, font = AR, dir = 'rtl'}) => (
  <div style={{background: bg, color, fontFamily: font, fontWeight: 900, fontSize: size, padding: `${size * 0.14}px ${size * 0.45}px`, borderRadius: size * 0.2,
    direction: dir, whiteSpace: 'nowrap', boxShadow: '0 10px 24px rgba(0,0,0,0.45)', border: `3px solid ${K.ink}`}}>{text}</div>
);

// Hand-drawn marker stroke that draws itself (progress 0..1) and "boils" a little every 3 frames.
export const Scribble: React.FC<{d: string; p: number; color?: string; w?: number; len?: number; width: number; height: number; style?: React.CSSProperties}> = ({d, p, color = K.red, w = 10, len = 3000, width, height, style}) => {
  const f = useCurrentFrame();
  const k = Math.floor(f / 3);
  return (
    <svg width={width} height={height} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', ...style}}>
      <path d={d} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={len}
        strokeDashoffset={len * (1 - p)} transform={`translate(${(rnd(k) - 0.5) * 3},${(rnd(k + 9) - 0.5) * 3})`} />
    </svg>
  );
};

// Arrow-ish marker from (x1,y1) to (x2,y2) with a curved body and head.
export const arrowPath = (x1: number, y1: number, x2: number, y2: number, bend = 0.25) => {
  const mx = (x1 + x2) / 2 - (y2 - y1) * bend, my = (y1 + y2) / 2 + (x2 - x1) * bend;
  const a = Math.atan2(y2 - my, x2 - mx), h = 34;
  return `M${x1},${y1} Q${mx},${my} ${x2},${y2} M${x2 - h * Math.cos(a - 0.5)},${y2 - h * Math.sin(a - 0.5)} L${x2},${y2} L${x2 - h * Math.cos(a + 0.5)},${y2 - h * Math.sin(a + 0.5)}`;
};
export const circlePath = (cx: number, cy: number, rx: number, ry: number) =>
  `M${cx + rx},${cy} C${cx + rx},${cy - ry * 1.1} ${cx - rx * 1.05},${cy - ry * 1.05} ${cx - rx},${cy} C${cx - rx * 1.02},${cy + ry * 1.1} ${cx + rx * 1.1},${cy + ry * 1.05} ${cx + rx * 1.06},${cy - ry * 0.18}`;

// Rubber stamp that slams in (scale 2.2 -> 1, little shake).
export const Stamp: React.FC<{text: string; at: number; color?: string; size?: number; rot?: number}> = ({text, at, color = K.red, size = 90, rot = -12}) => {
  const f = useCurrentFrame();
  if (f < at) return null;
  const k = f - at;
  const s = k < 6 ? 2.2 - 1.2 * (k / 6) : 1;
  const sh = k >= 6 && k < 12 ? (rnd(f) - 0.5) * 8 : 0;
  return (
    <div style={{transform: `rotate(${rot}deg) scale(${s}) translate(${sh}px,${sh}px)`, opacity: Math.min(1, k / 3), border: `${size * 0.08}px solid ${color}`,
      color, fontFamily: AR, fontWeight: 900, fontSize: size, padding: `0 ${size * 0.3}px`, borderRadius: size * 0.12, whiteSpace: 'nowrap',
      maskImage: 'radial-gradient(circle at 30% 40%, #000 60%, rgba(0,0,0,0.75) 100%)', background: 'rgba(0,0,0,0.0)'}}>{text}</div>
  );
};

// Counting number (Western digits). format adds thousands separators.
export const Count: React.FC<{from?: number; to: number; a: number; b: number; size?: number; color?: string; suffix?: string; prefix?: string; font?: string}> = ({from = 0, to, a, b, size = 200, color = K.yellow, suffix = '', prefix = '', font = EN}) => {
  const f = useCurrentFrame();
  const v = Math.round(lin(f, a, b, from, to));
  return <div style={{fontFamily: font, fontWeight: 900, fontSize: size, color, direction: 'ltr', whiteSpace: 'nowrap', textShadow: '0 10px 30px rgba(0,0,0,0.5)'}}>{prefix}{v.toLocaleString('en-US')}{suffix}</div>;
};

// Light cone from a point (x,y) towards angle `ang` (deg), with flicker.
export const Beam: React.FC<{x: number; y: number; ang: number; len: number; spread: number; color?: string; op?: number; width: number; height: number}> = ({x, y, ang, len, spread, color = '#FFF6D8', op = 0.5, width, height}) => {
  const f = useCurrentFrame();
  const a = (ang * Math.PI) / 180, s = (spread * Math.PI) / 360;
  const p1 = [x + Math.cos(a - s) * len, y + Math.sin(a - s) * len], p2 = [x + Math.cos(a + s) * len, y + Math.sin(a + s) * len];
  const id = `bm${Math.round(x)}${Math.round(y)}${Math.round(ang)}`;
  return (
    <svg width={width} height={height} style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id={id} x1={x} y1={y} x2={x + Math.cos(a) * len} y2={y + Math.sin(a) * len} gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor={color} stopOpacity={op * (0.9 + 0.1 * rnd(f))} />
          <stop offset="1" stopColor={color} stopOpacity={0} />
        </linearGradient>
      </defs>
      <polygon points={`${x},${y} ${p1[0]},${p1[1]} ${p2[0]},${p2[1]}`} fill={`url(#${id})`} />
    </svg>
  );
};

// Film strip (vertical when vertical=true). frames = image paths (or null = blank). offset in px scrolls it.
export const Strip: React.FC<{frames: (string | null)[]; fw: number; fh: number; offset?: number; vertical?: boolean; color?: string; bw?: boolean;
  gap?: number; holes?: number; render?: (i: number) => React.ReactNode}> = ({frames, fw, fh, offset = 0, vertical = false, color = '#151311', bw = false, gap = 10, holes = 4, render}) => {
  const rail = (vertical ? fw : fh) * 0.16;
  const n = frames.length;
  const L = n * ((vertical ? fh : fw) + gap);
  const hole = (k: number, side: number) => {
    const step = ((vertical ? fh : fw) + gap) / holes;
    return Array.from({length: n * holes}, (_, i) => (
      <div key={`${side}${i}`} style={{position: 'absolute', background: '#E8E4DA', borderRadius: 4,
        ...(vertical ? {top: i * step + step * 0.3, left: side ? undefined : rail * 0.28, right: side ? rail * 0.28 : undefined, width: rail * 0.44, height: step * 0.45}
          : {left: i * step + step * 0.3, top: side ? undefined : rail * 0.28, bottom: side ? rail * 0.28 : undefined, height: rail * 0.44, width: step * 0.45})}} />
    ));
  };
  return (
    <div style={{position: 'relative', overflow: 'visible', background: color, borderRadius: 6,
      width: vertical ? fw + rail * 2 : L, height: vertical ? L : fh + rail * 2, transform: vertical ? `translateY(${-offset}px)` : `translateX(${-offset}px)`,
      boxShadow: '0 20px 40px rgba(0,0,0,0.5)'}}>
      {hole(0, 0)}{hole(0, 1)}
      {frames.map((src, i) => (
        <div key={i} style={{position: 'absolute', overflow: 'hidden', background: '#2a2622', width: fw, height: fh,
          ...(vertical ? {left: rail, top: i * (fh + gap) + gap / 2} : {top: rail, left: i * (fw + gap) + gap / 2})}}>
          {render ? render(i) : src ? <Img src={img(src)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: bw ? 'grayscale(1) contrast(1.2)' : undefined}} /> : null}
        </div>
      ))}
    </div>
  );
};

// Shake helper for impacts (frames since hit).
export const shake = (k: number, amp = 14, len = 10) => (k < 0 || k > len ? 0 : (rnd(k * 7.7) - 0.5) * amp * (1 - k / len));

// White flash at a frame (for scene accents).
export const Flash: React.FC<{at: number; color?: string; len?: number}> = ({at, color = '#fff', len = 8}) => {
  const f = useCurrentFrame();
  const o = f < at ? 0 : 1 - lin(f, at, at + len, 0, 1, Easing.out(Easing.quad));
  return o > 0 ? <AbsoluteFill style={{background: color, opacity: o * 0.85, mixBlendMode: 'screen'}} /> : null;
};
