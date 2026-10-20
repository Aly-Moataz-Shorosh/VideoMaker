import React from 'react';
import {Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base, Highlight} from '../blocks/Base';
import {C, theme, isVertical} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

// Comment-keyword CTA (Aly's comment -> DM automation): a comment box types the keyword, it posts,
// then a DM notification arrives with the link. Frames are relative to the cue start.
export const commentCtaSchema = z.object({
  keyword: z.string().default('يوتيوب'),
  title: z.string().default('اكتب في *كومنت*'),
  dm: z.string().default('ده لينك الفيديو كامل 🎬'),
  typeAt: z.number().default(14),
  sendAt: z.number().default(45),
  dmAt: z.number().default(70),
  avatar: z.string().default('brand/avatar-old.png'),
  name: z.string().default('Aly Shorosh'),
  top: z.number().default(0.4),
  hx: z.number().default(0.5), // 16:9: card center x (fraction) — CTA clip has Aly on the left -> ~0.7
  htop: z.number().default(0.2), // 16:9: card top
  accent: z.enum(['gold', 'blue', 'red', 'green']).default('gold'),
  previewBg: z.string().default(''),
  qr: z.string().default(''), // QR image of the full video link (Aly 2026-10-15: viewers reach the video even if he doesn't reply)
  qrAt: z.number().default(96),
  qrLabel: z.string().default('أو امسح الكود وشوف الفيديو كامل'),
});

export const CommentCta: React.FC<z.infer<typeof commentCtaSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vertical = isVertical(width, height);
  const acc = C[p.accent];
  const pOut = exit(frame, durationInFrames);
  const k = Math.min(enter(frame, fps), pOut);
  const W = vertical ? width * 0.86 : width * 0.36;
  const left = vertical ? (width - W) / 2 : width * p.hx - W / 2;
  const top = vertical ? height * p.top : height * p.htop;

  const chars = [...p.keyword];
  const n = Math.round(interpolate(frame, [p.typeAt, p.sendAt - 8], [0, chars.length], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const typed = chars.slice(0, n).join('');
  const press = frame >= p.sendAt - 4 && frame < p.sendAt + 4;
  const posted = enter(frame, fps, p.sendAt);
  const dmP = enter(frame, fps, p.dmAt);
  const caret = frame < p.sendAt && Math.floor(frame / 8) % 2 === 0;

  const card: React.CSSProperties = {background: '#FFFFFF', color: '#111', borderRadius: theme.radius, boxShadow: theme.shadow};
  return (
    <Base previewBg={p.previewBg}>
      <div style={{position: 'absolute', left, top, width: W, opacity: Math.min(1, k * 1.4) * (p.qr ? 1 - enter(frame, fps, p.qrAt) : 1),
        transform: `translateY(${lerp(k, 140, 0)}px) scale(${lerp(k, 0.85, 1)})`, display: 'flex', flexDirection: 'column', gap: 22}}>
        {p.title ? (
          <div style={{alignSelf: 'center', fontSize: 64, fontWeight: 900, textShadow: theme.textShadow,
            WebkitTextStroke: `3px ${C.outline}`, paintOrder: 'stroke fill'}}>
            <Highlight text={p.title} accent={acc} />
          </div>
        ) : null}
        {posted > 0.01 ? (
          <div style={{...card, display: 'flex', gap: 18, alignItems: 'center', padding: '18px 24px', opacity: posted,
            transform: `translateY(${lerp(posted, 60, 0)}px)`}}>
            <div style={{width: 64, height: 64, borderRadius: 32, background: `linear-gradient(135deg, ${acc}, ${C.red})`, flexShrink: 0}} />
            <div style={{flex: 1}}>
              <div style={{fontSize: 26, color: '#666', fontWeight: 700}}>@انت · دلوقتي</div>
              <div style={{fontSize: 52, fontWeight: 900}}>{p.keyword}</div>
            </div>
            <div style={{fontSize: 44, transform: `scale(${lerp(enter(frame, fps, p.sendAt + 10), 0.2, 1)})`}}>❤️</div>
          </div>
        ) : null}
        <div style={{...card, display: 'flex', alignItems: 'center', gap: 16, padding: '14px 18px 14px 24px'}}>
          <div style={{flex: 1, fontSize: 46, fontWeight: 800, color: n ? '#111' : '#999', minHeight: 64, display: 'flex', alignItems: 'center'}}>
            {frame < p.sendAt ? (n ? typed : 'أضف تعليق...') : 'أضف تعليق...'}
            {caret ? <span style={{width: 4, height: 50, background: acc, marginRight: 6}} /> : null}
          </div>
          <div style={{background: acc, color: C.outline, borderRadius: 999, padding: '6px 30px', fontSize: 38, fontWeight: 900,
            transform: `scale(${press ? 0.86 : 1})`, boxShadow: press ? `0 0 0 10px ${acc}55` : 'none'}}>
            نشر
          </div>
        </div>
        {dmP > 0.01 ? (
          <div style={{...card, background: C.panel, color: C.ink, display: 'flex', gap: 16, alignItems: 'center', padding: '16px 22px',
            opacity: dmP, transform: `translateY(${lerp(dmP, -40, 0)}px) scale(${lerp(dmP, 0.9, 1)})`, borderRight: `8px solid ${acc}`}}>
            <img src={staticFile(p.avatar)} style={{width: 70, height: 70, borderRadius: 35, objectFit: 'cover'}} />
            <div>
              <div style={{fontSize: 28, color: C.inkSoft, fontWeight: 700, fontFamily: 'Montserrat', direction: 'ltr', textAlign: 'right'}}>{p.name} · DM</div>
              <div style={{fontSize: 42, fontWeight: 800}}>{p.dm}</div>
            </div>
          </div>
        ) : null}

      </div>
        {p.qr && enter(frame, fps, p.qrAt) > 0.01 ? (() => {
          const q = enter(frame, fps, p.qrAt);
          return (
            <div style={{...card, position: 'absolute', left: (width - (vertical ? 700 : 520)) / 2, width: vertical ? 700 : 520, top: top + 20, boxSizing: 'border-box', display: 'flex', alignItems: 'center', gap: 22, padding: '16px 26px 16px 16px',
              opacity: q, transform: `translateY(${lerp(q, 50, 0)}px) scale(${lerp(q, 0.8, 1)})`, border: `6px solid ${acc}`}}>
              <Img src={staticFile(p.qr)} style={{width: vertical ? 230 : 180, height: vertical ? 230 : 180, display: 'block'}} />
              <div style={{fontSize: vertical ? 40 : 32, fontWeight: 900, maxWidth: vertical ? 360 : 260, lineHeight: 1.25}}>{p.qrLabel}</div>
            </div>
          );
        })() : null}
    </Base>
  );
};
