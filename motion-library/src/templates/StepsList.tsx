import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {C, theme, isVertical} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

// Numbered steps that reveal one by one along a growing line; `current` step glows (process / menu path).
export const stepsListSchema = z.object({
  items: z.array(z.string()).default(['Clip', 'Audio Operations', 'Ripple Delete Silence']),
  current: z.number().default(-1), // -1 = last
  stagger: z.number().default(12), // frames between steps
  side: z.enum(['left', 'right']).default('left'),
  previewBg: z.string().default(''),
});

export const StepsList: React.FC<z.infer<typeof stepsListSchema>> = ({items, current, stagger, side, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vertical = isVertical(width, height);
  const pOut = exit(frame, durationInFrames);
  const cur = current < 0 ? items.length - 1 : current;
  const w = vertical ? width * 0.84 : width * 0.32;
  const left = vertical ? (width - w) / 2 : side === 'left' ? width * 0.03 : width * 0.97 - w;
  const top = vertical ? height * 0.4 : height * 0.2;
  const k = vertical ? 1.35 : 1; // bigger in 9:16 (phone screen)
  const rowH = 104 * k;
  const lineP = Math.min(1, frame / (stagger * items.length + 6));
  return (
    <Base previewBg={previewBg}>
      <div style={{position: 'absolute', left, top, width: w, opacity: pOut}}>
        <div style={{position: 'absolute', right: 38, top: 40, width: 6, borderRadius: 3, background: C.panel,
          height: (items.length - 1) * rowH * lineP}} />
        {items.map((t, i) => {
          const p = enter(frame, fps, i * stagger);
          const on = i === cur && frame > i * stagger + 6;
          const isLatin = /^[A-Za-z0-9 .\-]+$/.test(t);
          return (
            <div key={i} style={{height: rowH, display: 'flex', alignItems: 'center', gap: 22, opacity: Math.min(1, p * 1.5),
              transform: `translateX(${lerp(p, side === 'left' ? -80 : 80, 0)}px)`}}>
              <div style={{width: 82 * k, height: 82 * k, borderRadius: 41 * k, flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: on ? C.gold : C.panel, color: on ? C.bg : C.ink, fontFamily: 'Montserrat', fontWeight: 900, fontSize: 40 * k,
                boxShadow: on ? `0 0 30px ${C.gold}99` : theme.shadow, transform: `scale(${on ? 1.08 : 1})`}}>{i + 1}</div>
              <div style={{fontSize: (on ? 54 : 46) * k, fontWeight: 900, color: on ? C.gold : C.ink, fontFamily: isLatin ? 'Montserrat' : 'Cairo',
                direction: isLatin ? 'ltr' : 'rtl', textShadow: theme.textShadow, WebkitTextStroke: `3px ${C.outline}`, paintOrder: 'stroke fill'}}>{t}</div>
            </div>
          );
        })}
      </div>
    </Base>
  );
};
