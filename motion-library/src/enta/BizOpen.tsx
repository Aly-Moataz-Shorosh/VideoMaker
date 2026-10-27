import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {enter, lerp} from '../blocks/anim';
import {MeetBg} from './Meet';
import {GEO, rings} from '../blocks/geo';
import cairo from '../cairo/data.json';
import {E, Hi, Sticker, Tape, accentOf, stickerBorder} from './kit';

// Opening of رواد الأعمال ep01 (Karim Tamer, 2026-10-27). In the recording Aly's camera was a tiny Meet self-view (139x124 px)
// while he introduced the department and the guest (0:17-2:03). Aly: "make me the one on screen, but don't blow the picture up
// until it pixelates; cover it with a lot of motion graphics + Blender". So this is ONE full-screen board for that stretch:
//   - his self-view, pre-cut and scaled 3.2x with lanczos (work/scripts/aly_open.sh), shown at most at that size inside an
//     ON-AIR TV sticker frame (scanlines + white border hide the softness): hero (centre) -> left (beside the scenes) -> mini
//   - layers on his words: Blender clips (tools/blender/biz_scenes.py, transparent webm, subject on the right two thirds),
//     headlines, chips, taped pictures, stickers, big numbers, an X stamp.
// All times = frames from the cue start (30 fps).

const pt = z.object({at: z.number(), m: z.enum(['hero', 'left', 'mini', 'off'])});
const layer = z.object({
  k: z.enum(['clip', 'head', 'chips', 'pics', 'stk', 'xmark', 'big', 'phone', 'map', 'flavours']),
  at: z.number(), dur: z.number(),
  file: z.string().optional(), rate: z.number().optional(),
  text: z.string().optional(), sub: z.string().optional(), x: z.number().optional(), y: z.number().optional(), size: z.number().optional(),
  accent: z.string().optional(), rot: z.number().optional(), name: z.string().optional(),
  items: z.array(z.record(z.string(), z.any())).optional(),
  zoomAt: z.number().optional(), pinAt: z.number().optional(), sel: z.number().optional(), selAt: z.number().optional(),
});
export const bizOpenSchema = z.object({
  aly: z.string().default('projects/entabiz01/aly_open.mp4'),
  alyW: z.number().default(480), alyH: z.number().default(306), // size of the pre-scaled clip = the biggest it is ever shown
  name: z.string().default('علي معتز شُرُش'),
  cam: z.array(pt).default([{at: 0, m: 'hero'}]),
  // the guest behind a theatre curtain (Aly 2026-10-27: "حط الكدر بتاع كريم في مكان بس عليه ستارة… والستارة تتفتح")
  guest: z.object({src: z.string(), from: z.number().default(0), label: z.string().default('ضيف الحلقة'), name: z.string().default(''),
    openAt: z.number(), pos: z.array(z.object({at: z.number(), m: z.enum(['corner', 'big', 'side', 'off'])}))}).nullable().default(null),
  layers: z.array(layer).default([]),
  previewBg: z.string().default(''),
});
type L = z.infer<typeof layer>;

const sm = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const life = (f: number, l: {at: number; dur: number}, out = 8) => Math.min(1, Math.max(0, (l.at + l.dur - f) / out));

// the camera frame position per mode (centre x, centre y, scale of the pre-scaled clip)
const POS: Record<string, [number, number, number]> = {hero: [960, 500, 1.12], left: [295, 520, 1.0], mini: [190, 170, 0.5], off: [-300, 560, 0.6]};

// guest frame positions: [centre x, centre y, width] (16:9)
const GPOS: Record<string, [number, number, number]> = {corner: [1660, 170, 380], big: [1230, 470, 860], side: [1500, 300, 560], off: [2300, 170, 380]};

// red velvet curtain over the guest's frame: two halves with folds that slide apart (and bunch up) at openAt
const Curtain: React.FC<{k: number; w: number; h: number}> = ({k, w, h}) => {
  const half = (left: boolean) => {
    const cw = (w / 2) * (1 - 0.82 * k);
    const folds = 'repeating-linear-gradient(90deg, #7d1414 0px, #b3261e ' + (w / 28) + 'px, #8e1a17 ' + (w / 14) + 'px)';
    return (
      <div style={{position: 'absolute', top: 0, [left ? 'left' : 'right']: 0, width: cw, height: h, background: folds, boxShadow: `inset ${left ? -18 : 18}px 0 30px rgba(0,0,0,.45)`,
        borderBottomLeftRadius: left ? 0 : 30 * k, borderBottomRightRadius: left ? 30 * k : 0}}>
        <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(255,220,160,.18), transparent 30%, rgba(0,0,0,.35))'}} />
      </div>
    );
  };
  return (
    <AbsoluteFill>
      {half(true)}{half(false)}
      {/* pelmet (valance) with gold fringe */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: h * 0.13, background: 'linear-gradient(180deg, #a51f1a, #6e1210)', borderBottom: `${Math.max(4, h * 0.02)}px dotted ${E.mustard}`,
        boxShadow: '0 8px 16px rgba(0,0,0,.4)'}} />
    </AbsoluteFill>
  );
};

const Guest: React.FC<{g: NonNullable<z.infer<typeof bizOpenSchema>['guest']>}> = ({g}) => {
  const f = useCurrentFrame();
  let i = 0;
  while (i + 1 < g.pos.length && g.pos[i + 1].at <= f) i++;
  const cur = g.pos[i], prev = i ? g.pos[i - 1] : cur;
  const k = sm((f - cur.at) / 18);
  const a = GPOS[prev.m], b = GPOS[cur.m];
  const x = lerp(k, a[0], b[0]), y = lerp(k, a[1], b[1]), w = lerp(k, a[2], b[2]), h = (w * 800) / 1582; // his whole Meet tile, its own shape (no crop)
  const open = sm((f - g.openAt) / 22);
  const pop = enter(f, 30, g.pos[0].at);
  const shake = f < g.openAt && f > g.openAt - 20 ? Math.sin(f * 2.2) * 3 : 0; // the curtain trembles just before it opens
  return (
    <div style={{position: 'absolute', left: x - w / 2, top: y - h / 2, width: w, height: h, transform: `scale(${pop}) rotate(${1.5 + shake * 0.2}deg)`}}>
      <div style={{position: 'absolute', inset: 0, borderRadius: 16, overflow: 'hidden', ...stickerBorder(Math.max(5, w / 70)), background: '#140c0c'}}>
        {open > 0 ? <OffthreadVideo src={staticFile(g.src)} muted startFrom={g.from} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover'}} /> : null}
        <Curtain k={open} w={w} h={h} />
        {open < 0.5 ? (
          <div style={{position: 'absolute', left: '50%', top: '58%', transform: `translate(-50%, -50%) scale(${1 - open * 2})`, background: E.paper, color: E.ink, fontWeight: 900,
            fontSize: w / 13, padding: '4px 20px', borderRadius: 8, whiteSpace: 'nowrap', direction: 'rtl', ...stickerBorder(4)}}>
            {g.label} <span style={{color: E.orange}}>؟</span>
          </div>
        ) : null}
      </div>
      {g.name && open > 0.6 ? (
        <div style={{position: 'absolute', left: '50%', bottom: -38 - w / 40, transform: `translateX(-50%) rotate(-2deg) scale(${enter(f, 30, g.openAt + 14)})`, background: E.orange, color: E.ink,
          fontWeight: 900, fontSize: w / 16 + 6, padding: '4px 22px', borderRadius: 8, whiteSpace: 'nowrap', direction: 'rtl', ...stickerBorder(5)}}>{g.name}</div>
      ) : null}
    </div>
  );
};

const AlyCam: React.FC<{src: string; w: number; h: number; name: string; cam: z.infer<typeof pt>[]}> = ({src, w, h, name, cam}) => {
  const f = useCurrentFrame();
  let i = 0;
  while (i + 1 < cam.length && cam[i + 1].at <= f) i++;
  const cur = cam[i], prev = i ? cam[i - 1] : cur;
  const k = sm((f - cur.at) / 18);
  const a = POS[prev.m], b = POS[cur.m];
  const x = lerp(k, a[0], b[0]), y = lerp(k, a[1], b[1]), s = lerp(k, a[2], b[2]);
  const pop = enter(f, 30, 2);
  const W = w * s, H = h * s;
  const showName = cur.m !== 'mini' && cur.m !== 'off';
  return (
    <div style={{position: 'absolute', left: x - W / 2, top: y - H / 2, width: W, height: H, transform: `scale(${pop}) rotate(${lerp(k, -1.5, -1.5)}deg)`}}>
      <div style={{position: 'absolute', inset: 0, borderRadius: 22 * s + 6, overflow: 'hidden', ...stickerBorder(Math.max(5, 9 * s)), background: '#111'}}>
        <OffthreadVideo src={staticFile(src)} muted style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover'}} />
        {/* TV feel: fine scanlines + soft vignette (also hides the upscale softness) */}
        <AbsoluteFill style={{background: 'repeating-linear-gradient(0deg, rgba(0,0,0,.13) 0 2px, transparent 2px 4px)', mixBlendMode: 'multiply'}} />
        <AbsoluteFill style={{background: 'radial-gradient(ellipse 75% 75% at 50% 45%, transparent 60%, rgba(0,0,0,.42))'}} />
      </div>
      <div style={{position: 'absolute', right: -26 * s, top: -40 * s, transform: `rotate(8deg) scale(${enter(f, 30, 10)})`}}><Sticker name="onair" size={150 * s + 30} /></div>
      {showName ? (
        <div style={{position: 'absolute', left: '50%', bottom: -34 * s - 14, transform: `translateX(-50%) rotate(-2deg) scale(${enter(f, 30, 16)})`, background: E.paper, color: E.ink,
          fontWeight: 900, fontSize: 30 * s + 6, padding: '6px 22px', borderRadius: 8, whiteSpace: 'nowrap', ...stickerBorder(5), direction: 'rtl'}}>
          {name}
          <Tape w={90} rot={-8} style={{top: -18, left: -30}} />
        </div>
      ) : null}
    </div>
  );
};

const Head: React.FC<{l: L; f: number}> = ({l, f}) => {
  const p = enter(f, 30, l.at), o = life(f, l);
  const acc = accentOf(l.accent ?? 'mustard');
  return (
    <div style={{position: 'absolute', left: l.x ?? 1240, top: l.y ?? 110, transform: `translate(-50%, -50%) translateY(${lerp(p, 30, 0)}px) rotate(${l.rot ?? -1.5}deg) scale(${lerp(p, 0.7, 1)})`,
      opacity: Math.min(1, p * 1.5) * o, direction: 'rtl', textAlign: 'center'}}>
      <div style={{background: E.paper, color: E.ink, fontWeight: 900, fontSize: l.size ?? 62, padding: '10px 34px 14px', borderRadius: 12, whiteSpace: 'nowrap', ...stickerBorder(8)}}>
        <Hi text={l.text ?? ''} color={E.orange} />
      </div>
      {l.sub ? <div style={{marginTop: 14, fontSize: (l.size ?? 62) * 0.55, fontWeight: 800, color: acc, textShadow: '0 4px 12px rgba(0,0,0,.6)', whiteSpace: 'nowrap'}}><Hi text={l.sub} color={E.white} /></div> : null}
    </div>
  );
};

const Chips: React.FC<{l: L; f: number}> = ({l, f}) => {
  const o = life(f, l);
  return (
    <div style={{position: 'absolute', left: l.x ?? 1240, top: l.y ?? 300, transform: 'translateX(-50%)', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 18, opacity: o, direction: 'rtl'}}>
      {(l.items ?? []).map((it, i) => {
        const at = l.at + (it.at ?? i * 12);
        if (f < at) return <div key={i} style={{height: 0}} />;
        const p = enter(f, 30, at);
        const acc = accentOf(it.accent ?? ['orange', 'blue', 'olive', 'mustard'][i % 4]);
        return (
          <div key={i} style={{display: 'flex', alignItems: 'center', gap: 14, background: acc, color: E.ink, fontWeight: 900, fontSize: it.size ?? 44, padding: '8px 30px',
            borderRadius: 50, border: `5px solid ${E.white}`, boxShadow: '0 10px 22px rgba(0,0,0,.45)', whiteSpace: 'nowrap',
            transform: `translateX(${lerp(p, 80, 0)}px) scale(${lerp(p, 0.6, 1)}) rotate(${(i % 2 ? 1.5 : -1.5)}deg)`, opacity: Math.min(1, p * 1.6)}}>
            {it.emo ? <Img src={staticFile(`fluent/${it.emo}.png`)} style={{width: (it.size ?? 44) * 1.25, height: (it.size ?? 44) * 1.25}} /> : null}
            <Hi text={it.text} color={E.white} />
          </div>
        );
      })}
    </div>
  );
};

const Pics: React.FC<{l: L; f: number}> = ({l, f}) => {
  const o = life(f, l);
  return (
    <>
      {(l.items ?? []).map((it, i) => {
        const at = l.at + (it.at ?? i * 8);
        if (f < at) return null;
        if (it.out !== undefined && f >= l.at + it.out) return null; // an item can hand over to the next one at the same spot
        const p = it.cut ? 1 : enter(f, 30, at);
        const bare = !!it.bare;
        return (
          <div key={i} style={{position: 'absolute', left: it.x, top: it.y, width: it.w, transform: `translate(-50%, -50%) translateY(${lerp(p, 60, 0)}px) rotate(${(it.rot ?? 0) * p + (1 - p) * 10}deg) scale(${lerp(p, 0.5, 1)})`,
            opacity: Math.min(1, p * 1.6) * o}}>
            <div style={{position: 'relative', borderRadius: bare ? 0 : 10, overflow: 'hidden', ...(bare ? {} : stickerBorder(8)), background: bare ? 'transparent' : '#fff'}}>
              {String(it.src).endsWith('.mp4') || String(it.src).endsWith('.webm')
                ? <Sequence from={at} layout="none"><OffthreadVideo src={staticFile(it.src)} muted startFrom={it.from ?? 0} style={{width: '100%', display: 'block'}} /></Sequence>
                : <Img src={staticFile(it.src)} style={{width: '100%', display: 'block'}} />}
            </div>
            {bare ? null : <Tape w={Math.min(140, it.w * 0.35)} rot={-6} style={{top: -20, left: it.w / 2 - Math.min(70, it.w * 0.17)}} />}
            {it.cap ? <div style={{position: 'absolute', left: '50%', bottom: -54, transform: 'translateX(-50%) rotate(-2deg)', background: E.ink, color: E.white, fontWeight: 900,
              fontSize: 32, padding: '4px 18px', borderRadius: 8, whiteSpace: 'nowrap', border: `3px solid ${E.white}`, direction: 'rtl'}}><Hi text={it.cap} color={E.mustard} /></div> : null}
          </div>
        );
      })}
    </>
  );
};

// phone mockup: posts slide up one after the other (Instagram feel)
const Phone: React.FC<{l: L; f: number}> = ({l, f}) => {
  const p = enter(f, 30, l.at), o = life(f, l);
  const items = l.items ?? [];
  const per = Math.max(20, (l.dur - 20) / Math.max(1, items.length));
  const t = Math.max(0, (f - l.at - 10) / per), base = Math.min(items.length - 1, Math.floor(t));
  const off = Math.max(0, base - 1 + sm(((t - base) * per) / 12)); // scroll position in posts (slides up 12 frames at each new post)
  const W = l.size ?? 380, H = W * 2.05, inner = W - 28;
  return (
    <div style={{position: 'absolute', left: l.x ?? 1300, top: l.y ?? 560, width: W, height: H, transform: `translate(-50%, -50%) translateY(${lerp(p, 200, 0)}px) rotate(${l.rot ?? 4}deg)`,
      opacity: Math.min(1, p * 1.5) * o}}>
      <div style={{position: 'absolute', inset: 0, background: '#0d0f14', borderRadius: W * 0.14, border: '6px solid #2a2e38', boxShadow: '0 30px 60px rgba(0,0,0,.6)', overflow: 'hidden'}}>
        <div style={{position: 'absolute', top: 18, left: '50%', transform: 'translateX(-50%)', width: W * 0.3, height: 22, borderRadius: 12, background: '#000'}} />
        {l.text ? <div style={{position: 'absolute', top: 54, left: 0, right: 0, textAlign: 'center', color: '#fff', fontWeight: 800, fontSize: 24, fontFamily: 'Arial'}}>{l.text}</div> : null}
        <div style={{position: 'absolute', left: 14, top: 96, width: inner, height: H - 130, overflow: 'hidden', borderRadius: 10}}>
          {items.map((it, i) => (
            <Img key={i} src={staticFile(it.src)} style={{position: 'absolute', left: 0, top: (i - off) * (inner + 12), width: inner, height: inner, objectFit: 'cover', borderRadius: 6}} />
          ))}
        </div>
      </div>
    </div>
  );
};


// Map (Aly 2026-10-27: "حاجة تعبر إنه خريج GUC اللي في التجمع… اعمل خريطة"): Egypt (Natural Earth) -> the camera dives into Cairo
// (today's Nile from OSM, the cairohistory data) -> a pin drops on the German University in Cairo, New Cairo
// (29.988 N, 31.442 E — Wikidata Q691097). One SVG in world map units (10 units / degree), the viewBox flies (log zoom).
const NILE_EG: number[][] = [[32.9, 24.09], [32.88, 24.9], [32.64, 25.69], [32.2, 26.2], [31.65, 26.6], [31.18, 27.18], [30.75, 28.1], [30.95, 28.7], [31.1, 29.07],
  [31.22, 29.6], [31.24, 30.05], [31.2, 30.25]];
const DELTA: number[][][] = [[[31.2, 30.25], [30.9, 30.8], [30.55, 31.2], [30.42, 31.46]], [[31.2, 30.25], [31.35, 30.8], [31.6, 31.15], [31.81, 31.42]]];
const W2 = (lon: number, lat: number) => [((lon + 180) / 360) * GEO.w, ((90 - lat) / 180) * GEO.h];
const C0 = (cairo as any).center as number[];
const m2w = (p: number[]) => W2(C0[0] + p[0] / 96350, C0[1] + p[1] / 110574); // cairo data metres -> world units
const GUC = W2(31.442, 29.988), CAI = W2(31.245, 30.05);
const BizMap: React.FC<{l: L; f: number}> = ({l, f}) => {
  const t = f - l.at, o = life(f, l, 12), zIn = l.zoomAt ?? 36, pinAt = l.pinAt ?? 62;
  const k = sm((t - zIn) / 34);
  // viewBox: Egypt -> greater Cairo (log interpolation of the size so the dive feels constant)
  const eg = {cx: W2(30.6, 26.9)[0], cy: W2(30.6, 26.9)[1], w: 150}, ca = {cx: (CAI[0] + GUC[0]) / 2 + 0.02, cy: (CAI[1] + GUC[1]) / 2 + 0.01, w: 4.2};
  const w = Math.exp(Math.log(eg.w) + (Math.log(ca.w) - Math.log(eg.w)) * k), h = (w * 9) / 16;
  const cx = eg.cx + (ca.cx - eg.cx) * k, cy = eg.cy + (ca.cy - eg.cy) * k;
  const px = w / 1920; // one screen pixel in world units
  const egy = rings('EGY').map((r) => 'M' + r.map((q) => q.join(',')).join('L') + 'Z').join('');
  const path = (pts: number[][]) => 'M' + pts.map((q) => q.join(',')).join('L');
  const nile = ((cairo as any).nile as number[][][]).map((r) => path(r.map(m2w))).join('');
  // today's main roads (OSM, the cairohistory data): motorways/trunks thicker — only once we are over Cairo
  const roads = ((cairo as any).roads as {k: string; pts: number[][]}[]);
  const big = roads.filter((r) => r.k === 'm' || r.k === 't').map((r) => path(r.pts.map(m2w))).join('');
  const mid = roads.filter((r) => r.k === 'p').map((r) => path(r.pts.map(m2w))).join('');
  const pin = t >= pinAt ? enter(f, 30, l.at + pinAt) : 0;
  const ring = ((t - pinAt) % 40) / 40;
  const lab = (x: number, y: number, text: string, size: number, col = E.ink, bg = E.paper, show = 1) => show > 0.01 ? (
    <g transform={`translate(${x} ${y}) scale(${px})`} opacity={show}>
      <foreignObject x={-300} y={-40} width={600} height={80}>
        <div style={{display: 'flex', justifyContent: 'center'}}><div style={{background: bg, color: col, fontWeight: 900, fontSize: size, padding: '2px 16px', borderRadius: 8,
          border: `4px solid ${E.white}`, whiteSpace: 'nowrap', direction: 'rtl', boxShadow: '0 6px 12px rgba(0,0,0,.4)'}}>{text}</div></div>
      </foreignObject>
    </g>) : null;
  const enterP = sm(t / 14);
  return (
    <div style={{position: 'absolute', left: 560, top: 70, width: 1300, height: 760, borderRadius: 26, overflow: 'hidden', ...stickerBorder(9), opacity: o * enterP,
      transform: `scale(${0.9 + 0.1 * enterP}) rotate(-1deg)`, background: '#2E6F93'}}>
      <svg viewBox={`${cx - w / 2} ${cy - h / 2} ${w} ${h}`} preserveAspectRatio="xMidYMid slice" style={{width: '100%', height: '100%'}}>
        <rect x={cx - w} y={cy - h} width={w * 2} height={h * 2} fill="#2E6F93" />
        <path d={egy} fill="#E7D7B1" stroke={E.white} strokeWidth={px * 5} strokeLinejoin="round" />
        {/* Nile: simplified line for the whole country, the real OSM river when we are close */}
        <g opacity={1 - k}>
          <path d={path(NILE_EG.map((q) => W2(q[0], q[1])))} fill="none" stroke="#3A8DB6" strokeWidth={px * 7} strokeLinecap="round" strokeLinejoin="round" />
          {DELTA.map((d, n) => <path key={n} d={path(d.map((q) => W2(q[0], q[1])))} fill="none" stroke="#3A8DB6" strokeWidth={px * 5} strokeLinecap="round" />)}
        </g>
        <g opacity={sm((k - 0.55) / 0.4)} fill="none" strokeLinecap="round" strokeLinejoin="round">
          <path d={mid} stroke="#FFFDF5" strokeWidth={px * 2.2} opacity={0.7} />
          <path d={big} stroke="#FFFDF5" strokeWidth={px * 4.5} />
        </g>
        <path d={nile} fill="#3A8DB6" stroke="#3A8DB6" strokeWidth={px * 10} strokeLinejoin="round" opacity={k} />
        {/* Cairo dot, then New Cairo area + the pin on GUC */}
        <circle cx={CAI[0]} cy={CAI[1]} r={px * (12 + 6 * Math.sin(t / 5))} fill={E.orange} stroke={E.white} strokeWidth={px * 4} opacity={1 - k * 0.6} />
        {lab(CAI[0] - px * 10, CAI[1] - px * 60, 'القاهرة', 40, E.ink, E.paper, 1 - k)}
        {lab(W2(29.0, 26.0)[0], W2(29.0, 26.0)[1], 'مصر', 64, E.ink, E.mustard, 1 - k)}
        {lab(CAI[0] - px * 90, CAI[1] - px * 40, 'وسط البلد', 34, E.ink, E.paper, sm((t - zIn - 26) / 10))}
        <ellipse cx={GUC[0] + px * 40} cy={GUC[1] - px * 30} rx={px * 300} ry={px * 190} fill="rgba(232,181,74,.18)" stroke={E.mustard} strokeWidth={px * 4} strokeDasharray={`${px * 14} ${px * 12}`}
          opacity={sm((t - zIn - 30) / 10)} />
        {lab(GUC[0] + px * 60, GUC[1] - px * 260, 'التجمع الخامس', 42, E.ink, E.mustard, sm((t - zIn - 30) / 10))}
        {pin > 0 ? (
          <g transform={`translate(${GUC[0]} ${GUC[1] - px * 260 * (1 - Math.min(1, pin))}) scale(${px})`}>
            <circle r={30 + 80 * ring} fill="none" stroke={E.orange} strokeWidth={6} opacity={1 - ring} />
            <path d="M0,0 C-10,-30 -46,-50 -46,-86 A46,46 0 1 1 46,-86 C46,-50 10,-30 0,0 Z" fill={E.orange} stroke={E.white} strokeWidth={6} />
            <circle cy={-86} r={18} fill={E.white} />
          </g>
        ) : null}
        {lab(GUC[0], GUC[1] + px * 60, 'GUC · الجامعة الألمانية بالقاهرة', 36, E.white, E.ink, sm((t - pinAt - 8) / 10))}
      </svg>
      <div style={{position: 'absolute', left: 14, bottom: 10, fontSize: 18, color: 'rgba(255,255,255,.75)', fontWeight: 700}}>Natural Earth · OpenStreetMap · Wikidata</div>
    </div>
  );
};

// The show's 3 departments ("flavours") = their real logos from the intros (a frame without the wink, Aly 2026-10-27); the department
// name in each logo gets a drawn ring ("لو الناس مش واخدة بالها"), then this episode's one is selected: bigger, gold glow, ✓, the others dim.
const Flavours: React.FC<{l: L; f: number}> = ({l, f}) => {
  const items = l.items ?? [], sel = l.sel ?? 2, selAt = l.at + (l.selAt ?? 40), o = life(f, l, 10);
  const ks = sm((f - selAt) / 14);
  return (
    <>
      {items.map((it, i) => {
        const at = l.at + i * 7, p = enter(f, 30, at);
        if (f < at) return null;
        const isSel = i === sel, w = 300 * (1 + (isSel ? 0.22 : -0.06) * ks), h = w * 1.066;
        const x = (l.x ?? 1240) + (i - 1) * 360 + (isSel ? 0 : i < sel ? -20 : 20) * ks, y = (l.y ?? 520) - (isSel ? 26 : 0) * ks;
        const hk = sm((f - at - 10) / 14), hs = isSel ? sm((f - selAt) / 16) : 0;
        // hand-drawn ring around the department name, drawn INSIDE the picture (inside the card border) so it sits on the name
        const ring = (
            <svg viewBox="0 0 100 106.6" preserveAspectRatio="none" style={{position: 'absolute', inset: 0, width: '100%', height: '100%', overflow: 'visible'}}>
              {/* ring = the measured box of the department name in THIS logo (+ margin), so it never cuts the letters (Aly 2026-10-27) */}
              <ellipse cx={it.ring?.[0] ?? 50} cy={it.ring?.[1] ?? 10.3} rx={(it.ring?.[2] ?? 17) + (isSel ? 1.5 * hs : 0)} ry={(it.ring?.[3] ?? 7) + (isSel ? 0.6 * hs : 0)}
                fill="none" stroke={isSel ? E.orange : E.mustard} strokeWidth={isSel ? 1.4 + 1.0 * hs : 1.0} pathLength={100} strokeDasharray="100"
                strokeDashoffset={100 * (1 - Math.max(hk * 0.85, hs))} strokeLinecap="round" transform={`rotate(-1.5 ${it.ring?.[0] ?? 50} ${it.ring?.[1] ?? 10.3})`} />
            </svg>
        );
        return (
          <div key={i} style={{position: 'absolute', left: x - w / 2, top: y - h / 2, width: w, height: h, opacity: Math.min(1, p * 1.6) * o * (isSel ? 1 : 1 - 0.55 * ks),
            transform: `translateY(${lerp(p, 60, 0)}px) rotate(${(i - 1) * 3 * (1 - ks)}deg)`, filter: isSel ? undefined : `grayscale(${ks})`}}>
            <div style={{position: 'absolute', inset: 0, borderRadius: 16, overflow: 'hidden', ...stickerBorder(isSel ? 10 : 7),
              boxShadow: isSel ? `0 0 ${50 * ks}px rgba(232,181,74,${0.75 * ks}), 0 14px 30px rgba(0,0,0,.5)` : '0 14px 30px rgba(0,0,0,.5)'}}>
              <Img src={staticFile(it.src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
              {ring}
            </div>
            {isSel && ks > 0.05 ? <div style={{position: 'absolute', right: -40, top: -46, transform: `scale(${enter(f, 30, selAt + 6)}) rotate(10deg)`}}><Sticker name="check" size={110} /></div> : null}
          </div>
        );
      })}
    </>
  );
};

export const BizOpen: React.FC<z.infer<typeof bizOpenSchema>> = ({aly, alyW, alyH, name, cam, guest, layers}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const fadeIn = 1; // no fade-in: a fade let the stage (Karim's tile) show through right after the intro (Aly 2026-10-28)
  const fadeOut = interpolate(f, [durationInFrames - 10, durationInFrames], [1, 0], {extrapolateLeft: 'clamp'});
  const vis = (l: L) => f >= l.at && f < l.at + l.dur;
  return (
    <AbsoluteFill style={{opacity: Math.min(fadeIn, fadeOut)}}>
      <MeetBg frame={f} />
      {layers.filter((l) => l.k === 'clip' && vis(l)).map((l, i) => (
        <AbsoluteFill key={'c' + i} style={{opacity: Math.min(1, (f - l.at) / 10, life(f, l, 10))}}>
          {/* each Blender clip starts at ITS frame 0 when the layer starts (v1 bug: played from the board start -> only its last frame showed) */}
          <Sequence from={l.at} layout="none">
            <OffthreadVideo src={staticFile(l.file!)} transparent muted playbackRate={l.rate ?? 1} startFrom={0}
              style={{position: 'absolute', left: l.x ?? 0, top: 0, width: 1920, height: 1080}} />
          </Sequence>
        </AbsoluteFill>
      ))}
      {guest ? <Guest g={guest} /> : null}
      <AlyCam src={aly} w={alyW} h={alyH} name={name} cam={cam} />
      {layers.filter((l) => l.k !== 'clip' && vis(l)).map((l, i) => {
        if (l.k === 'head') return <Head key={i} l={l} f={f} />;
        if (l.k === 'chips') return <Chips key={i} l={l} f={f} />;
        if (l.k === 'pics') return <Pics key={i} l={l} f={f} />;
        if (l.k === 'phone') return <Phone key={i} l={l} f={f} />;
        if (l.k === 'map') return <BizMap key={i} l={l} f={f} />;
        if (l.k === 'flavours') return <Flavours key={i} l={l} f={f} />;
        const p = enter(f, 30, l.at), o = life(f, l);
        if (l.k === 'stk') return (
          <div key={i} style={{position: 'absolute', left: l.x, top: l.y, transform: `translate(-50%, -50%) scale(${p}) rotate(${(l.rot ?? 0) + Math.sin((f - l.at) / 12) * 3}deg)`, opacity: o}}>
            <Sticker name={l.name!} size={l.size ?? 140} />
          </div>
        );
        if (l.k === 'xmark') return (
          <div key={i} style={{position: 'absolute', left: l.x, top: l.y, transform: `translate(-50%, -50%) scale(${lerp(p, 2.2, 1)}) rotate(-8deg)`, opacity: Math.min(1, p * 2) * o}}>
            <Sticker name="cross" size={l.size ?? 260} />
          </div>
        );
        if (l.k === 'big') return (
          <div key={i} style={{position: 'absolute', left: l.x, top: l.y, transform: `translate(-50%, -50%) scale(${lerp(p, 0.4, 1)})`, opacity: Math.min(1, p * 1.6) * o, textAlign: 'center',
            direction: 'rtl', whiteSpace: 'nowrap'}}>
            <div style={{fontSize: l.size ?? 150, fontWeight: 900, color: accentOf(l.accent ?? 'mustard'), textShadow: '0 8px 0 rgba(0,0,0,.35), 0 0 40px rgba(232,181,74,.35)', lineHeight: 1}}>{l.text}</div>
            {l.sub ? <div style={{fontSize: (l.size ?? 150) * 0.3, fontWeight: 800, color: E.white, marginTop: 10, textShadow: '0 4px 10px rgba(0,0,0,.6)'}}><Hi text={l.sub} color={E.mustard} /></div> : null}
          </div>
        );
        return null;
      })}
    </AbsoluteFill>
  );
};
