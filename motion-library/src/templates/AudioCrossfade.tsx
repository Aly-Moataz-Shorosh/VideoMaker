import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {C, theme, isVertical} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

// Explains an audio cross fade: two clips meet with a hard cut ("click"), then they overlap, clip A fades out
// while clip B fades in (X-shaped volume lines) and a playhead plays through smoothly. Frames relative to cue start.
export const audioCrossfadeSchema = z.object({
  title: z.string().default('Cross fade audio'),
  overlapAt: z.number().default(80),
  doneAt: z.number().default(150),
  aLabel: z.string().default('المشهد اللي فات'),
  bLabel: z.string().default('المشهد اللي جاي'),
  doneLabel: z.string().default('من غير صوت قطعة ✓'),
  top: z.number().default(0.39),
  previewBg: z.string().default(''),
});

const cl = (f: number, a: number, b: number) => interpolate(f, [a, b], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

export const AudioCrossfade: React.FC<z.infer<typeof audioCrossfadeSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vertical = isVertical(width, height);
  const pOut = exit(frame, durationInFrames);
  const k = Math.min(enter(frame, fps), pOut);
  const W = vertical ? width * 0.9 : width * 0.46;
  const H = W * 0.52;
  const left = (width - W) / 2;
  const top = vertical ? height * p.top : height * 0.14;
  const pad = 30, trackW = W - pad * 2, y = H * 0.3, h = H * 0.36;
  const ov = cl(frame, p.overlapAt, p.overlapAt + 20); // B slides over A
  const done = cl(frame, p.doneAt, p.doneAt + 10);
  const clipW = trackW * 0.5, olap = trackW * 0.18 * ov;
  const ax = pad, bx = pad + clipW - olap;
  const cutX = pad + clipW;
  // LTR timeline (time flows left -> right) even in RTL UI
  const bars = (x0: number, w: number, color: string, gain: (u: number) => number, seed: number) => Array.from({length: 22}, (_, i) => {
    const u = (i + 0.5) / 22;
    const a = (0.35 + 0.6 * Math.abs(Math.sin(i * 1.3 + seed))) * gain(u);
    const bw = w / 22;
    return <div key={i} style={{position: 'absolute', left: x0 + i * bw + bw * 0.2, width: bw * 0.6, top: y + h / 2 - (h * 0.85 * a) / 2,
      height: h * 0.85 * a, background: color, borderRadius: 4, opacity: 0.95}} />;
  });
  const fadeFrac = (olap / clipW) || 0;
  const gainA = (u: number) => (u > 1 - fadeFrac ? (1 - u) / Math.max(fadeFrac, 1e-3) : 1);
  const gainB = (u: number) => (u < fadeFrac ? u / Math.max(fadeFrac, 1e-3) : 1);
  const play = cl(frame, p.overlapAt + 24, p.doneAt);
  const head = lerp(play, ax + clipW * 0.55, bx + clipW * 0.45);
  const click = frame < p.overlapAt ? 0.5 + 0.5 * Math.sin(frame / 3) : 1 - ov;
  return (
    <Base previewBg={p.previewBg}>
      <div style={{position: 'absolute', left, top, width: W, height: H, opacity: Math.min(1, k * 1.4),
        transform: `translateY(${lerp(k, 140, 0)}px) scale(${lerp(k, 0.85, 1)})`}}>
        <div style={{position: 'absolute', inset: -8, borderRadius: theme.radius + 8, background: `linear-gradient(135deg, ${C.gold}, ${C.blue})`, boxShadow: theme.shadow}} />
        <div style={{position: 'absolute', inset: 0, borderRadius: theme.radius, background: C.bg, overflow: 'hidden'}}>
          <div style={{position: 'absolute', top: 12, right: 26, fontSize: 40, fontWeight: 900, fontFamily: 'Montserrat', direction: 'ltr'}}>{p.title}</div>
          <div style={{position: 'absolute', left: ax, width: clipW, top: y, height: h, borderRadius: 12, background: `${C.blue}55`, border: `3px solid ${C.blue}`}} />
          {bars(ax, clipW, C.blue, gainA, 0)}
          <div style={{position: 'absolute', left: bx, width: clipW, top: y + (ov ? 0 : 0), height: h, borderRadius: 12, background: `${C.gold}44`, border: `3px solid ${C.gold}`}} />
          {bars(bx, clipW, C.gold, gainB, 2)}
          {/* X-shaped fade lines over the overlap */}
          {ov > 0.05 ? (
            <svg style={{position: 'absolute', left: bx, top: y, width: olap, height: h, overflow: 'visible'}}>
              <line x1={0} y1={6} x2={olap} y2={h - 6} stroke={C.ink} strokeWidth={5} strokeDasharray="10 7" />
              <line x1={0} y1={h - 6} x2={olap} y2={6} stroke={C.ink} strokeWidth={5} strokeDasharray="10 7" />
            </svg>
          ) : null}
          <div style={{position: 'absolute', left: ax + 10, top: y + h + 10, whiteSpace: 'nowrap', fontSize: 30, fontWeight: 800, color: C.blue}}>{p.aLabel}</div>
          <div style={{position: 'absolute', left: bx + clipW - 10, top: y + h + 10, transform: 'translateX(-100%)', whiteSpace: 'nowrap', fontSize: 30, fontWeight: 800, color: C.gold}}>{p.bLabel}</div>
          {/* hard cut "click" before the fade */}
          <div style={{position: 'absolute', left: cutX - 34, top: y - 66, fontSize: 40, fontWeight: 900, color: C.red, opacity: click,
            transform: `scale(${1 + 0.15 * Math.sin(frame / 2)})`}}>طق! 💥</div>
          {play > 0 ? <div style={{position: 'absolute', left: head, top: y - 14, width: 5, height: h + 28, background: C.ink, boxShadow: `0 0 12px ${C.ink}`}} /> : null}
          <div style={{position: 'absolute', bottom: 12, left: 0, right: 0, textAlign: 'center', fontSize: 42, fontWeight: 900, color: C.green, opacity: done,
            transform: `scale(${lerp(done, 0.7, 1)})`}}>{p.doneLabel}</div>
        </div>
      </div>
    </Base>
  );
};
