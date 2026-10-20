import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, K, Clip, Halftone, Paper, Pop, Scene, Stamp, Strip, Tag, Title, lin, rnd, spr, useBeats} from './kit';
import {Hook} from './s02';

// Short 9 — The Odyssey was edited with scissors: digital edit -> list of cut numbers -> a person cuts the negative by hand.
const PJ = 'projects/2026-10-08 shorts theodesy/';
type B = {b?: Record<string, number>};

const Scissors: React.FC<{x: number; y: number; s?: number; open: number}> = ({x, y, s = 1, open}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    {[1, -1].map((d) => (
      <g key={d} transform={`rotate(${d * open * 18})`}>
        <path d={`M0,0 L160,${d * -10} L170,0 Z`} fill="#D9D9D9" stroke="#111" strokeWidth={5} />
        <circle cx={-60} cy={d * 34} r={34} fill="none" stroke={K.red} strokeWidth={16} />
        <line x1={0} y1={0} x2={-34} y2={d * 22} stroke={K.red} strokeWidth={16} />
      </g>
    ))}
    <circle r={8} fill="#111" />
  </g>
);

export const S9Hook: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  return (
    <Hook b={b} n={9} title="الأوديسة اتمنتجت *بالمقص*!" side={
      <svg width={1080} height={1920} style={{position: 'absolute'}}><g opacity={lin(f, 14, 24)}><Scissors x={200} y={900} s={1.1} open={0.5 + 0.5 * Math.sin(f / 3)} /></g></svg>
    } />
  );
};

// Old-school editing: real footage of cutting & splicing film by hand.
export const S9Old: React.FC<B> = ({b}) => {
  const at = useBeats(b);
  return (
    <Scene bg={K.ink}>
      <Pop at={0} x={540} y={800} rot={2} from={0.85}><Clip src={PJ + 'broll/b1_edit.mp4'} start={2} w={880} h={1220} seed={91} /></Pop>
      <Pop at={4} x={540} y={220} rot={-3}><Tag text="مونتاج أفلام زمان" size={58} /></Pop>
      <Pop at={at('cut', 6.9)} x={250} y={1300} rot={-6}><Tag text="✂ قص يدوي" bg={K.yellow} size={56} /></Pop>
      <Pop at={at('glue', 9.7)} x={800} y={1380} rot={6}><Tag text="ولزق يدوي" bg={K.red} color={K.white} size={56} /></Pop>
    </Scene>
  );
};

// Nolan's pipeline: film -> digital -> edit on a computer -> list of cut numbers.
export const S9How: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const at = useBeats(b);
  const tDig = at('digital', 6.5), tPc = at('pc', 8.3), tNums = at('nums', 11.3);
  const step = (a: number) => spr(f, fps, a, 160, 14);
  const codes = ['00:12:04:17  →  00:12:09:02', '00:12:09:03  →  00:12:15:21', '00:12:15:22  →  00:12:18:10', '00:12:18:11  →  00:12:26:05',
    '00:12:26:06  →  00:12:31:14', '00:12:31:15  →  00:12:40:00'];
  return (
    <Scene bg="#121315">
      <div style={{position: 'absolute', top: 180, left: 60, right: 60, display: 'flex', justifyContent: 'center'}}>
        <Title text="فيلم بالحجم ده… يتمنتج *إزاي*؟" size={84} at={2} />
      </div>
      {/* film -> scanner */}
      <div style={{position: 'absolute', left: 60, top: 470, transform: `scale(${step(10)})`}}>
        <Strip vertical frames={[PJ + 'img/poster.jpg', PJ + 'img/poster.jpg']} fw={160} fh={120} />
      </div>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <path d="M290,600 L400,600" stroke={K.yellow} strokeWidth={10} markerEnd="" opacity={step(tDig)} />
        <path d="M385,580 L410,600 L385,620" stroke={K.yellow} strokeWidth={10} fill="none" opacity={step(tDig)} />
      </svg>
      {/* laptop with a timeline */}
      <div style={{position: 'absolute', left: 430, top: 440, transform: `scale(${step(tPc - 8)})`, transformOrigin: '0 0'}}>
        <div style={{width: 560, height: 340, background: '#1E2126', border: `10px solid #3A3D42`, borderRadius: 16, padding: 18, position: 'relative', overflow: 'hidden'}}>
          {Array.from({length: 4}, (_, r) => (
            <div key={r} style={{position: 'absolute', left: 18, top: 40 + r * 64, height: 46, width: 1200, transform: `translateX(${-(f * 3) % 300}px)`, display: 'flex', gap: 6}}>
              {Array.from({length: 12}, (_, i) => <div key={i} style={{width: 60 + rnd(r * 13 + i) * 90, height: 46, borderRadius: 6,
                background: [K.cyan, K.yellow, '#D6338A', '#7BD389'][r]}} />)}
            </div>
          ))}
          <div style={{position: 'absolute', left: 260, top: 20, bottom: 20, width: 4, background: K.red}} />
        </div>
        <div style={{width: 640, height: 26, marginLeft: -40, background: '#3A3D42', borderRadius: '0 0 18px 18px'}} />
      </div>
      <Pop at={tDig} x={300} y={820} rot={-4}><Tag text="يحوّلوه ديجيتال" size={50} /></Pop>
      <Pop at={tPc + 4} x={720} y={880} rot={3}><Tag text="مونتاج على الكمبيوتر" bg={K.cyan} size={50} /></Pop>
      {/* printed cut list */}
      {f >= tNums ? (
        <div style={{position: 'absolute', left: 170, top: 1000, width: 740, transform: `translateY(${lin(f, tNums, tNums + 20, -60, 0)}px)`}}>
          <Paper w={740} h={Math.min(560, 70 + (f - tNums) * 16)} seed={93} color={K.white}>
            <div style={{padding: '24px 36px', fontFamily: 'Consolas, monospace', fontSize: 38, color: K.ink, direction: 'ltr'}}>
              <div style={{fontFamily: AR, fontWeight: 900, fontSize: 44, direction: 'rtl', marginBottom: 10}}>أرقام القطعات</div>
              {codes.map((c, i) => f >= tNums + 6 + i * 6 ? <div key={i}>{c}</div> : null)}
            </div>
          </Paper>
        </div>
      ) : null}
    </Scene>
  );
};

// Behind Aly: "does the computer cut it by itself?" -> NO!
export const S9Robot: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tNo = at('no', 5.3);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 0, right: 0, top: 150, display: 'flex', justifyContent: 'center', opacity: f < tNo ? 1 : 0.25}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 24}}>
          <div style={{fontSize: 150}}>🤖</div>
          <div style={{fontSize: 120}}>✂️</div>
          <div style={{fontFamily: EN, fontWeight: 900, fontSize: 160, color: K.yellow}}>?</div>
        </div>
      </div>
      <Pop at={10} out={tNo - 4} x={540} y={420}><Tag text="الكمبيوتر يقص لوحده؟" size={56} /></Pop>
      <div style={{position: 'absolute', left: 0, right: 0, top: 280, display: 'flex', justifyContent: 'center'}}>
        <Stamp text="لا!" at={tNo} size={230} rot={-10} />
      </div>
    </AbsoluteFill>
  );
};

// A person finds the exact frame and cuts the negative with scissors by hand (real footage).
export const S9Hand: React.FC<B> = ({b}) => {
  const at = useBeats(b);
  return (
    <Scene bg={K.ink}>
      <Pop at={0} x={540} y={800} rot={-2} from={0.85}><Clip src={PJ + 'broll/b1_edit.mp4'} start={27} w={880} h={1220} seed={95} /></Pop>
      <Pop at={6} x={540} y={220} rot={3}><Tag text="بني آدم بإيده" bg={K.yellow} size={60} /></Pop>
      <Pop at={at('scissors', 4.9)} x={280} y={1340} rot={-5}><Tag text="✂ بمقص" size={56} /></Pop>
      <Pop at={at('glue', 6.1)} x={800} y={1400} rot={5}><Tag text="ويلزق" bg={K.red} color={K.white} size={56} /></Pop>
    </Scene>
  );
};

// Film forces preparation; digital = shoot & improvise.
export const S9Prep: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tCost = at('cost', 4.8), tPrep = at('prep', 10), tDig = at('digital', 13.1), tImp = at('improv', 16.8), tEdit = at('edit', 19.6);
  const takes = Math.max(1, Math.floor((f - tDig) / 2));
  return (
    <Scene bg="#16130F">
      <div style={{position: 'absolute', top: 170, left: 60, right: 60, display: 'flex', justifyContent: 'center'}}>
        <Title text="*الخام* بيعلّمك تحضّر" size={96} at={2} />
      </div>
      <div style={{position: 'absolute', left: 50, top: 420, width: 470, height: 1000, background: K.paper, borderRadius: 12, padding: 26, border: `6px solid ${K.ink}`}}>
        <Tag text="خام 🎞" bg={K.yellow} size={48} />
        {['سكريبت', 'ستوري بورد', 'بروفة', 'كل لقطة محسوبة'].map((t, i) => f >= tPrep + i * 8 ? (
          <div key={i} style={{fontFamily: AR, fontWeight: 900, fontSize: 46, color: K.ink, marginTop: 34, display: 'flex', gap: 14, alignItems: 'center'}}>
            <span style={{color: '#2E9E4F', fontSize: 54}}>✓</span>{t}
          </div>
        ) : null)}
        {f >= tCost ? <div style={{position: 'absolute', bottom: 30, right: 26}}><Tag text="غالي + مرهق" bg={K.red} color={K.white} size={42} /></div> : null}
      </div>
      <div style={{position: 'absolute', left: 560, top: 420, width: 470, height: 1000, background: '#22262C', borderRadius: 12, padding: 26, border: `6px solid ${K.ink}`,
        opacity: lin(f, tDig - 6, tDig)}}>
        <Tag text="ديجيتال 📱" bg={K.cyan} size={48} />
        {f >= tDig ? (
          <div style={{marginTop: 80, textAlign: 'center'}}>
            <div style={{fontFamily: EN, fontWeight: 900, fontSize: 60, color: K.paper2}}>TAKE</div>
            <div style={{fontFamily: EN, fontWeight: 900, fontSize: 200, color: K.white, lineHeight: 1}}>{takes}</div>
          </div>
        ) : null}
        {f >= tImp ? <div style={{marginTop: 60, display: 'flex', justifyContent: 'center'}}><Tag text="ارغي وارتجل" size={46} /></div> : null}
        {f >= tEdit ? <div style={{marginTop: 30, display: 'flex', justifyContent: 'center'}}><Tag text="ونظبط في المونتاج" bg={K.yellow} size={42} /></div> : null}
      </div>
    </Scene>
  );
};

// Behind Aly at the end: "everything prepared beforehand" with storyboard frames.
export const S9Ready: React.FC<B> = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 160, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 20}}>
        {Array.from({length: 4}, (_, i) => (
          <div key={i} style={{transform: `scale(${spr(f, 30, i * 4, 160, 13)}) rotate(${(rnd(i) - 0.5) * 10}deg)`}}>
            <Paper w={220} h={170} seed={97 + i} color={K.white}>
              <svg width={220} height={170}><rect x={20} y={20} width={180} height={120} fill="none" stroke="#141210" strokeWidth={4} />
                <circle cx={60 + i * 30} cy={70} r={18} fill="#141210" /><line x1={40} y1={120} x2={180} y2={120} stroke="#141210" strokeWidth={4} /></svg>
            </Paper>
          </div>
        ))}
      </div>
      <Pop at={16} x={540} y={430} rot={-3}><Tag text="كل حاجة متحضّرة من قبلها" bg={K.yellow} size={56} /></Pop>
    </AbsoluteFill>
  );
};
