import React from 'react';
import {AbsoluteFill, Img, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, OLD, K, Halftone, Photo, Pop, Scene, Stamp, Strip, Tag, Title, img, lin, rnd, spr, useBeats} from './kit';
import {Hook} from './s02';
import {ShipScene} from './s01';

// Short 7 — digital era: "Samir w Shahir w Baheer" colours shocked us; old films have soul (grain, no pixels).
const PJ = 'projects/2026-10-08 shorts theodesy/';
type B = {b?: Record<string, number>};

export const S7Hook: React.FC<B> = ({b}) => (
  <Hook b={b} n={7} title="ليه ألوان *سمير وشهير وبهير* صدمتنا؟" side={
    <Pop at={16} x={190} y={1000} rot={-8}><Photo src={PJ + 'img/samir.jpg'} w={300} h={220} bw={false} seed={71} /></Pop>
  } />
);

// Film strip turns into pixels: the digital era; early-2000s films; the movie pops in.
export const S7Digital: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tDig = at('digital', 0.2), tCam = at('cam', 2.5), tY = at('years', 9), tMov = at('movie', 11.1);
  const px = lin(f, tDig + 4, tDig + 40);
  return (
    <Scene bg="#101215">
      <div style={{position: 'absolute', left: 140, top: 330, width: 800, height: 600}}>
        <div style={{position: 'absolute', inset: 0, opacity: 1 - px}}><Strip frames={[PJ + 'img/samir.jpg']} fw={800} fh={480} /></div>
        <div style={{position: 'absolute', left: 0, top: 60, display: 'grid', gridTemplateColumns: 'repeat(20, 40px)'}}>
          {Array.from({length: 240}, (_, i) => {
            const k = lin(f, tDig + 4 + rnd(i) * 30, tDig + 14 + rnd(i) * 30);
            const c = ['#E5232B', '#2EC4D6', '#FFC21A', '#7BD389', '#F5F3EF', '#D6338A'][Math.floor(rnd(i * 3) * 6)];
            return <div key={i} style={{width: 38, height: 38, margin: 1, background: c, opacity: k * 0.9, transform: `scale(${k})`}} />;
          })}
        </div>
      </div>
      <Pop at={tDig + 6} x={540} y={220} rot={-3}><Tag text="عصر الديجيتال" bg={K.cyan} size={66} /></Pop>
      <Pop at={tCam} x={300} y={1100} rot={-5}><Tag text="بكاميرا عادية خالص" size={52} /></Pop>
      <Pop at={tY} x={780} y={1100} rot={5}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 120, color: K.yellow, textShadow: '0 8px 0 #000'}}>2000s</div></Pop>
      {f >= tMov ? <Pop at={tMov} x={540} y={1370} rot={-2}><Tag text="ومنهم: سمير وشهير وبهير" bg={K.yellow} size={58} /></Pop> : null}
    </Scene>
  );
};

// Behind Aly (middle): the movie picture big behind him + "إيه ده؟!".
export const S7Shock: React.FC<B> = ({b}) => {
  const at = useBeats(b);
  return (
    <AbsoluteFill>
      <Pop at={0} x={540} y={520} rot={-3} from={0.8}><Photo src={PJ + 'img/samir.jpg'} w={960} h={620} bw={false} seed={72} pos="50% 30%" /></Pop>
      <Pop at={at('what', 4)} x={800} y={230} rot={8}>
        <div style={{background: K.white, border: `6px solid ${K.ink}`, borderRadius: 30, padding: '8px 30px', fontFamily: AR, fontWeight: 900, fontSize: 80, color: K.ink,
          boxShadow: '8px 10px 0 rgba(0,0,0,0.85)', whiteSpace: 'nowrap'}}>إيه ده؟!</div>
      </Pop>
    </AbsoluteFill>
  );
};

// Saturation slider: colours pump up to "crazy", swatches pop; then back to normal ("we got used to it").
export const S7Colors: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tSat = at('sat', 3.2), tBack = at('back', 10.1), tNorm = at('normal', 14);
  const s = 0.35 + 1.9 * lin(f, 6, tSat + 20) - 1.0 * lin(f, tBack, tBack + 30);
  const knob = (s - 0.35) / 1.9;
  return (
    <Scene bg={K.ink}>
      <Pop at={0} x={540} y={680} from={0.85}>
        <div style={{width: 960, height: 640, borderRadius: 10, overflow: 'hidden', boxShadow: '0 30px 60px rgba(0,0,0,0.6)'}}>
          <Img src={img(PJ + 'img/samir.jpg')} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: '50% 25%', filter: `saturate(${s}) contrast(${1 + (s - 1) * 0.12})`}} />
        </div>
      </Pop>
      <div style={{position: 'absolute', left: 120, right: 120, top: 1110}}>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 52, color: K.white, marginBottom: 14}}>تشبّع الألوان</div>
        <div style={{position: 'relative', height: 26, borderRadius: 13, background: 'linear-gradient(to left, #E5232B, #FFC21A, #7BD389, #2EC4D6, #888)'}}>
          <div style={{position: 'absolute', top: -22, left: `${(1 - knob) * 100}%`, width: 70, height: 70, marginLeft: -35, borderRadius: 35, background: K.white, border: `6px solid ${K.ink}`}} />
        </div>
      </div>
      {f >= tSat && f < tBack ? ['#E8438E', '#3FAE49', '#E5232B', '#F2C14E'].map((c, i) => (
        <Pop key={i} at={tSat + i * 3} x={200 + i * 230} y={1330}><div style={{width: 130, height: 130, borderRadius: 18, background: c, border: `6px solid ${K.ink}`}} /></Pop>
      )) : null}
      {f < tBack ? <Pop at={tSat + 4} x={540} y={240} rot={-3}><Tag text="ألوان جامدة ومشبّعة" bg={K.yellow} size={62} /></Pop>
        : <Pop at={tBack} x={540} y={240} rot={3}><Tag text="بعد ما اتعودنا عليها…" size={60} /></Pop>}
      <div style={{position: 'absolute', left: 380, top: 1330}}><Stamp text="عادي" at={tNorm} size={100} rot={-8} color={K.paper} /></div>
    </Scene>
  );
};

// Old films have a soul: a flickering sepia frame with grain, scratches, gate weave.
export const S7Soul: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const weave = Math.sin(f * 1.7) * 3 + (rnd(f) - 0.5) * 3;
  return (
    <Scene bg="#0A0806">
      <div style={{position: 'absolute', left: 60, top: 330, width: 960, height: 680, overflow: 'hidden', transform: `translateY(${weave}px)`, borderRadius: 30,
        filter: `sepia(0.85) contrast(1.15) brightness(${0.85 + 0.15 * rnd(f * 3)})`}}>
        <ShipScene w={960} h={680} />
        <Img src={img(`bg/grain_${Math.floor(f / 2) % 3}.png`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: 0.8, mixBlendMode: 'overlay'}} />
        {rnd(Math.floor(f / 3)) > 0.4 ? <div style={{position: 'absolute', top: 0, bottom: 0, left: `${rnd(Math.floor(f / 3) * 7) * 100}%`, width: 3, background: 'rgba(255,255,255,0.5)'}} /> : null}
        <div style={{position: 'absolute', inset: 0, background: 'radial-gradient(ellipse, transparent 50%, rgba(0,0,0,0.7) 100%)'}} />
      </div>
      <Pop at={at('old', 2)} x={540} y={220} rot={-3}><Tag text="أفلام قديمة… زي تيتو" size={58} /></Pop>
      <Pop at={at('soul', 9.4)} x={540} y={1250} from={0.2}><div style={{fontFamily: OLD, fontSize: 230, color: K.yellow, textShadow: '0 10px 0 #000', lineHeight: 1}}>روح</div></Pop>
    </Scene>
  );
};

// Pixels (squares) vs film grain (chemical particles) under a magnifier.
export const S7Grain: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tGrain = at('grain', 0.8), tPix = at('pixels', 6.7), tAtoms = at('atoms', 11);
  const z = 1 + 2.5 * lin(f, 4, 60);
  const lens = (src: string, top: number, col: string, label: string, a: number) => (
    <div style={{position: 'absolute', left: 240, top, width: 600, height: 600, borderRadius: 300, overflow: 'hidden', border: `14px solid ${col}`, opacity: lin(f, a - 6, a),
      boxShadow: '0 20px 50px rgba(0,0,0,0.7)', background: '#000'}}>
      <Img src={img(PJ + src)} style={{width: 1000, height: 660, objectFit: 'cover', transform: `translate(-200px,-30px) scale(${z})`, transformOrigin: '50% 35%',
        imageRendering: src.endsWith('.png') ? 'pixelated' : 'auto'}} />
      {src.endsWith('.jpg') ? <Img src={img(`bg/grain_${Math.floor(f / 2) % 3}.png`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: 0.9, mixBlendMode: 'overlay', transform: 'scale(1.6)'}} /> : null}
      <div style={{position: 'absolute', bottom: 40, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Tag text={label} bg={col} size={50} /></div>
    </div>
  );
  return (
    <Scene bg={K.ink}>
      {lens('img/poster_grain.jpg', 160, K.yellow, 'ذرات كيميائية', tGrain)}
      {lens('img/poster_px.png', 820, K.cyan, 'بيكسلز = مربعات', tPix)}
      {f >= tPix + 20 ? <div style={{position: 'absolute', left: 300, top: 1100, width: 480, height: 14, background: K.red, transform: 'rotate(-35deg)', opacity: lin(f, tPix + 20, tPix + 26)}} /> : null}
      <Pop at={tAtoms} x={540} y={770}><Tag text="انت شايف ذرات المادة نفسها" bg={K.white} size={50} /></Pop>
    </Scene>
  );
};

// Behind Aly at the end: film beats digital.
export const S7Better: React.FC<B> = () => (
  <AbsoluteFill>
    <div style={{position: 'absolute', top: 230, left: 60, right: 60, display: 'flex', justifyContent: 'center'}}>
      <Title text="الخام *أحسن* من الديجيتال" size={100} at={4} stroke />
    </div>
  </AbsoluteFill>
);
