import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base, Highlight} from '../blocks/Base';
import {C, theme, isVertical} from '../blocks/theme';
import {enter, lerp} from '../blocks/anim';

// Aly's standard reel end card (r3/r5/r7/r11): black; question + promise on top (white + red highlight);
// long-video thumbnail center; socials list; YouTube "watch the full video" + avatar; QR (from build_edit).
export const ctaEndcardSchema = z.object({
  question: z.string().default('عايز تعرف الفيديو ده اتعمل إزاي؟'),
  promise: z.string().default('شوف الفيديو ده فيه شرح مجاني *بكل حب وإخلاص شديد*'),
  thumb: z.string().default('test/thumb_genjutsu.jpg'),
  qr: z.string().default(''),
  qrUrl: z.string().default(''),
  socials: z.boolean().default(true),
});

const SOCIALS: [string, string, string][] = [
  ['youtube.com/', 'AlyShorosh', '#FF2D2D'],
  ['instagram ', '@alyshorosh', '#E1306C'],
  ['behance.net/', 'shorosh', '#1E6BFF'],
  ['linkedin.com/in/', 'shorosh', '#2D8CFF'],
  ['facebook.com/', 'aly.shorosh', '#3B6CFF'],
];

export const CtaEndcard: React.FC<z.infer<typeof ctaEndcardSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const v = isVertical(width, height);
  const a = enter(frame, fps), b = enter(frame, fps, 6), c = enter(frame, fps, 12), d = enter(frame, fps, 18);
  const thumbW = v ? width * 0.82 : width * 0.36;
  const red = '#FF2D2D';
  return (
    <Base>
      <AbsoluteFill style={{background: '#000', opacity: Math.min(1, a * 2)}} />
      <div style={{position: 'absolute', top: v ? height * 0.12 : height * 0.07, left: 40, right: 40, textAlign: 'center',
        opacity: a, transform: `translateY(${lerp(a, -30, 0)}px)`}}>
        <div style={{fontSize: v ? 64 : 52, fontWeight: 900}}>{p.question}</div>
        <div style={{fontSize: v ? 46 : 38, fontWeight: 800, marginTop: 6}}><Highlight text={p.promise} accent={red} /></div>
      </div>
      <Img src={staticFile(p.thumb)} style={{position: 'absolute', width: thumbW, left: (width - thumbW) / 2,
        top: v ? height * 0.3 : height * 0.3, borderRadius: 18, boxShadow: '0 20px 60px rgba(255,255,255,0.08)',
        opacity: b, transform: `scale(${lerp(b, 0.85, 1)})`}} />
      {p.socials ? (
        <div style={{position: 'absolute', left: v ? 60 : 50, bottom: v ? height * 0.2 : 60, direction: 'ltr', fontFamily: 'Montserrat',
          fontWeight: 700, fontSize: v ? 30 : 24, lineHeight: 1.45, opacity: d}}>
          {SOCIALS.map(([k, h, col]) => (
            <div key={h}><span style={{color: col}}>{k}</span><span style={{color: C.ink === '#FFFFFF' ? '#fff' : '#fff'}}>{h}</span></div>
          ))}
        </div>
      ) : null}
      <div style={{position: 'absolute', left: 0, right: 0, bottom: v ? height * 0.06 : 50, display: 'flex', flexDirection: 'column',
        alignItems: 'center', gap: 10, opacity: c, transform: `translateY(${lerp(c, 30, 0)}px)`}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 14, fontSize: v ? 44 : 34, fontWeight: 900}}>
          <Img src={staticFile('logos/youtube-icon.svg')} style={{height: v ? 44 : 34}} />
          <span>شاهد الفيديو كاملاً على <span style={{color: red}}>YouTube</span></span>
        </div>
        <div style={{fontFamily: 'Montserrat', fontSize: v ? 26 : 20, color: '#ccc', direction: 'ltr'}}>Watch the full video on YouTube</div>
        <div style={{display: 'flex', alignItems: 'center', gap: 12, background: '#1a1a1a', borderRadius: 999, padding: '6px 22px 6px 8px', direction: 'ltr'}}>
          <Img src={staticFile('brand/avatar-old.png')} style={{width: v ? 64 : 52, height: v ? 64 : 52, borderRadius: '50%', background: '#e9b67d'}} />
          <span style={{fontFamily: 'Montserrat', fontWeight: 800, fontSize: v ? 32 : 26, color: C.gold === '#F5B83D' ? '#F5B83D' : C.gold}}>Aly Shorosh</span>
        </div>
      </div>
      {p.qr ? (
        <div style={{position: 'absolute', right: v ? 60 : 50, bottom: v ? height * 0.2 : 60, background: '#fff', padding: 10, borderRadius: 12,
          opacity: d, transform: `scale(${lerp(d, 0.6, 1)})`, boxShadow: theme.shadow}}>
          <Img src={staticFile(p.qr)} style={{width: v ? 200 : 170, height: v ? 200 : 170, display: 'block'}} />
        </div>
      ) : null}
    </Base>
  );
};
