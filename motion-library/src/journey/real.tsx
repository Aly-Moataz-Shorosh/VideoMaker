import React from 'react';
import {Easing, Img, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, JY, lin, Sec, spr} from './kit';

// REAL examples on top of the motion (Aly 2026-10-22 review: "موشن بس من غير صور مش نافع" — the viewer must SEE the real thing).
// Pictures: his own work first, then crops of his own video, then free Commons pictures (credits in the .txt).
const REAL = 'projects/2026-10-22 shorts Journey to the center of computer graphics/real/';
export type RealItem = {src: string; at: number; out?: number; x: number; y: number; w: number; h?: number; shape?: 'circle' | 'card';
  label?: string; pos?: string; zoom?: number; pix?: [number, number, number, number]; rot?: number; fit?: 'cover' | 'contain'; bg?: string};

// pix = [x, y, w, h] in % of the picture: that small part shown big with hard pixels (the REAL pixels of a real photo)
const Pic: React.FC<{it: RealItem; f: number}> = ({it, f}) => {
  const z = (it.zoom ?? 1.06) + 0.04 * lin(f, it.at, it.at + 150);
  if (it.pix) {
    const [px, py, pw, ph] = it.pix;
    // background-position p% puts p% of the picture on p% of the box -> start of the region = px / (100 - pw)
    return (
      <div style={{position: 'absolute', inset: 0, backgroundImage: `url("${staticFile(REAL + it.src)}")`, backgroundRepeat: 'no-repeat',
        backgroundSize: `${10000 / pw}% ${10000 / ph}%`, backgroundPosition: `${(px / (100 - pw)) * 100}% ${(py / (100 - ph)) * 100}%`, imageRendering: 'pixelated'}} />
    );
  }
  return <Img src={staticFile(REAL + it.src)} style={{width: '100%', height: '100%', objectFit: it.fit ?? 'cover', objectPosition: it.pos ?? '50% 50%',
    transform: `scale(${it.fit === 'contain' ? 1 : z})`, background: it.bg}} />;
};

export const JyReal: React.FC<{items: RealItem[]; sec?: Sec}> = ({items, sec = 'huwa'}) => {
  const f = useCurrentFrame();
  const {fps, durationInFrames: d} = useVideoConfig();
  const ring = sec === 'oz' ? '#F2C230' : sec === 'prog' ? '#F7C531' : JY.huwa.a;
  return (
    <>
      {items.map((it, i) => {
        if (f < it.at) return null;
        const out = it.out ?? d;
        const o = 1 - lin(f, out - 7, out, 0, 1, Easing.in(Easing.cubic));
        if (o <= 0) return null;
        const p = spr(f, fps, it.at, 170, 13);
        const circle = (it.shape ?? 'circle') === 'circle';
        const w = it.w, h = circle ? it.w : it.h ?? it.w * 0.6;
        return (
          <div key={i} style={{position: 'absolute', left: it.x - w / 2, top: it.y - h / 2, width: w, height: h, opacity: Math.min(1, p * 1.5) * o,
            transform: `scale(${(0.4 + 0.6 * p) * (0.8 + 0.2 * o)}) rotate(${(it.rot ?? 0) * p}deg)`}}>
            <div style={{position: 'absolute', inset: 0, borderRadius: circle ? '50%' : 22, overflow: 'hidden', border: `${circle ? 9 : 8}px solid #fff`,
              boxShadow: `0 0 0 5px ${ring}, 0 22px 44px rgba(0,0,0,0.35)`, background: '#fff'}}>
              <Pic it={it} f={f} />
            </div>
            {it.src.startsWith('his_') ? (
              // his own work -> his Behance (Aly 2026-10-22: "لو هتستخدم حاجة من شغلي حط لينك بيهانس بتاعتي")
              <div style={{position: 'absolute', left: '50%', top: h + (it.label ? 44 : -8), transform: 'translateX(-50%)', whiteSpace: 'nowrap', fontFamily: 'Montserrat',
                fontWeight: 800, fontSize: 24, color: '#fff', background: '#1769FF', padding: '3px 14px', borderRadius: 16, direction: 'ltr'}}>Bē be.net/shorosh</div>
            ) : null}
            {it.label ? (
              <div style={{position: 'absolute', left: '50%', top: h - 8, transform: 'translateX(-50%)', whiteSpace: 'nowrap', fontFamily: AR, fontWeight: 900, fontSize: 30,
                color: '#fff', background: '#1E1E24', padding: '4px 16px', borderRadius: 20, direction: 'rtl'}}>{it.label}</div>
            ) : null}
          </div>
        );
      })}
    </>
  );
};

// Aly himself in a circle telling the story (Oz chapters): his matted face from the published chapter (same timeline as the voice),
// on a calm disc. src = transparent webm of the crop around his head; box = which part of the crop fills the circle.
export const FaceCircle: React.FC<{file: string; keys?: {t: number; x: number; y: number; d: number}[]; box?: [number, number, number]; ring?: string}> = ({file, keys = [{t: 0, x: 900, y: 1390, d: 220}], box = [360, 330, 420], ring = '#F2C230'}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 150, 15);
  // where it is now: last key passed, gliding 12 frames from the previous one
  let k = 0;
  keys.forEach((q, i) => { if (f >= q.t * fps) k = i; });
  const cur = keys[k], prev = keys[Math.max(0, k - 1)];
  const u = k === 0 ? 1 : lin(f, cur.t * fps, cur.t * fps + 12, 0, 1, Easing.inOut(Easing.cubic));
  const x = prev.x + (cur.x - prev.x) * u, y = prev.y + (cur.y - prev.y) * u, d = prev.d + (cur.d - prev.d) * u;
  const s = d / box[2];
  return (
    <div style={{position: 'absolute', left: x - d / 2, top: y - d / 2, width: d, height: d, borderRadius: '50%', overflow: 'hidden', transform: `scale(${p})`,
      background: 'radial-gradient(circle at 50% 40%, #FFF6DF 0%, #F2D58A 100%)', border: '8px solid #fff', boxShadow: `0 0 0 6px ${ring}, 0 22px 44px rgba(0,0,0,0.3)`}}>
      <OffthreadVideo transparent muted src={staticFile(file)} style={{position: 'absolute', width: 720 * s, height: 720 * s,
        left: d / 2 - box[0] * s, top: d / 2 - box[1] * s}} />
    </div>
  );
};
