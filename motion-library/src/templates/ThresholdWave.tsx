import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base, Highlight} from '../blocks/Base';
import {C, theme, isVertical} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

// Explains a silence threshold: waveform + dB line. Bars under the line turn red and are removed (silence),
// bars over it glow green (speech kept), then the gaps close (ripple delete). Frames relative to cue start.
export const thresholdWaveSchema = z.object({
  title: z.string().default('Threshold'),
  db: z.string().default('-20 dB'),
  silenceAt: z.number().default(60),
  keepAt: z.number().default(120),
  collapseAt: z.number().default(170),
  silenceLabel: z.string().default('تحت الخط = صمت ✂️'),
  keepLabel: z.string().default('فوق الخط = كلام ✓'),
  top: z.number().default(0.39),
  previewBg: z.string().default(''),
});

// Deterministic "speech" envelope: words (loud) separated by pauses (quiet).
const N = 44;
const amps = Array.from({length: N}, (_, i) => {
  const word = Math.floor(i / 6) % 2 === 0 || i % 13 === 7;
  const n = (Math.sin(i * 12.9898) * 43758.5453) % 1;
  const r = Math.abs(n);
  return word ? 0.45 + 0.55 * r : 0.06 + 0.16 * r;
});
const TH = 0.3;

export const ThresholdWave: React.FC<z.infer<typeof thresholdWaveSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vertical = isVertical(width, height);
  const pOut = exit(frame, durationInFrames);
  const k = Math.min(enter(frame, fps), pOut);
  const W = vertical ? width * 0.9 : width * 0.46;
  const H = W * 0.5;
  const left = (width - W) / 2;
  const top = vertical ? height * p.top : height * 0.14;
  const pad = 40, plotW = W - pad * 2, plotH = H - 120, mid = 70 + plotH / 2;
  const red = interpolate(frame, [p.silenceAt, p.silenceAt + 10], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const gone = interpolate(frame, [p.silenceAt + 22, p.silenceAt + 40], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const green = interpolate(frame, [p.keepAt, p.keepAt + 10], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const col = interpolate(frame, [p.collapseAt, p.collapseAt + 20], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const kept = amps.map((a) => a >= TH);
  const nKept = kept.filter(Boolean).length;
  const step = plotW / N, stepK = plotW / nKept;
  let ki = 0;
  const lineY = (plotH / 2) * TH;

  return (
    <Base previewBg={p.previewBg}>
      <div style={{position: 'absolute', left, top, width: W, height: H, opacity: Math.min(1, k * 1.4),
        transform: `translateY(${lerp(k, 140, 0)}px) scale(${lerp(k, 0.85, 1)})`}}>
        <div style={{position: 'absolute', inset: -8, borderRadius: theme.radius + 8, background: `linear-gradient(135deg, ${C.gold}, ${C.blue})`, boxShadow: theme.shadow}} />
        <div style={{position: 'absolute', inset: 0, borderRadius: theme.radius, background: C.bg, overflow: 'hidden'}}>
          <div style={{position: 'absolute', top: 14, right: 26, fontSize: 44, fontWeight: 900, fontFamily: 'Montserrat', direction: 'ltr'}}>{p.title}</div>
          {amps.map((a, i) => {
            const isKept = kept[i];
            const grow = enter(frame, fps, i * 0.6);
            const x0 = pad + i * step;
            const x1 = isKept ? pad + (ki++) * stepK : x0;
            const x = lerp(col, x0, x1);
            const w = lerp(col, step * 0.62, isKept ? stepK * 0.62 : 0);
            const h = plotH * a * grow * (isKept ? 1 : 1 - gone);
            const c = isKept ? (green > 0 ? C.green : C.blue) : (red > 0 ? C.red : C.blue);
            return <div key={i} style={{position: 'absolute', left: x, width: Math.max(0, w), top: mid - h / 2, height: h, borderRadius: 6,
              background: c, opacity: isKept ? 1 : 1 - gone * 0.6, boxShadow: isKept && green ? `0 0 14px ${C.green}` : 'none'}} />;
          })}
          {[-1, 1].map((s) => (
            <div key={s} style={{position: 'absolute', left: pad - 10, right: pad - 10, top: mid + s * lineY, borderTop: `4px dashed ${C.gold}`,
              opacity: interpolate(frame, [12, 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) * (1 - col)}} />
          ))}
          <div style={{position: 'absolute', left: pad, top: mid - lineY - 50, background: C.gold, color: C.outline, fontWeight: 900, fontSize: 34,
            padding: '0 16px', borderRadius: 10, fontFamily: 'Montserrat', direction: 'ltr', opacity: interpolate(frame, [16, 26], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) * (1 - col)}}>
            {p.db}
          </div>
          <div style={{position: 'absolute', bottom: 14, left: 0, right: 0, display: 'flex', justifyContent: 'space-around', fontSize: 38, fontWeight: 900}}>
            <span style={{color: C.red, opacity: red, transform: `scale(${lerp(red, 0.6, 1)})`}}>{p.silenceLabel}</span>
            <span style={{color: C.green, opacity: green, transform: `scale(${lerp(green, 0.6, 1)})`}}>{p.keepLabel}</span>
          </div>
        </div>
      </div>
    </Base>
  );
};
