import React from 'react';
import {Easing, useCurrentFrame} from 'remotion';
import {AR, EN, Pop, lin, spr, useBeats} from '../film/kit';
import {Ball, Cursor, Echo, FileCard, Head, Hud, Key, Logo, MONO, Note, Orbit, P, PScene, Pill, SelBox, Term, Ticker, Typed} from './kit';

// ffmpeg v2 (Aly 2026-10-14: ONE short with the whole tutorial) — the steps the split shorts were missing.
type B = {b?: Record<string, number>};
const Top: React.FC<{text: string; at?: number; y?: number; size?: number}> = ({text, at = 2, y = 190, size = 84}) => (
  <div style={{position: 'absolute', top: y, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Head text={text} at={at} size={size} /></div>
);
const Step: React.FC<{n: number}> = ({n}) => {
  const f = useCurrentFrame();
  const p = spr(f, 30, 0);
  return (
    <div style={{position: 'absolute', right: 64, top: 110, transform: `scale(${p})`, background: P.ink, color: P.lime, fontFamily: EN, fontWeight: 900, fontSize: 34,
      padding: '6px 20px', direction: 'ltr', border: `3px solid ${P.lime}`}}>STEP {n}</div>
  );
};
const BUILDS = ['ffmpeg-N-100898-gd16b0a4bf0-win64-gpl-shared-vulkan.zip', 'ffmpeg-N-100898-win64-gpl-vulkan.zip', 'ffmpeg-N-100898-win64-lgpl-shared.zip', 'ffmpeg-N-100898-win64-lgpl.zip'];

// GitHub page with the Windows builds -> take any link
export const F4Github: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const gh = at('gh', 3.2), any = at('any', 7.5);
  return (
    <PScene>
      <Top text={f < any ? 'هيفتح موقع *GitHub*' : 'خد *أي* لينك منهم'} at={f < any ? 2 : any} />
      <Pop at={gh} x={540} y={420}><div style={{width: 160, height: 160, borderRadius: '50%', background: P.white, border: `5px solid ${P.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <Logo name="github" s={120} color={P.ink} /></div></Pop>
      <Orbit cx={540} cy={420} rx={170} ry={70} at={gh + 3} />
      <Pop at={1} x={540} y={900} from={0.8}>
        <div style={{width: 960, background: '#0D1117', border: `5px solid ${P.ink}`, boxShadow: `14px 16px 0 ${P.deep}`, padding: 30, direction: 'ltr', fontFamily: EN}}>
          <div style={{fontSize: 34, color: '#E6EDF3', fontWeight: 800}}>FFmpeg Builds · Windows · Assets</div>
          {BUILDS.map((n, i) => (
            <div key={n} style={{marginTop: 18, display: 'flex', alignItems: 'center', gap: 16, fontSize: 28, color: '#58A6FF', opacity: lin(f, 4 + i * 3, 9 + i * 3),
              background: f >= any && i === 0 ? 'rgba(184,255,60,0.18)' : undefined, padding: '6px 10px'}}>📦 {n}</div>
          ))}
        </div>
      </Pop>
      {f >= any ? <SelBox x={70} y={740} w={940} h={66} at={any} label="any" tagBelow /> : null}
      <Cursor x={lin(f, any - 12, any - 2, 900, 600)} y={lin(f, any - 12, any - 2, 1400, 780)} click={any} />
    </PScene>
  );
};

// download the first one
export const F4Zip: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const first = at('first', 2.3), dl = at('dl', 6.8);
  const prog = lin(f, dl, dl + 18, 0, 1, (x) => x);
  return (
    <PScene>
      <Top text="نزّل *أول واحد*" at={1} />
      <Pop at={first} x={540} y={720}>
        <div style={{width: 260, height: 300, background: P.yellow, border: `6px solid ${P.ink}`, borderRadius: 18, position: 'relative', boxShadow: `0 16px 0 ${P.deep}`}}>
          {Array.from({length: 7}, (_, i) => <div key={i} style={{position: 'absolute', left: 116 + (i % 2) * 14, top: 16 + i * 26, width: 14, height: 14, background: P.ink}} />)}
          <div style={{position: 'absolute', bottom: 24, left: 0, right: 0, textAlign: 'center', fontFamily: EN, fontWeight: 900, fontSize: 50}}>ZIP</div>
        </div>
      </Pop>
      <Pop at={first + 4} x={540} y={950}><div style={{fontFamily: MONO, fontSize: 30, color: P.white, direction: 'ltr'}}>{BUILDS[0]}</div></Pop>
      {f >= dl - 8 ? (
        <Pop at={dl - 8} x={540} y={1120}>
          <div style={{width: 640, height: 110, background: '#5CB85C', border: `5px solid ${P.ink}`, borderRadius: 14, display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontFamily: EN, fontWeight: 900, fontSize: 52, color: P.white, transform: `scale(${f >= dl && f < dl + 6 ? 0.94 : 1})`}}>⬇ Download</div>
        </Pop>
      ) : null}
      {f >= dl ? (
        <div style={{position: 'absolute', left: 220, top: 1260, width: 640, height: 34, background: P.lav, border: `4px solid ${P.ink}`}}>
          <div style={{width: `${prog * 100}%`, height: '100%', background: P.lime}} />
        </div>
      ) : null}
      <Cursor x={lin(f, first, dl - 3, 950, 640)} y={lin(f, first, dl - 3, 1400, 1140)} click={dl} />
    </PScene>
  );
};

// unzip -> open the folder -> folders inside
export const F4Folder: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const open = at('open', 3.6), find = at('find', 5.9);
  const sub = ['bin', 'doc', 'include', 'lib', 'share'];
  return (
    <PScene>
      <Top text={f < find ? 'فك الضغط وافتح الفولدر' : 'هتلاقي فيه *فولدرات*'} at={f < find ? 1 : find} />
      <Pop at={0} x={330} y={640}>
        <div style={{width: 200, height: 230, background: P.yellow, border: `6px solid ${P.ink}`, borderRadius: 16, transform: `rotate(${-8 + 8 * lin(f, open - 10, open)}deg)`,
          opacity: 1 - lin(f, open, open + 8)}}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 44, textAlign: 'center', marginTop: 150}}>ZIP</div></div>
      </Pop>
      <Pop at={4} x={760} y={640}><Echo text="→" size={150} color={P.lime} at={4} /></Pop>
      <Pop at={open - 6} x={760} y={640}>
        <svg width={260} height={200} viewBox="0 0 130 100"><path d="M5,20 L45,20 L55,30 L125,30 L125,95 L5,95 Z" fill="#E8A92B" stroke={P.ink} strokeWidth={3} />
          <path d="M5,50 L125,50 L125,95 L5,95 Z" fill={P.yellow} stroke={P.ink} strokeWidth={3} /></svg>
      </Pop>
      {sub.map((n, i) => {
        if (f < find + i * 3) return null;
        const hi = n === 'bin';
        return (
          <Pop key={n} at={find + i * 3} x={150 + i * 195} y={1060}>
            <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8}}>
              <svg width={140} height={108} viewBox="0 0 130 100"><path d="M5,20 L45,20 L55,30 L125,30 L125,95 L5,95 Z" fill={hi ? P.lime : '#E8A92B'} stroke={P.ink} strokeWidth={4} /></svg>
              <div style={{fontFamily: EN, fontWeight: 800, fontSize: 36, color: P.white}}>{n}</div>
            </div>
          </Pop>
        );
      })}
      {f >= find + 16 ? <Pop at={find + 16} x={150} y={1270}><Note text="ده المهم 👆" size={56} /></Pop> : null}
    </PScene>
  );
};

// drag ffmpeg.exe into CMD instead of typing its long path
export const F4DragExe: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const drag = at('drag', 4.6), drop = at('drop', 5.9);
  const px = lin(f, drag, drop, 0, 1, Easing.inOut(Easing.cubic));
  const x = 540, y = lin(f, drag, drop, 1240, 640);
  return (
    <PScene>
      <Top text="*اسحب* البرنامج جوّه" at={1} />
      <Pop at={0} x={540} y={600} from={0.9}>
        <Term w={980} h={420} size={36}>
          <span style={{color: '#9A9A9A'}}>C:\…\bin&gt;</span>
          {f >= drop ? <Typed text="C:\Users\pc\Downloads\ffmpeg-N-100898-win64-gpl-shared-vulkan\bin\ffmpeg.exe" a={drop} b={drop + 10} color={P.white} /> : null}
        </Term>
      </Pop>
      {f < drop + 2 ? (
        <div style={{position: 'absolute', left: x - 90, top: y - 90, width: 180, height: 180, background: P.white, border: `5px solid ${P.ink}`, borderRadius: 30,
          display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${1 - 0.4 * px})`, opacity: 1 - lin(f, drop - 1, drop + 2)}}><Logo name="ffmpeg" s={120} color="#0B8A1F" /></div>
      ) : null}
      <Cursor x={x + 40} y={y + 40} />
      {f >= drop + 8 ? <Pop at={drop + 8} x={540} y={1100}><Pill text="بدل ما تكتب اللينك بتاعه ✓" size={54} /></Pop> : null}
      {f >= drop + 14 ? <Pop at={drop + 14} x={540} y={1300}><Note text="اللينك الطويل اتكتب لوحده" size={62} color={P.yellow} /></Pop> : null}
    </PScene>
  );
};

// the whole command, piece by piece
export const F4Anatomy: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const prog = at('prog', 2.9), ii = at('i', 5.1), vid = at('vid', 7.8), inn = at('inn', 12), out = at('out', 12.4), same = at('same', 14);
  const parts: [string, string, string, number][] = [
    ['ffmpeg.exe', 'البرنامج', P.white, prog], ['-i', 'input', P.lime, ii], ['"bee circle 2.mov"', 'الفيديو الأصلي', P.yellow, vid], ['"…FFMPEG.mp4"', 'الأوتبوت', P.teal, out],
  ];
  return (
    <PScene>
      <Top text="الأمر كله *حتة حتة*" at={0} />
      {parts.map(([code, ar, c, a], i) => {
        if (f < a) return null;
        const p = spr(f, 30, a);
        return (
          <div key={i} style={{position: 'absolute', left: 90, right: 90, top: 380 + i * 250, height: 200, display: 'flex', alignItems: 'center', gap: 30, direction: 'ltr',
            transform: `translateX(${(1 - p) * -300}px)`, opacity: Math.min(1, p * 2)}}>
            <div style={{width: 80, height: 80, borderRadius: '50%', background: c, border: `4px solid ${P.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontFamily: EN, fontWeight: 900, fontSize: 44, color: P.ink}}>{i + 1}</div>
            <div style={{flex: 1, background: '#0B0B0E', border: `5px solid ${P.ink}`, boxShadow: `10px 10px 0 ${P.deep}`, padding: '20px 28px'}}>
              <div style={{fontFamily: MONO, fontSize: 46, color: c, whiteSpace: 'nowrap'}}>{code}</div>
              <div style={{fontFamily: AR, fontWeight: 900, fontSize: 40, color: P.white, direction: 'rtl', textAlign: 'right'}}>{ar}</div>
            </div>
          </div>
        );
      })}
      {f >= same ? <Pop at={same} x={540} y={1430}><Pill text="نفس المكان… ونفس الاسم؟ 🤔" size={52} bg={P.pink} /></Pop> : null}
    </PScene>
  );
};

// same name is not allowed -> rename: add FFMPEG
export const F4Rename: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const ren = at('ren', 1.0), ff = at('ff', 1.9);
  return (
    <PScene>
      <Top text="غيّر *اسم* الأوتبوت" at={0} />
      <Pop at={0} x={540} y={700}>
        <div style={{fontFamily: MONO, fontSize: 58, color: P.white, direction: 'ltr', background: '#0B0B0E', padding: '24px 36px', border: `5px solid ${P.ink}`, whiteSpace: 'nowrap'}}>
          "bee circle {f >= ff ? <span style={{color: P.lime, background: 'rgba(184,255,60,0.2)'}}>FFMPEG</span> : <span style={{color: P.pink}}>2</span>}.mp4"
        </div>
      </Pop>
      {f < ff ? <Pop at={ren - 6} x={540} y={980}><Pill text="نفس الاسم ميفعش ✗" size={56} bg={P.pink} /></Pop> : <Pop at={ff} x={540} y={980}><Pill text="اسم جديد ✓" size={60} /></Pop>}
    </PScene>
  );
};

// on a 5 MB file you won't feel it — on 100 MB files you will
export const F4Big: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const five = at('five', 3.1), hund = at('hund', 8.8);
  const h = lin(f, hund, hund + 16, 0, 1, Easing.out(Easing.cubic));
  return (
    <PScene>
      <Top text={f < hund ? 'هنا الفرق _مش باين_ قوي' : 'بس في الفيديوهات *الكبيرة*…'} at={f < hund ? 1 : hund} />
      <Pop at={five} x={300} y={1000}><FileCard ext="MOV" name="5 MB" w={200} color={P.pink} /></Pop>
      {f >= hund ? (
        <>
          <div style={{position: 'absolute', left: 560, bottom: 560, width: 180, height: 760 * h, background: P.pink, border: `5px solid ${P.ink}`}} />
          <div style={{position: 'absolute', left: 780, bottom: 560, width: 180, height: 120 * h, background: P.lime, border: `5px solid ${P.ink}`}} />
          <Pop at={hund + 6} x={650} y={1400}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 56, color: P.white}}>100 MB</div></Pop>
          <Pop at={hund + 12} x={870} y={1400}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 56, color: P.lime}}>↓↓</div></Pop>
          <Pop at={hund + 16} x={300} y={1300} rot={-6}><Note text="هتحس قوي" size={70} /></Pop>
        </>
      ) : null}
    </PScene>
  );
};

// done fast (small file)
export const F4Done: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const done = at('done', 0.2);
  const p = lin(f, done, done + 30, 0, 1, (x) => x);
  return (
    <PScene>
      <Top text="خلص *بسرعة* ⚡" at={done} size={96} />
      <div style={{position: 'absolute', left: 140, top: 760, width: 800, height: 60, background: P.lav, border: `5px solid ${P.ink}`}}>
        <div style={{width: `${p * 100}%`, height: '100%', background: P.lime}} />
      </div>
      <div style={{position: 'absolute', top: 860, left: 0, right: 0, textAlign: 'center', fontFamily: MONO, fontSize: 44, color: P.white, direction: 'ltr'}}>{Math.round(p * 100)}%</div>
      {p >= 1 ? <Pop at={done + 30} x={540} y={1100}><Pill text="Done ✓" dir="ltr" font={EN} size={80} /></Pop> : null}
    </PScene>
  );
};

// the new video appears next to the old one
export const F4New: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const nm = at('name', 1.6);
  return (
    <PScene>
      <Top text="ده الفيديو *الجديد*" at={0} />
      <Pop at={0} x={300} y={800}><FileCard ext="MOV" name="bee circle 2.mov" w={240} color={P.pink} /></Pop>
      <Pop at={6} x={780} y={800}><FileCard ext="MP4" name="bee circle FFMPEG.mp4" w={240} color={P.lime} /></Pop>
      <SelBox x={640} y={600} w={280} h={420} at={nm} label="NEW" />
      <Pop at={10} x={540} y={420}><div style={{transform: `translateY(${8 * Math.sin(f / 7)}px)`}}><Ball d={120} id="nw" /></div></Pop>
    </PScene>
  );
};
