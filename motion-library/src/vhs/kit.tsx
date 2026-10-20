import React from 'react';
import {AbsoluteFill, Easing, Img, OffthreadVideo, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, Halftone, img, lin, rnd, spr} from '../film/kit';

// "VHS tape" kit for the vhstodigital shorts (2026-10-09). Same engine as the film shorts (FilmShort + make_shorts.py),
// different look: CRT black-blue, VCR blue screen, on-screen display (PLAY / REC / timecode), scanlines, tracking noise,
// RGB split, and the three RCA colours (red / white / yellow) as the palette.
export const V = {
  ink: '#07080F', ink2: '#11142A', blue: '#1F33E8', blue2: '#0B1580', white: '#F2F2EE', dim: '#8A8FA8',
  red: '#E8322E', yellow: '#FFD21F', rcaW: '#ECECE4', green: '#3BE07A', mag: '#FF3EA5', cyan: '#33E1FF', shell: '#1B1B1E',
};
export const MONO = 'Montserrat';

// Background under everything: deep CRT blue-black, soft magenta/cyan glow, faint scanlines + grain.
export const VhsBg: React.FC<{tint?: string}> = ({tint = V.blue}) => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const x = 50 + 30 * Math.sin(f / 95), y = 35 + 18 * Math.cos(f / 130);
  return (
    <AbsoluteFill style={{background: V.ink}}>
      <AbsoluteFill style={{background: `radial-gradient(circle at ${x}% ${y}%, ${tint}55 0%, transparent 48%)`}} />
      <AbsoluteFill style={{background: `radial-gradient(circle at ${100 - x}% ${88 - y / 2}%, ${V.mag}22 0%, transparent 42%)`}} />
      <Grid />
      <Img src={img(`bg/grain_${Math.floor(f / 2) % 3}.png`)} style={{position: 'absolute', width, height, opacity: 0.18}} />
    </AbsoluteFill>
  );
};

// Retro perspective grid at the bottom (80s video box art), slowly moving.
export const Grid: React.FC<{op?: number; color?: string}> = ({op = 0.16, color = V.cyan}) => {
  const f = useCurrentFrame();
  const lines = [];
  for (let i = 0; i < 14; i++) {
    const t = ((i + (f / 40) % 1) / 14);
    const yy = 1250 + Math.pow(t, 2.2) * 700;
    lines.push(<line key={'h' + i} x1={0} y1={yy} x2={1080} y2={yy} stroke={color} strokeWidth={2} opacity={op * t * 1.6} />);
  }
  for (let i = -10; i <= 10; i++) lines.push(<line key={'v' + i} x1={540 + i * 30} y1={1250} x2={540 + i * 260} y2={1950} stroke={color} strokeWidth={2} opacity={op} />);
  return <svg width={1080} height={1920} style={{position: 'absolute'}}>{lines}</svg>;
};

// Look on top of everything: scanlines, a rolling tracking-noise band, RGB fringe flicker, vignette, small OSD.
export const VhsFx: React.FC<{strength?: number; osd?: boolean}> = ({strength = 1, osd = true}) => {
  const f = useCurrentFrame();
  const {width, height, fps} = useVideoConfig();
  const band = ((f * 7) % (height + 400)) - 200;
  const glitch = rnd(Math.floor(f / 4) * 17) > 0.93;
  const s = Math.floor(f / fps);
  const tc = `${Math.floor(s / 3600)}:${String(Math.floor(s / 60) % 60).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <AbsoluteFill style={{opacity: 0.22 * strength, backgroundImage: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.9) 0px, rgba(0,0,0,0.9) 2px, transparent 2px, transparent 5px)'}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: band, height: 90, opacity: 0.16 * strength,
        background: 'linear-gradient(180deg, transparent, rgba(255,255,255,0.55) 45%, rgba(255,255,255,0.15) 60%, transparent)', filter: 'blur(2px)'}} />
      <Img src={img(`bg/grain_${Math.floor(f / 2) % 3}.png`)} style={{position: 'absolute', width, height, opacity: 0.22 * strength, mixBlendMode: 'overlay'}} />
      {glitch ? <AbsoluteFill style={{background: `linear-gradient(90deg, ${V.mag}22, transparent 30%, transparent 70%, ${V.cyan}22)`}} /> : null}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, transparent 55%, rgba(0,0,0,0.6) 100%)'}} />
      {osd ? (
        <div style={{position: 'absolute', left: 64, top: 70, fontFamily: MONO, fontWeight: 800, fontSize: 40, color: V.white, letterSpacing: 2, direction: 'ltr',
          textShadow: `3px 0 ${V.mag}aa, -3px 0 ${V.cyan}aa`, opacity: 0.85}}>
          PLAY ▶<span style={{marginLeft: 30, opacity: 0.8}}>SP {tc}</span>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// Text with VHS RGB fringe.
export const Rgb: React.FC<{children: React.ReactNode; size?: number; color?: string; font?: string; dir?: 'rtl' | 'ltr'; amp?: number}> = ({children, size = 90, color = V.white, font = AR, dir = 'rtl', amp = 4}) => {
  const f = useCurrentFrame();
  const j = amp * (1 + (rnd(Math.floor(f / 3)) > 0.85 ? 2 : 0));
  return (
    <div style={{fontFamily: font, fontWeight: 900, fontSize: size, color, direction: dir, whiteSpace: 'nowrap', lineHeight: 1.15,
      textShadow: `${j}px 0 ${V.mag}cc, ${-j}px 0 ${V.cyan}cc, 0 8px 22px rgba(0,0,0,0.6)`}}>{children}</div>
  );
};

// Blue VCR screen panel with OSD-style text.
export const BluePanel: React.FC<{w: number; h: number; children?: React.ReactNode}> = ({w, h, children}) => (
  <div style={{width: w, height: h, background: V.blue, position: 'relative', overflow: 'hidden', borderRadius: 18, boxShadow: '0 30px 60px rgba(0,0,0,0.6)'}}>
    <AbsoluteFill style={{backgroundImage: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.25) 0px, rgba(0,0,0,0.25) 2px, transparent 2px, transparent 5px)'}} />
    <div style={{position: 'relative', width: '100%', height: '100%'}}>{children}</div>
  </div>
);

// Old CRT TV. Children are drawn inside the (rounded) screen. w = outer width.
export const Crt: React.FC<{w: number; children?: React.ReactNode; on?: number; knob?: boolean}> = ({w, children, on = 1, knob = true}) => {
  const h = w * 0.82, sw = w * (knob ? 0.72 : 0.86), sh = h * 0.78;
  return (
    <div style={{width: w, height: h + w * 0.06, position: 'relative', filter: 'drop-shadow(0 30px 40px rgba(0,0,0,0.6))'}}>
      <div style={{position: 'absolute', inset: 0, bottom: w * 0.06, background: 'linear-gradient(160deg,#5A4632,#3A2C1F)', borderRadius: w * 0.06,
        border: `${w * 0.012}px solid #1E160F`}} />
      <div style={{position: 'absolute', left: w * 0.05, top: h * 0.11, width: sw, height: sh, borderRadius: w * 0.07, background: '#050608', overflow: 'hidden',
        border: `${w * 0.018}px solid #15110D`}}>
        <div style={{position: 'absolute', inset: 0, transform: `scaleY(${0.02 + 0.98 * on})`, opacity: Math.min(1, on * 2)}}>{children}</div>
        <AbsoluteFill style={{backgroundImage: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.35) 0px, rgba(0,0,0,0.35) 2px, transparent 2px, transparent 4px)'}} />
        <AbsoluteFill style={{background: 'radial-gradient(ellipse at 35% 25%, rgba(255,255,255,0.18), transparent 45%), radial-gradient(ellipse at 50% 50%, transparent 60%, rgba(0,0,0,0.65) 100%)'}} />
      </div>
      {knob ? (
        <div style={{position: 'absolute', right: w * 0.04, top: h * 0.14, width: w * 0.14, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: w * 0.03}}>
          {[0, 1].map((i) => <div key={i} style={{width: w * 0.09, height: w * 0.09, borderRadius: '50%', background: '#222', border: `${w * 0.008}px solid #8B7355`}} />)}
          {Array.from({length: 6}, (_, i) => <div key={'g' + i} style={{width: w * 0.1, height: w * 0.008, background: '#1E160F'}} />)}
        </div>
      ) : null}
      <div style={{position: 'absolute', left: w * 0.12, bottom: 0, width: w * 0.08, height: w * 0.07, background: '#1E160F'}} />
      <div style={{position: 'absolute', right: w * 0.12, bottom: 0, width: w * 0.08, height: w * 0.07, background: '#1E160F'}} />
    </div>
  );
};

// Video playing inside a screen (object-fit cover); crop with pos/zoom. src = public path.
export const Footage: React.FC<{src: string; start: number; pos?: string; zoom?: number; bw?: boolean; rate?: number; filter?: string}> = ({src, start, pos = '50% 50%', zoom = 1, bw = false, rate = 1, filter}) => {
  const {fps} = useVideoConfig();
  return (
    <OffthreadVideo muted src={img(src)} startFrom={Math.round(start * fps)} playbackRate={rate}
      style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', objectPosition: pos, transform: `scale(${zoom})`, transformOrigin: pos,
        filter: filter ?? (bw ? 'grayscale(1) contrast(1.3)' : undefined)}} />
  );
};

// VHS cassette (big). spin = reel rotation (deg), label text on the sticker. Local box 600x360, centred.
export const Cassette: React.FC<{x: number; y: number; s?: number; spin?: number; label?: string; rot?: number; color?: string}> = ({x, y, s = 1, spin = 0, label = '', rot = 0, color = V.shell}) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
    <rect x={-300} y={-180} width={600} height={360} rx={22} fill={color} stroke="#000" strokeWidth={6} />
    <rect x={-270} y={-160} width={540} height={110} rx={8} fill={V.white} />
    <rect x={-270} y={-160} width={540} height={26} fill={V.red} />
    <text x={0} y={-75} textAnchor="middle" fontFamily={AR} fontWeight={900} fontSize={52} fill="#111" direction="rtl">{label}</text>
    <rect x={-190} y={-30} width={380} height={130} rx={14} fill="#0B0B0D" stroke="#333" strokeWidth={4} />
    {[-110, 110].map((cx, i) => (
      <g key={i} transform={`translate(${cx},35)`}>
        <circle r={i ? 40 : 58} fill="#3A2A1C" />
        <g transform={`rotate(${spin})`}>
          <circle r={26} fill={V.white} />
          {[0, 60, 120, 180, 240, 300].map((a) => <rect key={a} x={-4} y={-26} width={8} height={12} fill="#111" transform={`rotate(${a})`} />)}
          <circle r={9} fill="#111" />
        </g>
      </g>
    ))}
    <rect x={-300} y={120} width={600} height={60} rx={10} fill="#000" opacity={0.35} />
    {[-200, -100, 0, 100, 200].map((xx) => <rect key={xx} x={xx - 18} y={140} width={36} height={18} rx={4} fill="#000" opacity={0.6} />)}
  </g>
);

// Small camcorder tape (Hi8 / Video8). Local box 300x190.
export const SmallTape: React.FC<{x: number; y: number; s?: number; spin?: number; rot?: number; label?: string}> = ({x, y, s = 1, spin = 0, rot = 0, label = 'Hi8'}) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
    <rect x={-150} y={-95} width={300} height={190} rx={14} fill="#26262B" stroke="#000" strokeWidth={5} />
    <rect x={-130} y={-80} width={260} height={56} rx={6} fill={V.yellow} />
    <text x={0} y={-38} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={38} fill="#111">{label}</text>
    <rect x={-100} y={-8} width={200} height={70} rx={10} fill="#0B0B0D" />
    {[-55, 55].map((cx) => (
      <g key={cx} transform={`translate(${cx},27) rotate(${spin})`}>
        <circle r={22} fill={V.white} />
        {[0, 90, 180, 270].map((a) => <rect key={a} x={-3} y={-22} width={6} height={9} fill="#111" transform={`rotate(${a})`} />)}
      </g>
    ))}
  </g>
);

// VCR (video player). Local box 640x190. led = 0..1 green light, slot = tape inserted 0..1 (tape slides in).
export const Vcr: React.FC<{x: number; y: number; s?: number; led?: number; play?: boolean}> = ({x, y, s = 1, led = 1, play = false}) => {
  const f = useCurrentFrame();
  return (
    <g transform={`translate(${x},${y}) scale(${s})`}>
      <rect x={-320} y={-95} width={640} height={190} rx={14} fill="#2A2A2F" stroke="#000" strokeWidth={6} />
      <rect x={-320} y={-95} width={640} height={30} rx={10} fill="#3A3A40" />
      <rect x={-260} y={-40} width={300} height={44} rx={6} fill="#0B0B0D" stroke="#555" strokeWidth={3} />
      <rect x={70} y={-45} width={200} height={60} rx={6} fill="#061A10" />
      <text x={170} y={-4} textAnchor="middle" fontFamily={MONO} fontWeight={800} fontSize={34} fill={V.green} opacity={0.4 + 0.6 * led} direction="ltr">
        {play ? `▶ ${String(Math.floor(f / 30) % 60).padStart(2, '0')}:${String(f % 30).padStart(2, '0')}` : '-- : --'}
      </text>
      {[-240, -180, -120, -60].map((xx, i) => <rect key={xx} x={xx} y={35} width={44} height={26} rx={5} fill={i === 1 && play ? V.green : '#4A4A52'} />)}
      <circle cx={260} cy={48} r={10} fill={V.green} opacity={led} />
      <text x={-260} y={-62} fontFamily={EN} fontWeight={800} fontSize={20} fill={V.dim} direction="ltr">VIDEO CASSETTE RECORDER</text>
    </g>
  );
};

// One RCA plug pointing right (tip at x). color = red / white / yellow.
export const RcaPlug: React.FC<{x: number; y: number; color: string; s?: number; rot?: number}> = ({x, y, color, s = 1, rot = 0}) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
    <rect x={-90} y={-16} width={60} height={32} rx={8} fill={color} stroke="#000" strokeWidth={4} />
    <rect x={-32} y={-12} width={22} height={24} fill="#BFC3C9" stroke="#000" strokeWidth={3} />
    <rect x={-12} y={-5} width={14} height={10} fill="#DADDE2" stroke="#000" strokeWidth={2} />
  </g>
);

// Cable from a to b (cubic), drawn progressively p 0..1, optional flowing dashes (signal) when flow > 0.
export const Cable: React.FC<{a: number[]; b: number[]; color: string; p: number; w?: number; flow?: number; sag?: number}> = ({a, b, color, p, w = 14, flow = 0, sag = 120}) => {
  const f = useCurrentFrame();
  const d = `M${a[0]},${a[1]} C${a[0] + (b[0] - a[0]) * 0.3},${a[1] + sag} ${a[0] + (b[0] - a[0]) * 0.7},${b[1] + sag} ${b[0]},${b[1]}`;
  const L = 2600;
  return (
    <g>
      <path d={d} fill="none" stroke="#000" strokeWidth={w + 6} strokeLinecap="round" strokeDasharray={L} strokeDashoffset={L * (1 - p)} opacity={0.6} />
      <path d={d} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round" strokeDasharray={L} strokeDashoffset={L * (1 - p)} />
      {flow > 0 ? <path d={d} fill="none" stroke="#fff" strokeWidth={w * 0.4} strokeLinecap="round" strokeDasharray="6 40" strokeDashoffset={-f * 6} opacity={0.8 * flow * (p >= 1 ? 1 : 0)} /> : null}
    </g>
  );
};

// Small box device (converter / capture card). Local box w x h centred; label on top, ports text.
export const Box: React.FC<{x: number; y: number; w: number; h: number; label: string; sub?: string; color?: string; glow?: number}> = ({x, y, w, h, label, sub, color = '#2C2F3A', glow = 0}) => (
  <g transform={`translate(${x},${y})`}>
    {glow > 0 ? <rect x={-w / 2 - 18} y={-h / 2 - 18} width={w + 36} height={h + 36} rx={30} fill={V.cyan} opacity={0.25 * glow} /> : null}
    <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={18} fill={color} stroke="#000" strokeWidth={5} />
    <rect x={-w / 2} y={-h / 2} width={w} height={h * 0.22} rx={14} fill="#fff" opacity={0.08} />
    <text x={0} y={sub ? -4 : 14} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={Math.min(46, w / 6)} fill={V.white} direction="ltr">{label}</text>
    {sub ? <text x={0} y={40} textAnchor="middle" fontFamily={AR} fontWeight={800} fontSize={Math.min(34, w / 8)} fill={V.yellow} direction="rtl">{sub}</text> : null}
  </g>
);

// Laptop. Children (HTML) are shown on its screen via foreignObject. Local box 520 wide.
export const Laptop: React.FC<{x: number; y: number; s?: number; children?: React.ReactNode}> = ({x, y, s = 1, children}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <rect x={-240} y={-300} width={480} height={300} rx={18} fill="#1C1E26" stroke="#000" strokeWidth={6} />
    <rect x={-222} y={-284} width={444} height={266} rx={6} fill="#05060A" />
    <foreignObject x={-222} y={-284} width={444} height={266}><div style={{width: 444, height: 266, position: 'relative', overflow: 'hidden', borderRadius: 6}}>{children}</div></foreignObject>
    <path d="M-290,0 L290,0 L260,34 L-260,34 Z" fill="#2E313C" stroke="#000" strokeWidth={6} />
    <rect x={-50} y={4} width={100} height={10} rx={4} fill="#111" />
  </g>
);

// Port label chip (e.g. "AV", "HDMI", "USB").
export const Chip: React.FC<{text: string; bg?: string; color?: string; size?: number}> = ({text, bg = V.white, color = '#111', size = 40}) => (
  <div style={{background: bg, color, fontFamily: EN, fontWeight: 900, fontSize: size, padding: `${size * 0.12}px ${size * 0.4}px`, borderRadius: size * 0.25,
    border: '4px solid #000', direction: 'ltr', whiteSpace: 'nowrap', boxShadow: '0 10px 22px rgba(0,0,0,0.5)'}}>{text}</div>
);

// Wiggle/blink helper for "attention" accents.
export const blink = (f: number, a: number, every = 8) => (f < a ? 0 : Math.floor((f - a) / every) % 2 ? 0.35 : 1);
export {spr, lin, rnd, Halftone, Easing};
