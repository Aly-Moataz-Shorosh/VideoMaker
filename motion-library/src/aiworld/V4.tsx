// «عالم الـ AI كله» rough cut v4 (Aly's v3 notes 1-16, 2026-11-22). Built on the APPROVED kit of «انت بتشتغل ايه»:
// every element = an enta board Item (Fluent 3D, taped photo, white logo tile, paper text, chip, counting number, arrow) placed
// by meaning, ENTERS on its word and LEAVES smoothly ('out'); paper Title; the show's glitch (EntaGlitch) on the opening cuts;
// only the BACKGROUND moves (stars), never text/objects; captions = the script on its word times. Props: make_props_v4.py.
import React from 'react';
import {AbsoluteFill, Easing, Img, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {fontCss} from '../blocks/theme';
import {Item} from '../enta/BoardBiz';
import {EntaGlitch} from '../enta/EntaPop';
import {E, Grain, Hi, stickerBorder} from '../enta/kit';
import {enter} from '../blocks/anim';

const gold = '#E9B949', navy = '#0B1430', ink = '#F3EEDF', amber = '#FF9F43';
const S = (p?: string) => (p ? staticFile(p) : '');
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// Arabic line with English words kept in their place (each Latin run isolated) — note 5
export const Rtl: React.FC<{text: string; hi?: string}> = ({text, hi}) => (
  <span style={{direction: 'rtl', unicodeBidi: 'isolate'}}>
    {text.split(/(\*[^*]+\*|[A-Za-z0-9](?:[\w.:+\-/$%]*[\w+$%])?(?:\s+[A-Za-z0-9](?:[\w.:+\-/$%]*[\w+$%])?)*)/g).map((p, i) =>
      p.startsWith('*') ? <span key={i} style={{color: hi ?? gold}}>{p.slice(1, -1)}</span>
        : /^[A-Za-z0-9]/.test(p) ? <bdi key={i} dir="ltr">{p}</bdi> : <span key={i}>{p}</span>)}
  </span>
);

const clip = z.object({src: z.string(), from: z.number(), dur: z.number(), skip: z.number().optional()});
const scene = z.object({k: z.string(), start: z.number(), dur: z.number(), title: z.string().optional(), items: z.array(z.record(z.string(), z.any())).default([]),
  clips: z.array(clip).default([]), url: z.string().optional(), fx: z.string().optional(), hud: z.number().optional(), glitch: z.array(z.number()).default([]),
  words: z.array(z.object({t: z.number(), w: z.string()})).default([]), fam: z.array(z.number()).default([])});
export const aiV4Schema = z.object({
  fps: z.number().default(25), duration: z.number().default(10), outW: z.number().default(1920),
  scenes: z.array(scene).default([]), hud: z.array(z.object({a: z.number(), b: z.number(), i: z.number()})).default([]),
  caps: z.array(z.object({a: z.number(), b: z.number(), t: z.string()})).default([]),
  families: z.array(z.string()).default(['التوليد', 'الـ LLMs والـ agents', 'السكريبتات', 'الـ MCP', 'الـ skills', 'الإنسان']),
});
type Scene = z.infer<typeof scene>;

// ---------- background: the S4g night-blue with gold stars; ONLY this layer moves (notes 3, 9) ----------
const StarField: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const push = interpolate(f, [0, Math.max(1, dur * fps)], [1, 1.07]);
  const drift = f * 0.25;
  const star = (x: number, y: number, s: number, k: number) => (
    <g key={k} transform={`translate(${x},${y}) rotate(${(k * 37) % 72}) scale(${s})`} opacity={0.32 + 0.22 * Math.sin(f / 40 + k)}>
      {[0, 72, 144, 216, 288].map((r) => <line key={r} x1={0} y1={0} x2={0} y2={-9} stroke={gold} strokeWidth={1.8} strokeLinecap="round" transform={`rotate(${r})`} />)}
    </g>);
  const stars: React.ReactNode[] = [];
  for (let r = 0; r < 15; r++) for (let c = 0; c < 23; c++) stars.push(star(c * 92 + (r % 2) * 46 - 46 + (drift % 92), r * 82 - 20, 1 + ((r * 7 + c) % 3) * 0.12, r * 23 + c));
  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 90% at 50% 40%, #16245a 0%, ${navy} 55%, #050815 100%)`, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${push})`}}><svg width={1920} height={1080}>{stars}</svg></AbsoluteFill>
      <AbsoluteFill style={{background: 'radial-gradient(60% 50% at 50% 30%, rgba(255,159,67,.12), transparent 70%)'}} />
    </AbsoluteFill>
  );
};

// paper title of the show, enters and LEAVES smoothly
const PaperTitle: React.FC<{text?: string; dur: number}> = ({text, dur}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  if (!text) return null;
  const p = enter(f, fps, 3), o = interpolate(f, [dur * fps - 12, dur * fps - 2], [1, 0], clamp);
  return (
    <div style={{position: 'absolute', top: 54, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: o}}>
      <div style={{position: 'relative', background: E.paper, color: E.ink, fontFamily: 'Cairo', fontSize: 58, fontWeight: 900, padding: '8px 42px', borderRadius: 10,
        transform: `rotate(-1.5deg) scale(${p})`, ...stickerBorder(7), overflow: 'hidden'}}>
        <Grain opacity={0.3} seed={43} /><span style={{position: 'relative'}}><Rtl text={text} hi={E.orange} /></span>
      </div>
    </div>
  );
};

const Items: React.FC<{items: Scene['items']}> = ({items}) => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{fontFamily: 'Cairo'}}>{items.map((d, i) => <Item key={i} d={d} f={f} />)}</AbsoluteFill>;
};

const ClipSeq: React.FC<{c: z.infer<typeof clip>; start: number}> = ({c, start}) => {
  const {fps} = useVideoConfig();
  return (
    <Sequence from={Math.round((c.from - start) * fps)} durationInFrames={Math.max(1, Math.round(c.dur * fps))}>
      <OffthreadVideo src={S(c.src)} muted startFrom={Math.round((c.skip || 0) * fps)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
    </Sequence>
  );
};

// ---------- the jet = 6 families: HTML labels (RTL correct, note 5) ----------
const JetMap: React.FC<{s: Scene; families: string[]}> = ({s, families}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const parts = [[-390, 10], [-210, -175], [0, -40], [210, -175], [390, 10], [0, 175]];
  const X = (x: number) => 960 + x * 1.55, Y = (y: number) => 560 + y * 1.55;
  const out = interpolate(f, [s.dur * fps - 12, s.dur * fps - 2], [1, 0], clamp);
  return (
    <AbsoluteFill style={{opacity: out}}>
      <svg width={1920} height={1080} viewBox="-620 -380 1240 700" style={{position: 'absolute', inset: 0}}>
        <path d="M0,-260 L60,-60 L380,40 L380,90 L60,60 L40,200 L120,250 L120,280 L0,260 L-120,280 L-120,250 L-40,200 L-60,60 L-380,90 L-380,40 L-60,-60 Z"
          fill="rgba(95,211,230,.10)" stroke="#5FD3E6" strokeOpacity={0.75} strokeWidth={3} strokeDasharray="12 8" />
      </svg>
      {parts.map(([x, y], i) => {
        const at = s.fam[i] !== undefined ? s.fam[i] : 0;
        const show = s.fam.length ? f >= at : true;
        const p = s.fam.length ? enter(f, fps, at) : 1, hot = s.hud === i;
        return (
          <div key={i} style={{position: 'absolute', left: X(x), top: Y(y), transform: `translate(-50%,-50%) scale(${0.5 + 0.5 * p})`, opacity: show ? 1 : 0.25,
            background: hot ? E.mustard : E.paper, color: E.ink, borderRadius: 14, padding: '10px 26px', minWidth: 230, textAlign: 'center', ...stickerBorder(6),
            fontFamily: 'Cairo', boxShadow: '0 12px 24px rgba(0,0,0,.45)'}}>
            <div style={{fontFamily: 'Montserrat', fontWeight: 900, fontSize: 34, color: E.orange}}>{i + 1}</div>
            <div style={{fontWeight: 900, fontSize: 34, whiteSpace: 'nowrap'}}><Rtl text={families[i]} /></div>
          </div>);
      })}
    </AbsoluteFill>
  );
};
const MiniHud: React.FC<{i: number; families: string[]}> = ({i, families}) => (
  <div style={{position: 'absolute', top: 22, right: 26, display: 'flex', gap: 6, direction: 'rtl', fontFamily: 'Cairo'}}>
    {families.map((n, k) => (
      <div key={k} style={{padding: '3px 12px', borderRadius: 8, fontSize: 19, fontWeight: 800, whiteSpace: 'nowrap',
        color: k === i ? E.ink : 'rgba(243,238,223,.7)', background: k === i ? E.mustard : 'rgba(8,14,36,.62)', border: `1px solid ${k === i ? E.white : 'rgba(233,185,73,.3)'}`}}><Rtl text={n} /></div>
    ))}
  </div>
);

// ---------- browser with a REAL page (screenshot), stays on its word for its sentence ----------
const Browser: React.FC<{s: Scene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const pages = s.items.filter((d) => d.k === 'page');
  const cur = [...pages].reverse().find((d) => f >= d.at) ?? pages[0];
  if (!cur) return null;
  const p = enter(f, fps, cur.at), o = interpolate(f, [(cur.out ?? s.dur * fps) - 10, cur.out ?? s.dur * fps], [1, 0], clamp);
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', paddingTop: 70}}>
      <div style={{width: 1420, height: 800, borderRadius: 20, overflow: 'hidden', background: '#0e1220', boxShadow: '0 30px 80px rgba(0,0,0,.6)', ...stickerBorder(6),
        transform: `translateY(${(1 - p) * 60}px) scale(${0.9 + 0.1 * p})`, opacity: Math.min(1, p * 1.5) * o}}>
        <div style={{height: 50, background: '#1a2036', display: 'flex', alignItems: 'center', gap: 10, padding: '0 18px'}}>
          {['#FF5A6E', '#F5C451', '#4CD37A'].map((c) => <div key={c} style={{width: 14, height: 14, borderRadius: 7, background: c}} />)}
          <div style={{marginLeft: 20, flex: 1, height: 30, borderRadius: 15, background: '#0b0f1c', color: 'rgba(243,238,223,.7)', fontFamily: 'Montserrat', fontSize: 18,
            display: 'flex', alignItems: 'center', padding: '0 16px'}}>{cur.url ?? s.url ?? ''}</div>
        </div>
        <Img src={S(cur.src)} style={{width: '100%', height: 750, objectFit: 'cover',   /* the page scrolls slowly like a screen recording (a still page = a frozen frame) */
          objectPosition: cur.pos ?? `50% ${interpolate(f, [cur.at + 15, cur.out ?? s.dur * fps], [0, 100], {...clamp, easing: Easing.inOut(Easing.sin)})}%`}} />
      </div>
    </AbsoluteFill>
  );
};

// ---------- text -> picture (prompt types) and picture -> SAME picture edited (wipe) ----------
const Split: React.FC<{s: Scene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const out = interpolate(f, [s.dur * fps - 12, s.dur * fps - 2], [1, 0], clamp);
  const side = (d: Record<string, any>, i: number) => {
    const t0 = d.at ?? 0, p = enter(f, fps, t0);
    const typed = interpolate(f, [t0, t0 + 40], [0, 1], clamp), reveal = interpolate(f, [t0 + 45, t0 + 65], [0, 1], clamp);
    const wipe = interpolate(f, [t0 + 20, t0 + 60], [0, 1], clamp);
    return (
      <div key={i} style={{position: 'relative', width: 860, height: 484, borderRadius: 12, overflow: 'hidden', ...stickerBorder(7), background: '#0b1020',
        transform: `translateY(${(1 - p) * 50}px) rotate(${i ? 1.2 : -1.2}deg)`, opacity: Math.min(1, p * 1.5)}}>
        {!d.src ? <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', background: E.paper, color: E.ink, fontFamily: 'Cairo',
          fontWeight: 900, fontSize: 64, padding: 40, textAlign: 'center'}}><Rtl text={d.cap ?? ''} hi={E.orange} /></div>
          : /\.(mp4|webm)$/.test(d.src) ? <Sequence from={t0} layout="none"><OffthreadVideo src={S(d.src)} muted startFrom={3} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></Sequence>
          : <Img src={S(d.src)} style={{width: '100%', height: '100%', objectFit: 'cover', opacity: d.prompt ? reveal : 1}} />}
        {d.before ? <div style={{position: 'absolute', inset: 0, clipPath: `inset(0 0 0 ${wipe * 100}%)`}}>
          <Img src={S(d.before)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          <div style={{position: 'absolute', top: 0, bottom: 0, left: 0, width: 6, background: E.mustard}} /></div> : null}
        {d.prompt && reveal < 1 ? <div style={{position: 'absolute', inset: 0, background: `rgba(8,14,36,${0.93 - 0.9 * reveal})`, padding: 30, fontFamily: 'Consolas, monospace',
          fontSize: 25, lineHeight: 1.45, color: '#cfe3ff', direction: 'ltr', textAlign: 'left'}}><span style={{color: E.mustard}}>prompt › </span>
          {String(d.prompt).slice(0, Math.floor(String(d.prompt).length * typed))}</div> : null}
        {d.cap && d.src ? <div style={{position: 'absolute', bottom: 14, right: 14, background: E.paper, color: E.ink, fontFamily: 'Cairo', fontWeight: 900, fontSize: 30, padding: '4px 18px',
          borderRadius: 8, ...stickerBorder(4)}}><Rtl text={d.cap} hi={E.orange} /></div> : null}
      </div>);
  };
  return <AbsoluteFill style={{flexDirection: 'row-reverse', gap: 50, alignItems: 'center', justifyContent: 'center', paddingTop: 90, opacity: out}}>
    {s.items.filter((d) => d.k === 'split').map(side)}</AbsoluteFill>;
};

// ---------- noise -> picture (diffusion) ----------
const Diffusion: React.FC<{s: Scene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const d = s.items.find((x) => x.k === 'diff'); if (!d) return null;
  const k = interpolate(f, [d.at ?? 0, s.dur * fps - 15], [0, 1], clamp), out = interpolate(f, [s.dur * fps - 12, s.dur * fps - 2], [1, 0], clamp);
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', paddingTop: 60, opacity: out}}>
      <div style={{position: 'relative', width: 1200, height: 675, borderRadius: 12, overflow: 'hidden', ...stickerBorder(7)}}>
        <Img src={S(d.src)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: `blur(${(1 - k) * 26}px)`}} />
        <Img src={S('projects/aiworld/v3/noise.png')} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: Math.pow(1 - k, 1.3)}} />
      </div>
      <div style={{position: 'absolute', top: 40, fontFamily: 'Montserrat', fontWeight: 900, color: E.mustard, fontSize: 40}}>step {Math.floor(k * 30)} / 30</div>
    </AbsoluteFill>
  );
};

// ---------- song: each line's clip + its words in gold (the song lines ARE the captions there) ----------
const Lyr: React.FC<{s: Scene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const t = s.start + f / fps;
  const lines = s.items.filter((d) => d.k === 'line');
  const line = [...lines].reverse().find((d) => t >= d.t - 0.05);
  const words = line ? s.words.filter((w) => w.t >= line.t - 0.05 && w.t < line.end) : [];
  return (
    <AbsoluteFill>
      {s.clips.map((c, i) => <ClipSeq key={i} c={c} start={s.start} />)}
      <AbsoluteFill style={{background: 'linear-gradient(transparent 50%, rgba(5,8,21,.78))'}} />
      <div style={{position: 'absolute', bottom: 70, left: 80, right: 80, display: 'flex', flexWrap: 'wrap', gap: '6px 18px', justifyContent: 'center', direction: 'rtl', fontFamily: 'Cairo'}}>
        {words.map((w, i) => {
          const p = enter(f, fps, Math.round((w.t - s.start) * fps));
          const o = line ? interpolate(t, [line.end - 0.35, line.end - 0.05], [1, 0], clamp) : 1;
          return <bdi key={i} style={{fontSize: 74, fontWeight: 900, color: t >= w.t ? gold : 'rgba(243,238,223,.25)', transform: `translateY(${(1 - p) * 30}px)`, opacity: o,
            textShadow: '0 6px 26px rgba(0,0,0,.7)', display: 'inline-block'}}>{w.w}</bdi>;
        })}
      </div>
    </AbsoluteFill>
  );
};

const SceneView: React.FC<{s: Scene; families: string[]}> = ({s, families}) => {
  const video = ['AV', 'CLIP', 'LYR'].includes(s.k);
  return (
    <AbsoluteFill>
      {!video && <StarField dur={s.dur} />}
      {s.k === 'AV' || s.k === 'CLIP' ? <AbsoluteFill>{s.clips.map((c, i) => <ClipSeq key={i} c={c} start={s.start} />)}</AbsoluteFill> : null}
      {s.glitch.map((g, i) => <Sequence key={'g' + i} from={Math.round((g - s.start) * 25) - 3} durationInFrames={8}><EntaGlitch seed={i + 3} strength={1} previewBg="" /></Sequence>)}
      {s.k === 'MAP6' && <JetMap s={s} families={families} />}
      {s.k === 'WEB' && <Browser s={s} />}
      {s.k === 'SPLIT' && <Split s={s} />}
      {s.fx === 'diffusion' && <Diffusion s={s} />}
      {s.k === 'LYR' && <Lyr s={s} />}
      <Items items={s.items.filter((d) => !['page', 'split', 'diff', 'line'].includes(d.k))} />
      {s.k !== 'LYR' && <PaperTitle text={s.title} dur={s.dur} />}
    </AbsoluteFill>
  );
};

// captions = the script itself on its word times (note 11); not over the song (its lines are the captions there)
const Captions: React.FC<{caps: z.infer<typeof aiV4Schema>['caps']; t: number}> = ({caps, t}) => {
  const c = caps.find((x) => t >= x.a && t < x.b);
  if (!c) return null;
  const e_ = Math.min(0.12, (c.b - c.a) / 3), o = interpolate(t, [c.a, c.a + e_, c.b - e_, c.b], [0, 1, 1, 0], clamp);
  return (
    <div style={{position: 'absolute', left: 0, right: 0, bottom: 34, display: 'flex', justifyContent: 'center', opacity: o, fontFamily: 'Cairo'}}>
      <div style={{background: 'rgba(5,8,21,.72)', color: ink, fontWeight: 800, fontSize: 44, padding: '4px 26px', borderRadius: 12, maxWidth: 1500, textAlign: 'center'}}>
        <Rtl text={c.t} /></div>
    </div>
  );
};

export const AiWorldV4: React.FC<z.infer<typeof aiV4Schema>> = (p) => {
  const {width} = useVideoConfig(); const f = useCurrentFrame(); const t = f / p.fps;
  const h = p.hud.find((x) => t >= x.a && t < x.b);
  return (
    <AbsoluteFill style={{background: navy, overflow: 'hidden'}}>
      <style>{fontCss}</style>
      <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `scale(${width / 1920})`, transformOrigin: 'left top'}}>
        {p.scenes.map((s, i) => (
          <Sequence key={i} from={Math.round(s.start * p.fps)} durationInFrames={Math.max(1, Math.round(s.dur * p.fps))}>
            <SceneView s={s} families={p.families} />
          </Sequence>
        ))}
        {h && <MiniHud i={h.i} families={p.families} />}
        <Captions caps={p.caps} t={t} />
      </div>
    </AbsoluteFill>
  );
};
