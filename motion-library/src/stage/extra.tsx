import React from 'react';
import {Easing, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {GEO, lonLat, MapPaths} from '../blocks/geo';
import {AR, bi, EN, L, lin, S, spr, W} from './kit';

// Review 2026-10-19 scenes: the REAL thing he talks about (pictures, thumbnails + QR, a moving map) and explaining motion
// (pixels vs vectors, video = frames). Stage box coords; beats b = seconds from the cue start.
const bt = (b: Record<string, number> | undefined, k: string, fps: number, d = 0) => Math.round((b?.[k] ?? d) * fps);
const out = (f: number, dur: number) => 1 - lin(f, dur - 7, dur);
const M = (f: string) => staticFile(`projects/newstage19/media/${f}`);

// ---------- Pic: one picture, optional zoom from one focus to another (z0 -> z1 between beats 'z0' and 'z1') ----------
// focus = [x%, y%, scale]
export const Pic: React.FC<{dur: number; file: string; w?: number; h?: number; fit?: 'cover' | 'contain'; label?: string; from?: number[]; to?: number[];
  b?: Record<string, number>; bg?: string}> = ({dur, file, w = 960, h = 600, fit = 'cover', label, from = [50, 50, 1], to, b, bg = '#000'}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 150, 15);
  const k0 = bt(b, 'z0', fps, 0), k1 = bt(b, 'z1', fps, dur / fps - 0.4);
  const e = to ? lin(f, k0, k1, 0, 1, Easing.inOut(Easing.cubic)) : f / Math.max(1, dur) * 0.3;
  const fx = to ? from[0] + (to[0] - from[0]) * e : from[0], fy = to ? from[1] + (to[1] - from[1]) * e : from[1];
  const sc = to ? from[2] + (to[2] - from[2]) * e : from[2] * (1 + 0.05 * e);
  return (
    <div style={{position: 'absolute', left: (W - w) / 2, top: L.stageTop + (830 - h) / 2 - 40, width: w, height: h, borderRadius: 30, overflow: 'hidden', background: bg,
      opacity: Math.min(1, p * 1.5) * out(f, dur), transform: `scale(${0.85 + 0.15 * p})`, boxShadow: '0 40px 80px rgba(0,0,0,0.55)', border: '2px solid rgba(255,255,255,0.14)'}}>
      <Img src={M(file)} style={{width: '100%', height: '100%', objectFit: fit, transform: `scale(${sc})`, transformOrigin: `${fx}% ${fy}%`}} />
      {label ? <div style={{position: 'absolute', left: 16, bottom: 14, padding: '2px 16px', borderRadius: 12, background: 'rgba(0,0,0,0.7)', fontFamily: AR, fontWeight: 800, fontSize: 30,
        color: '#fff', direction: 'rtl'}}>{bi(label)}</div> : null}
    </div>
  );
};

// ---------- Pics: a row/grid of pictures popping on beats p0, p1, ... ----------
export const Pics: React.FC<{dur: number; items: {file: string; t?: string}[]; size?: number; cols?: number; round?: boolean; title?: string; b?: Record<string, number>}> = (
  {dur, items, size = 220, cols = 5, round = false, title, b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <div style={{position: 'absolute', left: 30, right: 30, top: L.stageTop + 40, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 20, opacity: out(f, dur)}}>
      {title ? <div style={{fontFamily: AR, fontWeight: 900, fontSize: 56, color: S.yellow, direction: 'rtl'}}>{bi(title)}</div> : null}
      <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 18, maxWidth: cols * (size + 18), direction: 'rtl'}}>
        {items.map((it, i) => {
          const k = bt(b, `p${i}`, fps, 0.2 + i * 0.4);
          const q = spr(f, fps, k, 220, 12);
          return (
            <div key={i} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6, opacity: Math.min(1, q * 1.6), transform: `scale(${0.4 + 0.6 * q}) rotate(${(1 - q) * -12}deg)`}}>
              <div style={{width: size, height: size, borderRadius: round ? size / 2 : 26, overflow: 'hidden', background: '#fff', boxShadow: '0 16px 30px rgba(0,0,0,0.45)'}}>
                <Img src={M(it.file)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></div>
              {it.t ? <div style={{fontFamily: AR, fontWeight: 900, fontSize: 36, color: '#fff'}}>{bi(it.t)}</div> : null}
            </div>
          );
        })}
      </div>
    </div>
  );
};

// ---------- Thumbs: his YouTube videos / a playlist as thumbnails (+ QR), marks circle some of them ----------
export const Thumbs: React.FC<{dur: number; items: {file: string; t?: string; mark?: boolean}[]; qr?: string; title?: string; cols?: number; b?: Record<string, number>}> = (
  {dur, items, qr, title, cols = 2, b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const tw = cols === 2 ? 420 : 300;
  const km = bt(b, 'mark', fps, 1.5);
  return (
    <div style={{position: 'absolute', left: 30, right: 30, top: L.stageTop - 10, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14, opacity: out(f, dur)}}>
      {title ? <div style={{fontFamily: AR, fontWeight: 900, fontSize: 48, color: S.yellow, direction: 'rtl', textAlign: 'center'}}>{bi(title)}</div> : null}
      <div style={{display: 'flex', gap: 22, alignItems: 'center', direction: 'rtl'}}>
        <div style={{display: 'grid', gridTemplateColumns: `repeat(${cols}, ${tw}px)`, gap: 14}}>
          {items.map((it, i) => {
            const q = spr(f, fps, 3 + i * 3, 200, 14);
            const m = it.mark && f >= km ? spr(f, fps, km + i * 4, 220, 12) : 0;
            return (
              <div key={i} style={{position: 'relative', opacity: q, transform: `translateY(${(1 - q) * 30}px)`}}>
                <Img src={M(it.file)} style={{width: tw, height: tw * 9 / 16, objectFit: 'cover', borderRadius: 14, display: 'block', boxShadow: '0 10px 24px rgba(0,0,0,0.45)'}} />
                {it.t ? <div style={{fontFamily: AR, fontWeight: 800, fontSize: 24, color: '#fff', marginTop: 4, direction: 'rtl', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', width: tw}}>{bi(it.t)}</div> : null}
                {m > 0 ? <svg width={tw + 40} height={tw * 9 / 16 + 40} style={{position: 'absolute', left: -20, top: -20}}>
                  <ellipse cx={(tw + 40) / 2} cy={(tw * 9 / 16 + 40) / 2} rx={(tw + 20) / 2} ry={(tw * 9 / 16 + 20) / 2} fill="none" stroke={S.red} strokeWidth={8}
                    strokeDasharray={2000} strokeDashoffset={2000 * (1 - m)} strokeLinecap="round" /></svg> : null}
              </div>
            );
          })}
        </div>
        {qr ? <div style={{background: '#fff', padding: 12, borderRadius: 18, opacity: spr(f, fps, 10, 200, 14)}}><Img src={M(qr)} style={{width: 220, height: 220, display: 'block'}} /></div> : null}
      </div>
    </div>
  );
};

// ---------- MapTour: ONE world map; the camera flies Egypt -> Germany -> USA (beats s0, s1, s2), each country lights up ----------
const STOPS: Record<string, {lon: number; lat: number; t: string}> = {EGY: {lon: 30, lat: 27, t: 'مصر'}, DEU: {lon: 10.4, lat: 51, t: 'ألمانيا'}, USA: {lon: -98, lat: 39, t: 'أمريكا'}};
export const MapTour: React.FC<{dur: number; stops?: string[]; b?: Record<string, number>}> = ({dur, stops = ['EGY', 'DEU', 'USA'], b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ks = stops.map((s, i) => bt(b, `s${i}`, fps, 0.3 + i * 2));
  let i = 0;
  ks.forEach((k, j) => { if (f >= k - 12) i = j; });
  const prev = Math.max(0, i - 1);
  const e = lin(f, ks[i] - 12, ks[i] + 6, 0, 1, Easing.inOut(Easing.cubic));
  const [ax, ay] = lonLat(STOPS[stops[prev]].lon, STOPS[stops[prev]].lat), [bx, by] = lonLat(STOPS[stops[i]].lon, STOPS[stops[i]].lat);
  const mid = i > 0 ? Math.sin(e * Math.PI) : 0; // zoom out a bit while flying
  const cx = ax + (bx - ax) * e, cy = ay + (by - ay) * e;
  const z = 4.2 - 2.4 * mid;
  const VW = 960, VH = 640;
  const vbW = GEO.w / z * (VW / 960) * 0.55, vbH = vbW * VH / VW;
  const lit = (iso: string) => stops.indexOf(iso) >= 0 && stops.indexOf(iso) <= i && f >= ks[stops.indexOf(iso)] - 4;
  return (
    <div style={{position: 'absolute', left: (W - VW) / 2, top: L.stageTop, width: VW, height: VH, borderRadius: 34, overflow: 'hidden', opacity: out(f, dur) * Math.min(1, f / 6),
      background: 'radial-gradient(circle at 50% 40%, #12305A 0%, #0A1630 80%)', boxShadow: '0 30px 60px rgba(0,0,0,0.5)', border: '2px solid rgba(255,255,255,0.14)'}}>
      <svg width={VW} height={VH} viewBox={`${cx - vbW / 2} ${cy - vbH / 2} ${vbW} ${vbH}`}>
        <MapPaths style={(iso) => ({fill: lit(iso) ? (iso === stops[i] ? S.yellow : '#E9B949') : '#2C4E7E', stroke: '#0A1630', strokeWidth: 1.2 / z * 2})} />
        {/* the flight path so far */}
        {stops.slice(0, i + 1).map((s, j) => {
          if (j === 0) return null;
          const [x0, y0] = lonLat(STOPS[stops[j - 1]].lon, STOPS[stops[j - 1]].lat), [x1, y1] = lonLat(STOPS[s].lon, STOPS[s].lat);
          const pr = j < i ? 1 : e;
          const mx = (x0 + x1) / 2, my = Math.min(y0, y1) - Math.abs(x1 - x0) * 0.25;
          return <path key={j} d={`M${x0} ${y0} Q${mx} ${my} ${x1} ${y1}`} fill="none" stroke="#fff" strokeWidth={6 / z * 2} strokeDasharray={`${14 / z * 2} ${10 / z * 2}`}
            pathLength={1} style={{strokeDasharray: 1, strokeDashoffset: 1 - pr}} />;
        })}
        {stops.slice(0, i + 1).map((s) => { const [x, y] = lonLat(STOPS[s].lon, STOPS[s].lat); return <circle key={s} cx={x} cy={y} r={9 / z * 2} fill={S.red} stroke="#fff" strokeWidth={3 / z * 2} />; })}
      </svg>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 22, display: 'flex', justifyContent: 'center'}}>
        <span style={{fontFamily: AR, fontWeight: 900, fontSize: 66, color: S.ink, background: S.yellow, padding: '0 26px 8px', borderRadius: 18,
          transform: `scale(${0.8 + 0.2 * spr(f, fps, ks[i], 240, 12)})`}}>{STOPS[stops[i]].t}</span>
      </div>
    </div>
  );
};

// ---------- PixVec: the same circle as Pixels (blocky when you zoom) vs Vector (always smooth: points + curves) ----------
export const PixVec: React.FC<{dur: number; b?: Record<string, number>}> = ({dur, b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const kz = bt(b, 'zoom', fps, 1.2);
  const z = 1 + 5 * lin(f, kz, kz + 40, 0, 1, Easing.inOut(Easing.cubic));
  const N = 24, cell = 380 / N;
  const panel = (vec: boolean, x: number) => {
    const q = spr(f, fps, vec ? 8 : 0, 200, 14);
    return (
      <div style={{position: 'absolute', left: x, top: L.stageTop + 20, width: 440, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12, opacity: q}}>
        <div style={{width: 440, height: 440, borderRadius: 30, overflow: 'hidden', background: '#F4F6FB', position: 'relative'}}>
          <svg width={440} height={440} viewBox={`${220 - 220 / z + 70 * (z - 1) / z} ${220 - 220 / z - 60 * (z - 1) / z} ${440 / z} ${440 / z}`} shapeRendering={vec ? 'geometricPrecision' : 'crispEdges'}>
            {vec ? <>
              <circle cx={220} cy={220} r={160} fill={S.blue} />
              {[[220, 60], [380, 220], [220, 380], [60, 220]].map(([px, py], i) => <rect key={i} x={px - 6} y={py - 6} width={12} height={12} fill="#fff" stroke={S.ink} strokeWidth={2} />)}
              <path d="M220 60 L310 60 M220 60 L130 60" stroke={S.ink} strokeWidth={2} />
            </> : Array.from({length: N * N}).map((_, i) => {
              const gx = i % N, gy = Math.floor(i / N);
              const cxp = 30 + (gx + 0.5) * cell, cyp = 30 + (gy + 0.5) * cell;
              const inside = Math.hypot(cxp - 220, cyp - 220) <= 160;
              return inside ? <rect key={i} x={30 + gx * cell} y={30 + gy * cell} width={cell} height={cell} fill={S.blue} /> : null;
            })}
            {!vec && z > 3 ? Array.from({length: N + 1}).map((_, i) => <g key={i}><line x1={30 + i * cell} y1={30} x2={30 + i * cell} y2={410} stroke="#0002" strokeWidth={0.6} />
              <line x1={30} y1={30 + i * cell} x2={410} y2={30 + i * cell} stroke="#0002" strokeWidth={0.6} /></g>) : null}
          </svg>
          {f >= kz ? <div style={{position: 'absolute', right: 12, top: 10, fontFamily: EN, fontWeight: 900, fontSize: 30, color: S.ink}}>🔍 ×{z.toFixed(0)}</div> : null}
        </div>
        <div style={{fontFamily: EN, fontWeight: 900, fontSize: 52, color: vec ? S.green : S.red}}>{vec ? 'Vector' : 'Pixels'}</div>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 34, color: '#fff', direction: 'rtl'}}>{vec ? 'نقط ومنحنيات.. مش بتبكسل' : 'مربعات صغيرة.. بتبكسل'}</div>
      </div>
    );
  };
  return <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 1920, opacity: out(f, dur)}}>{panel(false, 570)}{panel(true, 70)}</div>;
};

// ---------- Flipbook: video = many pictures in a row (a runner's frames, then they play) ----------
const runner = (k: number) => {
  const a = Math.sin(k / 6 * Math.PI * 2), c = Math.cos(k / 6 * Math.PI * 2);
  return `M50 22 L50 58 M50 34 L${50 + 18 * a} ${46 - 4 * c} M50 34 L${50 - 18 * a} ${46 + 4 * c} M50 58 L${50 + 16 * a} ${80 - 6 * Math.abs(c)} M50 58 L${50 - 16 * a} ${80 - 6 * Math.abs(a)}`;
};
export const Flipbook: React.FC<{dur: number; b?: Record<string, number>}> = ({dur, b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const kp = bt(b, 'play', fps, 1.2);
  const k = f >= kp ? Math.floor((f - kp) / 3) % 6 : -1;
  return (
    <div style={{position: 'absolute', left: 0, top: L.stageTop + 20, width: W, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 24, opacity: out(f, dur)}}>
      <div style={{display: 'flex', gap: 10, direction: 'ltr'}}>
        {Array.from({length: 6}).map((_, i) => {
          const q = spr(f, fps, i * 3, 220, 14);
          return <svg key={i} width={140} height={140} viewBox="0 0 100 100" style={{background: '#F4F6FB', borderRadius: 14, opacity: q, outline: k === i ? `5px solid ${S.yellow}` : undefined}}>
            <circle cx={50} cy={14} r={8} fill={S.ink} /><path d={runner(i)} stroke={S.ink} strokeWidth={6} strokeLinecap="round" fill="none" /></svg>;
        })}
      </div>
      <div style={{fontFamily: EN, fontWeight: 900, fontSize: 40, color: S.soft}}>{f >= kp ? '▶ 1 2 3 4 5 6 1 2 3 …' : '6 صور'}</div>
      <svg width={300} height={300} viewBox="0 0 100 100" style={{background: '#F4F6FB', borderRadius: 26, opacity: lin(f, kp - 4, kp + 4)}}>
        <circle cx={50} cy={14} r={8} fill={S.ink} /><path d={runner(Math.max(0, k))} stroke={S.ink} strokeWidth={6} strokeLinecap="round" fill="none" /></svg>
      <div style={{fontFamily: AR, fontWeight: 900, fontSize: 52, color: '#fff', direction: 'rtl'}}>فيديو = صور ورا بعض بسرعة</div>
    </div>
  );
};
