// «عالم الـ AI كله» (2026-11-20, RUN_v9). Two compositions:
//  - ai-world-rough: the whole 16:9 timeline as a rough cut (placeholder card per shot, free motion, captions).
//  - ai-world-hud:   ONE transparent overlay element (badge / families / counter / card) -> ProRes 4444 or WebM alpha,
//                    to drop as a layer over the video in CapCut / Premiere (Tip 2).
// Props come from projects/<code>/work/scripts/make_props.py.
import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Sequence, OffthreadVideo, staticFile} from 'remotion';
import {z} from 'zod';
import {fontCss} from '../blocks/theme';

const ink = '#EAF2FF', dim = 'rgba(234,242,255,.62)', cyan = '#38E1FF', gold = '#FFC24B', red = '#FF5A6E', violet = '#8B7BFF';
const TYPE: Record<string, {c: string; n: string}> = {
  A: {c: '#FF8A3D', n: 'A · حقيقي + lipsync'}, B: {c: gold, n: 'B · علي الـ AI'}, C: {c: violet, n: 'C · لقطة سينمائية'},
  D: {c: '#5CF2A8', n: 'D · 3D'}, E: {c: cyan, n: 'E · موشن'}, F: {c: '#FF6FB5', n: 'F · سكرين'},
};
const ar: React.CSSProperties = {fontFamily: 'Cairo, sans-serif', direction: 'rtl', unicodeBidi: 'isolate'};

const shot = z.object({n: z.number(), chapter: z.string(), start: z.number(), dur: z.number(), type: z.string(),
  style: z.string(), world: z.string(), what: z.string(), tool: z.string(), free_paid: z.string(), cost: z.any(), transition: z.string()});
export const aiWorldSchema = z.object({
  fps: z.number().default(25), duration: z.number().default(10), outW: z.number().default(1920),
  shots: z.array(shot).default([]),
  caps: z.array(z.object({a: z.number(), b: z.number(), t: z.string()})).default([]),
  chapters: z.array(z.object({id: z.string(), title: z.string(), start: z.number(), end: z.number()})).default([]),
});
export const aiHudSchema = z.object({
  kind: z.enum(['badge', 'families', 'counter', 'card']).default('badge'),
  title: z.string().default('موديل ≠ أداة ≠ workflow'), sub: z.string().default('Seedance · Higgsfield · صورة ← فيديو ← صوت'),
  from: z.number().default(3), to: z.number().default(28), label: z.string().default('فيديو في الأسبوع'),
  duration: z.number().default(5),
});

const hash = (s: string) => [...s].reduce((h, ch) => (h * 31 + ch.charCodeAt(0)) >>> 0, 7);
const worldBg = (w: string) => {
  const h = hash(w) % 360;
  return `radial-gradient(120% 90% at 30% 20%, hsl(${h} 60% 22%), hsl(${(h + 40) % 360} 55% 9%) 70%, #05070d)`;
};

// --- shared pieces -------------------------------------------------------------------------------
export const Badge: React.FC<{scale?: number}> = ({scale = 1}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 14}});
  return (
    <div style={{position: 'absolute', top: 28 * scale, left: 28 * scale, transform: `scale(${s * scale})`, transformOrigin: 'left top',
      display: 'flex', alignItems: 'center', gap: 10, padding: '8px 18px', borderRadius: 999, background: 'rgba(8,12,24,.72)',
      border: `1.5px solid ${cyan}`, boxShadow: `0 0 18px ${cyan}55`}}>
      <span style={{fontFamily: 'Montserrat', fontWeight: 800, color: cyan, fontSize: 22}}>AI ×</span>
      <span style={{...ar, color: ink, fontSize: 22, fontWeight: 700}}>بإشراف علي</span>
    </div>
  );
};

const Families: React.FC = () => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const fam = ['التوليد', 'الـ LLMs والـ agents', 'السكريبتات الذكية', 'الـ MCP', 'الـ skills', 'الإنسان'];
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(3, 420px)', gap: 26, direction: 'rtl'}}>
        {fam.map((t, i) => {
          const s = spring({frame: f - i * 0.9 * fps, fps, config: {damping: 12}});
          return (
            <div key={t} style={{...ar, transform: `translateY(${(1 - s) * 60}px) scale(${0.6 + 0.4 * s})`, opacity: s,
              padding: '26px 30px', borderRadius: 22, background: 'rgba(10,16,32,.78)', border: `2px solid ${i === 5 ? gold : cyan}`,
              boxShadow: `0 0 26px ${(i === 5 ? gold : cyan)}44`, color: ink, fontSize: 40, fontWeight: 800, display: 'flex', gap: 18, alignItems: 'center'}}>
              <span style={{fontFamily: 'Montserrat', color: i === 5 ? gold : cyan, fontSize: 48}}>{i + 1}</span>{t}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const Counter: React.FC<{from: number; to: number; label: string}> = ({from, to, label}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const p = interpolate(f, [0.4 * fps, 2.4 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: (x) => 1 - Math.pow(1 - x, 3)});
  const v = Math.round(from + (to - from) * p);
  const hit = spring({frame: f - 2.4 * fps, fps, config: {damping: 8}});
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
      <div style={{fontFamily: 'Montserrat', fontWeight: 900, fontSize: 260, color: ink, transform: `scale(${1 + 0.12 * hit})`,
        textShadow: `0 0 40px ${gold}aa`}}>{v.toLocaleString('en-US')}</div>
      <div style={{...ar, color: gold, fontSize: 56, fontWeight: 800, marginTop: -20}}>{label}</div>
    </AbsoluteFill>
  );
};

const Card: React.FC<{title: string; sub: string}> = ({title, sub}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 13}});
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'flex-end', paddingBottom: 170}}>
      <div style={{...ar, transform: `translateY(${(1 - s) * 80}px)`, opacity: s, minWidth: 900, maxWidth: 1500, textAlign: 'center',
        padding: '28px 46px', borderRadius: 26, background: 'rgba(8,12,24,.8)', border: `2px solid ${cyan}`, boxShadow: `0 0 30px ${cyan}44`}}>
        <div style={{color: ink, fontSize: 58, fontWeight: 900}}>{title}</div>
        <div style={{color: dim, fontSize: 32, fontWeight: 600, marginTop: 6}}>{sub}</div>
      </div>
    </AbsoluteFill>
  );
};

// --- transparent overlay (one element) --------------------------------------------------------------
export const AiHud: React.FC<z.infer<typeof aiHudSchema>> = (p) => (
  <AbsoluteFill style={{background: 'transparent'}}>
    <style>{fontCss}</style>
    {p.kind === 'badge' && <Badge scale={1.4} />}
    {p.kind === 'families' && <Families />}
    {p.kind === 'counter' && <Counter from={p.from} to={p.to} label={p.label} />}
    {p.kind === 'card' && <Card title={p.title} sub={p.sub} />}
  </AbsoluteFill>
);

// --- rough cut --------------------------------------------------------------------------------------
// grey Blender blockouts (tools/blender/aiworld_blockouts.py) shown in the rough cut for D shots
const BLOCK: Record<string, string> = {C01: 'jet', C05: 'jet', C11: 'jet', C12: 'jet', C02: 'lab', C07: 'lab', C02f: 'bridge'};
const Blockout: React.FC<{s: z.infer<typeof shot>; clip: string}> = ({s, clip}) => (
  <AbsoluteFill style={{background: '#05070d'}}>
    <OffthreadVideo src={staticFile(`projects/aiworld/${clip}_blockout.mp4`)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
    <div style={{...ar, position: 'absolute', top: 90, right: 60, background: 'rgba(6,9,18,.75)', border: '2px solid #5CF2A8', borderRadius: 16,
      padding: '10px 22px', color: ink, fontSize: 34, fontWeight: 800}}>Blender blockout — {s.what}</div>
  </AbsoluteFill>
);

const ShotView: React.FC<{s: z.infer<typeof shot>; bare?: boolean}> = ({s, bare}) => {
  if (s.type === 'D' && BLOCK[s.chapter] && !bare) return <Blockout s={s} clip={BLOCK[s.chapter]} />;
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const T = TYPE[s.type] || TYPE.E;
  const push = interpolate(f, [0, s.dur * fps], [1.0, 1.08]);
  const pulse = 0.5 + 0.5 * Math.cos((f / fps) * Math.PI * 1.3);   // ~1.5 s visual event marker
  const inn = spring({frame: f, fps, config: {damping: 14}});
  const paid = s.free_paid === 'paid';
  return (
    <AbsoluteFill style={{background: worldBg(s.world), overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${push})`}}>
        {[...Array(14)].map((_, i) => {
          const x = (hash(s.world + i) % 1000) / 10, y = (hash(i + s.what) % 1000) / 10;
          return <div key={i} style={{position: 'absolute', left: `${x}%`, top: `${(y + (f / fps) * (4 + i % 5)) % 100}%`, width: 6 + i % 4 * 4,
            height: 6 + i % 4 * 4, borderRadius: 99, background: T.c, opacity: 0.18 + 0.2 * pulse}} />;
        })}
      </AbsoluteFill>
      {!bare && <div style={{position: 'absolute', inset: '120px 140px 210px', borderRadius: 30, border: `3px ${paid ? 'dashed' : 'solid'} ${T.c}`,
        background: 'rgba(6,9,18,.55)', transform: `scale(${0.92 + 0.08 * inn})`, opacity: inn, display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center', gap: 18, padding: 40}}>
        <div style={{...ar, color: T.c, fontSize: 38, fontWeight: 900}}>{T.n} · {s.style}</div>
        <div style={{...ar, color: ink, fontSize: 64, fontWeight: 900, textAlign: 'center', lineHeight: 1.25}}>{s.what}</div>
        <div style={{...ar, color: dim, fontSize: 32}}>العالم: {s.world}</div>
        <div style={{...ar, color: paid ? gold : '#5CF2A8', fontSize: 30, fontWeight: 800, marginTop: 8}}>
          {paid ? `لقطة مدفوعة مطلوبة — ${s.tool} — ${s.cost}` : `مجاني — ${s.tool}`}
        </div>
      </div>}
      <div style={{position: 'absolute', top: 34, right: 40, fontFamily: 'Montserrat', color: dim, fontSize: 24}}>#{s.n} · {s.chapter}</div>
    </AbsoluteFill>
  );
};

// Layout is drawn at 1920x1080 and scaled to the output width (outW 1280 = 720p proxy; CLI --scale gave 720.036 px).
export const AiWorldRough: React.FC<z.infer<typeof aiWorldSchema>> = (p) => {
  const {width} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: '#05070d', overflow: 'hidden'}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `scale(${width / 1920})`, transformOrigin: 'left top'}}>
        <RoughInner {...p} />
      </div>
    </AbsoluteFill>
  );
};

const RoughInner: React.FC<z.infer<typeof aiWorldSchema>> = ({shots, caps, chapters}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const t = f / fps;
  const cap = caps.find((c) => t >= c.a && t < c.b);
  const ch = chapters.find((c) => t >= c.start && t < c.end);
  return (
    <AbsoluteFill style={{background: '#05070d'}}>
      <style>{fontCss}</style>
      {shots.map((s) => {
        const fam = s.chapter === 'C01' && s.type === 'E';
        const c28 = s.chapter === 'C00' && s.type === 'E';
        const c474 = s.chapter === 'C065' && s.what.includes('474K');
        return (
          <Sequence key={s.n} from={Math.round(s.start * fps)} durationInFrames={Math.max(1, Math.round(s.dur * fps))}>
            <ShotView s={s} bare={fam || c28 || c474} />
            {fam && <Families />}
            {c28 && <Counter from={3} to={28} label="فيديو في الأسبوع" />}
            {c474 && <Counter from={0} to={474000} label="مشاهدة في آخر شهر" />}
          </Sequence>
        );
      })}
      <Badge />
      {ch && <div style={{...ar, position: 'absolute', left: 40, bottom: 34, color: dim, fontSize: 26, fontWeight: 700}}>{ch.title}</div>}
      {cap && <div style={{...ar, position: 'absolute', left: 0, right: 0, bottom: 96, textAlign: 'center'}}>
        <span style={{background: 'rgba(0,0,0,.62)', color: ink, fontSize: 52, fontWeight: 800, padding: '6px 22px', borderRadius: 14}}>{cap.t}</span>
      </div>}
    </AbsoluteFill>
  );
};
