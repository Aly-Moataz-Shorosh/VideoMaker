import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base, Highlight} from '../blocks/Base';
import {C, theme, isVertical} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

export const keywordPopSchema = z.object({
  text: z.string().default('السكتات بتاكل *وقتك*'),
  tag: z.string().default(''),
  side: z.enum(['left', 'right']).default('left'),
  accent: z.enum(['gold', 'blue']).default('gold'),
  previewBg: z.string().default(''),
});

export const KeywordPop: React.FC<z.infer<typeof keywordPopSchema>> = ({text, tag, side, accent, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vertical = isVertical(width, height);
  const accentC = C[accent];
  const pIn = enter(frame, fps);
  const pOut = exit(frame, durationInFrames);
  const p = Math.min(pIn, pOut);
  const line = enter(frame, fps, 6);
  const tagP = enter(frame, fps, 3);
  // Auto-fit: longer text gets smaller so it stays on 1-2 lines in the side zone.
  const plain = text.replace(/\*/g, '').length;
  const size = (vertical ? 118 : 108) * Math.min(1, 11 / Math.max(11, plain * 0.75));

  const box: React.CSSProperties = vertical
    ? {left: 72, right: 72, top: height * 0.44, alignItems: 'center'} // 9:16 graphics zone 0.40-0.66 (captions below)
    : {
        // RTL: flex-start = right edge. Anchor the block on the edge nearest the speaker.
        [side === 'left' ? 'left' : 'right']: 90,
        width: width * 0.3, // Aly is usually centered
        top: height * 0.28,
        alignItems: side === 'left' ? 'flex-start' : 'flex-end',
      };

  return (
    <Base previewBg={previewBg}>
      <div style={{position: 'absolute', display: 'flex', flexDirection: 'column', gap: 18, ...box}}>
        {tag ? (
          <div
            style={{
              opacity: tagP * pOut,
              transform: `translateY(${lerp(tagP, 20, 0)}px)`,
              background: C.panel,
              borderRadius: 999,
              padding: '8px 26px',
              fontSize: 36,
              fontWeight: 800,
              color: C.inkSoft,
              display: 'flex',
              alignItems: 'center',
              gap: 12,
              boxShadow: theme.shadow,
            }}
          >
            <span style={{width: 14, height: 14, borderRadius: 7, background: accentC}} />
            {tag}
          </div>
        ) : null}
        <div
          style={{
            fontSize: size,
            fontWeight: theme.weights.title,
            lineHeight: 1.15,
            textShadow: theme.textShadow,
            WebkitTextStroke: `3px ${C.outline}`,
            paintOrder: 'stroke fill',
            opacity: p,
            transform: `scale(${lerp(p, 0.6, 1)}) rotate(${lerp(p, -6, -2)}deg)`,
            transformOrigin: side === 'left' ? 'right center' : 'left center',
            textAlign: vertical ? 'center' : 'right',
          }}
        >
          <Highlight text={text} accent={accentC} />
        </div>
        <div
          style={{
            height: 8,
            width: `${Math.min(line, pOut) * 55}%`,
            background: accentC,
            borderRadius: 4,
            transform: 'rotate(-2deg)',
            boxShadow: `0 0 18px ${accentC}88`,
          }}
        />
      </div>
    </Base>
  );
};
