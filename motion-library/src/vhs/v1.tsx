import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, Pop, Scene, Stamp, Tag, Title, Count, Flash, arrowPath, Scribble, useBeats} from '../film/kit';
import {BluePanel, Box, Cable, Cassette, Chip, Crt, Footage, Laptop, Rgb, RcaPlug, SmallTape, V, Vcr, blink, lin, spr} from './kit';

// Short 1 — convert your tapes to digital at home (his own way: AV -> HDMI converter -> capture card -> USB -> PC).
export const PJ = 'projects/2026-10-09 shorts vhstodigital/';
export const SRC = PJ + 'desk.mp4';
export const CLIP = (n: string) => PJ + n + '.mp4'; // cropped real footage (work/scripts/clips.sh)
type B = {b?: Record<string, number>};

export const SeriesTag: React.FC<{text?: string}> = ({text = 'VHS ➜ DIGITAL'}) => (
  <Pop at={0} x={540} y={160} from={0.6}><div style={{background: V.blue, padding: '8px 26px', borderRadius: 10, border: '4px solid #000'}}>
    <Rgb size={46} font={EN} dir="ltr">{text}</Rgb></div></Pop>
);

// Hook behind Aly (he is at the bottom): big title on top, tape(s) around.
export const Hook: React.FC<{title: string; children?: React.ReactNode; tag?: string; top?: number; size?: number; stamp?: string; stampAt?: number; noTag?: boolean}> = ({title, children, tag, top = 250, size = 88, stamp, stampAt = 30, noTag}) => (
  <AbsoluteFill>
    {noTag ? null : <SeriesTag text={tag} />}
    <div style={{position: 'absolute', top, left: 50, right: 50, display: 'flex', justifyContent: 'center'}}>
      <Title text={title} size={size} at={2} stagger={2} stroke />
    </div>
    {children}
    {stamp ? <Pop at={stampAt} x={540} y={top + 420}><Stamp text={stamp} at={0} size={110} color={V.yellow} rot={-6} /></Pop> : null}
  </AbsoluteFill>
);

// Generic title behind Aly (he is at the bottom). props: title, stamp (beat 'stamp').
export const VTitle: React.FC<B & {title: string; stamp?: string; noTag?: boolean}> = ({b, title, stamp, noTag}) => {
  const at = useBeats(b);
  return <Hook title={title} stamp={stamp} stampAt={at('stamp', 1)} noTag={noTag} />;
};

// Full signal chain, vertical: VCR -> RCA (red/white/yellow) -> AV->HDMI -> HDMI -> capture card -> USB -> laptop.
// k = steps shown (0..6, fractional = drawing), pulse = signal flowing.
export const Chain: React.FC<{k: number; flow?: number; y0?: number; small?: boolean}> = ({k, flow = 0, y0 = 300}) => {
  const st = (i: number) => Math.max(0, Math.min(1, k - i));
  const yV = y0, yC = y0 + 420, yK = y0 + 760, yL = y0 + 1180;
  return (
    <svg width={1080} height={1920} style={{position: 'absolute'}}>
      {st(0) > 0 ? <g opacity={Math.min(1, st(0) * 2)}><Vcr x={540} y={yV} s={1.15} led={1} play /></g> : null}
      {[V.red, V.rcaW, V.yellow].map((c, i) => (
        <Cable key={c} a={[380 + i * 60, yV + 110]} b={[440 + i * 60, yC - 90]} color={c} p={st(1)} w={13} flow={flow} sag={60} />
      ))}
      {st(2) > 0 ? <g opacity={Math.min(1, st(2) * 2)}><Box x={540} y={yC} w={420} h={150} label="AV ➜ HDMI" sub="كونفرتر" glow={flow} /></g> : null}
      <Cable a={[540, yC + 80]} b={[540, yK - 70]} color="#111" p={st(3)} w={22} flow={flow} sag={0} />
      {st(4) > 0 ? <g opacity={Math.min(1, st(4) * 2)}><Box x={540} y={yK} w={420} h={130} label="CAPTURE CARD" sub="كارت تسجيل" color="#3A2C4A" glow={flow} /></g> : null}
      <Cable a={[540, yK + 70]} b={[540, yL - 320]} color="#777" p={st(5)} w={12} flow={flow} sag={0} />
      {st(6) > 0 ? (
        <g opacity={Math.min(1, st(6) * 2)}>
          <Laptop x={540} y={yL} s={1.05}>
            <div style={{position: 'absolute', inset: 0, background: V.blue, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
              <div style={{fontFamily: EN, fontWeight: 900, fontSize: 56, color: V.white, direction: 'ltr'}}>● REC</div>
            </div>
          </Laptop>
        </g>
      ) : null}
    </svg>
  );
};

export const V1Hook: React.FC<B & {title?: string; stamp?: string}> = ({b, title = 'شرايطك القديمة *ملهاش نسخة تانية*', stamp}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  return (
    <Hook title={title} stamp={stamp} stampAt={at('stamp', 3)}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <g opacity={lin(f, 10, 20)}><Cassette x={540 + 20 * Math.sin(f / 20)} y={lin(f, 10, 30, 200, 600)} s={0.7} rot={-6 + 3 * Math.sin(f / 15)} spin={f * 4} label="فرح ١٩٩٨" /></g>
      </svg>
    </Hook>
  );
};

// Big VHS + small Hi8 camera tape -> "آثار" stamp -> must become digital.
export const V1Tapes: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  return (
    <Scene>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <g opacity={lin(f, 0, 8)}><Cassette x={540} y={560} s={1.4} rot={-4} spin={f * 3} label="VHS" /></g>
        {f >= at('hi8', 2) ? <g transform={`translate(0,${(1 - spr(f, 30, at('hi8', 2))) * 400})`}><SmallTape x={760} y={1000} s={1.5} rot={8} spin={f * 5} /></g> : null}
      </svg>
      <Pop at={6} x={300} y={310} rot={-5}><Tag text="الشريط الكبير" bg={V.white} size={54} /></Pop>
      <Pop at={at('hi8', 2) + 6} x={360} y={1130} rot={4}><Tag text="شريط الكاميرات السوني" bg={V.yellow} size={50} /></Pop>
      <Pop at={at('old', 5)} x={540} y={1340}><Stamp text="آثار!" at={0} size={130} color={V.red} /></Pop>
    </Scene>
  );
};

// Idea: the tape becomes an "input device" for the computer, like a webcam; the PC watches it in real time.
export const V1Idea: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const p = lin(f, at('cam', 1), at('cam', 1) + 18);
  return (
    <Scene>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <Cassette x={300} y={560} s={0.95} spin={f * 4} label="VHS" />
        <Scribble d={arrowPath(560, 700, 680, 930, 0.2)} p={lin(f, 6, 20)} color={V.yellow} w={12} width={1080} height={1920} />
        <Laptop x={600} y={1330} s={1.45}>
          <div style={{position: 'absolute', inset: 0, background: '#111'}}>
            <div style={{position: 'absolute', inset: 0, background: V.blue, opacity: lin(f, 14, 24)}} />
            <div style={{position: 'absolute', left: 16, top: 12, fontFamily: EN, fontWeight: 900, fontSize: 30, color: V.white, opacity: lin(f, 14, 24), direction: 'ltr'}}>NEW INPUT ▶</div>
          </div>
        </Laptop>
        {/* webcam icon */}
        <g transform={`translate(860,560) scale(${p * 1.2})`} opacity={p}>
          <circle r={90} fill="#222" stroke="#000" strokeWidth={6} /><circle r={52} fill="#0B0B12" stroke="#555" strokeWidth={6} />
          <circle r={22} fill={V.cyan} opacity={0.7} /><rect x={-60} y={90} width={120} height={30} rx={10} fill="#222" />
        </g>
      </svg>
      <Pop at={at('cam', 1) + 4} x={760} y={340} rot={4}><Tag text="زي كاميرا الويب" bg={V.yellow} size={52} /></Pop>
      <Pop at={at('pc', 3)} x={540} y={1480}><Tag text="الكمبيوتر بيتفرج عليه ويسجّله" bg={V.white} size={56} /></Pop>
    </Scene>
  );
};

// No copy-paste: a 3-hour tape takes 3 hours. Clock counting.
export const V1Hours: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  return (
    <Scene>
      <div style={{position: 'absolute', top: 400, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
        <BluePanel w={940} h={440}>
          <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 10}}>
            <Rgb size={60} font={EN} dir="ltr">● REC</Rgb>
            <Count to={180} a={6} b={at('n', 3) + 20} size={190} color={V.white} suffix=" min" />
          </div>
        </BluePanel>
      </div>
      <Pop at={at('n', 3)} x={540} y={1050}><Title text="شريط *3 ساعات* = تسجيل 3 ساعات" size={86} stroke /></Pop>
      <Pop at={at('copy', 5)} x={540} y={1360} rot={-4}><Stamp text="مفيش Copy Paste" at={0} size={96} color={V.red} /></Pop>
    </Scene>
  );
};

// His own way, part 1: real shot of the RCA plugs into the converter + the diagram building.
export const V1Convert: React.FC<B & {clip?: number; pos?: string; zoom?: number}> = ({b, clip = 12, pos = '50% 50%', zoom = 1}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  return (
    <Scene>
      <Pop at={0} x={540} y={520} from={0.8}><Crt w={860}><Footage src={SRC} start={clip} pos={pos} zoom={zoom} /></Crt></Pop>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {[V.red, V.rcaW, V.yellow].map((c, i) => <RcaPlug key={c} x={lin(f, at('rca', 1), at('rca', 1) + 14, 120, 400)} y={1060 + i * 70} color={c} s={1.6} />)}
        {f >= at('box', 2.5) ? <g opacity={lin(f, at('box', 2.5), at('box', 2.5) + 8)}><Box x={700} y={1130} w={360} h={230} label="AV ➜ HDMI" sub="كونفرتر" glow={blink(f, at('box', 2.5)) * 0.8} /></g> : null}
      </svg>
      <Pop at={at('hdmi', 4)} x={540} y={1360}><Chip text="HDMI OUT" bg={V.yellow} size={60} /></Pop>
    </Scene>
  );
};

// Why a capture card: the laptop's HDMI is an OUTPUT (it treats it as a new monitor) -> X; capture card -> USB -> ✓.
export const V1Why: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const x1 = at('no', 2), cap = at('cap', 5);
  return (
    <Scene>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <Laptop x={540} y={900} s={1.5}>
          <div style={{position: 'absolute', inset: 0, background: '#0E1030', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <div style={{fontFamily: AR, fontWeight: 900, fontSize: 44, color: V.white}}>شاشة عرض 🖥️</div>
          </div>
        </Laptop>
        <Cable a={[100, 480]} b={[250, 860]} color="#111" p={lin(f, 4, 18)} w={26} sag={40} />
        {f < cap ? null : (
          <g opacity={lin(f, cap, cap + 8)}>
            <Box x={540} y={1250} w={480} h={160} label="CAPTURE CARD" sub="كارت تسجيل" color="#3A2C4A" glow={1} />
            <Cable a={[540, 1335]} b={[540, 1440]} color="#777" p={lin(f, cap + 8, cap + 20)} w={14} flow={1} sag={0} />
          </g>
        )}
      </svg>
      <Pop at={6} x={250} y={400} rot={-6}><Chip text="HDMI" size={64} /></Pop>
      {f >= x1 && f < cap ? <Pop at={x1} x={540} y={760}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 420, color: V.red, textShadow: '0 10px 0 #000', lineHeight: 1}}>✕</div></Pop> : null}
      <Pop at={6} x={540} y={1260} rot={-3} out={cap}><Tag text="الكمبيوتر بيعتبره شاشة عرض 🖥️" bg={V.white} size={54} /></Pop>
      <Pop at={x1 + 4} x={700} y={420} rot={5} out={cap}><Tag text="ده خروج… مش دخول" bg={V.yellow} size={58} /></Pop>
      <Pop at={cap + 18} x={540} y={1470}><Chip text="USB ➜ PC  ✓" bg={V.green} size={56} /></Pop>
    </Scene>
  );
};

// Recap: the whole chain builds step by step on his words, then the signal flows.
export const V1Chain: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const steps = ['vcr', 'av', 'conv', 'hdmi', 'cap', 'usb', 'pc'];
  let k = 0;
  steps.forEach((s, i) => { k = Math.max(k, Math.min(i + 1, lin(f, at(s, i * 0.8), at(s, i * 0.8) + 8, i, i + 1))); });
  return (
    <Scene>
      <Chain k={k} flow={k >= 7 ? 1 : 0} y0={260} />
      <Flash at={at('pc', 5.6) + 8} color={V.cyan} />
    </Scene>
  );
};

// Result: real capture on the PC, colour stays, no black & white.
export const V1Result: React.FC<B & {clip?: number; pos?: string; zoom?: number; tag?: string}> = ({b, clip = 0, pos = '50% 50%', zoom = 1.06, tag = 'ألوان ثابتة… من غير أبيض وأسود'}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  return (
    <Scene>
      <Pop at={0} x={540} y={640} from={0.7}><Crt w={980} knob={false}><Footage src={CLIP('mine_obs')} start={clip} pos={pos} zoom={zoom} /></Crt></Pop>
      <div style={{position: 'absolute', left: 120, top: 330, opacity: blink(f, 4, 15)}}><Rgb size={52} font={EN} dir="ltr" color={V.red}>● REC</Rgb></div>
      <Pop at={at('color', 1.5)} x={540} y={1180} rot={-3}><Tag text={tag} bg={V.yellow} size={54} /></Pop>
      <Pop at={at('hd', 3)} x={540} y={1330}><Chip text="HD ✓" bg={V.green} size={64} /></Pop>
    </Scene>
  );
};

// End behind Aly: once it is digital — YouTube, flash, hard disk, send to family.
export const V1End: React.FC<B & {title?: string; items?: string[][]}> = ({b, title = 'بقت *ديجيتال* اعمل بيها اللي انت عايزه', items = [['يوتيوب', '▶', V.red], ['فلاشة', '💾', V.yellow], ['هارد', '🗄️', V.white]]}) => {
  const at = useBeats(b);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 220, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Title text={title} size={76} stroke /></div>
      {items.map(([t, ic, c], i) => (
        <Pop key={t} at={at('i' + i, 0.6 + i * 0.5)} x={220 + i * 320} y={620} rot={(i - 1) * 5}>
          <div style={{width: 250, height: 210, borderRadius: 30, background: c, border: '5px solid #000', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 16px 30px rgba(0,0,0,0.5)'}}>
            <div style={{fontSize: 90}}>{ic}</div>
            <div style={{fontFamily: AR, fontWeight: 900, fontSize: 46, color: '#111'}}>{t}</div>
          </div>
        </Pop>
      ))}
    </AbsoluteFill>
  );
};

// Two programs to record with: OBS Studio (free) or the program on the EasyCap CD ("VHS to DVD").
const AppWin: React.FC<{title: string; color: string; children?: React.ReactNode}> = ({title, color, children}) => (
  <div style={{width: 820, height: 330, background: '#1B1D26', border: '5px solid #000', borderRadius: 18, overflow: 'hidden', boxShadow: '0 24px 44px rgba(0,0,0,0.6)'}}>
    <div style={{height: 64, background: color, display: 'flex', alignItems: 'center', padding: '0 24px', gap: 14, direction: 'ltr'}}>
      {[V.red, V.yellow, V.green].map((c) => <div key={c} style={{width: 20, height: 20, borderRadius: 10, background: c}} />)}
      <div style={{fontFamily: EN, fontWeight: 900, fontSize: 36, color: V.white, marginLeft: 12}}>{title}</div>
    </div>
    <div style={{position: 'relative', height: 266}}>{children}</div>
  </div>
);
export const V1Soft: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  return (
    <Scene>
      <div style={{position: 'absolute', top: 230, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Title text="وتسجّل على *أي برنامج*" size={84} stroke /></div>
      <Pop at={at('obs', 1.5)} x={540} y={640} rot={-2}>
        <AppWin title="OBS Studio" color="#302E3D">
          <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 30, direction: 'ltr'}}>
            <svg width={150} height={150} viewBox="-50 -50 100 100"><circle r={46} fill="#E8E8EE" /><circle r={38} fill="#302E3D" />
              {[0, 120, 240].map((a) => <circle key={a} cx={20 * Math.cos(((a + f * 2) * Math.PI) / 180)} cy={20 * Math.sin(((a + f * 2) * Math.PI) / 180)} r={13} fill="#E8E8EE" />)}</svg>
            <div style={{fontFamily: EN, fontWeight: 900, fontSize: 64, color: V.white}}>● REC</div>
          </div>
        </AppWin>
      </Pop>
      <Pop at={at('dvd', 2.5)} x={540} y={1060} rot={2}>
        <AppWin title="VHS to DVD" color="#1F6E3A">
          <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 26, direction: 'rtl'}}>
            <div style={{fontSize: 120}}>💿</div>
            <div style={{fontFamily: AR, fontWeight: 900, fontSize: 52, color: V.white, lineHeight: 1.3}}>البرنامج اللي<br />بييجي مع الوصلة</div>
          </div>
        </AppWin>
      </Pop>
    </Scene>
  );
};
