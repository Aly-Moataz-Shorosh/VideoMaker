import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

// Line-icon motion graphics for the analysis cards (scene-analysis, 2026-11-06).
// One style: 3 px round strokes, white ink + ONE accent colour (the card's kind). Box 200 x 116.
export const KIND = {edit: '#F4F4F5', sound: '#22D3EE', camera: '#A78BFA'} as const;
export const SC = {'55': '#4C9BE8', '56': '#F2A93B', add: '#E5559A', x: '#7D8590'} as Record<string, string>;
const INK = '#E8EBF0';
const DIM = '#5B6573';
const st = (c = INK, w = 3) => ({stroke: c, strokeWidth: w, fill: 'none', strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const});
const loop = (f: number, n: number) => (f % n) / n;
const ease = (x: number) => 0.5 - Math.cos(Math.PI * Math.min(1, Math.max(0, x))) / 2;

const Person: React.FC<{x: number; y: number; s?: number; c?: string}> = ({x, y, s = 1, c = INK}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <circle cx={0} cy={-14} r={8} {...st(c)} />
    <path d="M-16 14 Q-16 -2 0 -2 Q16 -2 16 14" {...st(c)} />
  </g>
);
const Frame: React.FC<{x: number; y: number; w: number; h: number; c?: string; o?: number}> = ({x, y, w, h, c = INK, o = 1}) => (
  <rect x={x} y={y} width={w} height={h} rx={6} {...st(c, 2.5)} opacity={o} />
);
const Wave: React.FC<{x0: number; x1: number; y: number; a: number; c: string; ph?: number; k?: number}> = ({x0, x1, y, a, c, ph = 0, k = 0.12}) => {
  const pts: string[] = [];
  for (let x = x0; x <= x1; x += 3) pts.push(`${x},${y + Math.sin(x * k + ph) * a * Math.sin(((x - x0) / (x1 - x0)) * Math.PI)}`);
  return <polyline points={pts.join(' ')} {...st(c, 2.5)} />;
};
const Cam: React.FC<{x: number; y: number; r?: number; c?: string}> = ({x, y, r = 0, c = INK}) => (
  <g transform={`translate(${x},${y}) rotate(${r})`}>
    <rect x={-13} y={-9} width={20} height={18} rx={3} {...st(c, 2.5)} />
    <path d="M7 -5 L15 -9 L15 9 L7 5" {...st(c, 2.5)} />
  </g>
);

export const Anim: React.FC<{k: string; c: string; lead?: number; bars?: {d: number; sc: string}[]}> = ({k, c, lead, bars}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const box = (ch: React.ReactNode) => <svg width={200} height={116} viewBox="0 0 200 116">{ch}</svg>;
  const grow = (d: number, dl = 0) => ease((t - dl) / d);
  if (k === 'jcut' || k === 'bridge') {
    // Two tracks: V (scene A | scene B) and A; the audio of B starts BEFORE the picture cut.
    const cut = 128, lead2 = k === 'jcut' ? 52 : 70;
    const pa = grow(1.2, 0.2);
    return box(<>
      <text x={6} y={36} fill={DIM} fontFamily="Montserrat" fontWeight={800} fontSize={13}>V</text>
      <text x={6} y={84} fill={DIM} fontFamily="Montserrat" fontWeight={800} fontSize={13}>A</text>
      <rect x={22} y={22} width={cut - 24} height={22} rx={4} fill="#2A3340" />
      <rect x={cut + 2} y={22} width={196 - cut - 4} height={22} rx={4} fill={c} opacity={0.9} />
      <rect x={22} y={70} width={(cut - lead2) - 24} height={22} rx={4} fill="#2A3340" />
      <rect x={cut - lead2 + 2} y={70} width={(196 - (cut - lead2) - 4) * pa} height={22} rx={4} fill={c} opacity={0.9} />
      <line x1={cut} y1={12} x2={cut} y2={102} {...st('#FF5A5A', 2)} strokeDasharray="4 4" />
      <line x1={cut - lead2} y1={58} x2={cut - lead2} y2={104} {...st(c, 2)} strokeDasharray="4 4" />
      <path d={`M${cut - lead2} 108 L${cut} 108`} {...st(INK, 2)} opacity={pa} />
      <text x={cut - lead2 / 2} y={62} textAnchor="middle" fill={INK} fontFamily="Montserrat" fontWeight={800} fontSize={13} opacity={pa}>{lead ? `${lead.toFixed(1)} s` : ''}</text>
      {k === 'bridge' && <Wave x0={cut - lead2 + 4} x1={194} y={81} a={6} c="#0D1015" ph={t * 6} />}
    </>);
  }
  if (k === 'srs') {
    const side = Math.floor(t / 0.9) % 2;
    return box(<>
      <Frame x={8} y={22} w={86} h={66} c={side === 0 ? c : DIM} />
      <Frame x={106} y={22} w={86} h={66} c={side === 1 ? c : DIM} />
      <Person x={64} y={66} c={side === 0 ? INK : DIM} />
      <Person x={136} y={66} c={side === 1 ? INK : DIM} />
      <path d="M88 104 L112 104 M106 98 L112 104 L106 110" {...st(INK, 2)} transform={side ? 'rotate(180 100 104)' : ''} />
    </>);
  }
  if (k === 'react') {
    return box(<>
      <Frame x={60} y={14} w={96} h={72} c={c} />
      <Person x={108} y={64} />
      {[0, 1, 2].map((i) => {
        const p = loop(f + i * 10, 30);
        return <path key={i} d={`M${40 - p * 26} ${50 - 14} Q${48 - p * 26} 50 ${40 - p * 26} ${50 + 14}`} {...st(INK, 2.5)} opacity={1 - p} transform="scale(-1 1) translate(-80 0)" />;
      })}
      <text x={20} y={106} fill={DIM} fontFamily="Montserrat" fontWeight={700} fontSize={12}>off-screen voice</text>
    </>);
  }
  if (k === 'insert') {
    const p = grow(1.4, 0.3);
    return box(<>
      <Frame x={14} y={14} w={172} h={88} c={DIM} />
      <Person x={60} y={74} c={p > 0.5 ? DIM : INK} />
      <g transform={`translate(${interpolate(p, [0, 1], [0, 0])},0)`}>
        <path d="M136 40 L136 34 L144 34 L144 40 L150 50 L150 88 L130 88 L130 50 Z" {...st(p > 0.5 ? c : INK)} />
      </g>
      <rect x={interpolate(p, [0, 1], [24, 114])} y={interpolate(p, [0, 1], [24, 26])} width={interpolate(p, [0, 1], [72, 52])} height={interpolate(p, [0, 1], [66, 68])} rx={4} {...st(c, 2.5)} strokeDasharray="6 5" />
    </>);
  }
  if (k === 'dirty') {
    return box(<>
      <Frame x={14} y={14} w={172} h={88} c={DIM} />
      <Person x={136} y={76} s={0.8} />
      <rect x={14} y={14} width={78} height={88} rx={6} fill="#0B0E13" opacity={0.92} />
      <path d="M92 14 Q74 58 92 102" {...st(c, 2.5)} />
      <text x={22} y={62} fill={c} fontFamily="Montserrat" fontWeight={800} fontSize={12}>FG</text>
    </>);
  }
  if (k === 'static') {
    const p = ease(loop(f, 75) * 1.6);
    return box(<>
      <Frame x={40} y={14} w={120} h={88} c={c} />
      <Person x={100} y={interpolate(p, [0, 1], [74, 70])} s={interpolate(p, [0, 1], [0.9, 1.45])} />
      <Cam x={20} y={58} c={DIM} />
      <text x={6} y={110} fill={DIM} fontFamily="Montserrat" fontWeight={700} fontSize={11}>camera locked</text>
    </>);
  }
  if (k === 'arc') {
    const a = interpolate(loop(f, 90), [0, 1], [-150, -30]) * (Math.PI / 180);
    const cx = 100, cy = 64, r = 52;
    return box(<>
      <ellipse cx={cx} cy={cy} rx={r} ry={30} {...st(DIM, 2)} strokeDasharray="5 6" />
      <Person x={cx} y={cy + 10} s={0.8} />
      {(() => {
        const x = cx + Math.cos(a) * r, y = cy - Math.sin(a) * 30;
        return <Cam x={x} y={y} r={(Math.atan2(cy - y, cx - x) * 180) / Math.PI} c={c} />;
      })()}
      <path d={`M${cx - r} ${cy + 6} A ${r} 30 0 0 0 ${cx + r} ${cy + 6}`} {...st(c, 2.5)} opacity={0.5} />
    </>);
  }
  if (k === 'hidden') {
    const p = loop(f, 75);
    const dark = interpolate(p, [0.25, 0.5, 0.62, 0.85], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    const after = p > 0.56;
    return box(<>
      <Frame x={30} y={14} w={140} h={88} c={DIM} />
      {!after ? <Person x={interpolate(p, [0, 0.5], [100, 40], {extrapolateRight: 'clamp'})} y={74} /> :
        <path d="M70 100 L90 40 L110 40 L130 100" {...st(SC['56'])} />}
      <rect x={30} y={14} width={140} height={88} rx={6} fill="#000" opacity={dark} />
      {p > 0.5 && p < 0.62 && <text x={100} y={64} textAnchor="middle" fill={c} fontFamily="Montserrat" fontWeight={900} fontSize={16}>CUT</text>}
    </>);
  }
  if (k === 'cross') {
    const n = Math.floor(t / 0.45) % 6;
    return box(<>
      <text x={6} y={36} fill={SC['55']} fontFamily="Montserrat" fontWeight={800} fontSize={12}>55</text>
      <text x={6} y={84} fill={SC['56']} fontFamily="Montserrat" fontWeight={800} fontSize={12}>56</text>
      {[0, 1, 2, 3, 4, 5].map((i) => (
        <rect key={i} x={28 + i * 28} y={i % 2 ? 70 : 22} width={24} height={22} rx={4} fill={i % 2 ? SC['56'] : SC['55']} opacity={i <= n ? 0.95 : 0.18} />
      ))}
      <polyline points={[0, 1, 2, 3, 4, 5].slice(0, n + 1).map((i) => `${40 + i * 28},${i % 2 ? 81 : 33}`).join(' ')} {...st(INK, 2)} />
    </>);
  }
  if (k === 'echo') {
    return box(<>
      {[0, 1, 2, 3].map((i) => <Wave key={i} x0={20 + i * 34} x1={70 + i * 34} y={58} a={22 - i * 5} c={i === 0 ? c : INK} ph={t * 5 - i} k={0.3} />)}
      {[1, 2, 3].map((i) => <text key={i} x={45 + i * 34} y={104} textAnchor="middle" fill={DIM} fontFamily="Montserrat" fontWeight={700} fontSize={11}>{`×${i + 1}`}</text>)}
    </>);
  }
  if (k === 'asl') {
    // real shot lengths (passed through window.ASL in the card) -> drawn by the parent; here a simple pace metronome.
    const B = bars ?? [];
    const p = grow(1.6, 0.2);
    const bw = 186 / Math.max(1, B.length);
    return box(<>
      {B.map((b, i) => <rect key={i} x={8 + i * bw} y={100 - Math.min(84, b.d * 6.5) * p} width={Math.max(1, bw - 0.6)} height={Math.min(84, b.d * 6.5) * p} fill={SC[b.sc] ?? DIM} />)}
      <line x1={8} y1={101} x2={194} y2={101} {...st(DIM, 1.5)} />
    </>);
  }
  if (k === 'jump' || k === 'jump2') {
    const n = Math.floor(t / 0.6) % 3;
    const xs = k === 'jump' ? [70, 112, 92] : [80, 100, 120];
    return box(<>
      <Frame x={30} y={14} w={140} h={88} c={c} />
      <Person x={xs[n]} y={k === 'jump' ? 76 : 72} />
      {k === 'jump2' && [0, 1, 2].map((i) => <rect key={i} x={60 + i * 26} y={92 - (n >= i ? 12 : 0)} width={18} height={n >= i ? 12 : 0} fill={SC['56']} />)}
      <text x={176} y={30} fill={INK} fontFamily="Montserrat" fontWeight={900} fontSize={14}>{`${n + 1}`}</text>
    </>);
  }
  if (k === 'fade') {
    const p = grow(2.6, 0.2);
    return box(<>
      <Wave x0={10} x1={190} y={58} a={34 * (1 - p)} c={c} ph={t * 8} k={0.32} />
      <line x1={10} y1={58} x2={190} y2={58} {...st(DIM, 1.5)} opacity={p} />
      <text x={190} y={106} textAnchor="end" fill={DIM} fontFamily="Montserrat" fontWeight={800} fontSize={12}>{p > 0.95 ? 'SILENCE' : ''}</text>
    </>);
  }
  if (k === 'drips') {
    return box(<>
      {[0, 1].map((i) => {
        const p = loop(f + i * 22, 44);
        return <g key={i}>
          <path d={`M${80 + i * 40} ${8 + p * 70} q-6 9 0 13 q6 -4 0 -13`} fill={c} opacity={p < 0.8 ? 1 : 0} />
          <ellipse cx={80 + i * 40} cy={98} rx={p > 0.78 ? (p - 0.78) * 160 : 0} ry={p > 0.78 ? (p - 0.78) * 36 : 0} {...st(c, 2)} opacity={1 - (p - 0.78) * 4} />
        </g>;
      })}
      <line x1={20} y1={98} x2={180} y2={98} {...st(DIM, 1.5)} />
    </>);
  }
  if (k === 'montage') {
    const p = t * 50;
    return box(<>
      {[0, 1, 2, 3, 4, 5].map((i) => {
        const x = ((i * 58 - p) % 348 + 348) % 348 - 58;
        return <Frame key={i} x={x} y={18} w={50} h={36} c={i % 2 ? SC['56'] : INK} />;
      })}
      <Wave x0={10} x1={190} y={86} a={10} c={c} ph={t * 6} k={0.25} />
      <text x={190} y={112} textAnchor="end" fill={DIM} fontFamily="Montserrat" fontWeight={800} fontSize={11}>V.O.</text>
    </>);
  }
  if (k === 'crane') {
    const p = ease(loop(f, 90) * 1.3);
    const ang = interpolate(p, [0, 1], [10, -38]);
    return box(<>
      <line x1={10} y1={106} x2={190} y2={106} {...st(DIM, 2)} />
      <rect x={30} y={88} width={30} height={16} rx={3} {...st(INK, 2.5)} />
      <g transform={`translate(45,88) rotate(${ang})`}>
        <line x1={0} y1={0} x2={110} y2={0} {...st(c, 3)} />
        <Cam x={118} y={0} r={-ang + 18} c={INK} />
      </g>
    </>);
  }
  if (k === 'top') {
    return box(<>
      <rect x={40} y={56} width={120} height={46} rx={6} {...st(DIM, 2)} />
      <ellipse cx={100} cy={80} rx={24} ry={10} {...st(SC['56'], 2.5)} />
      <Cam x={100} y={20} r={90} c={c} />
      <line x1={100} y1={34} x2={100} y2={64} {...st(c, 2)} strokeDasharray="4 4" />
    </>);
  }
  if (k === 'track') {
    const p = loop(f, 80);
    return box(<>
      <line x1={10} y1={98} x2={190} y2={98} {...st(DIM, 2)} />
      {[0, 1, 2, 3, 4].map((i) => <line key={i} x1={((i * 50 - p * 200) % 250 + 250) % 250 - 30} y1={104} x2={((i * 50 - p * 200) % 250 + 250) % 250 - 10} y2={104} {...st(DIM, 2)} />)}
      <Person x={70} y={80} />
      <Cam x={140} y={72} r={180} c={c} />
      <path d="M150 52 L176 52 M170 46 L176 52 L170 58" {...st(c, 2)} transform="rotate(180 163 52)" />
    </>);
  }
  return box(<Frame x={20} y={20} w={160} h={76} c={c} />);
};

// Small line icons for labels / on-video marks (INSERT SHOT style: icon inside a small box).
export const MiniIcon: React.FC<{k: string; c?: string}> = ({k, c = INK}) => {
  const s = (ch: React.ReactNode) => <svg width={44} height={30} viewBox="0 0 44 30">{ch}</svg>;
  if (k === 'insert') return s(<><path d="M24 7 L24 4 L28 4 L28 7 L31 12 L31 26 L21 26 L21 12 Z" {...st(c, 2)} /><rect x={6} y={8} width={12} height={14} rx={2} {...st(c, 2)} strokeDasharray="3 3" /></>);
  if (k === 'dirty') return s(<><rect x={4} y={4} width={36} height={22} rx={3} {...st(c, 2)} /><rect x={4} y={4} width={14} height={22} rx={3} fill={c} opacity={0.8} /><circle cx={30} cy={13} r={3} {...st(c, 2)} /></>);
  if (k === 'neg') return s(<><rect x={4} y={4} width={36} height={22} rx={3} {...st(c, 2)} /><circle cx={12} cy={12} r={3} {...st(c, 2)} /><path d="M7 24 Q12 17 17 24" {...st(c, 2)} /><rect x={22} y={8} width={14} height={14} {...st(c, 1.5)} strokeDasharray="2 3" /></>);
  if (k === 'arc') return s(<><path d="M6 20 A 16 9 0 0 0 38 20" {...st(c, 2)} /><path d="M34 15 L38 20 L32 22" {...st(c, 2)} /><circle cx={22} cy={10} r={3} {...st(c, 2)} /></>);
  if (k === 'tilt') return s(<><path d="M10 24 L10 8 M6 12 L10 7 L14 12" {...st(c, 2)} /><path d="M18 18 L36 18 M32 14 L37 18 L32 22" {...st(c, 2)} /></>);
  if (k === 'fwf') return s(<><rect x={4} y={4} width={36} height={22} rx={3} {...st(c, 2)} /><rect x={14} y={8} width={16} height={18} {...st(c, 2)} /></>);
  if (k === 'top') return s(<><rect x={16} y={3} width={12} height={9} rx={2} {...st(c, 2)} /><path d="M22 12 L22 18" {...st(c, 2)} /><ellipse cx={22} cy={23} rx={12} ry={4} {...st(c, 2)} /></>);
  if (k === 'cam') return s(<><rect x={8} y={8} width={20} height={15} rx={3} {...st(c, 2)} /><path d="M28 12 L36 8 L36 23 L28 19" {...st(c, 2)} /></>);
  if (k === 'scissors') return s(<><circle cx={12} cy={21} r={4} {...st(c, 2)} /><circle cx={12} cy={9} r={4} {...st(c, 2)} /><path d="M15 11 L36 22 M15 19 L36 8" {...st(c, 2)} /></>);
  if (k === 'wave') return s(<path d="M4 15 L9 15 L12 7 L16 23 L20 4 L24 26 L28 10 L31 18 L34 15 L40 15" {...st(c, 2)} />);
  return s(<rect x={4} y={4} width={36} height={22} rx={3} {...st(c, 2)} />);
};
export const kindIcon = (k: string) => (k === 'edit' ? 'scissors' : k === 'sound' ? 'wave' : 'cam');
