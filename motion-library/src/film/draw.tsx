import React from 'react';
import {useCurrentFrame} from 'remotion';
import {K, rnd} from './kit';

// Hand-drawn / engraving-style SVG pieces for the film shorts. All drawn in a local box, placed with <g transform>.
const INK = '#141210';

// Engraved eye (almond, lashes, iris with radial hatching). look = iris x shift (-1..1), open = 0..1.
export const Eye: React.FC<{x: number; y: number; s?: number; open?: number; look?: number; glow?: number}> = ({x, y, s = 1, open = 1, look = 0, glow = 0}) => {
  const h = 70 * open;
  return (
    <g transform={`translate(${x},${y}) scale(${s})`}>
      <path d={`M-150,0 Q0,${-h * 2} 150,0 Q0,${h * 2} -150,0 Z`} fill={K.white} stroke={INK} strokeWidth={7} />
      <clipPath id={`eyec${x}${y}`}><path d={`M-150,0 Q0,${-h * 2} 150,0 Q0,${h * 2} -150,0 Z`} /></clipPath>
      <g clipPath={`url(#eyec${x}${y})`}>
        <circle cx={look * 40} cy={0} r={62} fill="#6B5A3E" stroke={INK} strokeWidth={5} />
        {Array.from({length: 36}, (_, i) => {
          const a = (i / 36) * Math.PI * 2;
          return <line key={i} x1={look * 40 + Math.cos(a) * 26} y1={Math.sin(a) * 26} x2={look * 40 + Math.cos(a) * 60} y2={Math.sin(a) * 60} stroke={INK} strokeWidth={2} opacity={0.6} />;
        })}
        <circle cx={look * 40} cy={0} r={26} fill={INK} />
        <circle cx={look * 40 - 12} cy={-14} r={9} fill="#fff" />
        {glow > 0 ? <circle cx={look * 40} cy={0} r={62} fill={K.yellow} opacity={glow * 0.6} /> : null}
        {Array.from({length: 14}, (_, i) => <line key={'h' + i} x1={-150 + i * 22} y1={-h * 1.1} x2={-130 + i * 22} y2={-h * 0.7} stroke={INK} strokeWidth={2} opacity={0.35} />)}
      </g>
      {Array.from({length: 9}, (_, i) => {
        const t = 0.15 + i * 0.09, px = -150 + 300 * t, py = -h * 2 * 2 * t * (1 - t);
        return <line key={'l' + i} x1={px} y1={py} x2={px + (t - 0.5) * 40} y2={py - 34 * open} stroke={INK} strokeWidth={5} strokeLinecap="round" />;
      })}
    </g>
  );
};

export const Sun: React.FC<{x: number; y: number; r?: number; spin?: number}> = ({x, y, r = 70, spin = 0}) => (
  <g transform={`translate(${x},${y}) rotate(${spin})`}>
    {Array.from({length: 16}, (_, i) => {
      const a = (i / 16) * Math.PI * 2;
      return <line key={i} x1={Math.cos(a) * r * 1.2} y1={Math.sin(a) * r * 1.2} x2={Math.cos(a) * r * (i % 2 ? 1.55 : 1.8)} y2={Math.sin(a) * r * (i % 2 ? 1.55 : 1.8)}
        stroke={K.yellow} strokeWidth={9} strokeLinecap="round" />;
    })}
    <circle r={r} fill={K.yellow} stroke={INK} strokeWidth={6} />
    {Array.from({length: 6}, (_, i) => <path key={'c' + i} d={`M${-r * 0.6 + i * 18},${r * 0.2} q8,-10 16,0`} stroke={INK} strokeWidth={3} fill="none" opacity={0.4} />)}
  </g>
);

// Pyramid with engraved hatching on the shadow side.
export const Pyramid: React.FC<{x: number; y: number; s?: number; lit?: number}> = ({x, y, s = 1, lit = 1}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <path d="M-160,0 L0,-170 L40,0 Z" fill={lit > 0.5 ? '#E6C27A' : '#B99A5E'} stroke={INK} strokeWidth={6} strokeLinejoin="round" />
    <path d="M40,0 L0,-170 L160,0 Z" fill="#9C7C45" stroke={INK} strokeWidth={6} strokeLinejoin="round" />
    {Array.from({length: 11}, (_, i) => <line key={i} x1={45 + i * 10} y1={-2} x2={8 + i * 6} y2={-150 + i * 13} stroke={INK} strokeWidth={2.5} opacity={0.55} />)}
    {Array.from({length: 6}, (_, i) => <line key={'b' + i} x1={-150 + i * 26} y1={-14 - i * 26} x2={30 - i * 4} y2={-14 - i * 26} stroke={INK} strokeWidth={2} opacity={0.3} />)}
  </g>
);

export const Palm: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => {
  const f = useCurrentFrame();
  const sway = Math.sin(f / 18) * 3;
  return (
    <g transform={`translate(${x},${y}) scale(${s})`}>
      <path d="M0,0 Q-10,-90 6,-190" stroke={INK} strokeWidth={14} fill="none" strokeLinecap="round" />
      <g transform={`translate(6,-190) rotate(${sway})`}>
        {[-150, -110, -60, -20, 20, 60, 110, 150].map((a, i) => (
          <path key={i} d={`M0,0 Q${Math.sin((a * Math.PI) / 180) * 60},${-40 - Math.cos((a * Math.PI) / 180) * 30} ${Math.sin((a * Math.PI) / 180) * 120},${-Math.cos((a * Math.PI) / 180) * 70 + 20}`}
            stroke="#2F5D3A" strokeWidth={12} fill="none" strokeLinecap="round" />
        ))}
      </g>
    </g>
  );
};

// Simple brain (two lobes with folds); lit 0..1 glows yellow.
export const Brain: React.FC<{x: number; y: number; s?: number; lit?: number}> = ({x, y, s = 1, lit = 0}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    {lit > 0 ? <circle r={150} fill={K.yellow} opacity={0.25 * lit} /> : null}
    <path d="M0,-90 C-60,-110 -130,-80 -125,-20 C-150,20 -110,80 -60,75 C-30,100 0,80 0,60 C0,80 30,100 60,75 C110,80 150,20 125,-20 C130,-80 60,-110 0,-90 Z"
      fill={lit > 0.5 ? '#F3D9A0' : '#E7B9B0'} stroke={INK} strokeWidth={6} />
    <path d="M0,-90 L0,60" stroke={INK} strokeWidth={4} />
    {['M-100,-30 q20,-20 40,0 t40,0', 'M-110,20 q25,-18 50,0 t40,-4', 'M-80,55 q20,-14 40,-2', 'M20,-60 q20,-20 40,0 t40,10', 'M20,0 q22,-18 44,0 t40,0', 'M30,50 q20,-14 44,0'].map((d, i) => (
      <path key={i} d={d} stroke={INK} strokeWidth={4} fill="none" strokeLinecap="round" />
    ))}
  </g>
);

// Running stick figure in marker style; t = phase (radians). Ground at y.
export const Runner: React.FC<{x: number; y: number; s?: number; t: number; color?: string}> = ({x, y, s = 1, t, color = INK}) => {
  const leg = (ph: number) => {
    const th = Math.sin(t + ph) * 0.8, kn = Math.max(0, Math.sin(t + ph + 1.2)) * 1.1;
    const hx = 0, hy = -95, kx = hx + Math.sin(th) * 50, ky = hy + Math.cos(th) * 50, fx = kx + Math.sin(th - kn) * 50, fy = ky + Math.cos(th - kn) * 50;
    return <path d={`M${hx},${hy} L${kx},${ky} L${fx},${fy}`} stroke={color} strokeWidth={14} fill="none" strokeLinecap="round" strokeLinejoin="round" />;
  };
  const arm = (ph: number) => {
    const th = Math.sin(t + ph) * 0.9;
    const sx = 6, sy = -175, ex = sx + Math.sin(th) * 40, ey = sy + Math.cos(th) * 40;
    return <path d={`M${sx},${sy} L${ex},${ey} L${ex + 30},${ey - 14 + Math.sin(t + ph) * 10}`} stroke={color} strokeWidth={12} fill="none" strokeLinecap="round" />;
  };
  const bob = Math.abs(Math.sin(t)) * -8;
  return (
    <g transform={`translate(${x},${y + bob}) scale(${s})`}>
      {leg(0)}{leg(Math.PI)}
      <path d="M0,-95 L10,-185" stroke={color} strokeWidth={16} strokeLinecap="round" />
      {arm(Math.PI)}{arm(0)}
      <circle cx={18} cy={-215} r={26} fill={color} />
    </g>
  );
};

// Camera obscura cut-away: a dark room seen from the side. Outside (left): sun, palm, pyramid. Pinhole in the left
// wall; rays cross through it and draw the scene upside-down on the right wall. Props are 0..1 progress values.
export const Obscura: React.FC<{w: number; h: number; box: number; hole: number; rays: number; image: number; plate?: number; burn?: number}> = ({w, h, box, hole, rays, image, plate = 0, burn = 0}) => {
  const f = useCurrentFrame();
  const G = 1010; // ground line
  const rw = 600 * box, rh = 720 * box, rx = 440, ry = 900 - rh / 2; // room (left wall = rx), centred on y 900
  const hy = ry + rh / 2;
  const pts: [number, number][] = [[135, 690], [310, 820], [395, G]]; // palm top, pyramid tip, ground
  const wallX = rx + rw - 18;
  return (
    <svg width={w} height={h} style={{position: 'absolute', left: 0, top: 0}}>
      <Sun x={150} y={300} r={56} spin={f * 0.5} />
      <Palm x={140} y={G} s={1.45} />
      <Pyramid x={310} y={G} s={1.1} />
      <line x1={0} y1={G} x2={rx} y2={G} stroke={K.paper2} strokeWidth={5} />
      {box > 0.01 ? (
        <g>
          <rect x={rx} y={ry} width={rw} height={rh} fill="#0B0A09" stroke={K.white} strokeWidth={9} />
          {Array.from({length: 18}, (_, i) => <line key={i} x1={rx + 10} y1={ry + 10 + i * (rh / 18)} x2={rx + rw - 10} y2={ry + 10 + i * (rh / 18)} stroke="#fff" strokeWidth={1} opacity={0.05} />)}
          {hole > 0 ? <rect x={rx - 7} y={hy - 11 * hole} width={16} height={22 * hole} fill={K.yellow} /> : null}
          {rays > 0 ? pts.map(([px, py], i) => {
            const k = Math.min(1, rays * 1.2 - i * 0.1);
            if (k <= 0) return null;
            const ty = hy + (hy - py) * ((wallX - rx) / (rx - px));
            const q = Math.max(0, (k - 0.5) * 2);
            const mx = px + (rx - px) * Math.min(1, k * 2), my = py + (hy - py) * Math.min(1, k * 2);
            return (
              <g key={i}>
                <line x1={px} y1={py} x2={mx} y2={my} stroke={K.yellow} strokeWidth={6} strokeDasharray="16 11" strokeDashoffset={-f * 2} />
                {k > 0.5 ? <line x1={rx} y1={hy} x2={rx + (wallX - rx) * q} y2={hy + (ty - hy) * q} stroke={K.yellow} strokeWidth={6} strokeDasharray="16 11" strokeDashoffset={-f * 2} /> : null}
              </g>
            );
          }) : null}
          {/* the outside scene, upside-down, on the far wall (or burnt into the chemical plate) */}
          <g opacity={image} transform={`translate(${wallX - 4},${hy}) scale(${-0.62 * box},${-0.62 * box}) translate(${-60},${-G + 210})`}>
            <Palm x={140} y={G} s={1.45} />
            <Pyramid x={310} y={G} s={1.1} />
          </g>
          {plate > 0 ? (
            <g>
              <rect x={wallX - 34} y={ry + 40} width={40} height={rh - 80} fill="#8F959B" stroke={K.white} strokeWidth={4} opacity={plate} />
              <rect x={wallX - 34} y={ry + 40} width={40} height={(rh - 80) * burn} fill="#2B2B2B" opacity={plate * 0.9} />
            </g>
          ) : null}
        </g>
      ) : null}
    </svg>
  );
};

// Old hand-crank movie camera (side view): box, lens, two reels on top; crank spins with t.
export const CrankCamera: React.FC<{x: number; y: number; s?: number; t: number}> = ({x, y, s = 1, t}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    {[-70, 70].map((cx, i) => (
      <g key={i} transform={`translate(${cx},-170) rotate(${t * 40 * (i ? 1 : 1.1)})`}>
        <circle r={78} fill="#2A2621" stroke={INK} strokeWidth={6} />
        {Array.from({length: 5}, (_, k) => <circle key={k} cx={Math.cos(k * 1.256) * 44} cy={Math.sin(k * 1.256) * 44} r={16} fill={K.paper2} stroke={INK} strokeWidth={3} />)}
        <circle r={12} fill={K.paper2} />
      </g>
    ))}
    <rect x={-150} y={-100} width={300} height={190} rx={14} fill="#5A4632" stroke={INK} strokeWidth={7} />
    {Array.from({length: 7}, (_, i) => <line key={i} x1={-140} y1={-80 + i * 26} x2={140} y2={-80 + i * 26} stroke={INK} strokeWidth={2} opacity={0.35} />)}
    <rect x={150} y={-40} width={70} height={70} fill="#2A2621" stroke={INK} strokeWidth={6} />
    <circle cx={240} cy={-5} r={34} fill="#3D4A55" stroke={INK} strokeWidth={6} />
    <circle cx={240} cy={-5} r={16} fill="#9FB4C4" />
    <g transform={`translate(-150,0) rotate(${t * 60})`}>
      <line x1={0} y1={0} x2={-60} y2={0} stroke={INK} strokeWidth={10} strokeLinecap="round" />
      <circle cx={-60} cy={0} r={10} fill={K.red} />
    </g>
    <path d="M-60,90 L-110,260 M60,90 L110,260 M0,90 L0,260" stroke={INK} strokeWidth={10} strokeLinecap="round" />
  </g>
);

// Seeded tiny rng re-export for scenes that need stable random layouts.
export const r = rnd;
