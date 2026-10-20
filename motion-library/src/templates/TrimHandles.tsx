import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {C, theme, isVertical} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

// Explains Pre head / Post tail: a speech clip between silences. Silence is cut away, but a few frames
// before (pre) and after (post) the speech stay, then everything closes up. Frames relative to cue start.
export const trimHandlesSchema = z.object({
  title: z.string().default('Pre head / Post tail'),
  cutAt: z.number().default(20),
  preAt: z.number().default(55),
  postAt: z.number().default(100),
  closeAt: z.number().default(150),
  preLabel: z.string().default('Pre head'),
  postLabel: z.string().default('Post tail'),
  doneLabel: z.string().default('الكلام مش مقصوص ✓'),
  top: z.number().default(0.39),
  previewBg: z.string().default(''),
});

const cl = (f: number, a: number, b: number) => interpolate(f, [a, b], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

export const TrimHandles: React.FC<z.infer<typeof trimHandlesSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vertical = isVertical(width, height);
  const pOut = exit(frame, durationInFrames);
  const k = Math.min(enter(frame, fps), pOut);
  const W = vertical ? width * 0.9 : width * 0.46;
  const H = W * 0.5;
  const left = (width - W) / 2;
  const top = vertical ? height * p.top : height * 0.14;
  const pad = 36, trackW = W - pad * 2, trackY = H * 0.36, trackH = H * 0.3;
  // layout (fractions of track): silence 0-.3 | speech .3-.7 | silence .7-1 ; handles = .08 each
  const S0 = 0.3, S1 = 0.7, HW = 0.08;
  const cut = cl(frame, p.cutAt, p.cutAt + 10);
  const pre = cl(frame, p.preAt, p.preAt + 10);
  const post = cl(frame, p.postAt, p.postAt + 10);
  const close = cl(frame, p.closeAt, p.closeAt + 18);
  const gone = cl(frame, p.closeAt - 6, p.closeAt + 6);
  // after closing: pre handle + speech + post handle centered
  const total = HW + (S1 - S0) + HW, off = (1 - total) / 2;
  const X = (f: number, closed: number) => pad + trackW * lerp(close, f, closed);
  const block = (x0: number, x1: number, bg: string, extra: React.CSSProperties = {}) => (
    <div style={{position: 'absolute', left: x0, width: Math.max(0, x1 - x0), top: trackY, height: trackH, borderRadius: 10, background: bg, ...extra}} />
  );
  const wave = (x0: number, x1: number) => Array.from({length: 18}, (_, i) => {
    const a = 0.35 + 0.6 * Math.abs(Math.sin(i * 1.7));
    const w = (x1 - x0) / 18;
    return <div key={i} style={{position: 'absolute', left: x0 + i * w + w * 0.2, width: w * 0.6, top: trackY + trackH / 2 - (trackH * 0.8 * a) / 2,
      height: trackH * 0.8 * a, background: '#ffffff66', borderRadius: 4}} />;
  });
  const sp0 = X(S0, off + HW), sp1 = X(S1, off + HW + (S1 - S0));
  const tag = (x: number, txt: string, c: string, o: number, below = false) => (
    <div style={{position: 'absolute', left: x, top: below ? trackY + trackH + 16 : trackY - 62, transform: `translateX(-50%) scale(${lerp(o, 0.6, 1)})`,
      opacity: o, background: c, color: C.outline, fontWeight: 900, fontSize: 32, padding: '0 14px', borderRadius: 10, whiteSpace: 'nowrap',
      fontFamily: 'Montserrat', direction: 'ltr'}}>{txt}</div>
  );
  return (
    <Base previewBg={p.previewBg}>
      <div style={{position: 'absolute', left, top, width: W, height: H, opacity: Math.min(1, k * 1.4),
        transform: `translateY(${lerp(k, 140, 0)}px) scale(${lerp(k, 0.85, 1)})`}}>
        <div style={{position: 'absolute', inset: -8, borderRadius: theme.radius + 8, background: `linear-gradient(135deg, ${C.gold}, ${C.blue})`, boxShadow: theme.shadow}} />
        <div style={{position: 'absolute', inset: 0, borderRadius: theme.radius, background: C.bg, overflow: 'hidden'}}>
          <div style={{position: 'absolute', top: 12, right: 26, fontSize: 40, fontWeight: 900, fontFamily: 'Montserrat', direction: 'ltr'}}>{p.title}</div>
          {/* silence left / right (red when cut, disappears on close) */}
          {block(X(0, off), X(S0 - HW, off), cut ? C.red : '#3A4352', {opacity: (1 - gone) * lerp(cut, 1, 0.75)})}
          {block(X(S1 + HW, off + total), X(1, off + total), cut ? C.red : '#3A4352', {opacity: (1 - gone) * lerp(cut, 1, 0.75)})}
          {/* handles: grey silence -> gold kept frames */}
          {block(X(S0 - HW, off), X(S0, off + HW), pre ? C.gold : cut ? C.red : '#3A4352', {opacity: pre ? 1 : (1 - gone) * lerp(cut, 1, 0.75)})}
          {block(X(S1, off + HW + (S1 - S0)), X(S1 + HW, off + total), post ? C.gold : cut ? C.red : '#3A4352', {opacity: post ? 1 : (1 - gone) * lerp(cut, 1, 0.75)})}
          {block(sp0, sp1, C.blue, {boxShadow: `0 0 18px ${C.blue}`})}
          {wave(sp0, sp1)}
          <div style={{position: 'absolute', left: sp0, width: sp1 - sp0, top: trackY - 58, textAlign: 'center', fontSize: 36, fontWeight: 900,
            color: C.blue, textShadow: theme.textShadow}}>كلام</div>
          {cut && !gone ? ['✂️', '✂️'].map((s, i) => (
            <div key={i} style={{position: 'absolute', left: X(i ? 0.85 : 0.1, 0), top: trackY + trackH + 10, fontSize: 44, opacity: cut}}>{s}</div>
          )) : null}
          {tag((X(S0 - HW, off) + X(S0, off + HW)) / 2, p.preLabel, C.gold, pre)}
          {tag((X(S1, off + HW + (S1 - S0)) + X(S1 + HW, off + total)) / 2, p.postLabel, C.gold, post)}
          <div style={{position: 'absolute', bottom: 16, left: 0, right: 0, textAlign: 'center', fontSize: 42, fontWeight: 900, color: C.green, opacity: close}}>
            {p.doneLabel}
          </div>
        </div>
      </div>
    </Base>
  );
};
