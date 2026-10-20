import React from 'react';
import {AbsoluteFill, Easing, Img, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, img, lin, rnd, spr} from '../film/kit';

// "Pop studio" kit (ffmpeg shorts, 2026-10-14). Look from Aly's 5 Behance references:
// Dtmg.tv showreel (electric violet + neon lime, glossy 3D smiley ball + hand cursor, stretched italic type "NEEEEW",
// checkerboard transparency, pixel dissolves, grid, crosshairs), Portfolio 2026 (black tape tickers "••• LOGOS & MARKS",
// torn paper, polaroids with handwritten notes, grid paper), Disney DNA (lavender HUD panels: mono text, % bars,
// dotted scan boxes with corner handles), ShakeUp (orange + black, Inter-like tight type), Multer (chunky retro type).
export const P = {
  vio: '#4B1FE0', vio2: '#2C10A8', deep: '#130A3D', lime: '#B8FF3C', pink: '#FF4FA8', teal: '#45E6CF', yellow: '#FFD43B',
  paper: '#F3F0E8', ink: '#0C0B12', white: '#FFFFFF', orange: '#FF551A', lav: '#E4E2FB', blue: '#2A2CE8', dim: '#9C93D9',
};
export const MONO = 'Consolas, "Courier New", monospace';
export const HAND = 'ArefRuqaa';
export const popFontCss = `@font-face{font-family:'ArefRuqaa';src:url('${staticFile('fonts/ArefRuqaa.ttf')}') format('truetype');}`;

// ---------- background + top layer ----------
export const PopBg: React.FC<{tint?: string}> = ({tint = P.vio}) => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const x = 50 + 28 * Math.sin(f / 80), y = 40 + 20 * Math.cos(f / 110);
  const off = (f * 0.6) % 90;
  return (
    <AbsoluteFill style={{background: tint}}>
      <AbsoluteFill style={{background: `radial-gradient(circle at ${x}% ${y}%, #7B5BFF 0%, transparent 55%)`, opacity: 0.8}} />
      <AbsoluteFill style={{background: `radial-gradient(circle at ${100 - x}% ${90 - y / 2}%, ${P.deep} 0%, transparent 60%)`, opacity: 0.9}} />
      <AbsoluteFill style={{backgroundImage: 'linear-gradient(rgba(255,255,255,0.09) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,0.09) 2px, transparent 2px)',
        backgroundSize: '90px 90px', backgroundPosition: `0 ${off}px`}} />
      {/* crosshair marks on some grid crossings */}
      <svg width={width} height={height} style={{position: 'absolute', opacity: 0.35}}>
        {Array.from({length: 9}, (_, i) => {
          const cx = 90 * Math.floor(rnd(i * 3.1) * 12) , cy = 90 * Math.floor(rnd(i * 7.7) * 21) + off;
          return <g key={i} stroke={P.white} strokeWidth={3}><line x1={cx - 14} y1={cy} x2={cx + 14} y2={cy} /><line x1={cx} y1={cy - 14} x2={cx} y2={cy + 14} /></g>;
        })}
      </svg>
      <Img src={img(`bg/grain_${Math.floor(f / 2) % 3}.png`)} style={{position: 'absolute', width, height, opacity: 0.22, mixBlendMode: 'overlay'}} />
    </AbsoluteFill>
  );
};

// Design-tool frame on top: corner brackets, tiny mono labels, light grain, soft vignette.
export const PopFx: React.FC<{label?: string}> = ({label = 'FFMPEG.EXE'}) => {
  const f = useCurrentFrame();
  const {width, height, fps} = useVideoConfig();
  const s = f / fps;
  const tc = `00:${String(Math.floor(s)).padStart(2, '0')}:${String(f % fps).padStart(2, '0')}`;
  const c = (x: number, y: number, sx: number, sy: number) => (
    <path key={`${x}${y}`} d={`M${x},${y + 60 * sy} L${x},${y} L${x + 60 * sx},${y}`} stroke={P.white} strokeWidth={5} fill="none" opacity={0.85} />
  );
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <Img src={img(`bg/grain_${(Math.floor(f / 2) + 1) % 3}.png`)} style={{position: 'absolute', width, height, opacity: 0.16, mixBlendMode: 'overlay'}} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, transparent 60%, rgba(10,4,40,0.45) 100%)'}} />
      <svg width={width} height={height} style={{position: 'absolute'}}>
        {c(40, 40, 1, 1)}{c(width - 40, 40, -1, 1)}{c(40, height - 40, 1, -1)}{c(width - 40, height - 40, -1, -1)}
      </svg>
      <div style={{position: 'absolute', left: 64, top: 58, fontFamily: MONO, fontSize: 26, color: P.white, opacity: 0.8, direction: 'ltr', letterSpacing: 2}}>
        <span style={{color: P.lime}}>●</span> {label} <span style={{opacity: 0.6, marginLeft: 18}}>{tc}</span>
      </div>
      <div style={{position: 'absolute', right: 64, top: 58, fontFamily: MONO, fontSize: 26, color: P.white, opacity: 0.7, direction: 'ltr', letterSpacing: 2}}>1080×1920</div>
    </AbsoluteFill>
  );
};

// ---------- scene wrapper with pixel dissolve in / out ----------
export const PScene: React.FC<{children: React.ReactNode; bg?: string; px?: boolean}> = ({children, bg, px = true}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d, width, height} = useVideoConfig();
  const a = Math.min(lin(f, 0, 5), lin(f, d - 5, d, 1, 0, Easing.in(Easing.cubic)));
  const s = 1.035 - 0.035 * lin(f, 0, 10) + 0.02 * (f / Math.max(1, d));
  // pixel blocks that vanish at the start / appear at the end
  const N = 12, M = 21, B = width / N;
  const tin = 9, tout = 7;
  const blocks: React.ReactNode[] = [];
  if (px && (f < tin || f > d - tout)) {
    for (let i = 0; i < N; i++) for (let j = 0; j < M; j++) {
      const r = rnd(i * 31 + j * 7);
      const on = f < tin ? r > f / tin : r < (f - (d - tout)) / tout;
      if (on) blocks.push(<rect key={i + '_' + j} x={i * B} y={j * B} width={B + 1} height={B + 1} fill={r > 0.8 ? P.lime : r > 0.6 ? P.vio2 : P.vio} />);
    }
  }
  return (
    <AbsoluteFill style={{background: bg, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${s})`, opacity: px ? 1 : a}}>{children}</AbsoluteFill>
      {blocks.length ? <svg width={width} height={height} style={{position: 'absolute'}}>{blocks}</svg> : null}
    </AbsoluteFill>
  );
};

// ---------- pieces ----------
export const Checker: React.FC<{w: number; h: number; size?: number; a?: string; b?: string; style?: React.CSSProperties}> = ({w, h, size = 36, a = '#FFFFFF', b = '#D9D6E8', style}) => (
  <div style={{width: w, height: h, background: `repeating-conic-gradient(${b} 0% 25%, ${a} 0% 50%) 0 0 / ${size * 2}px ${size * 2}px`, ...style}} />
);

// Figma-like selection box that draws itself, 8 square handles, optional name tag.
export const SelBox: React.FC<{x: number; y: number; w: number; h: number; at?: number; color?: string; label?: string; dash?: boolean; tagBelow?: boolean}> = ({x, y, w, h, at = 0, color = P.lime, label, dash = false, tagBelow = false}) => {
  const f = useCurrentFrame();
  if (f < at) return null;
  const p = lin(f, at, at + 9);
  const per = 2 * (w + h);
  const hs = 20;
  const hp = spr(f, 30, at + 6, 260, 14);
  const pts = [[0, 0], [w / 2, 0], [w, 0], [w, h / 2], [w, h], [w / 2, h], [0, h], [0, h / 2]];
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, pointerEvents: 'none'}}>
      <svg width={w + 40} height={h + 40} style={{position: 'absolute', left: -20, top: -20, overflow: 'visible'}}>
        <rect x={20} y={20} width={w} height={h} fill="none" stroke={color} strokeWidth={5} strokeDasharray={dash ? '14 10' : `${per}`} strokeDashoffset={dash ? -f : per * (1 - p)} />
        {pts.map(([px, py], i) => (
          <rect key={i} x={20 + px - hs / 2} y={20 + py - hs / 2} width={hs} height={hs} fill={P.white} stroke={color} strokeWidth={4}
            transform={`translate(${(1 - hp) * 0}) `} opacity={hp} />
        ))}
      </svg>
      {label ? (
        <div style={{position: 'absolute', left: -2, [tagBelow ? 'bottom' : 'top']: tagBelow ? -64 : -64, background: color, color: P.ink, fontFamily: MONO, fontWeight: 700,
          fontSize: 30, padding: '4px 14px', direction: 'ltr', whiteSpace: 'nowrap', opacity: hp, transform: `translateY(${(1 - hp) * 12}px)`}}>{label}</div>
      ) : null}
    </div>
  );
};

// Glossy 3D ball (optionally a smiley) — Dtmg showreel mascot.
export const Ball: React.FC<{d: number; color?: string; smile?: boolean; id?: string; rot?: number}> = ({d, color = '#6F57FF', smile = true, id = 'b', rot = 0}) => (
  <svg width={d} height={d} viewBox="0 0 100 100" style={{overflow: 'visible', transform: `rotate(${rot}deg)`}}>
    <defs>
      <radialGradient id={`g${id}`} cx="35%" cy="30%" r="75%">
        <stop offset="0" stopColor="#FFFFFF" stopOpacity={0.95} />
        <stop offset="0.18" stopColor={color} stopOpacity={1} />
        <stop offset="0.75" stopColor={P.vio2} />
        <stop offset="1" stopColor={P.deep} />
      </radialGradient>
    </defs>
    <ellipse cx={52} cy={104} rx={34} ry={6} fill="#000" opacity={0.25} />
    <circle cx={50} cy={50} r={48} fill={`url(#g${id})`} />
    {smile ? (
      <g fill="none" stroke={P.deep} strokeWidth={5} strokeLinecap="round">
        <ellipse cx={38} cy={40} rx={4} ry={8} fill={P.deep} stroke="none" />
        <ellipse cx={62} cy={40} rx={4} ry={8} fill={P.deep} stroke="none" />
        <path d="M30,58 Q50,78 70,58" />
      </g>
    ) : null}
  </svg>
);

// Big arrow cursor (glossy), with a click ring when `click` frame is reached.
export const Cursor: React.FC<{x: number; y: number; s?: number; click?: number; color?: string}> = ({x, y, s = 1, click, color = P.white}) => {
  const f = useCurrentFrame();
  const k = click === undefined ? -1 : f - click;
  const press = k >= 0 && k < 6 ? 0.85 : 1;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: 0, height: 0}}>
      {k >= 0 && k < 16 ? (
        <div style={{position: 'absolute', left: -60 * s, top: -60 * s, width: 120 * s, height: 120 * s, borderRadius: '50%', border: `${8 * s}px solid ${P.lime}`,
          transform: `scale(${0.3 + k / 10})`, opacity: 1 - k / 16}} />
      ) : null}
      <svg width={110 * s} height={140 * s} viewBox="0 0 22 28" style={{position: 'absolute', left: -4 * s, top: -4 * s, transform: `scale(${press})`, transformOrigin: '0 0',
        filter: 'drop-shadow(6px 10px 0 rgba(12,6,50,0.35))'}}>
        <path d="M2,2 L2,22 L7.2,17.4 L10.6,25.4 L14,24 L10.7,16.2 L17.6,16 Z" fill={color} stroke={P.ink} strokeWidth={1.6} strokeLinejoin="round" />
      </svg>
    </div>
  );
};

// Stretched italic type with an echo trail that collapses in (Dtmg "NEEEEEW").
export const Echo: React.FC<{text: string; at?: number; size?: number; color?: string; font?: string; n?: number; dir?: 'ltr' | 'rtl'; skew?: number; stroke?: string}> = ({text, at = 0, size = 160, color = P.white, font = EN, n = 5, dir = 'ltr', skew = -10, stroke}) => {
  const f = useCurrentFrame();
  if (f < at) return null;
  const p = lin(f, at, at + 12, 0, 1, Easing.out(Easing.cubic));
  const sx = 1 + 0.6 * (1 - p);
  return (
    <div style={{position: 'relative', display: 'inline-block', fontFamily: font, fontWeight: 900, fontSize: size, lineHeight: 1, whiteSpace: 'nowrap', direction: dir,
      transform: `skewX(${skew}deg) scaleX(${sx})`, letterSpacing: -size * 0.02}}>
      {Array.from({length: n}, (_, i) => (
        <span key={i} style={{position: 'absolute', left: -(i + 1) * size * 0.16 * (1 - p * 0.75), top: 0, color: 'transparent', WebkitTextStroke: `${Math.max(2, size / 50)}px ${color}`,
          opacity: (0.6 - i * 0.1) * (1 - p * 0.6)}}>{text}</span>
      ))}
      <span style={{position: 'relative', color, WebkitTextStroke: stroke ? `${size / 22}px ${stroke}` : undefined, paintOrder: 'stroke fill',
        textShadow: `0 ${size * 0.05}px 0 ${P.deep}`}}>{text}</span>
    </div>
  );
};

// Arabic headline: words pop in; "*w*" = lime pill, "_w_" = pink pill.
export const Head: React.FC<{text: string; at?: number; size?: number; color?: string; width?: number; stagger?: number}> = ({text, at = 0, size = 92, color = P.white, width = 960, stagger = 3}) => {
  const f = useCurrentFrame();
  const words: {t: string; m: string}[] = [];
  let mode = '';
  for (const raw of text.split(' ')) {
    let w = raw;
    const open = !mode && (w.startsWith('*') || w.startsWith('_')) ? w[0] : '';
    if (open) {mode = open; w = w.slice(1);}
    const cur = mode;
    const m = mode ? w.match(mode === '*' ? /^(.*)\*([!؟?.,،:…]*)$/ : /^(.*)_([!؟?.,،:…]*)$/) : null;
    if (m) {w = m[1] + m[2]; mode = '';}
    words.push({t: w, m: cur});
  }
  return (
    <div style={{width, direction: 'rtl', textAlign: 'center', lineHeight: 1.3, fontFamily: AR, fontWeight: 900, fontSize: size, color}}>
      {words.map(({t, m}, i) => {
        const p = spr(f, 30, at + i * stagger, 240, 14);
        const pill = m === '*' ? P.lime : m === '_' ? P.pink : '';
        return (
          <span key={i} style={{display: 'inline-block', margin: `0 ${size * 0.1}px`, opacity: Math.min(1, p * 2), transform: `translateY(${(1 - p) * size * 0.6}px) rotate(${(1 - p) * -6}deg)`,
            color: pill ? P.ink : color, background: pill || undefined, padding: pill ? `0 ${size * 0.18}px` : undefined, borderRadius: pill ? size * 0.5 : undefined,
            textShadow: pill ? undefined : `0 ${size * 0.06}px 0 ${P.deep}`}}>{t}</span>
        );
      })}
    </div>
  );
};

// Black tape band with a scrolling mono ticker (Portfolio 2026 "••• LOGOS & MARKS").
export const Ticker: React.FC<{y: number; text: string; rot?: number; bg?: string; color?: string; speed?: number; size?: number; at?: number}> = ({y, text, rot = -4, bg = P.ink, color = P.white, speed = 4, size = 40, at = 0}) => {
  const f = useCurrentFrame();
  if (f < at) return null;
  const p = lin(f, at, at + 10);
  const unit = `${text}   ✦✦✦   `;
  return (
    <div style={{position: 'absolute', left: -200, right: -200, top: y, height: size * 1.7, background: bg, transform: `rotate(${rot}deg) scaleX(${p})`, overflow: 'hidden',
      boxShadow: '0 12px 0 rgba(12,6,50,0.35)'}}>
      <div style={{position: 'absolute', top: size * 0.3, left: -((f * speed) % 1200), whiteSpace: 'nowrap', fontFamily: EN, fontWeight: 900, fontSize: size, color, letterSpacing: 4, direction: 'ltr'}}>
        {unit.repeat(8)}
      </div>
    </div>
  );
};

// Lavender HUD panel (Disney DNA): mono rows + % bars, dotted frame with corner handles.
export const Hud: React.FC<{w: number; title: string; rows: {k: string; v: string; p?: number; c?: string}[]; at?: number}> = ({w, title, rows, at = 0}) => {
  const f = useCurrentFrame();
  return (
    <div style={{width: w, background: P.lav, border: `3px dashed ${P.blue}`, padding: 26, direction: 'ltr', fontFamily: MONO, color: P.blue, position: 'relative',
      boxShadow: '0 16px 0 rgba(12,6,50,0.35)'}}>
      {[[0, 0], [1, 0], [0, 1], [1, 1]].map(([a, b], i) => (
        <div key={i} style={{position: 'absolute', width: 16, height: 16, background: P.white, border: `3px solid ${P.blue}`, left: a ? undefined : -10, right: a ? -10 : undefined,
          top: b ? undefined : -10, bottom: b ? -10 : undefined}} />
      ))}
      <div style={{fontWeight: 900, fontSize: 38, marginBottom: 14, fontFamily: EN, letterSpacing: 1}}>{title}</div>
      {rows.map((r, i) => {
        const p = lin(f, at + 6 + i * 5, at + 22 + i * 5);
        return (
          <div key={i} style={{marginBottom: 14, opacity: lin(f, at + i * 5, at + 4 + i * 5)}}>
            <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 28}}><span style={{opacity: 0.75}}>{r.k}</span><span style={{fontWeight: 700}}>{r.v}</span></div>
            {r.p !== undefined ? (
              <div style={{height: 16, background: '#C9C6F2', marginTop: 6}}><div style={{height: '100%', width: `${(r.p ?? 0) * p * 100}%`, background: r.c ?? P.blue}} /></div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
};

// File icon card: page with folded corner, extension badge, name + size under it.
export const FileCard: React.FC<{ext: string; name?: string; size?: string; w?: number; color?: string; sq?: number}> = ({ext, name, size, w = 300, color = P.pink, sq = 1}) => {
  const h = w * 1.25;
  return (
    <div style={{width: w, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16}}>
      <svg width={w} height={h} viewBox="0 0 100 125" style={{overflow: 'visible', transform: `scale(${1 / sq}, ${sq})`, transformOrigin: '50% 100%'}}>
        <path d="M6,4 L68,4 L94,30 L94,121 L6,121 Z" fill={P.white} stroke={P.ink} strokeWidth={3.5} strokeLinejoin="round" />
        <path d="M68,4 L68,30 L94,30" fill="#E3E0F5" stroke={P.ink} strokeWidth={3.5} strokeLinejoin="round" />
        <rect x={14} y={72} width={72} height={34} rx={6} fill={color} stroke={P.ink} strokeWidth={3} />
        <text x={50} y={96} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={20} fill={P.ink}>{ext}</text>
        <path d="M26,30 L46,42 L26,54 Z" fill={P.vio} />
      </svg>
      {name ? <div style={{fontFamily: EN, fontWeight: 700, fontSize: w * 0.1, color: P.white, direction: 'ltr', whiteSpace: 'nowrap', textShadow: `0 4px 0 ${P.deep}`}}>{name}</div> : null}
      {size ? <div style={{fontFamily: EN, fontWeight: 900, fontSize: w * 0.17, color: P.ink, background: P.lime, padding: '2px 18px', direction: 'ltr', whiteSpace: 'nowrap'}}>{size}</div> : null}
    </div>
  );
};

// cmd.exe window. lines = array of nodes (already typed); children overlay.
export const Term: React.FC<{w: number; h: number; title?: string; children?: React.ReactNode; size?: number}> = ({w, h, title = 'C:\\Windows\\system32\\cmd.exe', children, size = 34}) => (
  <div style={{width: w, height: h, background: '#0B0B0E', border: `5px solid ${P.ink}`, boxShadow: `14px 16px 0 ${P.deep}`, position: 'relative', overflow: 'hidden', direction: 'ltr'}}>
    <div style={{height: 64, background: P.white, display: 'flex', alignItems: 'center', padding: '0 18px', gap: 14, fontFamily: EN, fontSize: 24, color: P.ink, fontWeight: 600}}>
      <div style={{width: 30, height: 24, background: '#0B0B0E', borderRadius: 3, color: P.white, fontSize: 14, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: MONO}}>C:\</div>
      <div style={{flex: 1, whiteSpace: 'nowrap', overflow: 'hidden'}}>{title}</div>
      <div style={{display: 'flex', gap: 26, fontSize: 30}}><span>—</span><span>☐</span><span>✕</span></div>
    </div>
    <div style={{padding: 26, fontFamily: MONO, fontSize: size, color: '#E8E8E8', lineHeight: 1.45, whiteSpace: 'pre-wrap', wordBreak: 'break-all'}}>{children}</div>
  </div>
);

// Typed text: shows the first n chars of `text` between frames a..b, with a blinking block cursor while typing.
export const Typed: React.FC<{text: string; a: number; b: number; color?: string; caret?: boolean}> = ({text, a, b, color, caret = true}) => {
  const f = useCurrentFrame();
  const n = Math.round(lin(f, a, b, 0, text.length, (x) => x));
  const typing = f >= a - 10 && (f <= b + 25 || caret);
  return (
    <span style={{color}}>{text.slice(0, n)}{typing && Math.floor(f / 8) % 2 === 0 ? <span style={{background: '#E8E8E8', color: 'transparent'}}>_</span> : null}</span>
  );
};

// 3D keyboard key that presses at `press`.
export const Key: React.FC<{label: string; w?: number; h?: number; press?: number; color?: string; size?: number}> = ({label, w = 220, h = 180, press, color = P.white, size = 52}) => {
  const f = useCurrentFrame();
  const k = press === undefined ? -1 : f - press;
  const down = k >= 0 && k < 7 ? 1 - Math.abs(k - 3) / 4 : 0;
  const d = 26 * (1 - down * 0.8);
  return (
    <div style={{width: w, height: h + 26, position: 'relative'}}>
      <div style={{position: 'absolute', left: 0, top: 26, width: w, height: h, background: '#8F86C9', borderRadius: 28, border: `5px solid ${P.ink}`}} />
      <div style={{position: 'absolute', left: 0, top: 26 - d, width: w, height: h, background: color, borderRadius: 28, border: `5px solid ${P.ink}`, display: 'flex', alignItems: 'center',
        justifyContent: 'center', fontFamily: EN, fontWeight: 900, fontSize: size, color: P.ink, direction: 'ltr', whiteSpace: 'nowrap'}}>{label}</div>
    </div>
  );
};

// Brand logo from public/logos/*.svg tinted with a flat colour (CSS mask).
export const Logo: React.FC<{name: string; s: number; color?: string}> = ({name, s, color = P.white}) => (
  <div style={{width: s, height: s, background: color, WebkitMaskImage: `url(${img(`logos/${name}.svg`)})`, WebkitMaskSize: 'contain', WebkitMaskRepeat: 'no-repeat',
    WebkitMaskPosition: 'center'}} />
);
export const WinLogo: React.FC<{s: number; color?: string}> = ({s, color = '#00A4EF'}) => (
  <svg width={s} height={s} viewBox="0 0 20 20"><rect x={0} y={0} width={9.4} height={9.4} fill={color} /><rect x={10.6} y={0} width={9.4} height={9.4} fill={color} />
    <rect x={0} y={10.6} width={9.4} height={9.4} fill={color} /><rect x={10.6} y={10.6} width={9.4} height={9.4} fill={color} /></svg>
);

// Polaroid with his real footage (start sec in the source clip) + handwritten note.
export const Polaroid: React.FC<{src: string; start?: number; w: number; h: number; note?: string; pos?: string; zoom?: number; still?: boolean}> = ({src, start = 0, w, h, note, pos = '50% 50%', zoom = 1, still = false}) => {
  const {fps} = useVideoConfig();
  return (
    <div style={{width: w + 40, padding: '20px 20px 0', background: P.paper, boxShadow: '0 22px 0 rgba(12,6,50,0.4)', position: 'relative'}}>
      <div style={{width: w, height: h, overflow: 'hidden', background: '#000', position: 'relative'}}>
        {still ? <Img src={img(src)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: pos, transform: `scale(${zoom})`, transformOrigin: pos}} />
          : <OffthreadVideo muted src={img(src)} startFrom={Math.round(start * fps)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: pos, transform: `scale(${zoom})`, transformOrigin: pos}} />}
      </div>
      <div style={{height: note ? 96 : 40, fontFamily: HAND, fontSize: 52, color: P.ink, display: 'flex', alignItems: 'center', justifyContent: 'center', direction: 'rtl'}}>{note}</div>
      <div style={{position: 'absolute', top: -22, left: '50%', width: 150, height: 44, marginLeft: -75, background: 'rgba(184,255,60,0.85)', transform: 'rotate(-4deg)'}} />
    </div>
  );
};

// Neon marker loop (orbit) drawn around a point — the green ring around "NEW".
export const Orbit: React.FC<{cx: number; cy: number; rx: number; ry: number; at?: number; color?: string; rot?: number; w?: number}> = ({cx, cy, rx, ry, at = 0, color = P.lime, rot = -12, w = 12}) => {
  const f = useCurrentFrame();
  const p = lin(f, at, at + 14);
  const L = 2 * Math.PI * Math.max(rx, ry) * 1.1;
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', pointerEvents: 'none'}}>
      <ellipse cx={cx} cy={cy} rx={rx} ry={ry} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round" strokeDasharray={L} strokeDashoffset={L * (1 - p)}
        transform={`rotate(${rot + f * 0.3} ${cx} ${cy})`} />
    </svg>
  );
};

// Pill tag (Arabic or Latin).
export const Pill: React.FC<{text: string; bg?: string; color?: string; size?: number; dir?: 'rtl' | 'ltr'; font?: string}> = ({text, bg = P.lime, color = P.ink, size = 48, dir = 'rtl', font = AR}) => (
  <div style={{background: bg, color, fontFamily: font, fontWeight: 900, fontSize: size, padding: `${size * 0.12}px ${size * 0.55}px`, borderRadius: size, whiteSpace: 'nowrap', direction: dir,
    border: `4px solid ${P.ink}`, boxShadow: `0 8px 0 ${P.deep}`}}>{text}</div>
);

// Hand-drawn arrow / note in the handwriting font.
export const Note: React.FC<{text: string; size?: number; color?: string; rot?: number}> = ({text, size = 60, color = P.lime, rot = -5}) => (
  <div style={{fontFamily: HAND, fontSize: size, color, transform: `rotate(${rot}deg)`, whiteSpace: 'nowrap', direction: 'rtl', textShadow: `0 4px 0 ${P.deep}`}}>{text}</div>
);
