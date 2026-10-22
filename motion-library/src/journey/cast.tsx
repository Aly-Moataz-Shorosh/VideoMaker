import React from 'react';
import {useCurrentFrame} from 'remotion';

// The rest of the Oz cast, drawn in the same flat style as Dorothy and the Scarecrow (kit.tsx): outline + soft ground shadow.
// Never film footage (Aly 2026-10-22). All take (x, y) = feet line centre, s = scale (1 ≈ 400 px tall).
const OUT = 'drop-shadow(3px 0 0 #2B1D14) drop-shadow(-3px 0 0 #2B1D14) drop-shadow(0 3px 0 #2B1D14) drop-shadow(0 -3px 0 #2B1D14) drop-shadow(0 14px 10px rgba(0,0,0,0.25))';
const Svg: React.FC<{x: number; y: number; s: number; flip?: boolean; shadow?: boolean; children: React.ReactNode; rot?: number}> = ({x, y, s, flip, shadow = true, children, rot = 0}) => (
  <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', filter: OUT}}>
    {shadow ? <ellipse cx={x} cy={y + 178 * s} rx={75 * s} ry={14 * s} fill="rgba(0,0,0,0.18)" /> : null}
    <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${flip ? -s : s} ${s})`}>{children}</g>
  </svg>
);
const eyes = (f: number, look = 0, y = -122, dx = 13, r = 5.5, col = '#1A1A1A') => {
  const blink = f % 120 < 4;
  return <><ellipse cx={-dx + look * 5} cy={y} rx={r * 0.8} ry={blink ? 1 : r} fill={col} /><ellipse cx={dx + look * 5} cy={y} rx={r * 0.8} ry={blink ? 1 : r} fill={col} /></>;
};
const mouth = (f: number, talk: boolean, y = -98, w = 7) => <ellipse cx={0} cy={y} rx={w} ry={talk ? 2 + 4 * Math.abs(Math.sin(f / 2.5)) : 1.8} fill="#5A2A1A" />;

// the Tin Man: rust patches fade when he is oiled (rust 1 -> 0), stiff = no swing
export const TinMan: React.FC<{x: number; y: number; s?: number; rust?: number; walk?: boolean; talk?: boolean; flip?: boolean; look?: number; stiff?: boolean; heart?: number}> = ({x, y, s = 1, rust = 0, walk = false, talk = false, flip, look = 0, stiff = false, heart = 0}) => {
  const f = useCurrentFrame();
  const w = walk && !stiff ? Math.sin(f / 4) : 0;
  const bob = walk ? Math.abs(Math.sin(f / 4)) * -6 : 0;
  const metal = '#C9D2DA', dark = '#8E9AA6';
  const rustSpot = (cx: number, cy: number, r: number) => <circle cx={cx} cy={cy} r={r} fill="#A0522D" opacity={rust * 0.85} />;
  return (
    <Svg x={x} y={y + bob} s={s} flip={flip}>
      <g transform={`rotate(${w * 16} -14 60)`}><rect x={-26} y={56} width={22} height={112} rx={8} fill={metal} stroke={dark} strokeWidth={3} /><rect x={-30} y={160} width={30} height={16} rx={4} fill={dark} /></g>
      <g transform={`rotate(${-w * 16} 14 60)`}><rect x={4} y={56} width={22} height={112} rx={8} fill={metal} stroke={dark} strokeWidth={3} /><rect x={0} y={160} width={30} height={16} rx={4} fill={dark} /></g>
      <g transform={`rotate(${stiff ? 8 : -w * 20 + 8} -46 -58)`}><rect x={-58} y={-64} width={22} height={96} rx={9} fill={metal} stroke={dark} strokeWidth={3} />{rustSpot(-47, -10, 8)}</g>
      <g transform={`rotate(${stiff ? -8 : w * 20 - 8} 46 -58)`}><rect x={36} y={-64} width={22} height={96} rx={9} fill={metal} stroke={dark} strokeWidth={3} /></g>
      <rect x={-46} y={-76} width={92} height={136} rx={22} fill={metal} stroke={dark} strokeWidth={4} />
      {[-40, -10, 20].map((yy) => <line key={yy} x1={-44} y1={yy} x2={44} y2={yy} stroke={dark} strokeWidth={2} />)}
      {rustSpot(-18, -40, 12)}{rustSpot(22, 30, 10)}
      {/* the heart he wants */}
      <path d="M0 0 C -14 -16 -30 -4 -18 10 L 0 26 L 18 10 C 30 -4 14 -16 0 0 Z" transform="translate(0 -40) scale(0.9)" fill={heart > 0 ? '#E8175D' : 'none'} fillOpacity={heart}
        stroke="#5A6672" strokeWidth={3} strokeDasharray={heart > 0 ? undefined : '6 5'} />
      <rect x={-34} y={-150} width={68} height={70} rx={14} fill={metal} stroke={dark} strokeWidth={4} />
      {rustSpot(20, -100, 7)}
      <path d="M -36 -150 L 36 -150 L 6 -204 L -6 -204 Z" fill={dark} />
      <rect x={-6} y={-226} width={12} height={24} fill={dark} />
      {eyes(f, look, -122, 13, 6)}
      <polygon points="0,-116 -5,-104 5,-104" fill={dark} />
      {mouth(f, talk, -92, 9)}
    </Svg>
  );
};

// the Lion: big mane; scared = shaking + ears down; roar = mouth wide
export const Lion: React.FC<{x: number; y: number; s?: number; walk?: boolean; talk?: boolean; roar?: boolean; scared?: boolean; flip?: boolean; look?: number; brave?: number}> = ({x, y, s = 1, walk = false, talk = false, roar = false, scared = false, flip, look = 0, brave = 0}) => {
  const f = useCurrentFrame();
  const w = walk ? Math.sin(f / 4) : 0;
  const shake = scared ? Math.sin(f * 2.4) * 3 : 0;
  const fur = '#D9A35B', mane = '#9A5B23';
  const mn = Array.from({length: 18}, (_, i) => {
    const a = (i / 18) * Math.PI * 2, r1 = 62, r2 = 82 + (i % 2) * 10;
    return `${Math.cos(a) * (i % 2 ? r2 : r1 + 10)},${Math.sin(a) * (i % 2 ? r2 : r1 + 10) - 120}`;
  }).join(' ');
  return (
    <Svg x={x + shake} y={y} s={s} flip={flip}>
      <path d="M 40 40 Q 110 20 100 -40" stroke={fur} strokeWidth={10} fill="none" strokeLinecap="round" /><circle cx={100} cy={-44} r={12} fill={mane} />
      <g transform={`rotate(${w * 16} -16 50)`}><rect x={-30} y={40} width={26} height={126} rx={12} fill={fur} /><ellipse cx={-17} cy={168} rx={20} ry={11} fill={fur} /></g>
      <g transform={`rotate(${-w * 16} 16 50)`}><rect x={4} y={40} width={26} height={126} rx={12} fill={fur} /><ellipse cx={17} cy={168} rx={20} ry={11} fill={fur} /></g>
      <ellipse cx={0} cy={-4} rx={52} ry={72} fill={fur} />
      <ellipse cx={0} cy={10} rx={30} ry={46} fill="#F0CE94" />
      <g transform={`rotate(${scared ? 30 : -w * 18 + 10} -46 -50)`}><rect x={-60} y={-56} width={24} height={88} rx={11} fill={fur} /></g>
      <g transform={`rotate(${scared ? -30 : w * 18 - 10} 46 -50)`}><rect x={36} y={-56} width={24} height={88} rx={11} fill={fur} /></g>
      <polygon points={mn} fill={mane} />
      {brave > 0 ? <g opacity={brave}><circle cx={0} cy={-14} r={16} fill="#F2C230" stroke="#C99A1E" strokeWidth={3} /><path d="M -8 -32 L 0 -50 L 8 -32 Z" fill="#E8175D" /></g> : null}
      <circle cx={-48} cy={-168} r={14} fill={fur} transform={scared ? 'rotate(30 -48 -168)' : undefined} /><circle cx={48} cy={-168} r={14} fill={fur} />
      <ellipse cx={0} cy={-120} rx={56} ry={54} fill={fur} />
      {eyes(f, look, -128, 18, scared ? 8 : 6)}
      {scared ? <><path d="M -28 -146 L -8 -140 M 8 -140 L 28 -146" stroke="#5A2A1A" strokeWidth={4} /></> : null}
      <ellipse cx={0} cy={-104} rx={12} ry={8} fill="#5A2A1A" />
      {roar ? <ellipse cx={0} cy={-82} rx={22} ry={16 + 4 * Math.sin(f / 2)} fill="#7A1E1E" /> : mouth(f, talk, -86, 9)}
      {roar ? <><polygon points="-14,-92 -8,-80 -2,-92" fill="#fff" /><polygon points="2,-92 8,-80 14,-92" fill="#fff" /></> : null}
    </Svg>
  );
};

// the "Wizard": an ordinary man (bald, side hair, mustache, green coat, bow tie)
export const Wizard: React.FC<{x: number; y: number; s?: number; talk?: boolean; flip?: boolean; look?: number; point?: boolean}> = ({x, y, s = 1, talk = false, flip, look = 0, point = false}) => {
  const f = useCurrentFrame();
  return (
    <Svg x={x} y={y + Math.sin(f / 20) * 2} s={s} flip={flip}>
      <rect x={-28} y={56} width={24} height={116} rx={9} fill="#2B3A2E" /><rect x={4} y={56} width={24} height={116} rx={9} fill="#2B3A2E" />
      <ellipse cx={-16} cy={172} rx={22} ry={10} fill="#1A1A1A" /><ellipse cx={16} cy={172} rx={22} ry={10} fill="#1A1A1A" />
      <g transform={`rotate(${point ? -140 : 8} -50 -58)`}><rect x={-62} y={-64} width={24} height={110} rx={11} fill="#1F7A45" /><circle cx={-50} cy={50} r={12} fill="#F2C9A0" /></g>
      <g transform="rotate(-8 50 -58)"><rect x={38} y={-64} width={24} height={110} rx={11} fill="#1F7A45" /><circle cx={50} cy={50} r={12} fill="#F2C9A0" /></g>
      <path d="M -54 -72 Q 0 -86 54 -72 L 58 70 L -58 70 Z" fill="#1F7A45" />
      <path d="M -16 -78 L 0 -20 L 16 -78 Z" fill="#FFF6DF" />
      <path d="M -14 -70 L 0 -62 L 14 -70 L 14 -54 L 0 -62 L -14 -54 Z" fill="#C8102E" />
      {[-30, -6, 18].map((yy) => <circle key={yy} cx={-24} cy={yy} r={4} fill="#F2C230" />)}
      <ellipse cx={0} cy={-128} rx={44} ry={50} fill="#F2C9A0" />
      <path d="M -44 -128 Q -48 -150 -34 -160 L -30 -128 Z M 44 -128 Q 48 -150 34 -160 L 30 -128 Z" fill="#9A9A9A" />
      {eyes(f, look, -134, 15, 5)}
      <path d="M -24 -112 Q -12 -102 0 -110 Q 12 -102 24 -112 Q 12 -94 0 -102 Q -12 -94 -24 -112 Z" fill="#7A7A7A" />
      {mouth(f, talk, -96, 8)}
    </Svg>
  );
};

// the princess of the city (pink gown, crown, wand that sparkles)
export const Princess: React.FC<{x: number; y: number; s?: number; talk?: boolean; point?: number; look?: number}> = ({x, y, s = 1, talk = false, point = 0, look = 0}) => {
  const f = useCurrentFrame();
  const tw = 0.5 + 0.5 * Math.sin(f / 4);
  return (
    <Svg x={x} y={y + Math.sin(f / 18) * 3} s={s}>
      <path d="M -26 -60 L 26 -60 L 92 170 L -92 170 Z" fill="#F7A8C8" />
      <path d="M -60 60 Q 0 80 60 60" stroke="#E8789F" strokeWidth={4} fill="none" /><path d="M -76 120 Q 0 144 76 120" stroke="#E8789F" strokeWidth={4} fill="none" />
      <rect x={-30} y={-80} width={60} height={34} rx={12} fill="#F7A8C8" />
      <g transform="rotate(10 -40 -64)"><rect x={-52} y={-70} width={18} height={84} rx={9} fill="#F7DCC6" /></g>
      <g transform={`rotate(${-20 - point * 110} 40 -64)`}>
        <rect x={34} y={-70} width={18} height={84} rx={9} fill="#F7DCC6" />
        <line x1={43} y1={14} x2={43} y2={84} stroke="#C99A1E" strokeWidth={5} />
        <polygon points="43,74 50,90 66,92 53,102 58,118 43,108 28,118 33,102 20,92 36,90" fill="#F2C230" transform="translate(0 6)" />
        <circle cx={43} cy={100} r={26 * tw} fill="#FFF3B0" opacity={0.5 * point} />
      </g>
      <ellipse cx={0} cy={-120} rx={36} ry={40} fill="#F7DCC6" />
      <path d="M -40 -118 Q -46 -170 0 -168 Q 46 -170 40 -118 Q 52 -70 30 -60 L 30 -118 Q 0 -150 -30 -118 L -30 -60 Q -52 -70 -40 -118 Z" fill="#F2D27A" />
      <path d="M -24 -160 L -18 -186 L -6 -168 L 0 -192 L 6 -168 L 18 -186 L 24 -160 Z" fill="#F2C230" stroke="#C99A1E" strokeWidth={2} />
      {eyes(f, look, -122, 12, 5)}
      <circle cx={-20} cy={-106} r={6} fill="#F2A5A5" opacity={0.6} /><circle cx={20} cy={-106} r={6} fill="#F2A5A5" opacity={0.6} />
      {mouth(f, talk, -100, 6)}
    </Svg>
  );
};

// small happy people of the city (no detail, colourful)
export const Townie: React.FC<{x: number; y: number; s?: number; c: string; hop?: number}> = ({x, y, s = 1, c, hop = 0}) => {
  const f = useCurrentFrame();
  const j = Math.abs(Math.sin(f / 6 + hop)) * 14;
  return (
    <Svg x={x} y={y - j} s={s} shadow={false}>
      <rect x={-14} y={30} width={12} height={60} rx={6} fill="#5B4A3A" /><rect x={2} y={30} width={12} height={60} rx={6} fill="#5B4A3A" />
      <path d="M -36 -40 L 36 -40 L 44 40 L -44 40 Z" fill={c} />
      <circle cx={0} cy={-70} r={30} fill="#F2C9A0" />
      <path d="M -32 -76 Q 0 -120 32 -76 Z" fill={c} />
      {eyes(f + hop * 30, 0, -70, 10, 4)}
      <path d="M -8 -56 Q 0 -50 8 -56" stroke="#5A2A1A" strokeWidth={3} fill="none" />
    </Svg>
  );
};
