import React from 'react';
import {Img, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {enter, exit, lerp} from '../blocks/anim';
import {E, Grain, Hi, Sticker, stickerBorder, Tape} from './kit';

// Collage of internet pictures (thumbnail look): photos with a white border drop in one by one on their words,
// tilted, taped, optional sepia, a caption on a tape strip. A photo can also be a short muted clip (.mp4/.webm).
// x/y = centre of each photo (0..1 of the frame), w = width in px, at = frame inside the cue.
const item = z.object({
  src: z.string(), x: z.number(), y: z.number(), w: z.number().default(440), h: z.number().default(0), at: z.number().default(0),
  rot: z.number().default(0), caption: z.string().default(''), sepia: z.boolean().default(false), pos: z.string().default('50% 40%'),
  fit: z.enum(['cover', 'contain']).default('cover'), sticker: z.string().default(''), start: z.number().default(0),
  bare: z.boolean().default(false), // logo alone: no white card, no tape (ep01: a logo in a white card looked like an empty picture)
});
export const entaPhotosSchema = z.object({
  items: z.array(item).default([
    {src: 'enta/fx_bokeh.jpg', x: 0.5, y: 0.35, w: 520, h: 0, at: 0, rot: -4, caption: 'صورة *من النت*', sepia: false, pos: '50% 40%', fit: 'cover', sticker: 'star_y', start: 0, bare: false},
  ]),
  accent: z.enum(['orange', 'blue', 'olive', 'mustard']).default('orange'),
  previewBg: z.string().default(''),
});

const isVid = (s: string) => /\.(mp4|webm|mov)$/i.test(s);

export const EntaPhotos: React.FC<z.infer<typeof entaPhotosSchema>> = ({items, accent, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const out = exit(frame, durationInFrames, 9);
  const acc = (E as Record<string, string>)[accent];
  return (
    <Base previewBg={previewBg}>
      {[false, true].map((capPass) => items.map((it, i) => {
        // 2 passes (biz ep01 review 2026-10-28: a caption was hidden under the next photo's tape): photos first, then every caption
        // on top of all the photos, with the same box + motion as its photo.
        const p = enter(frame, fps, it.at);
        if (frame < it.at || (capPass && !it.caption)) return null;
        const h = it.h || it.w * 0.66;
        const drift = (frame - it.at) / 30; // slow Ken Burns inside the frame
        const media: React.CSSProperties = {width: '100%', height: '100%', objectFit: it.fit, objectPosition: it.pos,
          transform: `scale(${1.04 + drift * 0.01})`, filter: it.sepia ? 'sepia(.85) contrast(1.1) brightness(.95)' : 'none',
          background: it.fit === 'contain' && !it.bare ? E.white : undefined};
        return (
          <div key={(capPass ? 'c' : 'p') + i} style={{position: 'absolute', left: it.x * width - it.w / 2, top: it.y * height - h / 2, width: it.w, height: h,
            opacity: Math.min(1, p * 1.6) * out,
            transform: `translateY(${lerp(p, -70, 0) + lerp(out, 50, 0)}px) scale(${lerp(p, 1.3, 1)}) rotate(${lerp(p, it.rot * 3, it.rot)}deg)`}}>
            {capPass ? null : (
              <>
                <div style={it.bare ? {position: 'absolute', inset: 0, filter: 'drop-shadow(0 12px 24px rgba(0,0,0,.5))'} : {position: 'absolute', inset: 0, overflow: 'hidden', background: '#222', ...stickerBorder(10)}}>
                  {isVid(it.src)
                    ? <OffthreadVideo muted src={staticFile(it.src)} startFrom={Math.round(it.start * fps)} style={media} />
                    : <Img src={staticFile(it.src)} style={media} />}
                  {it.bare ? null : <Grain opacity={0.18} seed={11 + i} />}
                </div>
                {it.bare ? null : <Tape w={150} rot={-38} style={{top: -18, left: -50}} />}
                {it.bare ? null : <Tape w={150} rot={38} olive style={{bottom: -14, right: -50}} />}
                {it.sticker ? (
                  <div style={{position: 'absolute', top: -55, right: -45, transform: `scale(${enter(frame, fps, it.at + 8)}) rotate(${Math.sin(frame / 8) * 8}deg)`}}>
                    <Sticker name={it.sticker} size={120} />
                  </div>
                ) : null}
              </>
            )}
            {capPass ? (
              <div style={{position: 'absolute', bottom: -42, left: '50%', transform: `translateX(-50%) rotate(${-it.rot * 0.6 - 2}deg)`,
                background: E.paper, color: E.ink, padding: '6px 24px', fontWeight: 900, fontSize: 36, whiteSpace: 'nowrap',
                borderRadius: 6, boxShadow: '0 8px 18px rgba(0,0,0,.45)', opacity: enter(frame, fps, it.at + 6)}}>
                <Hi text={it.caption} color={acc} />
              </div>
            ) : null}
          </div>
        );
      }))}
    </Base>
  );
};
