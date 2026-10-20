import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate, Easing} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {C, theme, isVertical} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

// Animated comparison bars on a glass panel. Highest value gold, others blue. side 'full' = centered big.
export const barChartSchema = z.object({
  title: z.string().default('وقت المونتاج'),
  unit: z.string().default(' دقيقة'),
  items: z.array(z.object({label: z.string(), value: z.number()})).default([
    {label: 'يدوي', value: 60}, {label: 'Ripple Delete', value: 5},
  ]),
  side: z.enum(['left', 'right', 'full']).default('left'),
  previewBg: z.string().default(''),
});

export const BarChart: React.FC<z.infer<typeof barChartSchema>> = ({title, unit, items, side, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vertical = isVertical(width, height);
  const pIn = enter(frame, fps);
  const pOut = exit(frame, durationInFrames);
  const max = Math.max(...items.map((i) => i.value), 1);
  const full = side === 'full' || vertical;
  const w = full ? width * (vertical ? 0.86 : 0.6) : width * 0.3;
  const left = full ? (width - w) / 2 : side === 'left' ? width * 0.03 : width * 0.97 - w;
  const top = vertical ? height * 0.38 : height * 0.18;
  const barH = Math.min(84, (height * 0.5) / items.length - 30);
  return (
    <Base previewBg={previewBg}>
      <div style={{position: 'absolute', left, top, width: w, padding: '34px 40px', borderRadius: theme.radius,
        background: `${C.bg}D9`, backdropFilter: 'blur(14px)', boxShadow: theme.shadow, border: `2px solid ${C.panel}`,
        opacity: Math.min(pIn * 1.5, pOut), transform: `translateY(${lerp(pIn, 60, 0)}px) scale(${lerp(Math.min(pIn, pOut), 0.9, 1)})`}}>
        <div style={{fontSize: 50, fontWeight: 900, marginBottom: 24, display: 'flex', alignItems: 'center', gap: 14}}>
          <span style={{width: 10, height: 44, borderRadius: 5, background: C.gold}} />{title}
        </div>
        {items.map((it, i) => {
          const g = interpolate(frame, [8 + i * 6, 8 + i * 6 + fps * 0.8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
          const isMax = it.value === max;
          const col = isMax ? C.gold : C.blue;
          return (
            <div key={i} style={{marginBottom: 22}}>
              <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 36, fontWeight: 800, color: C.inkSoft, marginBottom: 8}}>
                <span>{it.label}</span>
                <span style={{color: col, fontFamily: 'Montserrat', direction: 'ltr'}}>{Math.round(it.value * g)}{unit}</span>
              </div>
              <div style={{height: barH, borderRadius: barH / 2, background: C.panel, overflow: 'hidden'}}>
                <div style={{height: '100%', width: `${(it.value / max) * 100 * g}%`, borderRadius: barH / 2,
                  background: `linear-gradient(270deg, ${col}, ${col}AA)`, boxShadow: `0 0 24px ${col}66`}} />
              </div>
            </div>
          );
        })}
      </div>
    </Base>
  );
};
