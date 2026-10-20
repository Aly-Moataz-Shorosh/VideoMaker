import React from 'react';
import {Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {enter, exit, lerp} from '../blocks/anim';
import {accentOf, E, Grain, Hi, Sticker, stickerBorder, Tape} from './kit';

// Term explainer card (show bible: "every term → explainer card + example"). Paper card with a white sticker
// border slaps onto the screen, tape lands on top, then the meaning, then "مثال" with a drawn arrow.
// side = where the card sits (opposite the speaker); 'center' = gap between Aly and the guest in the wide shot.
export const entaTermSchema = z.object({
  term: z.string().default('رسومات *تنفيذية*'),
  en: z.string().default(''), // English name under the term (LTR)
  def: z.string().default('الرسمة اللي المقاول بيبني منها'),
  example: z.string().default(''),
  exampleAt: z.number().default(45), // frame the example line appears (on its word)
  pic: z.string().default(''), // optional small picture inside the card (public path)
  sticker: z.string().default(''), // optional sticker from his sheet on the card corner
  side: z.enum(['left', 'right', 'center']).default('right'),
  accent: z.enum(['orange', 'blue', 'olive', 'mustard']).default('orange'),
  paper: z.enum(['cream', 'blue']).default('cream'),
  top: z.number().default(0.12),
  previewBg: z.string().default(''),
});

export const EntaTerm: React.FC<z.infer<typeof entaTermSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const inP = enter(frame, fps), out = exit(frame, durationInFrames, 9), k = Math.min(inP, out);
  const tape = enter(frame, fps, 5), defP = enter(frame, fps, 9), exP = enter(frame, fps, p.exampleAt);
  const acc = accentOf(p.accent);
  const w = 600;
  const cx = p.side === 'center' ? width / 2 : p.side === 'left' ? width * 0.25 : width * 0.75;
  const rot = p.side === 'left' ? -3 : 3;
  const bg = p.paper === 'blue' ? E.bluePaper : E.paper;
  return (
    <Base previewBg={p.previewBg}>
      <div style={{position: 'absolute', left: cx - w / 2, top: height * p.top, width: w, opacity: Math.min(1, k * 1.5),
        transform: `translateY(${lerp(inP, -40, 0) + lerp(out, 60, 0)}px) scale(${lerp(inP, 1.35, 1) * lerp(out, 0.85, 1)}) rotate(${lerp(inP, rot * 4, rot)}deg)`}}>
        <div style={{position: 'relative', background: bg, borderRadius: 18, padding: '34px 38px 30px', color: E.ink, ...stickerBorder(9)}}>
          <Grain opacity={0.3} seed={7} />
          {p.pic ? (
            <Img src={staticFile(p.pic)} style={{width: '100%', height: 250, objectFit: 'cover', borderRadius: 8, marginBottom: 18,
              border: `5px solid ${E.white}`, filter: 'sepia(.25) contrast(1.05)', opacity: defP}} />
          ) : null}
          <div style={{fontSize: 64, fontWeight: 900, lineHeight: 1.15, textAlign: 'right'}}>
            <Hi text={p.term} color={acc} />
          </div>
          {p.en ? (
            <div style={{direction: 'ltr', textAlign: 'right', fontFamily: 'Montserrat', fontWeight: 700, fontSize: 30, opacity: 0.65,
              marginTop: 2, letterSpacing: 0.5}}>{p.en}</div>
          ) : null}
          <div style={{height: 6, width: `${defP * 40}%`, background: acc, borderRadius: 3, margin: '12px 0 14px auto', transform: 'rotate(-1.5deg)'}} />
          {p.def ? (
            <div style={{fontSize: 38, fontWeight: 700, lineHeight: 1.35, opacity: defP, transform: `translateY(${lerp(defP, 14, 0)}px)`}}>
              <Hi text={p.def} color={acc} />
            </div>
          ) : null}
          {p.example ? (
            <div style={{marginTop: 18, display: 'flex', alignItems: 'center', gap: 14, opacity: exP, transform: `translateX(${lerp(exP, -30, 0)}px)`}}>
              <span style={{background: acc, color: E.white, fontWeight: 900, fontSize: 28, padding: '4px 16px', borderRadius: 10,
                transform: 'rotate(-3deg)', flexShrink: 0}}>مثال</span>
              <span style={{fontSize: 34, fontWeight: 800, lineHeight: 1.3}}><Hi text={p.example} color={acc} /></span>
            </div>
          ) : null}
        </div>
        <Tape w={190} rot={-6} style={{top: -34, left: w / 2 - 95, opacity: tape, transform: `rotate(-6deg) scale(${lerp(tape, 1.4, 1)})`}} />
        {p.sticker ? (
          <div style={{position: 'absolute', top: -60, [p.side === 'left' ? 'right' : 'left']: -50,
            transform: `scale(${enter(frame, fps, 12)}) rotate(${Math.sin(frame / 9) * 6}deg)`}}>
            <Sticker name={p.sticker} size={150} />
          </div>
        ) : null}
      </div>
    </Base>
  );
};
