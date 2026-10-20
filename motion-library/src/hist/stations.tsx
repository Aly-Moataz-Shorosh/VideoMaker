import React from 'react';
import {H} from './pal';
import {Bubble, Fire, Person} from './people';

// One component per era. Local coords: x = 0 at the station centre, y = 0 on the standing line (y < 0 = up).
// Events (seconds on the short's timeline) drive the actions: ev('hands') -> 0..1 progress helpers.
export type Ev = {on: (k: string, d?: number, delay?: number) => number; has: (k: string) => boolean; t: number};
const c01 = (x: number) => Math.max(0, Math.min(1, x));
const ease = (x: number) => 1 - Math.pow(1 - c01(x), 3);
const pop = (x: number) => { const u = c01(x); return u < 1 ? 1 - Math.pow(1 - u, 3) * Math.cos(u * 7) : 1; };
const rnd = (s: number) => { const x = Math.sin(s * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

// dashed reveal of a path
const Draw: React.FC<{d: string; p: number; color: string; w?: number; len?: number; fill?: string}> = ({d, p, color, w = 8, len = 1400, fill}) => (
  <>
    {fill ? <path d={d} fill={fill} opacity={c01((p - 0.7) / 0.3)} /> : null}
    <path d={d} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={len} strokeDashoffset={len * (1 - c01(p))} />
  </>
);

// ---------- 0. speech: a tribe around a fire, a word travels from mouth to mouth ----------
export const Speech: React.FC<{e: Ev}> = ({e}) => {
  const {t} = e;
  const chain = e.on('chain', 4.5); // bubble passes person to person
  const lost = e.on('lost', 1.2);
  const ppl = [-330, -120, 120, 330];
  const k = chain * 3; const i = Math.min(2, Math.floor(k));
  const bx = ppl[i] + (ppl[i + 1] - ppl[i]) * ease(k - i) + 20, by = -300 - Math.sin((k - i) * Math.PI) * 80;
  const gens = e.on('gens', 3.0), out = ease(e.on('out', 1.5));
  return (
    <g>
      {out < 1 ? <g opacity={1 - out} transform={`scale(1,${1 - out * 0.8})`}><Fire x={0} y={0} s={1.1} t={t} /></g> : null}
      {out > 0 ? Array.from({length: 5}, (_, i) => { const ph = (t * 0.6 + i / 5) % 1; return <circle key={i} cx={Math.sin(ph * 6 + i) * 20} cy={-40 - ph * 260} r={18 + ph * 30} fill={H.stone3} opacity={(1 - ph) * 0.5 * out} />; }) : null}
      {/* generations: the secret of fire passes grandson to grandson, each one fainter */}
      {gens > 0 ? [0, 1, 2, 3].map((g) => {
        const u = c01(gens * 4.5 - g);
        return u > 0 ? <g key={g} opacity={u * (1 - g * 0.22)}><Person x={520 + g * 150} t={t + g} s={0.8 - g * 0.06} face={-1} robe={H.soil1} robe2={H.soil2} seed={30 + g} ghost={g * 0.2} />
          <Bubble x={545 + g * 150} y={-240 + g * 12} s={0.55 * pop(u)} kind={g < 2 ? 'fire' : 'q'} flip /></g> : null;
      }) : null}
      <Person x={ppl[0]} t={t} face={1} act={e.has('chain') && chain < 0.33 ? 'talk' : 'idle'} robe={H.soil1} robe2={H.soil2} hat="fur" seed={1} />
      <Person x={ppl[1]} t={t} face={1} act={chain > 0.33 && chain < 0.66 ? 'talk' : 'idle'} robe={H.terra} robe2={H.terra2} seed={2} s={0.9} />
      <Person x={ppl[2]} t={t} face={-1} act={chain > 0.66 && chain < 1 ? 'talk' : 'idle'} robe={H.soil1} robe2={H.soil2} seed={3} s={0.95} />
      <Person x={ppl[3]} t={t} face={-1} act={lost > 0 ? 'talk' : 'idle'} robe={H.sand3} robe2={H.soil1} hat="fur" seed={4} beard />
      {e.has('chain') && chain < 1 ? <Bubble x={bx} y={by} s={1.0} kind="fire" o={c01(chain * 12)} /> : null}
      {e.has('lost') ? <Bubble x={ppl[3] + 30} y={-300} s={1.05 * pop(lost)} kind="q" flip /> : null}
      {e.has('talk') ? <Bubble x={ppl[0] + 30} y={-290} s={pop(e.on('talk', 0.5))} kind="dots" /> : null}
    </g>
  );
};

// ---------- 1. village: civilisations without writing (knowledge lives only in mouths) ----------
export const Village: React.FC<{e: Ev}> = ({e}) => {
  const {t} = e;
  const fade = ease(e.on('fade', 2.2));
  const hut = (x: number, s: number, c: string) => (
    <g transform={`translate(${x},0) scale(${s})`}>
      <rect x={-90} y={-130} width={180} height={130} fill={H.stone} />
      <rect x={-90} y={-130} width={60} height={130} fill={H.stone2} />
      <path d="M-120,-120 L0,-250 L120,-120 Z" fill={H.sand3} />
      <path d="M-120,-120 L0,-250 L-20,-120 Z" fill={H.soil1} opacity={0.5} />
      <rect x={-22} y={-80} width={44} height={80} rx={20} fill={H.plum2} />
    </g>
  );
  return (
    <g style={{filter: fade ? `saturate(${1 - fade * 0.9})` : undefined}} opacity={1 - fade * 0.6}>
      {hut(-260, 1.1, H.sand3)}
      {hut(250, 0.9, H.sand3)}
      <Person x={-40} t={t} act="talk" robe={H.terra} robe2={H.terra2} beard hat="turban" seed={5} />
      <Person x={70} t={t} s={0.6} face={-1} robe={H.gold} robe2={H.sand3} seed={6} />
      <Person x={150} t={t} s={0.55} face={-1} robe={H.teal} robe2={H.teal2} seed={7} />
      {e.has('talk') ? <Bubble x={-10} y={-270} s={pop(e.on('talk', 0.5))} kind="book" /> : null}
    </g>
  );
};

// ---------- 2. cave: paintings drawn by a caveman, hand stencils "I was here" ----------
export const Cave: React.FC<{e: Ev}> = ({e}) => {
  const {t} = e;
  const paint = e.on('paint', 3.2);
  const hands = e.on('hands', 2.4);
  const bison = 'M-250,-420 Q-230,-470 -170,-470 Q-120,-500 -60,-470 Q-20,-460 -10,-420 L-20,-380 L-40,-380 L-50,-410 L-150,-410 L-170,-370 L-190,-370 L-200,-410 Q-240,-400 -250,-420 Z';
  const horse = 'M60,-470 Q110,-500 170,-480 Q210,-470 230,-440 L250,-450 L240,-420 L220,-400 L200,-380 L190,-380 L195,-410 L110,-410 L100,-375 L88,-375 L90,-415 Q60,-420 60,-470 Z';
  const deer = 'M-120,-300 Q-90,-330 -40,-320 L-20,-360 L-10,-330 L0,-370 L4,-326 Q20,-300 0,-290 L-10,-260 L-20,-260 L-25,-285 L-80,-285 L-90,-255 L-100,-255 Z';
  const hand = (x: number, y: number, r: number, k: number) => {
    const u = c01(hands * 5 - k);
    return u > 0 ? (
      <g key={k} transform={`translate(${x},${y}) rotate(${r}) scale(${0.9 + 0.1 * u})`} opacity={u}>
        <circle r={58} fill={H.terra} opacity={0.35} />
        <path d="M-20,40 L-24,-2 L-34,-30 Q-30,-40 -22,-30 L-12,-8 L-12,-52 Q-6,-60 0,-52 L0,-12 L6,-58 Q12,-64 16,-56 L12,-10 L22,-48 Q30,-52 30,-42 L22,-4 L32,-26 Q40,-26 38,-16 L24,34 Z" fill={H.cream} opacity={0.85} />
      </g>
    ) : null;
  };
  return (
    <g>
      {/* rock mass */}
      <path d="M-560,0 L-540,-520 Q-420,-700 -100,-690 Q240,-720 460,-600 Q580,-480 560,0 Z" fill={H.stone3} />
      <path d="M-560,0 L-540,-520 Q-420,-700 -100,-690 L-180,-560 Q-420,-520 -440,0 Z" fill={H.soil1} opacity={0.35} />
      <path d="M-470,0 L-460,-470 Q-300,-610 0,-600 Q300,-610 470,-470 L470,0 Z" fill={H.soil3} />
      <path d="M-430,0 L-420,-450 Q-280,-570 0,-560 Q290,-570 430,-450 L430,0 Z" fill={H.stone2} />
      <path d="M-430,0 L-420,-450 Q-280,-570 0,-560 Q-200,-480 -260,0 Z" fill={H.stone3} opacity={0.35} />
      {/* paintings */}
      <g transform="translate(0,30)">
        <Draw d={bison} p={paint * 1.6} color={H.terra2} w={7} fill={H.terra} />
        <Draw d={horse} p={paint * 1.6 - 0.5} color={H.soil3} w={7} fill={H.soil2} />
        <Draw d={deer} p={paint * 1.6 - 0.7} color={H.terra2} w={6} fill={H.rust} />
      </g>
      {hand(-330, -230, -14, 0)}{hand(-250, -140, 10, 1)}{hand(300, -260, 18, 2)}{hand(230, -150, -6, 3)}{hand(360, -150, 4, 4)}
      <Person x={-60} t={t} act={e.has('paint') && paint < 1 ? 'paint' : 'idle'} face={-1} robe={H.soil1} robe2={H.soil2} hat="fur" beard seed={8} />
      <Fire x={170} y={0} s={0.55} t={t} />
    </g>
  );
};

// ---------- 3. Sumer: ziggurat + scribe pressing wedges into a clay tablet ----------
export const Sumer: React.FC<{e: Ev}> = ({e}) => {
  const {t} = e;
  const cune = e.on('cune', 3.0);
  const z = (w: number, y: number, h: number, c: string) => <rect x={-w / 2} y={y - h} width={w} height={h} fill={c} />;
  const wedges = Array.from({length: 24}, (_, i) => {
    const u = c01(cune * 26 - i);
    const r = Math.floor(i / 6), cI = i % 6;
    return u > 0 ? <path key={i} d={`M${-70 + cI * 26},${-80 + r * 34} l14,-6 l-4,16 Z`} fill={H.soil3} opacity={u} transform={`rotate(${rnd(i) * 30 - 15} ${-70 + cI * 26} ${-80 + r * 34})`} /> : null;
  });
  return (
    <g>
      <g transform="translate(120,0)">
        {z(700, 0, 120, H.sand3)}{z(700, 0, 120 - 30, H.sand2)}
        {z(520, -120, 110, H.sand3)}{z(520, -120, 80, H.sand2)}
        {z(340, -230, 100, H.sand3)}{z(340, -230, 70, H.sand2)}
        {z(170, -330, 90, H.terra)}
        <path d="M-40,0 L-20,-330 L20,-330 L40,0 Z" fill={H.sand} opacity={0.8} />
        {[-60, -40, -20, 0, 20, 40, 60].map((d) => <rect key={d} x={d - 3} y={-325} width={6} height={325} fill={H.sand3} opacity={0.25} />)}
      </g>
      {/* tablet on a stand, big so the wedges read */}
      <g transform="translate(-260,-170)">
        <rect x={-110} y={-140} width={220} height={190} rx={34} fill={H.stone} />
        <rect x={-110} y={-140} width={220} height={60} rx={30} fill={H.cream2} opacity={0.6} />
        {wedges}
        <rect x={-14} y={50} width={28} height={120} fill={H.wood2} />
      </g>
      <Person x={-430} t={t} act={e.has('cune') && cune < 1 ? 'write' : 'idle'} face={1} robe={H.cream} robe2={H.cream2} beard hair={H.ink} seed={9} />
    </g>
  );
};

// ---------- 4. Egypt: temple pylon whose walls fill with hieroglyphs, a scribe carving ----------
const GLYPHS = ['eye', 'bird', 'ankh', 'wave', 'reed', 'sun', 'hand', 'snake'];
const Glyph: React.FC<{k: string; x: number; y: number; s?: number; c: string}> = ({k, x, y, s = 1, c}) => (
  <g transform={`translate(${x},${y}) scale(${s})`} fill={c} stroke={c}>
    {k === 'eye' ? <><path d="M-16,0 Q0,-12 16,0 Q0,12 -16,0 Z" /><path d="M-4,6 L-8,16" strokeWidth={3} /></> : null}
    {k === 'bird' ? <path d="M-14,10 L-6,-4 Q-2,-14 8,-12 L14,-10 L6,-6 L8,10 Z" /> : null}
    {k === 'ankh' ? <><ellipse cx={0} cy={-10} rx={6} ry={8} fill="none" strokeWidth={4} /><path d="M0,-2 L0,16 M-10,2 L10,2" strokeWidth={4} /></> : null}
    {k === 'wave' ? <path d="M-16,0 l5,-5 l5,5 l5,-5 l5,5 l5,-5 l5,5" fill="none" strokeWidth={3} /> : null}
    {k === 'reed' ? <path d="M-2,14 L-2,-8 Q4,-16 8,-12 Q2,-10 2,-6 L2,14 Z" /> : null}
    {k === 'sun' ? <><circle r={9} fill="none" strokeWidth={4} /><circle r={2.5} /></> : null}
    {k === 'hand' ? <path d="M-14,4 L10,4 Q16,4 16,0 Q16,-4 10,-4 L-14,-4 Z" /> : null}
    {k === 'snake' ? <path d="M-14,8 Q-8,-6 0,4 Q8,14 14,-6" fill="none" strokeWidth={4} /> : null}
  </g>
);
export const Egypt: React.FC<{e: Ev}> = ({e}) => {
  const {t} = e;
  const hi = e.on('hiero', 3.5);
  const carve = e.has('carve') ? e.on('carve', 1000) * 1000 : 0;
  const tower = (x: number, flip: number) => (
    <g transform={`translate(${x},0) scale(${flip},1)`}>
      <path d="M-170,0 L-140,-520 L150,-520 L170,0 Z" fill={H.stone} />
      <path d="M-170,0 L-140,-520 L-60,-520 L-80,0 Z" fill={H.stone2} />
      <rect x={-150} y={-545} width={310} height={30} fill={H.sand3} />
      <rect x={-150} y={-520} width={310} height={10} fill={H.terra} opacity={0.6} />
    </g>
  );
  const cols = [];
  let n = 0;
  for (let c = 0; c < 4; c++) for (let r = 0; r < 9; r++) {
    const u = c01(hi * 40 - n); n++;
    if (u <= 0) continue;
    cols.push(<Glyph key={`${c}-${r}`} k={GLYPHS[(c * 3 + r * 5) % GLYPHS.length]} x={-330 - 60 + c * 40 + (c > 1 ? 590 : 0)} y={-460 + r * 48} s={1.1 * (0.6 + 0.4 * u)} c={H.plum} />);
  }
  return (
    <g>
      {tower(-330, 1)}{tower(330, -1)}
      <rect x={-160} y={-420} width={320} height={420} fill={H.stone2} />
      <rect x={-90} y={-330} width={180} height={330} fill={H.plum2} />
      <rect x={-180} y={-440} width={360} height={40} fill={H.sand3} />
      <circle cx={0} cy={-420} r={22} fill={H.gold} />
      <path d="M-60,-420 Q0,-440 60,-420" stroke={H.gold} strokeWidth={8} fill="none" />
      {cols}
      {/* obelisk */}
      <g transform="translate(560,0)"><path d="M-36,0 L-24,-560 L0,-600 L24,-560 L36,0 Z" fill={H.stone} /><path d="M-36,0 L-24,-560 L0,-600 L-4,0 Z" fill={H.stone2} />
        {[0, 1, 2, 3, 4, 5].map((r) => <Glyph key={r} k={GLYPHS[r]} x={4} y={-500 + r * 70} c={H.stone3} />)}</g>
      <Person x={-560} t={t} act={carve > 0 && carve < 6 ? 'chisel' : 'idle'} face={1} robe={H.cream} robe2={H.cream2} hat="egypt" seed={10} />
      {carve > 0 && carve < 6 ? Array.from({length: 6}, (_, i) => {
        const ph = ((t * 3 + i / 6) % 1);
        return <circle key={i} cx={-500 + ph * 60 * (rnd(i) - 0.2)} cy={-250 - ph * 40 + ph * ph * 120} r={4} fill={H.stone2} opacity={1 - ph} />;
      }) : null}
    </g>
  );
};

// ---------- 5. Pyramids: the mystery (how were they built?) + theories ----------
export const Pyramids: React.FC<{e: Ev}> = ({e}) => {
  const {t} = e;
  const q = e.on('q', 1.0);
  const r1 = e.on('ramp1', 1.4), r2 = e.on('ramp2', 1.4), x1 = e.on('x1', 0.5), x2 = e.on('x2', 0.5), crane = e.on('crane', 1.2);
  const pyr = (x: number, w: number, h: number) => (
    <g transform={`translate(${x},0)`}>
      <path d={`M${-w / 2},0 L0,${-h} L${w / 2},0 Z`} fill={H.sand} />
      <path d={`M0,${-h} L${w / 2},0 L${w * 0.1},0 Z`} fill={H.sand3} />
      {Array.from({length: 9}, (_, i) => <path key={i} d={`M${(-w / 2) * (1 - (i + 1) / 10)},${-h * (i + 1) / 10} L${(w / 2) * (1 - (i + 1) / 10)},${-h * (i + 1) / 10}`} stroke={H.sand2} strokeWidth={3} opacity={0.6} />)}
    </g>
  );
  const qm = (x: number, y: number, k: number) => {
    const u = pop(q * 3 - k);
    return u > 0 ? <text key={k} x={x} y={y + Math.sin(t * 3 + k) * 8} textAnchor="middle" fontFamily="Cairo" fontWeight={900} fontSize={120 * u} fill={H.plum}
      stroke={H.cream} strokeWidth={10} paintOrder="stroke">؟</text> : null;
  };
  const X = (x: number, y: number, u: number) => u > 0 ? (
    <g transform={`translate(${x},${y}) scale(${pop(u)})`}><circle r={44} fill={H.red} /><path d="M-18,-18 L18,18 M18,-18 L-18,18" stroke={H.cream} strokeWidth={10} strokeLinecap="round" /></g>) : null;
  return (
    <g>
      {pyr(260, 520, 420)}{pyr(-180, 640, 520)}{pyr(-520, 300, 230)}
      {/* theory 1: straight ramp */}
      {r1 > 0 ? <g opacity={1 - x1 * 0.5}><path d={`M-500,0 L${-500 + 320 * ease(r1)},${-260 * ease(r1)} L${-500 + 320 * ease(r1)},0 Z`} fill={H.terra} opacity={0.75} />
        {X(-380, -330, x1)}</g> : null}
      {/* theory 2: spiral ramp */}
      {r2 > 0 ? <g opacity={1 - x2 * 0.5}><Draw d="M-480,-10 L120,-10 L-60,-180 L-300,-180 L-180,-350 L-100,-350" p={r2} color={H.terra} w={18} len={1900} />{X(-60, -440, x2)}</g> : null}
      {crane > 0 ? <g transform={`translate(520,0)`} opacity={ease(crane)}>
        <rect x={-10} y={-640} width={20} height={640} fill={H.navy} /><rect x={-200} y={-650} width={330} height={18} fill={H.navy} />
        <path d={`M-180,-632 L-180,${-632 + 240 * ease(crane)}`} stroke={H.ink} strokeWidth={3} /><rect x={-210} y={-400 + 240 * (ease(crane) - 1)} width={60} height={40} fill={H.sand3} /></g> : null}
      {qm(-180, -600, 0)}{qm(260, -500, 1)}{qm(-520, -300, 2)}
      <Person x={-760} t={t} act={e.has('q') ? 'point' : 'idle'} face={1} robe={H.cream} robe2={H.cream2} hat="egypt" seed={11} s={0.9} />
    </g>
  );
};

// ---------- 6. China: gate + bamboo slips unrolling with characters ----------
export const China: React.FC<{e: Ev}> = ({e}) => {
  const {t} = e;
  const b = ease(e.on('bamboo', 2.2));
  const chars = '書文字天地人火水山木日月'.split('');
  return (
    <g>
      <g transform="translate(160,0)">
        {[-210, 210].map((x) => <rect key={x} x={x - 26} y={-520} width={52} height={520} fill={H.red} />)}
        <path d="M-360,-520 Q0,-470 360,-520 L320,-600 Q0,-560 -320,-600 Z" fill={H.plum} />
        <path d="M-300,-600 Q0,-570 300,-600 L260,-660 Q0,-630 -260,-660 Z" fill={H.teal2} />
        <rect x={-230} y={-470} width={460} height={34} fill={H.red} />
        <rect x={-90} y={-440} width={180} height={70} fill={H.gold} /><text x={0} y={-390} textAnchor="middle" fontSize={50} fill={H.plum} fontWeight={900}>文字</text>
      </g>
      {/* bamboo slips: unroll from the left */}
      <g transform="translate(-460,-420)">
        {Array.from({length: 12}, (_, i) => {
          const u = c01(b * 13 - i);
          return u > 0 ? <g key={i} transform={`translate(${i * 34},0)`} opacity={u}><rect x={0} y={0} width={28} height={300} rx={6} fill={i % 2 ? H.sand : H.sand2} />
            {[0, 1, 2].map((r) => <text key={r} x={14} y={60 + r * 90} textAnchor="middle" fontSize={30} fill={H.ink}>{chars[(i + r * 5) % chars.length]}</text>)}</g> : null;
        })}
        <path d="M0,50 L410,50 M0,250 L410,250" stroke={H.wood2} strokeWidth={4} opacity={b} />
      </g>
      <Person x={-600} t={t} act={e.has('bamboo') ? 'read' : 'idle'} face={1} robe={H.teal} robe2={H.teal2} seed={12} />
    </g>
  );
};

// ---------- 7. Rome: temple facade, Latin inscription carved letter by letter ----------
export const Rome: React.FC<{e: Ev}> = ({e}) => {
  const {t} = e;
  const lat = e.on('latin', 2.8);
  const txt = 'SENATVS·POPVLVSQVE·ROMANVS';
  const shown = txt.slice(0, Math.floor(c01(lat) * txt.length));
  return (
    <g>
      <path d="M-470,-560 L0,-760 L470,-560 Z" fill={H.stone} /><path d="M-400,-575 L0,-730 L400,-575 Z" fill={H.stone2} />
      <rect x={-470} y={-560} width={940} height={90} fill={H.cream2} />
      <text x={0} y={-500} textAnchor="middle" fontFamily="Montserrat" fontWeight={700} fontSize={42} letterSpacing={3} fill={H.plum}>{shown}</text>
      {[-380, -230, -80, 80, 230, 380].map((x) => (
        <g key={x}><rect x={x - 34} y={-470} width={68} height={440} fill={H.cream} /><rect x={x - 34} y={-470} width={22} height={440} fill={H.cream2} />
          <rect x={x - 46} y={-470} width={92} height={22} fill={H.stone} /><rect x={x - 46} y={-40} width={92} height={40} fill={H.stone} /></g>
      ))}
      <Person x={-600} t={t} act={e.has('latin') && lat < 1 ? 'chisel' : 'idle'} face={1} robe={H.cream} robe2={H.cream2} hat="roman" seed={13} />
    </g>
  );
};

// ---------- 8. Paper: scrolls & books, a pigeon carries a letter, a ship sails ----------
export const Paper: React.FC<{e: Ev}> = ({e}) => {
  const {t} = e;
  const pg = e.on('pigeon', 3.2), sh = e.on('ship', 4.0), bk = e.on('book', 1.2), sheets = e.on('sheets', 2.4);
  const wing = Math.sin(t * 18) * 18;
  return (
    <g>
      {/* water strip for the ship */}
      <rect x={-560} y={-120} width={1120} height={60} fill={H.blue} opacity={0.8} />
      <path d={`M-560,-120 ${Array.from({length: 16}, (_, i) => `q35,${i % 2 ? 10 : -10} 70,0`).join(' ')}`} stroke={H.cream} strokeWidth={4} fill="none" opacity={0.6} />
      {sh > 0 ? <g transform={`translate(${-500 + 1000 * sh},-130)`}>
        <path d="M-90,0 L90,0 L60,40 L-60,40 Z" fill={H.wood} /><rect x={-4} y={-170} width={8} height={170} fill={H.wood2} />
        <path d="M4,-160 L90,-30 L4,-30 Z" fill={H.cream} /><path d="M-6,-150 L-70,-40 L-6,-40 Z" fill={H.cream2} />
        <rect x={20} y={-70} width={34} height={24} fill={H.paper} stroke={H.terra} strokeWidth={3} /></g> : null}
      {/* table with a book */}
      <rect x={-220} y={-170} width={440} height={24} fill={H.wood} /><rect x={-200} y={-146} width={24} height={146} fill={H.wood2} /><rect x={176} y={-146} width={24} height={146} fill={H.wood2} />
      <g transform={`translate(0,-170)`}>
        <path d={`M0,-6 L${-150 * ease(bk + 0.15)},${-20} L${-150 * ease(bk + 0.15)},-6 Z`} fill={H.cream2} />
        <path d="M0,-6 L-150,-20 L-150,-2 L0,8 Z" fill={H.paper} /><path d="M0,-6 L150,-20 L150,-2 L0,8 Z" fill={H.cream} />
        <path d="M0,-6 L0,8" stroke={H.terra} strokeWidth={4} />
        {[0, 1, 2].map((r) => <path key={r} d={`M${-130},${-12 + r * 5} L${-20},${-4 + r * 5} M${20},${-4 + r * 5} L${130},${-12 + r * 5}`} stroke={H.plum3} strokeWidth={2} opacity={0.6} />)}
      </g>
      {/* flying sheets */}
      {sheets > 0 ? Array.from({length: 8}, (_, i) => {
        const u = c01(sheets * 1.5 - i * 0.08);
        return u > 0 && u < 1 ? <rect key={i} x={-40 + u * (300 + i * 60)} y={-220 - u * (220 + rnd(i) * 200) + u * u * 120} width={60} height={80} fill={H.paper} stroke={H.sand3} strokeWidth={2}
          transform={`rotate(${u * 300 * (rnd(i + 3) - 0.5)} ${-10 + u * (300 + i * 60)} ${-180 - u * 220})`} /> : null;
      }) : null}
      {/* scroll rack */}
      <g transform="translate(380,0)">
        <rect x={-110} y={-420} width={220} height={420} fill={H.wood2} />
        {[0, 1, 2, 3].map((r) => [0, 1, 2, 3].map((c) => <g key={`${r}${c}`} transform={`translate(${-80 + c * 54},${-370 + r * 100})`}><circle r={22} fill={H.paper} /><circle r={8} fill={H.sand3} /></g>))}
      </g>
      <Person x={-380} t={t} act={e.has('book') ? 'read' : 'idle'} face={1} robe={H.terra} robe2={H.terra2} hat="turban" beard seed={14} />
      {/* pigeon with a letter */}
      {pg > 0 && pg < 1 ? <g transform={`translate(${-600 + 1400 * pg},${-560 - Math.sin(pg * Math.PI) * 120})`}>
        <ellipse cx={0} cy={0} rx={34} ry={18} fill={H.cream} /><circle cx={30} cy={-12} r={13} fill={H.cream} /><path d="M40,-12 L54,-8 L40,-6 Z" fill={H.gold} />
        <path d={`M-6,-6 L-40,${-46 - wing} L10,-10 Z`} fill={H.cream2} /><path d="M-34,0 L-58,-10 L-56,10 Z" fill={H.cream2} />
        <rect x={-10} y={10} width={24} height={16} fill={H.paper} stroke={H.terra} strokeWidth={2} /></g> : null}
    </g>
  );
};

// ---------- 9. Baghdad: House of Wisdom (domes, shelves of books); 'burn' = fire + books into the river ----------
export const Baghdad: React.FC<{e: Ev}> = ({e}) => {
  const {t} = e;
  const burn = e.on('burn', 3.0);
  const lib = e.on('lib', 2.0);
  const ink = e.on('ink', 2.5);
  return (
    <g>
      <rect x={-560} y={-60} width={1120} height={60} fill={ink > 0 ? `rgb(${46 - 20 * ink},${58 - 30 * ink},${107 - 60 * ink})` : H.navy} opacity={0.85} />
      <g transform="translate(0,-60)">
        <rect x={-420} y={-380} width={840} height={380} fill={H.cream2} />
        <rect x={-420} y={-380} width={260} height={380} fill={H.stone} />
        {[-300, -100, 100, 300].map((x) => <path key={x} d={`M${x - 60},0 L${x - 60},-200 Q${x},-290 ${x + 60},-200 L${x + 60},0 Z`} fill={H.plum2} />)}
        {/* shelves of books inside the arches */}
        {[-300, -100, 100, 300].map((x, j) => [0, 1, 2].map((r) => Array.from({length: 6}, (_, i) => {
          const u = c01(lib * 20 - (j * 18 + r * 6 + i) * 0.25);
          return <rect key={`${j}${r}${i}`} x={x - 50 + i * 17} y={-60 - r * 56 - 40 * u} width={14} height={40 * u} fill={[H.terra, H.gold, H.teal, H.cream, H.red, H.navy][(i + r + j) % 6]} />;
        })))}
        <ellipse cx={0} cy={-380} rx={180} ry={150} fill={H.teal} /><ellipse cx={-60} cy={-400} rx={70} ry={90} fill={H.teal2} opacity={0.4} />
        <rect x={-190} y={-392} width={380} height={24} fill={H.gold} /><rect x={-6} y={-560} width={12} height={40} fill={H.gold} /><circle cx={0} cy={-570} r={12} fill={H.gold} />
        <g transform="translate(-360,0)"><rect x={-26} y={-620} width={52} height={620} fill={H.stone} /><ellipse cx={0} cy={-620} rx={40} ry={30} fill={H.teal} /><rect x={-36} y={-470} width={72} height={18} fill={H.gold} /></g>
      </g>
      {burn > 0 ? Array.from({length: 7}, (_, i) => <g key={i} transform={`translate(${-330 + i * 110},-140)`} opacity={Math.min(1, burn * 3)}><Fire t={t + i} s={0.6 + 0.6 * ease(burn) * (0.6 + rnd(i))} /></g>) : null}
      {burn > 0 ? Array.from({length: 10}, (_, i) => {
        const u = c01(burn * 1.6 - i * 0.07);
        return u > 0 && u < 1 ? <rect key={i} x={-250 + i * 55} y={-200 + u * u * 170} width={20} height={34} fill={[H.terra, H.gold, H.teal, H.red][i % 4]} transform={`rotate(${u * 200} ${-240 + i * 55} ${-180 + u * u * 170})`} /> : null;
      }) : null}
      {burn > 0 ? <rect x={-560} y={-1100} width={1120} height={1100} fill={H.plum2} opacity={0.18 * ease(burn)} /> : null}
      <Person x={-560} t={t} act={e.has('lib') ? 'read' : 'idle'} face={1} robe={H.cream} robe2={H.cream2} hat="turban" beard seed={15} />
      <Person x={560} t={t} act="read" face={-1} robe={H.navy} robe2={H.plum3} hat="turban" seed={16} s={0.95} />
    </g>
  );
};

// ---------- 10. Printing press: platen comes down, copies multiply and fly out ----------
export const Press: React.FC<{e: Ev}> = ({e}) => {
  const {t} = e;
  const pr = e.has('press') ? e.on('press', 1000) * 1000 : 0; // seconds since the first press
  const cyc = pr > 0 ? (pr * 0.55) % 1 : 0;
  const down = pr > 0 ? (cyc < 0.25 ? ease(cyc / 0.25) : cyc < 0.45 ? 1 : 1 - ease((cyc - 0.45) / 0.3)) : 0;
  const nCopies = pr > 0 ? Math.min(14, Math.floor(pr * 0.55 * 2) + 1) : 0;
  const fly = e.on('copies', 3.0);
  return (
    <g>
      <g transform="translate(-40,0)">
        {[-170, 170].map((x) => <rect key={x} x={x - 24} y={-640} width={48} height={640} fill={H.wood} />)}
        <rect x={-210} y={-660} width={420} height={50} fill={H.wood2} /><rect x={-210} y={-380} width={420} height={40} fill={H.wood2} />
        <rect x={-10} y={-610} width={20} height={150 + 40 * down} fill={H.stone3} />
        {/* screw handle */}
        <rect x={-150} y={-540 + 10 * down} width={300} height={14} rx={7} fill={H.wood2} transform={`rotate(${-20 + 40 * down} 0 ${-533 + 10 * down})`} />
        <rect x={-120} y={-460 + 40 * down} width={240} height={34} fill={H.wood} />
        <rect x={-180} y={-340} width={360} height={30} fill={H.wood2} /><rect x={-150} y={-350} width={300} height={10} fill={H.paper} />
        <rect x={-170} y={-310} width={30} height={310} fill={H.wood2} /><rect x={140} y={-310} width={30} height={310} fill={H.wood2} />
      </g>
      {/* stack of copies grows */}
      <g transform="translate(330,0)">
        <rect x={-110} y={-40} width={220} height={40} fill={H.wood2} />
        {Array.from({length: nCopies}, (_, i) => <rect key={i} x={-90 + (rnd(i) - 0.5) * 10} y={-52 - i * 12} width={180} height={12} fill={i % 2 ? H.paper : H.cream} stroke={H.sand3} strokeWidth={1.5} />)}
      </g>
      {fly > 0 ? Array.from({length: 18}, (_, i) => {
        const u = c01(fly * 1.4 - i * 0.04);
        return u > 0 && u < 1 ? <g key={i} transform={`translate(${330 + u * (500 + rnd(i) * 900)},${-200 - Math.sin(u * Math.PI) * (200 + rnd(i + 9) * 300)}) rotate(${u * 360 * (rnd(i + 2) - 0.5)})`}>
          <rect x={-34} y={-44} width={68} height={88} fill={H.paper} stroke={H.sand3} strokeWidth={2} />
          {[0, 1, 2, 3].map((r) => <rect key={r} x={-24} y={-30 + r * 16} width={48} height={5} fill={H.plum3} opacity={0.5} />)}</g> : null;
      }) : null}
      <Person x={-300} t={t} act={pr > 0 ? 'pull' : 'idle'} face={1} robe={H.navy} robe2={H.plum3} hat="cap" beard seed={17} />
    </g>
  );
};

// ---------- 11. Computer: desk, CRT, a document types itself; web cards pop ----------
export const Computer: React.FC<{e: Ev}> = ({e}) => {
  const {t} = e;
  const ty = e.on('type', 3.0), web = e.on('web', 1.6);
  return (
    <g>
      <rect x={-300} y={-260} width={600} height={30} fill={H.wood} /><rect x={-280} y={-230} width={30} height={230} fill={H.wood2} /><rect x={250} y={-230} width={30} height={230} fill={H.wood2} />
      <g transform="translate(0,-260)">
        <rect x={-180} y={-330} width={360} height={300} rx={26} fill={H.stone} /><rect x={-180} y={-330} width={110} height={300} rx={26} fill={H.stone2} />
        <rect x={-150} y={-300} width={300} height={220} rx={14} fill="#F7F3EA" />
        <rect x={-150} y={-300} width={300} height={26} rx={10} fill={H.blue} />
        {Array.from({length: 8}, (_, i) => <rect key={i} x={-130} y={-260 + i * 22} width={(i === 7 ? 120 : 250) * c01(ty * 8 - i)} height={8} fill={H.plum3} opacity={0.7} />)}
        <rect x={-40} y={-30} width={80} height={30} fill={H.stone2} /><rect x={-160} y={10} width={320} height={22} rx={6} fill={H.stone} />
      </g>
      {web > 0 ? [[-430, -640, H.blue], [-120, -720, H.red], [220, -680, H.teal], [470, -560, H.gold]].map(([x, y, c], i) => {
        const u = pop(web * 2.2 - i * 0.3);
        return u > 0 ? <g key={i} transform={`translate(${x},${(y as number) + Math.sin(t * 2 + i) * 10}) scale(${u})`}>
          <rect x={-90} y={-60} width={180} height={120} rx={16} fill={H.cream} /><rect x={-90} y={-60} width={180} height={28} rx={14} fill={c as string} />
          <circle cx={-56} cy={6} r={20} fill={c as string} opacity={0.6} /><rect x={-26} y={-6} width={96} height={10} rx={5} fill={H.plum3} opacity={0.5} /><rect x={-26} y={14} width={70} height={10} rx={5} fill={H.plum3} opacity={0.4} /></g> : null;
      }) : null}
      <Person x={-420} t={t} act={e.has('type') && ty < 1 ? 'type' : 'idle'} face={1} robe={H.teal} robe2={H.teal2} hair={H.soil3} seed={18} />
    </g>
  );
};

// ---------- 12. Now: big phone + screen with a video playing, icons and emojis orbit; viewers ----------
export const Now: React.FC<{e: Ev}> = ({e}) => {
  const {t} = e;
  const v = e.on('video', 1.2), icons = e.on('icons', 1.6), world = e.on('world', 1.6);
  const board = e.has('board') ? e.on('board', 1000) * 1000 : 0, hearts = e.on('hearts', 1), pct = e.on('pct', 1.6), emoji = e.on('emoji', 0.6);
  const play = (v > 0 ? pop(v) : 0);
  const ic = ['▶', '❤', '😂', '👍', '📷', '✏️'];
  return (
    <g>
      {/* big screen */}
      <g transform="translate(60,-260)">
        <rect x={-300} y={-430} width={600} height={360} rx={20} fill={H.ink} /><rect x={-280} y={-410} width={560} height={320} rx={10} fill={H.navy} />
        <circle cx={-120} cy={-300} r={60} fill={H.gold} opacity={0.9} /><path d="M-280,-90 L-150,-230 L-40,-140 L60,-260 L280,-90 Z" fill={H.teal} />
        <rect x={-280} y={-120} width={560 * ((t * 0.12) % 1)} height={8} fill={H.red} />
        <g transform={`translate(0,-250) scale(${play})`}><circle r={52} fill={H.red} /><path d="M-16,-26 L30,0 L-16,26 Z" fill={H.cream} /></g>
        <rect x={-16} y={-70} width={32} height={70} fill={H.ink} /><rect x={-110} y={0} width={220} height={20} rx={8} fill={H.ink} />
      </g>
      {/* phone */}
      <g transform={`translate(-330,-250) rotate(${-8 + Math.sin(t * 1.5) * 2})`}>
        <rect x={-90} y={-180} width={180} height={340} rx={26} fill={H.ink} /><rect x={-78} y={-164} width={156} height={300} rx={14} fill={H.cream} />
        <rect x={-78} y={-164} width={156} height={120} rx={10} fill={H.terra} /><g transform={`translate(0,-104) scale(${play * 0.6})`}><circle r={30} fill={H.cream} /><path d="M-9,-15 L17,0 L-9,15 Z" fill={H.terra} /></g>
        {[0, 1, 2].map((r) => <rect key={r} x={-62} y={-24 + r * 34} width={124} height={22} rx={8} fill={H.cream2} />)}
      </g>
      {icons > 0 ? ic.map((s, i) => {
        const a = (i / ic.length) * Math.PI * 2 + t * 0.6, u = pop(icons * 2 - i * 0.15);
        return u > 0 ? <g key={i} transform={`translate(${60 + Math.cos(a) * 420},${-520 + Math.sin(a) * 160}) scale(${u})`}>
          <circle r={46} fill={H.cream} /><text y={18} textAnchor="middle" fontSize={50}>{s}</text></g> : null;
      }) : null}
      {board > 0 ? <g opacity={ease(board * 2)}>
        <g transform="translate(560,-120)"><rect x={-8} y={-300} width={16} height={300} fill={H.plum2} /><rect x={-150} y={-560} width={300} height={260} rx={10} fill={H.cream} />
          <rect x={-136} y={-546} width={272} height={232} rx={6} fill={H.terra} /><path d="M0,-380 C-60,-430 -70,-480 -30,-490 C-10,-494 0,-480 0,-470 C0,-480 10,-494 30,-490 C70,-480 60,-430 0,-380 Z" fill={H.cream} transform={`translate(0,${-Math.sin(t * 4) * 6})`} /></g>
        <Person x={-560 + 800 * c01(board * 0.35)} t={t} s={0.8} act={board > 2.6 ? 'point' : 'idle'} face={1} robe={H.navy} robe2={H.plum3} hair={H.soil3} seed={40} />
      </g> : null}
      {hearts > 0 ? Array.from({length: 9}, (_, i) => { const ph = (t * 0.5 + i / 9) % 1; return <path key={i} d="M0,10 C-24,-8 -20,-26 -6,-26 C0,-26 0,-20 0,-18 C0,-20 0,-26 6,-26 C20,-26 24,-8 0,10 Z" fill={[H.red, H.rust, H.gold][i % 3]}
        transform={`translate(${-400 + i * 100 + Math.sin(t * 2 + i) * 20},${-300 - ph * 500}) scale(${1.2 + rnd(i)})`} opacity={(1 - ph) * c01(hearts * 3)} />; }) : null}
      {pct > 0 ? <g transform="translate(-330,-600) scale(0.85)">
        <circle r={150} fill={H.cream} /><circle r={110} fill="none" stroke={H.cream2} strokeWidth={60} />
        <circle r={110} fill="none" stroke={H.red} strokeWidth={60} strokeDasharray={`${2 * Math.PI * 110 * 0.82 * ease(pct)} 999`} transform="rotate(-90)" />
        <text y={22} textAnchor="middle" fontFamily="Cairo" fontWeight={900} fontSize={64} fill={H.plum}>{Math.round(82 * ease(pct))}%</text>
        <text y={210} textAnchor="middle" fontFamily="Cairo" fontWeight={900} fontSize={48} fill={H.plum} stroke={H.cream} strokeWidth={8} paintOrder="stroke">فيديو</text></g> : null}
      {emoji > 0 ? <g transform={`translate(-380,-620) scale(${pop(emoji)})`}>
        <rect x={-150} y={-60} width={300} height={110} rx={40} fill={H.cream} /><path d="M-110,48 L-140,90 L-70,48 Z" fill={H.cream} />
        <rect x={-120} y={-30} width={150} height={16} rx={8} fill={H.plum3} opacity={0.5} /><rect x={-120} y={0} width={110} height={16} rx={8} fill={H.plum3} opacity={0.4} />
        <circle cx={90} cy={-4} r={42} fill={H.gold} /><circle cx={76} cy={-14} r={6} fill={H.plum} /><circle cx={104} cy={-14} r={6} fill={H.plum} /><path d="M66,6 Q90,34 114,6 Z" fill={H.plum} /></g> : null}
      {world > 0 ? [-480, 60, 560].map((x, i) => {
        const u = pop(world * 2 - i * 0.3);
        return u > 0 ? <g key={i}><Person x={x} t={t + i} s={0.85} act="cheer" face={i === 2 ? -1 : 1} robe={[H.red, H.navy, H.terra][i]} robe2={H.plum2} seed={20 + i} />
          <g transform={`translate(${x},-300) scale(${u})`}><Flag k={i} /></g></g> : null;
      }) : null}
    </g>
  );
};

// simple drawn flags (emoji flags don't render on Windows): 0 China, 1 USA, 2 Egypt
const Flag: React.FC<{k: number}> = ({k}) => (
  <g>
    <rect x={-3} y={-10} width={6} height={90} fill={H.wood2} />
    <g transform="translate(3,-10)">
      {k === 0 ? <><rect width={96} height={64} fill="#DE2910" /><path d="M18,10 l4,12 h12 l-10,7 l4,12 l-10,-8 l-10,8 l4,-12 l-10,-7 h12 Z" fill="#FFDE00" /></> : null}
      {k === 1 ? <>{Array.from({length: 7}, (_, i) => <rect key={i} y={i * 9.2} width={96} height={4.6} fill="#B22234" />)}<rect width={96} height={64} fill="none" stroke="#fff" strokeWidth={0} /><rect width={40} height={34} fill="#3C3B6E" /></> : null}
      {k === 2 ? <><rect width={96} height={21} fill="#CE1126" /><rect y={21} width={96} height={22} fill="#fff" /><rect y={43} width={96} height={21} fill="#000" /><circle cx={48} cy={32} r={6} fill="#C09300" /></> : null}
    </g>
  </g>
);

// ---------- -1. weak human: animals beat him (fangs, speed, cold, heat) -> the mind -> tools -> together ----------
const Animal: React.FC<{k: string; x: number; t: number; s?: number}> = ({k, x, t, s = 1}) => (
  <g transform={`translate(${x},0) scale(${s})`}>
    {k === 'lion' ? <g><ellipse cx={0} cy={-110} rx={130} ry={60} fill={H.sand3} /><rect x={-110} y={-80} width={26} height={80} fill={H.sand3} /><rect x={80} y={-80} width={26} height={80} fill={H.sand3} />
      <circle cx={130} cy={-160} r={78} fill={H.terra2} /><circle cx={140} cy={-160} r={50} fill={H.sand2} /><circle cx={158} cy={-172} r={6} fill={H.ink} />
      <path d={`M150,-138 L196,${-140 + Math.abs(Math.sin(t * 3)) * 18} L150,-122 Z`} fill={H.plum} /><path d="M160,-138 l6,12 l6,-12 M176,-138 l6,12 l6,-12" fill={H.cream} />
      <path d="M-130,-120 Q-190,-150 -170,-200" stroke={H.sand3} strokeWidth={14} fill="none" /></g> : null}
    {k === 'cheetah' ? <g transform={`translate(${Math.sin(t * 9) * 6},0)`}><ellipse cx={0} cy={-90} rx={140} ry={38} fill={H.gold} />
      {[-90, -40, 10, 60, -60, 30].map((d, i) => <circle key={i} cx={d} cy={-96 + (i % 2) * 14} r={7} fill={H.plum} />)}
      <circle cx={140} cy={-110} r={34} fill={H.gold} /><circle cx={150} cy={-118} r={5} fill={H.ink} />
      <path d={`M-100,-60 L${-150 + Math.sin(t * 18) * 30},0 M-60,-60 L${-30 - Math.sin(t * 18) * 30},0 M80,-60 L${40 + Math.sin(t * 18) * 30},0 M110,-60 L${150 - Math.sin(t * 18) * 30},0`} stroke={H.gold} strokeWidth={16} strokeLinecap="round" />
      {[0, 1, 2].map((i) => <rect key={i} x={-260 - i * 40} y={-110 + i * 20} width={80} height={6} rx={3} fill={H.cream} opacity={0.6} />)}</g> : null}
    {k === 'bear' ? <g><ellipse cx={0} cy={-120} rx={130} ry={80} fill="#F4F1EA" /><circle cx={120} cy={-190} r={56} fill="#F4F1EA" /><circle cx={130} cy={-196} r={6} fill={H.ink} /><circle cx={170} cy={-186} r={8} fill={H.ink} />
      {[-90, -40, 50, 100].map((d) => <rect key={d} x={d - 18} y={-60} width={36} height={60} rx={12} fill="#E6E1D6" />)}</g> : null}
    {k === 'camel' ? <g><ellipse cx={0} cy={-170} rx={130} ry={50} fill={H.sand2} /><ellipse cx={-30} cy={-220} rx={60} ry={50} fill={H.sand2} /><ellipse cx={50} cy={-215} rx={50} ry={44} fill={H.sand2} />
      <path d="M110,-180 Q150,-260 150,-300" stroke={H.sand2} strokeWidth={36} fill="none" strokeLinecap="round" /><ellipse cx={170} cy={-306} rx={34} ry={20} fill={H.sand2} />
      {[-90, -50, 60, 100].map((d) => <rect key={d} x={d - 9} y={-130} width={18} height={130} fill={H.sand3} />)}</g> : null}
  </g>
);
export const Weak: React.FC<{e: Ev}> = ({e}) => {
  const {t} = e;
  const ks: [string, number][] = [['lion', -560], ['cheetah', -170], ['bear', 230], ['camel', 600]];
  const shown = (k: string) => e.on(k, 0.6);
  const brain = e.on('brain', 1.0), tools = e.on('tools', 1.2), team = e.on('team', 2.0);
  const X_ = (x: number, u: number) => u > 0.35 ? <g transform={`translate(${x},-360) scale(${pop((u - 0.35) * 2)})`}><circle r={40} fill={H.red} /><path d="M-15,-15 L15,15 M15,-15 L-15,15" stroke={H.cream} strokeWidth={9} strokeLinecap="round" /></g> : null;
  const cold = shown('bear'), hot = shown('camel');
  return (
    <g>
      {ks.map(([k, x]) => { const u = shown(k); return u > 0 ? <g key={k} opacity={ease(u * 2) * (brain > 0 ? 0.35 : 1)} transform={`translate(0,${(1 - ease(u)) * 60})`}><Animal k={k} x={x} t={t} s={0.85} />{X_(x, e.on(k, 1.6))}</g> : null; })}
      {cold > 0 && brain === 0 ? Array.from({length: 14}, (_, i) => <circle key={i} cx={130 + rnd(i) * 220} cy={-500 + ((t * 120 + rnd(i + 3) * 500) % 500)} r={5} fill="#fff" opacity={0.8} />) : null}
      {hot > 0 && brain === 0 ? [0, 1, 2].map((i) => <path key={i} d={`M${500 + i * 60},-420 q15,-20 0,-40 q-15,-20 0,-40`} stroke={H.rust} strokeWidth={6} fill="none" opacity={0.6} transform={`translate(0,${-((t * 40) % 40)})`} />) : null}
      <Person x={20} t={t} s={0.75} act={tools > 0 ? 'point' : 'idle'} face={1} robe={H.soil1} robe2={H.soil2} hat="fur" seed={50} />
      {brain > 0 ? <g transform={`translate(30,-300) scale(${pop(brain)})`}>
        <circle r={90 + Math.sin(t * 4) * 6} fill={H.yellow} opacity={0.35} />
        <path d="M-50,10 Q-62,-40 -20,-48 Q0,-70 24,-50 Q62,-44 52,0 Q60,30 24,36 Q0,52 -24,38 Q-58,36 -50,10 Z" fill="#F2A2A8" />
        <path d="M0,-50 L0,40 M-34,-20 Q-14,-10 -30,10 M30,-24 Q12,-8 32,14" stroke="#C86C78" strokeWidth={5} fill="none" /></g> : null}
      {tools > 0 ? <g opacity={ease(tools)}><rect x={70} y={-260} width={8} height={240} fill={H.wood2} transform="rotate(12 74 -140)" /><path d="M96,-282 L112,-240 L86,-244 Z" fill={H.stone3} />
        <Fire x={-140} y={0} s={0.5 * ease(tools)} t={t} /></g> : null}
      {team > 0 ? [-420, -280, 300, 440].map((x, i) => { const u = c01(team * 4 - i); return u > 0 ? <Person key={i} x={x} t={t + i} s={0.72} act="cheer" face={x < 0 ? 1 : -1} robe={[H.terra, H.soil1, H.sand3, H.teal][i]} robe2={H.plum2} seed={60 + i} /> : null; }) : null}
    </g>
  );
};

// ---------- 13. future: teach your kids, one vacation at a time (Photoshop -> montage -> motion) ----------
export const Future: React.FC<{e: Ev}> = ({e}) => {
  const {t} = e;
  const v = ['ps', 'edit', 'motion'].map((k) => e.on(k, 0.8));
  const job = e.on('job', 1.2);
  const desk = (x: number, k: number) => {
    const u = v[k];
    return (
      <g key={k} transform={`translate(${x},0)`} opacity={u > 0 ? 1 : 0.35}>
        <g transform={`translate(0,-470) scale(${u > 0 ? pop(u) : 0.8})`}><rect x={-90} y={-50} width={180} height={100} rx={16} fill={H.cream} /><rect x={-90} y={-50} width={180} height={30} rx={14} fill={[H.blue, H.terra, H.teal][k]} />
          <circle cx={-50} cy={20} r={16} fill={H.gold} /><text x={20} y={34} textAnchor="middle" fontFamily="Cairo" fontWeight={900} fontSize={34} fill={H.plum}>{`أجازة ${k + 1}`}</text></g>
        <rect x={-130} y={-170} width={260} height={20} fill={H.wood} /><rect x={-120} y={-150} width={16} height={150} fill={H.wood2} /><rect x={104} y={-150} width={16} height={150} fill={H.wood2} />
        <g transform="translate(20,-170)"><rect x={-90} y={-130} width={180} height={120} rx={10} fill={H.ink} /><rect x={-80} y={-120} width={160} height={100} rx={6} fill={H.navy} />
          {k === 0 ? <g><rect x={-70} y={-110} width={20} height={80} fill={H.plum3} /><circle cx={20} cy={-70} r={30} fill={H.gold} /><path d={`M${-10 + Math.sin(t * 3) * 30},-50 l40,-40`} stroke={H.cream} strokeWidth={6} strokeLinecap="round" /></g> : null}
          {k === 1 ? <g>{[0, 1, 2].map((r) => <rect key={r} x={-70 + r * 10} y={-100 + r * 26} width={110} height={18} rx={4} fill={[H.teal, H.terra, H.gold][r]} />)}<rect x={-70 + ((t * 60) % 140)} y={-110} width={4} height={86} fill={H.red} /></g> : null}
          {k === 2 ? <circle cx={-40 + ((t * 70) % 100)} cy={-40 - Math.abs(Math.sin(t * 5)) * 50} r={16} fill={H.red} /> : null}
          <rect x={-100} y={0} width={200} height={10} rx={4} fill={H.stone2} /></g>
        <Person x={-60} t={t + k} s={0.62} act={u > 0 ? 'type' : 'idle'} face={1} robe={[H.red, H.teal, H.gold][k]} robe2={H.plum3} seed={70 + k} />
      </g>
    );
  };
  return (
    <g>
      {desk(-420, 0)}{desk(0, 1)}{desk(420, 2)}
      {job > 0 ? <g transform={`translate(0,-700) scale(${pop(job)})`}><rect x={-90} y={-60} width={180} height={120} rx={18} fill={H.wood} /><rect x={-40} y={-90} width={80} height={40} rx={12} fill="none" stroke={H.wood2} strokeWidth={14} />
        <rect x={-90} y={-10} width={180} height={14} fill={H.wood2} /><circle cx={130} cy={-40} r={30} fill={H.gold} /><text x={130} y={-28} textAnchor="middle" fontWeight={900} fontSize={36} fill={H.plum}>$</text></g> : null}
    </g>
  );
};

export const STATIONS: Record<string, React.FC<{e: Ev}>> = {
  speech: Speech, village: Village, cave: Cave, sumer: Sumer, egypt: Egypt, pyramids: Pyramids, china: China, rome: Rome,
  paper: Paper, baghdad: Baghdad, press: Press, computer: Computer, now: Now, weak: Weak, future: Future,
};
