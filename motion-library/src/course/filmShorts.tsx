import React from 'react';
import {Easing, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, G, Glass, lin, Pill, spr} from '../glass/kit';
import {bi} from './kit';

// Explaining scenes for the film-making course shorts (2026-11-06). Every scene draws what he says in that sentence
// (Aly: "ال icons مش بتبقى كافية" -> real explaining motion, real pictures of his own setups).
const GOLD = '#FFC21A', RED = '#E5232B', PINK = '#E05A9A', INK = '#14181F';

const Tag: React.FC<{text: string; x?: number; y: number; at: number; c?: string; size?: number; until?: number}> = ({text, x, y, at, c = GOLD, size: s0 = 50, until}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const size = Math.min(s0, Math.floor(920 / (text.length * 0.6 + 1)));
  const p = spr(f, fps, at, 180, 13);
  const o = until === undefined ? 1 : 1 - lin(f, until - 6, until);
  if (f < at) return null;
  return (
    <div style={{position: 'absolute', left: x === undefined ? 0 : x, right: x === undefined ? 0 : undefined, top: y, display: 'flex', justifyContent: 'center',
      opacity: Math.min(1, p * 1.5) * o, transform: `scale(${0.6 + 0.4 * p})`}}>
      <div style={{padding: '10px 28px', borderRadius: 34, background: 'rgba(10,12,18,0.9)', border: `3px solid ${c}`, fontFamily: AR, fontWeight: 900, fontSize: size,
        color: '#fff', direction: 'rtl', whiteSpace: 'nowrap', boxShadow: `0 0 34px ${c}55`}}>{bi(text)}</div>
    </div>
  );
};

// keyframes [t (s), value...] -> eased value at frame f
const kf = (f: number, fps: number, keys: [number, number][]) => {
  if (!keys.length) return 0;
  let i = 0;
  while (i + 1 < keys.length && f >= keys[i + 1][0] * fps) i++;
  const a = keys[i], b = keys[Math.min(i + 1, keys.length - 1)];
  if (b === a) return a[1];
  return a[1] + (b[1] - a[1]) * lin(f, b[0] * fps - 14, b[0] * fps, 0, 1, Easing.inOut(Easing.cubic));
};

// ---------- camera angle: side view (camera goes up/down around the person) + what the camera SEES ----------
// modes: [(t, a)] a = -1 low angle (camera under, looking up) .. 0 eye level .. +1 high angle (camera over, looking down)
const Person: React.FC<{x: number; y: number; s: number; c?: string}> = ({x, y, s, c = '#E9EEF5'}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <circle cx={0} cy={-170} r={34} fill={c} />
    <path d="M -46 -126 Q 0 -140 46 -126 L 56 -10 L 26 -10 L 22 90 L -22 90 L -26 -10 L -56 -10 Z" fill={c} />
    <rect x={-24} y={90} width={18} height={70} rx={8} fill={c} />
    <rect x={6} y={90} width={18} height={70} rx={8} fill={c} />
  </g>
);
const Cam: React.FC<{x: number; y: number; rot: number; c: string}> = ({x, y, rot, c}) => (
  <g transform={`translate(${x} ${y}) rotate(${rot})`}>
    <rect x={-46} y={-30} width={78} height={60} rx={12} fill={c} />
    <path d="M 32 -16 L 62 -32 L 62 32 L 32 16 Z" fill={c} />
    <circle cx={-26} cy={-38} r={14} fill={c} /><circle cx={6} cy={-38} r={14} fill={c} />
  </g>
);
export const AngleScene: React.FC<{dur: number; modes?: [number, number][]; tags?: {t: number; text: string; c?: string}[]; cin?: boolean; cout?: boolean}> = ({dur, modes = [[0, 0]], tags = [], cin = false, cout = false}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = kf(f, fps, modes);
  const pIn = cin ? 1 : spr(f, fps, 0, 140, 16), o = cout ? 1 : 1 - lin(f, dur - 8, dur);
  // side view: person at (650, 760), camera on an arc to the left
  const ang = a * 50 * Math.PI / 180; // + = above
  const R = 260, hx = 640, hy = 530; // head height of the person in the side view
  const cx = hx - R * Math.cos(ang), cy = hy - R * Math.sin(ang);
  const rot = a * 50; // pointing at the head
  // preview: what the camera sees
  const up = Math.max(0, -a), down = Math.max(0, a);
  const tagNow = [...tags].reverse().find((t) => f >= t.t * fps);
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, opacity: Math.min(1, pIn * 1.4) * o}}>
      <div style={{position: 'absolute', left: 40, top: 340, transform: `translateY(${(1 - pIn) * 40}px)`}}>
        <Glass w={1000} h={900} pad={0} r={40} glow={GOLD}><div /></Glass>
      </div>
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <defs>
          <linearGradient id="cone" x1="0" x2="1"><stop offset="0" stopColor={GOLD} stopOpacity={0.55} /><stop offset="1" stopColor={GOLD} stopOpacity={0.05} /></linearGradient>
          <clipPath id="pv"><rect x={270} y={800} width={540} height={340} rx={26} /></clipPath>
        </defs>
        {/* side view: floor, arc, view cone, person, camera */}
        <line x1={120} y1={752} x2={960} y2={752} stroke="rgba(255,255,255,0.35)" strokeWidth={4} />
        <path d={`M ${hx - R * Math.cos(-1)} ${hy - R * Math.sin(-1)} A ${R} ${R} 0 0 1 ${hx - R * Math.cos(1)} ${hy - R * Math.sin(1)}`} fill="none" stroke="rgba(255,255,255,0.18)" strokeWidth={4} strokeDasharray="10 12" />
        <path d={`M ${cx} ${cy} L ${hx + 30} ${hy - 105} L ${hx + 30} ${hy + 130} Z`} fill="url(#cone)" />
        <line x1={cx} y1={cy} x2={hx} y2={hy} stroke={GOLD} strokeWidth={4} strokeDasharray="14 10" />
        <Person x={hx} y={hy + 119} s={0.7} />
        <Cam x={cx} y={cy} rot={rot} c={GOLD} />
        {/* preview frame: perspective of the person seen from the camera */}
        <g clipPath="url(#pv)">
          <rect x={270} y={800} width={540} height={340} fill={down > up ? '#2A2F3A' : '#1B2A44'} />
          {/* floor seen from above (high angle) / sky + ceiling seen from below (low angle) */}
          {Array.from({length: 9}).map((_, i) => <line key={i} x1={270} y1={1140 - i * 32 * (0.4 + down)} x2={810} y2={1140 - i * 32 * (0.4 + down)} stroke="rgba(255,255,255,0.10)" strokeWidth={3} opacity={down} />)}
          {Array.from({length: 7}).map((_, i) => <rect key={i} x={280 + i * 80} y={808} width={50} height={80 + 110 * up} fill="rgba(255,255,255,0.08)" opacity={up} />)}
          <g transform={`translate(540 ${1010 + 50 * down - 40 * up}) scale(${0.72 * (1 + 0.05 * up - 0.38 * down)} ${0.72 * (1 + 0.55 * up - 0.42 * down)})`}>
            {/* foreshortening: head big & body short from above, legs long & head small from below */}
            <circle cx={0} cy={-170 + 40 * down} r={34 * (1 + 0.6 * down - 0.35 * up)} fill="#E9EEF5" />
            <path d="M -46 -126 Q 0 -140 46 -126 L 56 -10 L 26 -10 L 22 90 L -22 90 L -26 -10 L -56 -10 Z" fill="#E9EEF5" />
            <rect x={-24} y={90} width={18} height={70 * (1 + 0.6 * up)} rx={8} fill="#E9EEF5" />
            <rect x={6} y={90} width={18} height={70 * (1 + 0.6 * up)} rx={8} fill="#E9EEF5" />
          </g>
        </g>
        <rect x={270} y={800} width={540} height={340} rx={26} fill="none" stroke={GOLD} strokeWidth={5} />
        <circle cx={306} cy={834} r={10} fill={RED} opacity={Math.floor(f / 15) % 2 ? 1 : 0.3} />
        <text x={326} y={844} fill="#fff" fontFamily={EN} fontWeight={800} fontSize={30}>REC</text>
      </svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 380, display: 'flex', justifyContent: 'center'}}>
        <Pill text={a > 0.5 ? 'High angle · الكاميرا فوق' : a < -0.5 ? 'Low angle · الكاميرا تحت' : 'Eye level · في مستوى العين'} size={40} color={a > 0.5 ? G.blue : a < -0.5 ? RED : GOLD} ink={a > 0.5 || a < -0.5 ? '#fff' : INK} />
      </div>
      <div style={{position: 'absolute', left: 270, top: 764, fontFamily: AR, fontWeight: 800, fontSize: 26, color: G.soft, direction: 'rtl', width: 540, textAlign: 'right'}}>الكاميرا شايفة كده:</div>
      {tagNow ? <Tag key={tagNow.t} text={tagNow.text} y={1160} at={Math.round(tagNow.t * fps)} c={tagNow.c ?? GOLD} size={46} /> : null}
    </div>
  );
};

// ---------- power in the frame: two people on a staircase, a power meter, eye line between them ----------
// steps: [(t, pinkStep, blackStep)] (0..5); under = the film clip plays under it (top half only)
export const PowerStairs: React.FC<{dur: number; steps?: [number, number, number][]; tags?: {t: number; text: string; c?: string}[]; under?: boolean; cin?: boolean; cout?: boolean; outB?: number}> = ({dur, steps = [[0, 0, 0]], tags = [], under = true, cin = false, cout = false, outB}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pIn = cin ? 1 : spr(f, fps, 0, 140, 16), o = cout ? 1 : 1 - lin(f, dur - 8, dur);
  const gone = outB === undefined ? 0 : lin(f, outB * fps, outB * fps + 20); // the other one leaves the frame
  const P = kf(f, fps, steps.map((s) => [s[0], s[1]])), B = kf(f, fps, steps.map((s) => [s[0], s[2]]));
  const top = under ? 330 : 520, H = 520;
  const N = 6, SW = 92, SH = 40, x0 = 150, y0 = top + H - 95; // staircase going up to the right
  const stepXY = (s: number, side: number) => ({x: x0 + s * SW + 40 + side * 26, y: y0 - s * SH});
  const p = stepXY(P, 1), b = stepXY(B, -1);
  const hp = p.y - 150, hb = b.y - 150; // head heights
  const diff = P - B; // + = pink higher
  const powP = Math.min(0.95, 0.5 + 0.12 * diff + 0.4 * gone), powB = 1 - powP;
  const tagNow = [...tags].reverse().find((t) => f >= t.t * fps);
  const fig = (x: number, y: number, c: string, name: string) => (
    <g transform={`translate(${x} ${y})`}>
      <circle cx={0} cy={-130} r={26} fill={c} />
      <path d="M -34 -100 Q 0 -110 34 -100 L 46 0 L -46 0 Z" fill={c} />
      <rect x={-20} y={0} width={14} height={20} fill={c} /><rect x={6} y={0} width={14} height={20} fill={c} />
      <text x={0} y={46} textAnchor="middle" fill="#fff" fontFamily={EN} fontWeight={800} fontSize={24}>{name}</text>
    </g>
  );
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, opacity: Math.min(1, pIn * 1.4) * o}}>
      <div style={{position: 'absolute', left: 40, top: top - 10}}><Glass w={1000} h={H + 20} pad={0} r={36} glow={GOLD}><div /></Glass></div>
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        {Array.from({length: N}).map((_, i) => (
          <path key={i} d={`M ${x0 + i * SW} ${y0 - i * SH + 20} L ${x0 + i * SW} ${y0 - (i + 1) * SH + 20} L ${x0 + (i + 1) * SW} ${y0 - (i + 1) * SH + 20}`} fill="none" stroke="rgba(255,255,255,0.55)" strokeWidth={6} strokeLinejoin="round" />
        ))}
        <line x1={x0} y1={y0 + 20} x2={x0 + N * SW + 40} y2={y0 + 20} stroke="rgba(255,255,255,0.3)" strokeWidth={4} />
        {/* eye line: level = equal power */}
        <line opacity={1 - gone} x1={b.x} y1={hb - 130 + 150} x2={p.x} y2={hp - 130 + 150} stroke={Math.abs(diff) < 0.15 ? G.green : GOLD} strokeWidth={4} strokeDasharray="12 10" />
        <g opacity={1 - gone} transform={`translate(${-260 * gone} 0)`}>{fig(b.x, b.y + 20, '#2B2B33', 'McGonagall')}</g>
        {fig(p.x, p.y + 20, PINK, 'Umbridge')}
        {/* crown on the higher one */}
        {Math.abs(diff) >= 0.15 || gone > 0.5 ? (() => { const w = diff > 0 || gone > 0.5 ? p : b; return <path transform={`translate(${w.x} ${w.y - 150}) scale(1.1)`} d="M -26 0 L -30 -30 L -14 -16 L 0 -36 L 14 -16 L 30 -30 L 26 0 Z" fill={GOLD} />; })() : null}
      </svg>
      {/* power meter */}
      <div style={{position: 'absolute', left: 820, top: top + 110, width: 180, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10}}>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 32, color: '#fff'}}>السلطة</div>
        <div style={{display: 'flex', gap: 22, alignItems: 'flex-end', height: 280}}>
          <div style={{width: 54, height: 280 * powB, borderRadius: 14, background: '#5B5B66', border: '3px solid #fff'}} />
          <div style={{width: 54, height: 280 * powP, borderRadius: 14, background: PINK, border: '3px solid #fff'}} />
        </div>
      </div>
      {tagNow ? <Tag key={tagNow.t} text={tagNow.text} x={60} y={top + 18} at={Math.round(tagNow.t * fps)} c={tagNow.c ?? GOLD} size={40} /> : null}
    </div>
  );
};

// ---------- his own setups climbing a staircase: "the tools are no excuse" ----------
export const ToolsLadder: React.FC<{dur: number; items: {img: string; text: string; at: number}[]; title?: string; titleAt?: number}> = ({dur, items, title, titleAt = 0}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const o = 1 - lin(f, dur - 8, dur);
  const n = items.length;
  const X = (i: number) => 60 + i * 175, Y = (i: number) => 1290 - i * 150; // card bottom-left corners
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, opacity: o}}>
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <path d={Array.from({length: n}).map((_, i) => `${i ? 'L' : 'M'} ${X(i)} ${Y(i)} L ${X(i) + 175} ${Y(i)}`).join(' ')} fill="none"
          stroke={GOLD} strokeWidth={8} strokeLinejoin="round" strokeDasharray={3000} strokeDashoffset={3000 * (1 - lin(f, 0, 24))} />
      </svg>
      {items.map((it, i) => {
        const p = spr(f, fps, it.at * fps, 160, 14);
        if (f < it.at * fps) return null;
        const x = X(i), y = Y(i) - 245;
        return (
          <div key={i} style={{position: 'absolute', left: x, top: y, width: 260, opacity: Math.min(1, p * 1.5), transform: `translateY(${(1 - p) * 60}px) scale(${0.8 + 0.2 * p})`}}>
            <Img src={staticFile(it.img)} style={{width: 260, height: 195, objectFit: 'cover', borderRadius: 18, border: `4px solid ${i === n - 1 ? GOLD : '#fff'}`, boxShadow: '0 20px 40px rgba(0,0,0,0.5)'}} />
            <div style={{marginTop: 8, textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 28, color: '#fff', direction: 'rtl', textShadow: '0 3px 10px #000'}}>{bi(it.text)}</div>
          </div>
        );
      })}
      {title ? <Tag text={title} y={350} at={Math.round(titleAt * fps)} size={58} /> : null}
    </div>
  );
};

export const filmScenes: Record<string, React.FC<any>> = {AngleScene, PowerStairs, ToolsLadder};
