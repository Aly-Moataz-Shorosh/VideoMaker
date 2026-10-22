import React from 'react';
import {Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, grad, JY, lin, Sec, spr} from './kit';

// End card of every short in the series (Aly 2026-10-22): the PLAYLIST thumbnail + its name + its QR on top,
// under it the thumbnail of the original video (NO QR on it). No CTA clip.
export const JourneyEnd: React.FC<{sec: Sec; plThumb: string; plName: string; qr: string; vidThumb: string; vidTitle: string}> = ({sec, plThumb, plName, qr, vidThumb, vidTitle}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const dark = sec === 'prog';
  const ink = dark ? '#fff' : JY[sec].ink;
  const a = spr(f, fps, 0, 150, 15), b = spr(f, fps, 8, 150, 15), c = spr(f, fps, 18, 150, 15);
  const veil = lin(f, 0, 10);
  return (
    <div style={{position: 'absolute', inset: 0, direction: 'rtl'}}>
      <div style={{position: 'absolute', inset: 0, background: dark ? 'rgba(14,38,39,0.9)' : sec === 'oz' ? 'rgba(255,240,205,0.92)' : 'rgba(225,225,228,0.92)', opacity: veil}} />
      <div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 58, color: ink, opacity: a,
        transform: `translateY(${(1 - a) * 30}px)`}}>شوف السلسلة كاملة 👇</div>
      <div style={{position: 'absolute', left: 140, top: 400, width: 800, transform: `scale(${0.85 + 0.15 * a})`, opacity: a}}>
        <div style={{padding: 10, borderRadius: 28, background: grad(sec), boxShadow: '0 30px 60px rgba(0,0,0,0.35)'}}>
          <Img src={staticFile(plThumb)} style={{width: '100%', aspectRatio: '16 / 9', objectFit: 'cover', borderRadius: 20, display: 'block'}} />
        </div>
        <div style={{position: 'absolute', left: 20, bottom: 20, background: 'rgba(0,0,0,0.75)', color: '#fff', fontFamily: AR, fontWeight: 800, fontSize: 30,
          padding: '6px 18px', borderRadius: 12}}>▶ بلايليست</div>
      </div>
      <div style={{position: 'absolute', left: 140, top: 880, width: 800, display: 'flex', alignItems: 'center', gap: 34, opacity: b, transform: `translateY(${(1 - b) * 40}px)`}}>
        <div style={{flex: 1, fontFamily: AR, fontWeight: 900, fontSize: 52, lineHeight: 1.25, color: ink}}>
          {plName}
          <div style={{fontFamily: EN, fontWeight: 700, fontSize: 22, letterSpacing: 1.5, opacity: 0.65, marginTop: 8, direction: 'ltr', textAlign: 'right'}}>JOURNEY TO THE CENTER OF COMPUTER GRAPHICS</div>
        </div>
        <div style={{width: 250, height: 250, background: '#fff', borderRadius: 22, padding: 14, boxShadow: '0 16px 36px rgba(0,0,0,0.3)'}}>
          <Img src={staticFile(qr)} style={{width: '100%', height: '100%'}} />
        </div>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 1210, textAlign: 'center', opacity: c}}>
        <div style={{fontFamily: AR, fontWeight: 800, fontSize: 36, color: ink, opacity: 0.8, marginBottom: 16}}>الحلقة الأصلية</div>
        <div style={{display: 'inline-block', width: 560, transform: `scale(${0.85 + 0.15 * c})`}}>
          <Img src={staticFile(vidThumb)} style={{width: '100%', aspectRatio: '16 / 9', objectFit: 'cover', borderRadius: 18, display: 'block', boxShadow: '0 20px 40px rgba(0,0,0,0.3)'}} />
          <div style={{marginTop: 14, fontFamily: AR, fontWeight: 800, fontSize: 32, color: ink}}>{vidTitle}</div>
        </div>
      </div>
    </div>
  );
};
