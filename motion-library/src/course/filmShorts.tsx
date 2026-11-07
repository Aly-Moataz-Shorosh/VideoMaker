import React from 'react';
import {Easing, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, G, Glass, lin, Pill, spr} from '../glass/kit';
import {bi} from './kit';
import {filmScenes2} from './filmShorts2';
import {filmScenes3} from './filmShorts3';

// Explaining scenes for the film-making course shorts (2026-11-06). Every scene draws what he says in that sentence
// (Aly: "ال icons مش بتبقى كافية" -> real explaining motion, real pictures of his own setups).
const GOLD = '#FFC21A', RED = '#E5232B', PINK = '#E05A9A', INK = '#14181F';

const Tag: React.FC<{text: string; x?: number; y: number; at: number; c?: string; size?: number; until?: number; maxW?: number}> = ({text, x, y, at, c = GOLD, size: s0 = 50, until, maxW = 920}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const size = Math.min(s0, Math.floor(maxW / (text.length * 0.6 + 1)));
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


// lines drawn ON a real picture to show where the camera is (Aly 2026-11-07: "اعمل خطوط.. لان مش باينة اوي")
// dir 'down' = camera above looking down (high angle), 'up' = camera under looking up (low angle)
const AngleLines: React.FC<{w: number; h: number; dir: string; at: number}> = ({w, h, dir, at}) => {
  const f = useCurrentFrame();
  const p = lin(f, at, at + 18), q = lin(f, at + 10, at + 24);
  const up = dir === 'up', cx = w / 2, cy = up ? h - 46 : 46, c = up ? RED : '#3BA9F5'; // camera glyph inside the picture (never on the caption under it)
  const L = 1400;
  return (
    <svg width={w} height={h + 120} style={{position: 'absolute', left: 0, top: -60, overflow: 'visible', pointerEvents: 'none'}}>
      <g transform="translate(0 60)">
        {[[0, up ? 0 : h], [w, up ? 0 : h], [w * 0.25, up ? 0 : h], [w * 0.75, up ? 0 : h]].map(([x, y], i) => (
          <line key={i} x1={cx} y1={cy} x2={x} y2={y} stroke={c} strokeWidth={i < 2 ? 6 : 3} strokeDasharray={`${L}`} strokeDashoffset={L * (1 - p)} opacity={i < 2 ? 0.95 : 0.6} style={{filter: `drop-shadow(0 0 8px ${c})`}} />
        ))}
        <g transform={`translate(${cx} ${cy}) scale(${0.6 + 0.4 * q}) rotate(${up ? -90 : 90})`} opacity={q}>
          <rect x={-46} y={-30} width={78} height={60} rx={12} fill={c} stroke="#fff" strokeWidth={4} />
          <path d="M 32 -16 L 62 -32 L 62 32 L 32 16 Z" fill={c} stroke="#fff" strokeWidth={4} />
        </g>
      </g>
    </svg>
  );
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
export const AngleScene: React.FC<{dur: number; modes?: [number, number][]; tags?: {t: number; text: string; c?: string}[]; cin?: boolean; cout?: boolean; pics?: {t: number; img: string; label: string; credit: string; dir?: string}[]}> = ({dur, modes = [[0, 0]], tags = [], cin = false, cout = false, pics = []}) => {
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
      {(() => { const pc = [...pics].reverse().find((q) => f >= q.t * fps); if (!pc) return null;
        const q = spr(f, fps, pc.t * fps, 150, 15);
        return (
          <div key={pc.t} style={{position: 'absolute', left: 230, top: 712, width: 620, opacity: Math.min(1, q * 1.5), transform: `translateX(${(1 - q) * 420}px) rotate(${-2 + (1 - q) * 6}deg)`}}>
            <div style={{padding: 12, borderRadius: 26, background: '#fff', boxShadow: '0 30px 70px rgba(0,0,0,0.6)'}}>
              <div style={{position: 'relative', width: 596, height: 335}}>
                <Img src={staticFile(pc.img)} style={{width: 596, height: 335, objectFit: 'cover', borderRadius: 16, display: 'block'}} />
                {pc.dir ? <AngleLines w={596} h={335} dir={pc.dir} at={Math.round(pc.t * fps) + 10} /> : null}
              </div>
              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 6px 2px', direction: 'rtl'}}>
                <span style={{fontFamily: AR, fontWeight: 900, fontSize: 34, color: INK}}>{bi(pc.label)}</span>
                <span style={{fontFamily: AR, fontWeight: 700, fontSize: 24, color: '#5A6270'}}>{bi(pc.credit)}</span>
              </div>
            </div>
          </div>);
      })()}
      {tagNow ? <Tag key={tagNow.t} text={tagNow.text} y={1150} at={Math.round(tagNow.t * fps)} c={tagNow.c ?? GOLD} size={46} /> : null}
    </div>
  );
};

// ---------- power in the frame: a podium of steps (McGonagall's side left, Umbridge's side right), eye line, power meter ----------
// steps: [(t, pinkStep, blackStep)] (0..4, 4 = top); under = the film clip plays under it. The right column (x > 790) stays free for
// his round webcam (Aly 2026-11-07: "حطني فوق"); the black figure has a white outline (Aly: "الاسود مش باين").
export const PowerStairs: React.FC<{dur: number; steps?: [number, number, number][]; tags?: {t: number; text: string; c?: string}[]; under?: boolean; cin?: boolean; cout?: boolean; outB?: number}> = ({dur, steps = [[0, 0, 0]], tags = [], under = true, cin = false, cout = false, outB}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pIn = cin ? 1 : spr(f, fps, 0, 140, 16), o = cout ? 1 : 1 - lin(f, dur - 8, dur);
  const gone = outB === undefined ? 0 : lin(f, outB * fps, outB * fps + 20); // the other one leaves the frame
  const P = kf(f, fps, steps.map((s) => [s[0], s[1]])), B = kf(f, fps, steps.map((s) => [s[0], s[2]]));
  const top = under ? 330 : 520, H = 520;
  const N = 4, SW = 70, SH = 46, L0 = 70, MID = 410, y0 = top + H - 80;
  const bx = (s: number) => L0 + s * SW + 36, px = (s: number) => 2 * MID - L0 - s * SW - 36, sy = (s: number) => y0 - s * SH;
  const b = {x: bx(B), y: sy(B)}, p = {x: px(P), y: sy(P)};
  const k = 0.85, head = (q: {y: number}) => q.y - 130 * k;
  const diff = P - B; // + = pink higher
  const powP = Math.min(0.95, Math.max(0.05, 0.5 + 0.14 * diff + 0.45 * gone)), powB = 1 - powP;
  const tagNow = [...tags].reverse().find((t) => f >= t.t * fps);
  const fig = (x: number, y: number, c: string, name: string) => (
    <g transform={`translate(${x} ${y}) scale(${k})`}>
      <circle cx={0} cy={-130} r={26} fill={c} stroke="#fff" strokeWidth={4} />
      <path d="M -34 -100 Q 0 -110 34 -100 L 46 0 L -46 0 Z" fill={c} stroke="#fff" strokeWidth={4} strokeLinejoin="round" />
      <rect x={-20} y={0} width={14} height={20} fill={c} stroke="#fff" strokeWidth={3} /><rect x={6} y={0} width={14} height={20} fill={c} stroke="#fff" strokeWidth={3} />
      <text x={0} y={54} textAnchor="middle" fill="#fff" fontFamily={EN} fontWeight={800} fontSize={26}>{name}</text>
    </g>
  );
  let d = `M ${L0} ${y0}`;
  for (let i = 0; i < N; i++) d += ` L ${L0 + i * SW} ${sy(i + 1)} L ${L0 + (i + 1) * SW} ${sy(i + 1)}`;
  d += ` L ${2 * MID - L0 - N * SW} ${sy(N)}`;
  for (let i = N - 1; i >= 0; i--) d += ` L ${2 * MID - L0 - i * SW} ${sy(i + 1)} L ${2 * MID - L0 - i * SW} ${sy(i)}`;
  const crown = Math.abs(diff) >= 0.15 || gone > 0.5 ? (diff > 0 || gone > 0.5 ? p : b) : null;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, opacity: Math.min(1, pIn * 1.4) * o}}>
      <div style={{position: 'absolute', left: 40, top: top - 10}}><Glass w={760} h={H + 20} pad={0} r={36} glow={GOLD}><div /></Glass></div>
      <div style={{position: 'absolute', left: 820, top: top + 230, width: 220}}><Glass w={220} h={H - 220} pad={0} r={30} glow={GOLD}><div /></Glass></div>
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <path d={d + ' Z'} fill="rgba(255,255,255,0.07)" stroke="rgba(255,255,255,0.6)" strokeWidth={6} strokeLinejoin="round" />
        <line opacity={1 - gone} x1={b.x} y1={head(b)} x2={p.x} y2={head(p)} stroke={Math.abs(diff) < 0.15 ? G.green : GOLD} strokeWidth={5} strokeDasharray="14 10" />
        <g opacity={1 - gone} transform={`translate(${-300 * gone} 0)`}>{fig(b.x, b.y, '#3A3A4C', 'McGonagall')}</g>
        {fig(p.x, p.y, PINK, 'Umbridge')}
        {crown ? <path transform={`translate(${crown.x} ${head(crown) - 40})`} d="M -26 0 L -30 -30 L -14 -16 L 0 -36 L 14 -16 L 30 -30 L 26 0 Z" fill={GOLD} stroke="#14181F" strokeWidth={2} /> : null}
      </svg>
      <div style={{position: 'absolute', left: 825, top: top + 250, width: 210, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8}}>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 30, color: '#fff'}}>السلطة</div>
        <div style={{display: 'flex', gap: 24, alignItems: 'flex-end', height: 170}}>
          <div style={{width: 56, height: 170 * powB, borderRadius: 14, background: '#3A3A4C', border: '3px solid #fff'}} />
          <div style={{width: 56, height: 170 * powP, borderRadius: 14, background: PINK, border: '3px solid #fff'}} />
        </div>
      </div>
      {tagNow ? <Tag key={tagNow.t} text={tagNow.text} x={60} y={top + 14} at={Math.round(tagNow.t * fps)} c={tagNow.c ?? GOLD} size={40} maxW={690} /> : null}
    </div>
  );
};

// ---------- his own setups climbing a staircase: "the tools are no excuse" ----------
export const ToolsLadder: React.FC<{dur: number; items: {img: string; text: string; at: number}[]; title?: string; titleAt?: number}> = ({dur, items, title, titleAt = 0}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const o = 1 - lin(f, dur - 8, dur);
  const n = items.length;
  const X = (i: number) => 60 + i * 175, Y = (i: number) => 1300 - i * 138; // card bottom-left corners
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


// ---------- two real shows side by side: where the camera is and what it makes you feel (Aly 2026-11-07: الدحيح vs أخ كبير) ----------
export const AngleVS: React.FC<{dur: number; cards: {img: string; name: string; credit: string; cam: string; feel: string; c: string; at: number; dir?: string}[]; title?: string; outro?: string; outroAt?: number}> = ({dur, cards, title, outro, outroAt = 2.4}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const o = 1 - lin(f, dur - 8, dur);
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, opacity: o}}>
      {title ? <Tag text={title} y={350} at={0} size={46} /> : null}
      {outro ? <Tag text={outro} y={1340} at={Math.round(outroAt * fps)} size={42} c={G.green} /> : null}
      {cards.map((c, i) => {
        const q = spr(f, fps, c.at * fps, 150, 15);
        if (f < c.at * fps) return null;
        const y = 450 + i * 430;
        return (
          <div key={i} style={{position: 'absolute', left: 50, top: y, width: 980, height: 390, display: 'flex', gap: 22, direction: 'rtl', alignItems: 'center',
            opacity: Math.min(1, q * 1.5), transform: `translateX(${(1 - q) * (i ? -300 : 300)}px)`}}>
            <div style={{position: 'relative', flexShrink: 0}}>
              <Img src={staticFile(c.img)} style={{width: 520, height: 292, objectFit: 'cover', borderRadius: 22, border: `5px solid ${c.c}`, boxShadow: `0 0 40px ${c.c}66`, display: 'block'}} />
              {c.dir ? <AngleLines w={520} h={292} dir={c.dir} at={Math.round(c.at * fps) + 8} /> : null}
              <div style={{position: 'absolute', right: 10, bottom: -18}}><Pill text={c.name} size={36} color={c.c} ink={c.c === GOLD ? INK : '#fff'} /></div>
            </div>
            <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 14}}>
              <div style={{fontFamily: AR, fontWeight: 900, fontSize: 38, color: '#fff', lineHeight: 1.3}}>{bi(c.cam)}</div>
              <div style={{fontFamily: AR, fontWeight: 800, fontSize: 32, color: c.c, lineHeight: 1.35}}>{bi(c.feel)}</div>
              <div style={{fontFamily: AR, fontWeight: 700, fontSize: 22, color: G.soft}}>{bi(c.credit)}</div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export const filmScenes: Record<string, React.FC<any>> = {AngleScene, PowerStairs, ToolsLadder, AngleVS, ...filmScenes2, ...filmScenes3};
