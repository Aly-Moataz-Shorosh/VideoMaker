import React, {useMemo} from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {RoomEnvironment} from 'three/examples/jsm/environments/RoomEnvironment.js';
import {lin, spr} from '../film/kit';

// Real 3D for the live Playmobil match reel (2026-11-01): the 21-point skeleton the tracking cameras build, the Playmobil
// body that gets put on top of it, and Aly himself as a Playmobil reporter (his crimson shirt + white collar, beard, mic).
type V = [number, number, number];
export const JOINTS = ['head', 'neck', 'shL', 'shR', 'elL', 'elR', 'wrL', 'wrR', 'fiL', 'fiR', 'hip', 'hpL', 'hpR',
  'knL', 'knR', 'anL', 'anR', 'heL', 'heR', 'toL', 'toR'] as const;   // = 21 points
type J = typeof JOINTS[number];
export type Pose = Record<J, V>;
export const BONES: [J, J][] = [['head', 'neck'], ['neck', 'shL'], ['neck', 'shR'], ['shL', 'elL'], ['shR', 'elR'], ['elL', 'wrL'],
  ['elR', 'wrR'], ['wrL', 'fiL'], ['wrR', 'fiR'], ['neck', 'hip'], ['hip', 'hpL'], ['hip', 'hpR'], ['hpL', 'knL'], ['hpR', 'knR'],
  ['knL', 'anL'], ['knR', 'anR'], ['anL', 'heL'], ['anR', 'heR'], ['anL', 'toL'], ['anR', 'toR']];
// the groups Aly names, in his order: head, shoulders, middle, arm joints, legs, heels, finger/toe tips
export const GROUPS: Record<string, J[]> = {
  head: ['head', 'neck'], sh: ['shL', 'shR'], mid: ['hip', 'hpL', 'hpR'], arm: ['elL', 'elR', 'wrL', 'wrR'],
  leg: ['knL', 'knR', 'anL', 'anR'], heel: ['heL', 'heR'], tip: ['fiL', 'fiR', 'toL', 'toR'],
};

// running cycle by forward kinematics (sagittal plane, z = forward)
const leg = (side: number, ph: number, bob: number): V[] => {
  const th = 0.62 * Math.sin(ph);                       // thigh swing
  const kn = 0.15 + 0.95 * Math.max(0, Math.sin(ph + 1.9)); // knee bend
  const hp: V = [side * 0.12, 0.98 + bob, 0];
  const k: V = [hp[0], hp[1] - 0.45 * Math.cos(th), hp[2] + 0.45 * Math.sin(th)];
  const a2 = th - kn;
  const an: V = [hp[0], k[1] - 0.45 * Math.cos(a2), k[2] + 0.45 * Math.sin(a2)];
  const he: V = [an[0], an[1] - 0.06, an[2] - 0.06];
  const to: V = [an[0], an[1] - 0.07, an[2] + 0.16];
  return [hp, k, an, he, to];
};
const arm = (side: number, sw: number, sh: V): V[] => {
  const el: V = [sh[0] + side * 0.05, sh[1] - 0.27 * Math.cos(sw), sh[2] + 0.27 * Math.sin(sw)];
  const a2 = sw + 1.45;
  const wr: V = [el[0], el[1] - 0.25 * Math.cos(a2), el[2] + 0.25 * Math.sin(a2)];
  const fi: V = [wr[0], wr[1] - 0.09 * Math.cos(a2), wr[2] + 0.09 * Math.sin(a2)];
  return [el, wr, fi];
};
export const runPose = (f: number): Pose => {
  const ph = (f / 18) * Math.PI * 2;
  const bob = 0.045 * Math.abs(Math.sin(ph));
  const [hpL, knL, anL, heL, toL] = leg(-1, ph, bob);
  const [hpR, knR, anR, heR, toR] = leg(1, ph + Math.PI, bob);
  const lean = 0.08;
  const shL: V = [-0.21, 1.5 + bob, lean], shR: V = [0.21, 1.5 + bob, lean];
  const [elL, wrL, fiL] = arm(-1, -0.7 * Math.sin(ph), shL);
  const [elR, wrR, fiR] = arm(1, 0.7 * Math.sin(ph), shR);
  return {head: [0, 1.76 + bob, lean + 0.03], neck: [0, 1.56 + bob, lean], shL, shR, elL, elR, wrL, wrR, fiL, fiR,
    hip: [0, 1.0 + bob, 0], hpL, hpR, knL, knR, anL, anR, heL, heR, toL, toR};
};
// reporter: standing, right hand holds the mic at his mouth, small idle sway
export const standPose = (f: number, talk: number): Pose => {
  const s = 0.012 * Math.sin(f / 22), n = 0.02 * talk;
  return {head: [s, 1.78 + n, 0.02], neck: [s, 1.56, 0], shL: [-0.22, 1.5, 0], shR: [0.22, 1.5, 0],
    elL: [-0.3, 1.24, 0.02], elR: [0.32, 1.2, 0.12], wrL: [-0.31, 1.0, 0.05], wrR: [0.2, 1.3, 0.3], fiL: [-0.31, 0.91, 0.07], fiR: [0.16, 1.36, 0.34],
    hip: [0, 1.0, 0], hpL: [-0.12, 0.98, 0], hpR: [0.12, 0.98, 0], knL: [-0.13, 0.54, 0], knR: [0.13, 0.54, 0],
    anL: [-0.13, 0.09, 0], anR: [0.13, 0.09, 0], heL: [-0.13, 0.03, -0.06], heR: [0.13, 0.03, -0.06], toL: [-0.13, 0.02, 0.16], toR: [0.13, 0.02, 0.16]};
};

const Env: React.FC = () => {
  const {gl, scene} = useThree();
  useMemo(() => {
    const pm = new THREE.PMREMGenerator(gl);
    scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
  }, [gl, scene]);
  return null;
};
const UP = new THREE.Vector3(0, 1, 0);
// a mesh stretched between two points (bones, limbs)
const Link: React.FC<{a: V; b: V; r: number; color: string; box?: [number, number]; s?: number; emissive?: string; rough?: number}> = ({a, b, r, color, box, s = 1, emissive, rough = 0.35}) => {
  const A = new THREE.Vector3(...a), B = new THREE.Vector3(...b);
  const len = A.distanceTo(B);
  const q = new THREE.Quaternion().setFromUnitVectors(UP, B.clone().sub(A).normalize());
  const mid = A.clone().add(B).multiplyScalar(0.5);
  if (s <= 0.001) return null;
  return (
    <mesh position={mid} quaternion={q} scale={[s, s, s]}>
      {box ? <boxGeometry args={[box[0], len + 0.04, box[1]]} /> : <cylinderGeometry args={[r, r, len, 20]} />}
      <meshStandardMaterial color={color} roughness={rough} metalness={0.02} emissive={emissive ?? '#000'} emissiveIntensity={emissive ? 0.8 : 0} />
    </mesh>
  );
};

// Playmobil palette = Aly's outfit in the video: crimson shirt, white collar, dark jeans, tan skin, dark hair + beard
const PM = {shirt: '#B3123C', collar: '#F4EFE6', jeans: '#23304A', skin: '#DDA06E', hair: '#2A1C14', ink: '#141018'};

const Head: React.FC<{p: V; mouth: number; s: number; face?: boolean}> = ({p, mouth, s, face = true}) => (
  <group position={p} scale={[s, s, s]}>
    <mesh position={[0, 0.06, 0]}><cylinderGeometry args={[0.2, 0.19, 0.3, 48]} /><meshStandardMaterial color={PM.skin} roughness={0.32} /></mesh>
    <mesh position={[0, 0.21, 0]} scale={[1, 0.38, 1]}><sphereGeometry args={[0.2, 40, 20]} /><meshStandardMaterial color={PM.skin} roughness={0.32} /></mesh>
    <mesh position={[0, -0.09, 0]} scale={[1, 0.3, 1]}><sphereGeometry args={[0.19, 40, 20]} /><meshStandardMaterial color={PM.skin} roughness={0.32} /></mesh>
    {/* Playmobil hair piece: dome + back */}
    <mesh position={[0, 0.2, -0.01]} scale={[1.12, 0.62, 1.12]}><sphereGeometry args={[0.2, 40, 20, 0, Math.PI * 2, 0, Math.PI * 0.55]} /><meshStandardMaterial color={PM.hair} roughness={0.45} /></mesh>
    <mesh position={[0, 0.1, -0.06]}><cylinderGeometry args={[0.215, 0.205, 0.2, 40, 1, false, Math.PI * 0.32, Math.PI * 1.36]} /><meshStandardMaterial color={PM.hair} roughness={0.45} side={THREE.DoubleSide} /></mesh>
    {face ? <>
      {/* beard ring on the jaw + moustache (Aly has both) */}
      <mesh position={[0, -0.075, 0]}><cylinderGeometry args={[0.2, 0.193, 0.09, 40, 1, true, -Math.PI * 0.36, Math.PI * 0.72]} /><meshStandardMaterial color={PM.hair} roughness={0.6} transparent opacity={0.7} side={THREE.DoubleSide} /></mesh>
      <mesh position={[0, 0.0, 0.198]} scale={[1, 0.35, 0.4]}><boxGeometry args={[0.12, 0.05, 0.03]} /><meshStandardMaterial color={PM.hair} /></mesh>
      {[-1, 1].map((k) => <mesh key={k} position={[k * 0.07, 0.1, 0.188]} scale={[1, 1.25, 0.5]}><sphereGeometry args={[0.022, 16, 12]} /><meshStandardMaterial color={PM.ink} roughness={0.2} /></mesh>)}
      {[-1, 1].map((k) => <mesh key={'b' + k} position={[k * 0.07, 0.16, 0.19]} rotation={[0, 0, -k * 0.15]}><boxGeometry args={[0.07, 0.014, 0.01]} /><meshStandardMaterial color={PM.hair} /></mesh>)}
      {/* mouth opens with his voice */}
      <mesh position={[0, -0.045, 0.188]} scale={[1, 0.25 + mouth * 1.5, 0.25]}><sphereGeometry args={[0.035, 20, 12]} /><meshStandardMaterial color="#5A1620" roughness={0.5} /></mesh>
    </> : null}
  </group>
);

// Playmobil body built on the skeleton: every part pops on in order (skin = frame it starts, -1 = never)
const Body: React.FC<{P: Pose; f: number; skin: number; mouth: number; mic?: boolean}> = ({P, f, skin, mouth, mic}) => {
  const {fps} = useVideoConfig();
  if (skin < 0) return null;
  const s = (i: number) => (f < skin ? 0 : spr(f, fps, skin + i * 2, 230, 12));
  const torsoA: V = [P.hip[0], P.hip[1] - 0.04, P.hip[2]], torsoB: V = [P.neck[0], P.neck[1] - 0.02, P.neck[2]];
  const A = new THREE.Vector3(...torsoA), B = new THREE.Vector3(...torsoB);
  const q = new THREE.Quaternion().setFromUnitVectors(UP, B.clone().sub(A).normalize());
  const mid = A.clone().add(B).multiplyScalar(0.5), len = A.distanceTo(B);
  const st = s(0);
  return (
    <group>
      {/* torso = Playmobil trapezoid (4-sided cylinder), crimson shirt + white collar */}
      {st > 0.001 ? <group position={mid} quaternion={q} scale={[st, st, st]}>
        <mesh rotation={[0, Math.PI / 4, 0]} scale={[1, 1, 0.55]}><cylinderGeometry args={[0.3, 0.36, len, 4]} /><meshStandardMaterial color={PM.shirt} roughness={0.42} /></mesh>
        <mesh position={[0, len / 2 - 0.02, 0.02]} rotation={[Math.PI / 2, 0, 0]} scale={[1.25, 0.9, 1]}><torusGeometry args={[0.1, 0.035, 12, 32]} /><meshStandardMaterial color={PM.collar} roughness={0.5} /></mesh>
        <mesh position={[0, len / 2 - 0.09, 0.118]} rotation={[0, 0, Math.PI / 4]}><boxGeometry args={[0.07, 0.07, 0.01]} /><meshStandardMaterial color={PM.collar} /></mesh>
        <mesh position={[0, -len / 2 + 0.03, 0]} rotation={[0, Math.PI / 4, 0]} scale={[1, 1, 0.55]}><cylinderGeometry args={[0.37, 0.37, 0.07, 4]} /><meshStandardMaterial color={PM.jeans} roughness={0.5} /></mesh>
      </group> : null}
      <Link a={P.shL} b={P.elL} r={0.075} color={PM.shirt} s={s(1)} />
      <Link a={P.shR} b={P.elR} r={0.075} color={PM.shirt} s={s(1)} />
      <Link a={P.elL} b={P.wrL} r={0.068} color={PM.shirt} s={s(2)} />
      <Link a={P.elR} b={P.wrR} r={0.068} color={PM.shirt} s={s(2)} />
      {/* the C-shaped Playmobil hands */}
      {([['wrL', 'fiL'], ['wrR', 'fiR']] as [J, J][]).map(([a, b], i) => s(3) > 0.001 ? (
        <mesh key={a} position={P[b]} rotation={[0, i ? -0.4 : 0.4, Math.PI / 2]} scale={s(3)}><torusGeometry args={[0.055, 0.028, 12, 24, Math.PI * 1.45]} /><meshStandardMaterial color={PM.skin} roughness={0.35} /></mesh>) : null)}
      <Link a={P.hpL} b={P.knL} r={0} box={[0.17, 0.2]} color={PM.jeans} s={s(4)} />
      <Link a={P.hpR} b={P.knR} r={0} box={[0.17, 0.2]} color={PM.jeans} s={s(4)} />
      <Link a={P.knL} b={P.anL} r={0} box={[0.16, 0.19]} color={PM.jeans} s={s(5)} />
      <Link a={P.knR} b={P.anR} r={0} box={[0.16, 0.19]} color={PM.jeans} s={s(5)} />
      <Link a={P.heL} b={P.toL} r={0} box={[0.17, 0.09]} color="#111" s={s(6)} />
      <Link a={P.heR} b={P.toR} r={0} box={[0.17, 0.09]} color="#111" s={s(6)} />
      <Head p={[P.head[0], P.head[1] - 0.02, P.head[2]]} mouth={mouth} s={s(7)} />
      {mic && s(3) > 0.001 ? (
        <group position={P.fiR} rotation={[-0.25, 0, 0.3]} scale={s(3)}>
          <mesh position={[0, 0.02, 0]}><cylinderGeometry args={[0.026, 0.02, 0.2, 20]} /><meshStandardMaterial color="#151515" roughness={0.3} /></mesh>
          <mesh position={[0, 0.14, 0]}><sphereGeometry args={[0.048, 24, 16]} /><meshStandardMaterial color="#9AA0A6" roughness={0.4} metalness={0.6} /></mesh>
          <mesh position={[0, 0.07, 0]}><boxGeometry args={[0.09, 0.07, 0.09]} /><meshStandardMaterial color="#E10600" roughness={0.4} /></mesh>
        </group>) : null}
    </group>
  );
};

// skeleton = glowing points + thin bones; hl = groups lit now
const Skel: React.FC<{P: Pose; on: number; lit: J[]; dim?: number}> = ({P, on, lit, dim = 1}) => (
  <group>
    {BONES.map(([a, b], i) => <Link key={i} a={P[a]} b={P[b]} r={0.012} color="#DDE6FF" emissive="#6E8BFF" s={on > 0.02 ? 1 : 0} />)}
    {JOINTS.map((j, i) => {
      const L = lit.includes(j);
      const k = Math.min(1, Math.max(0, on * 21 - i));   // points appear one by one (counter 1..21)
      return k <= 0 ? null : (
        <mesh key={j} position={P[j]} scale={k * (L ? 1.7 : 1) * dim}>
          <sphereGeometry args={[0.032, 20, 14]} />
          <meshStandardMaterial color={L ? '#FFD43B' : '#22D3EE'} emissive={L ? '#FFB300' : '#0AA5C2'} emissiveIntensity={1.4} />
        </mesh>
      );
    })}
  </group>
);

// tray/full scene: points count up (on: 0..1), named groups light up, Playmobil skin pops at `skin`
export const Fig3D: React.FC<{w: number; h: number; mode: 'run' | 'stand'; on?: number; lit?: J[]; skin?: number; skelFade?: number;
  mouth?: number; talk?: number; cam?: {r: number; y: number; ang: number; look: number; fov?: number}; mic?: boolean; ground?: boolean}> = (
  {w, h, mode, on = 1, lit = [], skin = -1, skelFade = 1, mouth = 0, talk = 0, cam = {r: 3.4, y: 1.1, ang: 0.5, look: 1.0}, mic, ground = true}) => {
  const f = useCurrentFrame();
  const P = mode === 'run' ? runPose(f) : standPose(f, talk);
  const cx = cam.r * Math.sin(cam.ang), cz = cam.r * Math.cos(cam.ang);
  return (
    <ThreeCanvas width={w} height={h} gl={{antialias: true, alpha: true}} camera={{position: [cx, cam.y, cz], fov: cam.fov ?? 34}}
      onCreated={({camera}) => camera.lookAt(0, cam.look, 0)}>
      <CamLook x={cx} y={cam.y} z={cz} look={cam.look} />
      <Env />
      <ambientLight intensity={0.45} />
      <directionalLight position={[2.5, 4, 3]} intensity={2.4} />
      <directionalLight position={[-3, 2, -2]} intensity={0.9} color="#9DB7FF" />
      {ground ? <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]}><circleGeometry args={[1.1, 48]} /><meshStandardMaterial color="#1C2B22" transparent opacity={0.55} /></mesh> : null}
      {skelFade > 0.01 ? <Skel P={P} on={on} lit={lit} dim={skelFade} /> : null}
      <Body P={P} f={f} skin={skin} mouth={mouth} mic={mic} />
    </ThreeCanvas>
  );
};
const CamLook: React.FC<{x: number; y: number; z: number; look: number}> = ({x, y, z, look}) => {
  const {camera} = useThree();
  camera.position.set(x, y, z);
  camera.lookAt(0, look, 0);
  return null;
};
export const litAt = (f: number, beats: [string, number][], fps: number, hold = 1.1): J[] => {
  const out: J[] = [];
  for (const [g, t] of beats) if (f >= t * fps && f < (t + hold) * fps) out.push(...(GROUPS[g] ?? []));
  return out;
};
export {lin};
