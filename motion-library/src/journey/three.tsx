import React, {useMemo} from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {RoomEnvironment} from 'three/examples/jsm/environments/RoomEnvironment.js';
import {lin, spr} from './kit';

// Real 3D for the Journey shorts (Aly 2026-10-22: "الرسومات عايزها احسن و اقوى و ممكن تستخدم three js").
// Every component = a transparent ThreeCanvas of size w x h; frames are scene frames.

const Env: React.FC = () => {
  const {gl, scene} = useThree();
  useMemo(() => {
    const pm = new THREE.PMREMGenerator(gl);
    scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
    (scene as any).environmentIntensity = 0.35; // colours stay saturated (full env washed them to pastel)
  }, [gl, scene]);
  return null;
};
const Lights: React.FC<{warm?: string; cool?: string}> = ({warm = '#FFFFFF', cool = '#9EC5FF'}) => (
  <>
    <ambientLight intensity={0.35} />
    <directionalLight position={[3, 5, 6]} intensity={2.2} color={warm} />
    <directionalLight position={[-5, -1, -3]} intensity={0.7} color={cool} />
  </>
);
const Canvas: React.FC<{w: number; h: number; z?: number; fov?: number; y?: number; children: React.ReactNode}> = ({w, h, z = 10, fov = 35, y = 0, children}) => (
  <ThreeCanvas width={w} height={h} camera={{position: [0, y, z], fov}} gl={{antialias: true, alpha: true}}>
    <Env />
    {children}
  </ThreeCanvas>
);
const mix = (a: string, b: string, t: number) => new THREE.Color(a).lerp(new THREE.Color(b), t);
const inHeart = (x: number, y: number) => (x * x + y * y - 1) ** 3 - x * x * y ** 3 <= 0;

// ---------- pixel heart as glossy voxels (raster = little coloured squares); zoom 0..1 flies the camera into the blocks ----------
export const VoxelHeart: React.FC<{w: number; h: number; n?: number; t0?: number; zoom?: number; spin?: boolean; gap?: number}> = ({w, h, n = 14, t0 = 0, zoom = 0, spin = true, gap = 0.08}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const cells = useMemo(() => {
    const out: {x: number; y: number; c: THREE.Color; k: number}[] = [];
    for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) {
      const x = ((c + 0.5) / n) * 2.6 - 1.3, y = 1.25 - ((r + 0.5) / n) * 2.6;
      if (inHeart(x, y)) out.push({x: c - n / 2 + 0.5, y: n / 2 - r - 0.5, c: mix('#E8175D', '#F7931E', c / n), k: r + c});
    }
    return out;
  }, [n]);
  const z = 26 - 22 * zoom;
  return (
    <Canvas w={w} h={h} z={z} fov={32}>
      <Lights />
      <group rotation={[0.18 * Math.sin(f / 50), spin ? 0.5 * Math.sin(f / 40) : 0, 0]}>
        {cells.map((q, i) => {
          const p = spr(f, fps, t0 + q.k * 0.9, 160, 12);
          if (p <= 0.001) return null;
          return (
            <mesh key={i} position={[q.x, q.y + (1 - p) * 9, (1 - p) * 4]} scale={Math.max(0.01, p) * (1 - gap)}>
              <boxGeometry args={[1, 1, 1]} />
              <meshPhysicalMaterial color={q.c} roughness={0.4} clearcoat={0.6} clearcoatRoughness={0.25} />
            </mesh>
          );
        })}
      </group>
    </Canvas>
  );
};

// ---------- the vector heart: an extruded, bevelled, glossy heart (smooth at any size) ----------
const heartShape = () => {
  const s = new THREE.Shape();
  s.moveTo(0, -1.6);
  s.bezierCurveTo(-0.6, -1.1, -2, -0.4, -2, 0.55);
  s.bezierCurveTo(-2, 1.4, -1.2, 1.9, -0.6, 1.9);
  s.bezierCurveTo(-0.2, 1.9, 0, 1.6, 0, 1.3);
  s.bezierCurveTo(0, 1.6, 0.2, 1.9, 0.6, 1.9);
  s.bezierCurveTo(1.2, 1.9, 2, 1.4, 2, 0.55);
  s.bezierCurveTo(2, -0.4, 0.6, -1.1, 0, -1.6);
  return s;
};
export const VectorHeart3D: React.FC<{w: number; h: number; t0?: number; scale?: number}> = ({w, h, t0 = 0, scale = 1}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const geo = useMemo(() => {
    const g = new THREE.ExtrudeGeometry(heartShape(), {depth: 0.7, bevelEnabled: true, bevelThickness: 0.25, bevelSize: 0.18, bevelSegments: 10, curveSegments: 64});
    g.center();
    return g;
  }, []);
  const p = spr(f, fps, t0, 120, 11);
  return (
    <Canvas w={w} h={h} z={9}>
      <Lights warm="#FFF1E0" />
      <pointLight position={[-3, 2, 4]} intensity={18} color="#F7931E" />
      <mesh geometry={geo} rotation={[0.15, 0.6 * Math.sin((f - t0) / 30), 0]} scale={Math.max(0.01, p) * scale}>
        <meshPhysicalMaterial color="#E8175D" roughness={0.18} clearcoat={1} clearcoatRoughness={0.05} sheen={0.4} sheenColor="#F7931E" />
      </mesh>
    </Canvas>
  );
};

// ---------- 3D programs short ----------
// "same principles": ONE model goes wireframe (modeling) -> material -> lighting -> rig bones -> moves (animation)
export const Principles3D: React.FC<{w: number; h: number; stage: number}> = ({w, h, stage}) => {
  const f = useCurrentFrame();
  const geo = useMemo(() => new THREE.TorusKnotGeometry(1.1, 0.36, 220, 32), []);
  const wire = stage < 1;
  return (
    <Canvas w={w} h={h} z={7}>
      {stage >= 2 ? <Lights /> : <ambientLight intensity={1.4} />}
      {stage >= 2 ? <spotLight position={[0, 5, 3]} intensity={60} angle={0.5} penumbra={0.6} color="#FFE2B8" /> : null}
      <group rotation={[0.3, f / 40, 0]} position={[0, stage >= 4 ? 0.3 * Math.sin(f / 6) : 0, 0]}>
        <mesh geometry={geo}>
          {wire ? <meshBasicMaterial color="#CFE3E1" wireframe /> : stage < 2 ? <meshStandardMaterial color="#B9B3AA" roughness={0.9} /> :
            <meshPhysicalMaterial color="#F7C531" metalness={0.6} roughness={0.25} clearcoat={1} />}
        </mesh>
        {stage >= 3 ? [0, 1, 2, 3].map((i) => (
          <mesh key={i} position={[Math.cos(i * 1.57) * 1.1, Math.sin(i * 1.57) * 1.1, 0]}>
            <sphereGeometry args={[0.12, 16, 16]} /><meshBasicMaterial color="#F08A24" />
          </mesh>
        )) : null}
      </group>
    </Canvas>
  );
};

// 3ds Max -> architecture: towers rise floor by floor + a room with a sofa
const winTex = (wall: string) => {
  const cv = document.createElement('canvas'); cv.width = 128; cv.height = 128; const c = cv.getContext('2d')!;
  c.fillStyle = wall; c.fillRect(0, 0, 128, 128);
  for (let y = 0; y < 4; y++) for (let x = 0; x < 3; x++) { c.fillStyle = (x + y) % 3 ? '#9FD6F2' : '#FFE08A'; c.fillRect(12 + x * 40, 10 + y * 30, 26, 18); }
  const tx = new THREE.CanvasTexture(cv); tx.colorSpace = THREE.SRGBColorSpace; tx.wrapS = tx.wrapT = THREE.RepeatWrapping; return tx;
};
export const Building3D: React.FC<{w: number; h: number; t0?: number}> = ({w, h, t0 = 0}) => {
  const f = useCurrentFrame();
  const towers: [number, number, number, string][] = [[-1.6, 0, 3.2, '#F7C531'], [0, -0.8, 4.6, '#E9EEF2'], [1.6, 0.3, 2.6, '#F08A24'], [0.9, 1.6, 1.8, '#CFE3E1'], [-0.9, 1.4, 2.2, '#E9EEF2']];
  const tex = useMemo(() => towers.map((q) => winTex(q[3])), []);
  return (
    <Canvas w={w} h={h} z={11} y={4} fov={34}>
      <Lights warm="#FFE9C9" />
      <group rotation={[0.45, f / 70, 0]} position={[0, -1.4, 0]}>
        <mesh position={[0, -0.05, 0]}><boxGeometry args={[5.4, 0.1, 4.4]} /><meshStandardMaterial color="#7FB685" roughness={0.9} /></mesh>
        {towers.map(([x, z, hh], i) => {
          const g = lin(f, t0 + i * 6, t0 + i * 6 + 30);
          const H = Math.max(0.01, hh * g);
          const m = tex[i].clone(); m.repeat.set(1, Math.max(0.2, H / 1.2)); m.needsUpdate = true;
          return (
            <mesh key={i} position={[x, H / 2, z]}><boxGeometry args={[1, H, 1]} /><meshStandardMaterial map={m} roughness={0.45} /></mesh>
          );
        })}
      </group>
    </Canvas>
  );
};
export const Room3D: React.FC<{w: number; h: number}> = ({w, h}) => {
  const f = useCurrentFrame();
  return (
    <Canvas w={w} h={h} z={9} y={3} fov={36}>
      <Lights warm="#FFE9C9" />
      <pointLight position={[0, 2.4, 0.5]} intensity={14} color="#FFD9A0" />
      <group rotation={[0.35, -0.6 + 0.25 * Math.sin(f / 50), 0]} position={[0, -1, 0]}>
        <mesh position={[0, 0, 0]}><boxGeometry args={[5, 0.1, 4]} /><meshStandardMaterial color="#C9A27A" roughness={0.7} /></mesh>
        <mesh position={[0, 1.5, -2]}><boxGeometry args={[5, 3, 0.1]} /><meshStandardMaterial color="#EFE6D6" /></mesh>
        <mesh position={[-2.5, 1.5, 0]}><boxGeometry args={[0.1, 3, 4]} /><meshStandardMaterial color="#E6DCCB" /></mesh>
        {/* sofa */}
        <mesh position={[0, 0.4, -1.3]}><boxGeometry args={[2.6, 0.5, 0.9]} /><meshStandardMaterial color="#2C5455" roughness={0.8} /></mesh>
        <mesh position={[0, 0.85, -1.7]}><boxGeometry args={[2.6, 0.8, 0.25]} /><meshStandardMaterial color="#2C5455" roughness={0.8} /></mesh>
        {[-1.35, 1.35].map((x) => <mesh key={x} position={[x, 0.6, -1.3]}><boxGeometry args={[0.25, 0.7, 0.9]} /><meshStandardMaterial color="#244748" /></mesh>)}
        {/* table + lamp + rug */}
        <mesh position={[0, 0.06, 0.4]}><cylinderGeometry args={[1.3, 1.3, 0.02, 48]} /><meshStandardMaterial color="#F08A24" /></mesh>
        <mesh position={[0, 0.35, 0.4]}><boxGeometry args={[1.2, 0.08, 0.7]} /><meshPhysicalMaterial color="#F7C531" clearcoat={1} roughness={0.2} /></mesh>
        <mesh position={[1.9, 1.1, -1.4]}><cylinderGeometry args={[0.05, 0.05, 2.2, 12]} /><meshStandardMaterial color="#333" /></mesh>
        <mesh position={[1.9, 2.2, -1.4]}><coneGeometry args={[0.35, 0.4, 24, 1, true]} /><meshStandardMaterial color="#FFF3D6" side={THREE.DoubleSide} emissive="#FFD9A0" emissiveIntensity={0.6} /></mesh>
      </group>
    </Canvas>
  );
};

// Maya -> animation: a ball with a tail jumps with squash & stretch (the classic animation exercise)
export const BouncingBall3D: React.FC<{w: number; h: number}> = ({w, h}) => {
  const f = useCurrentFrame();
  const T = 26, ph = (f % T) / T;
  const yv = 2.6 * 4 * ph * (1 - ph);
  const squash = ph < 0.08 || ph > 0.92 ? 0.7 : 1 + 0.18 * Math.abs(1 - 2 * ph) * (ph > 0.15 && ph < 0.85 ? 1 : 0);
  const x = -1.8 + ((f / T) % 4) * 1.2;
  return (
    <Canvas w={w} h={h} z={6.2} y={1.0}>
      <Lights />
      <mesh position={[x, -1.5 + 0.75 * squash + yv, 0]} scale={[1 / Math.sqrt(squash), squash, 1 / Math.sqrt(squash)]}>
        <sphereGeometry args={[0.75, 48, 32]} /><meshPhysicalMaterial color="#F08A24" roughness={0.25} clearcoat={1} />
      </mesh>
      <mesh position={[x, -1.49, 0]} rotation={[-Math.PI / 2, 0, 0]} scale={1 - yv / 4}><circleGeometry args={[0.75, 32]} /><meshBasicMaterial color="#000" transparent opacity={0.25} /></mesh>
    </Canvas>
  );
};

// Cinema 4D -> 3D motion graphics: a cloner grid of spheres in a travelling wave
export const Cloner3D: React.FC<{w: number; h: number}> = ({w, h}) => {
  const f = useCurrentFrame();
  const N = 9;
  return (
    <Canvas w={w} h={h} z={13} y={6} fov={34}>
      <Lights warm="#E6F0FF" />
      <group rotation={[0.5, f / 90, 0]}>
        {Array.from({length: N * N}, (_, i) => {
          const gx = (i % N) - (N - 1) / 2, gz = Math.floor(i / N) - (N - 1) / 2;
          const d = Math.sqrt(gx * gx + gz * gz);
          const y = Math.sin(d * 0.9 - f / 6) * 0.8;
          const s = 0.32 + 0.12 * Math.sin(d * 0.9 - f / 6);
          return (
            <mesh key={i} position={[gx * 0.9, y, gz * 0.9]} scale={s}>
              <sphereGeometry args={[1, 24, 16]} /><meshPhysicalMaterial color={mix('#1E5BD8', '#F7C531', (y + 0.8) / 1.6)} roughness={0.2} clearcoat={1} />
            </mesh>
          );
        })}
      </group>
    </Canvas>
  );
};

// Blender = general purpose: a monkey-ish head stand-in (rounded cube) spinning in the middle
export const Spinner3D: React.FC<{w: number; h: number; color?: string}> = ({w, h, color = '#F08A24'}) => {
  const f = useCurrentFrame();
  const geo = useMemo(() => new THREE.IcosahedronGeometry(1.4, 1), []);
  return (
    <Canvas w={w} h={h} z={7}>
      <Lights />
      <mesh geometry={geo} rotation={[f / 60, f / 45, 0]}><meshPhysicalMaterial color={color} roughness={0.3} clearcoat={1} flatShading /></mesh>
    </Canvas>
  );
};

// packaging (المجالات / صور): juice box, chips bag, carton as real 3D objects with printed labels (canvas textures)
const tex = (w: number, h: number, draw: (c: CanvasRenderingContext2D) => void) => {
  const cv = document.createElement('canvas'); cv.width = w; cv.height = h; draw(cv.getContext('2d')!);
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t;
};
export const Pack3D: React.FC<{w: number; h: number; at: number[]}> = ({w, h, at}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const T = useMemo(() => ({
    juice: tex(256, 512, (c) => { c.fillStyle = '#F7931E'; c.fillRect(0, 0, 256, 512); c.fillStyle = '#fff'; c.fillRect(0, 170, 256, 190); c.fillStyle = '#F2C230'; c.beginPath(); c.arc(128, 265, 70, 0, 7); c.fill();
      c.fillStyle = '#2E9E5B'; c.beginPath(); c.ellipse(150, 190, 30, 14, -0.5, 0, 7); c.fill(); c.fillStyle = '#7A2E10'; c.font = 'bold 54px Arial'; c.textAlign = 'center'; c.fillText('JUICE', 128, 440); }),
    chips: tex(512, 512, (c) => { const g = c.createLinearGradient(0, 0, 0, 512); g.addColorStop(0, '#E5232B'); g.addColorStop(1, '#A8121A'); c.fillStyle = g; c.fillRect(0, 0, 512, 512);
      c.fillStyle = '#F2C230'; c.beginPath(); c.ellipse(256, 270, 170, 120, 0, 0, 7); c.fill(); c.fillStyle = '#A8121A'; c.font = 'bold 92px Arial'; c.textAlign = 'center'; c.fillText('CHIPS', 256, 300); }),
    box: tex(256, 256, (c) => { c.fillStyle = '#C49A6C'; c.fillRect(0, 0, 256, 256); c.fillStyle = '#9A7650'; c.fillRect(0, 118, 256, 20); c.strokeStyle = '#7A5A38'; c.lineWidth = 6; c.strokeRect(70, 60, 116, 50);
      c.fillStyle = '#7A5A38'; c.font = 'bold 34px Arial'; c.textAlign = 'center'; c.fillText('FRAGILE', 128, 96); }),
  }), []);
  const p = at.map((a) => Math.max(0.001, spr(f, fps, a, 140, 11)));
  return (
    <Canvas w={w} h={h} z={10}>
      <Lights warm="#FFF1DC" />
      <group position={[-3.1, 0, 0]} rotation={[0.15, -0.6 + f / 80, 0]} scale={p[0]}>
        <mesh><boxGeometry args={[1.4, 2.6, 1]} /><meshStandardMaterial map={T.juice} roughness={0.5} /></mesh>
        <mesh position={[0, 1.55, 0]}><boxGeometry args={[1.4, 0.5, 0.2]} /><meshStandardMaterial color="#E07F10" /></mesh>
        <mesh position={[0.45, 1.7, 0.3]} rotation={[0, 0, -0.3]}><cylinderGeometry args={[0.06, 0.06, 1, 12]} /><meshStandardMaterial color="#E8175D" /></mesh>
      </group>
      <group rotation={[0.1, 0.4 * Math.sin(f / 30), 0]} scale={p[1]}>
        <mesh scale={[1.6, 2.2, 0.55]}><sphereGeometry args={[1, 48, 32]} /><meshPhysicalMaterial map={T.chips} roughness={0.25} clearcoat={1} metalness={0.2} /></mesh>
      </group>
      <group position={[3.1, -0.2, 0]} rotation={[0.35, 0.7 + f / 90, 0]} scale={p[2]}>
        <mesh><boxGeometry args={[1.9, 1.7, 1.9]} /><meshStandardMaterial map={T.box} roughness={0.9} /></mesh>
      </group>
    </Canvas>
  );
};
