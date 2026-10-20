import React from 'react';
import {AbsoluteFill, Easing, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import data from './data.json';
import {AR, EN, lin, rnd, spr} from '../film/kit';

// Cairo map engine (cairohistory 2026-10-09). Aly: "الخرايط تكون دقيقة… زي ما انا راسمها بالظبط و التوسع بتاعها يكون دقيق".
// Every city / wall / canal is HIS Google Earth drawing (assets/kmz -> work/scripts/build_map.py -> data.json, metres around
// 31.245E 30.05N, x east, y north); today's Nile = OSM; Egypt region = Natural Earth. One tilted 3D camera flies over it
// (refs: Paris 3D timelapse, Crash Course maps, countryball characters). Houses rise inside his polygons era by era.

type XY = number[];
const DT: any = data;
const LY = DT.layers as Record<string, {kind: string; pts: XY[]}>;
const DECO = DT.deco;
const RO = DT.rorg as number[];
const rw = (p: XY): XY => [RO[0] + p[0] * 1000, RO[1] + p[1] * 1000]; // region km -> world metres

export const M = {
  sea: '#2E7FA6', sand: '#E7D7B1', sand2: '#DCC79C', hill: '#C9AE7E', hillDk: '#A88B5C', water: '#3A8DB6', waterDk: '#2A6E93', waterHi: '#9AD7EE',
  ink: '#2A1D12', red: '#C3241C', gold: '#F4B63C', cream: '#FFF6E2', green: '#6E9A3E',
  field: ['#A3B661', '#8FA952', '#B7C272', '#7F9C4B', '#AAB967'],
};
// house colours per era (roof, wall)
const ERA: Record<string, {roof: string[]; wall: string; tint: string; line: string}> = {
  fustat: {roof: ['#D7A86E', '#C99560', '#E2B983'], wall: '#9C6B3E', tint: '#7FAE45', line: '#4E8A22'},
  askar: {roof: ['#DDB27A', '#CDA06A', '#E7C48F'], wall: '#A0743F', tint: '#2E9C95', line: '#16706B'},
  qatai: {roof: ['#D9A066', '#C78B54', '#E5B57E'], wall: '#96603A', tint: '#D59A2B', line: '#9A6A10'},
  fatimid: {roof: ['#F0E2C2', '#E6D2A8', '#F7EBD0'], wall: '#B79B6C', tint: '#D2453B', line: '#B0221A'},
  mamluk: {roof: ['#E3CB98', '#D6BA84', '#EBD6A8'], wall: '#A88A58', tint: '#C9A04A', line: '#8E6A20'},
};
export const POLY: Record<string, string> = {fustat: 'الفسطاط', askar: 'العسكر#poly', qatai: 'القطائع', fatimid: 'القاهرة الفاطمية'};

export type Cam = {t: number; x?: number; y?: number; at?: string; s: number; tilt?: number; rot?: number};
export type Ev = {l: string; at: number; out?: number; d?: number};
export type Lab = {n: string; at: number; out?: number; red?: boolean; text?: string; dy?: number; big?: boolean};
export type Yr = {at: number; y: number; era: string; suf?: string};
export type Ball = {c: string; at: number; out?: number; mood?: string; x?: number; y?: number; name?: string};
export type Seat = {at: number; n: string; k: number; name: string; yr?: string};

const sm = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
// position of a named place: point layer, polygon centroid (deco), or region point
export const place = (n: string): XY => {
  if (n.startsWith('@')) return n.slice(1).split(',').map(Number); // explicit "@x,y" metres
  if (DECO.centroid[n]) return DECO.centroid[n];
  const l = LY[n] || LY[n + '#pt'];
  if (l) return l.kind === 'pt' ? l.pts[0] : centroid(l.pts);
  const r = DT.region.pts[n];
  if (r) return rw(r);
  throw new Error('place? ' + n);
};
const centroid = (p: XY[]) => [p.reduce((a, q) => a + q[0], 0) / p.length, p.reduce((a, q) => a + q[1], 0) / p.length];

const camAt = (cams: Cam[], t: number) => {
  const pos = (c: Cam) => (c.at ? place(c.at) : [c.x ?? 0, c.y ?? 0]);
  let i = 0;
  while (i < cams.length - 1 && t >= cams[i + 1].t) i++;
  const a = cams[i], b = cams[Math.min(i + 1, cams.length - 1)];
  const span = Math.max(0.001, b.t - a.t);
  const u = a === b ? 0 : Easing.bezier(0.45, 0, 0.2, 1)(Math.max(0, Math.min(1, (t - a.t) / span)));
  const pa = pos(a), pb = pos(b);
  // zoom geometric; position follows the zoom so big zooms feel like a fly-in
  const s = Math.exp(Math.log(a.s) + (Math.log(b.s) - Math.log(a.s)) * u);
  const zf = Math.abs(Math.log(b.s / a.s)) > 1 ? (1 / s - 1 / a.s) / (1 / b.s - 1 / a.s) : u;
  const w = Math.max(0, Math.min(1, isFinite(zf) ? zf : u));
  return {x: pa[0] + (pb[0] - pa[0]) * w, y: pa[1] + (pb[1] - pa[1]) * w, s,
    tilt: (a.tilt ?? 38) + ((b.tilt ?? 38) - (a.tilt ?? 38)) * u, rot: (a.rot ?? 0) + ((b.rot ?? 0) - (a.rot ?? 0)) * u};
};

const mkProj = (cam: {x: number; y: number; s: number; tilt: number; rot: number}, W: number, H: number, cy: number, cx = 0.5) => {
  const t = (cam.tilt * Math.PI) / 180, r = (cam.rot * Math.PI) / 180;
  const ct = Math.cos(t), st = Math.sin(t), cr = Math.cos(r), sr = Math.sin(r);
  const Dm = (2.4 * H) / cam.s;
  return (x: number, y: number, z = 0): [number, number, number, number] => {
    const dx = x - cam.x, dy = y - cam.y;
    const rx = dx * cr - dy * sr, ry = dx * sr + dy * cr;
    const up = ry * ct + z * st;
    const depth = Dm + ry * st - z * ct;
    const k = Dm / Math.max(depth, Dm * 0.2);
    return [W * cx + rx * cam.s * k, cy - up * cam.s * k, k, ry];
  };
};
type Proj = ReturnType<typeof mkProj>;
const path = (pr: Proj, pts: XY[], close = true, z = 0) =>
  pts.map((p, i) => {const q = pr(p[0], p[1], z); return `${i ? 'L' : 'M'}${q[0].toFixed(1)} ${q[1].toFixed(1)}`;}).join('') + (close ? 'Z' : '');
const partial = (pts: XY[], p: number) => {
  if (p >= 1) return pts;
  const L: number[] = [0];
  for (let i = 1; i < pts.length; i++) L.push(L[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  const tot = L[L.length - 1] * Math.max(0, p);
  const out: XY[] = [pts[0]];
  for (let i = 1; i < pts.length; i++) {
    if (L[i] <= tot) out.push(pts[i]);
    else {const u = (tot - L[i - 1]) / (L[i] - L[i - 1] || 1); out.push([pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * u, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * u]); break;}
  }
  return out;
};
const orientFrom = (pts: XY[], from: XY) => {
  const d0 = Math.hypot(pts[0][0] - from[0], pts[0][1] - from[1]), d1 = Math.hypot(pts[pts.length - 1][0] - from[0], pts[pts.length - 1][1] - from[1]);
  return d0 <= d1 ? pts : [...pts].reverse();
};
const shade = (hex: string, k: number) => {
  const n = parseInt(hex.slice(1), 16);
  const c = (v: number) => Math.max(0, Math.min(255, Math.round(v * k)));
  return `rgb(${c(n >> 16)},${c((n >> 8) & 255)},${c(n & 255)})`;
};

// ---------------- billboard icons (screen space, drawn standing on the map) ----------------
const Mosque: React.FC<{c?: string; spiral?: boolean}> = ({c = '#F3E6C8', spiral}) => (
  <g>
    <rect x={-46} y={-40} width={92} height={40} fill={c} stroke={M.ink} strokeWidth={4} />
    <path d="M-26 -40 A26 26 0 0 1 26 -40Z" fill={c} stroke={M.ink} strokeWidth={4} />
    {spiral ? (
      <g><path d="M44 0 L44 -60 L58 -60 L58 -0Z" fill={c} stroke={M.ink} strokeWidth={4} />
        <path d="M40 -60 L62 -60 L56 -96 L46 -96Z" fill={c} stroke={M.ink} strokeWidth={4} />
        <path d="M42 -20 L60 -30 M42 -40 L60 -50 M44 -72 L58 -82" stroke={M.ink} strokeWidth={3} /></g>
    ) : (
      <g><rect x={46} y={-96} width={14} height={96} fill={c} stroke={M.ink} strokeWidth={4} />
        <path d="M44 -96 L53 -116 L62 -96Z" fill={c} stroke={M.ink} strokeWidth={4} /></g>
    )}
    {[-30, -10, 10, 30].map((x) => <path key={x} d={`M${x - 6} 0 L${x - 6} -18 A6 6 0 0 1 ${x + 6} -18 L${x + 6} 0`} fill={M.ink} opacity={0.75} />)}
  </g>
);
const Fort: React.FC<{c?: string}> = ({c = '#CDB48A'}) => (
  <g>
    <rect x={-60} y={-46} width={120} height={46} fill={c} stroke={M.ink} strokeWidth={4} />
    {[-60, 60].map((x) => <g key={x}><rect x={x - 18} y={-74} width={36} height={74} fill={c} stroke={M.ink} strokeWidth={4} />
      {[-18, -6, 6].map((d) => <rect key={d} x={x + d} y={-84} width={8} height={10} fill={c} stroke={M.ink} strokeWidth={3} />)}</g>)}
    {[-36, -16, 4, 24].map((x) => <rect key={x} x={x} y={-56} width={12} height={10} fill={c} stroke={M.ink} strokeWidth={3} />)}
    <path d="M-12 0 L-12 -24 A12 12 0 0 1 12 -24 L12 0Z" fill={M.ink} />
  </g>
);
const Gate: React.FC = () => (
  <g>
    {[-34, 34].map((x) => <g key={x}><rect x={x - 20} y={-70} width={40} height={70} fill="#E2CC9C" stroke={M.ink} strokeWidth={4} />
      {[-20, -7, 6].map((d) => <rect key={d} x={x + d} y={-80} width={9} height={10} fill="#E2CC9C" stroke={M.ink} strokeWidth={3} />)}</g>)}
    <rect x={-14} y={-50} width={28} height={50} fill="#E2CC9C" stroke={M.ink} strokeWidth={4} />
    <path d="M-10 0 L-10 -26 A10 10 0 0 1 10 -26 L10 0Z" fill={M.ink} />
  </g>
);
const Palace: React.FC<{c?: string}> = ({c = '#F5EEDC'}) => (
  <g>
    <rect x={-70} y={-48} width={140} height={48} fill={c} stroke={M.ink} strokeWidth={4} />
    <path d="M-80 -48 L0 -76 L80 -48Z" fill="#D9C79E" stroke={M.ink} strokeWidth={4} />
    {[-50, -26, 26, 50].map((x) => <rect key={x} x={x - 6} y={-40} width={12} height={20} fill={M.ink} opacity={0.7} />)}
    <rect x={-12} y={-30} width={24} height={30} fill={M.ink} />
  </g>
);
const Citadel: React.FC = () => (
  <g>
    <path d="M-90 0 L-90 -40 L90 -40 L90 0Z" fill="#CDB48A" stroke={M.ink} strokeWidth={4} />
    {[-90, -30, 30, 90].map((x) => <rect key={x} x={x - 14} y={-62} width={28} height={62} fill="#CDB48A" stroke={M.ink} strokeWidth={4} />)}
    <path d="M-30 -40 A30 30 0 0 1 30 -40Z" fill="#B8C3C9" stroke={M.ink} strokeWidth={4} />
    <rect x={40} y={-110} width={10} height={70} fill="#E8E2D2" stroke={M.ink} strokeWidth={3} />
  </g>
);
const ICON: Record<string, React.FC<any>> = {
  mosque: Mosque, spiral: (p) => <Mosque {...p} spiral />, fort: Fort, gate: Gate, palace: Palace, citadel: Citadel,
};

// ---------------- countryball-style city character ----------------
export const CityBall: React.FC<{c: string; r: number; f: number; mood?: string; seed?: number}> = ({c, r, f, mood = 'happy', seed = 1}) => {
  const e = ERA[c] || ERA.fustat;
  const blink = (Math.floor(f / 3) + seed * 7) % 37 === 0;
  const look = Math.sin(f / 23 + seed) * r * 0.08;
  const eyeY = -r * 0.12, eyeH = blink ? r * 0.04 : mood === 'angry' ? r * 0.16 : r * 0.24;
  return (
    <g>
      <ellipse cx={0} cy={r * 1.02} rx={r * 0.8} ry={r * 0.18} fill="#000" opacity={0.25} />
      <circle r={r} fill={e.tint} stroke={M.ink} strokeWidth={r * 0.07} />
      <path d={`M${-r} 0 A${r} ${r} 0 0 0 ${r} 0Z`} fill="#000" opacity={0.12} />
      {[-1, 1].map((sd) => (
        <g key={sd}>
          <ellipse cx={sd * r * 0.36} cy={eyeY} rx={r * 0.2} ry={eyeH} fill="#fff" stroke={M.ink} strokeWidth={r * 0.05} />
          {!blink ? <circle cx={sd * r * 0.36 + look} cy={eyeY + r * 0.03} r={r * 0.07} fill={M.ink} /> : null}
          {mood === 'angry' ? <path d={`M${sd * r * 0.6} ${eyeY - r * 0.3} L${sd * r * 0.16} ${eyeY - r * 0.16}`} stroke={M.ink} strokeWidth={r * 0.08} strokeLinecap="round" /> : null}
        </g>
      ))}
      {mood === 'happy' ? <path d={`M${-r * 0.22} ${r * 0.3} Q0 ${r * 0.48} ${r * 0.22} ${r * 0.3}`} stroke={M.ink} strokeWidth={r * 0.06} fill="none" strokeLinecap="round" /> : null}
      {mood === 'squeeze' ? <path d={`M${-r * 0.2} ${r * 0.36} L${r * 0.2} ${r * 0.36}`} stroke={M.ink} strokeWidth={r * 0.06} strokeLinecap="round" /> : null}
      {/* hats */}
      {c === 'fustat' ? <path d={`M${-r * 0.8} ${-r * 0.62} Q0 ${-r * 1.5} ${r * 0.8} ${-r * 0.62} Q0 ${-r * 0.85} ${-r * 0.8} ${-r * 0.62}Z`} fill="#F4F0E6" stroke={M.ink} strokeWidth={r * 0.05} /> : null}
      {c === 'askar' ? <g><path d={`M${-r * 0.78} ${-r * 0.55} A${r * 0.8} ${r * 0.7} 0 0 1 ${r * 0.78} ${-r * 0.55}Z`} fill="#8C8C8C" stroke={M.ink} strokeWidth={r * 0.05} />
        <rect x={-r * 0.06} y={-r * 1.45} width={r * 0.12} height={r * 0.3} fill={M.red} /></g> : null}
      {c === 'qatai' ? <g transform={`translate(${r * 0.15},${-r * 0.85}) scale(${r / 95})`}><path d="M-22 10 L-22 -30 L22 -30 L22 10Z M-26 -30 L26 -30 L18 -62 L-18 -62Z" fill="#E6CFA0" stroke={M.ink} strokeWidth={5} />
        <path d="M-22 -8 L22 -18 M-20 -44 L20 -52" stroke={M.ink} strokeWidth={4} /></g> : null}
      {c === 'fatimid' ? <path d={`M${-r * 0.6} ${-r * 0.7} L${-r * 0.6} ${-r * 1.25} L${-r * 0.3} ${-r * 0.98} L0 ${-r * 1.35} L${r * 0.3} ${-r * 0.98} L${r * 0.6} ${-r * 1.25} L${r * 0.6} ${-r * 0.7}Z`} fill={M.gold} stroke={M.ink} strokeWidth={r * 0.05} /> : null}
      {c === 'mamluk' ? <path d={`M${-r * 0.75} ${-r * 0.6} Q0 ${-r * 1.7} ${r * 0.75} ${-r * 0.6}Z`} fill="#E9E4D8" stroke={M.ink} strokeWidth={r * 0.05} /> : null}
    </g>
  );
};

const Crown: React.FC<{s: number}> = ({s}) => (
  <g transform={`scale(${s})`}>
    <path d="M-50 10 L-56 -40 L-26 -16 L0 -52 L26 -16 L56 -40 L50 10Z" fill={M.gold} stroke={M.ink} strokeWidth={6} strokeLinejoin="round" />
    <rect x={-52} y={4} width={104} height={16} rx={4} fill="#E39A1E" stroke={M.ink} strokeWidth={6} />
    {[-30, 0, 30].map((x) => <circle key={x} cx={x} cy={12} r={5} fill={M.red} />)}
    <circle cx={0} cy={-56} r={7} fill={M.red} stroke={M.ink} strokeWidth={4} />
  </g>
);

// ---------------- the map scene ----------------
export const CairoMap: React.FC<{cam: Cam[]; ev?: Ev[]; labels?: Lab[]; years?: Yr[]; balls?: Ball[]; seats?: Seat[]; icons?: {n: string; i: string; at: number; out?: number; s?: number}[];
  b?: Record<string, number>; cy?: number; cx?: number; hud?: number}> = ({cam, ev = [], labels = [], years = [], balls = [], seats = [], icons = [], cy = 0.57, cx = 0.5, hud = 0.1}) => {
  const f = useCurrentFrame();
  const {fps, width: W, height: H} = useVideoConfig();
  const t = f / fps;
  const c = camAt(cam, t);
  const pr = mkProj(c, W, H, H * cy, cx); // cx < 0.5 when Aly stands on the right
  // layer progress: 0 before, ramps to 1 over d, back to 0 after out
  const pg = (l: string, d0 = 1.2) => {
    let v = 0;
    for (const e of ev) if (e.l === l && t >= e.at) {
      const d = e.d ?? d0;
      const k = Math.min(1, (t - e.at) / d) * (e.out !== undefined ? 1 - Math.min(1, Math.max(0, (t - e.out) / 0.6)) : 1);
      v = Math.max(v, k);
    }
    return v;
  };
  const regionW = 1 - lin(c.s, 0.012, 0.05, 0, 1, (x) => x); // Egypt-scale features
  const cityW = lin(c.s, 0.02, 0.06, 0, 1, (x) => x); // Cairo detail
  const onScreen = (q: number[], m = 120) => q[0] > -m && q[0] < W + m && q[1] > -m && q[1] < H + m;
  const px = (m: number, k = 1) => m * c.s * k; // metres -> px

  // --- water
  const oldP = pg('oldnile', 1.6); // Aly's "شط النيل قديما" + islands (except Roda) under water
  const modern = pg('modern', 6); // modern city grows outward
  const roads = pg('roads', 2.5);
  const rivPath = DT.nile.map((r: XY[]) => path(pr, r)).join('');
  // --- houses (all eras) with progress
  type Box = {x: number; y: number; f: number; h: number; col: string; wall: string; p: number; d: number; flat?: boolean};
  const boxes: Box[] = [];
  const addCity = (key: string, list: number[][], p: number) => {
    if (p <= 0) return;
    const e = ERA[key];
    const cen = DECO.centroid[key] || place('القاهرة الفاطمية');
    const maxD = Math.max(...list.map((h) => Math.hypot(h[0] - cen[0], h[1] - cen[1]))) || 1;
    for (let i = 0; i < list.length; i++) {
      const h = list[i];
      const ord = 0.75 * (Math.hypot(h[0] - cen[0], h[1] - cen[1]) / maxD) + 0.25 * rnd(i * 3.1 + h[0]);
      const k = sm((p * 1.35 - ord) / 0.35);
      if (k <= 0) continue;
      boxes.push({x: h[0], y: h[1], f: h[2], h: h[3] * k, col: e.roof[h[4] % e.roof.length], wall: e.wall, p: k, d: 0});
    }
  };
  for (const k of ['fustat', 'askar', 'qatai', 'fatimid', 'mamluk']) addCity(k, DECO.houses[k], pg(k, 3));
  if (modern > 0) {
    const R = 400 + modern * 9500;
    DECO.blocks.forEach((b: number[], i: number) => {
      const k = sm((R - b[5]) / 900);
      if (k <= 0) return;
      const g = 0.86 + 0.14 * rnd(i);
      boxes.push({x: b[0], y: b[1], f: b[2], h: b[3] * k, col: ['#EFE9DD', '#E2D6C2', '#D9B8A0', '#F2EEE6'][i % 4] ? shade(['#EFE9DD', '#E2D6C2', '#D7B49A', '#F2EEE6'][i % 4], g) : '#EEE', wall: '#7C7062', p: k, d: 0, flat: true});
    });
  }
  const drawn: React.ReactNode[] = [];
  const shadows: React.ReactNode[] = [];
  if (cityW > 0.01) {
    for (const b of boxes) {
      const q = pr(b.x, b.y);
      if (!onScreen(q, 60)) continue;
      b.d = q[3];
    }
    boxes.sort((a, b) => b.d - a.d);
    for (let i = 0; i < boxes.length; i++) {
      const b = boxes[i];
      const q = pr(b.x, b.y);
      if (!onScreen(q, 60)) continue;
      const hf = (b.f * (b.flat ? 0.8 : 1.35)) / 2;
      const cs = [[b.x - hf, b.y - hf], [b.x + hf, b.y - hf], [b.x + hf, b.y + hf], [b.x - hf, b.y + hf]];
      const H3 = b.h * 2.2; // heights exaggerated (Paris-timelapse look)
      const g = cs.map((p) => pr(p[0], p[1], 0));
      const tp = cs.map((p) => pr(p[0], p[1], H3));
      const sz = Math.abs(tp[1][0] - tp[0][0]);
      if (sz < 0.6) continue;
      const pts = (a: number[][]) => a.map((p) => `${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ');
      // shadow towards south-east
      const sh = cs.map((p) => pr(p[0] + H3 * 0.6, p[1] - H3 * 0.6, 0));
      shadows.push(<polygon key={'s' + i} points={pts([g[0], g[1], sh[1], sh[2], sh[3], g[3]])} fill="#3A2A14" opacity={0.18 * b.p} />);
      const faces: React.ReactNode[] = [];
      for (let j = 0; j < 4; j++) {
        const a = j, bb = (j + 1) % 4;
        const area = (g[bb][0] - g[a][0]) * (tp[a][1] - g[a][1]) - (g[bb][1] - g[a][1]) * (tp[a][0] - g[a][0]);
        if (area <= 0) continue;
        faces.push(<polygon key={j} points={pts([g[a], g[bb], tp[bb], tp[a]])} fill={j % 2 ? shade(b.wall, 0.82) : b.wall} />);
      }
      drawn.push(
        <g key={'h' + i} opacity={Math.min(1, b.p * 2)}>
          {faces}
          <polygon points={pts(tp)} fill={b.col} stroke={b.flat ? '#00000022' : '#5A3C1E55'} strokeWidth={0.8} />
        </g>,
      );
    }
  }

  // --- walls (ribbons standing up)
  const wall = (pts: XY[], p: number, hM: number, col: string, key: string, tower = true) => {
    if (p <= 0) return null;
    const P = partial(pts, p);
    const segs: React.ReactNode[] = [];
    const Hh = hM * 2.2;
    for (let i = 1; i < P.length; i++) {
      const a0 = pr(P[i - 1][0], P[i - 1][1]), b0 = pr(P[i][0], P[i][1]);
      const a1 = pr(P[i - 1][0], P[i - 1][1], Hh), b1 = pr(P[i][0], P[i][1], Hh);
      segs.push(<polygon key={i} points={`${a0[0]},${a0[1]} ${b0[0]},${b0[1]} ${b1[0]},${b1[1]} ${a1[0]},${a1[1]}`} fill={col} stroke={M.ink} strokeWidth={1.4} />);
    }
    const tops = P.map((q) => pr(q[0], q[1], Hh));
    return (
      <g key={key}>
        <path d={path(pr, P, false)} stroke="#3A2A14" strokeOpacity={0.3} strokeWidth={Math.max(2, px(40))} fill="none" transform={`translate(${px(26)},${px(18)})`} />
        {segs}
        <polyline points={tops.map((q) => `${q[0]},${q[1]}`).join(' ')} fill="none" stroke={shade(col, 1.18)} strokeWidth={Math.max(2, px(22))} strokeLinejoin="round" />
        {tower ? P.filter((_, i) => i % 2 === 0).map((q, i) => {const s = pr(q[0], q[1], Hh); return <circle key={'t' + i} cx={s[0]} cy={s[1]} r={Math.max(2.5, px(30))} fill={shade(col, 1.1)} stroke={M.ink} strokeWidth={1.4} />;}) : null}
      </g>
    );
  };
  // aqueduct: arches
  const aqueduct = (p: number) => {
    if (p <= 0) return null;
    const P = partial(orientFrom(LY['سور مجرى العيون'].pts, place('فوم الخليج')), p);
    const Hh = 22 * 2.2;
    const segs: React.ReactNode[] = [];
    for (let i = 1; i < P.length; i++) {
      const a0 = pr(P[i - 1][0], P[i - 1][1]), b0 = pr(P[i][0], P[i][1]), a1 = pr(P[i - 1][0], P[i - 1][1], Hh), b1 = pr(P[i][0], P[i][1], Hh);
      segs.push(<polygon key={i} points={`${a0[0]},${a0[1]} ${b0[0]},${b0[1]} ${b1[0]},${b1[1]} ${a1[0]},${a1[1]}`} fill="#E3D2AA" stroke={M.ink} strokeWidth={1.2} />);
      const n = Math.max(1, Math.round(Math.hypot(b0[0] - a0[0], b0[1] - a0[1]) / 10));
      for (let j = 0; j < n; j++) {
        const u = (j + 0.5) / n;
        const x = a0[0] + (b0[0] - a0[0]) * u, y = a0[1] + (b0[1] - a0[1]) * u;
        const hh = (a1[1] - a0[1]) * 0.6;
        segs.push(<rect key={i + '_' + j} x={x - 2} y={y + hh} width={4} height={-hh} fill={M.ink} opacity={0.55} />);
      }
    }
    return <g>{segs}</g>;
  };

  // --- city ground tint + HIS outline
  const cityGround = (key: string) => {
    const p = Math.max(pg(key, 3), pg('outline_' + key, 1));
    if (p <= 0) return null;
    const e = ERA[key];
    const pts = LY[POLY[key]].pts;
    const foc = pg('focus_' + key, 0.5);
    return (
      <g key={'g' + key}>
        <path d={path(pr, pts)} fill={e.tint} fillOpacity={0.28 * Math.min(1, p * 2)} />
        <path d={path(pr, partial([...pts, pts[0]], Math.min(1, p * 1.6)), false)} fill="none" stroke={e.line} strokeWidth={Math.max(3, px(26)) + foc * 5}
          strokeDasharray={foc > 0 ? `${14} ${10}` : undefined} strokeDashoffset={-f * 2} strokeLinejoin="round" />
      </g>
    );
  };

  // --- region layer (Egypt scale)
  const R = DT.region;
  const canal = (k: string, col: string) => {
    const p = pg('canal_' + k, 2.6);
    if (p <= 0) return null;
    const pts = R.canals[k].map(rw);
    const P = partial(pts, p);
    const wpx = Math.max(5, px(1600));
    const head = P[P.length - 1];
    const hq = pr(head[0], head[1]);
    return (
      <g key={k}>
        <path d={path(pr, P, false)} stroke="#fff" strokeOpacity={0.6} strokeWidth={wpx + 8} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path d={path(pr, P, false)} stroke={col} strokeWidth={wpx} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        {p < 1 ? <circle cx={hq[0]} cy={hq[1]} r={wpx * 1.4 + 4 * Math.sin(f / 3)} fill={col} opacity={0.6} /> : null}
      </g>
    );
  };
  // little sail boat moving along a canal
  const boat = (k: string) => {
    const p = pg('boat_' + k, 4);
    if (p <= 0 || p >= 1) return null;
    const P = partial(R.canals[k].map(rw), p);
    const h = P[P.length - 1];
    const q = pr(h[0], h[1]);
    return (
      <g transform={`translate(${q[0]},${q[1]})`}>
        <path d="M-26 0 L26 0 L18 12 L-18 12Z" fill="#8A5A2B" stroke={M.ink} strokeWidth={3} />
        <path d="M0 0 L0 -46 L24 -6Z" fill="#FFF6E2" stroke={M.ink} strokeWidth={3} />
      </g>
    );
  };

  // --- labels (HTML, RTL text shaped by the browser)
  const labelEls = labels.map((L, i) => {
    if (t < L.at || (L.out !== undefined && t > L.out + 0.5)) return null;
    const pos = place(L.n);
    const q = pr(pos[0], pos[1]);
    const p = spr(f, fps, L.at * fps, 200, 14);
    const o = L.out !== undefined ? 1 - lin(t, L.out, L.out + 0.4) : 1;
    if (!onScreen(q, 200)) return null;
    const size = L.big ? 54 : 40;
    const lift = (L.dy ?? 70) * Math.max(0.8, Math.min(1.25, q[2]));
    return (
      <div key={'l' + i} style={{position: 'absolute', left: q[0], top: q[1], transform: `translate(-50%, ${-lift - size}px) scale(${0.4 + 0.6 * p})`, opacity: Math.min(1, p * 1.5) * o,
        transformOrigin: '50% 100%'}}>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: size, color: L.red ? '#fff' : M.ink, background: L.red ? M.red : M.cream, padding: '2px 22px 6px',
          borderRadius: 14, border: `4px solid ${M.ink}`, whiteSpace: 'nowrap', direction: 'rtl', boxShadow: '0 8px 18px rgba(0,0,0,0.35)'}}>{L.text ?? L.n.replace(/#.*$/, '')}</div>
        <div style={{position: 'absolute', left: '50%', top: '100%', width: 5, height: lift - 10, background: M.ink, transform: 'translateX(-50%)'}} />
        <div style={{position: 'absolute', left: '50%', top: `calc(100% + ${lift - 14}px)`, width: 22, height: 22, borderRadius: 11, background: L.red ? M.red : M.ink,
          border: '4px solid #fff', transform: 'translateX(-50%)'}} />
      </div>
    );
  });

  // --- icons standing on the map
  const iconEls = icons.map((I, i) => {
    if (t < I.at || (I.out !== undefined && t > I.out + 0.5)) return null;
    const pos = place(I.n);
    const q = pr(pos[0], pos[1]);
    if (!onScreen(q, 200)) return null;
    const p = spr(f, fps, I.at * fps, 190, 12);
    const o = I.out !== undefined ? 1 - lin(t, I.out, I.out + 0.4) : 1;
    const Ic = ICON[I.i];
    const s = (I.s ?? 0.75) * Math.max(0.7, Math.min(1.3, q[2])) * p * o * Math.min(1, cityW * 1.5);
    return <g key={'i' + i} transform={`translate(${q[0]},${q[1]}) scale(${s})`}><ellipse cx={0} cy={2} rx={70} ry={14} fill="#000" opacity={0.2} /><Ic /></g>;
  });

  // --- city characters
  const ballEls = balls.map((B, i) => {
    if (t < B.at || (B.out !== undefined && t > B.out + 0.5)) return null;
    const pos = B.x !== undefined ? [B.x, B.y ?? 0] : place(B.c);
    const q = pr(pos[0], pos[1]);
    const p = spr(f, fps, B.at * fps, 160, 10);
    const o = B.out !== undefined ? 1 - lin(t, B.out, B.out + 0.4) : 1;
    const bob = Math.sin(f / 9 + i) * 6;
    const r = 62 * p * o;
    if (r < 1) return null;
    const sq = B.mood === 'squeeze' ? 1 + 0.08 * Math.sin(f / 2) : 1;
    return (
      <g key={'b' + i} transform={`translate(${q[0]},${q[1] - 120 * p + bob}) scale(${sq},${1 / sq})`}>
        <CityBall c={B.c} r={r} f={f} mood={B.mood} seed={i} />
        {B.name ? <text y={r + 50} textAnchor="middle" fontFamily={AR} fontWeight={900} fontSize={40} fill="#fff" stroke={M.ink} strokeWidth={9} paintOrder="stroke">{B.name}</text> : null}
      </g>
    );
  });

  // --- seat of power: crown hopping between seats, numbered badges, dashed trail
  let seatEls: React.ReactNode = null;
  if (seats.length) {
    const done = seats.filter((s) => t >= s.at);
    const pts = done.map((s) => place(s.n));
    let cur = pts.length ? pts[pts.length - 1] : place(seats[0].n);
    let z = 0;
    if (done.length >= 2) {
      const a = pts[pts.length - 2], b2 = pts[pts.length - 1];
      const u = Math.min(1, (t - done[done.length - 1].at) / 0.8);
      const e = Easing.inOut(Easing.cubic)(u);
      cur = [a[0] + (b2[0] - a[0]) * e, a[1] + (b2[1] - a[1]) * e];
      z = Math.sin(Math.PI * e) * Math.max(500, Math.hypot(b2[0] - a[0], b2[1] - a[1]) * 0.5);
    }
    const trail = pts.length ? [...pts.slice(0, -1), cur] : [];
    const cq = pr(cur[0], cur[1], z + 260);
    seatEls = (
      <g>
        {trail.length > 1 ? <path d={path(pr, trail, false)} stroke={M.red} strokeWidth={8} strokeDasharray="18 14" fill="none" strokeLinecap="round" /> : null}
        {done.map((s, i) => {
          const q = pr(pts[i][0], pts[i][1]);
          const p = spr(f, fps, (s.at + (i ? 0.7 : 0)) * fps, 200, 12);
          return (
            <g key={i} transform={`translate(${q[0]},${q[1]}) scale(${p})`}>
              <circle r={34} fill={i === done.length - 1 ? M.gold : '#fff'} stroke={M.ink} strokeWidth={6} />
              <text y={14} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={40} fill={M.ink}>{s.k}</text>
            </g>
          );
        })}
        {done.length ? <g transform={`translate(${cq[0]},${cq[1] + Math.sin(f / 7) * 8}) rotate(${Math.sin(f / 11) * 6})`}><Crown s={1.05} /></g> : null}
      </g>
    );
  }

  // --- HUD: year counter + era (Paris timelapse style)
  const cy0 = years.filter((y) => t >= y.at);
  let hudEl: React.ReactNode = null;
  if (cy0.length) {
    const cur = cy0[cy0.length - 1], prev = cy0.length > 1 ? cy0[cy0.length - 2] : null;
    const u = lin(t, cur.at, cur.at + 0.9);
    const val = prev ? Math.round(prev.y + (cur.y - prev.y) * u) : cur.y;
    const pop = spr(f, fps, cur.at * fps, 260, 12);
    hudEl = (
      <div style={{position: 'absolute', left: 0, right: 0, top: H * hud, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <div style={{fontFamily: EN, fontWeight: 900, fontSize: 150, color: '#fff', lineHeight: 1, letterSpacing: 4, textShadow: '0 6px 0 #2A1D12, 0 12px 30px rgba(0,0,0,0.5)',
          transform: `scale(${0.9 + 0.1 * pop})`}}>{val}<span style={{fontSize: 70, marginLeft: 10}}>{cur.suf ?? ''}</span></div>
        <div style={{marginTop: 10, fontFamily: AR, fontWeight: 900, fontSize: 50, color: '#fff', background: M.red, padding: '2px 30px 8px', borderRadius: 12,
          border: `4px solid ${M.ink}`, direction: 'rtl', opacity: lin(t, cur.at + 0.15, cur.at + 0.5), transform: `translateY(${(1 - pop) * 20}px)`}}>{cur.era}</div>
      </div>
    );
  }

  // --- hills (Mokattam): soft shaded blobs south-east of the citadel
  const hills = cityW > 0 ? [[2600, -1200, 900], [3200, -2300, 1300], [3900, -3500, 1500], [3300, -4700, 1300], [4300, -5600, 1500], [4200, -300, 800], [4800, -1400, 1200]].map((h, i) => {
    const q = pr(h[0], h[1]);
    const rx = px(h[2], q[2]);
    return <ellipse key={i} cx={q[0]} cy={q[1]} rx={rx} ry={rx * Math.cos((c.tilt * Math.PI) / 180) * 0.8} fill={i % 2 ? M.hill : '#CFB687'} opacity={0.38} />;
  }) : null;

  const fieldsW = Math.max(pg('fields', 1.5), 0) * (1 - modern);
  const focOld = pg('focus_oldnile', 0.5);
  const oldWater = oldP > 0 ? (
    <g opacity={oldP}>
      <path d={path(pr, LY['شط النيل قديما'].pts)} fill={M.water} stroke={focOld > 0 ? '#fff' : 'none'} strokeWidth={6 * focOld} strokeDasharray="18 12" strokeDashoffset={-f * 2} />
      {DECO.islands.map((r: XY[], i: number) => <path key={i} d={path(pr, r)} fill={M.water} />)}
    </g>
  ) : null;
  const khalP = pg('khalij', 2.5);
  const khal = orientFrom(LY['الخليج / شارع بورسعيد'].pts, place('فوم الخليج'));

  return (
    <AbsoluteFill style={{background: M.sea, overflow: 'hidden'}}>
      <svg width={W} height={H} style={{position: 'absolute'}}>
        {/* land (Egypt) */}
        {R.land.map((r: XY[], i: number) => <path key={'L' + i} d={path(pr, r.map(rw))} fill={M.sand} stroke={shade(M.sand, 0.85)} strokeWidth={3} />)}
        {regionW > 0 ? (
          <g opacity={regionW}>
            {Object.entries(R.rivers).map(([k, ls]: any) => ls.map((ln: XY[], j: number) => ln.length > 1 ? (
              <path key={k + j} d={path(pr, ln.map(rw), false)} stroke={k.includes('Suez') || k.includes('Ismail') ? '#5FA9CC' : M.water}
                strokeWidth={k === 'Nile' ? Math.max(5, px(1300)) : Math.max(3, px(700))} fill="none" strokeLinecap="round" strokeLinejoin="round"
                opacity={k.includes('Suez') ? 0.35 : k.includes('Ismail') ? pg('ismailia', 1.5) : 1} />
            ) : null))}
            {R.lakes.map((r: XY[], i: number) => <path key={'K' + i} d={path(pr, r.map(rw))} fill={M.water} />)}
          </g>
        ) : null}
        {/* Cairo detail */}
        <g opacity={cityW}>
          {hills}
          {modern > 0 ? (() => {
            // built-up ground under the modern blocks: grows from the old core, river is painted over it
            const R = 400 + modern * 9500, n = 48;
            const ring = Array.from({length: n}, (_, i) => {const a = (i / n) * Math.PI * 2; const r = R * (0.92 + 0.08 * Math.sin(i * 2.7)); return [300 + r * Math.cos(a), -300 + r * Math.sin(a)];});
            return <path d={path(pr, ring)} fill="#D3C8B5" opacity={0.85} />;
          })() : null}
          {fieldsW > 0 ? DECO.fields.map((fl: number[], i: number) => {
            const q = pr(fl[0], fl[1]);
            if (!onScreen(q, 80)) return null;
            const h = fl[2] / 2;
            const a = (fl[4] * Math.PI) / 180, ca = Math.cos(a), sa = Math.sin(a);
            const cs = [[-h, -h], [h, -h], [h, h], [-h, h]].map(([dx, dy]) => pr(fl[0] + dx * ca - dy * sa, fl[1] + dx * sa + dy * ca));
            return <polygon key={'F' + i} points={cs.map((p) => `${p[0]},${p[1]}`).join(' ')} fill={M.field[fl[3]]} opacity={fieldsW * 0.6} stroke="#6E8A3A" strokeWidth={0.6} />;
          }) : null}
          {oldWater}
          <path d={rivPath} fill={M.water} fillRule="evenodd" stroke={M.waterDk} strokeWidth={2} />
          <path d={rivPath} fill="none" stroke={M.waterHi} strokeWidth={1.5} opacity={0.55} transform="translate(-2,-2)" />
          {oldP > 0 && DECO.roda.length ? <path d={path(pr, DECO.roda)} fill={M.sand2} stroke={M.waterDk} strokeWidth={2} opacity={oldP} /> : null}
          {fieldsW > 0 ? DECO.palms.map((p: number[], i: number) => {
            const q = pr(p[0], p[1]);
            if (!onScreen(q, 40)) return null;
            const r = Math.max(2, px(34, q[2]));
            return <g key={'P' + i} opacity={fieldsW}><circle cx={q[0] + r * 0.5} cy={q[1] + r * 0.4} r={r} fill="#000" opacity={0.15} /><circle cx={q[0]} cy={q[1] - r * 0.6} r={r} fill={i % 3 ? M.green : '#557F31'} /></g>;
          }) : null}
          {roads > 0 ? DT.roads.map((rd: any, i: number) => <path key={'R' + i} d={path(pr, rd.pts, false)} stroke="#FFFDF5" strokeWidth={rd.k === 'm' || rd.k === 't' ? 5 : rd.k === 'p' ? 3.5 : 2}
            fill="none" opacity={roads * 0.85} strokeLinecap="round" />) : null}
          {khalP > 0 ? (
            <g>
              <path d={path(pr, partial(khal, khalP), false)} stroke={M.waterDk} strokeWidth={Math.max(6, px(70)) + 4} fill="none" strokeLinecap="round" strokeLinejoin="round" />
              <path d={path(pr, partial(khal, khalP), false)} stroke="#4FB3DD" strokeWidth={Math.max(5, px(70))} fill="none" strokeLinecap="round" strokeLinejoin="round" />
              <path d={path(pr, partial(khal, khalP), false)} stroke="#C9F0FF" strokeWidth={Math.max(2, px(20))} fill="none" strokeDasharray="10 26" strokeDashoffset={-f * 3} strokeLinecap="round" />
            </g>
          ) : null}
          {['fustat', 'askar', 'qatai', 'fatimid'].map(cityGround)}
          {shadows}
          {wall(LY['اسوار صلاح الدين2'].pts, pg('swall', 3), 14, '#B9946A', 'sw2')}
          {wall(LY['اصوار صلاح الدين'].pts, pg('swall', 3), 14, '#B9946A', 'sw1')}
          {wall([...LY['القاهرة الفاطمية'].pts, LY['القاهرة الفاطمية'].pts[0]], pg('fwall', 2.2), 16, '#D8BC8A', 'fw')}
          {pg('citadel', 1.5) > 0 ? <path d={path(pr, LY['قلعة صلاح الدين الأيوبي'].pts)} fill="#B79A6E" opacity={pg('citadel', 1.5)} /> : null}
          {wall([...LY['قلعة صلاح الدين الأيوبي'].pts, LY['قلعة صلاح الدين الأيوبي'].pts[0]], pg('citadel', 1.5), 26, '#A88456', 'cit', false)}
          {aqueduct(pg('aqueduct', 2.5))}
          {drawn}
        </g>
        {regionW > 0 ? <g opacity={regionW}>{['sesostris', 'roman', 'amr'].map((k) => canal(k, k === 'amr' ? M.red : k === 'roman' ? '#7A4FB5' : '#E08A1E'))}{['sesostris', 'amr'].map(boat)}</g> : null}
        <g opacity={cityW}>{iconEls}</g>
        {seatEls}
        {ballEls}
      </svg>
      <Img src={staticFile(`bg/grain_${Math.floor(f / 2) % 3}.png`)} style={{position: 'absolute', width: W, height: H, opacity: 0.22, mixBlendMode: 'multiply'}} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 50%, transparent 58%, rgba(40,25,10,0.45) 100%)'}} />
      {labelEls}
      {hudEl}
    </AbsoluteFill>
  );
};
