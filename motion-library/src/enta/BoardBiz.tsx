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
            {vid ? <OffthreadVideo src={staticFile(d.src)} muted startFrom={d.from ?? 0} style={{width: '100%', height: d.h || d.ar ? '100%' : undefined, objectFit: 'cover', display: 'block'}} />
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
      return wrap(<div style={{fontSize: d.size ?? 120, fontWeight: 900, color: accentOf(d.color ?? 'mustard'), textShadow: '0 8px 0 rgba(0,0,0,.35)', whiteSpace: 'nowrap', direction: 'ltr'}}>{txt}</div>, 0);
    }
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
