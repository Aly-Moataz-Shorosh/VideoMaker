import React from 'react';
import {useCurrentFrame} from 'remotion';
import {AR, EN, Pop, lin, spr, useBeats} from '../film/kit';
import {Cursor, Echo, Head, Key, MONO, Note, P, PScene, Pill, SelBox, Term, Typed, WinLogo} from './kit';

// ffmpeg short 3 — 3 ways to open CMD (folder address bar / Windows search / Win + R).
type B = {b?: Record<string, number>; n?: number};
const Badge: React.FC<{n: number; total?: number}> = ({n, total = 3}) => (
  <div style={{position: 'absolute', left: 70, top: 160, display: 'flex', alignItems: 'center', gap: 18, direction: 'ltr'}}>
    <div style={{width: 150, height: 150, borderRadius: '50%', background: P.lime, border: `6px solid ${P.ink}`, boxShadow: `0 10px 0 ${P.deep}`, display: 'flex', alignItems: 'center',
      justifyContent: 'center', fontFamily: EN, fontWeight: 900, fontSize: 96, color: P.ink, fontStyle: 'italic'}}>{n}</div>
    <div style={{fontFamily: MONO, fontSize: 34, color: P.white, opacity: 0.8}}>/ {total}</div>
  </div>
);
const Opened: React.FC<{at: number; y?: number}> = ({at, y = 1180}) => {
  const f = useCurrentFrame();
  if (f < at) return null;
  return (
    <Pop at={at} x={540} y={y} from={0.5}>
      <Term w={820} h={300} size={36}><span style={{color: '#aaa'}}>Microsoft Windows{'\n'}C:\…&gt;</span><span style={{background: Math.floor(f / 8) % 2 ? '#ddd' : 'transparent'}}> </span></Term>
    </Pop>
  );
};

// hook title (over way 1's first second)
export const F3Hook: React.FC<B> = () => (
  <PScene>
    <div style={{position: 'absolute', top: 520, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Echo text="CMD" size={300} color={P.lime} at={0} /></div>
    <div style={{position: 'absolute', top: 900, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Head text="*3 طرق* تفتحه بيها" size={100} at={4} /></div>
  </PScene>
);

// 1. from the folder: address bar -> cmd -> Enter
export const F3Way1: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const click = at('search', 2.3), ty = at('type', 4.1), en = at('enter', 5.5);
  return (
    <PScene>
      <Badge n={1} />
      <div style={{position: 'absolute', top: 360, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Head text="من *الفولدر* نفسه" size={84} at={2} /></div>
      <Pop at={1} x={540} y={640} from={0.7}>
        <div style={{width: 960, height: 120, background: P.white, border: `5px solid ${P.ink}`, boxShadow: `0 14px 0 ${P.deep}`, display: 'flex', alignItems: 'center', gap: 18, padding: '0 26px',
          direction: 'ltr', fontFamily: MONO, fontSize: 38, color: P.ink}}>
          <span style={{fontSize: 44}}>📁</span>
          {f >= ty ? <Typed text="cmd" a={ty} b={ty + 9} /> : <span style={{background: f >= click ? '#9EC5FF' : undefined}}>…\ffmpeg\bin</span>}
        </div>
      </Pop>
      <SelBox x={60} y={580} w={960} h={120} at={click} label="address bar" />
      <Cursor x={lin(f, 0, click - 2, 900, 420)} y={lin(f, 0, click - 2, 1250, 660)} click={click} />
      {f < en + 3 ? <Pop at={ty - 2} x={540} y={1020}><Key label="Enter ↵" w={420} h={170} press={en} color={P.lime} size={64} /></Pop> : null}
      <Opened at={en + 3} />
    </PScene>
  );
};

// 2. Windows search: type CMD -> Enter
export const F3Way2: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const ty = at('type', 2.1), en = at('enter', 2.9);
  return (
    <PScene>
      <Badge n={2} />
      <div style={{position: 'absolute', top: 360, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Head text="من *سيرش* الويندوز" size={84} at={2} /></div>
      {f >= ty + 6 ? (
        <Pop at={ty + 6} x={540} y={860} from={0.7}>
          <div style={{width: 760, background: '#1E1E24', border: `5px solid ${P.ink}`, padding: 26, direction: 'ltr', boxShadow: `12px 14px 0 ${P.deep}`}}>
            <div style={{fontFamily: EN, fontSize: 30, color: '#aaa'}}>Best match</div>
            <div style={{marginTop: 16, display: 'flex', alignItems: 'center', gap: 22, background: f >= en ? '#3A3A55' : '#2A2A33', padding: 18}}>
              <div style={{width: 80, height: 64, background: '#0B0B0E', border: '3px solid #888', color: P.white, fontFamily: MONO, fontSize: 22, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>C:\</div>
              <div><div style={{fontFamily: EN, fontWeight: 700, fontSize: 40, color: P.white}}>Command Prompt</div><div style={{fontFamily: EN, fontSize: 26, color: '#aaa'}}>App</div></div>
            </div>
          </div>
        </Pop>
      ) : null}
      {/* taskbar */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 1240, height: 120, background: '#14141A', display: 'flex', alignItems: 'center', gap: 22, padding: '0 34px', direction: 'ltr',
        transform: `translateY(${(1 - spr(f, 30, 0)) * 200}px)`}}>
        <WinLogo s={60} color={P.white} />
        <div style={{width: 640, height: 76, background: P.white, display: 'flex', alignItems: 'center', gap: 16, padding: '0 22px', fontFamily: EN, fontSize: 34, color: '#555'}}>
          🔍 {f >= ty ? <span style={{color: P.ink, fontWeight: 700}}><Typed text="CMD" a={ty} b={ty + 6} /></span> : 'Type here to search'}
        </div>
      </div>
      <SelBox x={116} y={1262} w={640} h={76} at={ty - 4} label="search" tagBelow={false} />
      {f >= en ? <Pop at={en} x={880} y={1060}><Key label="↵" w={170} h={140} press={en} color={P.lime} size={70} /></Pop> : null}
    </PScene>
  );
};

// 3. hold the Windows key + R -> Run box -> cmd -> Enter
export const F3Way3: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const win = at('win', 1.2), r = at('r', 3.2), ty = at('type', 4.6), en = at('enter', 5.4);
  const hold = f >= win + 3 && f < en ? 1 : 0;
  return (
    <PScene>
      <Badge n={3} />
      <div style={{position: 'absolute', top: 360, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Echo text="WIN + R" size={120} color={P.lime} at={2} /></div>
      <div style={{position: 'absolute', left: 150, top: 560, display: 'flex', gap: 40, alignItems: 'center', direction: 'ltr'}}>
        <div style={{transform: `translateY(${hold * 18}px)`}}>
          <div style={{width: 300, height: 220, background: P.white, borderRadius: 28, border: `5px solid ${P.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: `0 ${26 - hold * 18}px 0 #8F86C9`}}><WinLogo s={110} color={P.blue} /></div>
        </div>
        <div style={{fontFamily: EN, fontWeight: 900, fontSize: 110, color: P.white, opacity: lin(f, r - 6, r)}}>+</div>
        <div style={{opacity: lin(f, r - 6, r)}}><Key label="R" w={240} h={220} press={r} size={110} /></div>
      </div>
      {f >= win + 3 && f < r ? <Pop at={win + 3} x={360} y={900}><Note text="خليك دايس…" size={60} /></Pop> : null}
      {f >= r + 4 ? (
        <Pop at={r + 4} x={540} y={1140} from={0.7}>
          <div style={{width: 820, background: '#F0F0F0', border: `5px solid ${P.ink}`, boxShadow: `12px 14px 0 ${P.deep}`, direction: 'ltr', fontFamily: EN}}>
            <div style={{height: 56, background: P.white, display: 'flex', alignItems: 'center', padding: '0 20px', fontSize: 28, fontWeight: 700}}>Run</div>
            <div style={{padding: 26, display: 'flex', alignItems: 'center', gap: 18, fontSize: 34}}>Open:
              <div style={{flex: 1, height: 64, background: P.white, border: '3px solid #2B7BC4', display: 'flex', alignItems: 'center', padding: '0 14px', fontFamily: MONO}}>
                {f >= ty ? <Typed text="cmd" a={ty} b={ty + 7} /> : null}
              </div>
            </div>
            <div style={{padding: '0 26px 24px', display: 'flex', justifyContent: 'flex-end', gap: 16}}>
              <div style={{padding: '8px 34px', border: '3px solid #2B7BC4', background: f >= en ? '#9EC5FF' : P.white, fontSize: 28}}>OK</div>
              <div style={{padding: '8px 22px', border: '3px solid #999', fontSize: 28}}>Cancel</div>
            </div>
          </div>
        </Pop>
      ) : null}
      {f >= en ? <Pop at={en} x={880} y={1400}><Key label="↵" w={170} h={140} press={en} color={P.lime} size={70} /></Pop> : null}
    </PScene>
  );
};

// end: what matters = reach CMD, the place where you type
export const F3End: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const cmd = at('cmd', 1.6), wr = at('write', 2.8);
  return (
    <PScene>
      <div style={{position: 'absolute', top: 200, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Head text="المهم توصل لـ *CMD*" size={88} at={2} /></div>
      <Pop at={cmd} x={540} y={780} from={0.6}><Term w={900} h={420} size={44}><span style={{color: '#888'}}>C:\…&gt;</span>{f >= wr ? <Typed text="ffmpeg …" a={wr} b={wr + 10} color={P.lime} /> : null}</Term></Pop>
      {f >= wr ? <Pop at={wr} x={540} y={1110} rot={-4}><Note text="هنا هتكتب الأوامر" size={76} /></Pop> : null}
      <div style={{position: 'absolute', top: 1260, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 30, direction: 'ltr'}}>
        {['1  📁', '2  🔍', '3  ⊞+R'].map((t, i) => (
          <div key={t} style={{opacity: lin(f, 4 + i * 4, 10 + i * 4), transform: `translateY(${(1 - lin(f, 4 + i * 4, 10 + i * 4)) * 40}px)`}}>
            <Pill text={t} dir="ltr" font={EN} size={46} bg={[P.lime, P.white, P.yellow][i]} />
          </div>
        ))}
      </div>
    </PScene>
  );
};
