import React from 'react';
import {Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {C, theme} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

// Free-plan quota running out: a credits battery drains with the count going down, turns red, shakes, "0 credits";
// then the two choices appear (pay / wait). Side card next to Aly.
export const creditsDrainSchema = z.object({
  logo: z.string().default('logos/figma.svg'),
  title: z.string().default('Figma Make Credits'),
  from: z.number().default(30),
  drainAt: z.number().default(10),
  emptyAt: z.number().default(60),
  options: z.array(z.object({text: z.string(), at: z.number()})).default([
    {text: '💸 تدفع فلوس', at: 90}, {text: '⏳ تستنى يوم يومين', at: 120}]),
  side: z.enum(['left', 'right']).default('right'),
  previewBg: z.string().default(''),
});

export const CreditsDrain: React.FC<z.infer<typeof creditsDrainSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const pIn = enter(frame, fps), out = exit(frame, durationInFrames);
  const lvl = interpolate(frame, [p.drainAt, p.emptyAt], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const empty = frame >= p.emptyAt;
  const shake = empty ? Math.sin(frame * 2.2) * 10 * Math.max(0, 1 - (frame - p.emptyAt) / 18) : 0;
  const col = lvl > 0.5 ? C.green : lvl > 0.2 ? C.gold : C.red;
  const vert = height > width;
  const W = 660, left = vert ? (width - W) / 2 : p.side === 'right' ? width * 0.97 - W : width * 0.03;
  return (
    <Base previewBg={p.previewBg}>
      <div style={{position: 'absolute', left, top: height * (vert ? 0.37 : 0.14), width: W, opacity: Math.min(pIn, out), transformOrigin: '50% 0%',
        transform: `translateX(${lerp(pIn, 200, 0) + shake}px) scale(${lerp(pIn, 0.8, 1) * (vert ? 0.82 : 1)})`}}>
        <div style={{background: C.panel, borderRadius: theme.radius, padding: 32, boxShadow: theme.shadow, borderBottom: `8px solid ${col}`}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 16, direction: 'ltr', fontFamily: 'Montserrat', fontWeight: 800, fontSize: 34}}>
            <Img src={staticFile(p.logo)} style={{width: 46, height: 46, objectFit: 'contain'}} />{p.title}
          </div>
          <div style={{marginTop: 26, display: 'flex', alignItems: 'center', gap: 10, direction: 'ltr'}}>
            <div style={{flex: 1, height: 110, borderRadius: 18, border: `6px solid ${C.inkSoft}`, padding: 8, boxSizing: 'border-box'}}>
              <div style={{width: `${lvl * 100}%`, height: '100%', borderRadius: 10, background: col, boxShadow: `0 0 24px ${col}`}} />
            </div>
            <div style={{width: 18, height: 46, borderRadius: 6, background: C.inkSoft}} />
          </div>
          <div style={{marginTop: 18, textAlign: 'center', direction: 'ltr', fontFamily: 'Montserrat', fontWeight: 900, fontSize: 64,
            color: empty ? C.red : C.ink}}>
            {Math.round(lvl * p.from)} <span style={{fontSize: 34, color: C.inkSoft}}>credits</span>
          </div>
          {empty ? (
            <div style={{textAlign: 'center', fontSize: 48, fontWeight: 900, color: C.red, transform: `scale(${lerp(enter(frame, fps, p.emptyAt), 1.6, 1)})`}}>
              الكريدت خلص!
            </div>
          ) : null}
        </div>
        <div style={{display: 'flex', flexDirection: 'column', gap: 18, marginTop: 26, alignItems: 'center'}}>
          {p.options.map((o, i) => {
            const a = enter(frame, fps, o.at);
            if (a <= 0.01) return null;
            return (
              <div key={i} style={{background: '#FFFFFF', color: '#14181F', borderRadius: 999, padding: '6px 36px', fontSize: 48, fontWeight: 900,
                boxShadow: theme.shadow, opacity: a, transform: `translateY(${lerp(a, 40, 0)}px)`}}>{o.text}</div>
            );
          })}
        </div>
      </div>
    </Base>
  );
};
