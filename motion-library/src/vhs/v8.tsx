import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {AR, EN, Pop, Scene, Stamp, Tag, Title, useBeats} from '../film/kit';
import {CLIP, Hook} from './v1';
import {Cassette, Crt, Footage, Rgb, SmallTape, V, Vcr, blink, lin, rnd, spr} from './kit';

// Short 8 — nostalgia: our old tapes are relics with no other copy; save our memories and our families.
type B = {b?: Record<string, number>};

const LABELS = ['فرح خالو ١٩٩٨', 'عيد ميلادي ٢٠٠٣', 'المصيف ٢٠٠١', 'سبوع أختي', 'العيد ١٩٩٩', 'رحلة الأقصر'];

export const V8Hook: React.FC<B> = () => {
  const f = useCurrentFrame();
  return (
    <Hook title="فاكر *شكلك زمان*؟">
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {[0, 1, 2].map((i) => {
          const p = spr(f, 30, 8 + i * 5);
          return <g key={i} opacity={Math.min(1, p * 2)}><Cassette x={300 + i * 240} y={560 + (1 - p) * -300 + i * 40} s={0.42} rot={(i - 1) * 12} spin={f * 3} label="" /></g>;
        })}
      </svg>
    </Hook>
  );
};

// A box of family tapes with hand-written labels; "no other copy".
export const V8Box: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  return (
    <Scene>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {LABELS.map((t, i) => {
          const p = spr(f, 30, 2 + i * 4, 150, 14);
          const x = 540 + ((i % 2) ? 120 : -120) + (rnd(i) - 0.5) * 60, y = 1180 - i * 150;
          return <g key={i} opacity={Math.min(1, p * 2)}><Cassette x={x} y={y - (1 - p) * 500} s={0.62} rot={(rnd(i + 3) - 0.5) * 14} spin={0} label={t} /></g>;
        })}
        {f >= at('hi8', 2.5) ? <g transform={`translate(0,${(1 - spr(f, 30, at('hi8', 2.5))) * 300})`}><SmallTape x={830} y={1360} s={1} rot={-10} spin={f * 3} /></g> : null}
      </svg>
      <Pop at={at('copy', 3.5)} x={540} y={1490}><Stamp text="مالهاش نسخة تانية" at={0} size={88} color={V.red} rot={-5} /></Pop>
    </Scene>
  );
};

// The tape plays: real footage of the old cartoon tape on the CRT, VCR below with spinning tape.
export const V8Play: React.FC<B & {clip?: number; pos?: string; zoom?: number; title?: string}> = ({b, clip = 18, pos = '50% 50%', zoom = 1.04, title = 'دي *آثار*… لازم نحتفظ بيها'}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const on = lin(f, 2, 12);
  return (
    <Scene>
      <Pop at={0} x={540} y={560} from={0.85}><Crt w={940} on={on}><Footage src={CLIP('easy_color')} start={clip} pos={pos} zoom={zoom} /></Crt></Pop>
      <svg width={1080} height={1920} style={{position: 'absolute'}}><Vcr x={540} y={1110} s={1.3} play led={1} /></svg>
      <Pop at={at('relic', 2)} x={540} y={1330}><Title text={title} size={72} stroke /></Pop>
    </Scene>
  );
};

// Tape -> digital file -> phone / flash / family far away.
export const V8Save: React.FC<B & {tag?: string; icons?: boolean; label?: string}> = ({b, tag = 'ابعته لأهلك في أي حتة', icons = true, label = 'فرح ١٩٩٨'}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const p = lin(f, at('dig', 1), at('dig', 1) + 22);
  const fam = at('fam', 3);
  return (
    <Scene>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <g opacity={1 - p}><Cassette x={540} y={640} s={1.25} spin={f * 4} label={label} /></g>
        {Array.from({length: 40}, (_, i) => {
          const r = rnd(i * 3.3), t = Math.max(0, Math.min(1, p * 1.6 - r * 0.6));
          return <rect key={i} x={340 + rnd(i) * 400 + (540 - 340 - rnd(i) * 400) * t} y={420 + rnd(i + 9) * 200 + 380 * t} width={18} height={18} fill={[V.mag, V.cyan, V.yellow][i % 3]} opacity={t > 0 && t < 1 ? 1 : 0} />;
        })}
      </svg>
      <Pop at={at('dig', 1) + 18} x={540} y={1000}>
        <div style={{width: 420, height: 500, background: V.white, borderRadius: 24, border: '6px solid #000', display: 'flex', flexDirection: 'column', alignItems: 'center',
          justifyContent: 'center', boxShadow: '0 20px 40px rgba(0,0,0,0.6)'}}>
          <div style={{fontSize: 190}}>🎞️</div><div style={{fontFamily: EN, fontWeight: 900, fontSize: 80, color: '#111', direction: 'ltr'}}>.MP4</div>
        </div>
      </Pop>
      {(icons ? [['📱', 220, 1380], ['💾', 540, 1440], ['👨‍👩‍👧', 860, 1380]] : []).map(([ic, x, y], i) => (
        <Pop key={i} at={fam + i * 4} x={x as number} y={y as number}><div style={{fontSize: 130}}>{ic}</div></Pop>
      ))}
      <Pop at={icons ? fam + 14 : 4} x={540} y={300}><Tag text={tag} bg={V.yellow} size={58} /></Pop>
    </Scene>
  );
};

// End behind Aly: "secure our memories and our families".
export const V8End: React.FC<B> = () => {
  const f = useCurrentFrame();
  return (
    <Scene>
      <div style={{position: 'absolute', top: 260, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Title text="كده _أمّنا_ ذكرياتنا… وأُسَرنا" size={90} stroke /></div>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <g opacity={lin(f, 4, 12)}>
          <path d="M540,620 L820,720 L800,1060 Q760,1300 540,1420 Q320,1300 280,1060 L260,720 Z" fill={V.blue} stroke="#000" strokeWidth={10} />
          <path d="M540,660 L780,745 L762,1050 Q728,1260 540,1370 Q352,1260 318,1050 L300,745 Z" fill="none" stroke={V.cyan} strokeWidth={4} opacity={0.6} />
        </g>
        <g opacity={lin(f, 8, 16)}><Cassette x={540} y={960} s={0.7} spin={f * 3} label="ذكرياتنا" /></g>
      </svg>
      <Pop at={22} x={540} y={1260}><Rgb size={90} font={EN} dir="ltr" color={V.green}>SAVED ✓</Rgb></Pop>
    </Scene>
  );
};

// Last line behind Aly: "pray for me while you watch your memories".
export const V8Pray: React.FC<B> = () => (
  <AbsoluteFill>
    <div style={{position: 'absolute', top: 260, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Title text="ادعيلي وانت بتتفرج على *ذكرياتك* 🤍" size={84} stroke /></div>
  </AbsoluteFill>
);

// Real intro footage (him with his tapes + the clone sketch) BIG so you see what he says (Aly review 1).
export const V8Real: React.FC<B & {clip?: number; title?: string; pos?: string; zoom?: number}> = ({clip = 0, title = '', pos = '50% 50%', zoom = 1}) => {
  const f = useCurrentFrame();
  return (
    <Scene>
      <div style={{position: 'absolute', top: 190, left: 40, right: 40, display: 'flex', justifyContent: 'center'}}><Title text={title} size={80} stroke /></div>
      <Pop at={0} x={540} y={800} from={0.9}>
        <div style={{width: 1040, height: 640, borderRadius: 30, overflow: 'hidden', border: '6px solid #000', position: 'relative', boxShadow: '0 30px 60px rgba(0,0,0,0.6)'}}>
          <Footage src={CLIP('intro')} start={clip} pos={pos} zoom={zoom} />
          <AbsoluteFill style={{backgroundImage: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.25) 0px, rgba(0,0,0,0.25) 2px, transparent 2px, transparent 5px)'}} />
          <div style={{position: 'absolute', left: 30, top: 24, opacity: blink(f, 2, 15)}}><Rgb size={44} font={EN} dir="ltr" color={V.white}>▶ PLAY</Rgb></div>
        </div>
      </Pop>
    </Scene>
  );
};
