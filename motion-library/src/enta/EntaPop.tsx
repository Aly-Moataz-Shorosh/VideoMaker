import React from 'react';
import {AbsoluteFill, Img, random, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {enter, exit, lerp} from '../blocks/anim';
import {E, Grain, Hi, Sticker, Tape} from './kit';

// ---------- stickers from his sheet popping around the speakers (reactions, ?!, stars, notes, masks...) ----------
const st = z.object({name: z.string(), x: z.number(), y: z.number(), size: z.number().default(160), at: z.number().default(0), rot: z.number().default(0)});
export const entaStickersSchema = z.object({
  items: z.array(st).default([{name: 'qmark', x: 0.5, y: 0.25, size: 200, at: 0, rot: 8}]),
  previewBg: z.string().default(''),
});
export const EntaStickers: React.FC<z.infer<typeof entaStickersSchema>> = ({items, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const out = exit(frame, durationInFrames, 7);
  return (
    <Base previewBg={previewBg}>
      {items.map((s, i) => {
        const p = enter(frame, fps, s.at);
        if (frame < s.at) return null;
        const wob = Math.sin((frame - s.at) / 6 + i) * 5;
        return (
          <div key={i} style={{position: 'absolute', left: s.x * width - s.size / 2, top: s.y * height - s.size / 2,
            transform: `scale(${p * out}) rotate(${s.rot + wob + lerp(p, -25, 0)}deg)`}}>
            <Sticker name={s.name} size={s.size} />
          </div>
        );
      })}
    </Base>
  );
};

// ---------- blue paper speech bubble next to a speaker's head (thumbnail look) ----------
export const entaBubbleSchema = z.object({
  text: z.string().default('انت بتشتغل *ايه*؟'),
  x: z.number().default(0.5), y: z.number().default(0.2), // bubble centre
  tail: z.enum(['left', 'right']).default('left'), // which side the speaker is on
  w: z.number().default(520),
  accent: z.enum(['orange', 'blue', 'olive', 'mustard']).default('orange'),
  previewBg: z.string().default(''),
});
export const EntaBubble: React.FC<z.infer<typeof entaBubbleSchema>> = ({text, x, y, tail, w, accent, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const p = enter(frame, fps), out = exit(frame, durationInFrames, 7), k = Math.min(p, out);
  const acc = (E as Record<string, string>)[accent];
  const tl = tail === 'left';
  return (
    <Base previewBg={previewBg}>
      <div style={{position: 'absolute', left: x * width - w / 2, top: y * height, width: w, transform: `translateY(-50%) scale(${k}) rotate(${tl ? 2 : -2}deg)`,
        transformOrigin: tl ? '0% 100%' : '100% 100%'}}>
        <div style={{position: 'relative', background: E.bluePaper, borderRadius: 999, padding: '34px 46px', textAlign: 'center',
          border: `6px solid ${E.ink}`, outline: `7px solid ${E.white}`, boxShadow: '0 16px 30px rgba(0,0,0,.5)', overflow: 'hidden'}}>
          <Grain opacity={0.35} seed={21} />
          <div style={{position: 'relative', fontSize: 58, fontWeight: 900, color: E.ink, lineHeight: 1.2}}><Hi text={text} color={acc} /></div>
        </div>
        <svg width={90} height={80} style={{position: 'absolute', bottom: -58, [tl ? 'left' : 'right']: 40, transform: tl ? 'none' : 'scaleX(-1)'}}>
          <path d="M10 0 L70 0 L4 74 Z" fill={E.bluePaper} stroke={E.ink} strokeWidth={6} strokeLinejoin="round" />
          <rect x={14} y={-8} width={50} height={14} fill={E.bluePaper} />
        </svg>
      </div>
    </Base>
  );
};

// ---------- guest name card (lower third): taped paper strip + ON AIR sticker ----------
export const entaNameSchema = z.object({
  name: z.string().default('أحمد معتز شُرُش'),
  role: z.string().default('خريج *فنون جميلة*'),
  side: z.enum(['left', 'right']).default('right'),
  accent: z.enum(['orange', 'blue', 'olive', 'mustard']).default('orange'),
  previewBg: z.string().default(''),
});
export const EntaName: React.FC<z.infer<typeof entaNameSchema>> = ({name, role, side, accent, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const p = enter(frame, fps), r = enter(frame, fps, 8), out = exit(frame, durationInFrames, 10);
  const acc = (E as Record<string, string>)[accent];
  const right = side === 'right';
  return (
    <Base previewBg={previewBg}>
      <div style={{position: 'absolute', [right ? 'right' : 'left']: width * 0.05, top: height * 0.5, display: 'flex', flexDirection: 'column',
        alignItems: right ? 'flex-start' : 'flex-end', transform: `translateX(${lerp(Math.min(p, out), right ? 600 : -600, 0)}px)`}}>
        <div style={{position: 'relative', background: E.paper, color: E.ink, padding: '14px 40px', fontSize: 66, fontWeight: 900,
          borderRadius: 8, border: `7px solid ${E.white}`, boxShadow: '0 14px 28px rgba(0,0,0,.5)', transform: 'rotate(-2deg)', overflow: 'hidden'}}>
          <Grain opacity={0.3} seed={31} />
          <span style={{position: 'relative'}}>{name}</span>
        </div>
        <div style={{marginTop: 10, background: E.ink, color: E.white, padding: '8px 30px', fontSize: 40, fontWeight: 800, borderRadius: 8,
          transform: `rotate(1.5deg) translateX(${lerp(Math.min(r, out), right ? 300 : -300, 0)}px)`, border: `4px solid ${E.white}`}}>
          <Hi text={role} color={acc} />
        </div>
        <div style={{position: 'absolute', top: -120, [right ? 'right' : 'left']: -40, transform: `scale(${enter(frame, fps, 14) * out}) rotate(-8deg)`}}>
          <Sticker name="onair" size={190} />
        </div>
        <Tape w={140} rot={-30} style={{top: -10, [right ? 'left' : 'right']: -40}} />
      </div>
    </Base>
  );
};

// ---------- glitch hit (his sheet: red/blue VHS bars + scanlines), 6-10 frames on cuts / jokes ----------
export const entaGlitchSchema = z.object({seed: z.number().default(1), strength: z.number().default(1), previewBg: z.string().default('')});
export const EntaGlitch: React.FC<z.infer<typeof entaGlitchSchema>> = ({seed, strength, previewBg}) => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const bars = ['fx_glitch_a', 'fx_glitch_b', 'fx_glitch_c', 'fx_pixels'];
  return (
    <Base previewBg={previewBg}>
      <AbsoluteFill style={{mixBlendMode: 'screen', opacity: strength}}>
        {[0, 1, 2].map((i) => {
          const r = (k: number) => random(`${seed}-${frame}-${i}-${k}`);
          return (
            <Img key={i} src={staticFile(`enta/${bars[Math.floor(r(1) * bars.length)]}.jpg`)}
              style={{position: 'absolute', left: (r(2) - 0.3) * width * 0.6, top: r(3) * height * 0.85, width: width * (0.6 + r(4) * 0.6),
                height: height * (0.12 + r(5) * 0.2), objectFit: 'fill'}} />
          );
        })}
        <Img src={staticFile('enta/fx_scanlines.jpg')} style={{width, height, objectFit: 'fill', opacity: 0.22}} />
      </AbsoluteFill>
    </Base>
  );
};

// ---------- light leak / flare sweep (warm, screen blend) for big moments ----------
export const entaLeakSchema = z.object({kind: z.enum(['leak_warm', 'leak_teal', 'flare_h', 'starflare', 'bokeh']).default('leak_warm'),
  x: z.number().default(0.2), y: z.number().default(0.3), previewBg: z.string().default('')});
export const EntaLeak: React.FC<z.infer<typeof entaLeakSchema>> = ({kind, x, y, previewBg}) => {
  const frame = useCurrentFrame();
  const {width, height, durationInFrames} = useVideoConfig();
  const t = frame / durationInFrames;
  const op = Math.sin(Math.PI * Math.min(1, t)) * 0.9;
  return (
    <Base previewBg={previewBg}>
      {/* pure CSS radial glow: fades to 0 well inside the frame, so it can never show a hard edge (ep01: the fx_leak crop did) */}
      <AbsoluteFill style={{mixBlendMode: 'screen', opacity: op, background:
        `radial-gradient(ellipse 45% 60% at ${(x + (t - 0.5) * 0.3) * 100}% ${y * 100}%, ${{leak_warm: 'rgba(255,170,80,.55)', leak_teal: 'rgba(90,200,210,.45)', flare_h: 'rgba(255,160,60,.5)', starflare: 'rgba(255,200,120,.5)', bokeh: 'rgba(255,180,100,.4)'}[kind]} 0%, transparent 70%)`}} />
    </Base>
  );
};

// ---------- bottom note (long videos have NO captions — Aly 2026-10-13): the point being explained, on a taped paper
// strip in the empty lower part of the frame, opposite the person in shot (or centred in the wide shot) ----------
export const entaNoteSchema = z.object({
  text: z.string().default('بيحوّل التصميم لـ*رسومات تنفيذية*'),
  sticker: z.string().default(''),
  side: z.enum(['left', 'right', 'center']).default('center'),
  accent: z.enum(['orange', 'blue', 'olive', 'mustard']).default('orange'),
  previewBg: z.string().default(''),
});
export const EntaNote: React.FC<z.infer<typeof entaNoteSchema>> = ({text, sticker, side, accent, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const p = enter(frame, fps), out = exit(frame, durationInFrames, 8), k = Math.min(p, out);
  const acc = (E as Record<string, string>)[accent];
  const cx = side === 'center' ? 0.5 : side === 'left' ? 0.27 : 0.73;
  const line = enter(frame, fps, 8);
  return (
    <Base previewBg={previewBg}>
      <div style={{position: 'absolute', left: cx * width, bottom: height * 0.07, transform: `translateX(-50%) translateY(${lerp(k, 120, 0)}px) rotate(${lerp(p, 4, -1.5)}deg)`,
        opacity: Math.min(1, k * 1.5), display: 'flex', alignItems: 'center', gap: 16}}>
        <div style={{position: 'relative', background: E.paper, color: E.ink, padding: '12px 34px 16px', borderRadius: 8, fontSize: 50, fontWeight: 900,
          whiteSpace: 'nowrap', border: `6px solid ${E.white}`, boxShadow: '0 12px 26px rgba(0,0,0,.5)', overflow: 'hidden'}}>
          <Grain opacity={0.28} seed={51} />
          <span style={{position: 'relative'}}><Hi text={text} color={acc} /></span>
          <div style={{position: 'absolute', left: 30, right: 30, bottom: 8, height: 6, borderRadius: 3, background: acc, transformOrigin: 'right',
            transform: `scaleX(${line})`, opacity: 0.8}} />
        </div>
        {sticker ? <div style={{transform: `scale(${enter(frame, fps, 6)}) rotate(${Math.sin(frame / 10) * 6}deg)`}}><Sticker name={sticker} size={100} /></div> : null}
        <Tape w={120} rot={-12} style={{top: -26, right: -30}} />
      </div>
    </Base>
  );
};
