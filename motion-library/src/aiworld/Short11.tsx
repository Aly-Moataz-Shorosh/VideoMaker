// Vertical SHORTS from the approved v11 world (Aly 2026-11-24, reach method / skill aly-reach-method).
// The 1920x1080 v11 stage is shown through an automatic CAMERA (per-frame cx, cy, zoom from shorts_props.py: it follows the items on
// screen) inside a 1080x1100 window; the short has its own title band (hook text → title → CTA), word captions and a handles footer.
// Pieces = ranges of the v11 timeline (seconds) played one after another; a short glitch marks every jump.
import React from 'react';
import {AbsoluteFill, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {fontCss} from '../blocks/theme';
import {E, stickerBorder} from '../enta/kit';
import {EntaGlitch} from '../enta/EntaPop';
import {enter} from '../blocks/anim';
import {Rtl} from './V4';
import {aiV11Schema, FaceShot, SceneView, StarField, V11Opts} from './V11';

const gold = '#E9B949', ink = '#F3EEDF', navy = '#0B1430';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const VIEW = {top: 330, h: 1100};   // the window on the stage

export const short11Schema = aiV11Schema.extend({
  pieces: z.array(z.object({a: z.number(), b: z.number(), o: z.number()})).default([]),
  cam: z.array(z.array(z.number())).default([]),          // per OUTPUT frame: [cx, cy, zoom] in stage px
  title: z.string().default(''), hook: z.string().default(''), cta: z.string().default(''), ctaFrom: z.number().default(9999),
  words: z.array(z.object({a: z.number(), b: z.number(), w: z.string()})).default([]),   // OUTPUT time
  series: z.string().default(''),
  end: z.object({from: z.number(), thumb: z.string(), line1: z.string(), line2: z.string()}).optional(),
});

const TitleBand: React.FC<{p: z.infer<typeof short11Schema>; t: number}> = ({p, t}) => {
  const f = useCurrentFrame();
  const hookEnd = p.hook ? 2.6 : 0;
  const mode = t >= p.ctaFrom && p.cta ? 'cta' : t < hookEnd ? 'hook' : 'title';
  const at = mode === 'cta' ? p.ctaFrom : mode === 'hook' ? 0 : hookEnd;
  const k = enter(f, 25, Math.round(at * 25));
  const text = mode === 'cta' ? p.cta : mode === 'hook' ? p.hook : p.title;
  const big = mode === 'hook';
  return (
    <div style={{position: 'absolute', top: 150, left: 40, right: 40, height: 160, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 8}}>
      {p.series && mode === 'title' ? <div style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 30, color: gold, opacity: Math.min(1, k * 1.5)}}><Rtl text={`سلسلة «${p.series}»`} /></div> : null}
      <div style={{background: mode === 'cta' ? gold : E.paper, color: E.ink, fontFamily: 'Cairo', fontWeight: 900, fontSize: big ? 72 : 54, padding: big ? '6px 40px' : '4px 30px',
        borderRadius: 14, ...stickerBorder(6), transform: `rotate(-1.2deg) scale(${0.6 + 0.4 * k})`, opacity: Math.min(1, k * 1.6), maxWidth: 1000, textAlign: 'center', lineHeight: 1.3}}>
        <Rtl text={text} hi={E.orange} /></div>
    </div>
  );
};

// English words next to each other stay in ONE left-to-right run («digital twin», not «twin digital»)
const runs = (ws: {a: number; b: number; w: string}[]) => {
  const out: {ar: boolean; w: typeof ws}[] = [];
  for (const w of ws) { const ar = /[؀-ۿ]/.test(w.w); const l = out[out.length - 1]; if (l && !ar && !l.ar) l.w.push(w); else out.push({ar, w: [w]}); }
  return out;
};
const Caps: React.FC<{words: {a: number; b: number; w: string}[]; t: number}> = ({words, t}) => {
  // groups of up to 5 words (a new group after a pause > .35 s); the word being said is gold
  const groups: {a: number; b: number; w: {a: number; b: number; w: string}[]}[] = [];
  for (const w of words) {
    const g = groups[groups.length - 1];
    if (!g || g.w.length >= 5 || w.a - g.b > 0.35 || /[.؟?!]$/.test(g.w[g.w.length - 1].w)) groups.push({a: w.a, b: w.b, w: [w]});
    else {g.w.push(w); g.b = w.b;}
  }
  const g = groups.find((x, i) => t >= x.a - 0.05 && t < (groups[i + 1]?.a ?? x.b + 0.4) && t < x.b + 0.6);
  if (!g) return null;
  return (
    <div style={{position: 'absolute', top: VIEW.top + VIEW.h + 40, left: 50, right: 50, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '4px 18px', direction: 'rtl'}}>
      {runs(g.w).map((r, i) => <bdi key={i} style={{fontFamily: 'Cairo', fontWeight: 900, fontSize: 62, textShadow: '0 5px 18px rgba(0,0,0,.8)',
        display: 'inline-flex', gap: '0 16px', direction: r.ar ? 'rtl' : 'ltr'}}>
        {r.w.map((w, j) => <span key={j} style={{color: t >= w.a ? gold : ink}}>{w.w.replace(/[.،,:؟?!]+$/, '')}</span>)}</bdi>)}
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

const EndCard: React.FC<{e: NonNullable<z.infer<typeof short11Schema>['end']>}> = ({e}) => {
  const f = useCurrentFrame(); const k = enter(f, 25, 0);
  return (
    <AbsoluteFill style={{background: 'rgba(5,8,21,.88)', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 34, opacity: Math.min(1, k * 1.6)}}>
      <div style={{fontFamily: 'Cairo', fontWeight: 900, fontSize: 62, color: gold}}><Rtl text={e.line1} /></div>
      <div style={{width: 900, aspectRatio: '16/9', borderRadius: 18, overflow: 'hidden', ...stickerBorder(8), transform: `scale(${0.8 + 0.2 * k})`}}>
        <Img src={staticFile(e.thumb)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></div>
      <div style={{fontFamily: 'Cairo', fontWeight: 900, fontSize: 50, color: ink}}><Rtl text={e.line2} /></div>
    </AbsoluteFill>
  );
};

export const AiWorldShort11: React.FC<z.infer<typeof short11Schema>> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const t = f / fps;
  const cam = p.cam[Math.min(p.cam.length - 1, f)] ?? [960, 540, 0.5625];
  const [cx, cy, zm] = cam;
  const tx = 540 - cx * zm, ty = VIEW.h / 2 - cy * zm;
  return (
    <AbsoluteFill style={{background: navy, overflow: 'hidden'}}>
      <style>{fontCss}</style>
      <AbsoluteFill style={{transform: 'scale(1.78)', transformOrigin: '50% 50%'}}><div style={{position: 'absolute', left: -420, top: 420, width: 1920, height: 1080}}><StarField /></div></AbsoluteFill>
      <div style={{position: 'absolute', left: 0, top: VIEW.top, width: 1080, height: VIEW.h, overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `translate(${tx}px, ${ty}px) scale(${zm})`, transformOrigin: '0 0'}}>
          <V11Opts.Provider value={{noTitle: true, noLyrics: true}}>
            {p.pieces.map((pc, i) => {
              const from = Math.round(pc.o * fps), dur = Math.max(1, Math.round((pc.b - pc.a) * fps));
              const a = Math.round(pc.a * fps);
              return (
                <Sequence key={i} from={from} durationInFrames={dur}>
                  <Sequence from={-a} layout="none">
                    {p.scenes.filter((s) => s.start < pc.b && s.start + s.dur > pc.a).map((s, j) => (
                      <Sequence key={j} from={Math.round(s.start * fps)} durationInFrames={Math.max(1, Math.round(s.dur * fps))}>
                        <SceneView s={s} families={p.families} subs={p.subs} />
                      </Sequence>))}
                    {p.faces.filter((c) => c.from < pc.b && c.from + c.dur > pc.a).map((c, j) => <FaceShot key={'f' + j} c={c} />)}
                  </Sequence>
                </Sequence>);
            })}
          </V11Opts.Provider>
        </div>
      </div>
      {p.pieces.slice(1).map((pc, i) => (
        <Sequence key={'g' + i} from={Math.round(pc.o * fps) - 3} durationInFrames={8}>
          <div style={{position: 'absolute', left: 0, top: VIEW.top, width: 1080, height: VIEW.h, overflow: 'hidden'}}><EntaGlitch seed={i * 13 + 5} strength={1} previewBg="" /></div>
        </Sequence>))}
      <TitleBand p={p} t={t} />
      <Caps words={p.words} t={t} />
      <Footer />
      {p.end ? <Sequence from={Math.round(p.end.from * fps)}><EndCard e={p.end} /></Sequence> : null}
      {void interpolate(0, [0, 1], [0, 1], clamp)}
    </AbsoluteFill>
  );
};
