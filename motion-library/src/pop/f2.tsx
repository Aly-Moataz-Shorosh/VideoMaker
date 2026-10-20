import React from 'react';
import {Easing, useCurrentFrame} from 'remotion';
import {AR, EN, Pop, lin, spr, useBeats} from '../film/kit';
import {Ball, Cursor, Echo, FileCard, Head, Hud, Logo, MONO, Note, Orbit, P, PScene, Pill, SelBox, Term, Ticker, Typed} from './kit';

// ffmpeg short 2 — "why does ffmpeg.exe open and close at once?" It's a console program that needs an input.
type B = {b?: Record<string, number>};
const Top: React.FC<{text: string; at?: number; y?: number; size?: number}> = ({text, at = 2, y = 190, size = 86}) => (
  <div style={{position: 'absolute', top: y, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Head text={text} at={at} size={size} /></div>
);
const ExeIcon: React.FC<{s?: number}> = ({s = 220}) => (
  <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14}}>
    <div style={{width: s, height: s, background: P.white, border: `6px solid ${P.ink}`, borderRadius: s * 0.16, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: `0 14px 0 ${P.deep}`}}>
      <Logo name="ffmpeg" s={s * 0.7} color="#0B8A1F" />
    </div>
    <div style={{fontFamily: EN, fontWeight: 800, fontSize: s * 0.2, color: P.white, direction: 'ltr'}}>ffmpeg.exe</div>
  </div>
);

// 1. double click -> a black window flashes open and closes
export const F2Flash: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const dbl = at('dbl', 1.0), op = at('open', 3.2), cl = at('close', 3.6);
  const win = f >= op && f < cl + 5 ? (f < cl ? spr(f, 30, op, 300, 16) : 1 - lin(f, cl, cl + 5)) : 0;
  return (
    <PScene>
      <Top text="دبل كليك… _فتح وقفل_ ⚡" at={2} />
      <Pop at={0} x={540} y={780}><ExeIcon s={240} /></Pop>
      <Cursor x={lin(f, 0, dbl - 2, 900, 600)} y={lin(f, 0, dbl - 2, 1300, 800)} click={dbl} />
      {f >= dbl + 4 && f < dbl + 14 ? <div style={{position: 'absolute', left: 640, top: 700, fontFamily: EN, fontWeight: 900, fontSize: 60, color: P.lime}}>×2</div> : null}
      {win > 0 ? (
        <div style={{position: 'absolute', left: 90, top: 520, transform: `scale(${win}, ${win * win})`, transformOrigin: '50% 50%'}}>
          <Term w={900} h={520} size={34}><span style={{color: '#aaa'}}>ffmpeg version N-100898 …{'\n'}usage: ffmpeg [options] [[infile options] -i infile]…</span></Term>
        </div>
      ) : null}
      {f >= cl + 4 ? (
        <>
          <Pop at={cl + 4} x={540} y={1230}><Echo text="?!" size={220} color={P.pink} at={cl + 4} /></Pop>
        </>
      ) : null}
    </PScene>
  );
};

// 2. why? it's not a buttons program, it's a console program
export const F2Why: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const no = at('no', 1.5), btn = at('btn', 2.4), con = at('con', 3.5);
  const x1 = lin(f, btn + 6, btn + 12);
  return (
    <PScene>
      <Top text="ليه؟" at={0} size={120} />
      <Pop at={no - 2} x={540} y={620}>
        <div style={{width: 760, height: 380, background: '#EDEBF7', border: `5px solid ${P.ink}`, boxShadow: `12px 14px 0 ${P.deep}`, padding: 30, direction: 'ltr', position: 'relative'}}>
          <div style={{display: 'flex', gap: 20}}>
            {['Open', 'Export', 'Settings'].map((t, i) => (
              <div key={t} style={{padding: '14px 26px', background: [P.vio, P.pink, P.teal][i], color: P.white, fontFamily: EN, fontWeight: 800, fontSize: 34, borderRadius: 12, border: `4px solid ${P.ink}`}}>{t}</div>
            ))}
          </div>
          <div style={{marginTop: 40, height: 18, background: '#C9C6F2', borderRadius: 9}}><div style={{width: '60%', height: '100%', background: P.vio, borderRadius: 9}} /></div>
          <div style={{marginTop: 30, height: 18, background: '#C9C6F2', borderRadius: 9}}><div style={{width: '35%', height: '100%', background: P.pink, borderRadius: 9}} /></div>
          <svg width={760} height={380} style={{position: 'absolute', left: 0, top: 0}}>
            <path d={`M60,60 L${60 + 640 * x1},${60 + 260 * x1}`} stroke={P.pink} strokeWidth={26} strokeLinecap="round" />
            <path d={`M700,60 L${700 - 640 * x1},${60 + 260 * x1}`} stroke={P.pink} strokeWidth={26} strokeLinecap="round" />
          </svg>
        </div>
      </Pop>
      <Pop at={btn} x={540} y={880}><Pill text="مش برنامج زراير" bg={P.pink} size={56} /></Pop>
      {f >= con ? (
        <>
          <Pop at={con} x={540} y={1180} from={0.6}><Term w={760} h={260} size={40}><Typed text="C:\> _" a={con} b={con + 8} /></Term></Pop>
          <Pop at={con + 6} x={540} y={1400}><Pill text="ده برنامج كونسول ✓" size={60} /></Pop>
        </>
      ) : null}
    </PScene>
  );
};

// 3. console = runs on the black screen, you type commands to it
export const F2Console: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const blk = at('black', 1.3), cmd = at('cmd', 3.3);
  const grow = lin(f, blk, blk + 12, 0, 1, Easing.inOut(Easing.cubic));
  return (
    <PScene>
      <Top text="كونسول يعني ايه؟" at={0} />
      <div style={{position: 'absolute', left: 540 - (300 + 230 * grow), top: 420, width: 600 + 460 * grow, height: 360 + 520 * grow, background: '#07070A',
        border: `6px solid ${P.ink}`, boxShadow: `14px 16px 0 ${P.deep}`, overflow: 'hidden', direction: 'ltr', fontFamily: MONO, fontSize: 40, color: '#E8E8E8', padding: 34, lineHeight: 1.6}}>
        {f >= cmd ? (
          <>
            <div><span style={{color: '#888'}}>C:\&gt;</span><Typed text="ffmpeg -i video.mov video.mp4" a={cmd} b={cmd + 22} color={P.lime} caret={false} /></div>
            {f >= cmd + 24 ? <div style={{color: '#888'}}><Typed text="frame= 60 fps=0.0 size= 90kB" a={cmd + 24} b={cmd + 34} /></div> : null}
          </>
        ) : <div style={{color: '#888'}}>C:\&gt;<span style={{background: Math.floor(f / 8) % 2 ? '#ddd' : 'transparent'}}> </span></div>}
      </div>
      {f >= blk ? <Pop at={blk + 6} x={540} y={1060}><Note text="الشاشة السودا" size={84} rot={-4} /></Pop> : null}
      {f >= cmd ? <Pop at={cmd + 4} x={540} y={1400}><Pill text="بتكتبله أوامر commands ⌨️" size={52} bg={P.white} /></Pop> : null}
    </PScene>
  );
};

// ffmpeg as a little machine with a funnel: it needs an input to work.
const Machine: React.FC<{on: number; off: number; feed?: number; out?: number}> = ({on, off, feed, out}) => {
  const f = useCurrentFrame();
  const light = f >= off ? '#FF3B4E' : f >= on ? P.lime : '#888';
  const shake = f >= on && f < off ? Math.sin(f * 2.4) * 3 : 0;
  return (
    <svg width={1080} height={1100} style={{position: 'absolute', left: 0, top: 420, overflow: 'visible'}}>
      <path d="M380,120 L700,120 L600,300 L480,300 Z" fill={P.white} stroke={P.ink} strokeWidth={8} />
      <text x={540} y={210} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={46} fill={P.vio}>INPUT</text>
      <g transform={`translate(${shake},0)`}>
        <rect x={300} y={300} width={480} height={360} rx={40} fill={P.vio2} stroke={P.ink} strokeWidth={8} />
        <rect x={360} y={360} width={360} height={160} rx={20} fill="#0B0B0E" stroke={P.ink} strokeWidth={6} />
        <text x={540} y={460} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={60} fill={P.lime}>ffmpeg</text>
        <circle cx={380} cy={600} r={28} fill={light} stroke={P.ink} strokeWidth={6} />
        {[0, 1, 2].map((i) => <rect key={i} x={450 + i * 80} y={585} width={60} height={30} rx={8} fill={P.lav} stroke={P.ink} strokeWidth={4} />)}
      </g>
      <path d="M780,520 L900,520 L900,620" fill="none" stroke={P.ink} strokeWidth={22} />
      {feed !== undefined && f >= feed && f < feed + 20 ? (
        <g transform={`translate(${470},${lin(f, feed, feed + 18, -320, 150)}) scale(0.5)`}><rect x={0} y={0} width={140} height={175} fill={P.white} stroke={P.ink} strokeWidth={8} />
          <rect x={14} y={100} width={112} height={50} fill={P.pink} stroke={P.ink} strokeWidth={6} /><text x={70} y={137} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={34}>MOV</text></g>
      ) : null}
      {out !== undefined && f >= out ? (
        <g transform={`translate(${840},${lin(f, out, out + 14, 560, 720)}) scale(0.5)`}><rect x={0} y={0} width={140} height={175} fill={P.white} stroke={P.ink} strokeWidth={8} />
          <rect x={14} y={100} width={112} height={50} fill={P.lime} stroke={P.ink} strokeWidth={6} /><text x={70} y={137} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={34}>MP4</text></g>
      ) : null}
    </svg>
  );
};

// 4. it needs an input to work on -> nothing given -> it opens and closes
export const F2Input: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const why = at('why', 4), inp = at('input', 5.9), none = at('none', 7.7), cl = at('close', 10);
  return (
    <PScene>
      <Top text={f < inp ? 'بس قفل بسرعة… _ليه؟_' : 'مستني *input* يشتغل عليه'} at={f < inp ? why : inp} size={80} />
      <Machine on={0} off={cl} />
      <SelBox x={370} y={530} w={340} h={190} at={inp} label="INPUT" dash />
      {f >= none ? <Pop at={none} x={540} y={1200} rot={-4}><Note text="فاضي… مفيش حاجة" size={58} color={P.yellow} /></Pop> : null}
      {f >= cl ? <Pop at={cl} x={540} y={1400}><Pill text="يفتح ← يقفل 🔁" size={60} bg={P.pink} /></Pop> : null}
    </PScene>
  );
};

// 5. I want to GIVE it an input -> the video goes in, mp4 comes out
export const F2Give: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const no = at('no', 1.5), give = at('give', 3.4);
  return (
    <PScene>
      <Top text="الحل: *ادّيله* الفيديو" at={give - 6} size={84} />
      <Machine on={give + 14} off={99999} feed={give} out={give + 22} />
      {f < give ? <Pop at={0} x={540} y={1420}><Pill text="مش عايز يفتح ويقفل ✗" size={52} bg={P.pink} /></Pop> : null}
      {f >= give + 26 ? <Pop at={give + 26} x={540} y={1420}><Pill text="اشتغل ✓" size={64} /></Pop> : null}
    </PScene>
  );
};

// 6. "-i" = input — the letter in the command
export const F2I: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const i = at('i', 0.6), inn = at('in', 1.7);
  return (
    <PScene>
      <Pop at={0} x={540} y={560} from={0.8}><Term w={960} h={260} size={44}><span>ffmpeg </span><span style={{color: P.lime, background: f >= i ? 'rgba(184,255,60,0.25)' : undefined}}>-i</span><span style={{color: P.yellow}}> "video.mov"</span></Term></Pop>
      {f >= i ? <Pop at={i} x={540} y={960}><Echo text="-i" size={300} color={P.lime} at={i} /></Pop> : null}
      {f >= inn ? <Pop at={inn} x={540} y={1260}><Echo text="= INPUT" size={130} color={P.white} at={inn} /></Pop> : null}
      <Orbit cx={540} cy={960} rx={260} ry={150} at={i + 4} />
    </PScene>
  );
};
