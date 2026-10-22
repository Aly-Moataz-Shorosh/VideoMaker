import React from 'react';
import {Easing, Img, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, grad, In, lin, Pill, Sc, Sec, spr} from './kit';

// HIS OWN motion (Aly review 2026-10-22: "الموشن جرافيك اللي انا عامله في الفيديو بتاعي احسن و بيعبر اكتر"):
// the part of his episode frame where his animation is (box in 1920x1080), playing in sync with his voice, shown big
// in the 9:16 stage (never more than ×1.6 so it does not get pixelated), inside his gradient frame.
const PJ = 'projects/2026-10-22 shorts Journey to the center of computer graphics/';
export const JyClip: React.FC<{src: string; from: number; box: [number, number, number, number]; sec?: Sec; cx?: number; cy?: number;
  maxW?: number; maxH?: number; maxS?: number; title?: string; full?: boolean}> = ({src, from, box, sec = 'huwa', cx = 540, cy = 830, maxW = 860, maxH = 860, maxS = 1.6, title, full}) => {
  const {fps} = useVideoConfig();
  const [x0, y0, x1, y1] = box;
  const bw = x1 - x0, bh = y1 - y0;
  const s = Math.min(maxW / bw, maxH / bh, maxS);
  const w = bw * s, h = bh * s;
  return (
    <Sc inF={6} outF={6}>
      {title ? <In at={0} x={540} y={340}><Pill text={title} bg={grad(sec)} ink="#fff" size={46} /></In> : null}
      <div style={{position: 'absolute', left: cx - w / 2 - 10, top: cy - h / 2 - 10, width: w + 20, height: h + 20, padding: 10, borderRadius: full ? 26 : 30,
        background: grad(sec), boxShadow: '0 24px 50px rgba(0,0,0,0.25)'}}>
        <div style={{position: 'relative', width: w, height: h, overflow: 'hidden', borderRadius: 20, background: '#C9C9CB'}}>
          <OffthreadVideo muted src={staticFile(PJ + src)} startFrom={Math.round(from * fps)}
            style={{position: 'absolute', width: 1920 * s, height: 1080 * s, left: -x0 * s, top: -y0 * s, maxWidth: 'none'}} />
        </div>
      </div>
    </Sc>
  );
};

// A REAL photo, then zoom in until its pixels show (Aly: "لما تجيب المربعات جيب الصورة و بعدين اعمل زوم").
// target = point in the picture (px), z = final zoom; nearest-neighbour so every square is one real pixel.
export const JyZoom: React.FC<{src: string; iw: number; ih: number; target: [number, number]; b?: Record<string, number>; z?: number; sec?: Sec}> = ({src, iw, ih, target, b = {}, z = 28, sec = 'huwa'}) => {
  const f = useCurrentFrame();
  const z0 = b.zoom ?? 30, bad = b.bad ?? 110;
  const W = 860, H = W * ih / iw;
  const u = lin(f, z0, bad, 0, 1, Easing.inOut(Easing.cubic));
  const k = Math.exp(Math.log(z) * u); // even feel of the zoom
  const tx = (target[0] / iw) * W, ty = (target[1] / ih) * H;
  const grid = lin(f, bad - 20, bad, 0, 1);
  return (
    <Sc>
      <In at={0} x={540} y={340}><Pill text={f < z0 ? 'صورة حقيقية 📷' : 'نكبّرها.. 🔍'} size={48} /></In>
      <div style={{position: 'absolute', left: 540 - W / 2 - 10, top: 830 - H / 2 - 10, padding: 10, borderRadius: 30, background: grad(sec), boxShadow: '0 24px 50px rgba(0,0,0,0.25)'}}>
        <div style={{position: 'relative', width: W, height: H, overflow: 'hidden', borderRadius: 20}}>
          <Img src={staticFile(PJ + 'real/' + src)} style={{position: 'absolute', width: W, height: H, imageRendering: 'pixelated',
            transformOrigin: `${tx}px ${ty}px`, transform: `scale(${k})`}} />
          {/* pixel grid when the squares are big */}
          <div style={{position: 'absolute', inset: 0, opacity: grid * 0.5, backgroundImage: `linear-gradient(rgba(255,255,255,.7) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.7) 1px, transparent 1px)`,
            backgroundSize: `${(W / iw) * k}px ${(W / iw) * k}px`, backgroundPosition: `${tx - tx * k}px ${ty - ty * k}px`}} />
        </div>
      </div>
      <In at={bad} x={540} y={1330}><Pill text="كل مربع = بيكسل.. والصورة بتبوظ" bg="#E53935" ink="#fff" size={44} /></In>
    </Sc>
  );
};

// Behance QR (Aly: "بدل الموقع بتاع بيهانس حط qr code صغير") — only next to his strongest works
export const BehanceQR: React.FC<{size?: number}> = ({size = 110}) => (
  <div style={{background: '#fff', padding: 6, borderRadius: 12, boxShadow: '0 8px 18px rgba(0,0,0,0.25)', textAlign: 'center'}}>
    <Img src={staticFile(PJ + 'qr_behance.png')} style={{width: size, height: size, display: 'block'}} />
    <div style={{fontFamily: 'Montserrat', fontWeight: 900, fontSize: size * 0.17, color: '#1769FF'}}>Bē Behance</div>
  </div>
);
export {spr, AR};
