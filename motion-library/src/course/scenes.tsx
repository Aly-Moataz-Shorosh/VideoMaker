import React from 'react';
import {AbsoluteFill, Easing, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Type} from '../glass/kit';
import {AR, bi, CC, CourseBg, EN, G, Glass, Ico, lin, Pill, spr, Src} from './kit';

// Full-screen scenes of the course (opening + inside-chapter animations). Every scene gets {dur} (frames) + its props.
type P = {dur: number; [k: string]: any};
const Out: React.FC<{dur: number; children: React.ReactNode; bg?: boolean}> = ({dur, children, bg = true}) => {
  const f = useCurrentFrame();
  const a = lin(f, 0, 10), b = 1 - lin(f, dur - 9, dur, 0, 1, Easing.in(Easing.cubic));
  const o = Math.min(a, b);
  return (
    <AbsoluteFill style={{opacity: o, filter: o < 0.99 ? `blur(${(1 - o) * 12}px)` : undefined}}>
      {bg ? <CourseBg /> : null}
      {children}
    </AbsoluteFill>
  );
};
const Center: React.FC<{y: number; children: React.ReactNode}> = ({y, children}) => (
  <div style={{position: 'absolute', left: 0, right: 0, top: y, display: 'flex', justifyContent: 'center'}}>{children}</div>
);

// 1) "I made this course in 2018" + the YouTube page screenshot, zooming onto the highlighted date.
const OProof: React.FC<P> = ({dur, img, line1, line2}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 8, 120, 18);
  // screenshot 1764x1424: start = whole width, top part; end = zoom onto title + highlighted date (~ (400, 1300) of the source)
  const k = lin(f, 40, 110, 0, 1, Easing.inOut(Easing.cubic));
  const s0 = 992 / 1764, s1 = 1.0;
  const s = s0 + (s1 - s0) * k;
  const left = (496 - 420 * s1) * k, top = (0 - 60 * s0) * (1 - k) + (330 - 1300 * s1) * k;
  return (
    <Out dur={dur}>
      <Center y={90}><Type text={line1} at={4} size={70} width={1500} /></Center>
      <div style={{position: 'absolute', left: 960, top: 600, transform: `translate(-50%,-50%) translateY(${(1 - p) * 60}px)`, opacity: Math.min(1, p * 1.3)}}>
        <Glass w={1020} pad={14} r={30} glow={G.gold}>
          <div style={{width: 992, height: 600, overflow: 'hidden', borderRadius: 20, position: 'relative', background: '#fff'}}>
            {/* image 1764x1424 -> fit width 992; date sits at ~ (100, 1362) of the source */}
            <Img src={staticFile(img)} style={{position: 'absolute', width: 1764 * s, left, top}} />
          </div>
        </Glass>
      </div>
      <Center y={950}><Type text={line2} at={70} size={46} width={1500} color={G.soft} /></Center>
    </Out>
  );
};

// 2) the name: Premiere Pro -> Premiere (26), "fundamentally still the same app".
const OName: React.FC<P> = ({dur, line1, line2, src}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const cut = lin(f, 40, 52);
  const p = spr(f, fps, 6, 140, 16);
  return (
    <Out dur={dur}>
      <Center y={120}><Type text={line1} at={4} size={64} width={1500} /></Center>
      <div style={{position: 'absolute', left: 960, top: 470, transform: `translate(-50%,-50%) scale(${0.9 + 0.1 * p})`, opacity: p, display: 'flex', alignItems: 'center', gap: 46, direction: 'ltr'}}>
        <div style={{width: 210, height: 205, borderRadius: 42, background: CC.prBg, border: `7px solid ${CC.violet}`, boxSizing: 'border-box', display: 'flex', alignItems: 'center',
          justifyContent: 'center', boxShadow: `0 20px 70px ${CC.violet}66`}}>
          <span style={{fontFamily: EN, fontWeight: 700, fontSize: 112, color: CC.violet}}>Pr</span>
        </div>
        <div style={{fontFamily: EN, fontWeight: 900, fontSize: 120, color: G.ink, display: 'flex', alignItems: 'baseline', gap: 30}}>
          <span>Premiere</span>
          <span style={{position: 'relative', color: lin(f, 40, 60) > 0.5 ? G.dim : G.ink, opacity: 1 - lin(f, 64, 84) * 0.75, fontSize: 120 - lin(f, 64, 84) * 40}}>
            Pro
            <span style={{position: 'absolute', left: -8, top: '52%', height: 12, width: `${cut * 108}%`, background: CC.coral, borderRadius: 8, transform: 'rotate(-6deg)'}} />
          </span>
          <span style={{fontSize: 70, color: G.gold, opacity: lin(f, 70, 84)}}>26</span>
        </div>
      </div>
      <Center y={690}><Type text={line2} at={88} size={54} width={1500} /></Center>
      <Center y={900}><div style={{opacity: lin(f, 110, 125)}}><Src text={src} /></div></Center>
    </Out>
  );
};

// 3) one big typed line (his intro note: "the course is more than enough").
const OLine: React.FC<P> = ({dur, line1, line2, big}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 40, 160, 12);
  return (
    <Out dur={dur}>
      <Center y={250}><Type text={line1} at={4} size={66} width={1500} /></Center>
      {big ? (
        <div style={{position: 'absolute', left: 960, top: 560, transform: `translate(-50%,-50%) scale(${0.6 + 0.4 * p}) rotate(${(1 - p) * -6}deg)`, opacity: Math.min(1, p * 1.5)}}>
          <Pill text={big} font={EN} dir="ltr" size={130} />
        </div>
      ) : null}
      {line2 ? <Center y={760}><Type text={line2} at={56} size={52} width={1500} color={G.soft} /></Center> : null}
    </Out>
  );
};

// 4) Claude's analysis: coverage of the official Adobe exam objectives, one bar per domain + the total ring.
const OChart: React.FC<P> = ({dur, title, sub, rows, total, cap, core, src}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ringP = lin(f, 60 + rows.length * 10, 120 + rows.length * 10, 0, 1, Easing.out(Easing.cubic));
  const R = 150, C = 2 * Math.PI * R;
  return (
    <Out dur={dur}>
      <div style={{position: 'absolute', right: 110, top: 70, direction: 'rtl', display: 'flex', alignItems: 'center', gap: 20}}>
        <div style={{padding: '6px 20px', borderRadius: 30, background: CC.coral, fontFamily: AR, fontWeight: 900, fontSize: 32, color: '#fff'}}>تحليل Claude</div>
        <Type text={title} at={2} size={52} width={1200} dir="rtl" />
      </div>
      <div style={{position: 'absolute', right: 110, top: 150, width: 1700, direction: 'rtl', fontFamily: AR, fontWeight: 700, fontSize: 30, color: G.soft, opacity: lin(f, 14, 28), textAlign: 'right'}}>{bi(sub)}</div>
      <div style={{position: 'absolute', right: 110, top: 300, width: 1060}}>
        {rows.map((r: any, i: number) => {
          const at = 30 + i * 10;
          const v = lin(f, at, at + 36, 0, r.v, Easing.out(Easing.cubic));
          const col = r.v >= 0.66 ? G.green : r.v >= 0.4 ? G.gold : CC.coral;
          const o = lin(f, at - 6, at + 6);
          return (
            <div key={i} style={{display: 'flex', alignItems: 'center', gap: 24, marginBottom: 30, opacity: o, direction: 'rtl'}}>
              <div style={{width: 420, textAlign: 'right'}}>
                <div style={{fontFamily: AR, fontWeight: 800, fontSize: 34, color: G.ink, lineHeight: 1.2}}>{r.ar}</div>
                <div style={{fontFamily: EN, fontWeight: 600, fontSize: 20, color: G.dim, direction: 'ltr', textAlign: 'right'}}>{r.en}</div>
              </div>
              <div style={{flex: 1, height: 44, borderRadius: 22, background: 'rgba(255,255,255,0.08)', position: 'relative', overflow: 'hidden'}}>
                <div style={{position: 'absolute', right: 0, top: 0, bottom: 0, width: `${v * 100}%`, borderRadius: 22, background: `linear-gradient(270deg, ${col}, ${col}AA)`, boxShadow: `0 0 24px ${col}66`}} />
              </div>
              <div style={{width: 110, fontFamily: EN, fontWeight: 900, fontSize: 40, color: col, direction: 'ltr', textAlign: 'left'}}>{Math.round(v * 100)}%</div>
            </div>
          );
        })}
      </div>
      <div style={{position: 'absolute', left: 150, top: 300, width: 380, textAlign: 'center', opacity: lin(f, 60 + rows.length * 10, 80 + rows.length * 10)}}>
        <svg width={360} height={360} viewBox="0 0 360 360">
          <circle cx={180} cy={180} r={R} fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth={28} />
          <circle cx={180} cy={180} r={R} fill="none" stroke={G.gold} strokeWidth={28} strokeLinecap="round" strokeDasharray={`${C * total * ringP} ${C}`} transform="rotate(-90 180 180)" />
          <text x={180} y={200} textAnchor="middle" fontFamily="Montserrat" fontWeight={900} fontSize={84} fill="#fff">{Math.round(total * 100 * ringP)}%</text>
        </svg>
        <div style={{fontFamily: AR, fontWeight: 800, fontSize: 30, color: G.ink, direction: 'rtl', marginTop: 6, lineHeight: 1.35}}>{bi(cap)}</div>

      </div>
      {core ? (
        <div style={{position: 'absolute', left: 0, right: 0, bottom: 120, display: 'flex', justifyContent: 'center', opacity: lin(f, 120, 136)}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 14, padding: '10px 26px', borderRadius: 40, background: 'rgba(255,107,91,0.14)', border: `2px solid ${CC.coral}`,
            fontFamily: AR, fontWeight: 800, fontSize: 30, color: G.ink, direction: 'rtl'}}><span style={{color: CC.coral}}>⊘</span>{bi(core)}</div>
        </div>
      ) : null}
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 50, display: 'flex', justifyContent: 'center', opacity: lin(f, 40, 56)}}><Src text={src} /></div>
    </Out>
  );
};

// 4') three yardsticks side by side (Aly: the number depends on what you compare with -> show all three, each with its source).
const OMeter: React.FC<P> = ({dur, title, sub, rings, note}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const R = 120, C = 2 * Math.PI * R;
  return (
    <Out dur={dur}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 60, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 22, direction: 'rtl'}}>
        <div style={{padding: '6px 20px', borderRadius: 30, background: CC.coral, fontFamily: AR, fontWeight: 900, fontSize: 32, color: '#fff'}}>تحليل Claude</div>
        <Type text={title} at={2} size={56} width={1100} dir="rtl" />
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 160, textAlign: 'center', direction: 'rtl', fontFamily: AR, fontWeight: 700, fontSize: 32, color: G.soft, opacity: lin(f, 12, 26)}}>{bi(sub)}</div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 250, display: 'flex', justifyContent: 'center', gap: 50, direction: 'rtl'}}>
        {rings.map((r: any, i: number) => {
          const at = 26 + i * 26;
          const p = spr(f, fps, at, 140, 16);
          const v = lin(f, at + 6, at + 46, 0, r.v, Easing.out(Easing.cubic));
          const col = r.v >= 0.9 ? G.green : r.v >= 0.75 ? G.gold : G.blue;
          return (
            <div key={i} style={{transform: `translateY(${(1 - p) * 60}px)`, opacity: Math.min(1, p * 1.4)}}>
              <Glass w={540} h={660} pad={28} r={40} glow={col}>
                <div style={{display: 'flex', justifyContent: 'center'}}>
                  <svg width={290} height={290} viewBox="0 0 290 290">
                    <circle cx={145} cy={145} r={R} fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth={24} />
                    <circle cx={145} cy={145} r={R} fill="none" stroke={col} strokeWidth={24} strokeLinecap="round" strokeDasharray={`${C * v} ${C}`} transform="rotate(-90 145 145)" />
                    <text x={145} y={165} textAnchor="middle" fontFamily="Montserrat" fontWeight={900} fontSize={66} fill="#fff">{Math.round(v * 100)}%</text>
                  </svg>
                </div>
                <div style={{fontFamily: AR, fontWeight: 900, fontSize: 36, color: G.ink, textAlign: 'center', direction: 'rtl', lineHeight: 1.3, marginTop: 6}}>{bi(r.head)}</div>
                <div style={{fontFamily: AR, fontWeight: 700, fontSize: 27, color: G.soft, textAlign: 'center', direction: 'rtl', lineHeight: 1.4, marginTop: 8}}>{bi(r.text)}</div>
                {r.miss ? <div style={{fontFamily: AR, fontWeight: 700, fontSize: 24, color: r.v >= 0.999 ? G.green : CC.coral, textAlign: 'center', direction: 'rtl', lineHeight: 1.4, marginTop: 12,
                  opacity: lin(f, at + 40, at + 52)}}>{bi(r.miss)}</div> : null}
                <div style={{position: 'absolute', left: 0, right: 0, bottom: 24, display: 'flex', justifyContent: 'center'}}><Src text={r.src} s={0.8} /></div>
              </Glass>
            </div>
          );
        })}
      </div>
      {note ? (
        <div style={{position: 'absolute', left: 0, right: 0, bottom: 60, display: 'flex', justifyContent: 'center', opacity: lin(f, 120, 136)}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 14, padding: '10px 26px', borderRadius: 40, background: 'rgba(255,107,91,0.14)', border: `2px solid ${CC.coral}`,
            fontFamily: AR, fontWeight: 800, fontSize: 28, color: G.ink, direction: 'rtl'}}><span style={{color: CC.coral}}>⊘</span>{bi(note)}</div>
        </div>
      ) : null}
    </Out>
  );
};

// 4b) why the whole-curriculum number is lower: three reasons, each a glass row with an icon (Aly asked: explain the gap).
const OWhy: React.FC<P> = ({dur, title, rows, foot}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <Out dur={dur}>
      <Center y={80}><Type text={title} at={2} size={60} width={1600} /></Center>
      <div style={{position: 'absolute', left: 0, right: 0, top: 220, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 26}}>
        {rows.map((r: any, i: number) => {
          const p = spr(f, fps, 16 + i * 22, 150, 16);
          return (
            <div key={i} style={{transform: `translateX(${(1 - p) * 90}px)`, opacity: Math.min(1, p * 1.4)}}>
              <Glass w={1500} pad={26} r={34} glow={r.c}>
                <div style={{display: 'flex', alignItems: 'center', gap: 30, direction: 'rtl'}}>
                  <div style={{width: 110, height: 110, borderRadius: 30, background: 'rgba(255,255,255,0.08)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}><Ico n={r.ico} s={0.85} c={r.c} /></div>
                  <div style={{flex: 1}}>
                    <div style={{fontFamily: AR, fontWeight: 900, fontSize: 42, color: G.ink}}>{bi(r.head)}</div>
                    <div style={{fontFamily: AR, fontWeight: 700, fontSize: 30, color: G.soft, marginTop: 4, lineHeight: 1.4}}>{bi(r.text)}</div>
                  </div>
                  {r.src ? <Src text={r.src} s={0.8} /> : null}
                </div>
              </Glass>
            </div>
          );
        })}
      </div>
      <Center y={930}><Type text={foot} at={100} size={46} width={1600} color={G.soft} /></Center>
    </Out>
  );
};

// 5) what changed / got easier since 2018 (each tile = icon, old -> new, source).
const OChanged: React.FC<P> = ({dur, title, tiles, foot}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <Out dur={dur}>
      <Center y={90}><Type text={title} at={2} size={62} width={1600} /></Center>
      <div style={{position: 'absolute', left: 0, right: 0, top: 260, display: 'flex', justifyContent: 'center', gap: 44, direction: 'rtl'}}>
        {tiles.map((t: any, i: number) => {
          const p = spr(f, fps, 20 + i * 14, 140, 15);
          return (
            <div key={i} style={{transform: `translateY(${(1 - p) * 80}px)`, opacity: Math.min(1, p * 1.4)}}>
              <Glass w={520} h={520} pad={34} r={40} glow={CC.violet}>
                <div style={{display: 'flex', justifyContent: 'center'}}><Ico n={t.ico} s={1.2} c={CC.violet} /></div>
                <div style={{fontFamily: EN, fontWeight: 900, fontSize: 40, color: G.ink, textAlign: 'center', marginTop: 18, direction: 'ltr'}}>{t.en}</div>
                <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 14, marginTop: 16, direction: 'ltr'}}>
                  <span style={{fontFamily: EN, fontWeight: 700, fontSize: 28, color: G.dim, textDecoration: 'line-through'}}>{t.old}</span>
                  <span style={{fontSize: 30, color: G.gold}}>→</span>
                  <span style={{fontFamily: EN, fontWeight: 800, fontSize: 30, color: G.gold}}>{t.neu}</span>
                </div>
                <div style={{fontFamily: AR, fontWeight: 700, fontSize: 30, color: G.soft, textAlign: 'center', marginTop: 18, direction: 'rtl', lineHeight: 1.4}}>{bi(t.ar)}</div>
                <div style={{position: 'absolute', left: 0, right: 0, bottom: 26, display: 'flex', justifyContent: 'center'}}><Src text={t.src} s={0.85} /></div>
              </Glass>
            </div>
          );
        })}
      </div>
      <Center y={880}><Type text={foot} at={70} size={46} width={1600} color={G.soft} /></Center>
    </Out>
  );
};

// 6) Claude's verdict.
const OVerdict: React.FC<P> = ({dur, q, yes, l1, l2, l3, sign}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 34, 170, 11);
  return (
    <Out dur={dur}>
      <Center y={110}><Type text={q} at={2} size={64} width={1600} /></Center>
      <div style={{position: 'absolute', left: 960, top: 330, transform: `translate(-50%,-50%) scale(${0.5 + 0.5 * p})`, opacity: Math.min(1, p * 1.4), display: 'flex', alignItems: 'center', gap: 30, direction: 'rtl'}}>
        <div style={{width: 130, height: 130, borderRadius: '50%', background: G.green, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 80, color: '#fff',
          fontWeight: 900, boxShadow: `0 0 60px ${G.green}AA`}}>✓</div>
        <Pill text={yes} color={G.green} ink="#fff" size={96} />
      </div>
      <Center y={480}><Type text={l1} at={56} size={48} width={1600} /></Center>
      <Center y={580}><Type text={l2} at={86} size={48} width={1600} /></Center>
      <Center y={720}><Type text={l3} at={120} size={48} width={1600} pill={G.blue} /></Center>
      <div style={{position: 'absolute', left: 140, bottom: 80, fontFamily: AR, fontWeight: 800, fontSize: 38, color: G.gold, direction: 'rtl', opacity: lin(f, 150, 166)}}>{sign}</div>
    </Out>
  );
};

// 7) timestamps: one page per episode, every chapter = time + name + its animated icon. Calm music under it (Aly).
const OStamps: React.FC<P> = ({dur, range, title, items}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = items.length;
  const cols = n > 9 ? 2 : 1;
  const per = Math.ceil(n / cols);
  return (
    <Out dur={dur}>
      <div style={{position: 'absolute', right: 110, top: 64, direction: 'rtl', display: 'flex', alignItems: 'center', gap: 22}}>
        <div style={{padding: '6px 22px', borderRadius: 30, background: G.gold, fontFamily: AR, fontWeight: 900, fontSize: 34, color: '#14181F'}}>{range}</div>
        <span style={{fontFamily: AR, fontWeight: 900, fontSize: 56, color: G.ink}}>{title}</span>
      </div>
      <div style={{position: 'absolute', right: 110, left: 110, top: 170, display: 'flex', gap: 50, direction: 'rtl'}}>
        {Array.from({length: cols}).map((_, c) => (
          <div key={c} style={{flex: 1}}>
            {items.slice(c * per, (c + 1) * per).map((it: any, i: number) => {
              const idx = c * per + i;
              const p = spr(f, fps, 8 + idx * 3, 160, 17);
              return (
                <div key={i} style={{display: 'flex', alignItems: 'center', gap: 18, height: Math.min(76, 840 / per), opacity: Math.min(1, p * 1.4), transform: `translateX(${(1 - p) * -40}px)`}}>
                  <div style={{width: 60, display: 'flex', justifyContent: 'center'}}><Ico n={it.ico} s={Math.min(0.55, 5.6 / per)} /></div>
                  <span style={{fontFamily: EN, fontWeight: 800, fontSize: Math.min(30, 330 / per), color: G.gold, direction: 'ltr', width: 120, textAlign: 'right'}}>{it.time}</span>
                  <span style={{fontFamily: AR, fontWeight: 800, fontSize: Math.min(32, 350 / per), color: G.ink, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{bi(it.ar)}</span>
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </Out>
  );
};

// ---------- chapter-1 animations (frame rate) ----------
// "Video = pictures in a row": a film strip of 8 frames of a bouncing ball, then the strip plays as motion.
const Flip: React.FC<P> = ({dur, at = 0}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const N = 8;
  const ball = (k: number) => ({x: 20 + k * 9, y: 70 - 55 * Math.abs(Math.sin((k / N) * Math.PI))});
  const play = Math.floor(Math.max(0, f - 70) / 3) % N; // after the strip is built, the frames run (8 fps)
  return (
    <Out dur={dur} bg={false}>
      <div style={{position: 'absolute', left: 30, top: 200, width: 620, direction: 'rtl', textAlign: 'center'}}>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 46, color: G.ink}}>الفيديو = <span style={{color: G.gold}}>صور</span> ورا بعض</div>
      </div>
      <div style={{position: 'absolute', left: 40, top: 300, width: 600, display: 'flex', flexWrap: 'wrap', gap: 12, justifyContent: 'center', direction: 'ltr'}}>
        {Array.from({length: N}).map((_, k) => {
          const p = spr(f, fps, 6 + k * 5, 180, 14);
          const b = ball(k);
          const on = f > 70 && k === play;
          return (
            <div key={k} style={{width: 135, height: 100, borderRadius: 10, background: on ? '#26324A' : '#141B28', border: `3px solid ${on ? G.gold : 'rgba(255,255,255,0.25)'}`, position: 'relative',
              transform: `scale(${0.6 + 0.4 * p})`, opacity: Math.min(1, p * 1.4)}}>
              <div style={{position: 'absolute', left: (b.x / 100) * 110 + 4, top: (b.y / 100) * 80, width: 18, height: 18, borderRadius: '50%', background: G.gold}} />
              <div style={{position: 'absolute', right: 6, bottom: 2, fontFamily: EN, fontWeight: 800, fontSize: 16, color: G.dim}}>{k + 1}</div>
            </div>
          );
        })}
      </div>
      <div style={{position: 'absolute', left: 140, top: 560, width: 400, height: 260, borderRadius: 18, background: '#141B28', border: '3px solid rgba(255,255,255,0.3)', opacity: lin(f, 60, 72),
        overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: (ball(play).x / 100) * 330 + 10, top: (ball(play).y / 100) * 200 + 10, width: 40, height: 40, borderRadius: '50%', background: G.gold, boxShadow: `0 0 24px ${G.gold}`}} />
        <div style={{position: 'absolute', left: 14, top: 10, fontFamily: EN, fontWeight: 800, fontSize: 22, color: '#FF5A5F'}}>● PLAY</div>
      </div>
    </Out>
  );
};

// fps race: the same run at 6 / 12 / 24 / 60 fps (position only updates on each frame of that rate) -> smoother as fps grows.
const FpsRace: React.FC<P> = ({dur, rates = [6, 12, 24, 60], note}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  return (
    <Out dur={dur} bg={false}>
      <div style={{position: 'absolute', left: 30, top: 190, width: 620, textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 44, color: G.ink, direction: 'rtl'}}>
        نفس الحركة.. بعدد صور مختلف
      </div>
      {rates.map((r: number, i: number) => {
        const q = Math.floor(t * r) / r; // last frame shown at this rate
        const x = ((q * 0.5) % 1);
        const p = lin(f, 8 + i * 6, 20 + i * 6);
        return (
          <div key={r} style={{position: 'absolute', left: 50, top: 320 + i * 115, width: 580, height: 90, opacity: p, direction: 'ltr'}}>
            <div style={{position: 'absolute', left: 0, top: 30, width: 110, fontFamily: EN, fontWeight: 900, fontSize: 32, color: r >= 24 ? G.green : r >= 12 ? G.gold : CC.coral}}>{r} fps</div>
            <div style={{position: 'absolute', left: 120, top: 44, width: 450, height: 4, background: 'rgba(255,255,255,0.15)', borderRadius: 2}} />
            <div style={{position: 'absolute', left: 120 + x * 420, top: 22, width: 46, height: 46, borderRadius: '50%', background: r >= 24 ? G.green : r >= 12 ? G.gold : CC.coral}} />
          </div>
        );
      })}
      {note ? <div style={{position: 'absolute', left: 30, top: 800, width: 620, textAlign: 'center', fontFamily: AR, fontWeight: 700, fontSize: 32, color: G.soft, direction: 'rtl', opacity: lin(f, 60, 74)}}>{note}</div> : null}
    </Out>
  );
};

// big counter: "30 صورة في الثانية" — 30 small frames fill a 1-second bar.
const PerSecond: React.FC<P> = ({dur, n = 30}) => {
  const f = useCurrentFrame();
  const k = Math.min(n, Math.floor(lin(f, 6, 6 + n * 1.2, 0, n + 0.01, Easing.linear)));
  return (
    <Out dur={dur} bg={false}>
      <div style={{position: 'absolute', left: 30, top: 230, width: 620, textAlign: 'center', direction: 'rtl'}}>
        <div style={{fontFamily: EN, fontWeight: 900, fontSize: 130, color: G.gold, direction: 'ltr'}}>{k}</div>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 44, color: G.ink, marginTop: -10}}>صورة في <span style={{color: G.blue}}>الثانية</span></div>
      </div>
      <div style={{position: 'absolute', left: 60, top: 560, width: 560, display: 'flex', flexWrap: 'wrap', gap: 6, direction: 'ltr'}}>
        {Array.from({length: n}).map((_, i) => (
          <div key={i} style={{width: 50, height: 36, borderRadius: 5, background: i < k ? G.gold : 'rgba(255,255,255,0.08)', border: '1.5px solid rgba(255,255,255,0.2)'}} />
        ))}
      </div>
      <div style={{position: 'absolute', left: 60, top: 760, width: 560, height: 6, borderRadius: 3, background: G.blue}} />
      <div style={{position: 'absolute', left: 60, top: 775, width: 560, textAlign: 'center', fontFamily: EN, fontWeight: 800, fontSize: 26, color: G.blue}}>1 second</div>
    </Out>
  );
};

// Episode agenda (left column at the start of an episode): icon rows light up one by one, the current one glows.
const Agenda: React.FC<P> = ({dur, ep, title, items}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const hi = Math.floor(Math.max(0, f - 20) / 40) % items.length;
  return (
    <Out dur={dur} bg={false}>
      <div style={{position: 'absolute', left: 40, top: 170, width: 600, direction: 'rtl'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 16}}>
          <div style={{padding: '4px 18px', borderRadius: 26, background: G.gold, fontFamily: AR, fontWeight: 900, fontSize: 30, color: '#14181F'}}>اللي جاي</div>
          <span style={{fontFamily: AR, fontWeight: 900, fontSize: 44, color: G.ink}}>{title}</span>
        </div>
        <div style={{marginTop: 30}}>
          {items.map((it: any, i: number) => {
            const p = spr(f, fps, 10 + i * 6, 160, 16);
            const on = i === hi;
            return (
              <div key={i} style={{display: 'flex', alignItems: 'center', gap: 20, padding: '10px 16px', marginBottom: 10, borderRadius: 22, opacity: Math.min(1, p * 1.4),
                transform: `translateX(${(1 - p) * -40}px)`, background: on ? 'rgba(255,255,255,0.10)' : 'transparent', border: on ? `2px solid ${G.gold}66` : '2px solid transparent'}}>
                <Ico n={it.ico} s={0.6} c={on ? G.gold : G.soft} live={on} />
                <span style={{fontFamily: AR, fontWeight: 800, fontSize: 34, color: on ? G.ink : G.soft}}>{bi(it.ar)}</span>
              </div>
            );
          })}
        </div>
      </div>
    </Out>
  );
};

// Chapter 47 (Claude): what to learn after this course. Two pages of 4 tiles (thumbnail + QR + one line + official source),
// then Claude's advice. Aly: "في اخر الفيديو حط الحاجات اللي ناقصة ... وانصحه بيها" + "قول ان كلود اللي مرشحه مش انا".
const NEXT = [
  {n: 'Text-Based Editing', ar: 'تقطع فيديو الكلام من النص المكتوب', v: 'tbe', src: 'Adobe blog'},
  {n: 'Captions', ar: 'ترجمة مكتوبة أوتوماتيك (Speech to Text)', v: 's2t', src: 'Adobe helpx'},
  {n: 'Auto Reframe', ar: 'نفس الفيديو طولي ومربع لكل منصة', v: 'reframe', src: 'Adobe helpx'},
  {n: 'Enhance Speech', ar: 'تنضيف الصوت بضغطة + Essential Sound', v: 'speech', src: 'Adobe helpx'},
  {n: 'Multi-camera', ar: 'مونتاج كذا كاميرا مع بعض (لقاء، حفلة)', v: 'multicam', src: 'Adobe helpx'},
  {n: 'Proxy', ar: 'نسخ خفيفة من الفيديو عشان الجهاز الضعيف', v: 'proxy', src: 'Adobe helpx'},
  {n: 'Motion Graphics Templates', ar: 'كتابات وجرافيكس جاهزة تعدّل فيها', v: 'mogrt', src: 'Adobe helpx'},
  {n: 'Generative Extend', ar: 'أدوات الـ AI: يطوّل الكليب ويتتبع الحاجات', v: 'genext', src: 'Adobe helpx'},
];
const ONext: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const page = f < 20 * fps ? 0 : f < 40 * fps ? 1 : 2;
  const pf = f - page * 20 * fps;
  return (
    <Out dur={dur}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 50, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 20, direction: 'rtl'}}>
        <div style={{padding: '6px 20px', borderRadius: 30, background: CC.coral, fontFamily: AR, fontWeight: 900, fontSize: 30, color: '#fff'}}>ترشيحات Claude</div>
        <span style={{fontFamily: AR, fontWeight: 900, fontSize: 54, color: G.ink}}>اللي ناقصك تتعلمه بعد الكورس ده</span>
      </div>
      {page < 2 ? (
        <div style={{position: 'absolute', left: 80, right: 80, top: 170, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 30, direction: 'rtl'}}>
          {NEXT.slice(page * 4, page * 4 + 4).map((it, i) => {
            const p = spr(pf, fps, 8 + i * 10, 140, 16);
            return (
              <div key={it.n} style={{opacity: Math.min(1, p * 1.4) * (1 - lin(pf, 20 * fps - 10, 20 * fps)), transform: `translateY(${(1 - p) * 50}px)`}}>
                <Glass w={865} h={370} pad={22} r={30} glow={G.blue}>
                  <div style={{display: 'flex', gap: 22, direction: 'rtl', alignItems: 'center'}}>
                    <div style={{position: 'relative', width: 400, height: 225, borderRadius: 16, overflow: 'hidden', flexShrink: 0}}>
                      <Img src={staticFile(`projects/premiere/vids/${it.v}.jpg`)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
                    </div>
                    <div style={{flex: 1}}>
                      <div style={{fontFamily: EN, fontWeight: 900, fontSize: 36, color: G.gold, direction: 'ltr', textAlign: 'right', lineHeight: 1.15}}>{it.n}</div>
                      <div style={{fontFamily: AR, fontWeight: 700, fontSize: 28, color: G.soft, marginTop: 10, lineHeight: 1.4}}>{bi(it.ar)}</div>
                    </div>
                  </div>
                  <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 14, direction: 'rtl'}}>
                    <Src text={it.src} s={0.85} />
                    <div style={{background: '#fff', padding: 6, borderRadius: 10}}><Img src={staticFile(`projects/premiere/qr/${it.v}.png`)} style={{width: 92, height: 92, display: 'block'}} /></div>
                  </div>
                </Glass>
              </div>
            );
          })}
        </div>
      ) : (
        <div style={{position: 'absolute', left: 160, right: 160, top: 260, direction: 'rtl', textAlign: 'center'}}>
          <Type text="نصيحتي: ابدأ بـ *Captions* و *Enhance_Speech*.. هيوفروا وقتك من أول فيديو" at={6} size={56} width={1600} />
          <div style={{marginTop: 50, opacity: lin(pf, 50, 66)}}><Type text="وبعدين Proxy لو جهازك تقيل، و Multi-camera لو بتصور بأكتر من كاميرا" at={50} size={44} width={1600} color={G.soft} /></div>
          <div style={{marginTop: 70, fontFamily: AR, fontWeight: 800, fontSize: 36, color: G.gold, opacity: lin(pf, 90, 104)}}>الترشيحات دي من Claude، مش من علي — وكل فيديو عليه QR</div>
        </div>
      )}
    </Out>
  );
};

export const courseScenes: Record<string, React.FC<P>> = {ONext,OProof, OName, OLine, OChart, OMeter, OWhy, OChanged, OVerdict, OStamps, Flip, FpsRace, PerSecond, Agenda};
