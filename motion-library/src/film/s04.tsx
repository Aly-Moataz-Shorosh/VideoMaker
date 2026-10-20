import React from 'react';
import {AbsoluteFill, Img, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, K, Clip, Halftone, Photo, Pop, Scene, Stamp, Strip, Tag, Title, img, lin, spr, useBeats, rnd} from './kit';
import {Palm, Pyramid, Sun} from './draw';
import {Hook} from './s02';

// Short 4 — silver halide, film, developing (التحميض), then colour.
const PJ = 'projects/2026-10-08 shorts theodesy/';
type B = {b?: Record<string, number>};

export const S4Hook: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  return (
    <Hook b={b} n={4} title="إزاي *شريط الفيلم* بيحفظ الصورة؟" side={
      <div style={{position: 'absolute', left: -60, top: 860, transform: `rotate(-12deg) translateX(${lin(f, 10, 40, -500, 0)}px)`}}>
        <Strip frames={[PJ + 'img/poster.jpg', PJ + 'img/samir.jpg', PJ + 'img/nolan_cam.jpg']} fw={170} fh={130} />
      </div>
    } />
  );
};

// Microscope view of silver halide crystals: light hits -> crystals turn black -> B&W picture.
export const S4Silver: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tHit = at('hit', 6.3), tBW = at('bw', 9.5);
  const N = 16, R = 380;
  const picture = (x: number, y: number) => { // pyramid silhouette -> which crystals get light
    const u = x / (R * 2), v = y / (R * 2);
    return v > 0.75 || (v > 0.3 && Math.abs(u - 0.5) < (v - 0.3) * 0.9);
  };
  return (
    <Scene bg="#0E0D0C">
      <div style={{position: 'absolute', left: 540 - R, top: 820 - R, width: R * 2, height: R * 2, borderRadius: R, overflow: 'hidden', border: `16px solid ${K.paper2}`,
        boxShadow: '0 0 0 10px #000, 0 30px 80px rgba(0,0,0,0.8)', background: '#9DA3A8'}}>
        <svg width={R * 2} height={R * 2}>
          {Array.from({length: N * N}, (_, i) => {
            const gx = i % N, gy = Math.floor(i / N);
            const x = (gx + 0.5 + (rnd(i) - 0.5) * 0.5) * (R * 2 / N), y = (gy + 0.5 + (rnd(i + 99) - 0.5) * 0.5) * (R * 2 / N);
            const lit = !picture(x, y);
            const dark = lit ? lin(f, tHit + (gy + gx) * 0.6, tHit + 12 + (gy + gx) * 0.6) : 0;
            const sz = 14 + rnd(i * 3) * 10;
            const shade = Math.round(205 - dark * 190);
            return <polygon key={i} points={`${x},${y - sz} ${x + sz * 0.9},${y + sz * 0.6} ${x - sz * 0.9},${y + sz * 0.6}`} transform={`rotate(${rnd(i * 7) * 120} ${x} ${y})`}
              fill={`rgb(${shade},${shade},${shade + 6})`} stroke="#2a2a2a" strokeWidth={1.5} />;
          })}
          {f >= tHit - 10 ? Array.from({length: 26}, (_, i) => {
            const k = ((f - tHit + 10 - i * 2) % 30) / 30;
            if (f - tHit + 10 - i * 2 < 0) return null;
            return <circle key={'p' + i} cx={rnd(i * 5) * R * 2} cy={k * R * 2} r={7} fill={K.yellow} opacity={1 - k} />;
          }) : null}
        </svg>
      </div>
      <Pop at={at('name', 0.8)} x={540} y={250} rot={-2}><Tag text="Silver Halide · هاليد الفضة" size={56} /></Pop>
      <Pop at={tHit} x={800} y={1290} rot={4} out={tBW - 2}><Tag text="الضوء يغمّقها" bg={K.yellow} size={56} /></Pop>
      <div style={{position: 'absolute', left: 100, top: 1400}}><Stamp text="أبيض وأسود فقط" at={tBW} size={70} rot={-6} /></div>
    </Scene>
  );
};

// The film reel unspools into a long strip; "sensitive to light".
export const S4Film: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tFilm = at('film', 9.9), tSens = at('sens', 14.7);
  const glow = lin(f, tSens, tSens + 10);
  return (
    <Scene bg={K.ink}>
      <div style={{position: 'absolute', top: 210, left: 60, right: 60, display: 'flex', justifyContent: 'center', opacity: 1 - lin(f, tFilm - 10, tFilm)}}>
        <Title text="قبل ما نوصل *للألوان*…" size={92} at={4} />
      </div>
      <Pop at={6} x={330} y={760} from={0.5}>
        <div style={{width: 520, height: 520, borderRadius: 260, overflow: 'hidden', transform: `rotate(${f * 3}deg)`, boxShadow: '0 30px 60px rgba(0,0,0,0.7)'}}>
          <Img src={img(PJ + 'img/reel.webp')} style={{width: 780, height: 520, objectFit: 'cover', objectPosition: '25% 50%', marginLeft: -40, filter: 'grayscale(0.4) contrast(1.1)'}} />
        </div>
      </Pop>
      {f >= tFilm - 20 ? (
        <div style={{position: 'absolute', top: 1060, left: 0, transform: `translateX(${lin(f, tFilm - 20, tFilm + 60, 1100, -500, (x) => x)}px) rotate(-6deg)`,
          filter: `drop-shadow(0 0 ${40 * glow}px ${K.yellow})`}}>
          <Strip frames={[PJ + 'img/poster.jpg', PJ + 'img/samir.jpg', PJ + 'img/imax_set.jpg', PJ + 'img/nolan_cam.jpg', PJ + 'img/poster.jpg', PJ + 'img/samir.jpg']}
            fw={300} fh={220} bw />
        </div>
      ) : null}
      <Pop at={tFilm} x={760} y={480} rot={4}><Tag text="شريط الفيلم" bg={K.yellow} size={68} /></Pop>
      <Pop at={tSens} x={540} y={1460} rot={-3}><Tag text="مادة حساسة للضوء" size={56} /></Pop>
    </Scene>
  );
};

// Real 16mm camera running (film exposed inside the camera).
export const S4Camera: React.FC<B> = () => (
  <Scene bg={K.ink}>
    <Pop at={0} x={540} y={800} rot={2} from={0.85}><Clip src={PJ + 'broll/b8_16mm.mp4'} start={13.5} w={860} h={1240} seed={41} /></Pop>
    <Pop at={8} x={540} y={240} rot={-3}><Tag text="جوه الكاميرا" size={58} /></Pop>
  </Scene>
);

// Too much light burns the film -> must be developed (التحميض) in the dark.
export const S4Burn: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tBurn = at('burn', 1.4), tDev = at('dev', 6.9);
  const burn = lin(f, tBurn, tBurn + 40, 0, 1, (x) => x);
  return (
    <Scene bg={f < tDev ? K.ink : '#2A0505'}>
      {f < tDev ? (
        <>
          <div style={{position: 'absolute', left: 140, top: 520, width: 800, height: 600, background: '#000', overflow: 'hidden', borderRadius: 6}}>
            <Img src={img(PJ + 'img/poster.jpg')} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: '50% 30%', filter: `brightness(${1 + burn * 3})`}} />
            {burn > 0 ? (
              <div style={{position: 'absolute', left: '45%', top: '40%', width: burn * 1400, height: burn * 1400, transform: 'translate(-50%,-50%)', borderRadius: '50%',
                background: `radial-gradient(circle, #fff 0%, #fff 30%, ${K.yellow} 45%, #B23A0E 55%, #000 62%, transparent 70%)`}} />
            ) : null}
          </div>
          <Pop at={tBurn} x={540} y={1260} rot={-4}><Tag text="⚠ ضوء قوي = الفيلم يتحرق" bg={K.red} color={K.white} size={54} /></Pop>
        </>
      ) : (
        <>
          <div style={{position: 'absolute', left: 540, top: 120, width: 300, height: 300, transform: 'translateX(-50%)', borderRadius: 150,
            background: `radial-gradient(circle, #FF3B30 0%, rgba(229,35,43,0.4) 40%, transparent 70%)`}} />
          <div style={{position: 'absolute', top: 470, left: 0, right: 0, textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 210, color: '#FF5A4E',
            textShadow: '0 0 60px rgba(255,60,40,0.7)'}}>التحميض</div>
          <Pop at={tDev + 8} x={540} y={980}><Tag text="في أوضة ضلمة بنور أحمر" bg="#140303" color="#FF8B80" size={52} /></Pop>
        </>
      )}
    </Scene>
  );
};

// Real darkroom footage + negative -> positive copies.
export const S4Develop: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tCopy = at('copies', 5.6);
  return (
    <Scene bg="#140303">
      <Pop at={0} x={540} y={700} rot={-2} from={0.85}><Clip src={PJ + 'broll/b5_tintype.mp4'} start={27.2} w={760} h={820} pos="50% 32%" zoom={1.7} seed={51} /></Pop>
      <Pop at={at('fix', 2.7)} x={540} y={220} rot={3}><Tag text="مواد كيميائية… والصورة تثبت" size={52} /></Pop>
      {f >= tCopy ? Array.from({length: 5}, (_, i) => {
        const k = spr(f, 30, tCopy + i * 4, 170, 14);
        return (
          <div key={i} style={{position: 'absolute', left: 120 + i * 175, top: 1130 + (i % 2) * 40, transform: `scale(${k}) rotate(${(rnd(i) - 0.5) * 18}deg)`}}>
            <Photo src={PJ + 'img/negative_hands.jpg'} w={170} h={220} bw seed={60 + i} pos="60% 40%" />
          </div>
        );
      }) : null}
      <Pop at={tCopy + 6} x={540} y={1420}><Tag text="نسخ دائمة" bg={K.yellow} size={58} /></Pop>
    </Scene>
  );
};

// Colour film: three sensitive layers stack up, the picture turns from B&W to colour.
export const S4Color: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tLayers = at('layers', 1.5), tColor = at('color', 7.2);
  const col = lin(f, tColor, tColor + 24);
  const layers = [{c: '#2EC4D6', t: 'سماوي'}, {c: '#D6338A', t: 'أرجواني'}, {c: '#FFC21A', t: 'أصفر'}];
  return (
    <Scene bg={K.ink}>
      <div style={{position: 'absolute', left: 140, top: 230, width: 800, height: 560, overflow: 'hidden', borderRadius: 8, boxShadow: '0 30px 60px rgba(0,0,0,0.6)'}}>
        <svg width={800} height={560} viewBox="0 330 640 600" style={{filter: `grayscale(${1 - col}) saturate(${1 + col * 0.3})`}}>
          <rect x={0} y={330} width={640} height={600} fill="#7FB7E6" />
          <Sun x={520} y={430} r={46} /><Palm x={150} y={900} s={1.1} /><Pyramid x={350} y={900} s={1.05} />
          <rect x={0} y={900} width={640} height={60} fill="#D9B46A" />
        </svg>
      </div>
      {layers.map((l, i) => {
        const k = spr(f, 30, tLayers + i * 6, 150, 13);
        return (
          <div key={i} style={{position: 'absolute', left: 190, top: 960 + i * 120, width: 700, height: 90, background: l.c, opacity: 0.9 * k, borderRadius: 10,
            transform: `perspective(900px) rotateX(55deg) translateY(${(1 - k) * 300}px)`, border: `4px solid ${K.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontFamily: AR, fontWeight: 900, fontSize: 54, color: K.ink}}>{l.t}</div>
        );
      })}
      <Pop at={tLayers} x={540} y={880}><Tag text="طبقات حساسة لكل لون" size={52} /></Pop>
      <div style={{position: 'absolute', left: 600, top: 760}}><Stamp text="بالألوان!" at={tColor} size={86} rot={-8} color={K.yellow} /></div>
    </Scene>
  );
};

// Behind Aly at the end: colour film strip "a picture from the past".
export const S4Past: React.FC<B> = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 220, left: 0, transform: `translateX(${-((f * 4) % 330)}px) rotate(-5deg)`}}>
        <Strip frames={Array(6).fill(0).map((_, i) => PJ + ['img/poster.jpg', 'img/samir.jpg', 'img/imax_set.jpg'][i % 3])} fw={300} fh={220} />
      </div>
      <Pop at={10} x={540} y={600} rot={-3}><Tag text="صورة محفوظة من الماضي" bg={K.yellow} size={56} /></Pop>
    </AbsoluteFill>
  );
};
