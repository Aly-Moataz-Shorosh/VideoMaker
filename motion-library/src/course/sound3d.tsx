import React, {useLayoutEffect, useMemo, useRef} from 'react';
import {OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {RoomEnvironment} from 'three/examples/jsm/environments/RoomEnvironment.js';
import {AR, bi, G, lin, spr} from './kit';

// Real 3D concept scenes for the audio-course shorts (Aly 2026-10-26: "الدايافرام اللي في المايك واهتزازه.. الموجة والموشن جرافيك
// يكون 3D"). Each scene fills the short's stage (1040 x 1000 under the step chip) on a transparent ThreeCanvas; time = scene frames.
// They draw exactly what he says: sound = air molecules pushing each other (a wave), a stone in water, a struck metal bar,
// the mic diaphragm moving with the wave, the speaker cone making the same wave again.
const TEAL = '#2EE6B6', VIOLET = '#8B5CF6', GOLD = G.gold;
const W = 1040, H = 1000;

const Env: React.FC = () => {
  const {gl, scene} = useThree();
  useMemo(() => {
    const pm = new THREE.PMREMGenerator(gl);
    scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
    (scene as any).environmentIntensity = 0.4;
  }, [gl, scene]);
  return null;
};
const Stage: React.FC<{z?: number; y?: number; fov?: number; fog?: boolean; children: React.ReactNode}> = ({z = 17, y = 1.5, fov = 38, fog = false, children}) => (
  <ThreeCanvas width={W} height={H} camera={{position: [0, y, z], fov}} gl={{antialias: true, alpha: true}}>
    <Env />
    {fog ? <fog attach="fog" args={['#0A1426', 9, 26]} /> : null}
    <ambientLight intensity={0.35} />
    <directionalLight position={[4, 6, 8]} intensity={2.2} />
    <directionalLight position={[-6, -2, -4]} intensity={0.8} color="#9EC5FF" />
    {children}
  </ThreeCanvas>
);
// Arabic caption pill over the 3D (what is on screen, in his words)
const Tag: React.FC<{text: string; y: number; at?: number; c?: string}> = ({text, y, at = 0, c = TEAL}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, at, 160, 14);
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: y, display: 'flex', justifyContent: 'center', opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * 20}px)`}}>
      <div style={{padding: '10px 26px', borderRadius: 30, background: 'rgba(10,14,22,0.86)', border: `3px solid ${c}`, fontFamily: AR, fontWeight: 900, fontSize: Math.min(44, Math.floor(900 / (text.length * 0.62))),
        color: '#fff', direction: 'rtl', boxShadow: `0 0 30px ${c}55`}}>{bi(text)}</div>
    </div>
  );
};
const Box: React.FC<{children: React.ReactNode; dur: number}> = ({children, dur}) => {
  const f = useCurrentFrame();
  const o = Math.min(lin(f, 0, 10), 1 - lin(f, dur - 8, dur));
  // soft edges: the 3D never ends on a hard rectangle (Aly: nothing cut by edges)
  const mask = 'radial-gradient(ellipse 72% 62% at 50% 45%, #000 62%, transparent 100%)';
  return <div style={{position: 'absolute', left: 20, top: 400, width: W, height: H, opacity: o}}><div style={{position: 'absolute', inset: 0, WebkitMaskImage: mask, maskImage: mask}}>{(children as any[])[0] ?? children}</div>{Array.isArray(children) ? children.slice(1) : null}</div>;
};

// a block of air molecules (instanced spheres). Longitudinal wave: each one moves back and forth along x, so bands get dense / thin.
const Air: React.FC<{nx?: number; ny?: number; nz?: number; x0?: number; x1?: number; amp: (x: number) => number; t: number; k?: number; w?: number; hot?: string}> = (
  {nx = 26, ny = 6, nz = 4, x0 = -5.5, x1 = 5.5, amp, t, k = 2.2, w = 5, hot = TEAL}) => {
  const ref = useRef<THREE.InstancedMesh>(null);
  const n = nx * ny * nz;
  const tmp = useMemo(() => new THREE.Object3D(), []);
  const col = useMemo(() => new THREE.Color(), []);
  useLayoutEffect(() => {
    const m = ref.current;
    if (!m) return;
    let i = 0;
    for (let a = 0; a < nx; a++) for (let b = 0; b < ny; b++) for (let c = 0; c < nz; c++) {
      const bx = x0 + (a / (nx - 1)) * (x1 - x0), by = (b - (ny - 1) / 2) * 0.55, bz = (c - (nz - 1) / 2) * 0.55;
      const A = amp(bx);
      const dx = A * Math.sin(k * bx - w * t);
      tmp.position.set(bx + dx, by, bz);
      tmp.scale.setScalar(0.14);
      tmp.updateMatrix();
      m.setMatrixAt(i, tmp.matrix);
      const dense = A > 0.001 ? Math.max(0, -Math.cos(k * bx - w * t)) : 0; // compression = brighter
      m.setColorAt(i, col.set(VIOLET).lerp(new THREE.Color(hot), dense));
      i++;
    }
    m.instanceMatrix.needsUpdate = true;
    if (m.instanceColor) m.instanceColor.needsUpdate = true;
  });
  return (
    <instancedMesh ref={ref} args={[undefined, undefined, n]}>
      <sphereGeometry args={[1, 14, 10]} />
      <meshPhysicalMaterial roughness={0.35} clearcoat={0.6} />
    </instancedMesh>
  );
};

// ---------- 1. sound = a wave: a glowing 3D ribbon travelling forward ----------
export const Wave3D: React.FC<{dur: number; text?: string}> = ({dur, text = 'الصوت = موجة'}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const grow = lin(f, 0, 30);
  const curve = useMemo(() => new THREE.CatmullRomCurve3(Array.from({length: 2}, () => new THREE.Vector3())), []);
  const pts = Array.from({length: 120}, (_, i) => {
    const u = i / 119, x = -5 + 10 * u * grow;
    return new THREE.Vector3(x, 1.3 * Math.sin(x * 1.6 - t * 4) * Math.exp(-((x + 5) * 0.04)), 0.6 * Math.cos(x * 1.6 - t * 4));
  });
  curve.points = pts;
  return (
    <Box dur={dur}>
      <Stage z={16} y={1.5}>
        <group rotation={[0.25, -0.3 + 0.1 * Math.sin(t / 2), 0]}>
          <mesh><tubeGeometry args={[curve, 240, 0.16, 16, false]} /><meshPhysicalMaterial color={TEAL} emissive={TEAL} emissiveIntensity={0.55} roughness={0.25} clearcoat={1} /></mesh>
          <mesh position={[0, -2.2, 0]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[16, 6]} /><meshStandardMaterial color="#0B1222" transparent opacity={0.6} /></mesh>
        </group>
      </Stage>
      <Tag text={text} y={790} at={12} />
    </Box>
  );
};

// ---------- 2. a stone thrown in water: the wave is not a thing you hold, it is the water moving ----------
export const Ripple3D: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const drop = 1.2; // seconds until the stone hits the water
  const geo = useMemo(() => new THREE.PlaneGeometry(40, 40, 220, 220), []);
  const pos = geo.attributes.position as THREE.BufferAttribute;
  const base = useMemo(() => Float32Array.from(pos.array as Float32Array), [pos]);
  const tt = t - drop;
  for (let i = 0; i < pos.count; i++) {
    const x = base[i * 3], y = base[i * 3 + 1];
    const r = Math.hypot(x, y);
    const front = tt * 3.2;
    const z = tt > 0 && r < front ? 0.45 * Math.sin((r - front) * 2.4) * Math.exp(-r * 0.18) * Math.exp(-(front - r) * 0.12) : 0;
    pos.setZ(i, z);
  }
  pos.needsUpdate = true;
  geo.computeVertexNormals();
  const sy = t < drop ? 5 - 5 * (t / drop) ** 2 : -1.5 - (t - drop) * 0.6;
  return (
    <Box dur={dur}>
      <Stage z={14} y={7} fog>
        <group rotation={[-Math.PI / 2.6, 0, 0]}>
          <mesh geometry={geo}><meshPhysicalMaterial color="#1D6FA3" roughness={0.15} metalness={0.1} clearcoat={1} transmission={0} /></mesh>
        </group>
        {sy > -1.4 ? <mesh position={[0, sy, 0.6]}><dodecahedronGeometry args={[0.5, 0]} /><meshStandardMaterial color="#8A8F98" roughness={0.9} /></mesh> : null}
      </Stage>
      <Tag text="الموجة مش حاجة بتمسكها.. دي حركة المية" y={790} at={50} />
    </Box>
  );
};

// ---------- 3. air molecules pushing each other (optionally a metal bar struck at the left = the source) ----------
export const Molecules3D: React.FC<{dur: number; bar?: boolean; text?: string}> = ({dur, bar = false, text}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const hit = bar ? 1.0 : 0.3;
  const front = Math.max(0, (t - hit) * 3.5);
  const amp = (x: number) => (x + 4.6 < front ? 0.22 : 0);
  const shake = bar && t > hit ? 0.08 * Math.sin(t * 60) * Math.exp(-(t - hit) * 0.8) : 0;
  const stick = bar ? Math.min(1, t / hit) : 1;
  return (
    <Box dur={dur}>
      <Stage z={16} y={2.5}>
        <group rotation={[0.35, -0.4, 0]}>
          <Air amp={amp} t={t} nx={22} x0={bar ? -3.8 : -4.6} x1={4.6} />
          {bar ? (
            <>
              <mesh position={[-4.9 + shake, 0, 0]}><boxGeometry args={[0.35, 3.6, 2.4]} /><meshPhysicalMaterial color="#C9D1DC" metalness={1} roughness={0.25} /></mesh>
              <mesh position={[-5.8 - 1.4 * (1 - stick), 1.0 + 1.2 * (1 - stick), 0]} rotation={[0, 0, -0.9 + 0.9 * stick]}>
                <cylinderGeometry args={[0.09, 0.09, 3, 12]} /><meshStandardMaterial color="#8B5A2B" roughness={0.8} />
              </mesh>
            </>
          ) : null}
        </group>
      </Stage>
      <Tag text={text ?? (bar ? 'الحديدة بتخبط الهوا.. والهوا يزق اللي جنبه' : 'ذرات الهوا بتخبط في بعض.. لحد ما توصلك')} y={790} at={14} />
    </Box>
  );
};

// ---------- 4. the mic: the wave hits a thin diaphragm, it moves, the move is recorded as a line ----------
export const Mic3D: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const front = t * 3.2;
  const amp = (x: number) => (x + 6 < front && x < 0.6 ? 0.2 : 0);
  const dia = 0.28 * Math.sin(2.2 * 1.3 - 5 * t) * (front > 6.6 ? 1 : 0); // the diaphragm follows the air at the mic
  const curve = useMemo(() => new THREE.CatmullRomCurve3([new THREE.Vector3(), new THREE.Vector3(1, 0, 0)]), []);
  const rec = Math.max(0, t - 2.1);
  const N = 90;
  curve.points = Array.from({length: N}, (_, i) => {
    const u = i / (N - 1), age = u * Math.min(rec, 3);
    return new THREE.Vector3(1.6 + u * 2.8, -2.5 + (rec > 0 ? 0.4 * Math.sin(1.3 * 2.2 - 5 * (t - age)) : 0), 0.2);
  });
  return (
    <Box dur={dur}>
      <Stage z={16} y={2}>
        <group rotation={[0.3, -0.85, 0]}>
          <group position={[-1.6, 0.6, 0]}><Air amp={amp} t={t} nx={14} x0={-4.4} x1={0.4} /></group>
          {/* mic capsule cut open: grille ring, the diaphragm (thin gold disc) and the body */}
          <group position={[0.6, 0.6, 0]} rotation={[0, 0, Math.PI / 2]}>
            <mesh position={[0, 0.45, 0]}><sphereGeometry args={[1.45, 20, 12, 0, Math.PI * 2, 0, Math.PI / 2]} /><meshStandardMaterial color="#C9D1DC" wireframe transparent opacity={0.55} /></mesh>
            <mesh position={[0, 0.45, 0]}><torusGeometry args={[1.35, 0.08, 12, 48]} /><meshPhysicalMaterial color="#AEB6C2" metalness={1} roughness={0.3} /></mesh>
            <mesh position={[0, 0.25 + dia, 0]}><cylinderGeometry args={[1.25, 1.25, 0.06, 48]} /><meshPhysicalMaterial color={GOLD} metalness={0.7} roughness={0.25} emissive={GOLD} emissiveIntensity={0.6} /></mesh>
            <mesh position={[0, -1.4, 0]}><cylinderGeometry args={[1.35, 0.9, 3.2, 40, 1, true]} /><meshPhysicalMaterial color="#2A3242" metalness={0.6} roughness={0.35} side={THREE.DoubleSide} /></mesh>
          </group>
        </group>
        {/* to the computer (facing the camera): the diaphragm's movement becomes a line */}
        <group position={[-0.7, -0.1, 2]}>
          <mesh position={[3.0, -2.5, 0]}><boxGeometry args={[3.4, 1.8, 0.1]} /><meshStandardMaterial color="#0E1626" emissive="#0E1626" /></mesh>
          {rec > 0 ? <mesh><tubeGeometry args={[curve, 120, 0.05, 8, false]} /><meshStandardMaterial color={TEAL} emissive={TEAL} emissiveIntensity={0.8} /></mesh> : null}
        </group>
      </Stage>
      <Tag text="الدايفرام: حاجة هشة بتتهز مع الموجة" y={60} at={10} c={GOLD} />
      <Tag text="وحركته بتتسجل على الكمبيوتر" y={880} at={75} />
    </Box>
  );
};

// ---------- 5. the speaker: the saved wave moves the cone, the cone pushes the air the same way, back to your ear ----------
export const Speaker3D: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const cone = 0.18 * Math.sin(5 * t);
  const front = Math.max(0, (t - 0.5) * 3.2);
  const amp = (x: number) => (x - 0.6 < front && x > 0.6 ? 0.2 : 0);
  return (
    <Box dur={dur}>
      <Stage z={16} y={2}>
        <group rotation={[0.3, -1.05, 0]} position={[0.6, 0, 0]}>
          <mesh position={[-3.2, 0.6, 0]}><boxGeometry args={[2.2, 4.4, 3]} /><meshPhysicalMaterial color="#1B2232" roughness={0.5} clearcoat={0.4} /></mesh>
          <mesh position={[-2.05 + cone, 0.6, 0]} rotation={[0, 0, -Math.PI / 2]}><coneGeometry args={[1.5, 0.9, 48, 1, true]} /><meshPhysicalMaterial color="#6B7790" roughness={0.45} side={THREE.DoubleSide} /></mesh>
          <mesh position={[-2.08, 0.6, 0]} rotation={[0, Math.PI / 2, 0]}><torusGeometry args={[1.55, 0.1, 12, 48]} /><meshPhysicalMaterial color={GOLD} metalness={0.8} roughness={0.3} /></mesh>
          <mesh position={[-1.7 + cone, 0.6, 0]}><sphereGeometry args={[0.35, 24, 16]} /><meshPhysicalMaterial color={GOLD} metalness={0.8} roughness={0.25} /></mesh>
          <group position={[0, 0.6, 0]}><Air amp={amp} t={t} nx={16} x0={0.6} x1={5.6} /></group>
        </group>
      </Stage>
      <Tag text="السماعة بتعمل نفس الاهتزازات في الهوا" y={790} at={12} />
    </Box>
  );
};

// ---------- the same scenes rendered in Blender 5.2 (tools/blender/sound_scenes.py): a transparent webm + the same tags ----------
// full = a clip rendered at the whole phone size (1080x1920, Aly 2026-10-26: "يكون مالي الشاشة") -> fills the frame UNDER the band and captions
export const BlenderClip: React.FC<{dur: number; file: string; full?: boolean; tags?: {text: string; y: number; at?: number; c?: string}[]}> = ({dur, file, full = false, tags = []}) => {
  const f = useCurrentFrame();
  return full ? (
  <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, opacity: Math.min(lin(f, 0, 10), 1 - lin(f, dur - 8, dur))}}>
    <OffthreadVideo src={staticFile(file)} transparent muted style={{position: 'absolute', inset: 0, width: 1080, height: 1920}} />
    {tags.map((g, i) => <Tag key={i} text={g.text} y={g.y} at={g.at ?? 12} c={g.c === 'gold' ? GOLD : g.c} />)}
  </div>
) : (
  <Box dur={dur}>
    <OffthreadVideo src={staticFile(file)} transparent muted style={{position: 'absolute', inset: 0, width: W, height: H}} />
    {tags.map((g, i) => <Tag key={i} text={g.text} y={g.y} at={g.at ?? 12} c={g.c === 'gold' ? GOLD : g.c} />)}
  </Box>
);
};

export const sound3d: Record<string, React.FC<any>> = {Wave3D, Ripple3D, Molecules3D, Mic3D, Speaker3D, BlenderClip};
