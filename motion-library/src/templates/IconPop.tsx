import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {C} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

// Small fast accent: emoji/icon pops near Aly's head with burst lines (fills gaps between big graphics).
export const iconPopSchema = z.object({
  icon: z.string().default('🤯'),
  x: z.number().default(0.33), // center (0..1)
  y: z.number().default(0.28),
  size: z.number().default(170),
  accent: z.enum(['gold', 'blue', 'red', 'green']).default('gold'),
  previewBg: z.string().default(''),
});

export const IconPop: React.FC<z.infer<typeof iconPopSchema>> = ({icon, x, y, size, accent, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const p = Math.min(enter(frame, fps), exit(frame, durationInFrames));
  const burst = Math.min(1, frame / 9);
  const wob = Math.sin(frame / 4) * 6 * (1 - Math.min(1, frame / 30));
  const cx = width * x, cy = height * y;
  return (
    <Base previewBg={previewBg}>
      <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
        {Array.from({length: 8}).map((_, i) => {
          const a = (i / 8) * Math.PI * 2;
          const r1 = size * 0.55 + burst * size * 0.25, r2 = r1 + size * 0.3 * (1 - burst * 0.6);
          return <line key={i} x1={cx + Math.cos(a) * r1} y1={cy + Math.sin(a) * r1} x2={cx + Math.cos(a) * r2} y2={cy + Math.sin(a) * r2}
            stroke={C[accent]} strokeWidth={8} strokeLinecap="round" opacity={1 - burst * 0.9} />;
        })}
      </svg>
      <div style={{position: 'absolute', left: cx - size, top: cy - size, width: size * 2, height: size * 2, display: 'flex',
        alignItems: 'center', justifyContent: 'center', fontSize: size, transform: `scale(${lerp(p, 0.2, 1)}) rotate(${wob}deg)`,
        opacity: p, filter: 'drop-shadow(0 10px 20px rgba(0,0,0,0.5))'}}>{icon}</div>
    </Base>
  );
};
