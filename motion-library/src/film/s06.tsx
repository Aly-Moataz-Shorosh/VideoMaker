import React from 'react';
import {AbsoluteFill, Img, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, OLD, K, Clip, Halftone, Pop, Scene, Stamp, Strip, Tag, Title, img, lin, spr, useBeats} from './kit';
import {Hook} from './s02';

// Short 6 — what 16mm and 35mm mean (frame size on the strip), "raw" = خام, 35mm = more detail.
const PJ = 'projects/2026-10-08 shorts theodesy/';
type B = {b?: Record<string, number>};

// A ruler with mm ticks; len in px for `mm` millimetres.
export const Ruler: React.FC<{mm: number; px: number; p: number}> = ({mm, px, p}) => (
  <svg width={px + 40} height={110} style={{overflow: 'visible'}}>
    <rect x={0} y={0} width={(px + 40) * p} height={90} fill="#D9D3C4" stroke="#141210" strokeWidth={4} rx={6} />
    {Array.from({length: mm + 1}, (_, i) => (i / mm) <= p ? (
      <line key={i} x1={20 + (i / mm) * px} y1={0} x2={20 + (i / mm) * px} y2={i % 5 === 0 ? 46 : 26} stroke="#141210" strokeWidth={i % 5 === 0 ? 4 : 2} />
    ) : null)}
    {Array.from({length: Math.floor(mm / 5) + 1}, (_, i) => (i * 5 / mm) <= p ? (
      <text key={'t' + i} x={20 + (i * 5 / mm) * px} y={78} fontSize={26} fontFamily={EN} fontWeight={800} textAnchor="middle" fill="#141210">{i * 5}</text>
    ) : null)}
  </svg>
);

export const S6Hook: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  return (
    <Hook b={b} n={6} title="يعني إيه *16* و *35* مللي؟" side={
      <div style={{position: 'absolute', left: 30, top: 700, transform: `rotate(-10deg) translateY(${lin(f, 12, 40, 300, 0)}px)`, opacity: lin(f, 12, 24)}}>
        <Strip vertical frames={[PJ + 'img/poster.jpg', PJ + 'img/samir.jpg', PJ + 'img/imax_set.jpg']} fw={190} fh={140} />
      </div>
    } />
  );
};

// A 16mm strip measured by a ruler; one frame (الكادر) highlighted.
export const S6Gauge: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tM = at('mm', 3.3), tFrame = at('frame', 7.4);
  const W = 360; // 16 mm -> 360 px  (22.5 px / mm)
  const hi = lin(f, tFrame, tFrame + 12);
  return (
    <Scene bg="#16130F">
      <Halftone color="#fff" size={18} dot={0.1} opacity={0.05} />
      <div style={{position: 'absolute', left: 540 - W / 2 - 60, top: 300, transform: `translateY(${-((f * 1.5) % 300)}px)`}}>
        <Strip vertical frames={Array(7).fill(PJ + 'img/samir.jpg')} fw={W * 0.62} fh={W * 0.45} gap={14} />
      </div>
      {hi > 0 ? (
        <div style={{position: 'absolute', left: 540 - 150, top: 820, width: 360, height: 250, border: `8px solid ${K.yellow}`, borderRadius: 6, opacity: hi,
          boxShadow: `0 0 0 2000px rgba(0,0,0,${0.55 * hi})`, transform: `scale(${1 + 0.06 * hi})`}} />
      ) : null}
      <div style={{position: 'absolute', left: 540 - W / 2 - 80, top: 1240}}><Ruler mm={16} px={W} p={lin(f, tM - 10, tM + 14)} /></div>
      <Pop at={tM} x={540} y={1420}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 150, color: K.yellow, textShadow: '0 10px 0 #000'}}>16mm</div></Pop>
      <Pop at={tFrame + 6} x={820} y={760} rot={5}><Tag text="ده الكادر" bg={K.yellow} size={58} /></Pop>
      <Pop at={6} x={300} y={220} rot={-3}><Tag text="أفلام كتير اتصورت على" size={52} /></Pop>
    </Scene>
  );
};

// Behind Aly: film = "فيلم سينما" = "خام".
export const S6Names: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tRaw = at('raw', 3.9);
  return (
    <AbsoluteFill>
      <Pop at={at('cinema', 2.3)} out={tRaw - 4} x={540} y={330} rot={-3}><Tag text="فيلم سينما" size={84} /></Pop>
      {f >= tRaw ? (
        <Pop at={tRaw} x={540} y={330} from={0.2}>
          <div style={{fontFamily: OLD, fontSize: 260, color: K.yellow, lineHeight: 1, textShadow: '0 10px 0 #000'}}>خام</div>
        </Pop>
      ) : null}
    </AbsoluteFill>
  );
};

// Real 16mm camera running.
export const S6Shoot: React.FC<B> = ({b}) => {
  const at = useBeats(b);
  return (
    <Scene bg={K.ink}>
      <Pop at={0} x={540} y={800} rot={-2} from={0.85}><Clip src={PJ + 'broll/b8_16mm.mp4'} start={2} w={860} h={1240} seed={61} /></Pop>
      <Pop at={at('many', 6.3)} x={540} y={240} rot={3}><Tag text="أفلام كتير اتصورت بيه" bg={K.yellow} size={56} /></Pop>
      <Pop at={8} x={230} y={1350} rot={-6}><Tag text="16mm" font={EN} dir="ltr" size={70} /></Pop>
    </Scene>
  );
};

// 16 vs 35 side by side, true scale; same picture, more detail in 35.
export const S6Bigger: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const at = useBeats(b);
  const t35 = at('m35', 6.5), tDet = at('detail', 12);
  const g = spr(f, fps, t35 - 6, 120, 14);
  const W16 = 300, W35 = W16 * 35 / 16 * g + W16 * (1 - g);
  return (
    <Scene bg="#16130F">
      <div style={{position: 'absolute', left: 60, top: 420}}>
        <Strip vertical frames={Array(3).fill(PJ + 'img/poster_px.png')} fw={W16 * 0.62} fh={W16 * 0.46} />
        <div style={{textAlign: 'center', fontFamily: EN, fontWeight: 900, fontSize: 70, color: K.paper, marginTop: 20}}>16mm</div>
      </div>
      {f >= t35 - 6 ? (
        <div style={{position: 'absolute', left: 380, top: 420}}>
          <Strip vertical frames={Array(3).fill(PJ + 'img/poster_wide.jpg')} fw={W35 * 0.62} fh={W35 * 0.46} />
          <div style={{textAlign: 'center', fontFamily: EN, fontWeight: 900, fontSize: 90, color: K.yellow, marginTop: 20}}>35mm</div>
        </div>
      ) : null}
      <Pop at={6} x={540} y={250}><Tag text="نسخة أكبر شوية" size={60} /></Pop>
      {f >= tDet ? (
        <div style={{position: 'absolute', left: 120, right: 120, top: 1480}}>
          <div style={{fontFamily: AR, fontWeight: 900, fontSize: 50, color: K.white, marginBottom: 10}}>التفاصيل / النقاوة</div>
          <div style={{height: 36, background: '#333', borderRadius: 18, overflow: 'hidden'}}>
            <div style={{height: '100%', width: `${30 + 65 * lin(f, tDet, tDet + 30)}%`, background: K.yellow}} />
          </div>
        </div>
      ) : null}
    </Scene>
  );
};

// Behind Aly at the end: "35mm = cleaner".
export const S6Clean: React.FC<B> = () => (
  <AbsoluteFill>
    <Pop at={4} x={540} y={300} rot={-3}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 200, color: K.yellow, textShadow: '0 10px 0 #000'}}>35mm</div></Pop>
    <Pop at={14} x={540} y={470} rot={2}><Tag text="جودة أعلى… ونقاوة أحسن" size={56} /></Pop>
  </AbsoluteFill>
);
