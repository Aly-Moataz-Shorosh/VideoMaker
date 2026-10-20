import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {C, theme, isVertical} from '../blocks/theme';
import {lerp} from '../blocks/anim';

// Always-on captions from whisper word timestamps (seconds, relative to this clip).
// Shows one short line (chunk) at a time; current word in accent color with a small pop.
export const captionsSchema = z.object({
  words: z.array(z.object({w: z.string(), start: z.number(), end: z.number()})).default([
    {w: 'السكتات', start: 0.0, end: 0.5}, {w: 'اللي', start: 0.5, end: 0.7}, {w: 'في', start: 0.7, end: 0.85},
    {w: 'الفيديو', start: 0.85, end: 1.3}, {w: 'بتاكل', start: 1.4, end: 1.8}, {w: 'وقتك', start: 1.8, end: 2.4},
  ]),
  maxWords: z.number().default(5),
  lift: z.number().default(0),
  bottomFrac: z.number().default(-1), // explicit bottom (fraction of height); -1 = default position // 9:16 split screen: 0..1 moves captions up between the big screen and the speaker
  accent: z.enum(['gold', 'blue']).default('gold'),
  previewBg: z.string().default(''),
});

type Word = {w: string; start: number; end: number};

const chunk = (words: Word[], max: number) => {
  const out: Word[][] = [];
  let cur: Word[] = [];
  words.forEach((wd, i) => {
    cur.push(wd);
    const gap = i + 1 < words.length ? words[i + 1].start - wd.end : 1;
    if (cur.length >= max || gap > 0.45 || /[.!?؟،]$/.test(wd.w)) {
      out.push(cur);
      cur = [];
    }
  });
  if (cur.length) out.push(cur);
  return out;
};

const isLatin = (w: string) => /^[A-Za-z0-9\-.,:'"/]+$/.test(w);
const groupLatin = (line: Word[]) => {
  const out: {ltr: boolean; items: {wd: Word; i: number}[]}[] = [];
  line.forEach((wd, i) => {
    const ltr = isLatin(wd.w);
    const last = out[out.length - 1];
    if (last && last.ltr && ltr) last.items.push({wd, i});
    else out.push({ltr, items: [{wd, i}]});
  });
  return out;
};

export const Captions: React.FC<z.infer<typeof captionsSchema>> = ({words, maxWords, accent, previewBg, lift, bottomFrac}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const t = frame / fps;
  const vertical = isVertical(width, height);
  const lines = chunk(words, vertical ? Math.min(maxWords, 3) : maxWords);
  const line = lines.find((l) => t >= l[0].start - 0.05 && t <= l[l.length - 1].end + 0.25);
  if (!line) return <Base previewBg={previewBg}>{null}</Base>;

  // Always ONE line: shrink font to fit the width (Arabic glyph ~0.55em wide).
  const chars = line.reduce((n, w) => n + w.w.length + 1, 0);
  const fit = Math.min(vertical ? 92 : 68, ((width - 160) / chars) * 1.5);
  return (
    <Base previewBg={previewBg}>
      <div style={{position: 'absolute', left: 60, right: 60, bottom: (bottomFrac ?? -1) >= 0 ? height * (bottomFrac as number) : vertical ? height * (0.27 + 0.17 * (lift ?? 0)) : 70, display: 'flex',
        justifyContent: 'center', flexWrap: 'nowrap', gap: vertical ? '0 30px' : '0 26px'}}>
        {groupLatin(line).map((g, gi) => (
          // Consecutive English words (e.g. "Ripple Delete Silence") keep left-to-right order.
          <span key={gi} style={{display: 'inline-flex', direction: g.ltr ? 'ltr' : 'rtl', gap: vertical ? 30 : 20}}>
            {g.items.map(({wd, i}) => {
              const next = line[i + 1];
              const active = t >= wd.start && t < (next ? next.start : wd.end + 0.2);
              const pop = active ? Math.min(1, (t - wd.start) * 12) : 0;
              return (
                <span key={i} style={{fontSize: fit, fontWeight: 900, color: active ? C[accent] : C.ink,
                  fontFamily: g.ltr ? 'Montserrat' : 'Cairo', opacity: t >= wd.start - 0.05 ? 1 : 0.55,
                  transform: `scale(${active ? lerp(pop, 1.14, 1.05) : 1})`, display: 'inline-block',
                  textShadow: theme.textShadow, WebkitTextStroke: `${vertical ? 5 : 4}px ${C.outline}`, paintOrder: 'stroke fill'}}>
                  {wd.w}
                </span>
              );
            })}
          </span>
        ))}
      </div>
    </Base>
  );
};
