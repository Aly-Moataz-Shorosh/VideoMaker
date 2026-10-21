import React from 'react';
import {AbsoluteFill, Audio, Easing, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Captions} from '../templates/Captions';
import {CommentCta} from '../templates/CommentCta';
import {commentCtaSchema} from '../templates/CommentCta';
import {applyPack} from '../blocks/theme';
import {fontCss} from '../blocks/theme';
import {FilmBg, FilmFx, Halftone, K, lin, spr} from './kit';
import {filmScenes} from './scenes';
import {vhsScenes} from '../vhs/scenes';
import {VhsBg, VhsFx} from '../vhs/kit';
import {cairoScenes} from '../cairo/scenes';
import {histScenes} from '../hist/world';
import {popScenes} from '../pop/scenes';
import {PopBg, PopFx, popFontCss} from '../pop/kit';
import {glassScenes} from '../glass/scenes';
import {auditionScenes} from '../glass/audition';
import {Cam, GlassBg, GlassFx} from '../glass/kit';
import {lottieScenes, LottieBg, LottieFx} from '../glass/lottie';
import {tabletScenes} from '../glass/tablet';

// Faceless-first vertical short (Aly 2026-10-08, theodesy): the whole short is motion graphics; Aly (cut out from the
// raw HDR clips, tools via work/scripts/faces.py) appears only at a few moments (start / middle / end).
// Built by projects/<code>/work/scripts/make_shorts.py -> props JSON. All times in timeline seconds.
export const filmShortSchema = z.object({
  fps: z.number().default(30),
  duration: z.number().default(5),
  voice: z.string().default(''),
  segs: z.array(z.object({src: z.number(), tl: z.number(), len: z.number()})).default([]),
  words: z.array(z.object({w: z.string(), start: z.number(), end: z.number()})).default([]),
  aly: z.array(z.object({file: z.string(), at: z.number(), dur: z.number(), from: z.number(), mode: z.string().default('bottom'),
    face: z.array(z.number()).default([0.5, 0.3]), rate: z.number().default(1), clipL: z.number().default(0), ain: z.boolean().default(true), aout: z.boolean().default(true)})).default([]),
  scenes: z.array(z.object({t: z.string(), at: z.number(), dur: z.number(), layer: z.string().default('front'), props: z.record(z.string(), z.any()).default({})})).default([]),
  cta: z.object({file: z.string(), tl: z.number(), len: z.number(), src: z.number()}).nullable().default(null),
  ctaCue: z.record(z.string(), z.any()).nullable().default(null),
  sfx: z.array(z.object({file: z.string(), at: z.number(), vol: z.number().default(0.5), dur: z.number().default(3), loop: z.boolean().default(false)})).default([]),
  tint: z.string().default(K.red),
  capBottom: z.number().default(0.12),
  ctaVol: z.number().default(0.5), // CTA clip was ~6 dB louder than the voice track
  sfxGain: z.number().default(1),
  // v4 (Aly 2026-10-09): his cut-out the WHOLE short at the bottom; full-screen scenes shrink into a screen card on top.
  layout: z.string().default('normal'), // global sound-effects level (voice is -12 LUFS podcast-style)
  look: z.string().default('film'), // 'film' (darkroom collage) | 'vhs' (vhstodigital 2026-10-09: CRT, OSD, RCA colours) | 'cairo' (map, cairohistory) | 'hist' (timeline world, historyOfGraphics) | 'pop' (ffmpeg 2026-10-14: violet/lime design-tool look, src/pop)
  // historyOfGraphics 2026-10-10: background music under his voice (fades in/out, lower under the CTA clip)
  music: z.object({file: z.string(), vol: z.number().default(0.12), from: z.number().default(0)}).nullable().default(null),
  // lighting 2026-10-14 (look 'glass'): his camera ALWAYS on screen = one continuous mp4 of the kept pieces + layout keys
  cam: z.object({file: z.string(), keys: z.array(z.object({t: z.number(), m: z.string()}))}).nullable().default(null),
});
const allScenes: Record<string, React.FC<any>> = {...filmScenes, ...vhsScenes, ...cairoScenes, ...histScenes, ...popScenes, ...glassScenes, ...auditionScenes, ...lottieScenes, ...tabletScenes};

// Aly cut-out (1080x1080 square webm). bottom = full width at the bottom with a halftone disc behind his head;
// left/right = smaller presenter in a corner while a scene plays behind.
const AlyCut: React.FC<{file: string; from: number; mode: string; face: number[]; rate?: number; disc?: string; clipL?: number; ain?: boolean; aout?: boolean}> = ({file, from, mode, face, rate = 1, disc = K.red, clipL = 0, ain = true, aout = true}) => {
  const f = useCurrentFrame();
  const {fps, width, height, durationInFrames: d} = useVideoConfig();
  // ain/aout false = this window continues the previous/next one (no pop between his pieces)
  const k = Math.min(ain ? spr(f, fps, 0, 150, 16) : 1, aout ? lin(f, d - 7, d, 1, 0, Easing.in(Easing.cubic)) : 1);
  if (mode === 'bubble-big') {
    // historyOfGraphics (Aly: "المقدمة بس اللي دايرة كبيرة"): big round webcam in the opening, then it SHRINKS into the small
    // bottom-left 'bubble-s' (same geometry) during its last 14 frames -> the next small bubble continues it (ain false)
    const u = lin(f, d - 14, d, 0, 1, Easing.inOut(Easing.cubic));
    const D0 = 560, x0 = (width - D0) / 2, y0 = height * 0.47;
    const D1 = 290, x1 = 40, y1 = height * 0.83;
    const D = D0 + (D1 - D0) * u, x = x0 + (x1 - x0) * u, y = y0 + (y1 - y0) * u;
    return (
      <AbsoluteFill>
        <div style={{position: 'absolute', left: x, top: y, width: D, height: D, borderRadius: '50%', overflow: 'hidden', border: `${14 - 4 * u}px solid ${disc}`,
          boxShadow: '0 18px 40px rgba(0,0,0,0.5)', transform: `scale(${ain ? spr(f, fps, 0, 150, 16) : 1})`}}>
          <OffthreadVideo muted src={staticFile(file)} startFrom={Math.round(from * fps)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        </div>
      </AbsoluteFill>
    );
  }
  if (mode.startsWith('bubble')) {
    // cairohistory: in his screen recording he sits small in a corner -> round "webcam" bubble (mode 'bubble' = left, 'bubble-r' = right)
    // 'bubble-s' (historyOfGraphics): smaller, under the timeline ruler, bottom-left, so it never covers the motion
    const D = mode === 'bubble-s' ? 290 : 380, x = mode === 'bubble-r' ? width - D - 50 : mode === 'bubble-s' ? 40 : 50, y = mode === 'bubble-s' ? height * 0.83 : height * 0.6;
    return (
      <AbsoluteFill>
        <div style={{position: 'absolute', left: x, top: y, width: D, height: D, borderRadius: '50%', overflow: 'hidden', border: `10px solid ${disc}`,
          boxShadow: '0 18px 40px rgba(0,0,0,0.5)', transform: `scale(${k}) rotate(${(1 - k) * -20}deg)`}}>
          <OffthreadVideo muted src={staticFile(file)} startFrom={Math.round(from * fps)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        </div>
      </AbsoluteFill>
    );
  }
  // face = [x, y, head width] in the square (from its alpha). Head ~32% of the screen width when 'bottom',
  // face centred horizontally, face at ~56% of the height; corners = smaller.
  const hw = face[2] || 0.3;
  const corner = mode === 'left' || mode === 'right';
  const full = mode === 'full';
  const s = Math.max(0.55, Math.min(1.8, (corner ? 0.2 : full ? 0.26 : mode === 'big' ? 0.4 : 0.32) / hw));
  // 'anchor' (cairohistory v2): square bottom on the screen bottom, size chosen so his face sits at 68% height, right side
  const W = mode === 'anchor' ? (height * 0.32) / Math.max(0.3, 1 - face[1]) : width * s;
  const cxT = mode === 'left' ? width * 0.26 : mode === 'right' || mode === 'anchor' ? width * 0.72 : width / 2;
  const left = cxT - W * face[0];
  const top = Math.max(height - W, height * (corner ? 0.7 : full ? 0.79 : 0.56) - W * face[1]) + (1 - k) * W * 0.6;
  const fx = left + W * face[0], fy = top + W * face[1];
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: fx - hw * W * (mode === 'anchor' ? 1.0 : 1.45), top: fy - hw * W * (mode === 'anchor' ? 0.95 : 1.3),
        width: hw * W * (mode === 'anchor' ? 2.0 : 2.9), height: hw * W * (mode === 'anchor' ? 2.0 : 2.9), borderRadius: '50%',
        background: disc, opacity: 0.9 * k, overflow: 'hidden', transform: `scale(${0.6 + 0.4 * k})`}}>
        <Halftone color={K.ink} size={16} dot={0.28} opacity={0.45} />
      </div>
      <OffthreadVideo transparent muted src={staticFile(file)} startFrom={Math.round(from * fps)} playbackRate={rate}
        style={{position: 'absolute', left, top, width: W, height: W, clipPath: clipL ? `inset(0 0 0 ${clipL * 100}%)` : undefined}} />
    </AbsoluteFill>
  );
};

export const FilmShort: React.FC<z.infer<typeof filmShortSchema>> = (p) => {
  applyPack('darkroom');
  const {fps} = useVideoConfig();
  const frame = useCurrentFrame();
  const F = (s: number) => Math.round(s * fps);
  const inCta = p.cta ? frame >= F(p.cta.tl) : false;
  const v4 = p.layout === 'v4';
  const scene = (layer: string) => p.scenes.filter((s) => (s.layer ?? 'front') === layer).map((s, i) => {
    const C = allScenes[s.t];
    if (!C) return null;
    const body = <C {...s.props} />;
    return (
      <Sequence key={layer + i} from={F(s.at)} durationInFrames={Math.max(1, F(s.dur))}>
        {v4 && layer === 'front' ? (
          // v4: the full-screen scene becomes a screen card in the top part, he stays visible below it
          <AbsoluteFill style={{transform: 'translateY(34px) scale(0.72)', transformOrigin: '50% 0%'}}>
            <AbsoluteFill style={{borderRadius: 48, overflow: 'hidden', border: `6px solid ${K.paper2}`, boxShadow: '0 40px 80px rgba(0,0,0,0.7)'}}>{body}</AbsoluteFill>
          </AbsoluteFill>
        ) : body}
      </Sequence>
    );
  });
  return (
    <AbsoluteFill style={{background: K.ink, direction: 'rtl', fontFamily: 'Cairo'}}>
      <style>{fontCss + popFontCss}</style>
      {p.look === 'lottie' ? <LottieBg /> : p.look === 'glass' ? <GlassBg /> : p.look === 'pop' ? <PopBg /> : p.look === 'vhs' ? <VhsBg tint={p.tint} /> : p.look === 'cairo' || p.look === 'hist' ? <AbsoluteFill style={{background: '#E7D7B1'}} /> : <FilmBg tint={p.tint} />}
      {scene('back')}
      {p.cam && !inCta ? <Cam file={p.cam.file} keys={p.cam.keys} /> : null}
      {!v4 && p.aly.map((a, i) => (
        <Sequence key={'a' + i} from={F(a.at)} durationInFrames={Math.max(1, F(a.dur))}>
          <AlyCut file={a.file} from={a.from} mode={a.mode} face={a.face} rate={a.rate ?? 1} disc={p.look === 'vhs' || p.look === 'hist' ? p.tint : K.red} clipL={a.clipL ?? 0} ain={a.ain ?? true} aout={a.aout ?? true} />
        </Sequence>
      ))}
      {scene('front')}
      {v4 ? p.aly.map((a, i) => (
        <Sequence key={'a4' + i} from={F(a.at)} durationInFrames={Math.max(1, F(a.dur))}>
          <AlyCut file={a.file} from={a.from} mode={a.mode} face={a.face} rate={a.rate ?? 1} disc={p.look === 'vhs' || p.look === 'hist' ? p.tint : K.red} clipL={a.clipL ?? 0} ain={a.ain ?? true} aout={a.aout ?? true} />
        </Sequence>
      )) : null}
      {!inCta && p.look !== 'cairo' && p.look !== 'hist' ? (p.look === 'lottie' ? <LottieFx /> : p.look === 'glass' ? <GlassFx /> : p.look === 'pop' ? <PopFx /> : p.look === 'vhs' ? <VhsFx /> : <FilmFx />) : null}
      {p.segs.map((s, i) => (
        <Sequence key={'v' + i} from={F(s.tl)} durationInFrames={Math.max(1, F(s.tl + s.len) - F(s.tl))}>
          <Audio src={staticFile(p.voice)} startFrom={F(s.src)} volume={(k) => Math.min(1, k / 3, (F(s.len) - k) / 3)} />
        </Sequence>
      ))}
      {p.music ? (
        <Audio src={staticFile(p.music.file)} startFrom={F(p.music.from ?? 0)}
          volume={(k) => (p.music?.vol ?? 0.12) * Math.min(1, k / 20, (F(p.duration) - k) / 30) * (p.cta && k >= F(p.cta.tl) ? 0.45 : 1)} />
      ) : null}
      {p.sfx.map((s, i) => (
        <Sequence key={'s' + i} from={F(s.at)} durationInFrames={Math.max(1, F(s.dur ?? 3))}>
          <Audio src={staticFile(s.file)} loop={!!s.loop}
            volume={(k) => Math.min(1, (s.vol ?? 0.5) * (p.sfxGain ?? 1)) * Math.max(0, Math.min(1, (F(s.dur ?? 3) - k) / 6))} />
        </Sequence>
      ))}
      {p.cta ? (
        <Sequence from={F(p.cta.tl)} durationInFrames={F(p.cta.len)}>
          <OffthreadVideo src={staticFile(p.cta.file)} startFrom={F(p.cta.src)} volume={p.ctaVol} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          {p.ctaCue ? (
            <Sequence from={F(p.ctaCue.at ?? 0)} durationInFrames={F(p.ctaCue.dur ?? p.cta.len)}>
              <CommentCta {...(commentCtaSchema.parse(p.ctaCue.props ?? {}) as any)} />
            </Sequence>
          ) : null}
        </Sequence>
      ) : null}
      <Captions words={p.words} maxWords={4} accent="gold" previewBg="" lift={0} bottomFrac={inCta ? 0.2 : p.capBottom} />
    </AbsoluteFill>
  );
};
