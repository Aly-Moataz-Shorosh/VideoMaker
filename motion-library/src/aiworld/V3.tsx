// «عالم الـ AI كله» rough cut v3 (Aly's 22 notes, 2026-11-21): one visual per sentence, full-frame motion, NO boxed cards,
// NO captions. Scenes come from projects/<code>/work/scripts/make_props_v3.py (plan_v3_data.py). Look = his S4g studio:
// deep night blue + small gold hand-painted stars + warm mashrabiya amber.
import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {fontCss} from '../blocks/theme';

const ink = '#F3EEDF', dim = 'rgba(243,238,223,.68)', gold = '#E9B949', amber = '#FF9F43', navy = '#0B1430', cyan = '#5FD3E6', red = '#FF5A6E';
const ar: React.CSSProperties = {fontFamily: 'Cairo, sans-serif', direction: 'rtl', unicodeBidi: 'isolate'};
const S = (p?: string) => (p ? staticFile(p) : '');

const item = z.object({t: z.number(), label: z.string().optional(), logo: z.string().optional(), img: z.string().optional(),
  emoji: z.string().optional(), num: z.string().optional(), qr: z.string().optional(), sub: z.string().optional(),
  before: z.string().optional(), prompt: z.string().optional()});
const clip = z.object({src: z.string(), from: z.number(), dur: z.number(), rate: z.number().optional(), label: z.string().optional(), skip: z.number().optional()});
const scene = z.object({k: z.string(), start: z.number(), dur: z.number(), title: z.string().optional(), items: z.array(item).default([]),
  clips: z.array(clip).default([]), imgs: z.array(z.string()).default([]), hud: z.number().optional(), step: z.string().optional(),
  url: z.string().optional(), fx: z.string().optional(), words: z.array(z.object({t: z.number(), w: z.string()})).default([])});
export const aiV3Schema = z.object({
  fps: z.number().default(25), duration: z.number().default(10), outW: z.number().default(1920),
  scenes: z.array(scene).default([]),
  hud: z.array(z.object({a: z.number(), b: z.number(), i: z.number()})).default([]),
  families: z.array(z.string()).default(['التوليد', 'LLMs والـ agents', 'السكريبتات', 'MCP', 'skills', 'الإنسان']),
});
type Scene = z.infer<typeof scene>;

// ---------- shared look ----------
const StarField: React.FC<{dim?: number}> = ({dim: d = 1}) => {
  const f = useCurrentFrame();
  const star = (x: number, y: number, s: number, k: number) => (
    <g key={k} transform={`translate(${x},${y}) rotate(${(k * 37) % 72}) scale(${s})`} opacity={0.35 * d + 0.25 * d * Math.sin(f / 40 + k)}>
      {[0, 72, 144, 216, 288].map((r) => <line key={r} x1={0} y1={0} x2={0} y2={-9} stroke={gold} strokeWidth={1.8} strokeLinecap="round" transform={`rotate(${r})`} />)}
    </g>);
  const stars = [] as React.ReactNode[];
  for (let r = 0; r < 14; r++) for (let c = 0; c < 22; c++) stars.push(star(c * 92 + (r % 2) * 46 + ((f * 0.08) % 92), r * 82 + 20, 1 + ((r * 7 + c) % 3) * 0.12, r * 22 + c));
  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 90% at 50% 40%, #16245a 0%, ${navy} 55%, #050815 100%)`}}>
      <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>{stars}</svg>
      <AbsoluteFill style={{background: 'radial-gradient(60% 50% at 50% 30%, rgba(255,159,67,.14), transparent 70%)'}} />
    </AbsoluteFill>
  );
};

const usePop = (t: number, start: number) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  return spring({frame: f - Math.round((t - start) * fps), fps, config: {damping: 13, stiffness: 140}});
};

const Logo: React.FC<{src?: string; size?: number}> = ({src, size = 120}) => src ? (
  <Img src={S(src)} style={{width: size, height: size, objectFit: 'contain', filter: 'drop-shadow(0 6px 18px rgba(0,0,0,.45))'}} />) : null;

const Chip: React.FC<{it: z.infer<typeof item>; start: number; big?: boolean}> = ({it, start, big}) => {
  const p = usePop(it.t, start);
  if (p <= 0.001) return null;
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 16, transform: `translateY(${(1 - p) * 40}px) scale(${0.7 + 0.3 * p})`, opacity: Math.min(1, p * 1.4),
      padding: big ? '16px 26px' : '10px 20px', borderRadius: 22, background: 'rgba(8,14,36,.72)', border: `1.5px solid ${gold}88`,
      boxShadow: `0 10px 30px rgba(0,0,0,.35), inset 0 0 0 1px rgba(255,255,255,.05)`, backdropFilter: 'blur(6px)'}}>
      {it.logo && <Logo src={it.logo} size={big ? 78 : 56} />}
      {it.emoji && <span style={{fontSize: big ? 70 : 50, lineHeight: 1}}>{it.emoji}</span>}
      {it.num && <span style={{fontFamily: 'Montserrat', fontWeight: 900, fontSize: big ? 76 : 52, color: gold}}>{it.num}</span>}
      {it.label && <span style={{...ar, color: ink, fontWeight: 800, fontSize: big ? 46 : 34, whiteSpace: 'nowrap'}}>{it.label}</span>}
    </div>
  );
};

const Title: React.FC<{text?: string; start: number; t0?: number; top?: number}> = ({text, start, t0, top = 70}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  if (!text) return null;
  const k = interpolate(f - ((t0 ?? start) - start) * fps, [0, 18], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const n = Math.ceil([...text].length * k);
  return (
    <div style={{position: 'absolute', top, left: 0, right: 0, textAlign: 'center'}}>
      <span style={{...ar, color: ink, fontSize: 66, fontWeight: 900, textShadow: '0 4px 24px rgba(0,0,0,.6)'}}>{[...text].slice(0, n).join('')}</span>
    </div>
  );
};

// a clip that never jumps back: its own sequence, trimmed (skip) and never slowed below 1 (rate>=1)
const ClipSeq: React.FC<{c: z.infer<typeof clip>; start: number; style?: React.CSSProperties}> = ({c, start, style}) => {
  const {fps} = useVideoConfig();
  return (
    <Sequence from={Math.round((c.from - start) * fps)} durationInFrames={Math.max(1, Math.round(c.dur * fps))}>
      <AbsoluteFill style={style}>
        <OffthreadVideo src={S(c.src)} muted startFrom={Math.round((c.skip || 0) * fps)} playbackRate={c.rate || 1}
          style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
    </Sequence>
  );
};

const Glitch: React.FC<{at: number; start: number}> = ({at, start}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const k = f - Math.round((at - start) * fps);
  if (k < -3 || k > 5) return null;
  const bars = [...Array(9)].map((_, i) => {
    const y = ((i * 131 + k * 53) % 1000) / 10, h = 2 + ((i * 7 + k) % 6);
    const dx = (((i * 97 + k * 31) % 9) - 4) * 28;
    return <div key={i} style={{position: 'absolute', left: 0, right: 0, top: `${y}%`, height: `${h}%`, transform: `translateX(${dx}px)`,
      background: i % 3 === 0 ? 'rgba(255,40,90,.35)' : i % 3 === 1 ? 'rgba(40,220,255,.35)' : 'rgba(255,255,255,.18)', mixBlendMode: 'screen'}} />;
  });
  return <AbsoluteFill style={{pointerEvents: 'none'}}>{bars}<AbsoluteFill style={{background: k === 0 ? 'rgba(255,255,255,.35)' : 'transparent'}} /></AbsoluteFill>;
};

const SideStack: React.FC<{items: Scene['items']; start: number; side?: 'right' | 'left'}> = ({items, start, side = 'right'}) => (
  <div style={{position: 'absolute', top: 150, bottom: 150, [side]: 60, width: 460, display: 'flex', flexDirection: 'column', gap: 18,
    justifyContent: 'center', alignItems: side === 'right' ? 'flex-end' : 'flex-start'} as React.CSSProperties}>
    {items.slice(-5).map((it, i) => <Chip key={i} it={it} start={start} />)}
  </div>
);

// ---------- the jet = 6 families ----------
const JetMap: React.FC<{s: Scene; families: string[]}> = ({s, families}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const t = s.start + f / fps;
  const parts = [[-390, 10], [-210, -175], [0, -40], [210, -175], [390, 10], [0, 175]];
  const shown = (i: number) => s.items[i] ? t >= s.items[i].t : s.hud !== undefined;
  return (
    <AbsoluteFill>
      <svg width={1920} height={1080} viewBox="-620 -380 1240 700" style={{position: 'absolute', inset: 0}}>
        <path d="M0,-260 L60,-60 L380,40 L380,90 L60,60 L40,200 L120,250 L120,280 L0,260 L-120,280 L-120,250 L-40,200 L-60,60 L-380,90 L-380,40 L-60,-60 Z"
          fill="rgba(95,211,230,.10)" stroke={cyan} strokeOpacity={0.75} strokeWidth={3} strokeDasharray="12 8" />
        {parts.map(([x, y], i) => {
          const on = shown(i); const hot = s.hud === i;
          const p = s.items[i] ? spring({frame: f - Math.round((s.items[i].t - s.start) * fps), fps, config: {damping: 12}}) : on ? 1 : 0;
          return (
            <g key={i} transform={`translate(${x},${y}) scale(${0.6 + 0.4 * p})`} opacity={on ? 1 : 0.3}>
              <rect x={-120} y={-52} width={240} height={104} rx={22} fill={hot ? 'rgba(233,185,73,.25)' : 'rgba(8,14,36,.8)'} stroke={hot ? gold : cyan} strokeWidth={hot ? 4 : 2} />
              <text x={0} y={-8} textAnchor="middle" fill={gold} style={{fontFamily: 'Montserrat', fontWeight: 900, fontSize: 30}}>{i + 1}</text>
              <text x={0} y={32} textAnchor="middle" fill={ink} style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 26}}>{families[i]}</text>
            </g>);
        })}
      </svg>
    </AbsoluteFill>
  );
};
const MiniHud: React.FC<{i: number; families: string[]}> = ({i, families}) => (
  <div style={{position: 'absolute', top: 26, right: 30, display: 'flex', gap: 6, direction: 'rtl'}}>
    {families.map((n, k) => (
      <div key={k} style={{...ar, padding: '4px 10px', borderRadius: 10, fontSize: 18, fontWeight: 800,
        color: k === i ? navy : dim, background: k === i ? gold : 'rgba(8,14,36,.6)', border: `1px solid ${k === i ? gold : 'rgba(233,185,73,.3)'}`}}>{n}</div>
    ))}
  </div>
);

// ---------- scene kinds ----------
const Browser: React.FC<{s: Scene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const t = s.start + f / fps;
  const idx = Math.max(0, s.items.filter((it) => it.img && t >= it.t).length - 1);
  const imgs = s.items.filter((it) => it.img);
  const cur = imgs[idx] || {img: s.imgs[0], t: s.start, label: ''};
  const lt = (t - cur.t) / Math.max(1, s.dur);
  const z = 1 + 0.12 * Math.min(1, lt * 1.6);
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
      <div style={{width: 1500, height: 860, borderRadius: 22, overflow: 'hidden', background: '#0e1220', boxShadow: '0 30px 80px rgba(0,0,0,.6)', border: `1.5px solid ${gold}55`}}>
        <div style={{height: 54, background: '#1a2036', display: 'flex', alignItems: 'center', gap: 10, padding: '0 18px'}}>
          {[red, '#F5C451', '#4CD37A'].map((c) => <div key={c} style={{width: 14, height: 14, borderRadius: 7, background: c}} />)}
          <div style={{marginLeft: 20, flex: 1, height: 32, borderRadius: 16, background: '#0b0f1c', color: dim, fontFamily: 'Montserrat', fontSize: 18, display: 'flex', alignItems: 'center', padding: '0 16px', gap: 10}}>
            {cur.logo && <Img src={S(cur.logo)} style={{width: 20, height: 20, objectFit: 'contain'}} />}{s.url || ''}
          </div>
        </div>
        <div style={{position: 'relative', height: 806, overflow: 'hidden'}}>
          {cur.img && <Img src={S(cur.img)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'top', transform: `scale(${z})`, transformOrigin: '50% 30%'}} />}
        </div>
      </div>
      {cur.label && <div style={{position: 'absolute', bottom: 40, left: 0, right: 0, textAlign: 'center'}}>
        <span style={{...ar, background: gold, color: navy, fontWeight: 900, fontSize: 40, padding: '6px 26px', borderRadius: 14}}>{cur.label}</span></div>}
    </AbsoluteFill>
  );
};

const Row: React.FC<{s: Scene; big?: boolean}> = ({s, big}) => (
  <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', padding: '170px 80px 120px'}}>
    <div style={{display: 'flex', flexWrap: 'wrap', gap: 26, justifyContent: 'center', alignItems: 'center', direction: 'rtl', maxWidth: 1700}}>
      {s.items.map((it, i) => <Chip key={i} it={it} start={s.start} big={big} />)}
    </div>
  </AbsoluteFill>
);

const LogoGrid: React.FC<{s: Scene}> = ({s}) => (
  <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', padding: '180px 80px 100px'}}>
    <div style={{display: 'flex', flexWrap: 'wrap', gap: 60, justifyContent: 'center', direction: 'rtl', maxWidth: 1700}}>
      {s.items.map((it, i) => <LogoPop key={i} it={it} start={s.start} />)}
    </div>
  </AbsoluteFill>
);
const LogoPop: React.FC<{it: z.infer<typeof item>; start: number}> = ({it, start}) => {
  const p = usePop(it.t, start);
  if (p <= 0.001) return null;
  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14, transform: `scale(${0.5 + 0.5 * p}) translateY(${(1 - p) * 50}px)`, opacity: Math.min(1, p * 1.5)}}>
      {it.logo ? <Logo src={it.logo} size={170} /> : <div style={{fontSize: 120}}>{it.emoji || '✦'}</div>}
      <span style={{fontFamily: 'Montserrat, Cairo', color: ink, fontWeight: 800, fontSize: 34}}>{it.label}</span>
      {it.sub && <span style={{...ar, color: gold, fontWeight: 700, fontSize: 26}}>{it.sub}</span>}
    </div>
  );
};

const Flow: React.FC<{s: Scene}> = ({s}) => (
  <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', padding: '160px 60px 100px'}}>
    <div style={{display: 'flex', flexWrap: 'wrap', gap: 14, alignItems: 'center', justifyContent: 'center', direction: 'rtl', maxWidth: 1800}}>
      {s.items.map((it, i) => (
        <React.Fragment key={i}>
          {i > 0 && <Arrow t={it.t} start={s.start} />}
          <FlowNode it={it} start={s.start} />
        </React.Fragment>))}
    </div>
  </AbsoluteFill>
);
const Arrow: React.FC<{t: number; start: number}> = ({t, start}) => { const p = usePop(t - 0.15, start); return <span style={{color: gold, fontSize: 64, opacity: p, fontFamily: 'Cairo'}}>←</span>; };
const FlowNode: React.FC<{it: z.infer<typeof item>; start: number}> = ({it, start}) => {
  const p = usePop(it.t, start);
  return (
    <div style={{opacity: p, transform: `scale(${0.6 + 0.4 * p})`, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10}}>
      {it.img && <Img src={S(it.img)} style={{width: 300, height: 170, objectFit: 'cover', borderRadius: 16, border: `2px solid ${gold}88`}} />}
      {it.logo && <Logo src={it.logo} size={90} />}
      <span style={{...ar, color: ink, fontWeight: 800, fontSize: 36, background: 'rgba(8,14,36,.7)', padding: '6px 18px', borderRadius: 14}}>{it.label}</span>
    </div>
  );
};

const Split: React.FC<{s: Scene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const wipe = interpolate(f, [fps * 0.4, fps * 1.4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const tt = s.start + f / fps;
  const typed = (it: z.infer<typeof item>) => interpolate(tt, [it.t, it.t + 1.6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const reveal = (it: z.infer<typeof item>) => interpolate(tt, [it.t + 1.8, it.t + 2.6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const wipeOf = (it: z.infer<typeof item>) => interpolate(tt, [it.t + 0.8, it.t + 2.4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const side = (i: number) => {
    const c = s.clips[i]; const it = s.items[i];
    return (
      <div style={{position: 'relative', width: 900, height: 560, borderRadius: 20, overflow: 'hidden', border: `2px solid ${i ? gold : cyan}88`, background: '#0b1020'}}>
        {c ? <OffthreadVideo src={S(c.src)} muted startFrom={Math.round((c.skip || 0) * fps)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          : it?.img ? <Img src={S(it.img)} style={{width: '100%', height: '100%', objectFit: 'cover', opacity: it.prompt ? reveal(it) : 1}} /> : null}
        {/* picture -> edited picture: the BEFORE image wipes away (Aly: the edit must be visible) */}
        {it?.before && <div style={{position: 'absolute', inset: 0, clipPath: `inset(0 0 0 ${wipeOf(it) * 100}%)`}}>
          <Img src={S(it.before)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          <div style={{position: 'absolute', top: 0, bottom: 0, left: 0, width: 6, background: gold, boxShadow: `0 0 20px ${gold}`}} /></div>}
        {/* text -> picture: the real prompt types, then the picture appears */}
        {it?.prompt && reveal(it) < 1 && <div style={{position: 'absolute', inset: 0, background: `rgba(8,14,36,${0.92 - 0.9 * reveal(it)})`, padding: 34,
          fontFamily: 'Consolas, monospace', fontSize: 25, lineHeight: 1.45, color: '#cfe3ff', direction: 'ltr', textAlign: 'left'}}>
          <span style={{color: gold}}>prompt › </span>{it.prompt.slice(0, Math.floor(it.prompt.length * typed(it)))}</div>}
        {it?.label && <div style={{position: 'absolute', bottom: 16, right: 16, ...ar, background: i ? gold : cyan, color: navy, fontWeight: 900, fontSize: 32, padding: '4px 18px', borderRadius: 12}}>{it.label}</div>}
      </div>);
  };
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', gap: 40, flexDirection: 'row-reverse', paddingTop: 80}}>
      <div style={{transform: `translateX(${(1 - Math.min(1, wipe * 2)) * 80}px)`, opacity: Math.min(1, wipe * 2)}}>{side(0)}</div>
      <div style={{transform: `translateX(${(1 - wipe) * -80}px)`, opacity: wipe}}>{side(1)}</div>
    </AbsoluteFill>
  );
};

const Bts: React.FC<{s: Scene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const t = s.start + f / fps;
  const imgs = s.items.filter((it) => it.img);
  const idx = Math.max(0, imgs.filter((it) => t >= it.t).length - 1);
  const cur = imgs[idx];
  const z = 1 + 0.06 * ((t - (cur?.t || s.start)) / 6);
  if (s.fx === 'diffusion' && cur?.img) {   // noise -> picture, step by step (pre-made noise PNG, cheap to render)
    const k = Math.min(1, (t - s.start) / Math.max(1, s.dur - 0.8)); const steps = Math.floor(k * 30);
    return (
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
        <div style={{position: 'relative', width: 1280, height: 720, borderRadius: 18, overflow: 'hidden', border: `2px solid ${amber}88`}}>
          <Img src={S(cur.img)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: `blur(${(1 - k) * 26}px)`}} />
          <Img src={S('projects/aiworld/v3/noise.png')} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: Math.pow(1 - k, 1.3), mixBlendMode: 'normal'}} />
        </div>
        <div style={{position: 'absolute', top: 60, fontFamily: 'Montserrat', fontWeight: 900, color: gold, fontSize: 40}}>step {steps} / 30</div>
        {cur.label && <div style={{position: 'absolute', bottom: 40, ...ar, color: ink, fontWeight: 800, fontSize: 40, background: 'rgba(8,14,36,.85)', padding: '6px 24px', borderRadius: 14}}>{cur.label}</div>}
      </AbsoluteFill>);
  }
  return (
    <AbsoluteFill>
      {s.clips.map((c, i) => <ClipSeq key={i} c={c} start={s.start} style={{filter: 'brightness(.5) blur(2px)'}} />)}
      <div style={{position: 'absolute', top: 40, left: 50, fontFamily: 'Montserrat', fontWeight: 900, fontSize: 22, letterSpacing: 4, color: amber}}>BEHIND THE SCENES</div>
      {cur?.img && <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', paddingTop: 40}}>
        <Img src={S(cur.img)} style={{maxWidth: 1560, maxHeight: 780, objectFit: 'contain', borderRadius: 18, border: `2px solid ${amber}88`, boxShadow: '0 30px 80px rgba(0,0,0,.6)', transform: `scale(${z})`}} />
      </AbsoluteFill>}
      {cur?.label && <div style={{position: 'absolute', bottom: 36, left: 0, right: 0, textAlign: 'center'}}>
        <span style={{...ar, background: 'rgba(8,14,36,.85)', color: ink, fontWeight: 800, fontSize: 38, padding: '6px 24px', borderRadius: 14, border: `1px solid ${amber}88`}}>{cur.label}</span></div>}
      {!cur && <Row s={s} big />}
    </AbsoluteFill>
  );
};

const Vid: React.FC<{s: Scene}> = ({s}) => (
  <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', padding: '140px 60px 80px'}}>
    <div style={{display: 'flex', flexWrap: 'wrap', gap: 34, justifyContent: 'center', direction: 'rtl', maxWidth: 1820}}>
      {s.items.map((it, i) => <VidCard key={i} it={it} start={s.start} small={s.items.length > 2} />)}
    </div>
  </AbsoluteFill>
);
const VidCard: React.FC<{it: z.infer<typeof item>; start: number; small?: boolean}> = ({it, start, small}) => {
  const p = usePop(it.t, start); const w = small ? 520 : 760;
  if (p <= 0.001) return null;
  return (
    <div style={{display: 'flex', gap: 16, alignItems: 'center', opacity: Math.min(1, p * 1.5), transform: `scale(${0.7 + 0.3 * p})`,
      background: 'rgba(8,14,36,.8)', borderRadius: 20, padding: 14, border: `1.5px solid ${gold}77`}}>
      <div style={{display: 'flex', flexDirection: 'column', gap: 8, width: w}}>
        <Img src={S(it.img)} style={{width: w, height: w * 9 / 16, objectFit: 'cover', borderRadius: 12}} />
        {it.label && <span style={{...ar, color: ink, fontWeight: 800, fontSize: small ? 24 : 32}}>{it.label}</span>}
      </div>
      {it.qr && <Img src={S(it.qr)} style={{width: small ? 150 : 210, height: small ? 150 : 210, borderRadius: 10}} />}
    </div>
  );
};

const Lyr: React.FC<{s: Scene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const t = s.start + f / fps;
  const line = [...s.items].reverse().find((it) => t >= it.t - 0.05);
  const words = line ? s.words.filter((w) => w.t >= line.t - 0.05 && (!line.sub || w.t < Number(line.sub))) : [];
  return (
    <AbsoluteFill>
      {s.clips.map((c, i) => <ClipSeq key={i} c={c} start={s.start} />)}
      <AbsoluteFill style={{background: 'linear-gradient(transparent 45%, rgba(5,8,21,.75))'}} />
      <div style={{position: 'absolute', bottom: 90, left: 80, right: 80, display: 'flex', flexWrap: 'wrap', gap: '6px 18px', justifyContent: 'center', direction: 'rtl'}}>
        {words.map((w, i) => {
          const p = spring({frame: f - Math.round((w.t - s.start) * fps), fps, config: {damping: 11, stiffness: 180}});
          return <span key={i} style={{...ar, fontSize: 78, fontWeight: 900, color: t >= w.t ? gold : 'rgba(243,238,223,.25)', transform: `translateY(${(1 - p) * 30}px)`,
            textShadow: '0 6px 26px rgba(0,0,0,.7)'}}>{w.w}</span>;
        })}
      </div>
    </AbsoluteFill>
  );
};

const Step: React.FC<{s: Scene}> = ({s}) => (
  <AbsoluteFill>
    <div style={{position: 'absolute', top: 60, right: 80, display: 'flex', alignItems: 'center', gap: 20, direction: 'rtl'}}>
      <div style={{width: 120, height: 120, borderRadius: 60, background: gold, color: navy, fontFamily: 'Montserrat', fontWeight: 900, fontSize: 64,
        display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{s.step}</div>
      <span style={{...ar, color: ink, fontWeight: 900, fontSize: 56}}>{s.title}</span>
    </div>
    {s.items.some((it) => it.img) ? <div style={{position: 'absolute', inset: '210px 120px 60px'}}><Browser s={{...s, title: undefined}} /></div> : <Row s={s} big />}
  </AbsoluteFill>
);

const Av: React.FC<{s: Scene; glitch: number[]}> = ({s, glitch}) => (
  <AbsoluteFill>
    {s.clips.map((c, i) => <ClipSeq key={i} c={c} start={s.start} />)}
    {glitch.map((g, i) => <Glitch key={i} at={g} start={s.start} />)}
    <SideStack items={s.items} start={s.start} />
  </AbsoluteFill>
);

const SceneView: React.FC<{s: Scene; families: string[]}> = ({s, families}) => {
  const bg = !['AV', 'CLIP', 'LYR'].includes(s.k);
  const glitch = s.k === 'AV' ? s.clips.slice(1).map((c) => c.from) : [];
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  // motion screens never stand still (freezedetect found 1-5 s still stretches): a slow push over the whole scene
  const push = bg ? interpolate(f, [0, Math.max(1, s.dur * fps)], [1.0, 1.06]) : 1;
  return (
    <AbsoluteFill style={{transform: `scale(${push})`}}>
      {bg && <StarField />}
      {s.k === 'AV' && <Av s={s} glitch={glitch} />}
      {s.k === 'CLIP' && <AbsoluteFill>{s.clips.map((c, i) => <ClipSeq key={i} c={c} start={s.start} />)}
        <SideStack items={s.items} start={s.start} />
        {s.clips.map((c, i) => c.label ? <Sequence key={'l' + i} from={Math.round((c.from - s.start) * 25)} durationInFrames={Math.round(c.dur * 25)}>
          <div style={{position: 'absolute', bottom: 46, left: 60, ...ar, background: 'rgba(8,14,36,.8)', color: gold, fontWeight: 800, fontSize: 34, padding: '6px 20px', borderRadius: 12}}>{c.label}</div></Sequence> : null)}
      </AbsoluteFill>}
      {s.k === 'MAP6' && <JetMap s={s} families={families} />}
      {s.k === 'LOGOS' && <LogoGrid s={s} />}
      {(s.k === 'KT' || s.k === 'NUM' || s.k === 'ICON') && <Row s={s} big />}
      {s.k === 'WEB' && <Browser s={s} />}
      {s.k === 'FLOW' && <Flow s={s} />}
      {s.k === 'SPLIT' && <Split s={s} />}
      {s.k === 'BTS' && <Bts s={s} />}
      {s.k === 'VID' && (s.clips.length ? <AbsoluteFill>{s.clips.map((c, i) => <ClipSeq key={i} c={c} start={s.start} />)}
        <AbsoluteFill style={{background: 'linear-gradient(90deg, transparent 35%, rgba(5,8,21,.85) 70%)'}} />
        <div style={{position: 'absolute', top: 120, bottom: 80, right: 40, width: 980, display: 'flex', flexDirection: 'column', gap: 18, justifyContent: 'center', alignItems: 'flex-end'}}>
          {s.items.map((it, i) => <VidCard key={i} it={it} start={s.start} small />)}</div></AbsoluteFill> : <Vid s={s} />)}
      {s.k === 'LYR' && <Lyr s={s} />}
      {s.k === 'STEP' && <Step s={s} />}
      {!['AV', 'CLIP', 'LYR', 'STEP'].includes(s.k) && <Title text={s.title} start={s.start} />}
    </AbsoluteFill>
  );
};

export const AiWorldV3: React.FC<z.infer<typeof aiV3Schema>> = (p) => {
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
      </div>
    </AbsoluteFill>
  );
};
