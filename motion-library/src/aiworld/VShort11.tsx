// NATIVE VERTICAL shorts from v11 (Aly 2026-11-24: «مش عايز إطار horizontal جوه الـ vertical»). The boards are RE-LAID OUT on a
// 1080x1920 stage by work/scripts/shorts_vprops.py (vertical packer, overlap = 0); this file draws them with the approved v11 parts.
// Full-frame generated clips: their 9:16 regeneration (clip.vertical) fills the frame; until then the 16:9 file is a placeholder crop.
// Talking circles sit in the title band beside the title. Captions under the boards, handles footer.
import React from 'react';
import {AbsoluteFill, Easing, Img, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {fontCss} from '../blocks/theme';
import {E, stickerBorder} from '../enta/kit';
import {EntaGlitch} from '../enta/EntaPop';
import {enter} from '../blocks/anim';
import {Rtl} from './V4';
import {ClipSeq, Diagram, Diffusion, GlitchCut, V11Opts} from './V11';

const gold = '#E9B949', ink = '#F3EEDF', navy = '#0B1430';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const S = (p?: string) => (p ? staticFile(p) : '');

const clip = z.object({src: z.string(), from: z.number(), dur: z.number(), skip: z.number().optional(), rate: z.number().optional(),
  circle: z.object({x: z.number(), y: z.number(), r: z.number()}).optional(), fx: z.number().optional(), fy: z.number().optional(),
  cin: z.boolean().optional(), cout: z.boolean().optional(), vertical: z.boolean().optional()});
const scene = z.object({k: z.string(), start: z.number(), dur: z.number(), title: z.string().nullable().optional(), items: z.array(z.record(z.string(), z.any())).default([]),
  clips: z.array(clip).default([]), url: z.string().optional(), fx: z.string().optional(), hud: z.number().optional(), glitch: z.array(z.number()).default([]),
  words: z.array(z.object({t: z.number(), w: z.string()})).default([]), fam: z.array(z.number()).default([])});
export const vshortSchema = z.object({
  fps: z.number().default(25), duration: z.number().default(10),
  scenes: z.array(scene).default([]), faces: z.array(clip).default([]),
  pieces: z.array(z.object({a: z.number(), b: z.number(), o: z.number()})).default([]),
  title: z.string().default(''), hook: z.string().default(''), cta: z.string().default(''), ctaFrom: z.number().default(9999),
  words: z.array(z.object({a: z.number(), b: z.number(), w: z.string()})).default([]), series: z.string().default(''),
  end: z.object({from: z.number(), thumb: z.string(), line1: z.string(), line2: z.string()}).optional(),
});
type Scene = z.infer<typeof scene>;
type P = z.infer<typeof vshortSchema>;

// ---------- stars for a 1080x1920 frame (same look as v11: navy + gold asterisks drifting on time) ----------
const VStars: React.FC = () => {
  const f = useCurrentFrame();
  const Wd = 13 * 92, drift = f * 0.22;
  const st: React.ReactNode[] = [];
  for (let r = 0; r < 25; r++) for (let c = 0; c < 13; c++) {
    const k = r * 13 + c, x = (((c * 92 + (r % 2) * 46 + drift) % Wd) + Wd) % Wd - 70, y = r * 80 - 20, s = 1 + ((r * 7 + c) % 3) * 0.12;
    st.push(<g key={k} transform={`translate(${x},${y}) rotate(${(k * 37) % 72}) scale(${s})`} opacity={0.3 + 0.2 * Math.sin(f / 40 + k)}>
      {[0, 72, 144, 216, 288].map((q) => <line key={q} x1={0} y1={0} x2={0} y2={-9} stroke={gold} strokeWidth={1.8} strokeLinecap="round" transform={`rotate(${q})`} />)}</g>);
  }
  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 70% at 50% 40%, #16245a 0%, ${navy} 55%, #050815 100%)`, overflow: 'hidden'}}>
      <svg width={1080} height={1920}>{st}</svg>
      <AbsoluteFill style={{background: 'radial-gradient(70% 40% at 50% 35%, rgba(255,159,67,.10), transparent 70%)'}} />
    </AbsoluteFill>
  );
};

// a full-frame clip: the 9:16 regeneration fills the frame; a 16:9 placeholder is cropped around its centre (flagged in the props script)
const VClipSeq: React.FC<{c: z.infer<typeof clip>; start: number}> = ({c, start}) => <ClipSeq c={c} start={start} />;

const VBrowser: React.FC<{s: Scene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const pages = s.items.filter((d) => d.k === 'page');
  const cur = [...pages].reverse().find((d) => f >= d.at) ?? pages[0];
  if (!cur) return null;
  const p = enter(f, fps, cur.at), o = interpolate(f, [(cur.out ?? s.dur * fps) - 10, cur.out ?? s.dur * fps], [1, 0], clamp);
  const Wd = 960, H = 980;
  return (
    <div style={{position: 'absolute', left: 60, top: 400, width: Wd, height: H + 44, borderRadius: 18, overflow: 'hidden', background: '#0e1220',
      boxShadow: '0 30px 80px rgba(0,0,0,.6)', ...stickerBorder(6), transform: `translateY(${(1 - p) * 50}px) scale(${0.92 + 0.08 * p})`, opacity: Math.min(1, p * 1.5) * o}}>
      <div style={{height: 44, background: '#1a2036', display: 'flex', alignItems: 'center', gap: 9, padding: '0 16px'}}>
        {['#FF5A6E', '#F5C451', '#4CD37A'].map((c) => <div key={c} style={{width: 13, height: 13, borderRadius: 7, background: c}} />)}
        <div style={{marginLeft: 18, flex: 1, height: 26, borderRadius: 13, background: '#0b0f1c', color: 'rgba(243,238,223,.7)', fontFamily: 'Montserrat', fontSize: 16,
          display: 'flex', alignItems: 'center', padding: '0 14px'}}>{cur.url ?? s.url ?? ''}</div>
      </div>
      <div style={{width: Wd, height: H, overflow: 'hidden', position: 'relative'}}>
        {/* the whole page width, scrolling down slowly (a still page = freeze) */}
        <Img src={S(cur.src)} style={{position: 'absolute', left: 0, width: Wd,
          top: interpolate(f, [cur.at + 15, cur.out ?? s.dur * fps], [0, -H * 0.9], {...clamp, easing: Easing.inOut(Easing.sin)})}} />
      </div>
    </div>
  );
};

// the 6 families as a vertical «jet»: nose up, parts in two columns (first family top-right)
const VJetMap: React.FC<{s: Scene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const fams = ['التوليد', 'الـ LLMs والـ agents', 'السكريبتات', 'الـ MCP', 'الـ skills', 'الإنسان'];
  const pos = [[790, 560], [290, 560], [790, 880], [290, 880], [790, 1200], [290, 1200]];
  const out = interpolate(f, [s.dur * fps - 12, s.dur * fps - 2], [1, 0], clamp);
  return (
    <AbsoluteFill style={{opacity: out}}>
      <svg width={1080} height={1920} viewBox="-540 -960 1080 1920" style={{position: 'absolute', inset: 0}}>
        <g transform="translate(0,-80) scale(1.55)">
          <path d="M0,-330 L50,-120 L290,0 L290,45 L50,10 L35,190 L100,240 L100,265 L0,245 L-100,265 L-100,240 L-35,190 L-50,10 L-290,45 L-290,0 L-50,-120 Z"
            fill="rgba(95,211,230,.10)" stroke="#5FD3E6" strokeOpacity={0.75} strokeWidth={2} strokeDasharray="10 7" />
        </g>
      </svg>
      {pos.map(([x, y], i) => {
        const at = s.fam[i] !== undefined ? s.fam[i] : 0;
        const show = s.fam.length ? f >= at : true, p = s.fam.length ? enter(f, fps, at) : 1, hot = s.hud === i;
        return (
          <div key={i} style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) scale(${0.5 + 0.5 * p})`, opacity: show ? 1 : 0.25,
            background: hot ? E.mustard : E.paper, color: E.ink, borderRadius: 14, padding: '10px 22px', minWidth: 330, textAlign: 'center', ...stickerBorder(5),
            fontFamily: 'Cairo', boxShadow: '0 12px 24px rgba(0,0,0,.45)'}}>
            <div style={{fontFamily: 'Montserrat', fontWeight: 900, fontSize: 38, color: E.orange}}>{i + 1}</div>
            <div style={{fontWeight: 900, fontSize: 38, whiteSpace: 'nowrap'}}><Rtl text={fams[i]} /></div>
          </div>);
      })}
    </AbsoluteFill>
  );
};

const VScene: React.FC<{s: Scene}> = ({s}) => {
  const video = ['AV', 'CLIP', 'LYR'].includes(s.k);
  return (
    <AbsoluteFill>
      {video ? <AbsoluteFill>{s.clips.map((c, i) => <VClipSeq key={i} c={c} start={s.start} />)}</AbsoluteFill> : null}
      {s.glitch.map((g, i) => <GlitchCut key={'g' + i} s={s as never} g={g} />)}
      {s.k === 'MAP6' && <VJetMap s={s} />}
      {s.k === 'WEB' && <VBrowser s={s} />}
      {s.fx === 'diffusion' && <Diffusion s={s as never} />}
      {video && s.items.some((d) => !['circle', 'line', 'brand', 'subscribe'].includes(d.k)) ? <AbsoluteFill style={{background: 'rgba(5,8,21,.45)'}} /> : null}
      <Diagram items={s.items.filter((d) => !['circle', 'line', 'brand', 'subscribe', 'page', 'split'].includes(d.k))} />
    </AbsoluteFill>
  );
};

// the talking face (circle) lives in the title band, right side
const BandFace: React.FC<{c: z.infer<typeof clip>}> = ({c}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const dur = Math.round(c.dur * fps), r = 95;
  const p = c.cin ? 1 : enter(f, fps, 0), o = c.cout ? 1 : interpolate(f, [dur - 8, dur], [1, 0], clamp);
  const S36 = r * 3.6, vl = c.fx != null ? r - (c.fx * 1920 - 420) * S36 / 1080 : -r * 0.8, vt = c.fy != null ? r - c.fy * S36 : -r * 0.38;
  return (
    <div style={{position: 'absolute', left: 1080 - 40 - 2 * r, top: 135, width: r * 2, height: r * 2, borderRadius: '50%', overflow: 'hidden', border: `6px solid ${E.white}`,
      boxShadow: '0 14px 30px rgba(0,0,0,.55)', opacity: Math.min(1, p * 1.6) * o, transform: `scale(${0.6 + 0.4 * p})`, background: navy}}>
      <OffthreadVideo src={S(c.src)} muted startFrom={Math.round((c.skip || 0) * fps)} style={{position: 'absolute', width: S36, height: S36, objectFit: 'cover',
        left: Math.min(0, Math.max(2 * r - S36, vl)), top: Math.min(0, Math.max(2 * r - S36, vt))}} />
    </div>
  );
};

const TitleBand: React.FC<{p: P; t: number; face: boolean}> = ({p, t, face}) => {
  const f = useCurrentFrame();
  const hookEnd = p.hook ? 2.6 : 0;
  const mode = t >= p.ctaFrom && p.cta ? 'cta' : t < hookEnd ? 'hook' : 'title';
  const at = mode === 'cta' ? p.ctaFrom : mode === 'hook' ? 0 : hookEnd;
  const k = enter(f, 25, Math.round(at * 25));
  const text = mode === 'cta' ? p.cta : mode === 'hook' ? p.hook : p.title;
  const big = mode === 'hook';
  return (
    <div style={{position: 'absolute', top: 140, left: 40, right: face ? 260 : 40, height: 190, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 8}}>
      {p.series && mode === 'title' ? <div style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 30, color: gold, opacity: Math.min(1, k * 1.5)}}><Rtl text={`سلسلة «${p.series}»`} /></div> : null}
      <div style={{background: mode === 'cta' ? gold : E.paper, color: E.ink, fontFamily: 'Cairo', fontWeight: 900, fontSize: big ? 70 : 50, padding: big ? '6px 36px' : '4px 26px',
        borderRadius: 14, ...stickerBorder(6), transform: `rotate(-1.2deg) scale(${0.6 + 0.4 * k})`, opacity: Math.min(1, k * 1.6), textAlign: 'center', lineHeight: 1.3}}>
        <Rtl text={text} hi={E.orange} /></div>
    </div>
  );
};

const runs = (ws: {a: number; b: number; w: string}[]) => {   // English words next to each other = ONE left-to-right run
  const out: {ar: boolean; w: typeof ws}[] = [];
  for (const w of ws) { const ar = /[؀-ۿ]/.test(w.w); const l = out[out.length - 1]; if (l && !ar && !l.ar) l.w.push(w); else out.push({ar, w: [w]}); }
  return out;
};
const Caps: React.FC<{words: P['words']; t: number}> = ({words, t}) => {
  const groups: {a: number; b: number; w: P['words']}[] = [];
  for (const w of words) {
    const g = groups[groups.length - 1];
    if (!g || g.w.length >= 5 || w.a - g.b > 0.35 || /[.؟?!]$/.test(g.w[g.w.length - 1].w)) groups.push({a: w.a, b: w.b, w: [w]});
    else {g.w.push(w); g.b = w.b;}
  }
  const g = groups.find((x, i) => t >= x.a - 0.05 && t < (groups[i + 1]?.a ?? x.b + 0.4) && t < x.b + 0.6);
  if (!g) return null;
  return (
    <div style={{position: 'absolute', top: 1450, left: 50, right: 50, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '4px 18px', direction: 'rtl'}}>
      {runs(g.w).map((r, i) => <bdi key={i} style={{fontFamily: 'Cairo', fontWeight: 900, fontSize: 62, textShadow: '0 5px 18px rgba(0,0,0,.8)', display: 'inline-flex', gap: '0 16px',
        direction: r.ar ? 'rtl' : 'ltr'}}>{r.w.map((w, j) => <span key={j} style={{color: t >= w.a ? gold : ink}}>{w.w.replace(/[.،,:؟?!]+$/, '')}</span>)}</bdi>)}
    </div>
  );
};

const Footer: React.FC = () => (
  <div style={{position: 'absolute', left: 0, right: 0, top: 1700, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 16, direction: 'ltr', opacity: 0.9}}>
    <Img src={staticFile('projects/aiworld/v6/imgs/v7__logo_face_full.png')} style={{width: 46, filter: 'drop-shadow(0 2px 6px rgba(0,0,0,.6))'}} />
    {[['youtube.png', '@AlyShorosh'], ['tiktok.png', '@alyshorosh'], ['instagram.ico', '@alyshorosh'], ['facebook.png', 'aly.shorosh']].map(([l, t]) => (
      <div key={l} style={{display: 'flex', alignItems: 'center', gap: 6}}>
        <Img src={staticFile('projects/aiworld/v6/logos/' + l)} style={{width: 24, height: 24, objectFit: 'contain'}} />
        <span style={{fontFamily: 'Montserrat', fontWeight: 700, fontSize: 21, color: ink, textShadow: '0 2px 6px rgba(0,0,0,.85)'}}>{t}</span></div>))}
  </div>
);

const EndCard: React.FC<{e: NonNullable<P['end']>}> = ({e}) => {
  const f = useCurrentFrame(); const k = enter(f, 25, 0);
  return (
    <AbsoluteFill style={{background: 'rgba(5,8,21,.9)', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 34, opacity: Math.min(1, k * 1.6)}}>
      <div style={{fontFamily: 'Cairo', fontWeight: 900, fontSize: 62, color: gold}}><Rtl text={e.line1} /></div>
      <div style={{width: 940, aspectRatio: '16/9', borderRadius: 18, overflow: 'hidden', ...stickerBorder(8), transform: `scale(${0.8 + 0.2 * k})`}}>
        <Img src={staticFile(e.thumb)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></div>
      <div style={{fontFamily: 'Cairo', fontWeight: 900, fontSize: 50, color: ink}}><Rtl text={e.line2} /></div>
    </AbsoluteFill>
  );
};

export const AiWorldVShort11: React.FC<P> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const t = f / fps;
  const pc = [...p.pieces].reverse().find((x) => t >= x.o);
  const ts = pc ? pc.a + (t - pc.o) : 0;
  const faceNow = p.faces.some((c) => ts >= c.from && ts < c.from + c.dur);
  return (
    <AbsoluteFill style={{background: navy, overflow: 'hidden'}}>
      <style>{fontCss}</style>
      <VStars />
      <V11Opts.Provider value={{noTitle: true, noLyrics: true, W: 1080, H: 1920}}>
        {p.pieces.map((pc2, i) => {
          const from = Math.round(pc2.o * fps), dur = Math.max(1, Math.round((pc2.b - pc2.a) * fps)), a = Math.round(pc2.a * fps);
          return (
            <Sequence key={i} from={from} durationInFrames={dur}>
              <Sequence from={-a} layout="none">
                {p.scenes.filter((s) => s.start < pc2.b && s.start + s.dur > pc2.a).map((s, j) => (
                  <Sequence key={j} from={Math.round(s.start * fps)} durationInFrames={Math.max(1, Math.round(s.dur * fps))}><VScene s={s} /></Sequence>))}
                {p.faces.filter((c) => c.from < pc2.b && c.from + c.dur > pc2.a).map((c, j) => (
                  <Sequence key={'f' + j} from={Math.round(c.from * fps)} durationInFrames={Math.max(1, Math.round(c.dur * fps))}><BandFace c={c} /></Sequence>))}
              </Sequence>
            </Sequence>);
        })}
      </V11Opts.Provider>
      {p.pieces.slice(1).map((pc2, i) => (
        <Sequence key={'g' + i} from={Math.round(pc2.o * fps) - 3} durationInFrames={8}><EntaGlitch seed={i * 13 + 5} strength={1} previewBg="" /></Sequence>))}
      <TitleBand p={p} t={t} face={faceNow} />
      <Caps words={p.words} t={t} />
      <Footer />
      {p.end ? <Sequence from={Math.round(p.end.from * fps)}><EndCard e={p.end} /></Sequence> : null}
    </AbsoluteFill>
  );
};
