import React from 'react';
import {AbsoluteFill, Easing, useCurrentFrame} from 'remotion';
import {AR, EN, Pop, lin, rnd, spr, useBeats} from '../film/kit';
import {Ball, Checker, Cursor, Echo, FileCard, Head, Hud, Key, Logo, MONO, Note, Orbit, P, PScene, Pill, Polaroid, SelBox, Term, Ticker, Typed, WinLogo} from './kit';

// ffmpeg short 1 — compress any video with one line (condensed tutorial). Beats = seconds from scene start.
type B = {b?: Record<string, number>; pics?: string};
const pic = (p: string | undefined, f: string) => `${p ?? ''}${f}`;
const Top: React.FC<{text: string; at?: number; y?: number; size?: number}> = ({text, at = 2, y = 190, size = 84}) => (
  <div style={{position: 'absolute', top: y, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Head text={text} at={at} size={size} /></div>
);

// 1. hook: 6 MB .mov -> 90 KB .mp4, "from the sky to the ground"
export const F1Hook: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const kb = at('kb', 3.5), diff = at('diff', 6.2), sky = at('sky', 8.2);
  const up = lin(f, sky, sky + 14, 0, 1, Easing.inOut(Easing.cubic));
  return (
    <PScene>
      <Top text="فيديو *6 ميجا*… بقى _90 كيلو_" at={3} />
      <Pop at={0} x={300} y={760 - up * 130}>
        <div style={{transform: `rotate(${-6 + 3 * Math.sin(f / 12)}deg)`}}><FileCard ext="MOV" name="bee circle 2.mov" size="5.95 MB" w={300} color={P.pink} /></div>
      </Pop>
      <SelBox x={130} y={520 - up * 130} w={340} h={500} at={6} color={P.pink} label="5.95 MB" />
      {f >= kb ? (
        <Pop at={kb} x={780} y={830 + up * 230}>
          <div style={{transform: `rotate(${5 + 3 * Math.sin(f / 10)}deg)`}}><FileCard ext="MP4" name="bee circle FFMPEG.mp4" size="90 KB" w={250} color={P.lime} /></div>
        </Pop>
      ) : null}
      {f >= diff ? <Pop at={diff} x={540} y={760}><Echo text="→" size={170} color={P.lime} at={diff} /></Pop> : null}
      {f >= sky ? (
        <>
          <Pop at={sky} x={560} y={470}><div style={{fontSize: 110}}>☁️</div></Pop>
          <Pop at={sky + 2} x={420} y={1250}><Head text="من *السما*… _للأرض_" size={84} at={0} width={760} /></Pop>
        </>
      ) : null}
      <Pop at={10} x={900} y={420}><div style={{transform: `translateY(${10 * Math.sin(f / 8)}px)`}}><Ball d={150} id="h1" /></div></Pop>
      <Ticker y={1440} text="FFMPEG ✦ COMPRESS ✦ CONVERT" at={4} rot={-3} />
    </PScene>
  );
};

// 2. google -> type FFmpeg
export const F1Google: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const ty = at('type', 2.6), ff = at('ff', 3.1);
  return (
    <PScene>
      <Top text="أول خطوة: *جوجل*" at={2} />
      <Pop at={3} x={540} y={640} from={0.6}>
        <div style={{width: 900, height: 140, background: P.white, borderRadius: 70, border: `5px solid ${P.ink}`, boxShadow: `0 14px 0 ${P.deep}`, display: 'flex', alignItems: 'center',
          gap: 26, padding: '0 40px', direction: 'ltr'}}>
          <Logo name="google" s={70} color={P.blue} />
          <div style={{fontFamily: EN, fontWeight: 700, fontSize: 64, color: P.ink, flex: 1}}><Typed text="FFmpeg" a={ty} b={ty + 12} caret /></div>
          <div style={{fontSize: 56}}>🔍</div>
        </div>
      </Pop>
      <Cursor x={lin(f, 0, ty - 4, 1000, 640)} y={lin(f, 0, ty - 4, 1400, 700)} click={ty - 4} />
      {f >= ff ? (
        <>
          <Pop at={ff} x={540} y={1080}>
            <div style={{width: 300, height: 300, background: P.white, borderRadius: 60, border: `6px solid ${P.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center',
              boxShadow: `0 18px 0 ${P.deep}`}}><Logo name="ffmpeg" s={210} color="#0B8A1F" /></div>
          </Pop>
          <Orbit cx={540} cy={1080} rx={300} ry={110} at={ff + 3} />
          <Pop at={ff + 6} x={540} y={1340}><Echo text="FFmpeg" size={150} color={P.white} at={ff + 6} /></Pop>
        </>
      ) : null}
    </PScene>
  );
};

// 3. ffmpeg.org: Download -> (I want the program itself) -> Windows
export const F1Site: React.FC<B> = ({b, pics}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const dl = at('dl', 1.4), want = at('want', 1.6), win = at('win', 3.6);
  const page2 = f >= want;
  const curX = !page2 ? lin(f, 0, dl - 3, 900, 560) : lin(f, want, win - 3, 560, 540);
  const curY = !page2 ? lin(f, 0, dl - 3, 1350, 960) : lin(f, want, win - 3, 960, 860);
  return (
    <PScene>
      <Top text={page2 ? 'عايز *البرنامج* نفسه' : 'الموقع الرسمي ← *Download*'} at={page2 ? want + 1 : 2} />
      <Pop at={2} x={540} y={820} from={0.7}>
        <div style={{width: 920, height: 660, background: '#1F2226', border: `5px solid ${P.ink}`, boxShadow: `14px 16px 0 ${P.deep}`, direction: 'ltr', position: 'relative', overflow: 'hidden'}}>
          <div style={{height: 64, background: P.white, display: 'flex', alignItems: 'center', gap: 16, padding: '0 22px', fontFamily: EN, fontSize: 28, color: P.ink}}>
            <span style={{color: '#E25'}}>●</span><span style={{color: '#EB2'}}>●</span><span style={{color: '#3B5'}}>●</span>
            <div style={{flex: 1, background: '#ECEAF5', borderRadius: 30, padding: '4px 22px', fontFamily: MONO}}>ffmpeg.org{page2 ? '/download.html' : ''}</div>
          </div>
          {!page2 ? (
            <div style={{padding: 50, color: '#EEE', fontFamily: EN}}>
              <div style={{display: 'flex', alignItems: 'center', gap: 20}}><Logo name="ffmpeg" s={70} color="#3ECF5A" /><span style={{fontSize: 58, fontWeight: 900}}>FFmpeg</span></div>
              <div style={{fontSize: 34, marginTop: 40, lineHeight: 1.4, opacity: 0.85}}>A complete, cross-platform solution to record, convert and stream audio and video.</div>
              <div style={{marginTop: 60, width: 340, height: 100, background: '#5CB85C', borderRadius: 8, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 40, fontWeight: 800,
                transform: `scale(${f >= dl && f < dl + 6 ? 0.94 : 1})`}}>⬇ Download</div>
            </div>
          ) : (
            <div style={{padding: 50, color: '#EEE', fontFamily: EN}}>
              <div style={{fontSize: 44, fontWeight: 900}}>Download FFmpeg</div>
              <div style={{display: 'flex', gap: 26, marginTop: 50}}>
                {[['linux', '#D9534F'], ['win', '#2B7BC4'], ['apple', '#AAA']].map(([n, c], i) => (
                  <div key={n} style={{width: 250, height: 170, background: c, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: lin(f, want + i * 3, want + 6 + i * 3)}}>
                    {n === 'win' ? <WinLogo s={100} color={P.white} /> : <Logo name={n} s={100} color={P.white} />}
                  </div>
                ))}
              </div>
              <div style={{marginTop: 50, display: 'flex', alignItems: 'center', gap: 20, fontSize: 34}}>
                <div style={{background: '#5CB85C', padding: '10px 24px', borderRadius: 8, position: 'relative'}}>Download Source Code
                  <svg width={420} height={80} style={{position: 'absolute', left: -10, top: -10}}><path d={`M10,60 L${lin(f, want + 8, want + 16, 10, 400)},${lin(f, want + 8, want + 16, 60, 10)}`} stroke={P.pink} strokeWidth={12} strokeLinecap="round" /></svg>
                </div>
                <span style={{fontFamily: AR, fontWeight: 900, color: P.pink, opacity: lin(f, want + 14, want + 20)}}>مش ده</span>
              </div>
            </div>
          )}
        </div>
      </Pop>
      {page2 ? <SelBox x={355} y={665} w={262} h={182} at={win} label="Windows" tagBelow /> : <SelBox x={130} y={880} w={352} h={112} at={dl} label="Download" />}
      <Cursor x={curX} y={curY} click={page2 ? win : dl} />
      {pics ? (
        <Pop at={8} x={850} y={1330} rot={6}><Polaroid src={pic(pics, page2 ? 'site_2.png' : 'site_1.png')} still w={330} h={186} note="من الفيديو" /></Pop>
      ) : null}
    </PScene>
  );
};

const FILES = ['avcodec-58.dll', 'avdevice-58.dll', 'avfilter-7.dll', 'avformat-58.dll', 'avutil-56.dll', 'ffmpeg.exe', 'ffplay.exe', 'ffprobe.exe', 'postproc-55.dll', 'swresample-3.dll', 'swscale-5.dll', ''];

// 4. open the bin folder -> all these files -> THE program = ffmpeg.exe
export const F1Bin: React.FC<B> = ({b, pics}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const all = at('all', 2.7), exe = at('exe', 5.7);
  const open = lin(f, 3, 12);
  const foc = lin(f, exe, exe + 10);
  return (
    <PScene>
      <Top text={f < exe ? 'افتح فولدر *bin*' : 'البرنامج هو *ده*'} at={f < exe ? 2 : exe} />
      <Pop at={0} x={540} y={420}>
        <svg width={260} height={200} viewBox="0 0 130 100">
          <path d="M5,20 L45,20 L55,30 L125,30 L125,95 L5,95 Z" fill="#E8A92B" stroke={P.ink} strokeWidth={3} />
          <path d={`M5,${95 - 55 * (1 - open * 0.35)} L125,${95 - 55 * (1 - open * 0.35)} L125,95 L5,95 Z`} fill={P.yellow} stroke={P.ink} strokeWidth={3} />
          <text x={65} y={82} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={22} fill={P.ink}>bin</text>
        </svg>
      </Pop>
      {FILES.map((n, i) => {
        if (!n) return null;
        const x = 200 + (i % 4) * 225, y = 690 + Math.floor(i / 4) * 255;
        const isExe = n === 'ffmpeg.exe';
        const p = spr(f, 30, all + i * 1.5, 220, 14);
        if (f < all + i * 1.5) return null;
        const s = isExe ? 1 + 0.35 * foc : 1;
        return (
          <div key={n} style={{position: 'absolute', left: x - 100, top: y - 100, width: 200, opacity: (isExe ? 1 : 1 - 0.75 * foc) * Math.min(1, p * 2),
            transform: `scale(${(0.4 + 0.6 * p) * s})`, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8, zIndex: isExe ? 2 : 1}}>
            {isExe || n.endsWith('.exe') ? (
              <div style={{width: 120, height: 120, background: isExe ? P.white : '#D8E9FF', border: `4px solid ${P.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                {isExe ? <Logo name="ffmpeg" s={86} color="#0B8A1F" /> : <div style={{width: 80, height: 60, background: '#2B7BC4'}} />}
              </div>
            ) : (
              <div style={{width: 100, height: 120, background: '#EEE', border: `4px solid ${P.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 50}}>⚙️</div>
            )}
            <div style={{fontFamily: EN, fontSize: 24, fontWeight: 700, color: P.white, direction: 'ltr', whiteSpace: 'nowrap'}}>{n}</div>
          </div>
        );
      })}
      <SelBox x={290} y={815} w={270} h={218} at={exe + 4} label="ffmpeg.exe" />
      {f >= exe ? <Pop at={exe + 8} x={540} y={1440}><Echo text="FFMPEG.EXE" size={120} color={P.lime} at={exe + 8} /></Pop> : null}
      {pics && f < exe ? <Pop at={all + 20} x={820} y={1420} rot={-5}><Polaroid src={pic(pics, 'bin.png')} still w={330} h={186} pos="40% 10%" zoom={1.6} note="الفولدر عندي" /></Pop> : null}
    </PScene>
  );
};

// 5. what it does: compresses + converts, easily
export const F1What: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const press = at('press', 0.9), conv = at('conv', 2.8), easy = at('easy', 6.6);
  const sq = f < press ? 1 : 1 - 0.55 * lin(f, press, press + 12, 0, 1, Easing.out(Easing.back(2)));
  const fmts = ['MP4', 'MKV', 'AVI', 'GIF', 'MP3', 'MOV'];
  return (
    <PScene>
      <Top text="بيعمل ايه؟" at={0} size={96} />
      <Pop at={press} x={290} y={650}><Pill text="بيضغط 🗜️" size={56} bg={P.pink} /></Pop>
      <Pop at={press + 2} x={290} y={960}>
        <div style={{transform: `scale(${sq + (1 - sq) * 0.3}, ${sq})`, transformOrigin: '50% 100%'}}><FileCard ext="MOV" w={240} color={P.pink} /></div>
      </Pop>
      {f >= press + 14 ? <Pop at={press + 14} x={290} y={1150}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 60, color: P.lime, direction: 'ltr'}}>↓ size</div></Pop> : null}
      {f >= conv ? (
        <>
          <Pop at={conv} x={790} y={650}><Pill text="بيحوّل convert 🔁" size={50} /></Pop>
          {fmts.map((t, i) => {
            const a = (f - conv) / 18 + (i / fmts.length) * Math.PI * 2;
            const p = spr(f, 30, conv + 3 + i * 2);
            return (
              <div key={t} style={{position: 'absolute', left: 790 + Math.cos(a) * 190 * p - 75, top: 960 + Math.sin(a) * 190 * p - 38, width: 150, height: 76, background: i % 2 ? P.lime : P.white,
                border: `4px solid ${P.ink}`, borderRadius: 40, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: EN, fontWeight: 900, fontSize: 38, color: P.ink, opacity: p}}>{t}</div>
            );
          })}
          <Pop at={conv + 2} x={790} y={960}><div style={{width: 150, height: 150, borderRadius: 30, background: P.white, border: `5px solid ${P.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <Logo name="ffmpeg" s={100} color="#0B8A1F" /></div></Pop>
        </>
      ) : null}
      {f >= easy ? <Pop at={easy} x={540} y={1360} rot={-4}><Pill text="بسهولة جدًا ✓" size={76} bg={P.yellow} /></Pop> : null}
    </PScene>
  );
};

// 6. open CMD from the folder's address bar: type cmd + Enter
export const F1Cmd: React.FC<B & {ways?: boolean}> = ({b, ways}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const click = at('search', 2.3), ty = at('type', 4.1), en = at('enter', 5.5);
  const typing = f >= ty;
  return (
    <PScene>
      <Top text="افتح *CMD* من الفولدر نفسه" at={1} />
      <Pop at={1} x={540} y={640} from={0.7}>
        <div style={{width: 960, height: 120, background: P.white, border: `5px solid ${P.ink}`, boxShadow: `0 14px 0 ${P.deep}`, display: 'flex', alignItems: 'center', gap: 18, padding: '0 26px',
          direction: 'ltr', fontFamily: MONO, fontSize: 38, color: P.ink}}>
          <span style={{fontSize: 44}}>📁</span>
          {typing ? <Typed text="cmd" a={ty} b={ty + 9} /> : (
            <span style={{background: f >= click ? '#9EC5FF' : undefined, whiteSpace: 'nowrap', overflow: 'hidden'}}>…\ffmpeg\bin</span>
          )}
        </div>
      </Pop>
      <SelBox x={60} y={580} w={960} h={120} at={click} label="address bar" />
      <Cursor x={lin(f, 0, click - 2, 900, 420)} y={lin(f, 0, click - 2, 1250, 660)} click={click} />
      <Pop at={ty - 2} x={540} y={1060}><Key label="Enter ↵" w={420} h={190} press={en} color={P.lime} size={70} /></Pop>
      {f >= en + 4 ? <Pop at={en + 4} x={540} y={1380}><Note text="هيفتح الشاشة السودا" size={72} /></Pop> : null}
      {ways && f >= en + 14 ? (
        <div style={{position: 'absolute', top: 1220, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 24, direction: 'ltr'}}>
          <Pill text="أو: سيرش الويندوز 🔍" size={40} bg={P.white} /><Pill text="Win + R" size={40} dir="ltr" font={EN} bg={P.yellow} />
        </div>
      ) : null}
    </PScene>
  );
};

// 7. the command: ffmpeg + SPACE + -i (dash = minus, small i)
export const F1Line: React.FC<B> = ({b, pics}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const nm = at('name', 1.9), sp = at('space', 3.9), sp2 = at('space2', 5.2), dash = at('dash', 5.7), mi = at('minus', 8.3), ii = at('i', 8.9);
  return (
    <PScene>
      <Top text="اكتب الأمر 👇" at={0} />
      <Pop at={0} x={540} y={600} from={0.8}>
        <Term w={980} h={420} size={48}>
          <span style={{color: '#9A9A9A'}}>C:\…\bin&gt;</span>
          <Typed text="ffmpeg" a={nm} b={nm + 10} color={P.white} caret={false} />
          {f >= sp ? <span style={{background: f < sp2 + 20 ? 'rgba(184,255,60,0.35)' : undefined}}> </span> : null}
          {f >= dash ? <Typed text="-i" a={dash} b={dash + 6} color={P.lime} /> : null}
        </Term>
      </Pop>
      <Pop at={sp - 3} x={540} y={1020} out={dash + 30}><Key label="SPACE" w={600} h={150} press={sp} size={60} /></Pop>
      {f >= sp ? <Pop at={sp + 4} x={540} y={1260} out={dash + 30}><Head text="مسافة… *مهمة جدًا*" size={80} /></Pop> : null}
      {f >= dash + 30 ? (
        <>
          <Pop at={dash + 30} x={380} y={1080}><Echo text="-i" size={260} color={P.lime} at={dash + 30} /></Pop>
          <Pop at={Math.max(dash + 34, mi)} x={750} y={1010} rot={-6}><Note text="شَرطة = minus" size={70} /></Pop>
          <Pop at={Math.max(dash + 40, ii)} x={750} y={1150} rot={4}><Pill text="i صغيرة small" size={52} dir="rtl" /></Pop>
          <Pop at={dash + 44} x={540} y={1340}><Pill text="-i = input" size={56} bg={P.white} dir="ltr" font={EN} /></Pop>
        </>
      ) : null}
    </PScene>
  );
};

// 8. drag the video file in -> "path\name.mov"
export const F1In: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const drop = at('drop', 1.2), fmt = at('fmt', 3.0);
  const px = lin(f, 4, drop, 0, 1, Easing.inOut(Easing.cubic));
  return (
    <PScene>
      <Top text="اسحب الفيديو *جوّه*" at={0} />
      <Pop at={0} x={540} y={600} from={1}>
        <Term w={980} h={420} size={44}>
          <span style={{color: '#9A9A9A'}}>C:\…\bin&gt;</span><span>ffmpeg </span><span style={{color: P.lime}}>-i </span>
          {f >= drop ? <Typed text={'"C:\\Users\\pc\\Desktop\\bee circle 2'} a={drop} b={drop + 8} color={P.yellow} caret={false} /> : null}
          {f >= drop + 8 ? <span style={{color: P.pink, background: f >= fmt ? 'rgba(255,79,168,0.25)' : undefined}}>.mov</span> : null}
          {f >= drop + 8 ? <span style={{color: P.yellow}}>"</span> : null}
        </Term>
      </Pop>
      {f < drop + 2 ? (
        <div style={{position: 'absolute', left: 540 - 110 + (200 - 540) * (1 - px) * 0, top: lin(f, 4, drop, 1250, 650) - 140, opacity: 1 - lin(f, drop - 2, drop + 2), transform: `rotate(${(1 - px) * -10}deg) scale(${1 - 0.4 * px})`}}>
          <FileCard ext="MOV" w={220} color={P.pink} />
        </div>
      ) : null}
      <Cursor x={lin(f, 4, drop, 560, 560)} y={lin(f, 4, drop, 1290, 690)} />
      {f >= fmt ? (
        <>
          <Pop at={fmt} x={540} y={1130}><Head text="اسم الفيديو *.الامتداد*" size={80} /></Pop>
          <Pop at={fmt + 3} x={540} y={1320}><Pill text={'" … "  الكوتيشن بتتعمل لوحدها'} size={44} bg={P.white} /></Pop>
        </>
      ) : null}
    </PScene>
  );
};

// 9. THE trick: output name ends with .mp4 instead of .mov
export const F1Trick: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const trick = at('trick', 1.2), mov = at('mov', 3.8), mp4 = at('mp4', 5.5);
  return (
    <PScene>
      <Top text="التريكة *كلها* هنا 👇" at={trick} size={90} />
      <Pop at={0} x={540} y={560} from={1}>
        <Term w={980} h={330} size={36}>
          <span>ffmpeg </span><span style={{color: P.lime}}>-i </span><span style={{color: P.yellow}}>"bee circle 2.mov"</span>{' '}
          <Typed text={'"bee circle FFMPEG'} a={4} b={trick + 6} color={P.teal} caret={false} />
          {f >= mp4 ? <span style={{color: P.lime, fontWeight: 700}}>.mp4"</span> : f >= mov ? <span style={{color: P.pink}}>.mov"</span> : null}
        </Term>
      </Pop>
      {f >= mov ? (
        <Pop at={mov} x={300} y={1040}>
          <div style={{position: 'relative'}}>
            <Echo text=".MOV" size={170} color={P.pink} at={mov} />
            <svg width={420} height={220} style={{position: 'absolute', left: -20, top: -20, overflow: 'visible'}}>
              <path d={`M10,20 L${lin(f, mov + 8, mov + 14, 10, 400)},${lin(f, mov + 8, mov + 14, 20, 200)}`} stroke={P.ink} strokeWidth={22} strokeLinecap="round" />
              <path d={`M400,20 L${lin(f, mov + 12, mov + 18, 400, 10)},${lin(f, mov + 12, mov + 18, 20, 200)}`} stroke={P.ink} strokeWidth={22} strokeLinecap="round" />
            </svg>
          </div>
        </Pop>
      ) : null}
      {f >= mp4 ? (
        <>
          <Pop at={mp4} x={760} y={1210}><Echo text=".MP4" size={210} color={P.lime} at={mp4} /></Pop>
          <Orbit cx={760} cy={1210} rx={290} ry={120} at={mp4 + 4} color={P.white} w={10} />
        </>
      ) : null}
      <Pop at={trick + 8} x={800} y={860} rot={-8}><Note text="آخر اسم الفيديو الجديد ✍️" size={56} color={P.yellow} /></Pop>
    </PScene>
  );
};

// 10. Enter
export const F1Enter: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const en = at('enter', 1.6);
  return (
    <PScene>
      <Top text="واضغط *Enter*" at={0} size={100} />
      <Pop at={0} x={540} y={870} from={0.5}><Key label="ENTER ↵" w={760} h={300} press={en} color={P.lime} size={120} /></Pop>
      <Cursor x={lin(f, 0, en - 2, 950, 640)} y={lin(f, 0, en - 2, 1400, 900)} click={en} />
      <Pop at={4} x={170} y={420}><div style={{transform: `translateY(${8 * Math.sin(f / 6)}px)`}}><Ball d={130} id="en" /></div></Pop>
    </PScene>
  );
};

const LOG = ['[libx264] frame I:1  Avg QP:9.25  size: 2577', '[libx264] frame P:33 Avg QP:20.74 size: 1757', '[libx264] frame B:26 Avg QP:28.21 size: 1129',
  'video:88kB audio:0kB muxing overhead: 2.16%', '[libx264] kb/s:119.86'];

// 11. result: 90 KB vs 6 MB — huge difference
export const F1End: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const kb = at('kb', 0.6), mb = at('mb', 2.0), diff = at('diff', 3.0);
  const big = lin(f, mb, mb + 14, 0, 1, Easing.out(Easing.cubic));
  return (
    <PScene>
      <div style={{position: 'absolute', top: 150, left: 60, right: 60, fontFamily: MONO, fontSize: 26, color: P.lime, direction: 'ltr', opacity: 1 - lin(f, 14, 22)}}>
        {LOG.map((l, i) => <div key={i} style={{opacity: lin(f, i * 2, i * 2 + 3)}}>{l}</div>)}
      </div>
      <div style={{position: 'absolute', top: 200, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: lin(f, 18, 22)}}><Head text="النتيجة" at={18} size={96} /></div>
      {/* bars */}
      <div style={{position: 'absolute', left: 170, bottom: 620, width: 300, height: 760 * big, background: P.pink, border: `5px solid ${P.ink}`, boxShadow: `12px 0 0 ${P.deep}`}} />
      <div style={{position: 'absolute', left: 610, bottom: 620, width: 300, height: Math.max(10, 11 * lin(f, kb, kb + 8)), background: P.lime, border: `5px solid ${P.ink}`}} />
      <div style={{position: 'absolute', left: 170, width: 300, bottom: 540, textAlign: 'center', fontFamily: EN, fontWeight: 900, fontSize: 52, color: P.white, direction: 'ltr'}}>.MOV</div>
      <div style={{position: 'absolute', left: 610, width: 300, bottom: 540, textAlign: 'center', fontFamily: EN, fontWeight: 900, fontSize: 52, color: P.white, direction: 'ltr'}}>.MP4</div>
      {f >= mb ? <Pop at={mb} x={320} y={1300 - 760 * big - 60}><Pill text="6 MB" dir="ltr" font={EN} bg={P.white} size={58} /></Pop> : null}
      {f >= kb ? <Pop at={kb} x={760} y={1210}><Pill text="90 KB" dir="ltr" font={EN} size={58} /></Pop> : null}
      {f >= diff ? (
        <>
          <Pop at={diff} x={760} y={900} rot={-6}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 150, color: P.lime, textShadow: `0 10px 0 ${P.deep}`, direction: 'ltr'}}>-98%</div></Pop>
          <Pop at={diff + 4} x={760} y={1050}><Head text="فرق *شاسع*" size={74} at={0} /></Pop>
        </>
      ) : null}
      <Pop at={6} x={540} y={1460}><Pill text="codec: H.264 (libx264)" dir="ltr" font={MONO} bg={P.lav} size={36} /></Pop>
    </PScene>
  );
};
