import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate, Easing} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {C, theme, isVertical} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

// Big number counting up beside Aly (optionally a ring when it is a percent).
export const counterSchema = z.object({
  value: z.number().default(20),
  from: z.number().default(0),
  prefix: z.string().default(''),
  suffix: z.string().default(' dB'),
  label: z.string().default('حد الصمت'),
  decimals: z.number().default(0),
  ring: z.boolean().default(false), // show percent ring (value 0..100)
  side: z.enum(['left', 'right']).default('left'),
  accent: z.enum(['gold', 'blue']).default('gold'),
  previewBg: z.string().default(''),
});

export const Counter: React.FC<z.infer<typeof counterSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vertical = isVertical(width, height);
  const pIn = enter(frame, fps);
  const pOut = exit(frame, durationInFrames);
  const k = interpolate(frame, [4, 4 + fps * 1.1], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  const v = lerp(k, p.from, p.value);
  const txt = `${p.prefix}${v.toFixed(p.decimals)}${p.suffix}`;
  const ac = C[p.accent];
  const box: React.CSSProperties = vertical
    ? {left: 0, right: 0, top: height * 0.42}
    : {[p.side]: width * 0.04, width: width * 0.28, top: height * 0.24};
  const R = 150;
  return (
    <Base previewBg={p.previewBg}>
      <div style={{position: 'absolute', ...box, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10,
        opacity: Math.min(pIn * 1.4, pOut), transform: `scale(${lerp(Math.min(pIn, pOut), 0.7, 1)})`}}>
        {p.ring ? (
          <svg width={R * 2 + 40} height={R * 2 + 40} style={{position: 'absolute', top: -40}}>
            <circle cx={R + 20} cy={R + 20} r={R} stroke={C.panel} strokeWidth={22} fill="none" />
            <circle cx={R + 20} cy={R + 20} r={R} stroke={ac} strokeWidth={22} fill="none" strokeLinecap="round"
              strokeDasharray={2 * Math.PI * R} strokeDashoffset={2 * Math.PI * R * (1 - v / 100)} transform={`rotate(-90 ${R + 20} ${R + 20})`} />
          </svg>
        ) : null}
        <div style={{fontFamily: 'Montserrat', fontWeight: 900, fontSize: vertical ? 190 : 170, color: ac, direction: 'ltr',
          lineHeight: 1, marginTop: p.ring ? 80 : 0, textShadow: theme.textShadow, WebkitTextStroke: `4px ${C.outline}`, paintOrder: 'stroke fill'}}>
          {txt}
        </div>
        <div style={{background: C.panel, borderRadius: 999, padding: '10px 30px', fontSize: 44, fontWeight: 800,
          marginTop: p.ring ? 60 : 6, boxShadow: theme.shadow, borderBottom: `4px solid ${ac}`}}>{p.label}</div>
      </div>
    </Base>
  );
};
