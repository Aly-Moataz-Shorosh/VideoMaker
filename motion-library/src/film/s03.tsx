import React from 'react';
import {AbsoluteFill, Img, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, OLD, K, Clip, Halftone, Paper, Photo, Pop, Scene, Stamp, Tag, Title, img, lin, spr, useBeats, rnd} from './kit';
import {Obscura, Palm, Pyramid, Sun} from './draw';
import {Person} from '../blocks/geo';
import {Hook} from './s02';

// Short 3 — trapping light: chemicals instead of the wall -> the picture stays -> photography is born.
const PJ = 'projects/2026-10-08 shorts theodesy/';
type B = {b?: Record<string, number>};

export const S3Hook: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  return (
    <Hook b={b} n={3} title="إزاي الإنسان *حبس* الضوء لأول مرة؟" side={
      <div style={{position: 'absolute', left: 60, top: 820, width: 260, height: 260, borderRadius: 130, background: K.yellow, opacity: lin(f, 18, 30),
        boxShadow: `0 0 ${60 + 30 * Math.sin(f / 5)}px ${K.yellow}`, border: `8px solid ${K.ink}`}}>
        <div style={{position: 'absolute', inset: -30, border: `10px dashed ${K.white}`, borderRadius: '50%', transform: `rotate(${f * 2}deg)`}} />
      </div>
    } />
  );
};

// Same camera obscura, but the wall becomes a chemical plate; the picture burns into it and stays.
export const S3Swap: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const plate = lin(f, at('plate', 0.2), at('plate', 0.2) + 14);
  const burn = lin(f, at('hit', 7.9), at('hit', 7.9) + 90, 0, 1, (x) => x);
  const stay = at('stay', 11);
  return (
    <Scene bg="#14110E">
      <Obscura w={1080} h={1920} box={1} hole={1} rays={lin(f, at('hit', 7.9) - 20, at('hit', 7.9) + 10)} image={0.25 + 0.75 * burn} plate={plate} burn={burn} />
      {/* chemistry bottles pouring */}
      {f >= at('chem', 2.5) ? (
        <svg width={1080} height={1920} style={{position: 'absolute'}}>
          {[0, 1, 2].map((i) => {
            const k = spr(f, 30, at('chem', 2.5) + i * 5, 160, 12);
            const x = 640 + i * 120, y = 330;
            return (
              <g key={i} transform={`translate(${x},${y}) rotate(${-40 * k}) scale(${k})`}>
                <path d="M-30,-70 L30,-70 L30,-30 L60,40 L-60,40 L-30,-30 Z" fill={[K.cyan, K.yellow, '#B9C4CC'][i]} stroke="#141210" strokeWidth={6} opacity={0.9} />
                <rect x={-20} y={-95} width={40} height={26} fill="#141210" />
              </g>
            );
          })}
        </svg>
      ) : null}
      <Pop at={at('chem', 2.5) + 6} x={760} y={520} rot={3}><Tag text="مواد كيميائية" size={52} /></Pop>
      <Pop at={at('sens', 5.8)} x={760} y={1340} rot={-3}><Tag text="حساسة للضوء" bg={K.yellow} size={58} /></Pop>
      <Pop at={at('change', 8.9)} x={300} y={1180} rot={4}><Tag text="تغيّر لونها" bg={K.red} color={K.white} size={52} /></Pop>
      <div style={{position: 'absolute', left: 300, top: 1420}}><Stamp text="وتفضل كده على طول" at={stay} size={60} rot={-6} color={K.yellow} /></div>
    </Scene>
  );
};

// Real wet-plate footage -> a framed old photograph; "projection" + "saving"; any time.
export const S3Keep: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tSave = at('save', 8.9), tAny = at('any', 11.5);
  const showPhoto = f >= at('photo', 5.5);
  return (
    <Scene bg={K.ink}>
      {!showPhoto ? (
        <Pop at={0} x={540} y={820} rot={2} from={0.85}>
          <Clip src={PJ + 'broll/b6_wetplate.mp4'} start={4.5} w={880} h={1150} seed={31} />
        </Pop>
      ) : (
        <Pop at={at('photo', 5.5)} x={540} y={760} rot={-3} from={0.6}>
          <div style={{padding: 34, background: 'linear-gradient(135deg,#6B4E2A,#C9A66B,#6B4E2A)', borderRadius: 12, boxShadow: '0 30px 60px rgba(0,0,0,0.7)'}}>
            <div style={{width: 560, height: 700, background: '#1E1A15', overflow: 'hidden', borderRadius: '45% 45% 8px 8px / 30% 30% 8px 8px', position: 'relative'}}>
              <svg width={560} height={700} viewBox="0 330 640 700" style={{filter: 'grayscale(1) sepia(0.6) contrast(1.1)'}}>
                <rect x={0} y={330} width={640} height={700} fill="#CDBB98" />
                <Palm x={170} y={900} s={1.2} /><Pyramid x={380} y={900} s={1.1} /><Sun x={520} y={460} r={40} />
                <rect x={0} y={900} width={640} height={200} fill="#8E7B5A" />
              </svg>
              <Halftone color="#000" size={6} dot={0.25} opacity={0.2} />
            </div>
          </div>
        </Pop>
      )}
      <Pop at={at('proj', 1.5)} out={tSave - 2} x={330} y={240} rot={-3}><Tag text="إسقاط ✓" size={56} /></Pop>
      <Pop at={tSave} x={720} y={240} rot={4}><Tag text="+ حفظ (Saving)" bg={K.yellow} size={58} /></Pop>
      {f >= tAny ? (
        <div style={{position: 'absolute', left: 390, top: 1250, width: 300, height: 300}}>
          <svg width={300} height={300}>
            <circle cx={150} cy={150} r={130} fill={K.paper} stroke="#141210" strokeWidth={10} />
            <line x1={150} y1={150} x2={150 + 90 * Math.sin((f - tAny) / 3)} y2={150 - 90 * Math.cos((f - tAny) / 3)} stroke="#141210" strokeWidth={10} strokeLinecap="round" />
            <line x1={150} y1={150} x2={150 + 60 * Math.sin((f - tAny) / 36)} y2={150 - 60 * Math.cos((f - tAny) / 36)} stroke={K.red} strokeWidth={12} strokeLinecap="round" />
          </svg>
          <div style={{position: 'absolute', top: 300, width: 300, textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 52, color: K.white}}>في أي وقت</div>
        </div>
      ) : null}
    </Scene>
  );
};

// Grandparents -> me -> grandchildren: the same photo travels through time.
export const S3Gens: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const at = useBeats(b);
  const tA = at('ancestors', 4.6), tK = at('kids', 6.9);
  const who = [{x: 200, label: 'أجدادي', yr: '1850', at: tA - 10, s: 1.05, c: K.paper2}, {x: 540, label: 'أنا', yr: '2026', at: 4, s: 1.1, c: K.yellow},
    {x: 880, label: 'أحفادي', yr: '2100', at: tK - 4, s: 0.85, c: K.cyan}];
  const hold = f < tA ? 1 : f < tK ? 0 : 2;
  const px = [200, 540, 880][hold === 1 ? 1 : hold === 0 ? 0 : 2];
  const k = spr(f, fps, hold === 0 ? tA : hold === 2 ? tK : 0, 90, 14);
  return (
    <Scene bg="#191612">
      <Halftone color="#fff" size={18} dot={0.1} opacity={0.05} />
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <line x1={80} y1={1230} x2={1000} y2={1230} stroke={K.paper} strokeWidth={6} strokeDasharray="20 14" />
        <path d="M1000,1230 l-30,-18 l0,36 Z" fill={K.paper} transform="rotate(180 1000 1230) translate(-920,0)" />
        {who.map((w, i) => f >= w.at ? (
          <g key={i} opacity={lin(f, w.at, w.at + 8)}><Person x={w.x} y={1180} s={210 * w.s} color={w.c} look={i === 0 ? 0.5 : i === 2 ? -0.5 : 0} /></g>
        ) : null)}
      </svg>
      {who.map((w, i) => f >= w.at ? (
        <React.Fragment key={i}>
          <Pop at={w.at + 4} x={w.x} y={1310}><Tag text={w.label} size={50} bg={w.c} /></Pop>
          <Pop at={w.at + 8} x={w.x} y={1400}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 46, color: K.dim}}>{w.yr}</div></Pop>
        </React.Fragment>
      ) : null)}
      {/* the photo moves to whoever is looking at it */}
      <div style={{position: 'absolute', left: (hold === 0 ? 540 + (200 - 540) * k : hold === 2 ? 200 + (880 - 200) * k : px) - 110, top: 560 - Math.sin(k * Math.PI) * 120,
        transform: `rotate(${(rnd(hold) - 0.5) * 16}deg)`}}>
        <Paper w={220} h={270} seed={44} color={K.white}>
          <div style={{position: 'absolute', inset: 14, background: '#CDBB98', overflow: 'hidden'}}>
            <svg width={192} height={242} viewBox="0 330 640 700" style={{filter: 'sepia(0.6)'}}><Palm x={170} y={900} s={1.2} /><Pyramid x={380} y={900} s={1.1} /></svg>
          </div>
        </Paper>
      </div>
      <div style={{position: 'absolute', top: 200, left: 60, right: 60, display: 'flex', justifyContent: 'center'}}>
        <Title text="نفس الصورة… *أجيال* بتشوفها" size={80} at={2} />
      </div>
    </Scene>
  );
};

// Behind Aly: "a miracle in itself".
export const S3Miracle: React.FC<B> = ({b}) => {
  const at = useBeats(b);
  return (
    <AbsoluteFill>
      <Pop at={at('word', 1.4)} x={540} y={340} rot={-4} from={0.2}>
        <div style={{fontFamily: OLD, fontSize: 250, color: K.yellow, textShadow: '0 10px 0 #000', lineHeight: 1}}>إعجاز</div>
      </Pop>
    </AbsoluteFill>
  );
};

// Inventors kept improving: real big-format camera footage, then a ghost image sharpening on a sensitive sheet.
export const S3Develop: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tSheet = at('sheet', 8), tGhost = at('ghost', 11.2);
  const sharp = lin(f, tGhost, tGhost + 60);
  return (
    <Scene bg={K.ink}>
      {f < tSheet ? (
        <>
          <Pop at={0} x={540} y={800} rot={-2} from={0.85}><Clip src={PJ + 'broll/b3_bigcam.mp4'} start={8} w={880} h={1180} seed={33} /></Pop>
          <Pop at={10} x={540} y={240} rot={3}><Tag text="مواد كتير… وتطوير كتير" size={56} /></Pop>
        </>
      ) : (
        <>
          <Pop at={tSheet} x={540} y={780} from={0.7}>
            <div style={{width: 760, height: 980, background: '#B8BEC4', borderRadius: 8, position: 'relative', overflow: 'hidden', boxShadow: '0 30px 60px rgba(0,0,0,0.6)'}}>
              <svg width={760} height={980} viewBox="0 330 640 820" style={{filter: `blur(${(1 - sharp) * 14}px)`, opacity: 0.15 + 0.85 * sharp}}>
                <Palm x={170} y={900} s={1.2} /><Pyramid x={400} y={900} s={1.2} />
              </svg>
              <Halftone color="#000" size={7} dot={0.22} opacity={0.2} />
            </div>
          </Pop>
          <Pop at={tSheet + 6} x={540} y={240} rot={-3}><Tag text="حاجة حساسة للضوء" bg={K.yellow} size={58} /></Pop>
          <Pop at={tGhost + 8} x={540} y={1370} rot={3}><Tag text="خيالات… شبه الصورة" size={56} /></Pop>
        </>
      )}
    </Scene>
  );
};

// Behind Aly at the end: "the beginning of photography" + 1826.
export const S3Born: React.FC<B> = ({b}) => {
  const at = useBeats(b);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 210, left: 60, right: 60, display: 'flex', justifyContent: 'center'}}>
        <Title text="بداية *الفوتوغرافيا*" size={110} at={at('word', 0.3)} stroke />
      </div>
      <div style={{position: 'absolute', left: 120, top: 470}}><Stamp text="أول صورة: 1826" at={at('year', 1.2)} size={66} rot={-7} color={K.yellow} /></div>
    </AbsoluteFill>
  );
};
