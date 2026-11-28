// The WHOLE song «أنا اللي كنت ماسك الفرشاة» as a vertical reel (Aly 2026-11-28). Props: work/scripts/song_vreel_props.py.
// Every song shot full frame in its 9:16 version (Higgsfield reframe), the lyrics ONE WHOLE LINE at a time (Aly: «مرة واحدة… جملة جملة»,
// not word by word), the song watermarks of v11 (face logo + faint static calligraphy signatures) laid out for 1080x1920,
// handles footer, the subscribe + platforms on the last line, end card = thumbnail + video length + QR of the full video.
import React from 'react';
import {AbsoluteFill, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {fontCss} from '../blocks/theme';
import {E, stickerBorder} from '../enta/kit';
import {enter} from '../blocks/anim';
import {Rtl} from './V4';
import {ClipSeq} from './V11';

const gold = '#E9B949', ink = '#F3EEDF', navy = '#0B1430';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const clip = z.object({src: z.string(), from: z.number(), dur: z.number(), skip: z.number().optional(), rate: z.number().optional()});
export const vsongSchema = z.object({
  fps: z.number().default(25), duration: z.number().default(10), start: z.number().default(0), songDur: z.number().default(10),
  clips: z.array(clip).default([]),
  lines: z.array(z.object({t: z.number(), end: z.number(), toks: z.array(z.object({t: z.number(), w: z.string(), en: z.boolean(), pre: z.string()}))})).default([]),
  title: z.string().default(''), titleDur: z.number().default(4), face: z.string().default(''), sign: z.string().default(''),
  sub: z.object({at: z.number(), logos: z.array(z.string()), handles: z.array(z.string())}).optional(),
  end: z.object({thumb: z.string(), qr: z.string(), line1: z.string(), line2: z.string(), length: z.string()}).optional(),
});
type P = z.infer<typeof vsongSchema>;

// a lyric line exactly like the original v11 song (Aly review 2 «نفس طريقة الكتابة اللي في الفيديو الأصلي»): the whole line is there at once,
// dim; each word rises in and turns gold on its own time; the line fades at its end. English tokens drawn LTR, an Arabic prefix glued to them.
const Tok: React.FC<{k: P['lines'][number]['toks'][number]; sung: boolean; p: number; o: number}> = ({k, sung, p, o}) => {
  const punct = k.en ? (k.w.match(/[.،,:؟?!»]+$/) ?? [''])[0] : '';
  const w = punct ? k.w.slice(0, -punct.length) : k.w;
  return (
    <span style={{display: 'inline-block', whiteSpace: 'nowrap', direction: 'rtl', unicodeBidi: 'isolate', fontSize: 64, fontWeight: 900,
      color: sung ? gold : 'rgba(243,238,223,.25)', transform: `translateY(${(1 - p) * 30}px)`, opacity: o, textShadow: '0 6px 26px rgba(0,0,0,.7)'}}>
      {k.pre}{k.pre ? <span style={{display: 'inline-block', width: '0.12em'}} /> : null}{k.en ? <bdi dir="ltr">{w}</bdi> : w}{punct}
    </span>);
};

const Lyric: React.FC<{l: P['lines'][number]; start: number}> = ({l}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const t = l.t + f / fps;
  const o = interpolate(t, [l.end - 0.35, l.end - 0.05], [1, 0], clamp);
  return (
    <div style={{position: 'absolute', left: 70, right: 70, top: 1270, height: 330, display: 'flex', flexWrap: 'wrap', alignContent: 'center',
      justifyContent: 'center', gap: '6px 16px', direction: 'rtl', fontFamily: 'Cairo', lineHeight: 1.35}}>
      {l.toks.map((k, i) => <Tok key={i} k={k} sung={t >= k.t} p={enter(f, fps, Math.round((k.t - l.t) * fps))} o={o} />)}
    </div>
  );
};

// the v11 song watermarks, re-placed for the vertical frame (static, faint) + his face logo top-right
const Marks: React.FC<{p: P}> = ({p}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const o = interpolate(f, [0, 15], [0, 1], clamp) * interpolate(f, [p.songDur * fps - 15, p.songDur * fps], [1, 0], clamp);
  const wm: [number, number, number, number][] = [[80, 380, 120, 0.05], [800, 620, 170, 0.05], [80, 1000, 140, 0.05], [790, 1180, 190, 0.045], [280, 760, 520, 0.012]];
  return (
    <AbsoluteFill style={{opacity: o}}>
      {wm.map(([x, y, w, a], i) => <Img key={i} src={staticFile(p.sign)} style={{position: 'absolute', left: x, top: y, width: w, opacity: a, filter: 'invert(1) brightness(1.4)'}} />)}
      <Img src={staticFile(p.face)} style={{position: 'absolute', right: 60, top: 60, width: 74, filter: 'drop-shadow(0 4px 10px rgba(0,0,0,.6))'}} />
    </AbsoluteFill>
  );
};

const Sub: React.FC<{s: NonNullable<P['sub']>; left: number}> = ({s, left}) => {
  const f = useCurrentFrame();
  const so = interpolate(f, [left - 12, left], [1, 0], clamp);
  return (
    <div style={{position: 'absolute', left: 70, top: 420, display: 'flex', flexDirection: 'column', gap: 16, opacity: so, direction: 'ltr'}}>
      {s.logos.map((l, i) => {
        const q = interpolate(f, [20 + i * 5, 30 + i * 5], [0, 1], clamp);
        return (
          <div key={i} style={{display: 'flex', alignItems: 'center', gap: 16, opacity: q, transform: `translateX(${(1 - q) * -40}px)`}}>
            <div style={{width: 66, height: 66, borderRadius: 18, background: E.paper, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 8px 18px rgba(0,0,0,.5)'}}>
              <Img src={staticFile(l)} style={{width: 44, height: 44, objectFit: 'contain'}} /></div>
            <div style={{fontFamily: 'Montserrat', fontWeight: 800, fontSize: 36, color: ink, textShadow: '0 3px 10px rgba(0,0,0,.85)'}}>{s.handles[i]}</div>
          </div>);
      })}
    </div>
  );
};

// the title only opens the reel (Aly review 1: «سيبه أول كام ثانية بس»), then fades out
const Title: React.FC<{text: string; show: number}> = ({text, show}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const k = enter(f, fps, 0);
  const o = interpolate(f, [show * fps - 12, show * fps], [1, 0], clamp);
  if (f > show * fps) return null;
  return (
    <div style={{position: 'absolute', top: 170, left: 150, right: 150, display: 'flex', justifyContent: 'center', opacity: o}}>
      <div style={{background: E.paper, color: E.ink, fontFamily: 'Cairo', fontWeight: 900, fontSize: 46, padding: '4px 26px', borderRadius: 14, ...stickerBorder(6),
        transform: `rotate(-1.2deg) scale(${0.6 + 0.4 * k})`, opacity: Math.min(1, k * 1.6), textAlign: 'center'}}><Rtl text={text} /></div>
    </div>
  );
};

const Footer: React.FC = () => (
  <div style={{position: 'absolute', left: 0, right: 0, top: 1720, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 16, direction: 'ltr', opacity: 0.9}}>
    {[['youtube.png', '@AlyShorosh'], ['tiktok.png', '@alyshorosh'], ['instagram.ico', '@alyshorosh'], ['facebook.png', 'aly.shorosh']].map(([l, t]) => (
      <div key={l} style={{display: 'flex', alignItems: 'center', gap: 6}}>
        <Img src={staticFile('projects/aiworld/v6/logos/' + l)} style={{width: 24, height: 24, objectFit: 'contain'}} />
        <span style={{fontFamily: 'Montserrat', fontWeight: 700, fontSize: 21, color: ink, textShadow: '0 2px 6px rgba(0,0,0,.85)'}}>{t}</span></div>))}
  </div>
);

const EndCard: React.FC<{e: NonNullable<P['end']>}> = ({e}) => {
  const f = useCurrentFrame(); const k = enter(f, 25, 0);
  const q = interpolate(f, [18, 32], [0, 1], clamp);
  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 70% at 50% 40%, #16245a 0%, ${navy} 55%, #050815 100%)`, alignItems: 'center', justifyContent: 'center',
      flexDirection: 'column', gap: 30, opacity: Math.min(1, k * 1.6)}}>
      <div style={{fontFamily: 'Cairo', fontWeight: 900, fontSize: 60, color: gold}}><Rtl text={e.line1} /></div>
      <div style={{width: 940, aspectRatio: '16/9', borderRadius: 18, overflow: 'hidden', ...stickerBorder(8), transform: `scale(${0.8 + 0.2 * k})`, position: 'relative'}}>
        <Img src={staticFile(e.thumb)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        <div style={{position: 'absolute', right: 16, bottom: 16, background: 'rgba(0,0,0,.85)', color: '#fff', fontFamily: 'Montserrat', fontWeight: 800, fontSize: 34,
          padding: '2px 14px', borderRadius: 8}}>{e.length}</div>
      </div>
      <div style={{fontFamily: 'Cairo', fontWeight: 900, fontSize: 48, color: ink, textAlign: 'center', maxWidth: 960}}><Rtl text={e.line2} /></div>
      <div style={{fontFamily: 'Cairo', fontWeight: 900, fontSize: 44, color: E.ink, background: gold, padding: '2px 28px', borderRadius: 14, ...stickerBorder(5), direction: 'rtl'}}>
        <span>مدة الفيديو: </span><bdi dir="ltr">{e.length}</bdi><span> دقيقة</span></div>
      <div style={{display: 'flex', alignItems: 'center', gap: 30, opacity: q, direction: 'rtl'}}>
        <div style={{width: 330, height: 330, background: '#fff', borderRadius: 18, padding: 14, ...stickerBorder(6)}}>
          <Img src={staticFile(e.qr)} style={{width: '100%', height: '100%'}} /></div>
        <div style={{fontFamily: 'Cairo', fontWeight: 900, fontSize: 44, color: gold, maxWidth: 470, lineHeight: 1.3}}><Rtl text="امسح الكود وشوف الفيديو كامل" /></div>
      </div>
    </AbsoluteFill>
  );
};

export const AiWorldVSong11: React.FC<P> = (p) => {
  const {fps} = useVideoConfig();
  const F = (t: number) => Math.round((t - p.start) * fps);
  const songF = Math.round(p.songDur * fps);
  return (
    <AbsoluteFill style={{background: navy, overflow: 'hidden'}}>
      <style>{fontCss}</style>
      <Sequence durationInFrames={songF}>
        {/* clips carry v11 seconds; ClipSeq places them against p.start */}
        {p.clips.map((c, i) => <ClipSeq key={i} c={c} start={p.start} />)}
        <AbsoluteFill style={{background: 'linear-gradient(transparent 58%, rgba(5,8,21,.82))'}} />
        <Marks p={p} />
        <Title text={p.title} show={p.titleDur} />
        {p.lines.map((l, i) => (
          <Sequence key={i} from={F(l.t)} durationInFrames={Math.max(1, Math.round((l.end - l.t) * fps))}><Lyric l={l} start={p.start} /></Sequence>))}
        {p.sub ? <Sequence from={F(p.sub.at)} durationInFrames={songF - F(p.sub.at)}><Sub s={p.sub} left={songF - F(p.sub.at)} /></Sequence> : null}
        <Footer />
      </Sequence>
      {p.end ? <Sequence from={songF}><EndCard e={p.end} /></Sequence> : null}
    </AbsoluteFill>
  );
};
