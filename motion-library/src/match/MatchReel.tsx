import React from 'react';
import {AbsoluteFill, Audio, Img, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {fontCss} from '../blocks/theme';
import {Caps, S, AR, EN, lin, spr, rnd} from '../stage/kit';
import {lonLat, rings} from '../blocks/geo';
import {Fig3D, litAt} from './fig3d';

// "Live Playmobil match" reel (2026-11-01, Aly's phone video 9:16, face on screen the whole time).
// Mix of his approved styles: he fills the frame (13) + text BEHIND him via his matte + paper/marker Vox-style cards in the tray
// under his face + real 3D (skeleton, Playmobil body, Aly as a Playmobil reporter). Match clips are small, mirrored, silent.
const cue = z.object({t: z.number(), d: z.number(), k: z.string(), p: z.record(z.string(), z.any()).default({})});
export const matchReelSchema = z.object({
  duration: z.number().default(5),
  src: z.string().default(''),
  roto: z.string().default(''),
  cues: z.array(cue).default([]),
  words: z.array(z.object({w: z.string(), start: z.number(), end: z.number(), hl: z.boolean().optional()})).default([]),
  zoom: z.array(z.array(z.number())).default([[0, 1]]),
  sfx: z.array(z.object({t: z.number(), file: z.string(), vol: z.number().default(0.3)})).default([]),
  amp: z.array(z.number()).default([]),
  capsHide: z.array(z.tuple([z.number(), z.number()])).default([]),
});
type Props = z.infer<typeof matchReelSchema>;
type B = Record<string, number>;
const P = 'projects/livematch/';
const f2 = (fps: number, b: B | undefined, k: string, d = 0) => Math.round((b?.[k] ?? d) * fps);
const TRAY = {y: 1210, h: 460};
const CAP_Y = 1090;
const VOX = {paper: '#F3EEE2', ink: '#16130F', marker: '#FFD43B', red: '#E5352B', blue: '#2F6BFF', green: '#1FA45B'};
const fade = (f: number, dur: number, k = 6) => Math.min(1, f / k, (dur - f) / k);

// ---------- Vox-style pieces in OUR animation (springs, pops) ----------
const Tape: React.FC<{x: number; y: number; r: number}> = ({x, y, r}) => (
  <div style={{position: 'absolute', left: x, top: y, width: 120, height: 34, background: 'rgba(255,233,150,0.78)', transform: `rotate(${r}deg)`,
    boxShadow: '0 2px 6px rgba(0,0,0,0.18)'}} />
);
const Paper: React.FC<{w: number; h: number; x?: number; y?: number; tilt?: number; dur: number; delay?: number; children: React.ReactNode; tape?: boolean; pad?: number}> = (
  {w, h, x = 540, y = TRAY.y + TRAY.h / 2, tilt = -2, dur, delay = 0, children, tape = true, pad = 12}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, delay, 210, 14);
  const o = Math.min(1, (dur - f) / 6);
  return (
    <div style={{position: 'absolute', left: x - w / 2, top: y - h / 2, width: w, height: h, opacity: o,
      transform: `translateY(${(1 - p) * 120}px) rotate(${tilt * p + (1 - p) * 8}deg) scale(${0.7 + 0.3 * p})`}}>
      <div style={{position: 'absolute', inset: 0, background: '#fff', padding: pad, boxShadow: '0 22px 50px rgba(0,0,0,0.55)', borderRadius: 4}}>
        <div style={{position: 'relative', width: '100%', height: '100%', overflow: 'hidden', background: VOX.paper}}>{children}
          <Img src={staticFile(`bg/grain_${Math.floor(f / 2) % 3}.png`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', opacity: 0.18, mixBlendMode: 'multiply'}} />
        </div>
      </div>
      {tape ? <><Tape x={-30} y={-14} r={-28} /><Tape x={w - 90} y={-14} r={24} /></> : null}
    </div>
  );
};
// headline with the yellow marker stroke behind it
const Marker: React.FC<{text: string; at?: number; size?: number; color?: string; ink?: string; style?: React.CSSProperties}> = ({text, at = 0, size = 58, color = VOX.marker, ink = VOX.ink, style}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, at, 240, 15);
  const sw = lin(f, at + 2, at + 12);
  if (f < at) return null;
  return (
    <div style={{position: 'relative', display: 'inline-block', direction: 'rtl', unicodeBidi: 'isolate', fontFamily: AR, fontWeight: 900, fontSize: size, color: ink,
      padding: '0 18px', lineHeight: 1.25, transform: `scale(${0.6 + 0.4 * p}) rotate(-1.5deg)`, ...style}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: '18%', bottom: '8%', background: color, transformOrigin: 'right', transform: `scaleX(${sw}) skewX(-8deg)`, zIndex: 0, borderRadius: 6}} />
      <span style={{position: 'relative'}}>{text}</span>
    </div>
  );
};
// hand-drawn marker circle around something
const Scribble: React.FC<{x: number; y: number; w: number; h: number; at: number; color?: string}> = ({x, y, w, h, at, color = VOX.red}) => {
  const f = useCurrentFrame();
  const p = lin(f, at, at + 12);
  if (f < at) return null;
  const d = `M ${w * 0.1} ${h * 0.55} C ${w * 0.05} ${h * 0.05}, ${w * 0.95} ${-h * 0.05}, ${w * 0.97} ${h * 0.5} S ${w * 0.2} ${h * 1.08}, ${w * 0.06} ${h * 0.45} S ${w * 0.5} ${h * 0.02}, ${w * 0.7} ${h * 0.12}`;
  return (
    <svg width={w} height={h} style={{position: 'absolute', left: x, top: y, overflow: 'visible'}}>
      <path d={d} fill="none" stroke={color} strokeWidth={8} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
    </svg>
  );
};
const Stamp: React.FC<{text: string; at: number; x: number; y: number; color?: string; size?: number; r?: number}> = ({text, at, x, y, color = VOX.red, size = 54, r = -10}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (f < at) return null;
  const p = spr(f, fps, at, 320, 11);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) rotate(${r}deg) scale(${2.2 - 1.2 * p})`, opacity: Math.min(1, p * 1.5),
      border: `6px solid ${color}`, color, borderRadius: 12, padding: '2px 18px', fontFamily: AR, fontWeight: 900, fontSize: size, background: 'rgba(255,255,255,0.88)',
      direction: 'rtl', unicodeBidi: 'isolate', whiteSpace: 'nowrap'}}>{text}</div>
  );
};
const Logo: React.FC<{file: string; at: number; x: number; y: number; h: number; chip?: boolean; maxW?: number}> = ({file, at, x, y, h, chip = true, maxW = 520}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (f < at) return null;
  const p = spr(f, fps, at, 260, 12);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) scale(${p}) rotate(${(1 - p) * -20}deg)`,
      background: chip ? '#fff' : 'transparent', borderRadius: 22, padding: chip ? 16 : 0, boxShadow: chip ? '0 12px 30px rgba(0,0,0,0.35)' : undefined}}>
      <Img src={staticFile(P + 'logos/' + file)} style={{height: h, maxWidth: maxW, objectFit: 'contain', display: 'block'}} />
    </div>
  );
};
const Vid: React.FC<{file: string; from?: number; w: number; h: number; rate?: number; style?: React.CSSProperties}> = ({file, from = 0, w, h, rate = 1, style}) => {
  const {fps} = useVideoConfig();
  return <OffthreadVideo src={staticFile(P + 'clips/' + file + '.mp4')} startFrom={Math.round(from * fps)} playbackRate={rate} muted
    style={{width: w, height: h, objectFit: 'cover', display: 'block', ...style}} />;
};
const Tag: React.FC<{text: string; x: number; y: number; at?: number; bg?: string; color?: string; size?: number}> = ({text, x, y, at = 0, bg = VOX.ink, color = '#fff', size = 40}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (f < at) return null;
  const p = spr(f, fps, at, 260, 14);
  return <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) scale(${p})`, background: bg, color, fontFamily: AR, fontWeight: 900,
    fontSize: size, padding: '4px 20px', borderRadius: 999, whiteSpace: 'nowrap', direction: 'rtl', unicodeBidi: 'isolate', boxShadow: '0 8px 20px rgba(0,0,0,0.35)'}}>{text}</div>;
};

// ---------- tray scenes (under his face) ----------
type Sc = React.FC<{dur: number; p: any}>;
const ClipCard: Sc = ({dur, p}) => {
  const {fps} = useVideoConfig();
  const w = p.w ?? 760, h = p.h ?? 428;
  return (
    <Paper w={w + 24} h={h + 24} dur={dur} tilt={p.tilt ?? -2}>
      <Vid file={p.file} from={p.from ?? 0} w={w} h={h} rate={p.rate ?? 1} />
      {p.label ? <div style={{position: 'absolute', right: 14, bottom: 12}}><Marker text={p.label} at={f2(fps, p.b, 'label', 0.15)} size={40} /></div> : null}
      {(p.logos ?? []).map((l: any, i: number) => <Logo key={i} file={l.file} at={f2(fps, l, 'at')} x={l.x ?? 90} y={l.y ?? 80} h={l.h ?? 90} />)}
      {(p.stamps ?? []).map((s: any, i: number) => <Stamp key={i} text={s.text} at={f2(fps, s, 'at')} x={s.x ?? w / 2} y={s.y ?? h / 2} color={s.color} size={s.size} r={s.r} />)}
      {(p.tags ?? []).map((s: any, i: number) => <Tag key={i} text={s.text} at={f2(fps, s, 'at')} x={s.x ?? w / 2} y={s.y ?? 50} bg={s.bg} color={s.color} size={s.size} />)}
      {p.live ? <LiveBug x={w - 120} y={30} /> : null}
    </Paper>
  );
};
const LiveBug: React.FC<{x: number; y: number}> = ({x, y}) => {
  const f = useCurrentFrame();
  return <div style={{position: 'absolute', left: x, top: y, display: 'flex', alignItems: 'center', gap: 10, background: VOX.red, color: '#fff', fontFamily: EN,
    fontWeight: 900, fontSize: 30, padding: '4px 14px', borderRadius: 8}}><div style={{width: 14, height: 14, borderRadius: 7, background: '#fff', opacity: Math.floor(f / 12) % 2 ? 0.3 : 1}} />LIVE</div>;
};
const Vs: Sc = ({dur, p}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const b = p.b as B;
  const sc = spr(f, fps, f2(fps, b, 'score'), 280, 12);
  return (
    <Paper w={860} h={420} dur={dur} tilt={1.5}>
      <div style={{position: 'absolute', inset: 0, background: `linear-gradient(100deg, #DC052D 0 48%, ${VOX.paper} 48% 52%, #FDE100 52%)`, opacity: 0.22}} />
      <Logo file="bayern.png" at={f2(fps, b, 'a')} x={620} y={185} h={230} chip={false} />
      <Logo file="bvb.png" at={f2(fps, b, 'b')} x={210} y={185} h={230} chip={false} />
      <div style={{position: 'absolute', left: 415, top: 120, transform: `scale(${sc})`, fontFamily: EN, fontWeight: 900, fontSize: 110, color: VOX.ink}}>
        {f >= f2(fps, b, 'score') ? '2-2' : 'VS'}</div>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 18, textAlign: 'center'}}><Marker text="الماتش الحقيقي" at={f2(fps, b, 'real')} size={50} /></div>
    </Paper>
  );
};
// Germany with the league's stadiums lighting up (18 clubs = 18 dots, places not named)
const CITIES: [number, number][] = [[11.58, 48.14], [7.47, 51.51], [7.0, 51.04], [12.37, 51.34], [8.68, 50.11], [9.18, 48.78], [10.79, 52.42], [7.84, 47.99], [8.25, 49.99],
  [6.44, 51.19], [13.4, 52.52], [8.8, 53.08], [10.89, 48.37], [8.89, 49.25], [10.15, 48.68], [9.99, 53.55], [6.96, 50.94], [7.1, 51.55]];
const MapDE: Sc = ({dur, p}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const rs = rings('DEU');
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  rs.forEach((r) => r.forEach(([x, y]) => {x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y);}));
  const H = 380, k = H / (y1 - y0), Wd = (x1 - x0) * k;
  const d = rs.map((r) => 'M' + r.map(([x, y]) => `${((x - x0) * k).toFixed(1)},${((y - y0) * k).toFixed(1)}`).join('L') + 'Z').join('');
  const draw = lin(f, 2, 22);
  return (
    <Paper w={860} h={440} dur={dur} tilt={-1.5}>
      <svg width={Wd} height={H} style={{position: 'absolute', left: 520 - Wd / 2, top: 22, overflow: 'visible'}}>
        <path d={d} fill="#E7DFCC" stroke={VOX.ink} strokeWidth={5} strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
        {CITIES.map(([lo, la], i) => {
          const [mx, my] = lonLat(lo, la);
          const q = spr(f, fps, 14 + i * 2, 300, 12);
          return f < 14 + i * 2 ? null : <g key={i} transform={`translate(${(mx - x0) * k},${(my - y0) * k}) scale(${q})`}>
            <circle r={13} fill={VOX.red} stroke="#fff" strokeWidth={4} /><circle r={24 + 6 * Math.sin((f - i * 3) / 6)} fill="none" stroke={VOX.red} strokeWidth={2} opacity={0.5} /></g>;
        })}
      </svg>
      <Logo file="bundesliga.png" at={f2(fps, p.b, 'logo', 0.6)} x={170} y={300} h={46} maxW={300} />
      <div style={{position: 'absolute', left: 30, top: 40}}><Marker text="كل الملاعب" at={10} size={50} /></div>
    </Paper>
  );
};
// TRACAB -> bought by EA (2025) -> EA = the FIFA game, now EA SPORTS FC
const Chain: Sc = ({dur, p}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const b = p.b as B;
  const arrow = lin(f, f2(fps, b, 'ea') - 6, f2(fps, b, 'ea') + 6);
  return (
    <Paper w={900} h={440} dur={dur} tilt={1}>
      <div style={{position: 'absolute', left: 520, top: 50, width: 340, height: 110, background: VOX.ink, borderRadius: 18, transform: `scale(${spr(f, fps, 0, 240, 14)})`}}>
        <Img src={staticFile(P + 'logos/tracab.png')} style={{width: 300, margin: '24px 20px'}} /></div>
      <svg width={300} height={120} style={{position: 'absolute', left: 230, top: 50}}>
        <path d="M 290 60 Q 150 0 20 60" fill="none" stroke={VOX.red} strokeWidth={8} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - arrow} />
        {arrow > 0.95 ? <path d="M 20 60 l 26 -22 M 20 60 l 32 6" stroke={VOX.red} strokeWidth={8} strokeLinecap="round" /> : null}
      </svg>
      <Tag text="اشترتها · 2025" x={385} y={150} at={f2(fps, b, 'ea') + 4} bg={VOX.red} size={34} />
      <Logo file="eablue.png" at={f2(fps, b, 'ea')} x={200} y={105} h={70} maxW={330} />
      <Logo file="eafc.png" at={f2(fps, b, 'fc')} x={250} y={300} h={130} />
      <div style={{position: 'absolute', right: 40, top: 255, direction: 'rtl', fontFamily: AR, fontWeight: 800, fontSize: 38, color: VOX.ink, lineHeight: 1.35,
        opacity: lin(f, f2(fps, b, 'fc') + 4, f2(fps, b, 'fc') + 12)}}>
        <Marker text="EA بتاعة FIFA" at={f2(fps, b, 'fc') + 2} size={46} /><br />اللعبة اسمها دلوقتي EA SPORTS FC</div>
      <Stamp text="AI" at={f2(fps, b, 'ai', 99)} x={690} y={200} color={VOX.blue} size={44} r={8} />
    </Paper>
  );
};
// top-down pitch: 22 players + ball tracked with trails (Vox dotted style)
const Track: Sc = ({dur, p}) => {
  const f = useCurrentFrame();
  const Wp = 800, Hp = 400;
  const pos = (i: number, t: number) => {
    const bx = (i < 11 ? 0.28 : 0.72) + 0.16 * Math.sin(t / 40 + i) + 0.05 * Math.sin(t / 13 + i * 2);
    const by = 0.1 + ((i % 11) / 10) * 0.8 + 0.06 * Math.sin(t / 30 + i * 1.7);
    return [bx * Wp, by * Hp];
  };
  const ball = (t: number) => [Wp * (0.5 + 0.3 * Math.sin(t / 22)), Hp * (0.5 + 0.32 * Math.sin(t / 15 + 1))];
  const on = lin(f, 0, 16);
  return (
    <Paper w={Wp + 40} h={Hp + 40} dur={dur} tilt={-1}>
      <svg width={Wp} height={Hp} style={{position: 'absolute', left: 8, top: 8}}>
        <rect width={Wp} height={Hp} fill="#2E7D4F" /><g stroke="#fff" strokeWidth={3} fill="none" opacity={0.75}>
          <rect x={10} y={10} width={Wp - 20} height={Hp - 20} /><line x1={Wp / 2} y1={10} x2={Wp / 2} y2={Hp - 10} /><circle cx={Wp / 2} cy={Hp / 2} r={55} />
          <rect x={10} y={Hp / 2 - 90} width={110} height={180} /><rect x={Wp - 120} y={Hp / 2 - 90} width={110} height={180} /></g>
        {Array.from({length: 22}).map((_, i) => {
          if (i / 22 > on) return null;
          const [x, y] = pos(i, f);
          const trail = [12, 8, 4].map((d) => pos(i, f - d));
          return <g key={i}>{trail.map(([tx, ty], k) => <circle key={k} cx={tx} cy={ty} r={3} fill="#fff" opacity={0.25 + k * 0.15} />)}
            <circle cx={x} cy={y} r={11} fill={i < 11 ? '#DC052D' : '#FDE100'} stroke={VOX.ink} strokeWidth={3} />
            <rect x={x - 17} y={y - 17} width={34} height={34} fill="none" stroke="#22D3EE" strokeWidth={2} strokeDasharray="5 4" /></g>;
        })}
        {(() => {const [x, y] = ball(f); return <g><circle cx={x} cy={y} r={8} fill="#fff" stroke={VOX.ink} strokeWidth={3} /><circle cx={x} cy={y} r={20} fill="none" stroke={VOX.marker} strokeWidth={3} /></g>;})()}
      </svg>
      <div style={{position: 'absolute', right: 26, top: 20}}><Marker text="22 لعيب + الكورة" at={8} size={42} /></div>
    </Paper>
  );
};
// cameras all around one player, rays meeting on him -> not a normal picture
const Cams: Sc = ({dur, p}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = 8, cx = 430, cy = 210;
  const no = f2(fps, p.b, 'photo', 99);
  return (
    <Paper w={880} h={440} dur={dur} tilt={1.2}>
      <svg width={860} height={420} style={{position: 'absolute', left: 0, top: 0}}>
        {Array.from({length: n}).map((_, i) => {
          const a = (i / n) * Math.PI * 2 + 0.2, x = cx + 360 * Math.cos(a), y = cy + 175 * Math.sin(a);
          const q = spr(f, fps, i * 2, 260, 13), ray = lin(f, 10 + i * 2, 22 + i * 2);
          return <g key={i}>
            <line x1={x} y1={y} x2={x + (cx - x) * ray} y2={y + (cy - y) * ray} stroke={VOX.blue} strokeWidth={3} strokeDasharray="10 7" opacity={0.8} />
            <g transform={`translate(${x},${y}) rotate(${(a * 180) / Math.PI + 180}) scale(${q})`}>
              <rect x={-26} y={-17} width={40} height={34} rx={6} fill={VOX.ink} /><path d="M 14 -10 L 30 -18 L 30 18 L 14 10 Z" fill={VOX.ink} />
              <circle cx={-6} cy={0} r={8} fill="#22D3EE" /></g></g>;
        })}
        {/* the player = skeleton dots forming */}
        <g transform={`translate(${cx},${cy - 10})`}>
          <circle cx={0} cy={-80} r={20} fill="none" stroke={VOX.ink} strokeWidth={6} />
          <path d="M 0 -60 L 0 20 M -40 -40 L 40 -40 M -40 -40 L -55 0 M 40 -40 L 58 -2 M 0 20 L -28 85 M 0 20 L 30 85" stroke={VOX.ink} strokeWidth={6} strokeLinecap="round" fill="none" />
          {[[0, -80], [0, -60], [-40, -40], [40, -40], [-55, 0], [58, -2], [0, 20], [-28, 85], [30, 85]].map(([x, y], i) =>
            <circle key={i} cx={x} cy={y} r={7 * lin(f, 18 + i, 24 + i)} fill={VOX.marker} stroke={VOX.ink} strokeWidth={2} />)}
        </g>
      </svg>
      {f >= no ? <div style={{position: 'absolute', left: 60, top: 270, width: 150, height: 110, background: '#fff', border: '6px solid #fff', boxShadow: '0 8px 18px rgba(0,0,0,0.3)',
        transform: `rotate(-8deg) scale(${spr(f, fps, no, 260, 12)})`}}>
        <Vid file="goalR" from={1} w={138} h={98} /><Stamp text="✗" at={no + 6} x={70} y={50} size={70} r={0} /></div> : null}
      <div style={{position: 'absolute', right: 24, top: 14}}><Marker text="من كل الزوايا" at={6} size={44} /></div>
    </Paper>
  );
};
// the 21-point skeleton in real 3D, counter, named groups light up on his words
const Skel: Sc = ({dur, p}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const b = p.b as B;
  const cnt = lin(f, f2(fps, b, 'count'), f2(fps, b, 'count') + 22);
  const n = Math.round(cnt * 21);
  const lit = litAt(f, (p.groups ?? []) as [string, number][], fps);
  const groupNow = ((p.groups ?? []) as [string, number][]).filter(([, t]) => f >= t * fps).slice(-1)[0];
  const names: Record<string, string> = {head: 'الراس', sh: 'الكتاف', mid: 'الوسط', arm: 'مفاصل الإيد', leg: 'الرجل', heel: 'الكعب', tip: 'أطراف الصوابع'};
  const ang = 0.5 + f / 60;
  return (
    <Paper w={900} h={450} dur={dur} tilt={-1} pad={10}>
      <div style={{position: 'absolute', inset: 0, background: 'radial-gradient(circle at 50% 45%, #1B2340 0%, #0B0E1A 75%)'}} />
      <div style={{position: 'absolute', left: 230, top: 0}}>
        <Fig3D w={420} h={430} mode="run" on={f < f2(fps, b, 'count') ? 0.04 : Math.max(0.04, cnt)} lit={lit} cam={{r: 3.3, y: 1.0, ang, look: 0.92}} ground={false} />
      </div>
      <div style={{position: 'absolute', right: 34, top: 40, textAlign: 'center', color: '#fff'}}>
        <div style={{fontFamily: EN, fontWeight: 900, fontSize: 130, lineHeight: 1, color: S.yellow}}>{Math.max(0, n)}</div>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 40}}>نقطة</div></div>
      <div style={{position: 'absolute', left: 30, top: 30}}><Marker text="Skeleton" at={f2(fps, b, 'name')} size={50} /></div>
      {groupNow && f < (groupNow[1] + 1.1) * fps ? <Tag text={names[groupNow[0]]} x={160} y={300} at={Math.round(groupNow[1] * fps)} bg={S.yellow} color={VOX.ink} size={46} /> : null}
      {(p.tags ?? []).map((s: any, i: number) => <Tag key={i} text={s.text} at={f2(fps, s, 'at')} x={s.x ?? 160} y={s.y ?? 300} bg={s.bg} size={s.size ?? 38} />)}
    </Paper>
  );
};
// semi-automated offside: last defender line vs attacker's points, the line decides
const Offside: Sc = ({dur, p}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ln = lin(f, 10, 24);
  const Pts: React.FC<{x: number; c: string; lead?: number}> = ({x, c, lead = 0}) => (
    <g transform={`translate(${x},190)`}>
      {[[0, -95], [0, -75], [-22, -60], [22, -60], [-30, -25], [30, -25], [0, -15], [-16, 30], [16 + lead, 30], [-18, 75], [18 + lead * 1.6, 75]].map(([px, py], i) =>
        <circle key={i} cx={px} cy={py} r={8} fill={c} stroke="#fff" strokeWidth={2} />)}
      <path d={`M0 -95 L0 -15 M-22 -60 L22 -60 M0 -15 L-18 75 M0 -15 L${18 + lead * 1.6} 75`} stroke="#fff" strokeWidth={3} opacity={0.6} fill="none" />
    </g>
  );
  return (
    <Paper w={880} h={440} dur={dur} tilt={1.4}>
      <div style={{position: 'absolute', inset: 0, background: 'repeating-linear-gradient(90deg, #2E7D4F 0 90px, #2A7447 90px 180px)'}} />
      <svg width={860} height={420} style={{position: 'absolute', inset: 0}}>
        <Pts x={360} c="#FDE100" />
        <Pts x={420} c="#DC052D" lead={20} />
        <line x1={378 + 0} y1={20} x2={378} y2={400} stroke="#22D3EE" strokeWidth={6} opacity={ln} />
        <line x1={458} y1={20} x2={458} y2={400} stroke={VOX.red} strokeWidth={6} opacity={ln} strokeDasharray="14 8" />
        <rect x={378} y={20} width={80 * ln} height={380} fill={VOX.red} opacity={0.22} />
      </svg>
      <Stamp text="تسلل" at={f2(fps, p.b, 'off', 0.9)} x={640} y={150} size={60} />
      <div style={{position: 'absolute', left: 24, top: 18}}><Marker text="Semi-Automated Offside" at={f2(fps, p.b, 'name', 0.3)} size={40} /></div>
    </Paper>
  );
};
// offside data -> moves the Playmobil figures
const Flow: Sc = ({dur, p}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const b = p.b as B;
  const ar = lin(f, f2(fps, b, 'move') - 8, f2(fps, b, 'move'));
  return (
    <Paper w={900} h={430} dur={dur} tilt={-1.2}>
      <div style={{position: 'absolute', right: 40, top: 60, width: 300, height: 300, background: VOX.ink, borderRadius: 24, display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center', transform: `scale(${spr(f, fps, 0, 240, 14)})`}}>
        <div style={{fontFamily: 'monospace', color: '#22D3EE', fontSize: 30, lineHeight: 1.3, textAlign: 'left'}}>
          {[0, 1, 2, 3, 4].map((i) => <div key={i}>x:{(rnd(i + Math.floor(f / 4)) * 99).toFixed(1)} y:{(rnd(i + 7 + Math.floor(f / 4)) * 60).toFixed(1)}</div>)}</div>
        <div style={{fontFamily: AR, fontWeight: 900, color: '#fff', fontSize: 40, marginTop: 10}}>داتا التسلل</div>
      </div>
      <svg width={260} height={100} style={{position: 'absolute', left: 320, top: 160}}>
        <path d="M 250 50 L 30 50" stroke={VOX.red} strokeWidth={10} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - ar} />
        {ar > 0.95 ? <path d="M 30 50 l 30 -26 M 30 50 l 30 26" stroke={VOX.red} strokeWidth={10} strokeLinecap="round" /> : null}
      </svg>
      {f >= f2(fps, b, 'move') ? <div style={{position: 'absolute', left: 40, top: 60, width: 300, height: 300, borderRadius: 24, overflow: 'hidden', border: '6px solid #fff',
        transform: `scale(${spr(f, fps, f2(fps, b, 'move'), 240, 13)})`, boxShadow: '0 10px 24px rgba(0,0,0,0.3)'}}><Vid file="p_penalty" from={0.5} w={300} h={300} /></div> : null}
      {f >= f2(fps, b, 'move') ? <div style={{position: 'absolute', left: 60, top: 370}}><Marker text="بتحرك العرايس" at={f2(fps, b, 'move') + 3} size={42} /></div> : null}
    </Paper>
  );
};
// skeleton -> the Playmobil body pops onto it, in 3D
const Wrap: Sc = ({dur, p}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const sk = f2(fps, p.b, 'skin', 1.5);
  return (
    <Paper w={900} h={450} dur={dur} tilt={1} pad={10}>
      <div style={{position: 'absolute', inset: 0, background: 'radial-gradient(circle at 50% 45%, #1B2340 0%, #0B0E1A 75%)'}} />
      <div style={{position: 'absolute', left: 240, top: 0}}>
        <Fig3D w={420} h={430} mode="run" on={1} skin={sk} skelFade={1 - lin(f, sk + 10, sk + 24) * 0.6} cam={{r: 4.3, y: 1.05, ang: 0.9 + f / 70, look: 1.0}} ground={false} />
      </div>
      <div style={{position: 'absolute', left: 30, top: 30}}><Marker text="Skeleton" at={2} size={46} /></div>
      <Tag text="+ جسم Playmobil" x={730} y={360} at={sk + 4} bg={S.yellow} color={VOX.ink} size={40} />
      <Logo file="playmobil.png" at={f2(fps, p.b, 'logo', 99)} x={720} y={110} h={90} chip={false} maxW={300} />
    </Paper>
  );
};
// Playmobil ≈ LEGO, plastic look
const Brands: Sc = ({dur, p}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const b = p.b as B;
  return (
    <Paper w={880} h={430} dur={dur} tilt={-1.5}>
      <Logo file="playmobil.png" at={0} x={640} y={110} h={110} chip={false} maxW={380} />
      <div style={{position: 'absolute', left: 405, top: 60, fontFamily: EN, fontWeight: 900, fontSize: 100, color: VOX.ink, opacity: lin(f, f2(fps, b, 'lego') - 4, f2(fps, b, 'lego'))}}>≈</div>
      <Logo file="lego.png" at={f2(fps, b, 'lego')} x={220} y={110} h={160} chip={false} />
      {f >= f2(fps, b, 'plastic') ? <div style={{position: 'absolute', left: 240, top: 230, width: 400, height: 170, borderRadius: 14, overflow: 'hidden', border: '6px solid #fff',
        transform: `rotate(2deg) scale(${spr(f, fps, f2(fps, b, 'plastic'), 240, 13)})`}}><Vid file="p_moon" w={400} h={170} /></div> : null}
      <Stamp text="بلاستيك" at={f2(fps, b, 'plastic') + 6} x={720} y={330} color={VOX.blue} size={48} r={8} />
    </Paper>
  );
};
const Render: Sc = ({dur, p}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pr = lin(f, 6, dur - 10);
  return (
    <Paper w={880} h={440} dur={dur} tilt={1.2}>
      <Vid file={p.file ?? 'p_heli'} from={p.from ?? 0} w={856} h={416} />
      <div style={{position: 'absolute', left: 24, top: 24, width: 160, height: 160, background: 'rgba(0,0,0,0.75)', borderRadius: 24, padding: 14,
        transform: `scale(${spr(f, fps, f2(fps, p.b, 'logo'), 240, 13)})`}}><Img src={staticFile(P + 'logos/unreal.png')} style={{width: 132, height: 132, objectFit: 'contain', filter: 'invert(1)'}} /></div>
      <div style={{position: 'absolute', right: 30, bottom: 30, width: 380, background: 'rgba(0,0,0,0.75)', borderRadius: 14, padding: '10px 16px', color: '#fff', fontFamily: EN, fontWeight: 800, fontSize: 26}}>
        RENDER · {Math.round(pr * 100)}%<div style={{height: 10, background: '#333', borderRadius: 5, marginTop: 6}}><div style={{width: `${pr * 100}%`, height: '100%', background: S.yellow, borderRadius: 5}} /></div></div>
      <div style={{position: 'absolute', right: 26, top: 24}}><Marker text={p.label ?? 'Unreal Engine'} at={f2(fps, p.b, 'logo') + 2} size={44} /></div>
    </Paper>
  );
};
const Channels: Sc = ({dur, p}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const b = p.b as B;
  return (
    <Paper w={880} h={430} dur={dur} tilt={-1}>
      <div style={{position: 'absolute', right: 30, top: 24}}><Marker text="خدوا حقوق البث" at={f2(fps, b, 'rights')} size={48} /></div>
      <Logo file="sky.png" at={4} x={640} y={185} h={80} maxW={330} />
      <Logo file="mbc3.png" at={10} x={250} y={190} h={140} />
      <div style={{position: 'absolute', left: 380, top: 290, fontFamily: EN, fontWeight: 900, fontSize: 52, color: VOX.ink, transform: `scale(${spr(f, fps, 16, 260, 13)})`}}>RTL+</div>
      <Tag text="وقنوات تانية…" x={250} y={385} at={20} size={30} />
      <Stamp text="بث تجريبي" at={f2(fps, b, 'beta')} x={640} y={330} color={VOX.red} size={50} />
    </Paper>
  );
};
// his 2020 video: thumbnail + QR (rule: never a QR without the thumbnail) + the note he asked for
const OldVideo: Sc = ({dur, p}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const b = p.b as B;
  const nt = f2(fps, b, 'note');
  return (
    <Paper w={900} h={450} dur={dur} tilt={1}>
      <div style={{position: 'absolute', right: 26, top: 26, width: 520, height: 292, border: '6px solid #fff', boxShadow: '0 10px 24px rgba(0,0,0,0.35)', transform: `rotate(-2deg)`}}>
        <Img src={staticFile(P + 'pics/old_video_thumb.jpg')} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        <Stamp text="2020" at={f2(fps, b, 'year')} x={70} y={40} color={VOX.red} size={44} r={-12} /></div>
      <div style={{position: 'absolute', left: 40, top: 40, width: 250, height: 250, background: '#fff', padding: 12, transform: `scale(${spr(f, fps, f2(fps, b, 'qr'), 240, 13)})`,
        boxShadow: '0 10px 24px rgba(0,0,0,0.3)'}}><Img src={staticFile(P + 'pics/qr_old.png')} style={{width: '100%', height: '100%'}} /></div>
      <div style={{position: 'absolute', left: 40, top: 300, width: 250, textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 30, color: VOX.ink, opacity: lin(f, f2(fps, b, 'qr'), f2(fps, b, 'qr') + 8)}}>الفيديو كامل</div>
      {f >= nt ? <div style={{position: 'absolute', left: 24, right: 24, bottom: 18, background: VOX.ink, color: '#fff', borderRadius: 14, padding: '10px 18px', direction: 'rtl',
        fontFamily: AR, fontWeight: 700, fontSize: 27, lineHeight: 1.35, transform: `translateY(${(1 - spr(f, fps, nt, 220, 15)) * 120}px)`}}>
        <span style={{color: S.yellow, fontWeight: 900}}>تنويه: </span>وقتها كنت بتكلم عن ⁦2D animation⁩ و⁦motion capture⁩ لشخصية أو اتنين — المرة دي ماتش كامل بـ 22 لعيب ⁦3D⁩ لايف</div> : null}
    </Paper>
  );
};
const Follow: Sc = ({dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const press = f >= 20 && f < 28;
  return (
    <Paper w={820} h={360} dur={dur} tilt={-1}>
      {['instagram.svg', 'tiktok.svg', 'youtube-icon.svg', 'facebook.svg'].map((l, i) => (
        <Img key={l} src={staticFile('logos/' + l)} style={{position: 'absolute', left: 150 + i * 150, top: 50, width: 100, height: 100, objectFit: 'contain',
          transform: `scale(${spr(f, fps, i * 3, 260, 12)})`}} />))}
      <div style={{position: 'absolute', left: 0, right: 0, top: 175, textAlign: 'center', fontFamily: EN, fontWeight: 900, fontSize: 52, color: VOX.ink}}>@alyshorosh</div>
      <div style={{position: 'absolute', left: 290, top: 250, width: 220, height: 70, borderRadius: 999, background: f >= 28 ? '#555' : VOX.red, color: '#fff', fontFamily: AR,
        fontWeight: 900, fontSize: 40, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${press ? 0.9 : 1})`}}>{f >= 28 ? 'متابَع ✓' : 'تابعني'}</div>
    </Paper>
  );
};
const Poll: Sc = ({dur, p}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const b = p.b as B;
  const card = (x: number, file: string, label: string, at: number, tilt: number) => (
    <div style={{position: 'absolute', left: x, top: 40, width: 380, transform: `rotate(${tilt}deg) scale(${spr(f, fps, at, 240, 13)})`}}>
      <div style={{border: '6px solid #fff', boxShadow: '0 10px 24px rgba(0,0,0,0.3)', height: 230, overflow: 'hidden'}}><Vid file={file} w={368} h={218} /></div>
      <div style={{textAlign: 'center', marginTop: 10}}><Marker text={label} at={at + 4} size={42} /></div>
    </div>
  );
  return (
    <Paper w={900} h={420} dur={dur} tilt={0.8}>
      {card(470, 'goalP', 'بالطريقة دي', 0, -2)}
      {card(40, 'goalR', 'ولا العادي؟', f2(fps, b, 'real'), 2)}
      <div style={{position: 'absolute', left: 405, top: 120, fontFamily: AR, fontWeight: 900, fontSize: 70, color: VOX.red, transform: `scale(${spr(f, fps, f2(fps, b, 'real'), 260, 12)})`}}>؟</div>
    </Paper>
  );
};
const TRAYS: Record<string, Sc> = {clip: ClipCard, vs: Vs, map: MapDE, chain: Chain, track: Track, cams: Cams, skel: Skel, offside: Offside, flow: Flow,
  wrap: Wrap, brands: Brands, render: Render, channels: Channels, old: OldVideo, follow: Follow, poll: Poll};

// ---------- full-screen moments (his face stays in a round bubble) ----------
const FaceBubble: React.FC<{src: string; x: number; y: number; d?: number; at: number}> = ({src, x, y, d = 300, at}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 2, 220, 14);
  const k = 0.5;   // face (540, 690) of the 1080x1920 source -> centre of the bubble
  return (
    <div style={{position: 'absolute', left: x - d / 2, top: y - d / 2, width: d, height: d, borderRadius: d / 2, overflow: 'hidden', border: `8px solid ${S.yellow}`,
      boxShadow: '0 14px 34px rgba(0,0,0,0.6)', transform: `scale(${p})`}}>
      <OffthreadVideo src={staticFile(src)} startFrom={Math.round(at * fps)} muted style={{position: 'absolute', width: 1080 * k, height: 1920 * k, left: d / 2 - 540 * k, top: d / 2 - 690 * k, maxWidth: 'none'}} />
    </div>
  );
};
// real match (top) vs the same moment in Playmobil (bottom), both mirrored and small inside paper frames
const Split: React.FC<{dur: number; p: any; src: string; at: number}> = ({dur, p, src, at}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const o = fade(f, dur, 5);
  const words = (p.words ?? []) as [number, string, string][];
  const cur = words.filter(([t]) => f >= t * fps).slice(-1)[0];
  const box = (y: number, file: string, label: string, color: string, tilt: number, delay: number, w2?: string) => (
    <div style={{position: 'absolute', left: 70, top: y, width: 940, height: 530, background: '#fff', padding: 12, boxShadow: '0 24px 60px rgba(0,0,0,0.6)',
      transform: `rotate(${tilt}deg) translateX(${(1 - spr(f, fps, delay, 200, 15)) * (tilt > 0 ? 1200 : -1200)}px)`}}>
      <Vid file={file} from={p.from ?? 0} w={916} h={506} />
      <div style={{position: 'absolute', right: 26, top: 22}}><Marker text={label} at={delay + 4} size={46} color={color} ink={color === VOX.marker ? VOX.ink : '#fff'} /></div>
      {w2 ? <div style={{position: 'absolute', left: 26, bottom: 22}}><Tag text={w2} x={0} y={0} bg={VOX.ink} size={46} /></div> : null}
    </div>
  );
  return (
    <AbsoluteFill style={{opacity: o}}>
      <AbsoluteFill style={{background: '#14110D'}}>
        <Img src={staticFile(`bg/grain_${Math.floor(f / 2) % 3}.png`)} style={{width: 1080, height: 1920, opacity: 0.25, mixBlendMode: 'screen'}} />
      </AbsoluteFill>
      {box(250, p.top, p.labels?.[0] ?? 'الماتش الحقيقي', VOX.marker, -1.5, 0, cur?.[1])}
      {box(890, p.bot, p.labels?.[1] ?? 'Playmobil', VOX.blue, 1.5, 3, cur?.[2])}
      <div style={{position: 'absolute', left: 540, top: 832, transform: 'translate(-50%,-50%)', fontFamily: EN, fontWeight: 900, fontSize: 90, color: S.yellow,
        textShadow: '0 6px 20px rgba(0,0,0,0.8)'}}>=</div>
      <FaceBubble src={src} x={880} y={1520} d={300} at={at} />
      <div style={{position: 'absolute', left: 70, top: 1440, fontFamily: AR, fontWeight: 700, fontSize: 26, color: 'rgba(255,255,255,0.6)', direction: 'rtl'}}>المصدر: ⁦Bundesliga⁩ — مقاطع قصيرة للمراجعة</div>
    </AbsoluteFill>
  );
};
// Aly as a Playmobil reporter: 3D figure with his shirt, beard and a mic, the match blurred behind, LIVE + name strap
const Reporter: React.FC<{dur: number; p: any; amp: number[]; at: number}> = ({dur, p, amp, at}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const g = Math.round(at * fps) + f;
  const a = amp.length ? (amp[Math.min(amp.length - 1, g)] + (amp[Math.min(amp.length - 1, g + 1)] ?? 0)) / 2 : 0;
  const o = fade(f, dur, 6);
  const b = p.b as B;
  return (
    <AbsoluteFill style={{opacity: o, background: '#000'}}>
      <AbsoluteFill style={{filter: 'blur(16px) brightness(0.62)', transform: 'scale(1.15)'}}>
        <Vid file={p.bg ?? 'p_lineup'} from={0} w={1080} h={1920} rate={0.6} />
      </AbsoluteFill>
      <div style={{position: 'absolute', left: 0, top: 260, transform: `scale(${1 + f / 900})`, transformOrigin: '50% 60%'}}>
        <Fig3D w={1080} h={1500} mode="stand" on={0} skin={0} skelFade={0} mouth={Math.min(1, a)} talk={a} mic cam={{r: 2.6, y: 1.45, ang: 0.32 + 0.05 * Math.sin(f / 50), look: 1.32, fov: 38}} ground={false} />
      </div>
      <LiveBug x={60} y={170} />
      {/* name strap like a TV reporter */}
      <div style={{position: 'absolute', right: 0, top: 1300, width: 900, transform: `translateX(${(1 - spr(f, fps, 8, 200, 16)) * 900}px)`}}>
        <div style={{background: S.yellow, color: VOX.ink, fontFamily: AR, fontWeight: 900, fontSize: 58, padding: '6px 40px', direction: 'rtl'}}>علي شُرُش</div>
        <div style={{background: VOX.ink, color: '#fff', fontFamily: AR, fontWeight: 700, fontSize: 38, padding: '6px 40px', direction: 'rtl'}}>مراسل من ملعب ⁦Playmobil⁩</div>
      </div>
      {/* the movies' motion capture vs this time live */}
      {(p.cards ?? []).map((c: any, i: number) => {
        const t0 = Math.round(c.at * fps), t1 = Math.round((c.at + c.d) * fps);
        if (f < t0 || f >= t1) return null;
        return <Sequence key={i} from={t0} durationInFrames={t1 - t0} layout="none">
          {c.k === 'mocap' ? <Paper w={380} h={470} x={250} y={520} tilt={-4} dur={t1 - t0}>
            <Img src={staticFile(P + 'pics/mocap.jpg')} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
            <div style={{position: 'absolute', left: 0, right: 0, bottom: 10, textAlign: 'center'}}><Marker text="Motion Capture" size={38} /></div>
            <div style={{position: 'absolute', left: 0, right: 0, top: 10, textAlign: 'center'}}><Marker text="في الأفلام" size={38} at={4} /></div></Paper> : null}
          {c.k === 'live' ? <><Stamp text="LIVE" at={0} x={180} y={470} size={70} color={VOX.red} r={-8} /><Stamp text="ماتش حقيقي" at={b?.real ?? 10} x={200} y={640} size={46} color={VOX.ink} r={5} /></> : null}
          {c.k === 'first' ? <><Stamp text="أول تجربة" at={0} x={195} y={470} size={58} color={VOX.red} r={-6} />
            <Logo file="bundesliga.png" at={8} x={200} y={630} h={34} maxW={300} /></> : null}
        </Sequence>;
      })}
    </AbsoluteFill>
  );
};

// ---------- text BEHIND him: drawn under his matte ----------
const Behind: React.FC<{dur: number; p: any}> = ({dur, p}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pp = spr(f, fps, 0, 200, 13);
  const o = Math.min(1, (dur - f) / 6);
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: p.y ?? 210, textAlign: 'center', opacity: o, transform: `scale(${0.6 + 0.4 * pp}) translateY(${(1 - pp) * 60}px)`}}>
      <span style={{fontFamily: /[A-Za-z0-9]/.test(p.text[0]) ? EN : AR, fontWeight: 900, fontSize: p.size ?? 260, lineHeight: 1, color: p.color ?? S.yellow, direction: 'rtl',
        unicodeBidi: 'isolate', letterSpacing: p.ls ?? 0, textShadow: '0 12px 40px rgba(0,0,0,0.55)', WebkitTextStroke: p.stroke ? `6px ${VOX.ink}` : undefined}}>{p.text}</span>
    </div>
  );
};

export const MatchReel: React.FC<Props> = ({duration, src, roto, cues, words, zoom, sfx, amp, capsHide}) => {
  const {fps} = useVideoConfig();
  const now = useCurrentFrame();
  const fr = (s: number) => Math.round(s * fps);
  const t = now / fps;
  const live = (c: {t: number; d: number}) => now >= fr(c.t) - 1 && now < fr(c.t + c.d) + 1;
  const zs = zoom.map((z) => z[0]), zv = zoom.map((z) => z[1]);
  const zm = zs.length > 1 ? interpolate(t, zs, zv, {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : zv[0];
  const camStyle: React.CSSProperties = {position: 'absolute', inset: 0, transform: `scale(${zm})`, transformOrigin: '50% 34%'};
  const full = cues.filter((c) => (c.k === 'split' || c.k === 'reporter') && live(c));
  const fullOn = full.some((c) => now >= fr(c.t) + 6 && now < fr(c.t + c.d) - 6);
  const behinds = cues.filter((c) => c.k === 'behind');
  const trays = cues.filter((c) => TRAYS[c.k]);
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <style>{fontCss}</style>
      {/* his video = the base, always there (sound comes from it) */}
      <div style={camStyle}><OffthreadVideo src={staticFile(src)} style={{width: 1080, height: 1920}} /></div>
      {/* text behind him + his matte on top of it (only decoded while a behind-text is up) */}
      {behinds.map((c, i) => !live(c) ? null : (
        <Sequence key={'b' + i} from={fr(c.t)} durationInFrames={fr(c.d)} layout="none">
          <div style={camStyle}><Behind dur={fr(c.d)} p={c.p} /></div>
          {roto ? <div style={camStyle}><OffthreadVideo src={staticFile(roto)} startFrom={fr(c.t)} transparent muted style={{width: 1080, height: 1920}} /></div> : null}
        </Sequence>))}
      {/* soft dark floor under the tray so the cards read on his shirt */}
      <AbsoluteFill style={{background: 'linear-gradient(180deg, transparent 52%, rgba(0,0,0,0.45) 68%, rgba(0,0,0,0.55) 100%)', opacity: fullOn ? 0 : 1}} />
      {trays.map((c, i) => {
        if (!live(c)) return null;
        const C = TRAYS[c.k];
        return <Sequence key={'t' + i} from={fr(c.t)} durationInFrames={fr(c.d)} layout="none"><C dur={fr(c.d)} p={c.p} /></Sequence>;
      })}
      {full.map((c, i) => (
        <Sequence key={'f' + i} from={fr(c.t)} durationInFrames={fr(c.d)} layout="none">
          {c.k === 'split' ? <Split dur={fr(c.d)} p={c.p} src={src} at={c.t} /> : <Reporter dur={fr(c.d)} p={c.p} amp={amp} at={c.t} />}
        </Sequence>))}
      <Caps words={words} hide={capsHide} top={fullOn ? 1700 : CAP_Y} />
      {sfx.map((s, i) => <Sequence key={'x' + i} from={fr(s.t)} durationInFrames={fr(2.5)} layout="none"><Audio src={staticFile(s.file)} volume={s.vol} /></Sequence>)}
    </AbsoluteFill>
  );
};
