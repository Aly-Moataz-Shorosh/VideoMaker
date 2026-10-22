import React from 'react';
import {AbsoluteFill, Easing, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {lin, rnd, spr} from '../film/kit';

// "رحلة إلى مركز الجرافيكس" shorts series (2026-10-22). One look per section of his project, taken from his own videos:
//  huwa = "هو ايه" (light grey vignette, flat corporate characters, magenta→orange "هو ايه!" logo, gradient frame on examples)
//  oz   = "المجالات و ساحر مدينة أوز" (yellow brick road, emerald city, the four characters DRAWN — never film footage)
//  prog = "البرامج" (dark teal, the program tree, yellow scroll badge, real program logos)
export type Sec = 'huwa' | 'oz' | 'prog';
export const JY = {
  huwa: {bg0: '#C9C9CB', bg1: '#8E8E92', ink: '#1E1E24', soft: '#4A4A55', a: '#E8175D', b: '#F7931E', card: '#FFFFFF'},
  oz: {bg0: '#FFE9B0', bg1: '#F2B24A', ink: '#2B1D14', soft: '#6B4A2E', a: '#1FA463', b: '#F2C230', card: '#FFF6DF', red: '#C8102E', sky: '#8FD3F4'},
  prog: {bg0: '#356A6B', bg1: '#1E4243', ink: '#FFFFFF', soft: '#CFE3E1', a: '#F7C531', b: '#F08A24', card: '#2A5556'},
};
export const AR = 'Cairo', EN = 'Montserrat';
export {lin, rnd, spr};
export const grad = (s: Sec) => `linear-gradient(120deg, ${JY[s].a}, ${JY[s].b})`;

// ---------- backgrounds (Aly 2026-10-22: "مريحة اكتر للعين" -> soft flat gradients, no grain, no busy lines) ----------
export const JourneyBg: React.FC<{sec: Sec}> = ({sec}) => {
  if (sec === 'oz') return <AbsoluteFill style={{background: 'linear-gradient(180deg, #DDEFF5 0%, #F4F1E4 55%, #F1E6C8 100%)'}} />;
  if (sec === 'prog') return <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, #33605F 0%, #2C5455 70%, #284D4E 100%)'}} />;
  return <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, #EEEEF1 0%, #E3E3E7 65%, #D8D8DD 100%)'}} />;
};

// ---------- section logos: HIS files (Aly 2026-10-22: "استخدم اللوجو نفسه.. نفس اللوجوهات بالظبط"), copied from F:\..\Aly Shorosh NEW ----------
export const LOGOS = 'projects/2026-10-22 shorts Journey to the center of computer graphics/logos/';
export const logo = (n: string) => staticFile(LOGOS + n);
// هو ايه logo = his "هو ايه2.png" (356 x 334) -> never shown bigger than that (no pixelation)
export const HuwaLogo: React.FC<{h?: number}> = ({h = 120}) => <Img src={logo('huwa.png')} style={{height: Math.min(h, 334), display: 'block'}} />;
export const OzBadge: React.FC<{d?: number}> = ({d = 120}) => <Img src={logo('oz.png')} style={{width: d, height: d, display: 'block'}} />;
export const ProgBadge: React.FC<{d?: number}> = ({d = 120}) => <Img src={logo('prog.png')} style={{height: d, display: 'block'}} />;

// channel logo + name at the very bottom of every short (Aly 2026-10-22), his "pp 2" artwork split into face + name
export const ChannelFooter: React.FC<{dark?: boolean}> = ({dark}) => (
  <div style={{position: 'absolute', left: 0, right: 0, bottom: 26, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 16, direction: 'ltr'}}>
    <Img src={logo('ch_face.png')} style={{height: 84}} />
    <Img src={logo('ch_name.png')} style={{height: 44}} />
  </div>
);

const STATIONS: {sec: Sec; name: string}[] = [{sec: 'huwa', name: 'هو ايه'}, {sec: 'oz', name: 'المجالات'}, {sec: 'prog', name: 'البرامج'}];

// ---------- series bar (top of every short): project name + the journey route with 3 stations ----------
// A walker dot runs along the road to this short's station in the first second; the station glows; label pill under it.
export const SeriesBar: React.FC<{sec: Sec; label: string}> = ({sec, label}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const dark = sec === 'prog';
  const ink = dark ? '#FFFFFF' : JY[sec].ink;
  const idx = STATIONS.findIndex((s) => s.sec === sec);
  const X = [870, 540, 210]; // RTL: first station on the right
  const Y = 118;
  const p = lin(f, 6, 34);
  const walkX = X[0] + (X[idx] - X[0]) * p;
  const inA = spr(f, fps, 0, 140, 16);
  const road = `M ${X[0]} ${Y} C 760 ${Y - 40}, 640 ${Y + 40}, ${X[1]} ${Y} S 320 ${Y - 40}, ${X[2]} ${Y}`;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 300, transform: `translateY(${(1 - inA) * -80}px)`, opacity: inA}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 300,
        background: dark ? 'linear-gradient(180deg, rgba(10,30,31,0.9) 55%, rgba(10,30,31,0))' : sec === 'oz' ? 'linear-gradient(180deg, rgba(255,250,235,0.85) 55%, rgba(255,250,235,0))' : 'linear-gradient(180deg, rgba(255,255,255,0.8) 55%, rgba(255,255,255,0))'}} />
      <div style={{position: 'absolute', top: 14, width: '100%', textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 40, color: ink, direction: 'rtl'}}>رحلة إلى مركز الجرافيكس</div>
      <svg width={1080} height={300} style={{position: 'absolute', top: 0}}>
        <path d={road} fill="none" stroke={sec === 'oz' ? '#C99A1E' : dark ? '#7FB3B1' : '#77777F'} strokeWidth={12} strokeLinecap="round" strokeDasharray="2 18" />
        <path d={road} fill="none" stroke={JY[sec].b} strokeWidth={9} strokeLinecap="round" pathLength={1} strokeDasharray={`${(idx / 2) * p} 1`} />
      </svg>
      {STATIONS.map((s, i) => {
        const on = i === idx;
        const done = i < idx;
        const pop = on ? spr(f, fps, 28, 200, 10) : 1;
        const d = on ? 96 : 70;
        return (
          <div key={s.sec} style={{position: 'absolute', left: X[i] - d / 2, top: Y - d / 2, width: d, height: d, transform: `scale(${on ? 0.7 + 0.3 * pop : 1})`,
            opacity: on || done ? 1 : 0.8, filter: on ? `drop-shadow(0 0 ${12 + 6 * Math.sin(f / 6)}px ${JY[sec].b})` : undefined}}>
            <div style={{width: d, height: d, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
              {s.sec === 'huwa' ? <HuwaLogo h={d * 0.95} /> : s.sec === 'oz' ? <OzBadge d={d} /> : <ProgBadge d={d * 0.72} />}
            </div>
            {on ? null : <div style={{position: 'absolute', top: d + 2, left: -70, right: -70, textAlign: 'center', fontFamily: AR, fontWeight: 800, fontSize: 24, color: ink, opacity: 0.75}}>{s.name}</div>}
          </div>
        );
      })}
      <div style={{position: 'absolute', left: walkX - 12, top: Y - 12, width: 24, height: 24, borderRadius: '50%', background: JY[sec].b, border: '4px solid #fff', opacity: p < 1 ? 1 : 0}} />
      <div style={{position: 'absolute', left: 30, right: 30, top: Y + 56, display: 'flex', direction: 'ltr', justifyContent: idx === 2 ? 'flex-start' : idx === 0 ? 'flex-end' : 'center', // never outside the frame, under its own station
        transformOrigin: idx === 2 ? '0% 50%' : idx === 0 ? '100% 50%' : '50% 50%', opacity: lin(f, 30, 40), transform: `scale(${0.8 + 0.2 * lin(f, 30, 40)})`}}>
        <span style={{fontFamily: AR, fontWeight: 900, fontSize: 32, color: dark ? JY.prog.bg1 : '#fff', background: grad(sec), padding: '4px 22px', borderRadius: 30,
          whiteSpace: 'nowrap', boxShadow: '0 6px 14px rgba(0,0,0,0.2)', direction: 'rtl'}}>{label.startsWith('=') ? label.slice(1) : `${STATIONS[idx].name} · ${label}`}</span>
      </div>
    </div>
  );
};

// ---------- small building blocks ----------
// Pop-in wrapper (absolute, centred on x,y). at/out in scene frames.
export const In: React.FC<{at?: number; out?: number; x: number; y: number; rot?: number; from?: number; children: React.ReactNode; slide?: number; z?: number}> = ({at = 0, out, x, y, rot = 0, from = 0.4, children, slide = 0, z}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (f < at) return null;
  const p = spr(f, fps, at, 190, 14);
  const o = out === undefined ? 1 : 1 - lin(f, out, out + 8, 0, 1, Easing.in(Easing.cubic));
  if (o <= 0) return null;
  const s = (from + (1 - from) * p) * (0.7 + 0.3 * o);
  return (
    <div style={{position: 'absolute', left: x, top: y, zIndex: z, opacity: Math.min(1, p * 1.5) * o,
      transform: `translate(-50%,-50%) translateY(${(1 - p) * slide}px) rotate(${rot * (1.5 - 0.5 * p)}deg) scale(${s})`}}>
      {children}
    </div>
  );
};

// Arabic text that types in letter by letter (a word at a time for Latin)
export const Type: React.FC<{text: string; at?: number; cps?: number; size?: number; color?: string; weight?: number; font?: string; dir?: 'rtl' | 'ltr'; style?: React.CSSProperties}> = ({text, at = 0, cps = 30, size = 60, color, weight = 900, font = AR, dir = 'rtl', style}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = Math.max(0, Math.floor(((f - at) / fps) * cps));
  if (f < at) return null;
  const words = text.split(' ');
  let left = n, shown = '';
  for (const w of words) { // whole words only (Arabic letters joined)
    if (left <= 0) break;
    shown += (shown ? ' ' : '') + w; left -= w.length + 1;
  }
  return <div style={{fontFamily: font, fontWeight: weight, fontSize: size, color, direction: dir, lineHeight: 1.25, whiteSpace: 'pre-wrap', ...style}}>{shown}</div>;
};

// Rounded pill label
export const Pill: React.FC<{text: string; bg?: string; ink?: string; size?: number; font?: string; dir?: 'rtl' | 'ltr'; border?: string}> = ({text, bg = '#fff', ink = '#1E1E24', size = 44, font = AR, dir = 'rtl', border}) => (
  <div style={{background: bg, color: ink, fontFamily: font, fontWeight: 900, fontSize: size, padding: `${size * 0.18}px ${size * 0.6}px`, borderRadius: size,
    whiteSpace: 'nowrap', direction: dir, boxShadow: '0 10px 24px rgba(0,0,0,0.18)', border}}>{text}</div>
);

// His "هو ايه" gradient frame around an example (magenta → orange), white inside
export const GFrame: React.FC<{w: number; h: number; children?: React.ReactNode; sec?: Sec; pad?: number; bg?: string}> = ({w, h, children, sec = 'huwa', pad = 10, bg = '#fff'}) => (
  <div style={{width: w, height: h, padding: pad, background: grad(sec), borderRadius: 26, boxShadow: '0 24px 50px rgba(0,0,0,0.25)'}}>
    <div style={{width: '100%', height: '100%', background: bg, borderRadius: 18, overflow: 'hidden', position: 'relative'}}>{children}</div>
  </div>
);

// Program / brand logo tile (real logo file in public/logos)
export const Logo: React.FC<{src: string; w?: number; h?: number; name?: string; dark?: boolean; tile?: boolean}> = ({src, w = 200, h = 200, name, dark, tile = true}) => (
  <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12}}>
    <div style={{width: w, height: h, borderRadius: 34, background: tile ? '#FFFFFF' : 'transparent', display: 'flex', alignItems: 'center', justifyContent: 'center',
      boxShadow: tile ? '0 16px 34px rgba(0,0,0,0.28)' : undefined}}>
      <Img src={logo(src)} style={{maxWidth: w * 0.78, maxHeight: h * 0.78, objectFit: 'contain'}} />
    </div>
    {name ? <div style={{fontFamily: EN, fontWeight: 800, fontSize: 34, color: dark ? '#fff' : '#1E1E24', whiteSpace: 'nowrap'}}>{name}</div> : null}
  </div>
);

// ---------- flat corporate character ("هو ايه" style): suit, tie, simple face; talk = mouth opens, point = right arm up ----------
export const FlatGuy: React.FC<{x: number; y: number; s?: number; suit?: string; shirt?: string; tie?: string; skin?: string; hair?: string;
  pose?: 'stand' | 'point' | 'think' | 'cheer'; talk?: boolean; look?: number; beard?: boolean; flip?: boolean}> = ({x, y, s = 1, suit = '#2C2C34', shirt = '#FFFFFF', tie = '#E8175D', skin = '#E9B98F', hair = '#2A1E17', pose = 'stand', talk = false, look = 0, beard = false, flip = false}) => {
  const f = useCurrentFrame();
  const blink = f % 96 < 4;
  const mouth = talk ? 3 + 5 * Math.abs(Math.sin(f / 2.6)) : 2;
  const bob = Math.sin(f / 18) * 2;
  const armR = pose === 'point' ? -150 : pose === 'cheer' ? -160 : pose === 'think' ? -120 : 6;
  const armL = pose === 'cheer' ? 160 : -6;
  return (
    <svg x={0} y={0} width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
      <g transform={`translate(${x} ${y + bob}) scale(${flip ? -s : s} ${s})`}>
        {/* legs */}
        <rect x={-30} y={60} width={26} height={150} rx={10} fill={suit} />
        <rect x={4} y={60} width={26} height={150} rx={10} fill={suit} />
        <ellipse cx={-20} cy={212} rx={24} ry={10} fill="#141418" />
        <ellipse cx={20} cy={212} rx={24} ry={10} fill="#141418" />
        {/* arms */}
        <g transform={`rotate(${armL} -52 -60)`}><rect x={-66} y={-66} width={26} height={130} rx={12} fill={suit} /><circle cx={-53} cy={70} r={13} fill={skin} /></g>
        <g transform={`rotate(${armR} 52 -60)`}><rect x={40} y={-66} width={26} height={130} rx={12} fill={suit} /><circle cx={53} cy={70} r={13} fill={skin} /></g>
        {/* body */}
        <path d="M -56 -70 Q 0 -88 56 -70 L 50 70 L -50 70 Z" fill={suit} />
        <path d="M -18 -78 L 0 -30 L 18 -78 Z" fill={shirt} />
        <path d="M -6 -64 L 6 -64 L 9 -10 L 0 4 L -9 -10 Z" fill={tie} />
        {/* head */}
        <rect x={-12} y={-100} width={24} height={26} fill={skin} />
        <ellipse cx={0} cy={-140} rx={42} ry={48} fill={skin} />
        <path d="M -44 -146 Q -40 -196 0 -192 Q 44 -196 44 -146 Q 30 -170 -2 -168 Q -30 -168 -44 -146 Z" fill={hair} />
        {beard ? <path d="M -40 -134 Q -36 -86 0 -88 Q 36 -86 40 -134 Q 30 -104 0 -106 Q -30 -104 -40 -134 Z" fill={hair} /> : null}
        <ellipse cx={-15 + look * 6} cy={-142} rx={5} ry={blink ? 1 : 6} fill="#1A1A1A" />
        <ellipse cx={15 + look * 6} cy={-142} rx={5} ry={blink ? 1 : 6} fill="#1A1A1A" />
        <path d="M -24 -158 L -8 -156 M 8 -156 L 24 -158" stroke={hair} strokeWidth={4} strokeLinecap="round" />
        <ellipse cx={look * 4} cy={-114} rx={10} ry={mouth} fill="#7A2E2E" />
      </g>
    </svg>
  );
};

// ---------- Oz cast (flat vector, drawn — never film footage) ----------
const OUT = 'drop-shadow(3px 0 0 #2B1D14) drop-shadow(-3px 0 0 #2B1D14) drop-shadow(0 3px 0 #2B1D14) drop-shadow(0 -3px 0 #2B1D14) drop-shadow(0 14px 10px rgba(0,0,0,0.25))';
export const Dorothy: React.FC<{x: number; y: number; s?: number; walk?: boolean; talk?: boolean; flip?: boolean; look?: number}> = ({x, y, s = 1, walk = false, talk = false, flip = false, look = 0}) => {
  const f = useCurrentFrame();
  const w = walk ? Math.sin(f / 4) : 0;
  const bob = walk ? Math.abs(Math.sin(f / 4)) * -6 : Math.sin(f / 20) * 2;
  const blink = f % 110 < 4;
  const mouth = talk ? 2 + 4 * Math.abs(Math.sin(f / 2.5)) : 1.5;
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', filter: OUT}}>
      <ellipse cx={x} cy={y + 182 * s} rx={70 * s} ry={14 * s} fill="rgba(0,0,0,0.18)" />
      <g transform={`translate(${x} ${y + bob}) scale(${flip ? -s : s} ${s})`}>
        {/* legs + ruby slippers */}
        <g transform={`rotate(${w * 18} -12 60)`}><rect x={-20} y={60} width={16} height={110} rx={7} fill="#F3D2B5" /><ellipse cx={-10} cy={172} rx={20} ry={10} fill="#C8102E" /><circle cx={-4} cy={168} r={3} fill="#FFB3C0" /></g>
        <g transform={`rotate(${-w * 18} 12 60)`}><rect x={4} y={60} width={16} height={110} rx={7} fill="#F3D2B5" /><ellipse cx={14} cy={172} rx={20} ry={10} fill="#C8102E" /><circle cx={20} cy={168} r={3} fill="#FFB3C0" /></g>
        {/* gingham dress */}
        <defs>
          <pattern id="ging" width="14" height="14" patternUnits="userSpaceOnUse">
            <rect width="14" height="14" fill="#9CC3EA" /><rect width="7" height="14" fill="#5E95D1" opacity={0.6} /><rect width="14" height="7" fill="#5E95D1" opacity={0.6} />
          </pattern>
        </defs>
        <path d="M -40 -40 L 40 -40 L 64 76 L -64 76 Z" fill="url(#ging)" />
        <rect x={-38} y={-76} width={76} height={42} rx={14} fill="#FFFFFF" />
        <rect x={-30} y={-72} width={60} height={60} rx={8} fill="url(#ging)" />
        {/* arms */}
        <g transform={`rotate(${-w * 22 + 10} -40 -60)`}><rect x={-52} y={-66} width={16} height={84} rx={8} fill="#F3D2B5" /></g>
        <g transform={`rotate(${w * 22 - 10} 40 -60)`}><rect x={36} y={-66} width={16} height={84} rx={8} fill="#F3D2B5" /></g>
        {/* basket */}
        <g transform={`translate(-58 ${14 + w * 4})`}><path d="M -18 0 L 18 0 L 13 22 L -13 22 Z" fill="#B5823C" /><path d="M -14 0 Q 0 -24 14 0" stroke="#8A5E26" strokeWidth={4} fill="none" /></g>
        {/* head + braids + ribbons */}
        <path d="M -38 -124 Q -56 -80 -46 -50" stroke="#6B3A1E" strokeWidth={12} fill="none" strokeLinecap="round" />
        <path d="M 38 -124 Q 56 -80 46 -50" stroke="#6B3A1E" strokeWidth={12} fill="none" strokeLinecap="round" />
        <circle cx={-48} cy={-92} r={7} fill="#5E95D1" /><circle cx={48} cy={-92} r={7} fill="#5E95D1" />
        <ellipse cx={0} cy={-122} rx={36} ry={40} fill="#F6D7BC" />
        <path d="M -38 -128 Q -36 -170 0 -166 Q 36 -170 38 -128 Q 22 -148 0 -148 Q -22 -148 -38 -128 Z" fill="#6B3A1E" />
        <ellipse cx={-13 + look * 5} cy={-122} rx={4.5} ry={blink ? 1 : 5.5} fill="#2A1A10" />
        <ellipse cx={13 + look * 5} cy={-122} rx={4.5} ry={blink ? 1 : 5.5} fill="#2A1A10" />
        <circle cx={-22} cy={-106} r={6} fill="#F2A5A5" opacity={0.6} /><circle cx={22} cy={-106} r={6} fill="#F2A5A5" opacity={0.6} />
        <ellipse cx={look * 3} cy={-100} rx={7} ry={mouth} fill="#9B3B3B" />
      </g>
    </svg>
  );
};

export const Scarecrow: React.FC<{x: number; y: number; s?: number; onPole?: boolean; walk?: boolean; talk?: boolean; flip?: boolean; look?: number; sad?: boolean}> = ({x, y, s = 1, onPole = false, walk = false, talk = false, flip = false, look = 0, sad = false}) => {
  const f = useCurrentFrame();
  const w = walk ? Math.sin(f / 4) : 0;
  const sway = onPole ? Math.sin(f / 14) * 3 : 0;
  const bob = walk ? Math.abs(Math.sin(f / 4)) * -6 : 0;
  const blink = f % 130 < 4;
  const mouth = talk ? 2 + 5 * Math.abs(Math.sin(f / 2.4)) : 2;
  const straw = (cx: number, cy: number, a: number, n = 5) => Array.from({length: n}, (_, i) => (
    <line key={i} x1={cx} y1={cy} x2={cx + Math.cos(a + (i - n / 2) * 0.22) * 22} y2={cy + Math.sin(a + (i - n / 2) * 0.22) * 22} stroke="#E8C25A" strokeWidth={3} strokeLinecap="round" />
  ));
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', filter: OUT}}>
      {!onPole ? <ellipse cx={x} cy={y + 178 * s} rx={70 * s} ry={14 * s} fill="rgba(0,0,0,0.18)" /> : null}
      <g transform={`translate(${x} ${y + bob}) rotate(${sway}) scale(${flip ? -s : s} ${s})`}>
        {onPole ? <><rect x={-8} y={-60} width={16} height={260} fill="#7A5230" /><rect x={-110} y={-62} width={220} height={14} fill="#7A5230" /></> : null}
        {/* legs */}
        <g transform={`rotate(${w * 18} -14 60)`}><rect x={-26} y={56} width={22} height={110} rx={6} fill="#5B6B3A" />{straw(-15, 166, Math.PI / 2)}</g>
        <g transform={`rotate(${-w * 18} 14 60)`}><rect x={4} y={56} width={22} height={110} rx={6} fill="#5B6B3A" />{straw(15, 166, Math.PI / 2)}</g>
        {/* arms: straight out on the pole */}
        <g transform={`rotate(${onPole ? -84 : -w * 22 + 8} -42 -58)`}><rect x={-54} y={-64} width={20} height={92} rx={6} fill="#8A6B3E" />{straw(-44, 30, Math.PI / 2)}</g>
        <g transform={`rotate(${onPole ? 84 : w * 22 - 8} 42 -58)`}><rect x={34} y={-64} width={20} height={92} rx={6} fill="#8A6B3E" />{straw(44, 30, Math.PI / 2)}</g>
        {/* patched coat */}
        <path d="M -46 -72 L 46 -72 L 40 64 L -40 64 Z" fill="#8A6B3E" />
        <rect x={-30} y={-30} width={22} height={20} fill="#C26A3A" transform="rotate(-8 -19 -20)" />
        <rect x={10} y={10} width={20} height={18} fill="#5E95D1" transform="rotate(10 20 19)" />
        <rect x={-46} y={40} width={92} height={10} fill="#5B4024" />
        {/* head: burlap sack + hat */}
        <ellipse cx={0} cy={-120} rx={40} ry={44} fill="#E4C99A" />
        {straw(-34, -96, Math.PI * 0.85, 4)}{straw(34, -96, Math.PI * 0.15, 4)}
        <path d="M -70 -150 L 70 -150 L 52 -140 L -52 -140 Z" fill="#6E5A2E" />
        <path d="M -36 -150 Q -30 -206 0 -204 Q 30 -206 36 -150 Z" fill="#7E6A36" />
        <rect x={-36} y={-162} width={72} height={10} fill="#4F3F1E" />
        <circle cx={-14 + look * 5} cy={-122} r={blink ? 1 : 6} fill="#1A1A1A" />
        <circle cx={14 + look * 5} cy={-122} r={blink ? 1 : 6} fill="#1A1A1A" />
        <path d={sad ? 'M -16 -94 Q 0 -104 16 -94' : 'M -18 -100 Q 0 -86 18 -100'} stroke="#3A2A1A" strokeWidth={4} fill="none" strokeLinecap="round" />
        {talk ? <ellipse cx={0} cy={-96} rx={8} ry={mouth} fill="#5A2A1A" /> : null}
        <polygon points="0,-116 -5,-104 5,-104" fill="#D9822B" />
      </g>
    </svg>
  );
};

// yellow brick road from the bottom to a vanishing point, bricks scroll when walking
export const BrickRoad: React.FC<{vx?: number; vy?: number; walk?: boolean; w0?: number}> = ({vx = 540, vy = 820, walk = false, w0 = 900}) => {
  const f = useCurrentFrame();
  const off = walk ? (f * 0.025) % 1 : 0;
  const rows = Array.from({length: 18}, (_, i) => {
    const t = (i + off) / 18; // 0 far .. 1 near
    const e = t * t;
    const y = vy + (1920 - vy) * e;
    const hw = 30 + (w0 / 2 - 30) * e;
    return {y, hw, i};
  });
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
      <path d={`M ${vx - 30} ${vy} L ${vx + 30} ${vy} L ${540 + w0 / 2} 1920 L ${540 - w0 / 2} 1920 Z`} fill="#F2C230" />
      {rows.map((r) => (
        <g key={r.i}>
          <line x1={vx + (540 - vx) * ((r.y - vy) / (1920 - vy)) - r.hw} y1={r.y} x2={vx + (540 - vx) * ((r.y - vy) / (1920 - vy)) + r.hw} y2={r.y} stroke="#C99A1E" strokeWidth={1 + 4 * ((r.y - vy) / (1920 - vy))} />
          {[-0.5, 0, 0.5].map((k, j) => (
            <line key={j} x1={vx + (540 - vx) * ((r.y - vy) / (1920 - vy)) + r.hw * (k + (r.i % 2 ? 0.25 : 0))} y1={r.y}
              x2={vx + (540 - vx) * ((r.y - vy) / (1920 - vy)) + r.hw * (k + (r.i % 2 ? 0.25 : 0))} y2={r.y + 10 + 50 * ((r.y - vy) / (1920 - vy)) ** 2} stroke="#C99A1E" strokeWidth={1 + 3 * ((r.y - vy) / (1920 - vy))} />
          ))}
        </g>
      ))}
    </svg>
  );
};

export const EmeraldCity: React.FC<{x: number; y: number; s?: number; glow?: number}> = ({x, y, s = 1, glow = 0.5}) => (
  <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
    <g transform={`translate(${x} ${y}) scale(${s})`} style={{filter: `drop-shadow(0 0 ${20 * glow}px #7CE0A0)`}}>
      {[[-90, 70, 18], [-55, 120, 22], [-18, 170, 26], [22, 140, 24], [58, 100, 20], [92, 60, 16]].map(([dx, h, w], i) => (
        <g key={i}><rect x={dx - w} y={-h} width={w * 2} height={h} fill={i % 2 ? '#1FA463' : '#2DBE6C'} /><polygon points={`${dx - w},${-h} ${dx},${-h - w * 1.8} ${dx + w},${-h}`} fill="#7CE0A0" /></g>
      ))}
      <rect x={-112} y={-4} width={224} height={10} fill="#14804A" />
    </g>
  </svg>
);

// corn field rows (the big farm where everyone works in pictures & graphic design)
export const CornField: React.FC<{y?: number; sway?: number}> = ({y = 1000, sway = 1}) => {
  const f = useCurrentFrame();
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
      {Array.from({length: 4}, (_, r) => (
        <g key={r}>
          {Array.from({length: 16}, (_, i) => {
            const x = i * 72 + (r % 2) * 36 - 20;
            const yy = y + r * 70;
            const h = 160 + rnd(i * 7 + r) * 60;
            const a = Math.sin(f / 22 + i * 0.6 + r) * 4 * sway;
            return (
              <g key={i} transform={`translate(${x} ${yy}) rotate(${a})`}>
                <rect x={-4} y={-h} width={8} height={h} fill={r < 2 ? '#6FA43A' : '#5A8E2E'} />
                <path d={`M 0 ${-h * 0.6} Q -36 ${-h * 0.7} -46 ${-h * 0.45}`} stroke="#7DB547" strokeWidth={9} fill="none" strokeLinecap="round" />
                <path d={`M 0 ${-h * 0.4} Q 36 ${-h * 0.5} 46 ${-h * 0.25}`} stroke="#7DB547" strokeWidth={9} fill="none" strokeLinecap="round" />
                <ellipse cx={6} cy={-h * 0.75} rx={8} ry={20} fill="#F2C230" />
              </g>
            );
          })}
        </g>
      ))}
      <rect x={0} y={y + 280} width={1080} height={1920 - y - 280} fill="#4E7E28" />
    </svg>
  );
};

// speech bubble = ONE path (body + tail, one continuous outline — Aly's rule #16)
export const Bubble: React.FC<{w: number; h: number; tail?: 'left' | 'right' | 'down'; children?: React.ReactNode; bg?: string; ink?: string}> = ({w, h, tail = 'down', children, bg = '#FFFFFF', ink = '#2B1D14'}) => {
  const r = 34, tx = tail === 'left' ? w * 0.22 : tail === 'right' ? w * 0.78 : w * 0.5;
  const d = `M ${r} 0 H ${w - r} Q ${w} 0 ${w} ${r} V ${h - r} Q ${w} ${h} ${w - r} ${h} H ${tx + 22} L ${tx + (tail === 'left' ? -40 : tail === 'right' ? 40 : 0)} ${h + 46} L ${tx - 22} ${h} H ${r} Q 0 ${h} 0 ${h - r} V ${r} Q 0 0 ${r} 0 Z`;
  return (
    <div style={{position: 'relative', width: w, height: h + 50}}>
      <svg width={w + 4} height={h + 54} style={{position: 'absolute', left: -2, top: -2, overflow: 'visible', filter: 'drop-shadow(0 10px 18px rgba(0,0,0,0.2))'}}>
        <path d={d} transform="translate(2 2)" fill={bg} stroke={ink} strokeWidth={5} strokeLinejoin="round" />
      </svg>
      <div style={{position: 'absolute', left: 0, top: 0, width: w, height: h, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center',
        fontFamily: AR, fontWeight: 900, color: ink, direction: 'rtl', padding: 20, boxSizing: 'border-box'}}>{children}</div>
    </div>
  );
};

// soft scene wrapper: quick fade/scale in, fade out, slow push
export const Sc: React.FC<{children: React.ReactNode; inF?: number; outF?: number}> = ({children, inF = 8, outF = 7}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  const a = Math.min(lin(f, 0, inF), lin(f, d - outF, d, 1, 0, Easing.in(Easing.cubic)));
  const s = 1.03 - 0.03 * lin(f, 0, inF + 6) + 0.02 * (f / Math.max(1, d));
  return <AbsoluteFill style={{opacity: a, transform: `scale(${s})`}}>{children}</AbsoluteFill>;
};
