import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {AR, EN, Count, Pop, Scene, Stamp, Tag, Title, Flash, useBeats} from '../film/kit';
import {Chain, CLIP, Hook} from './v1';
import {Box, Cable, Cassette, Chip, Crt, Footage, Laptop, Rgb, RcaPlug, V, blink, lin, rnd} from './kit';

// Short 4 — the famous way (EasyCap) vs his own way (AV->HDMI converter + capture card).
type B = {b?: Record<string, number>};
type C = B & {clip?: number; pos?: string; zoom?: number; clip2?: number; pos2?: string; zoom2?: number};

export const V4Hook: React.FC<B> = () => (
  <Hook title="الطريقة اللي في كل حتة على النت… _مش الأحسن_" />
);

// EasyCap = a cable: RCA in, USB out, straight to the laptop.
export const V4Easy: React.FC<B & {tag?: string}> = ({b, tag = 'الطريقة الأشهر: إيزي كاب'}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const usb = at('usb', 2.5);
  return (
    <Scene>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {[V.red, V.rcaW, V.yellow].map((c, i) => <RcaPlug key={c} x={lin(f, 2, 14, -100, 340)} y={580 + i * 90} color={c} s={2} />)}
        <g opacity={lin(f, 6, 14)}><Box x={560} y={670} w={380} h={260} label="EasyCap" color="#22252E" /></g>
        <Cable a={[750, 670]} b={[820, 1030]} color="#777" p={lin(f, usb, usb + 14)} w={18} flow={1} sag={80} />
        {f >= 10 ? <g opacity={lin(f, 10, 18)}><Laptop x={600} y={1400} s={1.35}><div style={{position: 'absolute', inset: 0, background: V.blue}} /></Laptop></g> : null}
      </svg>
      <Pop at={at('famous', 0.6)} x={540} y={330} rot={-3}><Tag text={tag} bg={V.white} size={58} /></Pop>
      <Pop at={usb + 4} x={280} y={980} rot={-6}><Chip text="AV ➜ USB" bg={V.yellow} size={60} /></Pop>
    </Scene>
  );
};

// The problem: his real capture turns black & white and cuts out. Footage + forced B&W flicker + dropouts.
export const V4Problem: React.FC<C> = ({b, clip = 0, pos = '50% 50%', zoom = 1.04}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const drop = rnd(Math.floor(f / 5) * 3.1) > 0.8;
  const bwOn = rnd(Math.floor(f / 9) * 7.7) > 0.4;
  return (
    <Scene>
      <Pop at={0} x={540} y={640} from={0.8}>
        <Crt w={980} knob={false}>
          <Footage src={CLIP('easy_bw')} start={clip} pos={pos} zoom={zoom} filter={bwOn ? 'grayscale(1) contrast(1.3)' : undefined} />
          {drop ? <AbsoluteFill style={{background: V.blue, display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Rgb size={70} font={EN} dir="ltr">NO SIGNAL</Rgb></AbsoluteFill> : null}
        </Crt>
      </Pop>
      <Pop at={at('bw', 1)} x={330} y={1180} rot={-4}><Tag text="أبيض وأسود" bg={V.white} size={60} /></Pop>
      <Pop at={at('cut', 2.5)} x={760} y={1300} rot={5}><Tag text="وبيفصل كتير" bg={V.red} color={V.white} size={60} /></Pop>
    </Scene>
  );
};

// His way: AV -> HDMI converter -> capture card -> USB.
export const V4Mine: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const k = lin(f, at('go', 0.3), at('go', 0.3) + 50, 0, 7);
  return (
    <Scene>
      <Chain k={k} flow={k >= 7 ? 1 : 0} y0={300} />
      <Pop at={4} x={830} y={150} rot={4}><Tag text="طريقتي" bg={V.yellow} size={66} /></Pop>
    </Scene>
  );
};

// Split screen: EasyCap (B&W, cuts) vs his way (colour, steady, HD).
export const V4Versus: React.FC<C> = ({b, clip = 0, pos = '50% 50%', zoom = 1.04, clip2 = 24, pos2 = '0% 50%', zoom2 = 1.04}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const drop = rnd(Math.floor(f / 6) * 5.3) > 0.82;
  const win = at('win', 3);
  return (
    <Scene>
      <Pop at={0} x={540} y={470} from={0.85}>
        <Crt w={720} knob={false}>
          <Footage src={CLIP('easy_bw')} start={clip} pos={pos} zoom={zoom} bw />
          {drop ? <AbsoluteFill style={{background: '#000'}} /> : null}
        </Crt>
      </Pop>
      <Pop at={6} x={540} y={1110} from={0.85}><Crt w={720} knob={false}><Footage src={CLIP('mine_dvd')} start={clip2} pos={pos2} zoom={zoom2} /></Crt></Pop>
      <Pop at={2} x={130} y={300} rot={-8}><Chip text="EasyCap" size={44} /></Pop>
      <Pop at={8} x={130} y={940} rot={-8}><Chip text="HDMI" bg={V.yellow} size={44} /></Pop>
      <Pop at={at('x', 1.5)} x={930} y={470}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 200, color: V.red, textShadow: '0 8px 0 #000'}}>✕</div></Pop>
      <Pop at={win} x={930} y={1110}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 200, color: V.green, textShadow: '0 8px 0 #000'}}>✓</div></Pop>
      <Pop at={win + 8} x={540} y={1330}><Stamp text="مبتقطعش خالص" at={0} size={84} color={V.green} rot={-4} /></Pop>
      <Flash at={win} color={V.green} len={6} />
    </Scene>
  );
};

// End behind Aly: "a million times better".
export const V4End: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 260, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Title text="أحسن *مليون مرة* من الإيزي كاب" size={90} stroke /></div>
      <Pop at={4} x={540} y={760}><div style={{opacity: blink(f, at('n', 0.8), 10) * 0.4 + 0.6, display: 'flex', direction: 'ltr', alignItems: 'center'}}><Rgb size={170} font={EN} dir="ltr" color={V.yellow}>×</Rgb><Count from={1} to={1000000} a={4} b={at('n', 0.8) + 12} size={170} color={V.yellow} /></div></Pop>
      <svg width={1080} height={1920} style={{position: 'absolute'}}><g opacity={lin(f, 6, 14)}><Cassette x={540} y={1180} s={1.1} rot={-5} spin={f * 6} label="HD ✓" /></g></svg>
    </AbsoluteFill>
  );
};
