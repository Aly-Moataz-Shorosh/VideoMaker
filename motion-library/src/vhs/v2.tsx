import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {AR, EN, Pop, Scene, Stamp, Tag, Title, Count, shake, useBeats} from '../film/kit';
import {Hook} from './v1';
import {BluePanel, Cassette, Chip, Crt, Laptop, Rgb, V, Vcr, lin, spr, rnd} from './kit';

// Short 2 — the photo studio used to convert a tape for 30 EGP, now 300: costly with many tapes + privacy -> do it at home.
type B = {b?: Record<string, number>};

export const V2Hook: React.FC<B> = () => {
  const f = useCurrentFrame();
  return (
    <Hook title="تحويل شريط فيديو واحد… كان بـ *30 جنيه*">
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <g opacity={lin(f, 8, 18)}><Cassette x={540} y={lin(f, 8, 26, 300, 760)} s={0.8} rot={5 * Math.sin(f / 14)} spin={f * 4} label="المصيف ٢٠٠٢" /></g>
      </svg>
    </Hook>
  );
};

// A photo studio shop: you hand the tape + your money, done.
export const V2Shop: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const give = at('give', 1.5), done = at('done', 4);
  const tp = lin(f, give, give + 16), mp = lin(f, give + 6, give + 22);
  return (
    <Scene>
      {/* shop front */}
      <div style={{position: 'absolute', left: 140, top: 300, width: 800, height: 700, background: '#2A2E44', border: '6px solid #000', borderRadius: 16}}>
        <div style={{position: 'absolute', left: -30, right: -30, top: -20, height: 140, background: V.red, border: '6px solid #000', borderRadius: 14,
          display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <div style={{fontFamily: AR, fontWeight: 900, fontSize: 70, color: V.white, textShadow: '0 5px 0 #000'}}>استوديو تصوير 📷</div>
        </div>
        <div style={{position: 'absolute', left: 60, right: 60, top: 180, bottom: 0, background: '#0E1024', border: '6px solid #000', borderBottom: 'none',
          backgroundImage: 'repeating-linear-gradient(90deg, rgba(255,255,255,0.05) 0 4px, transparent 4px 90px)'}} />
      </div>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <g opacity={1 - lin(f, give + 14, give + 18)}><Cassette x={lin(f, give, give + 16, 260, 540)} y={1300 - 500 * tp + 120 * Math.sin(tp * Math.PI)} s={0.5} rot={tp * 30} spin={f * 4} label="VHS" /></g>
        {[0, 1, 2].map((i) => (
          <g key={i} opacity={(1 - lin(f, give + 20, give + 24)) * (f >= give + 6 ? 1 : 0)} transform={`translate(${lin(f, give + 6, give + 22, 820, 560) + i * 20},${1300 - 480 * mp + i * 14}) rotate(${-10 + i * 8})`}>
            <rect x={-90} y={-45} width={180} height={90} rx={8} fill="#7FB07A" stroke="#1F3A1C" strokeWidth={5} />
            <text x={0} y={18} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={46} fill="#1F3A1C">EGP</text>
          </g>
        ))}
      </svg>
      <Pop at={2} x={540} y={1190}><Tag text="خد الشريط والفلوس… وانزل" bg={V.white} size={52} /></Pop>
      <Pop at={done} x={540} y={720}><Stamp text="خلصت ✓" at={0} size={110} color={V.green} rot={-8} /></Pop>
      <Pop at={at('costly', 6)} x={540} y={1430} rot={3}><Tag text="بس ده الحل المكلّف" bg={V.yellow} size={56} /></Pop>
    </Scene>
  );
};

// Many tapes = costly (Aly review: make the reason clear): tapes drop one by one, each "300", the total runs up.
export const V2Price: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const m = at('many', 0.1);
  const step = 5;
  const n = Math.max(0, Math.min(10, Math.floor((f - m) / step) + 1));
  return (
    <Scene>
      <div style={{position: 'absolute', top: 220, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Title text="شرايط *كتير*… = فلوس كتير" size={86} stroke /></div>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {Array.from({length: 10}, (_, i) => {
          if (f < m + i * step) return null;
          const p = spr(f, 30, m + i * step);
          const x = i === 9 ? 540 : 190 + (i % 3) * 350, y = i === 9 ? 1150 : 520 + Math.floor(i / 3) * 210;
          return (
            <g key={i} opacity={Math.min(1, p * 2)} transform={`translate(0,${(1 - p) * -260})`}>
              <Cassette x={x} y={y} s={0.42} rot={(rnd(i) - 0.5) * 16} spin={f * 3} label="" />
              <g transform={`translate(${x + 80},${y - 60}) rotate(8)`}>
                <rect x={-58} y={-26} width={116} height={52} rx={10} fill={V.yellow} stroke="#000" strokeWidth={4} />
                <text x={0} y={14} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={36} fill="#111">300</text>
              </g>
            </g>
          );
        })}
      </svg>
      <div style={{position: 'absolute', top: 1290, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
        <BluePanel w={820} h={170}><div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 22, direction: 'ltr'}}>
          <Rgb size={58} font={EN} dir="ltr">{`${n} × 300 =`}</Rgb>
          <div style={{fontFamily: EN, fontWeight: 900, fontSize: 92, color: V.yellow}}>{(n * 300).toLocaleString('en-US')}</div>
        </div></BluePanel>
      </div>
    </Scene>
  );
};

// Privacy: strangers watching your family tape on the shop's TV.
export const V2Privacy: React.FC<B & {clip?: number}> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const eyes = at('eyes', 1.2), lock = at('lock', 3.5);
  return (
    <Scene>
      <Pop at={0} x={540} y={620} from={0.8}>
        <Crt w={760}>
          <AbsoluteFill style={{background: V.blue, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <div style={{fontFamily: AR, fontWeight: 900, fontSize: 60, color: V.white, textAlign: 'center', lineHeight: 1.3}}>فيديوهات<br />العيلة 🎂</div>
          </AbsoluteFill>
        </Crt>
      </Pop>
      {[[160, 300], [900, 360], [140, 980], [920, 1000]].map(([x, y], i) => (
        <Pop key={i} at={eyes + i * 3} x={x} y={y} out={lock}><div style={{fontSize: 120, transform: `translateX(${4 * Math.sin((f + i * 9) / 4)}px)`}}>👀</div></Pop>
      ))}
      {f >= lock ? (
        <Pop at={lock} x={540} y={640}><div style={{width: 300, height: 300, borderRadius: '50%', background: V.yellow, border: '8px solid #000', display: 'flex', alignItems: 'center',
          justifyContent: 'center', fontSize: 170, boxShadow: '0 20px 40px rgba(0,0,0,0.6)'}}>🔒</div></Pop>
      ) : null}
      <Pop at={lock + 6} x={540} y={1180}><Title text="_خصوصيتك_ تفضل معاك" size={84} stroke /></Pop>
    </Scene>
  );
};

// The second way: at home, your own VCR + your PC (teaser -> full video).
export const V2Home: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  return (
    <Scene>
      <div style={{position: 'absolute', top: 260, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Title text="الحل التاني: *من بيتك*" size={96} stroke /></div>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <path d="M140,1000 L540,620 L940,1000 Z" fill={V.red} stroke="#000" strokeWidth={8} opacity={lin(f, 2, 10)} />
        <rect x={210} y={990} width={660} height={430} fill="#23263A" stroke="#000" strokeWidth={8} opacity={lin(f, 2, 10)} />
        {f >= at('vcr', 1.2) ? <g opacity={lin(f, at('vcr', 1.2), at('vcr', 1.2) + 8)}><Vcr x={540} y={1330} s={0.8} play /></g> : null}
        {f >= at('pc', 2.2) ? <g opacity={lin(f, at('pc', 2.2), at('pc', 2.2) + 8)}><Laptop x={540} y={1190} s={0.62}>
          <div style={{position: 'absolute', inset: 0, background: V.blue, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: EN, fontWeight: 900, fontSize: 60, color: V.white}}>● REC</div>
        </Laptop></g> : null}
      </svg>
      <Pop at={at('best', 3.5)} x={540} y={540}><Tag text="الأفضل لو شرايطك كتير ✓" bg={V.green} size={54} /></Pop>
    </Scene>
  );
};
