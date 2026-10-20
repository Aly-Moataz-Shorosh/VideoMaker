import React from 'react';
import {H} from './pal';

// Flat geometric people (Egypt-kit style: no outlines, two-tone shading). Feet at (0,0), ~250 px tall at s=1.
// act: idle | talk | paint | chisel | read | write | point | pull | type | cheer
export type Look = {skin?: string; robe?: string; robe2?: string; hair?: string; hat?: string; beard?: boolean};

export const Person: React.FC<Look & {x?: number; y?: number; s?: number; face?: number; act?: string; t: number; seed?: number; ghost?: number}> = ({
  x = 0, y = 0, s = 1, face = 1, act = 'idle', t, seed = 0, skin = H.skin, robe = H.cream, robe2 = H.cream2, hair = H.ink, hat = 'none', beard = false, ghost = 0,
}) => {
  const ph = t * 2.2 + seed * 1.7;
  const breathe = Math.sin(ph) * 2;
  const talk = act === 'talk' ? Math.abs(Math.sin(t * 9 + seed)) : 0;
  // arm angles (degrees, 0 = hanging down, positive = forward)
  let fa = 8 + Math.sin(ph) * 3, ba = -6;
  if (act === 'talk') fa = 40 + Math.sin(t * 3 + seed) * 25;
  if (act === 'point') fa = 95 + Math.sin(t * 2) * 4;
  if (act === 'paint') fa = 110 + Math.sin(t * 5 + seed) * 18;
  if (act === 'chisel') fa = 70 + (Math.sin(t * 9 + seed) > 0.6 ? -20 : 10);
  if (act === 'read' || act === 'write' || act === 'type') { fa = 62 + (act === 'write' || act === 'type' ? Math.sin(t * 12 + seed) * 6 : 0); ba = 55; }
  if (act === 'pull') fa = 150 + Math.sin(t * 2.4 + seed) * 25;
  if (act === 'cheer') { fa = 160 + Math.sin(t * 6) * 12; ba = -150 - Math.sin(t * 6) * 12; }
  const skinD = H.skin2;
  const sat = ghost ? `saturate(${1 - ghost}) opacity(${1 - ghost * 0.65})` : undefined;
  const arm = (a: number, back: boolean) => (
    <g transform={`translate(${back ? -4 : 6},-170) rotate(${-a})`}>
      <rect x={-9} y={-4} width={18} height={70} rx={9} fill={back ? robe2 : robe} />
      <rect x={-8} y={58} width={16} height={26} rx={8} fill={back ? skinD : skin} />
    </g>
  );
  return (
    <g transform={`translate(${x},${y}) scale(${s * face},${s})`} style={{filter: sat}}>
      <ellipse cx={0} cy={2} rx={46} ry={9} fill="rgba(40,20,20,0.22)" />
      {arm(ba, true)}
      {/* legs */}
      <rect x={-20} y={-70} width={15} height={70} rx={5} fill={skinD} />
      <rect x={4} y={-70} width={15} height={70} rx={5} fill={skin} />
      {/* robe */}
      <path d={`M-30,${-60} L-22,${-178 + breathe} L22,${-178 + breathe} L32,${-60} Z`} fill={robe} />
      <path d={`M-30,${-60} L-22,${-178 + breathe} L-4,${-178 + breathe} L-8,${-60} Z`} fill={robe2} />
      <rect x={-24} y={-118 + breathe * 0.5} width={50} height={9} fill={H.terra} opacity={0.85} />
      {/* neck + head */}
      <rect x={-7} y={-196 + breathe} width={14} height={22} fill={skinD} />
      <g transform={`translate(0,${-222 + breathe})`}>
        <ellipse cx={2} cy={0} rx={23} ry={27} fill={skin} />
        <path d="M-22,-4 Q-24,-30 2,-30 Q26,-30 25,-6 L18,-14 Q2,-22 -14,-12 Z" fill={hair} />
        <rect x={-23} y={-14} width={9} height={30} rx={4} fill={hair} />
        <circle cx={14} cy={-3} r={2.8} fill={H.ink} />
        <path d={`M8,${12} Q15,${15 + talk * 6} 21,${11}`} stroke={H.ink} strokeWidth={2.4} fill={talk > 0.05 ? H.ink : 'none'} />
        <path d="M22,0 L29,7 L22,9" fill={skinD} />
        {beard ? <path d="M-6,10 Q8,34 24,12 L22,22 Q8,40 -8,22 Z" fill={hair} /> : null}
        {hat === 'egypt' ? <path d="M-26,-6 Q-26,-34 2,-34 Q30,-34 28,-8 L30,26 L18,8 L-14,8 L-28,28 Z" fill={H.navy} /> : null}
        {hat === 'egypt' ? <path d="M-26,-14 L28,-14" stroke={H.gold} strokeWidth={4} /> : null}
        {hat === 'turban' ? <ellipse cx={1} cy={-24} rx={28} ry={16} fill={H.cream} /> : null}
        {hat === 'turban' ? <path d="M-26,-22 Q2,-10 28,-24" stroke={H.cream2} strokeWidth={5} fill="none" /> : null}
        {hat === 'roman' ? <path d="M-24,-10 Q-24,-36 2,-36 Q28,-36 26,-10 Z" fill={H.green2} /> : null}
        {hat === 'cap' ? <path d="M-24,-12 Q-22,-38 4,-36 Q28,-34 26,-12 L40,-10 L26,-6 Z" fill={H.red} /> : null}
        {hat === 'fur' ? <path d="M-26,-4 Q-30,-38 2,-38 Q34,-38 28,-4 Q14,-18 2,-18 Q-12,-18 -26,-4 Z" fill={H.soil1} /> : null}
      </g>
      {arm(fa, false)}
    </g>
  );
};

// Flickering fire (base at 0,0)
export const Fire: React.FC<{x?: number; y?: number; s?: number; t: number}> = ({x = 0, y = 0, s = 1, t}) => {
  const f = (k: number) => Math.sin(t * 13 + k) * 0.5 + Math.sin(t * 7.3 + k * 2) * 0.5;
  return (
    <g transform={`translate(${x},${y}) scale(${s})`}>
      <ellipse cx={0} cy={0} rx={150} ry={40} fill={H.yellow} opacity={0.18 + 0.05 * f(1)} />
      <path d={`M-38,0 Q-44,${-60 + f(1) * 8} ${-6 + f(2) * 6},${-120 + f(3) * 14} Q${10 + f(4) * 5},-70 ${30},${-90 + f(5) * 10} Q44,-40 38,0 Z`} fill={H.rust} />
      <path d={`M-22,0 Q-26,-40 ${0 + f(6) * 5},${-82 + f(7) * 10} Q20,-40 24,0 Z`} fill={H.gold} />
      <path d={`M-10,0 Q-12,-24 ${2 + f(8) * 3},${-46 + f(9) * 6} Q12,-22 10,0 Z`} fill={H.cream} />
      <rect x={-46} y={-6} width={92} height={12} rx={6} fill={H.wood2} transform="rotate(8)" />
      <rect x={-46} y={-6} width={92} height={12} rx={6} fill={H.wood} transform="rotate(-10)" />
    </g>
  );
};

// Speech bubble (tail at 0,0 pointing down-left), content = icon kind
export const Bubble: React.FC<{x: number; y: number; s?: number; kind?: string; o?: number; flip?: boolean}> = ({x, y, s = 1, kind = 'dots', o = 1, flip}) => (
  <g transform={`translate(${x},${y}) scale(${s * (flip ? -1 : 1)},${s})`} opacity={o}>
    <path d="M0,0 L10,-34 L34,-34 Z" fill={H.cream} />
    <rect x={-20} y={-120} width={150} height={92} rx={36} fill={H.cream} />
    <g transform={`translate(55,-74) scale(${flip ? -1 : 1},1)`}>
      {kind === 'dots' ? [-30, 0, 30].map((d) => <circle key={d} cx={d} cy={0} r={9} fill={H.plum} />) : null}
      {kind === 'fire' ? <path d="M-16,22 Q-24,-6 0,-30 Q4,-8 14,-14 Q26,6 16,22 Z" fill={H.rust} /> : null}
      {kind === 'q' ? <text x={0} y={18} textAnchor="middle" fontFamily="Cairo" fontWeight={900} fontSize={56} fill={H.plum}>؟</text> : null}
      {kind === 'skull' ? <g><circle cx={0} cy={-4} r={20} fill={H.plum} /><rect x={-11} y={10} width={22} height={14} rx={3} fill={H.plum} /><circle cx={-7} cy={-4} r={5} fill={H.cream} /><circle cx={7} cy={-4} r={5} fill={H.cream} /></g> : null}
      {kind === 'book' ? <g><path d="M-30,-18 L0,-10 L30,-18 L30,20 L0,26 L-30,20 Z" fill={H.terra} /><path d="M0,-10 L0,26" stroke={H.cream} strokeWidth={3} /></g> : null}
    </g>
  </g>
);
