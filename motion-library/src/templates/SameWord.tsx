import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {C, theme} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

// "Different words, SAME thing": chips appear one by one (as Aly says each name), then slide together into one
// card with a "= نفس الحاجة" tag. For terms he repeats in 2-3 forms so everyone understands (UI/UX, ...).
export const sameWordSchema = z.object({
  words: z.array(z.object({text: z.string(), at: z.number()})).default([
    {text: 'UI / UX', at: 0}, {text: 'User Interface & Experience', at: 20}, {text: 'واجهة وتجربة المستخدم', at: 45}]),
  mergeAt: z.number().default(80),
  tag: z.string().default('كلهم نفس الحاجة'),
  side: z.enum(['left', 'right']).default('right'),
  previewBg: z.string().default(''),
});

export const SameWord: React.FC<z.infer<typeof sameWordSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const out = exit(frame, durationInFrames);
  const m = interpolate(frame, [p.mergeAt, p.mergeAt + 14], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const vert = height > width; // 9:16: centered in the graphics zone
  const cx = vert ? width / 2 : p.side === 'right' ? width * 0.77 : width * 0.23;
  const y0b = height * (vert ? 0.4 : 0.3), stepB = vert ? 100 : 120;
  const cols = [C.blue, C.gold, C.green];
  const n = p.words.length;
  return (
    <Base previewBg={p.previewBg}>
      <div style={{position: 'absolute', inset: 0, opacity: out}}>
        {/* bracket that joins the chips */}
        <div style={{position: 'absolute', left: cx - 380, top: height * (vert ? 0.37 : 0.25), width: 760, height: height * (vert ? 0.3 : 0.5), borderRadius: theme.radius + 10,
          border: `6px solid ${C.gold}`, opacity: m, transform: `scale(${lerp(m, 1.15, 1)})`, boxShadow: `0 0 40px ${C.gold}55`, background: `${C.panel}cc`}} />
        {p.words.map((w, i) => {
          const a = enter(frame, fps, w.at);
          if (a <= 0.01) return null;
          const y0 = y0b + i * stepB;
          const y = lerp(m, y0, y0b + i * 98 + 10);
          const en = /[a-z]/i.test(w.text);
          return (
            <div key={i} style={{position: 'absolute', left: cx - 300, width: 600, top: y, display: 'flex', justifyContent: 'center',
              opacity: Math.min(1, a * 1.5), transform: `translateX(${lerp(a, 160, 0)}px) scale(${lerp(a, 0.6, 1)})`}}>
              <div style={{background: C.panel, borderRadius: 999, padding: '6px 34px', fontSize: en ? 46 : 54, fontWeight: 900, whiteSpace: 'nowrap',
                fontFamily: en ? 'Montserrat' : 'Cairo', direction: en ? 'ltr' : 'rtl', boxShadow: theme.shadow,
                borderBottom: `6px solid ${cols[i % 3]}`}}>{w.text}</div>
            </div>
          );
        })}
        {m > 0 ? (
          <div style={{position: 'absolute', left: cx - 300, width: 600, top: y0b + n * 98 + 30, display: 'flex', justifyContent: 'center',
            opacity: enter(frame, fps, p.mergeAt + 8)}}>
            <div style={{background: C.gold, color: '#0B0E13', borderRadius: 999, padding: '4px 40px', fontSize: 56, fontWeight: 900,
              transform: `scale(${lerp(enter(frame, fps, p.mergeAt + 8), 0.4, 1)})`}}>= {p.tag}</div>
          </div>
        ) : null}
      </div>
    </Base>
  );
};
