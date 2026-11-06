import React, {useMemo} from 'react';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';

// 3D SET view (Aly 2026-11-06 review: "شكل كادر كل set: حركة الكاميرا مع الممثلين مع الاضاءة بشكل 3d").
// One small diorama per set-up (table room, alley, pill room…), seen from a fixed 3/4 view. The FILM camera (violet, with its
// frustum = what the frame holds) does the shot's real move; actors are simple figures; lights = bulbs + beams (approx., from the image).
// Units: metres, y up. Positions are a DIAGRAM, not a survey.
export type V3 = [number, number, number];
export type CamPose = {pos: V3; look: V3; fov: number; move: string; amt?: number};
type Actor = {p: V3; c: string; face: number; sit?: boolean; lie?: boolean; kneel?: boolean; name?: string};
type Light = {p: V3; to: V3; c: string; k: 'key' | 'fire' | 'window' | 'sky' | 'practical'};
type Prop = {k: 'box' | 'cyl' | 'plane'; p: V3; s: V3; c: string; o?: number; r?: number};
export type SetDef = {view: V3; at: V3; actors: Actor[]; lights: Light[]; props: Prop[]};

const FARES = '#4C7DD8', IBR = '#8C8A52', OTHER = '#9AA4B2', NARG = '#3F8F5A', ASHRY = '#D0463E';
const WOOD = '#8A5A36', WALL = '#4A525E', FLOOR = '#30363F';
export const SETS: Record<string, SetDef> = {
  table: {view: [3.6, 3.4, 4.2], at: [0, 0.7, 0],
    actors: [{p: [1.05, 0, 0], c: FARES, face: -90, sit: true, name: 'Fares'}, {p: [-1.05, 0, 0], c: IBR, face: 90, sit: true, name: 'Ibrahim'}],
    lights: [{p: [1.9, 2.6, 1.0], to: [1.0, 1.1, 0], c: '#FFD9A0', k: 'key'}, {p: [-1.8, 2.6, -1.0], to: [-1.0, 1.1, 0], c: '#FFD9A0', k: 'key'}],
    props: [{k: 'plane', p: [0, 0, 0], s: [7, 1, 6], c: FLOOR}, {k: 'box', p: [0, 0.38, 0], s: [1.1, 0.06, 0.7], c: WOOD}, {k: 'box', p: [0, 0.18, 0], s: [0.9, 0.36, 0.5], c: '#3B2718'},
      {k: 'box', p: [1.35, 0.7, 0], s: [0.12, 1.4, 0.7], c: WOOD}, {k: 'box', p: [-1.35, 0.7, 0], s: [0.12, 1.4, 0.7], c: WOOD},
      {k: 'box', p: [0, 1.4, -2.4], s: [6, 2.8, 0.15], c: WALL}, {k: 'cyl', p: [0.5, 1.2, 2.1], s: [0.14, 2.4, 0.14], c: '#15181C'}, {k: 'cyl', p: [-0.6, 1.2, 2.3], s: [0.14, 2.4, 0.14], c: '#15181C'},
      {k: 'cyl', p: [0.1, 0.48, 0.1], s: [0.05, 0.22, 0.05], c: '#C8D6DA', o: 0.8}]},
  alley: {view: [4.2, 3.6, 5.2], at: [0, 0.8, -1],
    actors: [{p: [0, 0, 0], c: IBR, face: 0, name: 'Ibrahim'}, {p: [-0.9, 0, -2.6], c: OTHER, face: 0}, {p: [1.0, 0, -3.4], c: OTHER, face: 0}],
    lights: [{p: [-1.2, 0.3, -1.2], to: [0, 1, 0], c: '#FF8A2A', k: 'fire'}, {p: [1.3, 0.3, -2.4], to: [0, 1, 0], c: '#FF8A2A', k: 'fire'}, {p: [0.6, 1.6, 0.4], to: [0, 1.2, 0], c: '#FFB060', k: 'practical'}],
    props: [{k: 'plane', p: [0, 0, -1.5], s: [3.4, 1, 9], c: '#2A2016'}, {k: 'box', p: [-1.8, 1.6, -1.5], s: [0.2, 3.2, 9], c: '#3A2E22'}, {k: 'box', p: [1.8, 1.6, -1.5], s: [0.2, 3.2, 9], c: '#3A2E22'},
      {k: 'box', p: [0, 1.5, 1.6], s: [1.6, 1.6, 0.02], c: '#C8C2B0', o: 0.5}]},
  pills: {view: [3.4, 3.0, 3.8], at: [0, 0.9, 0],
    actors: [{p: [0, 0, 0], c: IBR, face: 20, name: 'Ibrahim'}],
    lights: [{p: [-1.6, 1.8, -1.2], to: [0, 1.2, 0], c: '#9EC8FF', k: 'window'}],
    props: [{k: 'plane', p: [0, 0, 0], s: [5, 1, 5], c: FLOOR}, {k: 'cyl', p: [0.55, 1.4, -0.3], s: [0.25, 2.8, 0.25], c: '#8A9496'},
      {k: 'box', p: [-1.75, 1.6, -1.2], s: [0.05, 1.2, 1.4], c: '#9EC8FF', o: 0.35}, {k: 'box', p: [0, 1.4, -2.0], s: [4, 2.8, 0.12], c: WALL},
      {k: 'box', p: [-0.5, 0.4, 0.9], s: [0.9, 0.06, 0.6], c: WOOD}]},
  narges: {view: [3.2, 2.6, 4.0], at: [0, 1.0, -1],
    actors: [{p: [0, 0, -1.6], c: NARG, face: 0, name: 'Narges'}],
    lights: [{p: [0.9, 2.2, -2.6], to: [0, 1.4, -1.6], c: '#FFE0B0', k: 'practical'}],
    props: [{k: 'plane', p: [0, 0, -1], s: [4, 1, 5], c: FLOOR}, {k: 'box', p: [-0.85, 1.3, -0.4], s: [0.3, 2.6, 0.3], c: '#C8B89A'}, {k: 'box', p: [0.85, 1.3, -0.4], s: [0.3, 2.6, 0.3], c: '#C8B89A'},
      {k: 'box', p: [0, 2.55, -0.4], s: [2.0, 0.2, 0.3], c: '#C8B89A'}]},
  street: {view: [4.6, 3.0, 5.0], at: [0, 0.8, -0.5],
    actors: [{p: [0, 0, 0], c: IBR, face: 20, name: 'Ibrahim'}, {p: [0.6, 0, 0.3], c: OTHER, face: -60, kneel: true}],
    lights: [{p: [-1.6, 0.3, -2.4], to: [0, 1, 0], c: '#FF8A2A', k: 'fire'}, {p: [1.8, 0.3, -3.0], to: [0, 1, 0], c: '#FF8A2A', k: 'fire'}, {p: [0, 3.2, -3.6], to: [0, 1, 0], c: '#8FB4FF', k: 'sky'}],
    props: [{k: 'plane', p: [0, 0, -1.5], s: [6, 1, 8], c: '#2A2016'}, {k: 'box', p: [0, 1.8, -4.6], s: [6, 3.6, 0.2], c: '#3A2E22'}]},
  roofN: {view: [4.6, 3.0, 4.8], at: [0, 0.4, -1],
    actors: [{p: [0, 0, 0], c: IBR, face: 200, lie: true, name: 'Ibrahim'}],
    lights: [{p: [-3, 3.5, -3], to: [0, 0.3, 0], c: '#7FA0D8', k: 'sky'}],
    props: [{k: 'plane', p: [0, 0, -2], s: [8, 1, 8], c: '#22262C'}, {k: 'cyl', p: [2.2, 1.8, -5.5], s: [0.25, 3.6, 0.25], c: '#C8B89A'}, {k: 'box', p: [1.4, 0.7, -5.5], s: [2.2, 1.4, 1.2], c: '#C8B89A'}]},
  roofD: {view: [6.5, 5.5, 7.5], at: [0, 1.5, -1],
    actors: [{p: [0, 1.6, -0.6], c: IBR, face: 180, sit: true, name: 'Ibrahim'}],
    lights: [{p: [-4, 6, -6], to: [0, 1.5, 0], c: '#9DB8E8', k: 'sky'}],
    props: [{k: 'box', p: [0, 0.8, -0.6], s: [3, 1.6, 2.4], c: '#3A4048'}, {k: 'box', p: [-3, 0.9, -3], s: [2, 1.8, 2], c: '#2C3138'}, {k: 'box', p: [3, 1.1, -3.5], s: [2, 2.2, 2], c: '#2C3138'},
      {k: 'plane', p: [0, 0, -1], s: [12, 1, 10], c: '#1C2026'}]},
  hole: {view: [3.0, 3.6, 3.2], at: [0, 0.3, 0],
    actors: [{p: [-0.45, 0, 0], c: ASHRY, face: 90, kneel: true, name: 'Ashry'}, {p: [0.45, 0, 0], c: IBR, face: -90, kneel: true, name: 'Ibrahim'}],
    lights: [{p: [0.8, 2.4, -1.0], to: [0, 0, 0], c: '#FFD9A0', k: 'practical'}],
    props: [{k: 'plane', p: [0, 0, 0], s: [4, 1, 4], c: '#2A251E'}, {k: 'cyl', p: [0, 0.01, 0.1], s: [0.35, 0.02, 0.35], c: '#090909'}, {k: 'box', p: [0, 0.25, -0.9], s: [1.6, 0.5, 0.8], c: '#C9B28A'}]},
  bike: {view: [4.8, 3.2, 3.2], at: [0, 0.9, -1],
    actors: [{p: [0, 0, 0], c: ASHRY, face: 180, sit: true, name: 'Ashry'}, {p: [-1.4, 0, -2.0], c: OTHER, face: 0}, {p: [1.3, 0, -3.0], c: OTHER, face: 30}, {p: [-1.1, 0, 1.6], c: OTHER, face: 90}],
    lights: [{p: [-2.5, 4.5, -2], to: [0, 1, 0], c: '#FFF3DD', k: 'sky'}],
    props: [{k: 'plane', p: [0, 0, -1.5], s: [4.2, 1, 10], c: '#3A3A38'}, {k: 'box', p: [0, 0.35, 0], s: [0.35, 0.5, 1.4], c: '#20242A'},
      {k: 'box', p: [-2.2, 1.8, -1.5], s: [0.2, 3.6, 10], c: '#4A4640'}, {k: 'box', p: [2.2, 1.8, -1.5], s: [0.2, 3.6, 10], c: '#4A4640'}]},
};

const ease = (x: number) => 0.5 - Math.cos(Math.PI * Math.min(1, Math.max(0, x))) / 2;
const v = (a: V3) => new THREE.Vector3(...a);
// The film camera's pose at progress u (0..1) of the shot, from the move words.
export const poseAt = (c: CamPose, u: number, f: number) => {
  const e = ease(u);
  const s = c.move.toLowerCase();
  const pos = v(c.pos), look = v(c.look);
  const dir = look.clone().sub(pos);
  const right = new THREE.Vector3().crossVectors(dir, new THREE.Vector3(0, 1, 0)).normalize();
  const a = c.amt ?? 1;
  if (s.includes('push') ) pos.add(dir.clone().normalize().multiplyScalar(0.7 * a * e));
  if (s.includes('pull')) pos.add(dir.clone().normalize().multiplyScalar(-0.7 * a * e));
  if (s.includes('truck right')) { pos.add(right.clone().multiplyScalar(0.9 * a * e)); look.add(right.clone().multiplyScalar(0.9 * a * e)); }
  if (s.includes('truck left')) { pos.add(right.clone().multiplyScalar(-0.9 * a * e)); look.add(right.clone().multiplyScalar(-0.9 * a * e)); }
  const yaw = (deg: number) => { const r = look.clone().sub(pos); r.applyAxisAngle(new THREE.Vector3(0, 1, 0), (-deg * Math.PI) / 180); look.copy(pos.clone().add(r)); };
  if (s.includes('whip')) yaw((s.includes('left') ? -70 : 70) * Math.min(1, u * 3));
  else if (s.includes('pan right')) yaw(24 * a * e);
  else if (s.includes('pan left')) yaw(-24 * a * e);
  if (s.includes('tilt up')) look.y += 0.9 * a * e;
  if (s.includes('tilt down')) look.y -= 0.9 * a * e;
  if (s.includes('arc')) { const r = pos.clone().sub(look); r.applyAxisAngle(new THREE.Vector3(0, 1, 0), (-38 * a * e * Math.PI) / 180); pos.copy(look.clone().add(r)); }
  if (s.includes('crane')) { pos.y += 3.5 * a * e; look.y += 0.6 * a * e; }
  if (s.includes('tracking')) { const fw = new THREE.Vector3(0, 0, -3.2 * e); pos.add(fw); look.add(fw); }
  if (s.includes('handheld')) { pos.x += Math.sin(f * 0.37) * 0.025; pos.y += Math.sin(f * 0.53 + 1) * 0.02; look.x += Math.sin(f * 0.29 + 2) * 0.04; }
  return {pos, look};
};

const Figure: React.FC<{a: Actor; shift?: V3}> = ({a, shift = [0, 0, 0]}) => {
  const h = a.sit ? 0.55 : a.kneel ? 0.45 : 0;
  const body = a.lie ? null : (
    <group position={[a.p[0] + shift[0], a.p[1] + shift[1], a.p[2] + shift[2]]} rotation={[0, (a.face * Math.PI) / 180, 0]}>
      <mesh position={[0, 0.95 - h + (a.sit ? 0.1 : 0), 0]}><capsuleGeometry args={[0.17, 0.62 - (a.sit ? 0.1 : 0), 6, 12]} /><meshStandardMaterial color={a.c} roughness={0.7} /></mesh>
      <mesh position={[0, 1.58 - h, 0]}><sphereGeometry args={[0.12, 16, 12]} /><meshStandardMaterial color="#C99A74" roughness={0.6} /></mesh>
      <mesh position={[0, 1.58 - h, 0.11]}><boxGeometry args={[0.07, 0.03, 0.03]} /><meshStandardMaterial color="#111" /></mesh>
      {!a.sit && !a.kneel && <><mesh position={[-0.08, 0.32, 0]}><capsuleGeometry args={[0.065, 0.5, 4, 8]} /><meshStandardMaterial color="#2B2B30" /></mesh>
        <mesh position={[0.08, 0.32, 0]}><capsuleGeometry args={[0.065, 0.5, 4, 8]} /><meshStandardMaterial color="#2B2B30" /></mesh></>}
    </group>);
  if (a.lie) return <group position={a.p} rotation={[0, (a.face * Math.PI) / 180, 0]}>
    <mesh position={[0, 0.2, 0]} rotation={[0, 0, Math.PI / 2.4]}><capsuleGeometry args={[0.17, 0.9, 6, 12]} /><meshStandardMaterial color={a.c} /></mesh>
    <mesh position={[-0.55, 0.42, 0]}><sphereGeometry args={[0.12, 16, 12]} /><meshStandardMaterial color="#C99A74" /></mesh></group>;
  return body;
};
const LightRig: React.FC<{l: Light}> = ({l}) => {
  const from = v(l.p), to = v(l.to);
  const len = from.distanceTo(to);
  const mid = from.clone().add(to).multiplyScalar(0.5);
  const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, -1, 0), to.clone().sub(from).normalize());
  const beam = l.k !== 'fire';
  return <group>
    <pointLight position={l.p} color={l.c} intensity={l.k === 'fire' ? 3.2 : 4.5} distance={8} decay={1.4} />
    <mesh position={l.p}><sphereGeometry args={[l.k === 'fire' ? 0.13 : 0.1, 14, 10]} /><meshBasicMaterial color={l.c} /></mesh>
    {l.k === 'fire' && <mesh position={[l.p[0], l.p[1] + 0.18, l.p[2]]}><coneGeometry args={[0.16, 0.42, 10]} /><meshBasicMaterial color="#FF6A1A" transparent opacity={0.85} /></mesh>}
    {beam && <mesh position={mid} quaternion={q}><coneGeometry args={[len * 0.32, len, 20, 1, true]} /><meshBasicMaterial color={l.c} transparent opacity={0.09} side={THREE.DoubleSide} depthWrite={false} /></mesh>}
  </group>;
};
const PropM: React.FC<{p: Prop}> = ({p}) => {
  const m = <meshStandardMaterial color={p.c} roughness={0.85} transparent={p.o !== undefined} opacity={p.o ?? 1} />;
  if (p.k === 'plane') return <mesh position={p.p} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[p.s[0], p.s[2]]} />{m}</mesh>;
  if (p.k === 'cyl') return <mesh position={p.p}><cylinderGeometry args={[p.s[0], p.s[0], p.s[1], 16]} />{m}</mesh>;
  return <mesh position={p.p} rotation={[0, p.r ?? 0, 0]}><boxGeometry args={p.s} />{m}</mesh>;
};
// Film camera body + frustum (what the frame holds).
const FilmCam: React.FC<{pos: THREE.Vector3; look: THREE.Vector3; fov: number; aspect: number}> = ({pos, look, fov, aspect}) => {
  const geo = useMemo(() => new THREE.BufferGeometry(), []);
  const m = new THREE.Matrix4().lookAt(pos, look, new THREE.Vector3(0, 1, 0));
  const q = new THREE.Quaternion().setFromRotationMatrix(m);
  const d = Math.min(1.0, pos.distanceTo(look) * 0.6);
  const hh = Math.tan((fov * Math.PI) / 360) * d, hw = hh * aspect;
  const c = [[-hw, -hh], [hw, -hh], [hw, hh], [-hw, hh]].map(([x, y]) => new THREE.Vector3(x, y, -d));
  const pts: THREE.Vector3[] = [];
  c.forEach((p, i) => { pts.push(new THREE.Vector3(0, 0, 0), p, p, c[(i + 1) % 4]); });
  geo.setFromPoints(pts);
  return <group position={pos} quaternion={q}>
    <mesh><boxGeometry args={[0.18, 0.16, 0.26]} /><meshStandardMaterial color="#A78BFA" emissive="#5B3FC4" emissiveIntensity={0.6} /></mesh>
    <mesh position={[0, 0, -0.17]} rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[0.06, 0.07, 0.1, 14]} /><meshStandardMaterial color="#222" /></mesh>
    <lineSegments geometry={geo}><lineBasicMaterial color="#C4B5FD" /></lineSegments>
    <mesh position={[0, 0, -d]}><planeGeometry args={[hw * 2, hh * 2]} /><meshBasicMaterial color="#A78BFA" transparent opacity={0.1} side={THREE.DoubleSide} depthWrite={false} /></mesh>
  </group>;
};
const View: React.FC<{eye: V3; at: V3}> = ({eye, at}) => {
  const {camera} = useThree();
  camera.position.set(...eye); camera.lookAt(...at); camera.updateProjectionMatrix();
  return null;
};

export const Set3D: React.FC<{w: number; h: number; set: string; cam: CamPose; u: number; f: number; trail?: boolean}> = ({w, h, set, cam, u, f}) => {
  const S = SETS[set] ?? SETS.table;
  const {pos, look} = poseAt(cam, u, f);
  const start = poseAt(cam, 0, 0).pos, end = poseAt(cam, 1, 0).pos;
  const path = useMemo(() => {
    const g = new THREE.BufferGeometry();
    const pts: THREE.Vector3[] = [];
    for (let i = 0; i <= 24; i++) pts.push(poseAt(cam, i / 24, 0).pos);
    g.setFromPoints(pts);
    const ln = new THREE.Line(g, new THREE.LineDashedMaterial({color: '#A78BFA', dashSize: 0.08, gapSize: 0.06}));
    ln.computeLineDistances(); return ln;
  }, [cam.pos.join(), cam.look.join(), cam.move]);
  const moving = start.distanceTo(end) > 0.05;
  // actor that moves with the camera (tracking)
  const shift: V3 = cam.move.toLowerCase().includes('tracking') ? [0, 0, -3.2 * ease(u)] : [0, 0, 0];
  return <ThreeCanvas width={w} height={h} gl={{antialias: true, alpha: true}} camera={{position: S.view, fov: 34}}>
    <View eye={[S.at[0] + (S.view[0] - S.at[0]) * 0.62, S.at[1] + (S.view[1] - S.at[1]) * 0.62, S.at[2] + (S.view[2] - S.at[2]) * 0.62]} at={S.at} />
    <ambientLight intensity={1.6} />
    <hemisphereLight args={['#b8c8e0', '#3a3028', 1.2]} />
    <directionalLight position={[3, 6, 4]} intensity={0.8} />
    {S.props.map((p, i) => <PropM key={i} p={p} />)}
    {S.actors.map((a, i) => <Figure key={i} a={a} shift={i === 0 ? shift : undefined} />)}
    {S.lights.map((l, i) => <LightRig key={i} l={l} />)}
    {moving && <primitive object={path} />}
    <FilmCam pos={pos} look={look} fov={cam.fov} aspect={2.29} />
  </ThreeCanvas>;
};
