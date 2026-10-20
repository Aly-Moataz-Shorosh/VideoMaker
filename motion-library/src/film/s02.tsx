import React from 'react';
import {AbsoluteFill, Easing, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, OLD, K, Halftone, Photo, Pop, Scene, Scribble, Stamp, Tag, Title, arrowPath, lin, spr, useBeats, rnd} from './kit';
import {Brain, Eye, Obscura, Palm, Pyramid, Sun} from './draw';
import {SeriesTag} from './s01';

// Short 2 — Ibn al-Haytham: how we really see + the camera obscura (القُمرة).
const PJ = 'projects/2026-10-08 shorts theodesy/';
type B = {b?: Record<string, number>};

export const Hook: React.FC<B & {n: number; title: string; side?: React.ReactNode}> = ({n, title, side}) => (
  <AbsoluteFill>
    <SeriesTag n={n} />
    <div style={{position: 'absolute', top: 230, left: 60, right: 60, display: 'flex', justifyContent: 'center'}}>
      <Title text={title} size={86} at={2} stagger={2} stroke />
    </div>
    {side}
  </AbsoluteFill>
);

export const S2Hook: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  return (
    <Hook b={b} n={2} title="آلاف السنين والناس فاكرة إن *عينك* بتطلع نور!" side={
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <g opacity={lin(f, 20, 34)}><Eye x={250} y={640} s={0.6} look={0.6} glow={0.5 + 0.5 * Math.sin(f / 5)} /></g>
      </svg>
    } />
  );
};

// Old theory: rays come OUT of the eye -> red cross.
export const S2Emission: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const ray = lin(f, at('rays', 0.4), at('rays', 0.4) + 16);
  return (
    <Scene bg={K.paper2}>
      <Halftone color="#000" size={14} dot={0.18} opacity={0.1} />
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <Eye x={300} y={800} s={1.1} look={0.7} glow={ray} />
        {[-0.25, 0, 0.25].map((a, i) => (
          <line key={i} x1={420} y1={800} x2={420 + 560 * ray * Math.cos(a)} y2={800 + 560 * ray * Math.sin(a)} stroke={K.yellow} strokeWidth={14} strokeDasharray="30 18"
            strokeDashoffset={f * 4} strokeLinecap="round" />
        ))}
        <g transform="translate(900,800)"><circle r={60} fill="#C24B6A" stroke="#141210" strokeWidth={6} /><path d="M0,60 L0,220" stroke="#2F5D3A" strokeWidth={12} /></g>
      </svg>
      <Pop at={4} x={540} y={420} rot={-3}><Tag text="النظرية القديمة" size={64} /></Pop>
      <Pop at={at('no', 1.4)} x={600} y={800}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 520, color: K.red, lineHeight: 1, textShadow: '0 10px 0 #000'}}>✕</div></Pop>
    </Scene>
  );
};

// Ibn al-Haytham portrait + "لا يا باشا".
export const S2Haytham: React.FC<B> = ({b}) => {
  const at = useBeats(b);
  return (
    <Scene bg={K.ink}>
      <Pop at={0} x={540} y={760} rot={-2} from={0.7}>
        <Photo src={PJ + 'img/haytham.jpg'} w={680} h={850} bw={true} seed={14} tone="#C9A66B" />
      </Pop>
      <Pop at={6} x={540} y={230}>
        <div style={{fontFamily: OLD, fontSize: 104, color: K.yellow, textShadow: '0 6px 0 #000', direction: 'rtl', whiteSpace: 'nowrap'}}>الحسن ابن الهيثم</div>
      </Pop>
      <Pop at={10} x={540} y={1240}><Tag text="965 – 1040 م" font={EN} dir="ltr" size={52} /></Pop>
      <Pop at={at('no', 1.3)} x={800} y={520} rot={8}>
        <div style={{background: K.white, border: `6px solid ${K.ink}`, borderRadius: 34, padding: '14px 36px', fontFamily: AR, fontWeight: 900, fontSize: 84,
          color: K.ink, boxShadow: '10px 12px 0 rgba(0,0,0,0.85)', whiteSpace: 'nowrap'}}>لا يا باشا!</div>
      </Pop>
    </Scene>
  );
};

// How we really see: sun -> rays hit the pyramid -> bounce into the eye -> brain makes the picture.
export const S2Light: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const at = useBeats(b);
  const tHit = at('hit', 0.6), tBounce = at('bounce', 4.4), tBrain = at('brain', 7.6), tPic = at('pic', 10.6);
  const r1 = lin(f, tHit, tHit + 20), r2 = lin(f, tBounce, tBounce + 18), r3 = lin(f, tBrain, tBrain + 16);
  const P = [520, 820], E = [800, 1150], S = [200, 300];
  const seg = (a: number[], b2: number[], k: number) => `M${a[0]},${a[1]} L${a[0] + (b2[0] - a[0]) * k},${a[1] + (b2[1] - a[1]) * k}`;
  const pic = spr(f, fps, tPic, 140, 12);
  return (
    <Scene bg="#16130F">
      <Halftone color="#fff" size={16} dot={0.1} opacity={0.05} />
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <Sun x={S[0]} y={S[1]} r={70} spin={f * 0.6} />
        <Pyramid x={P[0]} y={P[1] + 170} s={1.7} lit={r1} />
        {[0, 1, 2].map((i) => (
          <path key={i} d={seg([S[0] + 60, S[1] + 40 + i * 30], [P[0] - 40 + i * 50, P[1] - 30 + i * 40], r1)} stroke={K.yellow} strokeWidth={9} strokeDasharray="22 14"
            strokeDashoffset={-f * 3} fill="none" strokeLinecap="round" />
        ))}
        {[0, 1].map((i) => (
          <path key={'b' + i} d={seg([P[0] + 20 + i * 40, P[1] + 20 + i * 30], [E[0] - 120, E[1] - 10 + i * 20], r2)} stroke={K.yellow} strokeWidth={9} strokeDasharray="22 14"
            strokeDashoffset={-f * 3} fill="none" strokeLinecap="round" />
        ))}
        <Eye x={E[0]} y={E[1]} s={0.95} look={-0.8} glow={r2 * 0.8} />
        <path d={seg([E[0] - 40, E[1] + 70], [420, 1330], r3)} stroke={K.red} strokeWidth={8} fill="none" strokeDasharray="4 10" strokeDashoffset={-f * 3} />
        <Brain x={300} y={1330} s={1.0} lit={r3} />
      </svg>
      <Pop at={tHit + 6} x={760} y={640} rot={4}><Tag text="النور بيخبط في الحاجة" size={52} /></Pop>
      <Pop at={tBounce + 4} x={820} y={980} rot={-5}><Tag text="ويرتد لعينك" bg={K.yellow} size={56} /></Pop>
      <Pop at={tBrain + 6} x={720} y={1420} rot={3}><Tag text="والمخ يترجمه لصورة" bg={K.red} color={K.white} size={50} /></Pop>
      {f >= tPic ? (
        <div style={{position: 'absolute', left: 100, top: 990, width: 330, height: 230, transform: `scale(${pic})`, transformOrigin: '50% 100%'}}>
          <div style={{position: 'absolute', inset: 0, background: K.white, borderRadius: 120, border: `6px solid ${K.ink}`, overflow: 'hidden'}}>
            <svg width={330} height={230} viewBox="0 400 640 520"><Pyramid x={330} y={860} s={1.2} /><Sun x={120} y={500} r={40} /></svg>
          </div>
        </div>
      ) : null}
    </Scene>
  );
};

// Behind Aly: "he invented the qumra".
export const S2Name: React.FC<B> = ({b}) => {
  const at = useBeats(b);
  return (
    <AbsoluteFill>
      <Pop at={at('name', 1.5)} x={540} y={300} rot={-3}>
        <div style={{fontFamily: OLD, fontSize: 200, color: K.yellow, lineHeight: 1, textShadow: '0 8px 0 #000'}}>القُمرة</div>
      </Pop>
      <Pop at={at('name', 1.5) + 10} x={540} y={470}><Tag text="Camera Obscura" font={EN} dir="ltr" size={46} /></Pop>
    </AbsoluteFill>
  );
};

// The camera obscura: small box -> closed room -> pinhole -> light draws the outside scene upside-down inside.
export const S2Obscura: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const box = 0.55 + 0.45 * lin(f, at('room', 3.6), at('room', 3.6) + 18) ;
  const appear = lin(f, at('box', 1), at('box', 1) + 12);
  const hole = lin(f, at('hole', 5.5), at('hole', 5.5) + 8);
  const rays = lin(f, at('light', 6.2), at('light', 6.2) + 40, 0, 1, (x) => x);
  const image = lin(f, at('draw', 8.3), at('draw', 8.3) + 30);
  return (
    <Scene bg="#14110E">
      <div style={{position: 'absolute', inset: 0, opacity: appear}}>
        <Obscura w={1080} h={1920} box={box * appear} hole={hole} rays={rays} image={image} />
      </div>
      <Pop at={at('box', 1) + 4} x={740} y={400} rot={3}><Tag text={f < at('room', 3.6) ? 'صندوق صغير' : 'أوضة مقفولة'} size={56} /></Pop>
      <Pop at={at('hole', 5.5) + 4} x={300} y={1180} rot={-4}><Tag text="خُرم صغير" bg={K.yellow} size={56} /></Pop>
      <Pop at={at('draw', 8.3) + 20} x={740} y={1380} rot={4}><Tag text="الصورة بتترسم مقلوبة!" bg={K.red} color={K.white} size={50} /></Pop>
      {image > 0.5 ? (
        <Scribble width={1080} height={1920} p={lin(f, at('draw', 8.3) + 24, at('draw', 8.3) + 40)} d={arrowPath(760, 1330, 900, 1050, -0.3)} w={9} color={K.red} />
      ) : null}
    </Scene>
  );
};

// First projection of an image in history.
export const S2First: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const glow = 0.75 + 0.25 * Math.sin(f / 6);
  return (
    <Scene bg="#0A0908">
      <div style={{position: 'absolute', left: 140, top: 520, width: 800, height: 560, background: '#2B2219', boxShadow: `0 0 140px rgba(255,194,26,${0.35 * glow})`, overflow: 'hidden',
        borderRadius: 6}}>
        <svg width={800} height={560} viewBox="0 330 640 620" style={{transform: 'scaleY(-1)'}}>
          <Palm x={150} y={900} s={1.1} /><Pyramid x={330} y={900} s={1} /><Sun x={520} y={480} r={40} />
        </svg>
        <Halftone color="#000" size={8} dot={0.25} opacity={0.3} />
      </div>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <g fill="#000"><circle cx={540} cy={1260} r={70} /><rect x={430} y={1310} width={220} height={260} rx={90} /></g>
      </svg>
      <div style={{position: 'absolute', top: 190, left: 60, right: 60, display: 'flex', justifyContent: 'center'}}>
        <Title text="أول مرة الإنسان يعمل *إسقاط* لصورة" size={84} at={4} />
      </div>
      <Pop at={at('proj', 4)} x={540} y={1150} rot={-3}><Tag text="Projection" font={EN} dir="ltr" bg={K.yellow} size={58} /></Pop>
      <div style={{position: 'absolute', left: 250, top: 1400}}><Stamp text="سنة 1000 م تقريبًا" at={at('year', 2)} size={64} rot={-6} color={K.yellow} /></div>
    </Scene>
  );
};

// Behind Aly at the end: the projected (upside-down) picture on a wall behind him.
export const S2Wall: React.FC<B> = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 90, top: 200, width: 900, height: 640, background: K.paper, transform: `rotate(-2deg) scale(${0.9 + 0.1 * lin(f, 0, 10)})`,
        boxShadow: '0 30px 60px rgba(0,0,0,0.6)', overflow: 'hidden'}}>
        <svg width={900} height={640} viewBox="0 330 640 620" style={{transform: 'scaleY(-1)', opacity: 0.85}}>
          <Palm x={150} y={900} s={1.1} /><Pyramid x={330} y={900} s={1} /><Sun x={520} y={480} r={40} />
        </svg>
        <Halftone color="#000" size={9} dot={0.2} opacity={0.18} />
      </div>
      <Pop at={14} x={720} y={170} rot={5}><Tag text="على حيطة… أو أي حاجة" size={50} /></Pop>
    </AbsoluteFill>
  );
};
