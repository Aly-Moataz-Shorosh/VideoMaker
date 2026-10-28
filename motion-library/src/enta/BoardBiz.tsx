import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {enter, lerp} from '../blocks/anim';
import {Backdrop, Title, clamp} from './Board';
import {E, Grain, Hi, Sticker, Tape, accentOf, stickerBorder} from './kit';

// Full-screen boards for رواد الأعمال ep01 (Karim Tamer, 2026-10-27) — ONE declarative board (like glass tb_free):
// title + a list of items placed in px (1920x1080, centre of the item) that pop in on the speaker's words (frames from the cue start).
// Item kinds: emo (Fluent 3D), pic (taped photo / video), logo (white tile), text, chip, mark (✓/✗), sticker, arrow (drawn),
// path (drawn SVG line), walker (emoji walking along a path), bar (grows), num (counts), panel (comic panel / paper area),
// strike (red line through). Any item: `out` = frame it leaves, `grey` = frame it fades to grey (a closed / failed thing),
// `float` = gentle bob, `rot`. Calm Backdrop + paper Title as all enta boards. Text in RTL wrappers (Arabic + English mixed).

const it = z.record(z.string(), z.any());
export const bizFreeSchema = z.object({
  title: z.string().default(''),
  items: z.array(it).default([]),
  previewBg: z.string().default(''),
});

const sm = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));

// sample a point on an SVG path string (M/L/Q/C absolute only) at t in 0..1 via a hidden path element is not available in
// node -> paths for walkers are given as point lists [[x,y],...] and drawn as smooth polylines
const along = (pts: number[][], t: number) => {
  const seg: number[] = []; let L = 0;
  for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); seg.push(d); L += d; }
  let s = t * L;
  for (let i = 0; i < seg.length; i++) {
    if (s <= seg[i] || i === seg.length - 1) { const k = seg[i] ? Math.min(1, s / seg[i]) : 0; return [lerp(k, pts[i][0], pts[i + 1][0]), lerp(k, pts[i][1], pts[i + 1][1])]; }
    s -= seg[i];
  }
  return pts[pts.length - 1];
};
const polyD = (pts: number[][]) => pts.map((p, i) => (i ? 'L' : 'M') + p[0] + ' ' + p[1]).join(' ');
// the first part (0..t) of a polyline: drawn lines/dashes reveal by cutting the point list (works for dashed lines too)
const partial = (pts: number[][], t: number) => {
  const L = polyLen(pts); let s = t * L; const out = [pts[0]];
  for (let i = 1; i < pts.length; i++) {
    const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    if (s >= d) { out.push(pts[i]); s -= d; continue; }
    const k = d ? s / d : 0; out.push([lerp(k, pts[i - 1][0], pts[i][0]), lerp(k, pts[i - 1][1], pts[i][1])]); break;
  }
  return out;
};
const polyLen = (pts: number[][]) => pts.slice(1).reduce((a, p, i) => a + Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]), 0);

// keyframed value: list of [frame, ...values] -> values at f (smooth between keys, held outside)
const key = (ks: number[][] | undefined, f: number, def: number[]): number[] => {
  if (!ks || !ks.length) return def;
  if (f <= ks[0][0]) return ks[0].slice(1);
  for (let i = 1; i < ks.length; i++) if (f < ks[i][0]) {
    const k = sm((f - ks[i - 1][0]) / Math.max(1, ks[i][0] - ks[i - 1][0]));
    return ks[i].slice(1).map((v, j) => lerp(k, ks[i - 1][j + 1], v));
  }
  return ks[ks.length - 1].slice(1);
};
function last<T>(ks: [number, T][] | undefined, f: number, def: T): T { let v = def; for (const q of ks ?? []) if (f >= q[0]) v = q[1]; return v; }

// Karim as a character, Captain-Azouz style (Aly 2026-10-28: "خد صور له من الفيديو و قصها و حركها اكنها كارتون زي القبطان عزوز",
// "الوش بس من غير الكتف", "صغر الوش شوية علشان يبقى زي باقي الجسم"): his real head from the call (hair + headset, no shoulders)
// on a full cartoon body in black (zip knit, white tee at the collar, dark trousers, white shoes).
// moves [[f, x, y]], poses [[f, 'stand'|'walk'|'push'|'cheer'|'sad'|'jump']], faces [[f, name with neutral/happy/sad]]; s = height px;
// x/y = his feet; flip = faces left. The face moves in little steps like cut-out animation.
const Char: React.FC<{d: Record<string, any>; f: number; o: number; p: number}> = ({d, f, o, p}) => {
  const [x, y] = key(d.moves, f, [d.x ?? 960, d.y ?? 800]);
  const pose: string = last(d.poses, f, 'stand');
  const face: string = last(d.faces, f, d.face ?? 'neutral');
  const mood = pose === 'push' ? 'effort' : /happy/.test(face) ? 'happy' : /sad/.test(face) ? 'sad' : 'neutral';
  const S = d.s ?? 300, u = S / 100, t = f / 30;
  const sw = pose === 'walk' ? Math.sin(t * 9) : 0;
  const hop = pose === 'cheer' ? -Math.abs(Math.sin(t * 6)) * 6 * u : pose === 'jump' ? -5 * u : 0;
  const lean = pose === 'push' ? 12 + Math.sin(t * 14) * 2 : sw * 2;
  // arm / leg angles (deg from straight down, + = forward = towards +x; flip turns him round)
  const [aF, aB] = pose === 'push' ? [92, 78] : pose === 'cheer' ? [165, -165] : pose === 'walk' ? [sw * 32, -sw * 32] : pose === 'sad' ? [4, -4] : pose === 'jump' ? [130, -130] : [12, -12];
  const [lF, lB] = pose === 'walk' ? [sw * 26, -sw * 26] : pose === 'push' ? [14, -28] : pose === 'jump' ? [28, -22] : [4, -4];
  const skin = '#d3a07e', top = '#17181c', trousers = '#2a2f3b';
  const arm = (ax: number, ang: number) => {
    const r = (ang * Math.PI) / 180, ex = ax + Math.sin(r) * 25, ey = 43 + Math.cos(r) * 25;
    return <g><line x1={ax} y1={43} x2={ex} y2={ey} stroke={top} strokeWidth={8} strokeLinecap="round" /><circle cx={ex} cy={ey} r={3.6} fill={skin} /></g>;
  };
  const leg = (lx: number, ang: number) => {
    const r = (ang * Math.PI) / 180, ex = lx + Math.sin(r) * 24, ey = 72 + Math.cos(r) * 24;
    return <g><line x1={lx} y1={72} x2={ex} y2={ey} stroke={trousers} strokeWidth={9} strokeLinecap="round" /><ellipse cx={ex + 2.5} cy={ey + 1.5} rx={5.5} ry={3} fill="#f6f4ef" stroke="#c9c4bb" strokeWidth={0.6} /></g>;
  };
  const tilt = pose === 'sad' ? 8 : Math.round(Math.sin(Math.floor(f / 3) / 2.2) * 4);
  return (
    <div style={{position: 'absolute', left: x - 50 * u, top: y - 100 * u + hop, width: 100 * u, height: 100 * u, opacity: o,
      transform: `scale(${lerp(p, 0.6, 1)}) scaleX(${d.flip ? -1 : 1}) rotate(${lean}deg)`, transformOrigin: '50% 100%', filter: 'drop-shadow(0 10px 12px rgba(0,0,0,.45))'}}>
      <svg viewBox="0 0 100 100" style={{position: 'absolute', inset: 0, width: '100%', height: '100%', overflow: 'visible'}}>
        {leg(45.5, lB)}{leg(54.5, lF)}
        {arm(36, aB)}
        {/* torso: black zip knit, shoulders, white tee at the collar */}
        <path d="M 34 42 Q 36 38 44 37.5 L 56 37.5 Q 64 38 66 42 L 64 74 Q 50 77 36 74 Z" fill={top} />
        <path d="M 45 37.5 L 50 43 L 55 37.5 Z" fill="#f1ede6" />
        <path d="M 43.5 37 L 50 44 L 56.5 37" fill="none" stroke="#33343a" strokeWidth={1.6} />
        <line x1={50} y1={44} x2={50} y2={74} stroke="#5a5b61" strokeWidth={0.9} />
        <rect x={46.5} y={33} width={7} height={6} rx={2} fill="#bf8c6b" />{/* neck */}
      </svg>
      {/* his real head from the call WITH the headset (Aly 2026-10-28: "خده بالسماعة عادي"), no shoulders */}
      <Img src={staticFile(`projects/entabiz01/pics/karim_head_${mood}.png`)} style={{position: 'absolute', left: 33 * u, top: 4 * u, width: 34 * u, height: 34 * u,
        transform: `rotate(${tilt}deg)`, transformOrigin: '50% 95%'}} />
      <svg viewBox="0 0 100 100" style={{position: 'absolute', inset: 0, width: '100%', height: '100%', overflow: 'visible'}}>{arm(64, aF)}</svg>
    </div>
  );
};

// a small world ("العالم بتاعك", Aly 2026-10-28): a shaded sphere, a label, the players of that business on its rim (emoji/logos at
// angles), grow [[f, scale]], shake [[f]] (Karim pushes it: it shakes and does not move), ceiling at a frame (a glass dome he hits).
const Planet: React.FC<{d: Record<string, any>; f: number; o: number; p: number}> = ({d, f, o, p}) => {
  const R = d.r ?? 170, [g] = key(d.grow, f, [1]);
  const col = accentOf(d.color ?? 'blue');
  const sh = (d.shake ?? []).reduce((a: number, q: number[]) => (f >= q[0] && f < q[0] + 20 ? Math.sin((f - q[0]) * 2.2) * (20 - (f - q[0])) * 0.8 : a), 0);
  const spin = (f / 30) * 18;
  const ceil = d.ceiling !== undefined ? sm((f - d.ceiling) / 12) : 0, cr = d.ceilR ?? 1.45; // dome radius (x R)
  const id = `${Math.round(d.x)}_${Math.round(d.y)}`;
  return (
    <div style={{position: 'absolute', left: d.x + sh, top: d.y, width: 0, height: 0, opacity: o, transform: `scale(${lerp(p, 0.3, 1) * g})`}}>
      <svg style={{position: 'absolute', left: -R * 1.6, top: -R * 1.6, width: R * 3.2, height: R * 3.2, overflow: 'visible'}} viewBox={`${-R * 1.6} ${-R * 1.6} ${R * 3.2} ${R * 3.2}`}>
        <defs>
          <radialGradient id={`pl${id}`} cx="35%" cy="30%" r="75%">
            <stop offset="0%" stopColor="#ffffff" stopOpacity={0.55} /><stop offset="35%" stopColor={col} stopOpacity={1} /><stop offset="100%" stopColor="#0c0f18" stopOpacity={1} />
          </radialGradient>
          <clipPath id={`pc${id}`}><circle r={R} /></clipPath>
        </defs>
        <circle r={R * 1.12} fill={col} opacity={0.12} />
        <circle r={R} fill={`url(#pl${id})`} stroke={E.white} strokeWidth={6} />
        <g clipPath={`url(#pc${id})`} opacity={0.22}>
          {[-0.5, -0.15, 0.2, 0.55].map((k, i) => <ellipse key={i} cx={((spin * (i % 2 ? 1 : -1) + i * 90) % (R * 4)) - R * 2} cy={k * R} rx={R * 0.9} ry={R * 0.12} fill="#fff" />)}
        </g>
        {ceil > 0 ? <path d={`M ${-R * cr} ${-R * 0.1} A ${R * cr} ${R * cr} 0 0 1 ${R * cr} ${-R * 0.1}`} fill="none" stroke="rgba(200,230,255,.85)" strokeWidth={7}
          strokeDasharray={`${ceil * R * cr * 3.2} 9999`} style={{filter: 'drop-shadow(0 0 8px rgba(160,210,255,.8))'}} /> : null}
      </svg>
      {d.logo ? <div style={{position: 'absolute', left: -R * 0.32, top: -R * 0.32, width: R * 0.64, height: R * 0.64, borderRadius: R * 0.14, background: E.white,
        display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 8px 18px rgba(0,0,0,.5)'}}><Img src={staticFile(d.logo)} style={{width: '78%', height: '78%', objectFit: 'contain'}} /></div> : null}
      {d.icon ? <Img src={staticFile(`fluent/${d.icon}.png`)} style={{position: 'absolute', left: -R * 0.42, top: -R * 0.42, width: R * 0.84, height: R * 0.84}} /> : null}
      {(d.pop ?? []).map((q: Record<string, any>, i: number) => {
        if (f < (q.at ?? 0)) return null;
        const k = enter(f, 30, q.at ?? 0), a = ((q.ang ?? 0) - 90) * Math.PI / 180, s = q.s ?? R * 0.42;
        const gq = q.grey !== undefined ? interpolate(f, [q.grey, q.grey + 15], [0, 1], clamp) : 0;
        return <Img key={i} src={staticFile(q.src ?? `fluent/${q.n}.png`)} style={{position: 'absolute', left: Math.cos(a) * (R + s * 0.38) - s / 2, top: Math.sin(a) * (R + s * 0.38) - s / 2,
          width: s, height: s, objectFit: 'contain', transform: `rotate(${q.ang ?? 0}deg) scale(${k})`, filter: `drop-shadow(0 6px 8px rgba(0,0,0,.5)) grayscale(${gq})`, opacity: 1 - gq * 0.5}} />;
      })}
      {d.label ? <div style={{position: 'absolute', left: 0, top: R + 26, transform: 'translateX(-50%)', background: col, color: E.ink, fontWeight: 900, fontSize: d.labelSize ?? 34,
        padding: '6px 22px', borderRadius: 40, border: `4px solid ${E.white}`, whiteSpace: 'nowrap', direction: 'rtl', boxShadow: '0 8px 16px rgba(0,0,0,.45)'}}><Hi text={d.label} color={E.white} /></div> : null}
    </div>
  );
};

// cake seen from above at an angle (Aly's example 2026-10-28: "مش فارق تاخد قد إيه من التورتة… قد ما فارق حجم التورتة"):
// frac = the slice, cut at `cut`, the slice slides by `slide` [dx, dy] at `move`. r = radius in px.
const Cake: React.FC<{d: Record<string, any>; f: number; o: number; p: number}> = ({d, f, o, p}) => {
  const R = d.r ?? 150, ry = 0.55, H = R * 0.32, fr = d.frac ?? 0.25;
  const cutK = d.cut !== undefined ? sm((f - d.cut) / 10) : 0;
  const mv = d.move !== undefined ? sm((f - d.move) / 22) : 0;
  const a0 = -Math.PI / 2, a1 = a0 + fr * 2 * Math.PI;
  const pt = (a: number, dy = 0) => `${Math.cos(a) * R} ${Math.sin(a) * R * ry + dy}`;
  const sector = (s0: number, s1: number, dy = 0) => `M 0 ${dy} L ${pt(s0, dy)} A ${R} ${R * ry} 0 ${s1 - s0 > Math.PI ? 1 : 0} 1 ${pt(s1, dy)} Z`;
  const piece = (s0: number, s1: number, dx: number, dy: number, k2: string) => (
    <g key={k2} transform={`translate(${dx} ${dy})`}>
      <path d={sector(s0, s1, H)} fill="#7a3f22" stroke="#4a2412" strokeWidth={3} />
      <path d={sector(s0, s1, 0)} fill="#f3d9b5" stroke="#fff" strokeWidth={4} />
      {[0.2, 0.45, 0.7].map((k, i) => { const a = s0 + (s1 - s0) * k; return <circle key={i} cx={Math.cos(a) * R * 0.62} cy={Math.sin(a) * R * 0.62 * ry} r={R * 0.08} fill="#d6283c" />; })}
    </g>
  );
  const mid = (a0 + a1) / 2, out = 14 * cutK;
  const [sx, sy] = d.slide ?? [0, 160];
  return (
    <div style={{position: 'absolute', left: d.x, top: d.y, width: 0, height: 0, opacity: o, transform: `scale(${lerp(p, 0.4, 1)})`}}>
      <svg style={{position: 'absolute', left: -R * 2, top: -R * 2, width: R * 4, height: R * 4, overflow: 'visible'}} viewBox={`${-R * 2} ${-R * 2} ${R * 4} ${R * 4}`}>
        <ellipse cx={0} cy={H + R * 0.12} rx={R * 1.15} ry={R * 1.15 * ry} fill="#e9e4dc" stroke="#fff" strokeWidth={4} opacity={0.9} />
        {piece(a1, a0 + 2 * Math.PI, 0, 0, 'rest')}
        {piece(a0, a1, Math.cos(mid) * out + sx * mv, Math.sin(mid) * out * ry + sy * mv, 'slice')}
      </svg>
    </div>
  );
};

// playing card thrown onto the table (عزة النفس بتلعب كوتشينة): from -> to over dur frames with a spin, face = 'A♠' etc.
const Card: React.FC<{d: Record<string, any>; f: number; o: number}> = ({d, f, o}) => {
  const k = sm((f - (d.at ?? 0)) / (d.dur ?? 14));
  const [x0, y0] = d.from ?? [960, 1200], [x1, y1] = d.to ?? [960, 600];
  const x = lerp(k, x0, x1), y = lerp(k, y0, y1) - Math.sin(k * Math.PI) * (d.arc ?? 120);
  const red = /[♥♦]/.test(d.face ?? '');
  return (
    <div style={{position: 'absolute', left: x - 55, top: y - 78, width: 110, height: 156, borderRadius: 12, background: '#fbf8f1', border: '4px solid #fff', outline: '2px solid rgba(20,20,30,.45)',
      boxShadow: '0 12px 22px rgba(0,0,0,.5)', transform: `rotate(${lerp(k, d.spin ?? 540, d.rot ?? 0)}deg)`, opacity: o, display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontFamily: 'Montserrat', fontWeight: 900, fontSize: 58, color: red ? '#d6283c' : '#1c2030', direction: 'ltr'}}>{d.face ?? 'A♠'}</div>
  );
};

const Item: React.FC<{d: Record<string, any>; f: number}> = ({d, f}) => {
  const at = d.at ?? 0;
  if (f < at) return null;
  if (d.out !== undefined && f >= d.out + 10) return null;
  const p = enter(f, 30, at);
  const o = d.out !== undefined ? interpolate(f, [d.out, d.out + 10], [1, 0], clamp) : 1;
  const g = d.grey !== undefined ? interpolate(f, [d.grey, d.grey + 15], [0, 1], clamp) : 0;
  const bob = d.float ? Math.sin((f - at) / 14 + (d.x ?? 0)) * 8 : 0;
  const filt = g ? `grayscale(${g}) brightness(${1 - 0.35 * g})` : undefined;
  const wrap = (child: React.ReactNode, from = 40) => (
    <div style={{position: 'absolute', left: d.x, top: d.y, transform: `translate(-50%, -50%) translateY(${lerp(p, from, 0) + bob}px) scale(${lerp(p, 0.4, 1) * (d.scale ?? 1)}) rotate(${(d.rot ?? 0) * p}deg)`,
      opacity: Math.min(1, p * 1.6) * o, filter: filt}}>{child}</div>
  );
  switch (d.k) {
    case 'emo':
      return wrap(<Img src={staticFile(`fluent/${d.n}.png`)} style={{width: d.s ?? 180, height: d.s ?? 180, filter: 'drop-shadow(0 12px 16px rgba(0,0,0,.45))', transform: d.flip ? 'scaleX(-1)' : undefined}} />);
    case 'sticker':
      return wrap(<Sticker name={d.n} size={d.s ?? 140} />);
    case 'logo':
      return wrap(
        <div style={{width: d.s ?? 200, height: d.s ?? 200, background: d.bg ?? E.white, borderRadius: (d.s ?? 200) * 0.2, display: 'flex', alignItems: 'center', justifyContent: 'center',
          boxShadow: '0 12px 26px rgba(0,0,0,.5)', outline: '2px solid rgba(20,20,30,.4)'}}>
          <Img src={staticFile(d.src)} style={{width: (d.s ?? 200) * (1 - 2 * (d.pad ?? 0.16)), height: (d.s ?? 200) * (1 - 2 * (d.pad ?? 0.16)), objectFit: 'contain'}} />
        </div>);
    case 'pic': {
      const vid = /\.(mp4|webm)$/.test(d.src);
      return wrap(
        <div style={{position: 'relative', width: d.w ?? 420}}>
          <div style={{position: 'relative', borderRadius: d.round ? '50%' : 10, overflow: 'hidden', ...(d.bare ? {} : stickerBorder(8)), background: d.bare ? 'transparent' : '#fff',
            height: d.h, aspectRatio: d.ar}}>
            {vid ? <OffthreadVideo src={staticFile(d.src)} muted transparent={String(d.src).endsWith('.webm')} startFrom={d.from ?? 0} style={{width: '100%', height: d.h || d.ar ? '100%' : undefined, objectFit: 'cover', display: 'block'}} />
              : <Img src={staticFile(d.src)} style={{width: '100%', height: d.h || d.ar ? '100%' : undefined, objectFit: d.fit ?? 'cover', objectPosition: d.pos ?? '50% 50%', display: 'block'}} />}
          </div>
          {d.bare || d.tape === false ? null : <Tape w={Math.min(150, (d.w ?? 420) * 0.34)} rot={-6} style={{top: -22, left: (d.w ?? 420) / 2 - Math.min(75, (d.w ?? 420) * 0.17)}} />}
          {d.cap ? <div style={{position: 'absolute', left: '50%', bottom: -50, transform: 'translateX(-50%) rotate(-2deg)', background: E.ink, color: E.white, fontWeight: 900, fontSize: d.capSize ?? 32,
            padding: '4px 18px', borderRadius: 8, whiteSpace: 'nowrap', border: `3px solid ${E.white}`, direction: 'rtl'}}><Hi text={d.cap} color={E.mustard} /></div> : null}
        </div>, 60);
    }
    case 'text':
      return wrap(
        <div style={{fontSize: d.size ?? 48, fontWeight: 900, color: d.paper ? E.ink : (d.color ? accentOf(d.color) : E.white), whiteSpace: 'nowrap', direction: 'rtl', textAlign: 'center',
          textShadow: d.paper ? undefined : '0 4px 12px rgba(0,0,0,.55)', lineHeight: 1.25,
          ...(d.paper ? {background: d.paper === 'blue' ? E.bluePaper : E.paper, padding: '8px 28px', borderRadius: 10, ...stickerBorder(6)} : {})}}>
          {String(d.text).split('\n').map((ln, i) => <div key={i}><Hi text={ln} color={d.hi ? accentOf(d.hi) : d.paper ? E.orange : E.mustard} /></div>)}
        </div>);
    case 'chip':
      return wrap(
        <div style={{display: 'flex', alignItems: 'center', gap: 12, background: accentOf(d.bg ?? 'blue'), color: E.ink, fontWeight: 900, fontSize: d.size ?? 40, padding: '8px 28px', borderRadius: 50,
          border: `5px solid ${E.white}`, boxShadow: '0 10px 20px rgba(0,0,0,.45)', whiteSpace: 'nowrap', direction: 'rtl'}}>
          {d.emo ? <Img src={staticFile(`fluent/${d.emo}.png`)} style={{width: (d.size ?? 40) * 1.3, height: (d.size ?? 40) * 1.3}} /> : null}
          <Hi text={d.text} color={E.white} />
        </div>);
    case 'mark':
      return wrap(<Sticker name={d.ok ? 'check' : 'cross'} size={d.s ?? 90} />, 0);
    case 'panel':
      return (
        <div style={{position: 'absolute', left: d.x - d.w / 2, top: d.y - d.h / 2, width: d.w, height: d.h, transform: `scale(${lerp(p, 0.85, 1)}) rotate(${d.rot ?? 0}deg)`, opacity: Math.min(1, p * 1.6) * o,
          background: d.bg === 'blue' ? E.bluePaper : d.bg === 'dark' ? '#1d2230' : E.paper, borderRadius: 14, ...stickerBorder(7), overflow: 'hidden', filter: filt}}>
          <Grain opacity={0.22} seed={11 + Math.round(d.x)} />
          {d.label ? <div style={{position: 'absolute', top: 10, right: 16, background: E.ink, color: E.white, fontWeight: 900, fontSize: 30, padding: '2px 14px', borderRadius: 8, direction: 'rtl'}}><Hi text={d.label} color={E.mustard} /></div> : null}
        </div>
      );
    case 'arrow': case 'path': {
      const pts: number[][] = d.pts ?? [[d.x1, d.y1], [d.x2, d.y2]];
      const k = sm((f - at) / (d.dur ?? 14));
      const end = along(pts, Math.max(0.001, k)), pre = along(pts, Math.max(0, k - 0.02));
      const ang = Math.atan2(end[1] - pre[1], end[0] - pre[0]) * 180 / Math.PI;
      const col = accentOf(d.color ?? 'mustard');
      return (
        <svg style={{position: 'absolute', inset: 0, width: 1920, height: 1080, opacity: o, overflow: 'visible', filter: filt}}>
          <path d={polyD(partial(pts, k))} fill="none" stroke="rgba(0,0,0,.35)" strokeWidth={(d.w ?? 9) + 6} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={d.dash ? '2 24' : undefined} />
          <path d={polyD(partial(pts, k))} fill="none" stroke={col} strokeWidth={d.w ?? 9} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={d.dash ? '2 24' : undefined} />
          {d.k === 'arrow' && k > 0.05 ? <polygon points="0,-17 30,0 0,17" fill={col} stroke="rgba(0,0,0,.35)" strokeWidth={3} transform={`translate(${end[0]} ${end[1]}) rotate(${ang})`} /> : null}
        </svg>
      );
    }
    case 'poly': { // filled shape (iceberg, pyramid, sea) — grows from its bottom (or fades) on `at`
      const k = sm((f - at) / (d.dur ?? 16));
      const pts: number[][] = d.pts;
      const ys = pts.map((q) => q[1]), y1 = Math.max(...ys);
      return (
        <svg style={{position: 'absolute', inset: 0, width: 1920, height: 1080, opacity: o * (d.op ?? 1), overflow: 'visible', filter: filt}}>
          <g transform={d.grow === false ? undefined : `translate(0 ${y1 * (1 - k)}) scale(1 ${Math.max(0.001, k)})`} opacity={d.grow === false ? k : 1}>
            <polygon points={pts.map((q) => q.join(',')).join(' ')} fill={d.fill ? (accentOf(d.fill) === E.orange && !['orange'].includes(d.fill) ? d.fill : accentOf(d.fill)) : E.white}
              stroke={d.stroke ?? E.white} strokeWidth={d.sw ?? 6} strokeLinejoin="round" />
          </g>
        </svg>
      );
    }
    case 'wave': { // animated sea surface (the AI wave), a filled band that moves
      const amp = d.amp ?? 40, y0 = d.y ?? 700, ph = (f - at) / (d.speed ?? 9);
      const pts: string[] = [];
      for (let x = -20; x <= 1940; x += 20) pts.push(`${x},${y0 + Math.sin(x / 140 + ph) * amp + Math.sin(x / 61 - ph * 1.7) * amp * 0.3}`);
      const k = sm((f - at) / 14);
      return (
        <svg style={{position: 'absolute', inset: 0, width: 1920, height: 1080, opacity: o * k, overflow: 'visible'}}>
          <polygon points={`-20,1100 ${pts.join(' ')} 1940,1100`} fill={d.fill ?? 'rgba(92,139,192,.55)'} stroke={E.white} strokeWidth={5} />
        </svg>
      );
    }
    case 'walker': {
      const k = sm((f - at) / (d.dur ?? 60));
      let [x, y] = along(d.pts, k);
      if (d.wave) { const ph = (f - (d.wave.at ?? at)) / (d.wave.speed ?? 9); y = (d.wave.y ?? 700) + Math.sin(x / 140 + ph) * (d.wave.amp ?? 40) + Math.sin(x / 61 - ph * 1.7) * (d.wave.amp ?? 40) * 0.3 + (d.dy ?? 10); }
      const s = d.s ?? 120;
      return <Img src={staticFile(`fluent/${d.n}.png`)} style={{position: 'absolute', left: x - s / 2, top: y - s * 0.95, width: s, height: s, opacity: o, transform: `rotate(${Math.sin(f / 4) * 5}deg)`, filter: 'drop-shadow(0 10px 12px rgba(0,0,0,.45))'}} />;
    }
    case 'bar': {
      const k = sm((f - at) / (d.dur ?? 20));
      const h = (d.h ?? 300) * k;
      return (
        <div style={{position: 'absolute', left: d.x - (d.w ?? 120) / 2, top: d.y - h, width: d.w ?? 120, height: h, background: accentOf(d.color ?? 'orange'), borderRadius: '10px 10px 0 0',
          border: `5px solid ${E.white}`, borderBottom: 'none', boxShadow: '0 10px 24px rgba(0,0,0,.4)', opacity: o, filter: filt}}>
          {d.label && k > 0.6 ? <div style={{position: 'absolute', top: -64, left: '50%', transform: 'translateX(-50%)', color: E.white, fontWeight: 900, fontSize: d.size ?? 40, whiteSpace: 'nowrap', direction: 'rtl', textShadow: '0 4px 10px rgba(0,0,0,.6)'}}><Hi text={d.label} color={E.mustard} /></div> : null}
        </div>
      );
    }
    case 'num': {
      const k = sm((f - at) / (d.dur ?? 30));
      const v = lerp(k, d.from ?? 0, d.to ?? 100);
      const txt = (d.prefix ?? '') + (d.dec ? v.toFixed(d.dec) : Math.round(v).toLocaleString('en-US')) + (d.suffix ?? '');
      return wrap(<div style={{fontSize: d.size ?? 120, fontWeight: 900, color: accentOf(d.color ?? 'mustard'), textShadow: '0 8px 0 rgba(0,0,0,.35)', whiteSpace: 'nowrap', direction: /[\u0600-\u06FF]/.test(txt) ? 'rtl' : 'ltr'}}>{txt}</div>, 0);
    }
    case 'char':
      return <Char d={d} f={f} o={o} p={p} />;
    case 'planet':
      return <Planet d={d} f={f} o={o} p={p} />;
    case 'cake':
      return <Cake d={d} f={f} o={o} p={p} />;
    case 'card':
      return <Card d={d} f={f} o={o} />;
    case 'strike': {
      const k = sm((f - at) / 10);
      return <div style={{position: 'absolute', left: d.x - d.w / 2, top: d.y - 5, width: d.w * k, height: 10, background: E.orange, borderRadius: 5, transform: `rotate(${d.rot ?? -6}deg)`, transformOrigin: 'left center', opacity: o, boxShadow: '0 3px 8px rgba(0,0,0,.4)'}} />;
    }
    default:
      return null;
  }
};

export const BizFree: React.FC<z.infer<typeof bizFreeSchema>> = ({title, items}) => {
  const f = useCurrentFrame();
  return (
    <Backdrop>
      {/* panels first (comic frames / areas), then everything else in list order */}
      {items.filter((d) => d.k === 'panel').map((d, i) => <Item key={'p' + i} d={d} f={f} />)}
      {items.filter((d) => d.k !== 'panel').map((d, i) => <Item key={i} d={d} f={f} />)}
      {title ? <Title text={title} /> : null}
    </Backdrop>
  );
};
