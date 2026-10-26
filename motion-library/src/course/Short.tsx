import React from 'react';
import {AbsoluteFill, Audio, Easing, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {fontCss} from '../blocks/theme';
import {GlassBg, GlassFx, Type} from '../glass/kit';
import {FilmBg, FilmFx} from '../film/kit';
import {VhsBg, VhsFx} from '../vhs/kit';
import {PopBg, PopFx, popFontCss} from '../pop/kit';
import {LottieBg, LottieFx} from '../glass/lottie';
import {AR, bi, CC, Def, EN, G, Glass, Ico, Key, Kw, lin, Pill, spr, Src} from './kit';
import {courseAnims, HideNote} from './anims';
import {audioAnims} from './audioAnims';
import {sound3d} from './sound3d';
import {shortScenes} from './shortScenes';
import {courseScenes} from './scenes';
import {Captions} from '../templates/Captions';

// Vertical shorts series from the Premiere course (Aly 2026-10-18): every short in the SAME series frame (top band: Pr logo +
// "كورس Premiere" + posting number + where it is in the full course), a mix of approved looks behind, his recording only when the
// click matters (big card, zoom on his cursor, gold box), concept animations, step chips, CTA clip + QR of the full course at the end.
const cue = z.object({t: z.number(), d: z.number(), k: z.string(), p: z.record(z.string(), z.any()).default({})});
export const courseShortSchema = z.object({
  fps: z.number().default(30),
  duration: z.number().default(5),
  look: z.string().default('glass'),
  series: z.object({no: z.number(), total: z.number(), title: z.string(), at: z.string(), chap: z.number().default(0)}).default({no: 1, total: 44, title: '', at: '', chap: 0}),
  voice: z.array(z.object({file: z.string(), from: z.number(), to: z.number(), at: z.number(), gain: z.number().default(1)})).default([]),
  screens: z.array(z.object({t: z.number(), d: z.number(), file: z.string(), from: z.number(), keys: z.array(z.object({t: z.number(), sx: z.number(), sy: z.number(), sw: z.number()})).default([]),
    marks: z.array(z.object({t: z.number(), d: z.number(), x: z.number(), y: z.number(), r: z.number().default(46), w: z.number().default(0), h: z.number().default(0), label: z.string().default('')})).default([]), y: z.number().default(980),
    dual: z.object({top: z.object({sx: z.number(), sy: z.number(), sw: z.number()}), bottom: z.object({sx: z.number(), sy: z.number(), sw: z.number()})}).nullable().default(null), under: z.boolean().default(false),
    cin: z.boolean().default(false), cout: z.boolean().default(false)})).default([]), // cin/cout: the card stays from the screen piece before/after (one video, not separate shots)
  cues: z.array(cue).default([]),
  cta: z.object({file: z.string(), at: z.number(), d: z.number(), qr: z.string(), vol: z.number().default(1), word: z.string().default('كورس'), thumb: z.string().nullable().default(null)}).nullable().default(null),
  music: z.array(z.object({t: z.number(), d: z.number(), file: z.string(), from: z.number().default(0), vol: z.number().default(0.06)})).default([]),
  sfx: z.array(z.object({t: z.number(), file: z.string(), vol: z.number().default(0.3)})).default([]),
  env: z.array(z.number()).default([]), // his voice level per frame (0..1) for the bars
  words: z.array(z.object({w: z.string(), start: z.number(), end: z.number()})).default([]), // captions (corrected per short)
  // series identity (audio course 2026-10-26: same frame, its own name/logo) + recording size + end card (thumbnail + QR, never a QR alone)
  brand: z.object({logo: z.string().default('Pr'), name: z.string().default('كورس Premiere')}).default({logo: 'Pr', name: 'كورس Premiere'}),
  src: z.object({w: z.number(), h: z.number()}).default({w: 1276, h: 720}),
  end: z.object({at: z.number(), d: z.number(), thumb: z.string(), qr: z.string(), title: z.string().default('الكورس الكامل على القناة')}).nullable().default(null),
  footer: z.object({face: z.string(), name: z.string()}).nullable().default(null), // channel logo + name at the very bottom (Aly 2026-10-26)
});
type Props = z.infer<typeof courseShortSchema>;

const LOOK: Record<string, {Bg: React.FC<any>; Fx: React.FC<any>; acc: string; acc2: string}> = {
  glass: {Bg: GlassBg, Fx: GlassFx, acc: G.gold, acc2: G.blue},
  film: {Bg: FilmBg, Fx: FilmFx, acc: '#FFC21A', acc2: '#E5232B'},
  vhs: {Bg: VhsBg, Fx: (p: any) => <VhsFx {...p} osd={false} />, acc: '#FFD23F', acc2: '#3FC7DA'},
  pop: {Bg: PopBg, Fx: () => null, acc: '#C6FF3D', acc2: '#8B5CF6'},
  lottie: {Bg: LottieBg, Fx: LottieFx, acc: G.gold, acc2: G.blue},
  sound: {Bg: GlassBg, Fx: GlassFx, acc: '#2EE6B6', acc2: '#8B5CF6'}, // audio course: teal + violet of his thumbnail
};
// size of the screen recording (Premiere course 1276x720, audio course 1280x720)
const SrcCtx = React.createContext({w: 1276, h: 720});
const useSrc = () => React.useContext(SrcCtx);
const SOUND = '#2EE6B6';
// the series logo box: 'Pr' text, or 'wave' = sound bars (audio course)
const Logo: React.FC<{logo: string}> = ({logo}) => {
  const f = useCurrentFrame();
  if (logo === 'wave') return (
    <div style={{width: 84, height: 82, borderRadius: 18, background: '#101828', border: `4px solid ${SOUND}`, boxSizing: 'border-box', display: 'flex', alignItems: 'center',
      justifyContent: 'center', gap: 5, flexShrink: 0}}>
      {[0.45, 0.8, 1, 0.65, 0.35].map((h, i) => <div key={i} style={{width: 7, height: 50 * h * (0.75 + 0.25 * Math.sin(f / 5 + i * 1.7)), borderRadius: 4, background: i % 2 ? CC.violet : SOUND}} />)}
    </div>);
  return (
    <div style={{width: 84, height: 82, borderRadius: 18, background: CC.prBg, border: `4px solid ${CC.violet}`, boxSizing: 'border-box', display: 'flex', alignItems: 'center',
      justifyContent: 'center', flexShrink: 0}}><span style={{fontFamily: EN, fontWeight: 700, fontSize: 42, color: CC.violet}}>{logo}</span></div>);
};
export const CW = 1016, CH = 840, CTOP = 430; // the big screen card (Aly: the recording must be big in a short)

// ---------- the series frame (same in every short). Aly 2026-10-18: the short's title INSIDE the band, "Reel 01", the chapter
// number in the full video and the minute it starts at (no long phrase) ----------
const SeriesFrame: React.FC<{no: number; total: number; title: string; at: string; chap: number; acc: string; logo: string; name: string}> = ({no, total, title, at, chap, acc, logo, name}) => {
  const f = useCurrentFrame();
  const p = lin(f, 0, 14);
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div style={{position: 'absolute', inset: 14, borderRadius: 48, border: `6px solid ${CC.violet}`, boxShadow: `0 0 40px ${CC.violet}66, inset 0 0 40px ${CC.violet}33`}} />
      <div style={{position: 'absolute', left: 36, right: 36, top: 150, height: 150, borderRadius: 32, background: 'rgba(0,0,40,0.86)', border: `3px solid ${CC.violet}`,
        display: 'flex', alignItems: 'center', gap: 18, padding: '0 18px', direction: 'rtl', opacity: p, transform: `translateY(${(1 - p) * -30}px)`}}>
        <Logo logo={logo} />
        <div style={{flex: 1, minWidth: 0}}>
          <div style={{fontFamily: AR, fontWeight: 900, fontSize: 46, color: '#fff', lineHeight: 1.15, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{bi(title)}</div>
          <div style={{fontFamily: AR, fontWeight: 700, fontSize: 26, color: G.soft, marginTop: 6, whiteSpace: 'nowrap'}}>
            {bi(`${name} · الفصل ${chap} · الدقيقة ${at}`)}
          </div>
        </div>
        <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '6px 16px', borderRadius: 22, background: acc, flexShrink: 0, direction: 'ltr'}}>
          <span style={{fontFamily: EN, fontWeight: 800, fontSize: 20, color: '#14181F', letterSpacing: 1}}>REEL</span>
          <span style={{fontFamily: EN, fontWeight: 900, fontSize: 44, color: '#14181F', lineHeight: 1}}>{String(no).padStart(2, '0')}<span style={{fontSize: 22, opacity: 0.65}}>/{total}</span></span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// a setting and its result at the same moment: the panel he changes on top, the picture it changes below (Aly 2026-10-18)
type DMark = {t: number; d: number; x: number; y: number; r: number; label: string};
const DualCard: React.FC<{file: string; from: number; d: number; top: {sx: number; sy: number; sw: number}; bottom: {sx: number; sy: number; sw: number}; acc: string; under?: boolean; marks?: DMark[]}> = (
  {file, from, d, top, bottom, acc, under = false, marks = []}) => {
  const {w: SRCW, h: SRCH} = useSrc();
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const W = CW, H2 = (CH - 12) / 2;
  const pIn = spr(f, fps, 0, 140, 16), o = 1 - lin(f, d * fps - 8, d * fps);
  const pane = (c: {sx: number; sy: number; sw: number}, label: string, delay: number) => {
    const k = W / c.sw;
    const q = spr(f, fps, delay, 150, 16);
    return (
      <div style={{position: 'relative', width: W, height: H2, borderRadius: 22, overflow: 'hidden', background: '#000', transform: `translateX(${(1 - q) * (delay ? 60 : -60)}px)`, opacity: Math.min(1, q * 1.4)}}>
        <OffthreadVideo muted src={staticFile(file)} startFrom={Math.round(from * fps)} style={{position: 'absolute', left: -c.sx * k, top: -c.sy * k, width: SRCW * k, height: SRCH * k}} />
        {/* click marks (Aly: "مكنتش باين انا بدوس فين") — drawn in the pane that shows the clicked point */}
        {marks.map((m, j) => {
          const ch = c.sw * H2 / W;
          if (m.x < c.sx || m.x > c.sx + c.sw || m.y < c.sy || m.y > c.sy + ch) return null;
          if (f < m.t * fps || f > (m.t + m.d) * fps) return null;
          const q = spr(f, fps, m.t * fps, 220, 14), oo = 1 - lin(f, (m.t + m.d) * fps - 6, (m.t + m.d) * fps);
          const r = Math.max(26, m.r * k);
          return (
            <div key={j} style={{position: 'absolute', left: (m.x - c.sx) * k - r, top: (m.y - c.sy) * k - r, width: 2 * r, height: 2 * r, borderRadius: 18, border: `6px solid ${acc}`,
              opacity: oo, transform: `scale(${1.3 - 0.3 * q})`, boxShadow: `0 0 30px ${acc}AA`}}>
              <div style={{position: 'absolute', left: r - 50, top: r - 50, width: 100, height: 100, borderRadius: '50%', border: `5px solid ${acc}`,
                transform: `scale(${0.3 + 1.2 * lin(f, m.t * fps, m.t * fps + 16)})`, opacity: 1 - lin(f, m.t * fps, m.t * fps + 16)}} />
            </div>
          );
        })}
        <div style={{position: 'absolute', right: 12, top: 12}}><Pill text={label} size={30} color={delay ? acc : 'rgba(10,14,22,0.85)'} ink={delay ? '#14181F' : '#fff'} glow={false} /></div>
      </div>
    );
  };
  return (
    <div style={{position: 'absolute', left: 520 - W / 2 + 8, top: under ? CTOP + H2 + 40 : CTOP, transform: `scale(${0.92 + 0.08 * pIn})`, opacity: Math.min(1, pIn * 1.4) * o}}>
      <Glass w={W + 24} pad={12} r={34} glow={acc}>
        <div style={{display: 'flex', flexDirection: 'column', gap: 12}}>
          {under ? null : pane(top, 'الإعداد', 0)}
          {pane(bottom, under ? 'على الشاشة' : 'النتيجة', under ? 0 : 6)}
        </div>
      </Glass>
    </div>
  );
};

// big moment label over the card (e.g. "سريع ⏩" right when he says it in the demo)
const Label: React.FC<{text: string; dur: number; acc: string; img?: string}> = ({text, dur, acc, img}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 220, 11), o = 1 - lin(f, dur - 5, dur);
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: CTOP + 40, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 30, direction: 'rtl',
      opacity: Math.min(1, p * 1.5) * o, transform: `scale(${0.4 + 0.6 * p})`}}>
      {/* own space next to the pill, never on it (Aly 2026-10-26: overlaps in reel 29) */}
      {img ? <Img src={staticFile(`fluent/${img}.png`)} style={{width: 140, height: 140, flexShrink: 0, objectFit: 'contain', filter: 'drop-shadow(0 12px 24px rgba(0,0,0,0.5))'}} /> : null}
      <Pill text={text} size={96} color={acc} />
    </div>
  );
};

// correction of something said in the 2018 course (Aly: "لو انا قولت معلومة غلط صلحها"), with its source
const Fix: React.FC<{text: string; src: string; dur: number}> = ({text, src, dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 150, 15), o = 1 - lin(f, dur - 8, dur);
  return (
    <div style={{position: 'absolute', left: 60, right: 60, top: CTOP + CH - 250, opacity: Math.min(1, p * 1.4) * o, transform: `translateY(${(1 - p) * 40}px)`}}>
      <div style={{padding: '16px 22px', borderRadius: 28, background: 'rgba(12,16,26,0.94)', border: `3px solid ${CC.coral}`, direction: 'rtl', boxShadow: `0 0 40px ${CC.coral}55`}}>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 32, color: CC.coral}}>✎ تصحيح</div>
        <div style={{fontFamily: AR, fontWeight: 800, fontSize: 36, color: '#fff', lineHeight: 1.35, marginTop: 4}}>{bi(text)}</div>
        <div style={{marginTop: 8, display: 'flex', justifyContent: 'flex-end'}}><Src text={src} s={0.9} /></div>
      </div>
    </div>
  );
};

// ---------- his screen recording, big, with zoom keys and gold click marks ----------
const ScreenCard: React.FC<{file: string; from: number; d: number; keys: {t: number; sx: number; sy: number; sw: number}[]; marks: {t: number; d: number; x: number; y: number; r: number; w?: number; h?: number; label: string}[]; y: number; acc: string; cin?: boolean; cout?: boolean}> = (
  {file, from, d, keys, marks, y, acc, cin = false, cout = false}) => {
  const {w: SRCW, h: SRCH} = useSrc();
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const W = CW, H = CH;
  let i = 0;
  while (i + 1 < keys.length && f >= keys[i + 1].t * fps) i++;
  const a = keys[i] ?? {t: 0, sx: 0, sy: 0, sw: SRCW};
  const b = keys[Math.min(i + 1, keys.length - 1)] ?? a;
  const k = b === a ? 0 : lin(f, b.t * fps - 12, b.t * fps, 0, 1, Easing.inOut(Easing.cubic));
  const sx = a.sx + (b.sx - a.sx) * k, sy = a.sy + (b.sy - a.sy) * k, sw = a.sw + (b.sw - a.sw) * k;
  const sc = W / sw;
  // Aly 2026-10-26 (reel 26): "لقطات متفرقة مش فيديو على بعضه" -> between two screen pieces the card does not pop out and in again
  const pIn = cin ? 1 : spr(f, fps, 0, 140, 16), o = cout ? 1 : 1 - lin(f, d * fps - 8, d * fps);
  return (
    <div style={{position: 'absolute', left: 520 - W / 2 + 8, top: CTOP, transform: `scale(${0.9 + 0.1 * pIn})`, opacity: Math.min(1, pIn * 1.4) * o}}>
      <Glass w={W + 24} pad={12} r={34} glow={acc}>
        <div style={{position: 'relative', width: W, height: H, borderRadius: 24, overflow: 'hidden', background: '#000'}}>
          <OffthreadVideo muted src={staticFile(file)} startFrom={Math.round(from * fps)} style={{position: 'absolute', left: -sx * sc, top: -sy * sc, width: SRCW * sc, height: SRCH * sc}} />
          {marks.map((m, j) => {
            if (f < m.t * fps || f > (m.t + m.d) * fps) return null;
            const q = spr(f, fps, m.t * fps, 220, 14), oo = 1 - lin(f, (m.t + m.d) * fps - 6, (m.t + m.d) * fps);
            const r = m.r * sc;
            // Aly 2026-10-26: the box must be the size of the clicked word (Capture Noise Print was a tall narrow box)
            const bw = m.w ? (m.w + 14) * sc / 2 : r, bh = m.h ? (m.h + 10) * sc / 2 : r;
            return (
              <div key={j} style={{position: 'absolute', left: (m.x - sx) * sc - bw, top: (m.y - sy) * sc - bh, width: 2 * bw, height: 2 * bh, borderRadius: m.w ? 14 : 18, border: `6px solid ${acc}`,
                opacity: oo, transform: `scale(${1.3 - 0.3 * q})`, boxShadow: `0 0 30px ${acc}AA`}}>
                {m.label ? <div style={{position: 'absolute', left: '50%', top: -66, transform: 'translateX(-50%)'}}><Pill text={m.label} font={EN} dir="ltr" size={34} color={acc} /></div> : null}
                <div style={{position: 'absolute', left: bw - 50, top: bh - 50, width: 100, height: 100, borderRadius: '50%', border: `5px solid ${acc}`,
                  transform: `scale(${0.3 + 1.2 * lin(f, m.t * fps, m.t * fps + 16)})`, opacity: 1 - lin(f, m.t * fps, m.t * fps + 16)}} />
              </div>
            );
          })}
        </div>
      </Glass>
    </div>
  );
};

// ---------- hook: the result itself, before -> after, with a wipe line that sweeps across (two moments of his recording) ----------
const BeforeAfter: React.FC<{file: string; before: number; after: number; crop: {sx: number; sy: number; sw: number}; cropB?: {sx: number; sy: number; sw: number}; dur: number; acc: string; y?: number}> = (
  {file, before, after, crop, cropB, dur, acc, y = 760}) => {
  const {w: SRCW, h: SRCH} = useSrc();
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const W = CW, H = CH, sc = W / crop.sw;
  const p = spr(f, fps, 0, 120, 16), o = 1 - lin(f, dur - 8, dur);
  // the line sweeps from 'before' (all) to 'after' (all), then settles in the middle so both stay visible
  const w1 = lin(f, 6, 40, 1, 0, Easing.inOut(Easing.cubic)), w2 = lin(f, 48, 72, 0, 0.5, Easing.out(Easing.cubic));
  const wipe = f < 48 ? w1 : w2;
  const x = Math.max(0, Math.min(1, wipe)) * W;
  const vid = (t: number, c = crop) => { const k = W / c.sw; return <OffthreadVideo muted src={staticFile(file)} startFrom={Math.round(t * fps)} style={{position: 'absolute', left: -c.sx * k, top: -c.sy * k, width: SRCW * k, height: SRCH * k}} />; };
  return (
    <div style={{position: 'absolute', left: 520 - W / 2 + 8, top: CTOP, opacity: Math.min(1, p * 1.4) * o, transform: `scale(${0.88 + 0.12 * p}) rotate(${(1 - p) * -3}deg)`}}>
      <Glass w={W + 24} pad={12} r={34} glow={acc}>
        <div style={{position: 'relative', width: W, height: H, borderRadius: 24, overflow: 'hidden', background: '#000'}}>
          {vid(after)}
          <div style={{position: 'absolute', left: 0, top: 0, width: x, height: H, overflow: 'hidden'}}>{vid(before, cropB ?? crop)}</div>
          <div style={{position: 'absolute', left: x - 3, top: 0, width: 6, height: H, background: '#fff', boxShadow: `0 0 24px ${acc}`}} />
          <div style={{position: 'absolute', left: x - 30, top: H / 2 - 30, width: 60, height: 60, borderRadius: '50%', background: '#fff', boxShadow: `0 0 30px ${acc}`,
            display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: EN, fontWeight: 900, fontSize: 26, color: '#14181F'}}>⇆</div>
          <div style={{position: 'absolute', left: 16, top: 16}}><Pill text="قبل" size={36} color="rgba(10,14,22,0.85)" ink="#fff" glow={false} /></div>
          <div style={{position: 'absolute', right: 16, top: 16}}><Pill text="بعد" size={36} color={acc} /></div>
        </div>
      </Glass>
    </div>
  );
};

// ---------- step panel under the recording: big glowing number + the step + progress dots ----------
const StepPanel: React.FC<{n: number; total: number; text: string; dur: number; acc: string}> = ({n, total, text, dur, acc}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 160, 15), q = spr(f, fps, 4, 180, 12), o = 1 - lin(f, dur - 8, dur);
  return (
    <div style={{position: 'absolute', left: 40, right: 40, top: 318, display: 'flex', justifyContent: 'center', opacity: Math.min(1, p * 1.4) * o, transform: `translateY(${(1 - p) * -30}px)`}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 16, padding: '10px 26px 10px 10px', borderRadius: 40, background: 'rgba(10,14,22,0.9)', border: `3px solid ${acc}`, direction: 'rtl',
        boxShadow: `0 0 40px ${acc}44`}}>
        <div style={{width: 84, height: 84, borderRadius: 26, background: acc, color: '#14181F', fontFamily: EN, fontWeight: 900, fontSize: 56, display: 'flex', alignItems: 'center',
          justifyContent: 'center', flexShrink: 0, transform: `scale(${0.6 + 0.4 * q}) rotate(${(1 - q) * 25}deg)`, boxShadow: `0 0 30px ${acc}AA`}}>{n}</div>
        <div>
          <div style={{fontFamily: AR, fontWeight: 900, fontSize: 44, color: '#fff', lineHeight: 1.2}}>{bi(text)}</div>
          <div style={{display: 'flex', gap: 8, marginTop: 6}}>
            {Array.from({length: total}).map((_, i) => <div key={i} style={{width: i + 1 === n ? 40 : 14, height: 12, borderRadius: 6, background: i + 1 <= n ? acc : 'rgba(255,255,255,0.2)'}} />)}
          </div>
        </div>
      </div>
    </div>
  );
};

// ---------- his voice as living bars (fills the stage while he talks without a step) ----------
const VoiceBars: React.FC<{env: number[]; at: number; acc: string; acc2: string}> = ({env, at, acc, acc2}) => {
  const f = useCurrentFrame();
  const i = Math.max(0, f - at);
  const N = 28;
  return (
    <div style={{position: 'absolute', left: 90, right: 90, top: 1190, height: 220, display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
      {Array.from({length: N}).map((_, k) => {
        const v = env[Math.max(0, Math.min(env.length - 1, i - Math.abs(k - N / 2)))] ?? 0;
        const h = 14 + 200 * v * (0.55 + 0.45 * Math.abs(Math.sin(k * 1.3 + f / 6)));
        return <div key={k} style={{width: 18, height: h, borderRadius: 9, background: `linear-gradient(180deg, ${acc}, ${acc2})`, opacity: 0.85, boxShadow: `0 0 16px ${acc}55`}} />;
      })}
    </div>
  );
};

// ---------- step chip (number + one sentence) ----------
const Step: React.FC<{n: number; text: string; dur: number; acc: string}> = ({n, text, dur, acc}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 160, 16), o = 1 - lin(f, dur - 8, dur);
  return (
    <div style={{position: 'absolute', left: 50, right: 50, top: 1330, display: 'flex', justifyContent: 'center', opacity: Math.min(1, p * 1.4) * o, transform: `translateY(${(1 - p) * 40}px)`}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 18, padding: '14px 28px 14px 14px', borderRadius: 40, background: 'rgba(10,14,22,0.88)', border: `3px solid ${acc}`, direction: 'rtl', maxWidth: 960}}>
        <div style={{width: 70, height: 70, borderRadius: '50%', background: acc, color: '#14181F', fontFamily: EN, fontWeight: 900, fontSize: 38, display: 'flex', alignItems: 'center',
          justifyContent: 'center', flexShrink: 0}}>{n}</div>
        <span style={{fontFamily: AR, fontWeight: 900, fontSize: 42, color: '#fff', lineHeight: 1.3}}>{bi(text)}</span>
      </div>
    </div>
  );
};

// ---------- big statement in the stage (hook / result / tip) ----------
const Big: React.FC<{text: string; sub?: string; ico?: string; dur: number; acc: string; y?: number}> = ({text, sub, ico, dur, acc, y = 640}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const o = 1 - lin(f, dur - 8, dur);
  const q = spr(f, fps, 0, 140, 12);
  return (
    <div style={{position: 'absolute', left: 50, right: 50, top: y - 90, opacity: o, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 26}}>
      {ico ? <div style={{width: 300, height: 300, borderRadius: 80, background: 'rgba(255,255,255,0.06)', border: `3px solid ${acc}66`, boxShadow: `0 0 80px ${acc}44`,
        display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${0.5 + 0.5 * q}) rotate(${(1 - q) * -15}deg)`}}><Ico n={ico} s={2.2} c={acc} /></div> : null}
      <Type text={text} at={2} size={78} per={3} width={980} pill={acc} />
      {sub ? <div style={{opacity: lin(f, 20, 34)}}><Type text={sub} at={20} size={44} per={2} width={940} color={G.soft} pill={acc} /></div> : null}
    </div>
  );
};

// "⚡ أسهل في 2026" vertical card (thumbnail + QR), same content rules as the course.
const New26V: React.FC<{title: string; how: string; thumb?: string; qr?: string; channel?: string; src: string; dur: number}> = ({title, how, thumb, qr, channel, src, dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 140, 16), o = 1 - lin(f, dur - 10, dur);
  return (
    <div style={{position: 'absolute', left: 60, top: CTOP + 20, opacity: Math.min(1, p * 1.4) * o, transform: `translateY(${(1 - p) * 60}px)`}}>
      <Glass w={960} pad={30} r={40} glow={CC.violet}>
        <div style={{display: 'flex', direction: 'rtl'}}><div style={{padding: '6px 20px', borderRadius: 24, background: CC.violet, fontFamily: AR, fontWeight: 900, fontSize: 34, color: '#fff'}}>⚡ أسهل في Premiere 2026</div></div>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 54, color: '#fff', direction: 'rtl', textAlign: 'right', marginTop: 16}}>{bi(title)}</div>
        <div style={{fontFamily: AR, fontWeight: 700, fontSize: 36, color: G.soft, direction: 'rtl', textAlign: 'right', marginTop: 8, lineHeight: 1.4}}>{bi(how)}</div>
        {thumb && qr ? (
          <div style={{display: 'flex', gap: 20, marginTop: 20, alignItems: 'center', direction: 'rtl'}}>
            <Img src={staticFile(thumb)} style={{width: 480, height: 270, objectFit: 'cover', borderRadius: 18, border: '2px solid rgba(255,255,255,0.25)'}} />
            <div style={{background: '#fff', padding: 10, borderRadius: 14}}><Img src={staticFile(qr)} style={{width: 220, height: 220, display: 'block'}} /></div>
          </div>
        ) : null}
        {thumb ? <div style={{fontFamily: AR, fontWeight: 800, fontSize: 30, color: G.gold, direction: 'rtl', textAlign: 'right', marginTop: 12}}>{bi(`Claude هو اللي بيرشح الفيديو ده (${channel})، مش علي`)}</div> : null}
        <div style={{marginTop: 14, display: 'flex', justifyContent: 'flex-end'}}><Src text={src} s={1.1} /></div>
      </Glass>
    </div>
  );
};

// concept animation (made for a 640 px column) scaled into the vertical stage
const AnimV: React.FC<{name: string; dur: number; mini?: boolean; [k: string]: any}> = ({name, dur, mini = false, ...rest}) => {
  const C = courseAnims[name] ?? audioAnims[name] ?? courseScenes[name];
  if (!C) return null;
  // mini = the animation in the top half, his real screen under it (DualCard under)
  const k = mini ? 0.85 : 1.2;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920}}>
      <div style={{position: 'absolute', left: 540 - 340 * k, top: mini ? 330 - 150 * k : CTOP - 150 * 1.2 - 70, width: 680, transform: `scale(${k})`, transformOrigin: '0 0'}}>
        <HideNote.Provider value={true}><C dur={dur} {...rest} /></HideNote.Provider>
      </div>
    </div>
  );
};

// ---------- CTA: his phone clip + QR of the full course at the top (never on his face) ----------
const CtaV: React.FC<{file: string; dur: number; qr: string; vol: number; acc: string; word: string; thumb: string | null}> = ({file, dur, qr, vol, acc, word, thumb}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const q = spr(f, fps, 12, 140, 16);
  return (
    <AbsoluteFill style={{opacity: lin(f, 0, 8)}}>
      <OffthreadVideo src={staticFile(file)} volume={vol} style={{position: 'absolute', inset: 0, width: 1080, height: 1920, objectFit: 'cover'}} />
      <div style={{position: 'absolute', right: 70, top: 300, opacity: q, transform: `scale(${0.8 + 0.2 * q})`, transformOrigin: 'top right', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10}}>
        {thumb ? <Img src={staticFile(thumb)} style={{width: 400, height: 225, objectFit: 'cover', borderRadius: 16, border: '3px solid #fff', boxShadow: '0 20px 50px rgba(0,0,0,0.5)'}} /> : null}
        <div style={{background: '#fff', padding: 12, borderRadius: 18, boxShadow: '0 20px 50px rgba(0,0,0,0.5)'}}><Img src={staticFile(qr)} style={{width: 230, height: 230, display: 'block'}} /></div>
        <div style={{padding: '6px 16px', borderRadius: 20, background: 'rgba(10,14,22,0.85)', fontFamily: AR, fontWeight: 900, fontSize: 30, color: '#fff', direction: 'rtl'}}>الكورس الكامل</div>
      </div>
      <div style={{position: 'absolute', left: 60, right: 60, top: 1350, display: 'flex', justifyContent: 'center', opacity: lin(f, 40, 52)}}>
        <div style={{padding: '14px 30px', borderRadius: 40, background: 'rgba(10,14,22,0.88)', border: `3px solid ${acc}`, fontFamily: AR, fontWeight: 900, fontSize: 48, color: '#fff', direction: 'rtl'}}>
          اكتب <span style={{color: acc}}>"{word}"</span> في كومنت 💬
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- end card: course thumbnail + QR of the full video (a YouTube QR never without its thumbnail, Aly 2026-10-21) ----------
const EndCard: React.FC<{thumb: string; qr: string; title: string; dur: number; acc: string}> = ({thumb, qr, title, dur, acc}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 140, 16), q = spr(f, fps, 10, 150, 14), o = 1 - lin(f, dur - 8, dur);
  return (
    <AbsoluteFill style={{opacity: o, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 34, paddingTop: 160}}>
      <div style={{fontFamily: AR, fontWeight: 900, fontSize: 58, color: '#fff', direction: 'rtl', opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * -30}px)`}}>{bi(title)}</div>
      <Img src={staticFile(thumb)} style={{width: 940, height: 529, objectFit: 'cover', borderRadius: 28, border: `5px solid ${acc}`, boxShadow: `0 0 60px ${acc}66`,
        transform: `scale(${0.85 + 0.15 * p})`, opacity: Math.min(1, p * 1.4)}} />
      <div style={{display: 'flex', alignItems: 'center', gap: 30, direction: 'rtl', opacity: Math.min(1, q * 1.4), transform: `translateY(${(1 - q) * 40}px)`}}>
        <div style={{background: '#fff', padding: 14, borderRadius: 20}}><Img src={staticFile(qr)} style={{width: 260, height: 260, display: 'block'}} /></div>
        <div style={{fontFamily: AR, fontWeight: 800, fontSize: 40, color: G.soft, lineHeight: 1.5}}>امسح الـ QR<br />أو اللينك في الوصف</div>
      </div>
    </AbsoluteFill>
  );
};

export const CourseShort: React.FC<Props> = ({look, series, voice, screens, cues, cta, music, sfx, env, words, brand, src, end, footer}) => {
  const {fps} = useVideoConfig();
  const now = useCurrentFrame();
  const L = LOOK[look] ?? LOOK.glass;
  const fr = (s: number) => Math.round(s * fps);
  const inCta = cta ? now >= fr(cta.at) : false;
  const inEnd = end ? now >= fr(end.at) : false;
  const live = (t: number, d: number) => now >= fr(t) - 2 && now < fr(t + d) + 2;
  return (
    <SrcCtx.Provider value={src}>
    <AbsoluteFill style={{background: '#07090D'}}>
      <style>{fontCss + popFontCss}</style>
      <L.Bg />
      {screens.map((s, i) => !live(s.t, s.d) ? null : (
        <Sequence key={'s' + i} from={fr(s.t)} durationInFrames={fr(s.d)} layout="none">
          {s.dual ? <DualCard file={s.file} from={s.from} d={s.d} top={s.dual.top} bottom={s.dual.bottom} acc={L.acc} under={s.under} marks={s.marks} />
            : <ScreenCard file={s.file} from={s.from} d={s.d} keys={s.keys} marks={s.marks} y={s.y} acc={L.acc} cin={s.cin} cout={s.cout} />}
        </Sequence>
      ))}
      {cues.map((c, i) => {
        if (!live(c.t, c.d)) return null;
        const d = fr(c.d);
        let el: React.ReactNode = null;
        if (c.k === 'Step') el = <StepPanel {...(c.p as any)} dur={d} acc={L.acc} />;
        else if (c.k === 'BeforeAfter') el = <BeforeAfter {...(c.p as any)} dur={d} acc={L.acc} />;
        else if (c.k === 'Bars') el = <VoiceBars env={env} at={fr(c.t)} acc={L.acc} acc2={L.acc2} />;
        else if (c.k === 'Big') el = <Big {...(c.p as any)} dur={d} acc={L.acc} />;
        else if (c.k === 'Label') el = <Label {...(c.p as any)} dur={d} acc={L.acc} />;
        else if (c.k === 'Fix') el = <Fix {...(c.p as any)} dur={d} />;
        else if (c.k === 'Kw') el = <Kw {...(c.p as any)} dur={d} x={540} y={CTOP + CH - 50} />;
        else if (c.k === 'Key') el = <Key {...(c.p as any)} dur={d} x={1000} y={CTOP + CH - 160} />;
        else if (c.k === 'Def') el = <Def {...(c.p as any)} dur={d} x={540} y={1000} w={940} color={L.acc} />;
        else if (c.k === 'New26') el = <New26V {...(c.p as any)} dur={d} />;
        else if (shortScenes[c.k]) { const S2 = shortScenes[c.k]; el = <S2 {...(c.p as any)} dur={d} />; }
        else if (sound3d[c.k]) { const S3 = sound3d[c.k]; el = <S3 {...(c.p as any)} dur={d} />; }
        else el = <AnimV name={c.k} {...(c.p as any)} dur={d} />;
        return <Sequence key={'c' + i} from={fr(c.t)} durationInFrames={d} layout="none">{el}</Sequence>;
      })}
      {end ? <Sequence from={fr(end.at)} durationInFrames={fr(end.d)}><EndCard thumb={end.thumb} qr={end.qr} title={end.title} dur={fr(end.d)} acc={L.acc} /></Sequence> : null}
      {cta ? <Sequence from={fr(cta.at)} durationInFrames={fr(cta.d)}><CtaV file={cta.file} dur={fr(cta.d)} qr={cta.qr} vol={cta.vol} acc={L.acc} word={cta.word} thumb={cta.thumb} /></Sequence> : null}
      {inCta ? null : <L.Fx />}
      {inCta || inEnd ? null : <Captions words={words} maxWords={4} accent="gold" previewBg="" lift={0} bottomFrac={0.225} />}
      <SeriesFrame {...series} acc={L.acc} logo={brand.logo} name={brand.name} />
      {footer && !inCta ? (
        <div style={{position: 'absolute', left: 0, right: 0, bottom: 34, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 14, direction: 'ltr', opacity: 0.92}}>
          <Img src={staticFile(footer.face)} style={{height: 70}} />
          <Img src={staticFile(footer.name)} style={{height: 36}} />
        </div>) : null}
      {voice.map((v, i) => (
        <Sequence key={'v' + i} from={fr(v.at)} durationInFrames={Math.max(1, fr(v.to - v.from))} layout="none">
          <Audio src={staticFile(v.file)} startFrom={fr(v.from)} volume={(f) => v.gain * Math.min(1, f / 2, (fr(v.to - v.from) - f) / 2)} />
        </Sequence>
      ))}
      {music.map((m, i) => (
        <Sequence key={'m' + i} from={fr(m.t)} durationInFrames={fr(m.d)} layout="none">
          <Audio src={staticFile(m.file)} startFrom={fr(m.from)} volume={(f) => m.vol * Math.min(1, f / 15, (fr(m.d) - f) / 15)} />
        </Sequence>
      ))}
      {sfx.map((s, i) => <Sequence key={'x' + i} from={fr(s.t)} durationInFrames={fr(2)} layout="none"><Audio src={staticFile(s.file)} volume={s.vol} /></Sequence>)}
    </AbsoluteFill>
    </SrcCtx.Provider>
  );
};
