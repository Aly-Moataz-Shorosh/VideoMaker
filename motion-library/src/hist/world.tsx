import React from 'react';
import {AbsoluteFill, Easing, Img, Loop, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {H, ST, WORLD_END, mix, skyAt} from './pal';
import {Ev, STATIONS} from './stations';

// ONE back scene for a whole short (look 'hist'): a single continuous side-scrolling world, old on the LEFT, new on the RIGHT.
// The camera walks left -> right while he talks; it slows / stops on an era, zooms in/out, effects play, then walks on.
// Props (seconds on the short's timeline):
//  cam    [{t, x, z}]                       camera keyframes (x = world x at screen centre, z = zoom, 1 = default)
//  ev     [{s, k, at, out?}]                station actions (stations.tsx), e.g. {s:'cave', k:'hands', at: 3.2}
//  pics   [{at, out, src, x, y, side?, label?, video?}]  small round photo / video circles next to an object (world x, y)
//  words  [{at, out, text, y?, size?, color?}]  big kinetic words (screen y fraction)
//  era    [{at, st}]                         HUD era card + year (st = station key)
//  meters [{at, v:[speed, effort, survival], label?}]   the 3 criteria gauges (HUD), hidden until the first one
//  bursts [{at, x, y, c?}]                   light rays + ring at a world point (when the camera stops on something)
type Cam = {t: number; x: number; z?: number};
type P = {cam: Cam[]; ev?: {s: string; k: string; at: number; out?: number}[]; pics?: any[]; words?: any[]; era?: {at: number; st: string}[];
  meters?: {at: number; v: number[]; label?: string}[]; bursts?: {at: number; x: number; y: number; c?: string}[]; only?: string[]};

export const HY = 1130; // horizon (screen y at z = 1)
export const GY = 1335; // standing line
const RULER = 1400; // ruler band 1400-1470; captions sit under it, his round webcam bottom-left below them
const c01 = (x: number) => Math.max(0, Math.min(1, x));
const ez = Easing.bezier(0.45, 0, 0.25, 1);
const pop = (x: number) => { const u = c01(x); return u < 1 ? 1 - Math.pow(1 - u, 3) * Math.cos(u * 7) : 1; };
const rnd = (s: number) => { const x = Math.sin(s * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

const camAt = (cams: Cam[], t: number) => {
  let i = 0;
  while (i < cams.length - 1 && t >= cams[i + 1].t) i++;
  const a = cams[i], b = cams[Math.min(i + 1, cams.length - 1)];
  const u = a === b ? 0 : ez(c01((t - a.t) / Math.max(0.001, b.t - a.t)));
  const za = a.z ?? 1, zb = b.z ?? 1;
  // a little drift so the shot never freezes (one-shot feel)
  const drift = 6 * Math.sin(t * 0.7);
  return {x: a.x + (b.x - a.x) * u + drift, z: Math.exp(Math.log(za) + (Math.log(zb) - Math.log(za)) * u), v: Math.abs(b.x - a.x) / Math.max(0.3, b.t - a.t) * (u > 0 && u < 1 ? 1 : 0)};
};

// far layer: dunes / mountains / far pyramids / far city (parallax 0.35)
const Far: React.FC<{camX: number; z: number; W: number}> = ({camX, z, W}) => {
  const p = 0.35, zf = 1 + (z - 1) * 0.35;
  const ox = W / 2 - camX * p * zf;
  const pts = (amp: number, base: number, k: number, seed: number) => {
    const x0 = Math.floor((camX * p - W / zf) / 40) * 40, x1 = camX * p + W / zf + 80;
    let d = `M${x0},${base + 300}`;
    for (let x = x0; x <= x1; x += 40) d += ` L${x},${base - amp * (0.5 + 0.5 * Math.sin(x / k + seed)) - amp * 0.4 * Math.sin(x / (k * 0.37) + seed * 2)}`;
    return d + ` L${x1},${base + 300} Z`;
  };
  const city = camX > 11400;
  return (
    <svg width={W} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
      <g transform={`translate(${ox},${HY - HY * zf}) scale(${zf})`}>
        <path d={pts(160, HY - 40, 260, 1)} fill={mix(skyAt(camX)[1], H.plum3, 0.35)} opacity={0.55} />
        <path d={pts(90, HY + 10, 170, 4)} fill={mix(skyAt(camX)[1], H.terra2, 0.4)} opacity={0.6} />
        {/* far pyramids around Egypt */}
        {[[4700, 220], [5100, 300], [5450, 180]].map(([x, h], i) => <g key={i} transform={`translate(${x * p},${HY + 10})`} opacity={0.55}>
          <path d={`M${-h},0 L0,${-h * 0.8} L${h},0 Z`} fill={mix(H.sand2, skyAt(camX)[1], 0.4)} /><path d={`M0,${-h * 0.8} L${h},0 L${h * 0.2},0 Z`} fill={mix(H.sand3, skyAt(camX)[1], 0.3)} /></g>)}
        {/* far city skyline at the modern end */}
        {city ? Array.from({length: 26}, (_, i) => {
          const x = 12000 * p + i * 70, h = 120 + rnd(i) * 260;
          return <rect key={i} x={x} y={HY + 10 - h} width={56} height={h} fill={mix(H.navy, skyAt(camX)[1], 0.55)} opacity={0.6} />;
        }) : null}
      </g>
    </svg>
  );
};

// ground band + timeline ruler + soil strata with buried things (mid layer, moves with the world)
const Ground: React.FC<{x0: number; x1: number}> = ({x0, x1}) => {
  const ticks = [];
  for (let x = Math.floor(x0 / 100) * 100; x < x1; x += 100) ticks.push(<rect key={x} x={x - 2} y={RULER + 6} width={4} height={x % 500 === 0 ? 30 : 14} fill={H.plum} opacity={0.75} />);
  const bur = [];
  for (let i = Math.floor(x0 / 260); i < x1 / 260; i++) {
    const x = i * 260 + rnd(i) * 120, y = RULER + 150 + rnd(i + 7) * 380, k = Math.floor(rnd(i + 3) * 5), r = rnd(i + 5) * 60 - 30;
    const era = x / WORLD_END;
    bur.push(<g key={i} transform={`translate(${x},${y}) rotate(${r})`} opacity={0.55}>
      {k === 0 ? <path d="M-30,0 L30,0 L22,18 L-22,18 Z" fill={H.soil1} /> : null}
      {k === 1 ? <><rect x={-34} y={-6} width={68} height={12} rx={6} fill={H.cream2} /><circle cx={-34} cy={0} r={10} fill={H.cream2} /><circle cx={34} cy={0} r={10} fill={H.cream2} /></> : null}
      {k === 2 ? (era > 0.8 ? <rect x={-24} y={-24} width={48} height={48} rx={4} fill={H.navy} /> : <circle r={14} fill={H.gold} opacity={0.8} />) : null}
      {k === 3 ? <path d="M-20,-20 L20,-14 L14,20 L-24,12 Z" fill={H.stone3} /> : null}
      {k === 4 ? (era > 0.75 ? <rect x={-30} y={-18} width={60} height={36} rx={6} fill={H.ink} /> : <path d="M0,-22 L18,0 L0,22 L-18,0 Z" fill={H.terra2} />) : null}
    </g>);
  }
  return (
    <g>
      <rect x={x0} y={HY} width={x1 - x0} height={RULER - HY} fill={H.sand} />
      <rect x={x0} y={HY} width={x1 - x0} height={40} fill={H.sand2} opacity={0.5} />
      {Array.from({length: Math.ceil((x1 - x0) / 140)}, (_, i) => {
        const x = Math.floor(x0 / 140) * 140 + i * 140, k = Math.floor(x / 140);
        return <path key={i} d={`M${x + rnd(k) * 60},${HY + 60 + rnd(k + 2) * 180} l${30 + rnd(k + 1) * 40},0`} stroke={H.sand3} strokeWidth={5} strokeLinecap="round" opacity={0.5} />;
      })}
      <rect x={x0} y={RULER} width={x1 - x0} height={70} fill={H.plum} />
      <rect x={x0} y={RULER} width={x1 - x0} height={8} fill={H.gold} />
      {ticks.map((tk) => React.cloneElement(tk, {fill: H.cream}))}
      <rect x={x0} y={RULER + 70} width={x1 - x0} height={4200} fill={H.soil2} />
      {[0, 1, 2, 3].map((k) => <path key={k} d={`M${x0},${RULER + 160 + k * 150} ${Array.from({length: Math.ceil((x1 - x0) / 200) + 1}, (_, i) => `l200,${rnd(k * 31 + i + Math.floor(x0 / 200)) * 30 - 15}`).join(' ')} L${x1},${RULER + 4300} L${x0},${RULER + 4300} Z`}
        fill={[H.soil1, H.soil2, H.soil3, H.soil4][k]} opacity={0.75} />)}
      {bur}
    </g>
  );
};

// foreground: blurred grass / stones / palms / columns passing faster than the world (parallax 1.6)
const Fore: React.FC<{camX: number; z: number; W: number; v: number}> = ({camX, z, W, v}) => {
  // tall columns / palms ONLY half-way between two eras: when the camera rests on an era they are off screen (1.6 x 550 px away),
  // they sweep across the screen while the camera travels = a natural wipe (Egyptian kit promo)
  const p = 1.6, zf = z * 1.05;
  const xs = Object.values(ST).map((s) => s.x).sort((a, b) => a - b);
  const mids = xs.slice(1).map((x, i) => (x + xs[i]) / 2);
  const items = mids.map((m, i) => {
    const fx = m * p, sx = W / 2 + (fx - camX * p) * zf;
    if (sx < -700 || sx > W + 700) return null;
    return (
      <g key={i} transform={`translate(${fx},${1940})`}>
        {i % 2 ? <><rect x={-70} y={-1700} width={140} height={1700} fill={H.plum2} /><rect x={-92} y={-1720} width={184} height={56} fill={H.plum} /><rect x={-92} y={-300} width={184} height={40} fill={H.plum} /></>
          : <><path d="M-16,0 L-9,-1150 L9,-1150 L16,0 Z" fill={H.plum2} />{[0, 1, 2, 3, 4, 5].map((j) => <path key={j} d={`M0,-1150 Q${(j - 2.5) * 130},${-1260 + Math.abs(j - 2.5) * 20} ${(j - 2.5) * 240},${-1080 + Math.abs(j - 2.5) * 70}`} stroke={H.green2} strokeWidth={40} fill="none" strokeLinecap="round" />)}</>}
      </g>
    );
  });
  return (
    <svg width={W} height={1920} style={{position: 'absolute', left: 0, top: 0, filter: 'blur(8px)'}}>
      <g transform={`translate(${W / 2 - camX * p * zf},${1920 - 1920 * zf}) scale(${zf})`} opacity={0.95 * c01((v - 250) / 900)}>{items}</g>
    </svg>
  );
};

// dust motes + floating triangles + birds (screen space, light)
const Air: React.FC<{t: number; camX: number; W: number}> = ({t, camX, W}) => (
  <svg width={W} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
    {Array.from({length: 26}, (_, i) => {
      const x = ((rnd(i) * W * 1.4 - camX * (0.2 + rnd(i + 1) * 0.5) + t * 14) % (W * 1.4) + W * 1.4) % (W * 1.4) - W * 0.2;
      const y = 300 + rnd(i + 2) * 1000 + Math.sin(t * 0.8 + i) * 30;
      return i % 5 === 0
        ? <path key={i} d="M0,-12 L11,8 L-11,8 Z" transform={`translate(${x},${y}) rotate(${t * 40 + i * 40})`} fill={H.cream} opacity={0.5} />
        : <circle key={i} cx={x} cy={y} r={2 + rnd(i + 3) * 4} fill={H.cream} opacity={0.25 + 0.3 * Math.abs(Math.sin(t + i))} />;
    })}
    {Array.from({length: 4}, (_, i) => {
      const u = ((t * 0.07 + rnd(i)) % 1);
      const x = W * 1.1 - u * W * 1.3, y = 380 + i * 50 + Math.sin(t * 2 + i) * 10, w = Math.sin(t * 12 + i * 2) * 10;
      return <path key={'b' + i} d={`M${x - 16},${y - w} Q${x - 8},${y - 6} ${x},${y} Q${x + 8},${y - 6} ${x + 16},${y - w}`} stroke={H.plum} strokeWidth={4} fill="none" opacity={0.6} />;
    })}
  </svg>
);

// HUD: era card + year (top), the 3 criteria gauges under it
const LABELS = ['سرعة الانتشار', 'الجهد', 'البقاء'];
const COLS = [H.teal, H.rust, H.gold];
const Hud: React.FC<{t: number; fps: number; era?: {at: number; st: string}[]; meters?: {at: number; v: number[]; label?: string}[]; W: number}> = ({t, era = [], meters = [], W}) => {
  const cur = [...era].reverse().find((e) => t >= e.at);
  const prev = cur ? era[era.indexOf(cur) - 1] : undefined;
  const k = cur ? c01((t - cur.at) / 0.45) : 0;
  const s = cur ? ST[cur.st] : null;
  const mi = meters.findIndex((m, i) => t >= m.at && (i === meters.length - 1 || t < meters[i + 1].at));
  const m = mi >= 0 ? meters[mi] : null;
  const mp = mi > 0 ? meters[mi - 1].v : [0, 0, 0];
  const mk = m ? ez(c01((t - m.at) / 0.9)) : 0;
  const show = m ? c01((t - meters[0].at) / 0.4) : 0;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {s ? (
        <div style={{position: 'absolute', top: 118, width: W, display: 'flex', flexDirection: 'column', alignItems: 'center', direction: 'rtl'}}>
          <div style={{transform: `translateY(${(1 - pop(k)) * -40}px) scale(${0.85 + 0.15 * pop(k)})`, opacity: c01(k * 3), display: 'flex', alignItems: 'center', gap: 18}}>
            <div style={{width: 18, height: 18, background: H.gold, transform: 'rotate(45deg)'}} />
            <div style={{fontFamily: 'Cairo', fontWeight: 900, fontSize: 60, color: H.cream, background: H.plum, padding: '0px 40px 10px', borderRadius: 18,
              border: `5px solid ${H.gold}`, boxShadow: '0 12px 0 rgba(40,20,30,0.35)'}}>{s.name}</div>
            <div style={{width: 18, height: 18, background: H.gold, transform: 'rotate(45deg)'}} />
          </div>
          <div style={{marginTop: 10, fontFamily: 'Cairo', fontWeight: 900, fontSize: 46, color: H.plum, background: H.cream, padding: '0 26px 6px', borderRadius: 12,
            opacity: c01(k * 2 - 0.4), transform: `translateY(${(1 - ez(c01(k * 1.5 - 0.2))) * -20}px)`}}>{s.year}</div>
        </div>
      ) : null}
      {m && show > 0 ? (
        <div style={{position: 'absolute', top: 345, left: 70, right: 70, display: 'flex', gap: 22, opacity: show, direction: 'rtl'}}>
          {LABELS.map((lb, i) => {
            const v = mp[i] + (m.v[i] - mp[i]) * mk;
            const up = m.v[i] - mp[i];
            return (
              <div key={i} style={{flex: 1, background: 'rgba(42,24,48,0.88)', borderRadius: 16, padding: '8px 14px 12px', border: `3px solid ${COLS[i]}`}}>
                <div style={{display: 'flex', justifyContent: 'space-between', fontFamily: 'Cairo', fontWeight: 800, fontSize: 30, color: H.cream}}>
                  <span>{lb}</span>
                  {mi > 0 && Math.abs(up) > 0.04 ? <span style={{color: up > 0 ? (i === 1 ? '#FF8A6A' : '#8EE59B') : (i === 1 ? '#8EE59B' : '#FF8A6A'), opacity: c01((t - m.at) / 0.3)}}>{up > 0 ? '▲' : '▼'}</span> : null}
                </div>
                <div style={{height: 16, background: 'rgba(255,255,255,0.15)', borderRadius: 8, marginTop: 6, overflow: 'hidden', direction: 'ltr'}}>
                  <div style={{width: `${Math.max(3, v * 100)}%`, height: '100%', background: COLS[i], borderRadius: 8}} />
                </div>
              </div>
            );
          })}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

export const HWorld: React.FC<P> = (p) => {
  const f = useCurrentFrame();
  const {fps, width: W} = useVideoConfig();
  const t = f / fps;
  const c = camAt(p.cam, t);
  const v = Math.abs(camAt(p.cam, t + 0.05).x - camAt(p.cam, t - 0.05).x - 6 * (Math.sin((t + 0.05) * 0.7) - Math.sin((t - 0.05) * 0.7))) / 0.1;
  const z = c.z;
  // zoomed out: lift the world so the small eras sit in the middle of the screen, not under an empty sky
  const lift = Math.max(0, 1 - z) * 260;
  const tx = W / 2 - c.x * z, ty = HY - HY * z - lift;
  const toScreen = (x: number, y: number) => [W / 2 + (x - c.x) * z, HY + (y - HY) * z - lift];
  const x0 = c.x - W / (2 * z) - 200, x1 = c.x + W / (2 * z) + 200;
  const [s1, s2] = skyAt(c.x);
  const evs = p.ev ?? [];
  const mkEv = (st: string): Ev => ({
    t,
    has: (k) => evs.some((e) => e.s === st && e.k === k && t >= e.at && (e.out === undefined || t < e.out)),
    on: (k, d = 1, delay = 0) => {
      const e = [...evs].reverse().find((e) => e.s === st && e.k === k && t >= e.at + delay);
      if (!e || (e.out !== undefined && t >= e.out)) return 0;
      return c01((t - e.at - delay) / d) || 1e-6;
    },
  });
  // stations in view
  const vis = Object.entries(ST).filter(([k, s]) => s.x > x0 - 700 && s.x < x1 + 700 && (!p.only || p.only.includes(k)));
  const sunX = W * 0.72 - ((c.x * 0.05) % 200);
  return (
    <AbsoluteFill style={{background: s2, overflow: 'hidden'}}>
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${s1} 0%, ${s2} 60%)`}} />
      <AbsoluteFill style={{background: `radial-gradient(circle at ${(sunX / W) * 100}% 38%, rgba(255,246,214,0.95) 0%, rgba(255,240,200,0.5) 7%, rgba(255,240,200,0) 30%)`}} />
      <Far camX={c.x} z={z} W={W} />
      <svg width={W} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <g transform={`translate(${tx},${ty}) scale(${z})`}>
          <Ground x0={x0} x1={x1} />
          {/* year labels on the ruler */}
          {Object.values(ST).filter((s) => s.x > x0 - 300 && s.x < x1 + 300).map((s) => (
            <g key={s.x} transform={`translate(${s.x},${RULER + 46})`}>
              <circle cx={0} cy={-46} r={14} fill={H.gold} stroke={H.plum} strokeWidth={5} />
              <text x={0} y={8} textAnchor="middle" fontFamily="Cairo" fontWeight={800} fontSize={34} fill={H.cream} style={{direction: 'rtl'}}>{s.year}</text>
            </g>
          ))}
          {vis.map(([k, s]) => {
            const S = STATIONS[k];
            return <g key={k} transform={`translate(${s.x},${GY})`}><S e={mkEv(k)} /></g>;
          })}
          {/* bursts: rays + ring */}
          {(p.bursts ?? []).map((b, i) => {
            const u = (t - b.at) / 1.4;
            if (u < 0 || u > 1) return null;
            const col = b.c ?? H.cream;
            return <g key={i} transform={`translate(${b.x},${b.y})`} opacity={1 - u}>
              {Array.from({length: 14}, (_, j) => <path key={j} d={`M0,-${120 + 260 * ez(u)} L18,-${40 + 160 * ez(u)} L-18,-${40 + 160 * ez(u)} Z`} fill={col} transform={`rotate(${j * (360 / 14) + u * 30})`} />)}
              <circle r={60 + 300 * ez(u)} fill="none" stroke={col} strokeWidth={14 * (1 - u)} />
            </g>;
          })}
        </g>
      </svg>
      <Air t={t} camX={c.x} W={W} />
      <Fore camX={c.x} z={z} W={W} v={v} />
      {/* photo / video circles, screen sized, anchored to world points */}
      {(p.pics ?? []).map((pc, i) => {
        if (t < pc.at - 0.1 || t > pc.out + 0.4) return null;
        const u = pop((t - pc.at) / 0.5), o = 1 - ez(c01((t - pc.out) / 0.35));
        const [sx, sy] = toScreen(pc.x, pc.y);
        const D = pc.d ?? 230;
        const cx = Math.max(D / 2 + 30, Math.min(W - D / 2 - 30, sx)), cy = Math.max(600 + D / 2, Math.min(1300 - D / 2, sy)) + Math.sin(t * 2 + i) * 6;
        const src = staticFile(pc.src);
        return (
          <div key={i} style={{position: 'absolute', left: cx - D / 2, top: cy - D / 2, width: D, height: D, transform: `scale(${u * o})`}}>
            <div style={{position: 'absolute', inset: -12, borderRadius: '50%', background: H.cream, boxShadow: '0 14px 30px rgba(40,20,30,0.45)'}} />
            <div style={{position: 'absolute', inset: -4, borderRadius: '50%', background: H.plum}} />
            <div style={{position: 'absolute', inset: 0, borderRadius: '50%', overflow: 'hidden', background: H.ink}}>
              {pc.video ? (
                <Loop durationInFrames={Math.max(2, Math.round((pc.len ?? 2) * fps))}>
                  <OffthreadVideo muted src={src} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${pc.zoom ?? 1.15})`}} />
                </Loop>
              ) : (
                <Img src={src} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: pc.pos ?? '50% 50%',
                  transform: `scale(${(pc.zoom ?? 1.1) + 0.12 * c01((t - pc.at) / Math.max(1, pc.out - pc.at))})`}} />
              )}
            </div>
            {pc.label ? <div style={{position: 'absolute', top: D + 8, left: -60, right: -60, display: 'flex', justifyContent: 'center'}}>
              <div style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 30, color: H.cream, background: H.plum, padding: '0 16px 4px', borderRadius: 10, direction: 'rtl', whiteSpace: 'nowrap'}}>{pc.label}</div></div> : null}
          </div>
        );
      })}
      {/* big kinetic words */}
      {(p.words ?? []).map((w, i) => {
        if (t < w.at || t > w.out + 0.3) return null;
        const u = pop((t - w.at) / 0.4), o = 1 - c01((t - w.out) / 0.3);
        return (
          <div key={i} style={{position: 'absolute', top: (w.y ?? 0.25) * 1920, width: W, display: 'flex', justifyContent: 'center', opacity: o, direction: 'rtl'}}>
            <div style={{fontFamily: 'Cairo', fontWeight: 900, fontSize: w.size ?? 96, color: w.color ?? H.cream, WebkitTextStroke: `14px ${H.plum}`, paintOrder: 'stroke fill',
              transform: `scale(${u}) rotate(${(w.rot ?? -3) * (1 - u)}deg)`, textShadow: `0 10px 0 ${H.plum2}`, lineHeight: 1.15, textAlign: 'center'}}>{w.text}</div>
          </div>
        );
      })}
      <Hud t={t} fps={fps} era={p.era} meters={p.meters} W={W} />
      {/* paper grain + soft vignette */}
      <Img src={staticFile(`bg/grain_${Math.floor(f / 2) % 3}.png`)} style={{position: 'absolute', width: W, height: 1920, opacity: 0.28, mixBlendMode: 'multiply'}} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(40,15,25,0.35) 100%)'}} />
    </AbsoluteFill>
  );
};

export const histScenes: Record<string, React.FC<any>> = {hworld: HWorld};
