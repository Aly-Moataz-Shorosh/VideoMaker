import React from 'react';
import {AbsoluteFill, Img, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, K, Halftone, Photo, Pop, Scene, Stamp, Strip, Tag, Title, img, lin, rnd, shake, spr, useBeats} from './kit';
import {Hook} from './s02';

// Short 8 — IMAX 70: the frame turned sideways (biggest film ever), the loud camera, the sound-proof box, the mirror.
const PJ = 'projects/2026-10-08 shorts theodesy/';
type B = {b?: Record<string, number>};

export const S8Hook: React.FC<B> = ({b}) => (
  <Hook b={b} n={8} title="يعني إيه *IMAX 70*؟ وليه نولان عمل المستحيل؟" side={
    <Pop at={16} x={200} y={980} rot={-8}><Photo src={PJ + 'img/nolan_set.webp'} w={300} h={300} bw seed={81} pos="30% 30%" /></Pop>
  } />
);

// Drawn IMAX-ish camera body (big, heavy) with two magazines on top; shaking = noise.
const BigCam: React.FC<{x: number; y: number; s?: number; noise?: number}> = ({x, y, s = 1, noise = 0}) => {
  const f = useCurrentFrame();
  const j = noise * (rnd(f) - 0.5) * 10;
  return (
    <g transform={`translate(${x + j},${y + j * 0.6}) scale(${s})`}>
      <ellipse cx={-90} cy={-150} rx={100} ry={80} fill="#2C2C2E" stroke="#111" strokeWidth={6} />
      <ellipse cx={90} cy={-150} rx={100} ry={80} fill="#2C2C2E" stroke="#111" strokeWidth={6} />
      <rect x={-200} y={-90} width={400} height={230} rx={22} fill="#3A3D42" stroke="#111" strokeWidth={7} />
      <rect x={-170} y={-60} width={150} height={60} rx={8} fill="#1F2124" />
      <text x={-95} y={-18} fontSize={44} fontWeight={900} fontFamily={EN} fill={K.cyan} textAnchor="middle">IMAX</text>
      <rect x={200} y={-50} width={110} height={150} rx={10} fill="#222" stroke="#111" strokeWidth={6} />
      <circle cx={340} cy={25} r={70} fill="#1B1B1D" stroke="#111" strokeWidth={8} />
      <circle cx={340} cy={25} r={40} fill="#3B5168" />
      <circle cx={325} cy={10} r={12} fill="#9FC3E0" />
    </g>
  );
};

// 35 -> 70 -> turned sideways = IMAX 70 (much more area).
export const S8Gauges: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const at = useBeats(b);
  const t70 = at('m70', 0.6), tSide = at('side', 10.2), tArea = at('area', 12.9), tName = at('name', 14.6);
  const rot = spr(f, fps, tSide, 70, 16);
  const W70 = 300;
  return (
    <Scene bg="#121315">
      <Halftone color="#fff" size={18} dot={0.1} opacity={0.05} />
      <div style={{position: 'absolute', left: 120, top: 420, opacity: 1 - lin(f, tSide - 10, tSide)}}>
        <Strip vertical frames={Array(3).fill(PJ + 'img/poster_wide.jpg')} fw={150} fh={110} />
        <div style={{textAlign: 'center', fontFamily: EN, fontWeight: 900, fontSize: 60, color: K.paper}}>35mm</div>
      </div>
      {f >= t70 ? (
        <div style={{position: 'absolute', left: 540 - W70 / 2 - 40, top: 500, transform: `rotate(${-90 * rot}deg) scale(${1 + 0.5 * rot})`, transformOrigin: '50% 40%'}}>
          <Strip vertical frames={Array(3).fill(PJ + 'img/poster_wide.jpg')} fw={W70} fh={W70 * (0.45 + 0.55 * rot)} />
        </div>
      ) : null}
      {f >= tArea ? (
        <div style={{position: 'absolute', left: 540 - 50, top: 760, width: 100, height: 72, border: `6px dashed ${K.red}`, opacity: lin(f, tArea, tArea + 8)}} />
      ) : null}
      <Pop at={t70 + 4} out={tSide} x={780} y={300} rot={4}><Tag text="70mm" font={EN} dir="ltr" bg={K.yellow} size={70} /></Pop>
      <Pop at={tSide} x={540} y={260} rot={-3}><Tag text="خلّي الصورة بالعرض!" size={60} /></Pop>
      <Pop at={tArea + 4} x={300} y={1010} rot={-4}><Tag text="مساحة أكبر بكتير" bg={K.red} color={K.white} size={52} /></Pop>
      <Pop at={tName} x={540} y={1200}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 130, color: K.yellow, textShadow: '0 10px 0 #000'}}>IMAX 70mm</div></Pop>
    </Scene>
  );
};

// Bar race of frame area: 16 / 35 / 70 / IMAX (crown) -> "expensive".
export const S8Biggest: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tCost = at('cost', 11);
  const bars = [{l: '16mm', v: 0.12}, {l: '35mm', v: 0.28}, {l: '70mm', v: 0.52}, {l: 'IMAX', v: 1}];
  return (
    <Scene bg={K.ink}>
      <div style={{position: 'absolute', top: 180, left: 60, right: 60, display: 'flex', justifyContent: 'center'}}>
        <Title text="*أكبر* خام في الدنيا" size={100} at={3} />
      </div>
      <div style={{position: 'absolute', left: 110, right: 110, top: 480, height: 820, display: 'flex', alignItems: 'flex-end', gap: 40}}>
        {bars.map((x, i) => {
          const k = lin(f, 8 + i * 8, 28 + i * 8);
          return (
            <div key={i} style={{flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-end', height: '100%'}}>
              {i === 3 && k > 0.9 ? <div style={{fontSize: 110, marginBottom: 10}}>👑</div> : null}
              <div style={{width: '100%', height: `${x.v * 640 * k}px`, background: i === 3 ? K.yellow : K.paper2, borderRadius: '10px 10px 0 0', border: `5px solid ${K.ink}`}} />
              <div style={{fontFamily: EN, fontWeight: 900, fontSize: 46, color: i === 3 ? K.yellow : K.paper, marginTop: 12}}>{x.l}</div>
            </div>
          );
        })}
      </div>
      <div style={{position: 'absolute', left: 620, top: 1380}}><Stamp text="غالي!" at={tCost} size={110} rot={-10} /></div>
    </Scene>
  );
};

// Storyboard: long dialogue scenes = normal film, big action shots = IMAX.
export const S8Scenes: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tDlg = at('dialog', 6), tBig = at('big', 8.3);
  const cards = [{k: 'big', icon: '💥'}, {k: 'dlg', icon: '💬'}, {k: 'dlg', icon: '💬'}, {k: 'big', icon: '🏔️'}, {k: 'dlg', icon: '💬'}, {k: 'big', icon: '⛵'}];
  return (
    <Scene bg="#16130F">
      <div style={{position: 'absolute', top: 190, left: 60, right: 60, display: 'flex', justifyContent: 'center'}}>
        <Title text="IMAX لمشاهد *معينة* بس" size={90} at={2} />
      </div>
      <div style={{position: 'absolute', left: 70, right: 70, top: 470, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 34}}>
        {cards.map((c, i) => {
          const k = spr(f, 30, 6 + i * 5, 170, 13);
          const big = c.k === 'big';
          const mark = big ? f >= tBig : f >= tDlg;
          return (
            <div key={i} style={{height: 250, background: K.paper, borderRadius: 10, position: 'relative', transform: `scale(${k}) rotate(${(rnd(i) - 0.5) * 6}deg)`,
              border: `6px solid ${mark ? (big ? K.yellow : '#666') : K.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 120,
              opacity: mark && !big ? 0.55 : 1}}>
              {c.icon}
              {mark ? <div style={{position: 'absolute', top: 14, right: 14}}><Tag text={big ? 'IMAX' : '35mm'} font={EN} dir="ltr" bg={big ? K.yellow : '#9A968E'} size={40} /></div> : null}
            </div>
          );
        })}
      </div>
      <Pop at={tDlg + 4} x={540} y={1440} rot={-2}><Tag text="الحوار الطويل؟ مش بالـ IMAX" size={52} /></Pop>
    </Scene>
  );
};

// The camera is LOUD (film running inside) -> actors can't act; decibel meter in the red.
export const S8Noise: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tLoud = at('loud', 4.1);
  const noise = lin(f, tLoud - 10, tLoud + 6);
  const sh = noise * (rnd(f * 2) - 0.5) * 12;
  return (
    <Scene bg="#121315">
      <svg width={1080} height={1920} style={{position: 'absolute', transform: `translate(${sh}px,${sh * 0.5}px)`}}>
        <BigCam x={420} y={700} s={1.25} noise={noise} />
        {noise > 0 ? Array.from({length: 4}, (_, i) => {
          const k = ((f + i * 8) % 32) / 32;
          return <circle key={i} cx={520} cy={680} r={200 + k * 380} fill="none" stroke={K.red} strokeWidth={10} opacity={(1 - k) * noise} />;
        }) : null}
        {/* actors covering ears */}
        {[180, 900].map((x, i) => (
          <g key={i} transform={`translate(${x},1330)`}>
            <circle cx={0} cy={-140} r={52} fill={K.paper2} />
            <rect x={-70} y={-90} width={140} height={190} rx={50} fill={K.paper2} />
            {noise > 0.5 ? <><rect x={-80} y={-170} width={30} height={60} rx={14} fill={K.paper} /><rect x={50} y={-170} width={30} height={60} rx={14} fill={K.paper} /></> : null}
          </g>
        ))}
      </svg>
      <div style={{position: 'absolute', left: 140, right: 140, top: 1520}}>
        <div style={{height: 40, borderRadius: 20, background: '#2a2a2a', overflow: 'hidden', border: `4px solid ${K.paper2}`}}>
          <div style={{height: '100%', width: `${15 + 83 * noise + (rnd(f) - 0.5) * 6 * noise}%`, background: `linear-gradient(to right, #7BD389, ${K.yellow}, ${K.red})`}} />
        </div>
        <div style={{fontFamily: EN, fontWeight: 900, fontSize: 44, color: K.red, textAlign: 'center', marginTop: 8}}>dB</div>
      </div>
      <Pop at={at('film', 2.4)} x={540} y={220} rot={-3}><Tag text="جواها شريط بيلف" size={58} /></Pop>
      <Pop at={tLoud + 6} x={540} y={330} rot={3}><Tag text="صوت عالي… بيفصل الممثلين" bg={K.red} color={K.white} size={54} /></Pop>
    </Scene>
  );
};

// Behind Aly (middle): Nolan's decision.
export const S8Nolan: React.FC<B> = () => (
  <AbsoluteFill>
    <Pop at={0} x={540} y={470} rot={-3} from={0.8}><Photo src={PJ + 'img/nolan_set.webp'} w={900} h={640} bw seed={83} pos="40% 30%" /></Pop>
    <Pop at={12} x={760} y={190} rot={5}><Tag text="كريستوفر نولان" size={54} /></Pop>
  </AbsoluteFill>
);

// A sound-proof box closes around the camera -> waves stop, meter green.
export const S8Blimp: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tAll = at('all', 0.3), tBox = at('box', 5.4), tQuiet = at('quiet', 8.8);
  const box = lin(f, tBox, tBox + 20);
  const noise = 1 - lin(f, tBox + 10, tBox + 26);
  return (
    <Scene bg="#121315">
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <BigCam x={420} y={860} s={1.2} noise={noise} />
        {noise > 0.05 ? Array.from({length: 4}, (_, i) => {
          const k = ((f + i * 8) % 32) / 32;
          return <circle key={i} cx={520} cy={840} r={200 + k * 380} fill="none" stroke={K.red} strokeWidth={10} opacity={(1 - k) * noise} />;
        }) : null}
        {box > 0 ? (
          <g>
            <rect x={80} y={560 + (1 - box) * -700} width={920} height={300} rx={30} fill="#4A4F57" stroke="#111" strokeWidth={8} />
            <rect x={80} y={860 + (1 - box) * 900} width={920} height={300} rx={30} fill="#4A4F57" stroke="#111" strokeWidth={8} />
            {box > 0.98 ? Array.from({length: 10}, (_, i) => <circle key={i} cx={130 + i * 92} cy={590} r={8} fill="#222" />) : null}
          </g>
        ) : null}
      </svg>
      <Pop at={tAll} x={540} y={240} rot={-3}><Tag text="الفيلم كله بالحوار… IMAX" bg={K.yellow} size={56} /></Pop>
      <Pop at={tBox + 10} x={540} y={1320} rot={3}><Tag text="صندوق كاتم للصوت" size={60} /></Pop>
      <div style={{position: 'absolute', left: 140, right: 140, top: 1480}}>
        <div style={{height: 40, borderRadius: 20, background: '#2a2a2a', overflow: 'hidden', border: `4px solid ${K.paper2}`}}>
          <div style={{height: '100%', width: `${15 + 83 * noise}%`, background: noise > 0.4 ? K.red : '#7BD389'}} />
        </div>
      </div>
      <div style={{position: 'absolute', left: 380, top: 1580}}><Stamp text="هُس 🤫" at={tQuiet} size={80} rot={-6} color="#7BD389" /></div>
    </Scene>
  );
};

// Top view: actors can't see each other past the huge camera -> a mirror lets them.
export const S8Mirror: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tBlock = at('block', 3.4), tMirror = at('mirror', 7.7);
  const mir = lin(f, tMirror, tMirror + 14);
  const actor = (x: number, y: number, c: string) => (
    <g transform={`translate(${x},${y})`}><circle r={70} fill={c} stroke="#111" strokeWidth={6} /><circle cx={0} cy={-20} r={10} fill="#111" /></g>
  );
  return (
    <Scene bg="#16130F">
      <Halftone color="#fff" size={18} dot={0.1} opacity={0.05} />
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {actor(540, 420, K.paper)}
        {actor(540, 1340, K.yellow)}
        <rect x={360} y={760} width={360} height={240} rx={20} fill="#3A3D42" stroke="#111" strokeWidth={7} />
        <text x={540} y={895} fontSize={56} fontFamily={EN} fontWeight={900} fill={K.cyan} textAnchor="middle">IMAX</text>
        {f >= tBlock && mir < 0.5 ? (
          <>
            <line x1={540} y1={500} x2={540} y2={750} stroke={K.red} strokeWidth={10} strokeDasharray="24 16" />
            <text x={600} y={660} fontSize={120} fill={K.red} fontWeight={900}>✕</text>
          </>
        ) : null}
        {mir > 0 ? (
          <>
            <line x1={760} y1={780} x2={960} y2={980} stroke={K.cyan} strokeWidth={18 * mir} strokeLinecap="round" />
            <path d={`M560,480 L860,880 L560,1270`} stroke="#7BD389" strokeWidth={9} strokeDasharray="22 14" strokeDashoffset={-f * 3} fill="none" opacity={mir} />
          </>
        ) : null}
      </svg>
      <Pop at={tBlock + 4} x={250} y={880} rot={-4}><Tag text="مش شايفين بعض" bg={K.red} color={K.white} size={50} /></Pop>
      <Pop at={tMirror + 8} x={830} y={1120} rot={4}><Tag text="مراية!" bg={K.cyan} size={64} /></Pop>
      <Pop at={4} x={540} y={200}><Tag text="من فوق" size={50} /></Pop>
    </Scene>
  );
};

// Behind Aly at the end: the first film shot entirely in IMAX.
export const S8First: React.FC<B> = ({b}) => {
  const at = useBeats(b);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 230, left: 60, right: 60, display: 'flex', justifyContent: 'center'}}>
        <Title text="أول فيلم *كله* IMAX" size={110} at={at('first', 0.3)} stroke />
      </div>
      <div style={{position: 'absolute', left: 300, top: 520}}><Stamp text="THE ODYSSEY" at={at('first', 0.3) + 20} size={80} rot={-6} color={K.yellow} /></div>
    </AbsoluteFill>
  );
};
