import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {MapPaths, lonLat} from '../blocks/geo';
import {AR, EN, K, Clip, Count, Halftone, Paper, Pop, Scene, Stamp, Tag, Title, lin, rnd, spr, useBeats} from './kit';
import {Hook} from './s02';

// Short 10 — how much does shooting on film cost in Egypt? Super 8 / 16mm / 35mm, 20,000 EGP per minute, receipt.
const PJ = 'projects/2026-10-08 shorts theodesy/';
type B = {b?: Record<string, number>};

const Price: React.FC<{text: string; at: number; x: number; y: number; rot?: number; bg?: string}> = ({text, at, x, y, rot = -4, bg = K.yellow}) => (
  <Pop at={at} x={x} y={y} rot={rot}>
    <div style={{position: 'relative', background: bg, color: K.ink, fontFamily: AR, fontWeight: 900, fontSize: 64, padding: '10px 36px 10px 60px', borderRadius: 14,
      border: `6px solid ${K.ink}`, boxShadow: '8px 10px 0 rgba(0,0,0,0.8)', whiteSpace: 'nowrap', direction: 'rtl'}}>
      <span style={{position: 'absolute', left: 18, top: '50%', width: 22, height: 22, borderRadius: 11, background: K.ink, transform: 'translateY(-50%)'}} />
      {text}
    </div>
  </Pop>
);

const Super8: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <rect x={-170} y={-90} width={300} height={170} rx={26} fill="#C9C2B4" stroke="#111" strokeWidth={7} />
    <rect x={-150} y={-70} width={120} height={60} rx={10} fill="#2A2A2A" />
    <rect x={130} y={-60} width={120} height={110} rx={14} fill="#2A2A2A" stroke="#111" strokeWidth={6} />
    <circle cx={260} cy={-5} r={46} fill="#1B1B1D" stroke="#111" strokeWidth={6} /><circle cx={260} cy={-5} r={24} fill="#3B5168" />
    <path d="M-60,80 L-30,230 L40,230 L30,80 Z" fill="#3A3A3A" stroke="#111" strokeWidth={6} />
    <text x={-20} y={50} fontSize={40} fontWeight={900} fontFamily={EN} fill="#111">SUPER 8</text>
  </g>
);

export const S10Hook: React.FC<B> = ({b}) => (
  <Hook b={b} n={10} title="تصوير دقيقة *خام* في مصر بكام؟" side={<Price text="؟؟؟ ج" at={18} x={220} y={980} rot={-10} />} />
);

// Card 1: Super 8 — cheap camera, low quality, ~5,000 + film ~3,000.
export const S10Super8: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tCam = at('cam', 2.7), tQ = at('quality', 5.9), tP1 = at('p1', 12.5), tP2 = at('p2', 17.5);
  return (
    <Scene bg="#16130F">
      <Pop at={at('pricey', 1.2)} x={540} y={200} rot={-3}><Tag text="الأسعار غالية…" size={58} /></Pop>
      <svg width={1080} height={1920} style={{position: 'absolute'}}><g opacity={lin(f, tCam - 6, tCam + 4)} transform="translate(60,0)"><Super8 x={470} y={720} s={1.35} /></g></svg>
      <Pop at={tCam + 4} x={540} y={420}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 120, color: K.yellow, textShadow: '0 8px 0 #000'}}>Super 8</div></Pop>
      {f >= tQ ? (
        <div style={{position: 'absolute', left: 160, right: 160, top: 1130}}>
          <div style={{fontFamily: AR, fontWeight: 900, fontSize: 46, color: K.white, marginBottom: 10}}>الكواليتي</div>
          <div style={{height: 32, borderRadius: 16, background: '#333', overflow: 'hidden'}}><div style={{height: '100%', width: `${22 * lin(f, tQ, tQ + 16)}%`, background: K.red}} /></div>
        </div>
      ) : null}
      <Price text="الكاميرا ≈ 5,000 ج" at={tP1} x={540} y={1330} rot={-4} />
      <Price text="الفيلم ≈ 3,000 ج" at={tP2} x={540} y={1470} rot={3} bg={K.paper} />
    </Scene>
  );
};

// Card 2: 16mm — rent 5,000/day + film 8,000–9,000.
export const S1016: React.FC<B> = ({b}) => {
  const at = useBeats(b);
  return (
    <Scene bg={K.ink}>
      <Pop at={0} x={540} y={640} rot={2} from={0.85}><Clip src={PJ + 'broll/b8_16mm.mp4'} start={20} w={760} h={860} seed={101} /></Pop>
      <Pop at={4} x={540} y={170}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 110, color: K.yellow, textShadow: '0 8px 0 #000'}}>16mm</div></Pop>
      <Price text="إيجار 5,000 ج / اليوم" at={at('rent', 4.8)} x={540} y={1180} rot={-4} />
      <Price text="الخام 8,000 – 9,000 ج / الدقيقة" at={at('film', 10.8)} x={540} y={1330} rot={3} bg={K.paper} />
    </Scene>
  );
};

// Card 3: 35mm — only ONE office in Egypt rents the camera.
export const S1035: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const at = useBeats(b);
  const tOne = at('one', 4.1);
  const [x0, y0] = lonLat(24.5, 32), [x1] = lonLat(37.5, 21.5);
  const s = 560 / (x1 - x0);
  const e = spr(f, fps, tOne - 6, 120, 14);
  return (
    <Scene bg="#16130F">
      <Pop at={2} x={540} y={200}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 140, color: K.yellow, textShadow: '0 8px 0 #000'}}>35mm</div></Pop>
      <Pop at={8} x={540} y={350}><Tag text="أفلام كتير اتصورت بيها" size={50} /></Pop>
      <div style={{position: 'absolute', left: 260, top: 480, width: 600, height: 560, transform: `scale(${e})`}}>
        <svg width={600} height={560}>
          <g transform={`translate(${20 - x0 * s},${10 - y0 * s}) scale(${s})`}><MapPaths only={['EGY']} style={() => ({fill: K.paper, stroke: K.ink, strokeWidth: 3 / s})} /></g>
          <circle cx={330} cy={200} r={22 + 6 * Math.sin(f / 4)} fill={K.red} stroke={K.ink} strokeWidth={5} />
        </svg>
        <Halftone color="#000" size={9} dot={0.2} opacity={0.15} />
      </div>
      <Pop at={tOne} x={540} y={1180} rot={-3}><Tag text="مكتب واحد بس في مصر بيأجرها" bg={K.yellow} size={54} /></Pop>
      <Pop at={at('price', 8.9)} x={540} y={1330} rot={3}><Tag text="وإيجارها لليوم الواحد…" size={52} /></Pop>
    </Scene>
  );
};

// Behind Aly: 75,000 EGP per day counter.
export const S10Day: React.FC<B> = ({b}) => {
  const at = useBeats(b);
  const t = at('n', 1.5);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 180, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <Count to={75000} a={t} b={t + 22} size={190} suffix="" />
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 70, color: K.white}}>جنيه في اليوم!</div>
      </div>
    </AbsoluteFill>
  );
};

// One minute of 35mm film = 20,000 EGP: stopwatch + money counter + flying notes.
export const S10Minute: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  const at = useBeats(b);
  const t0 = at('min', 3.2);
  const k = lin(f, t0, d - 6, 0, 1, (x) => x);
  const a = k * Math.PI * 2;
  return (
    <Scene bg={K.ink}>
      <div style={{position: 'absolute', top: 170, left: 60, right: 60, display: 'flex', justifyContent: 'center'}}>
        <Title text="الخام لوحده: *للدقيقة*" size={92} at={2} />
      </div>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <g transform="translate(540,760)">
          <rect x={-40} y={-330} width={80} height={60} rx={10} fill={K.paper2} />
          <circle r={280} fill={K.paper} stroke="#141210" strokeWidth={14} />
          <path d={`M0,0 L0,-260 A260,260 0 ${k > 0.5 ? 1 : 0},1 ${Math.sin(a) * 260},${-Math.cos(a) * 260} Z`} fill={K.red} opacity={0.35} />
          {Array.from({length: 60}, (_, i) => <line key={i} x1={0} y1={-262} x2={0} y2={i % 5 ? -245 : -225} stroke="#141210" strokeWidth={i % 5 ? 3 : 7} transform={`rotate(${i * 6})`} />)}
          <line x1={0} y1={0} x2={Math.sin(a) * 230} y2={-Math.cos(a) * 230} stroke={K.red} strokeWidth={12} strokeLinecap="round" />
          <circle r={18} fill="#141210" />
        </g>
        {Array.from({length: 12}, (_, i) => {
          if (f < t0 + i * 6) return null;
          const q = ((f - t0 - i * 6) % 50) / 50;
          return <g key={i} transform={`translate(${120 + rnd(i) * 840},${1100 - q * 900}) rotate(${q * 200 + i * 30})`} opacity={1 - q}>
            <rect x={-60} y={-30} width={120} height={60} rx={6} fill="#7BB27A" stroke="#2E5A2C" strokeWidth={4} /><circle r={16} fill="#2E5A2C" opacity={0.6} /></g>;
        })}
      </svg>
      <div style={{position: 'absolute', top: 1140, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <Count to={20000} a={t0} b={d - 6} size={170} />
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 60, color: K.white}}>جنيه… لدقيقة واحدة</div>
      </div>
    </Scene>
  );
};

// The receipt keeps printing: camera rent, lenses, crew, actors, everything -> "expensive!".
export const S10Receipt: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const items = [{t: 'إيجار الكاميرا', a: at('rent', 0.3)}, {t: 'العدسات', a: at('lens', 1.5)}, {t: 'الطاقم', a: at('crew', 2.6)}, {t: 'الممثلين', a: at('actors', 3.8)},
    {t: 'وكل حاجة تانية…', a: at('all', 4.8)}];
  const n = items.filter((x) => f >= x.a).length;
  return (
    <Scene bg="#16130F">
      <div style={{position: 'absolute', left: 190, top: 160, width: 700}}>
        <Paper w={700} h={Math.min(1200, 260 + n * 170)} seed={105} color={K.white}>
          <div style={{padding: '36px 46px', fontFamily: AR, color: K.ink, direction: 'rtl'}}>
            <div style={{fontWeight: 900, fontSize: 58, textAlign: 'center', borderBottom: '4px dashed #141210', paddingBottom: 16}}>فاتورة تصوير 🎬</div>
            <div style={{display: 'flex', justifyContent: 'space-between', fontWeight: 900, fontSize: 48, marginTop: 26}}><span>الخام (دقيقة)</span><span style={{fontFamily: EN}}>20,000</span></div>
            {items.map((x, i) => f >= x.a ? (
              <div key={i} style={{display: 'flex', justifyContent: 'space-between', fontWeight: 900, fontSize: 48, marginTop: 26, transform: `translateX(${lin(f, x.a, x.a + 8, 60, 0)}px)`,
                opacity: lin(f, x.a, x.a + 6)}}><span>+ {x.t}</span><span style={{fontFamily: EN}}>???</span></div>
            ) : null)}
          </div>
        </Paper>
      </div>
      <div style={{position: 'absolute', left: 330, top: 1340}}><Stamp text="غالي… غالي!" at={at('pricey', 6.2)} size={100} rot={-10} /></div>
    </Scene>
  );
};

// Behind Aly at the end: digital = delete & redo freely.
export const S10Digital: React.FC<B> = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 170, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 40, alignItems: 'center'}}>
        <div style={{fontSize: 150, transform: `rotate(${Math.sin(f / 4) * 10}deg)`}}>🗑️</div>
        <div style={{fontFamily: EN, fontWeight: 900, fontSize: 170, color: K.cyan, transform: `rotate(${f * 4}deg)`}}>↻</div>
      </div>
      <Pop at={10} x={540} y={470} rot={-3}><Tag text="الديجيتال: امسح وعيد براحتك" bg={K.cyan} size={56} /></Pop>
    </AbsoluteFill>
  );
};
