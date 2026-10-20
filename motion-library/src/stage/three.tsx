import React, {useMemo} from 'react';
import {Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {RoomEnvironment} from 'three/examples/jsm/environments/RoomEnvironment.js';
import {AR, EN, L, lin, S, spr, W} from './kit';

// Real 3D (three.js) for the lecture shorts (Aly review 2026-10-19: show what a material / render / rotation IS, not a label).
// Drawn in the stage box (W x 830 from L.stageTop) like every tray scene. Beats b = seconds from the cue start.
const bt = (b: Record<string, number> | undefined, k: string, fps: number, d = 0) => Math.round((b?.[k] ?? d) * fps);
const out = (f: number, dur: number) => 1 - lin(f, dur - 7, dur);

// studio reflections without any file: three's RoomEnvironment through PMREM
const Env: React.FC<{bg?: string}> = ({bg}) => {
  const {gl, scene} = useThree();
  useMemo(() => {
    const pm = new THREE.PMREMGenerator(gl);
    scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.background = bg ? new THREE.Color(bg) : null;
  }, [gl, scene, bg]);
  return null;
};

const canvasTex = (w: number, h: number, draw: (c: CanvasRenderingContext2D) => void) => {
  const cv = document.createElement('canvas');
  cv.width = w; cv.height = h;
  draw(cv.getContext('2d')!);
  const t = new THREE.CanvasTexture(cv);
  t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return t;
};
const rnd = (i: number) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

// the materials he names: clay (start), a color, metal (reflections), glass, watermelon, honey, rock
const useMaterials = () => useMemo(() => {
  const melon = canvasTex(1024, 512, (c) => {
    c.fillStyle = '#2F7D2C'; c.fillRect(0, 0, 1024, 512);
    for (let i = 0; i < 16; i++) {
      c.fillStyle = i % 2 ? '#1B4F1C' : '#4E9A3A';
      c.beginPath();
      for (let y = 0; y <= 512; y += 8) c.lineTo(i * 64 + 18 * Math.sin(y / 40 + i), y);
      for (let y = 512; y >= 0; y -= 8) c.lineTo(i * 64 + 26 + 18 * Math.sin(y / 40 + i), y);
      c.fill();
    }
  });
  const rock = canvasTex(512, 512, (c) => {
    c.fillStyle = '#77736C'; c.fillRect(0, 0, 512, 512);
    for (let i = 0; i < 2600; i++) { const g = 80 + rnd(i) * 90; c.fillStyle = `rgb(${g},${g - 4},${g - 10})`; c.beginPath(); c.arc(rnd(i + 1) * 512, rnd(i + 2) * 512, 1 + rnd(i + 3) * 7, 0, 7); c.fill(); }
  });
  return {
    clay: new THREE.MeshStandardMaterial({color: '#BDB6AE', roughness: 0.85}),
    color: new THREE.MeshStandardMaterial({color: '#FF3D6E', roughness: 0.45}),
    metal: new THREE.MeshStandardMaterial({color: '#E9EDF5', metalness: 1, roughness: 0.08}),
    glass: new THREE.MeshPhysicalMaterial({color: '#FFFFFF', metalness: 0, roughness: 0.02, transmission: 1, thickness: 1.2, ior: 1.5, clearcoat: 1}),
    melon: new THREE.MeshStandardMaterial({map: melon, roughness: 0.35}),
    honey: new THREE.MeshPhysicalMaterial({color: '#F2A114', roughness: 0.08, transmission: 0.75, thickness: 2, ior: 1.45, clearcoat: 1, attenuationColor: new THREE.Color('#B85C00'), attenuationDistance: 0.8}),
    rock: new THREE.MeshStandardMaterial({map: rock, bumpMap: rock, bumpScale: 4, roughness: 1}),
  } as Record<string, THREE.Material>;
}, []);

const SWATCH: Record<string, [string, string]> = {
  color: ['#FF3D6E', 'لون'], metal: ['#DCE3EE', 'انعكاس'], glass: ['#BFE8FF', 'إزاز'], melon: ['#2F7D2C', 'بطيخة'], honey: ['#F2A114', 'عسل'], rock: ['#77736C', 'صخر'],
};

// ---------- Mat3D: ONE ball; the mouse drags a material swatch onto it and the ball becomes that material ----------
export const Mat3D: React.FC<{dur: number; order?: string[]; b?: Record<string, number>}> = ({dur, order = ['color', 'metal', 'glass', 'melon', 'honey', 'rock'], b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const M = useMaterials();
  const ks = order.map((k, i) => bt(b, k, fps, 0.6 + i * 1.1));
  // which material is on the ball: the last one dropped (drop = beat)
  let cur = 'clay';
  ks.forEach((k, i) => { if (f >= k) cur = order[i]; });
  // the drag that is happening now (0.5 s before its beat)
  const di = ks.findIndex((k) => f >= k - 15 && f < k + 4);
  const sw = (i: number) => ({x: 120 + i * 168, y: L.stageTop + 690});
  const ball = {x: W / 2, y: L.stageTop + 330};
  let cx = sw(0).x, cy = sw(0).y + 30;
  if (di >= 0) {
    const p = lin(f, ks[di] - 15, ks[di], 0, 1);
    cx = sw(di).x + (ball.x - sw(di).x) * p; cy = sw(di).y + (ball.y - sw(di).y) * p;
  } else {
    const nxt = ks.findIndex((k) => f < k);
    const j = nxt < 0 ? order.length - 1 : nxt;
    cx = sw(j).x + 10; cy = sw(j).y + 40;
  }
  const pop = di >= 0 ? 0 : Math.max(0, 1 - (f - (ks.filter((k) => f >= k).slice(-1)[0] ?? -99)) / 10);
  const rot = f / 50;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 1920, opacity: out(f, dur) * Math.min(1, f / 6)}}>
      <div style={{position: 'absolute', left: W / 2 - 330, top: L.stageTop - 10, width: 660, height: 660}}>
        <ThreeCanvas width={660} height={660} camera={{position: [0, 0, 3.2], fov: 40}} gl={{antialias: true, alpha: true}}>
          <Env />
          <ambientLight intensity={0.35} />
          <directionalLight position={[3, 4, 5]} intensity={2.2} />
          <directionalLight position={[-4, -2, -3]} intensity={0.6} color="#8FB2FF" />
          <mesh rotation={[0.3, rot, 0]} scale={1 + 0.06 * pop} material={M[cur]}>
            <sphereGeometry args={[1, 96, 64]} />
          </mesh>
        </ThreeCanvas>
      </div>
      {/* material swatches */}
      {order.map((k, i) => {
        const p = spr(f, fps, i * 3, 200, 14);
        const used = f >= ks[i];
        return (
          <div key={k} style={{position: 'absolute', left: sw(i).x - 62, top: sw(i).y - 62, width: 124, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: p * (used && cur !== k ? 0.45 : 1)}}>
            <div style={{width: 96, height: 96, borderRadius: 48, background: `radial-gradient(circle at 35% 30%, #fff8 0%, ${SWATCH[k][0]} 45%, #0008 100%)`,
              border: cur === k ? `5px solid ${S.yellow}` : '3px solid rgba(255,255,255,0.3)', boxShadow: '0 10px 24px rgba(0,0,0,0.45)'}} />
            <div style={{fontFamily: AR, fontWeight: 900, fontSize: 34, color: '#fff', marginTop: 6}}>{SWATCH[k][1]}</div>
          </div>
        );
      })}
      {/* the dragged swatch + cursor */}
      {di >= 0 ? <div style={{position: 'absolute', left: cx - 48, top: cy - 48, width: 96, height: 96, borderRadius: 48, opacity: 0.9,
        background: `radial-gradient(circle at 35% 30%, #fff8 0%, ${SWATCH[order[di]][0]} 45%, #0008 100%)`}} /> : null}
      <svg width={70} height={80} viewBox="0 0 28 32" style={{position: 'absolute', left: cx + 10, top: cy + 10, filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.6))'}}>
        <path d="M2 2 L2 26 L8 20 L12 30 L17 28 L13 18 L22 18 Z" fill="#fff" stroke="#111" strokeWidth={1.6} strokeLinejoin="round" />
      </svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: L.stageTop - 40, textAlign: 'center', fontFamily: EN, fontWeight: 900, fontSize: 54, color: S.yellow}}>Material</div>
    </div>
  );
};

// ---------- a little bear built from spheres (same model, 3 renders) ----------
const Bear: React.FC<{body: THREE.Material; muzzle: THREE.Material; eye: THREE.Material; outline?: boolean; rot: number}> = ({body, muzzle, eye, outline, rot}) => {
  const parts: [number[], number, THREE.Material][] = [
    [[0, -0.15, 0], 0.62, body], [[0, 0.72, 0], 0.5, body], [[-0.38, 1.12, 0], 0.17, body], [[0.38, 1.12, 0], 0.17, body],
    [[0, 0.6, 0.42], 0.2, muzzle], [[-0.17, 0.82, 0.42], 0.07, eye], [[0.17, 0.82, 0.42], 0.07, eye], [[0, 0.68, 0.6], 0.07, eye],
    [[-0.62, 0.0, 0.1], 0.2, body], [[0.62, 0.0, 0.1], 0.2, body], [[-0.32, -0.72, 0.15], 0.24, body], [[0.32, -0.72, 0.15], 0.24, body],
  ];
  const ol = useMemo(() => new THREE.MeshBasicMaterial({color: '#111', side: THREE.BackSide}), []);
  return (
    <group rotation={[0.05, rot, 0]}>
      {parts.map(([p, r, m], i) => (
        <group key={i} position={p as [number, number, number]}>
          <mesh material={m}><sphereGeometry args={[r, 64, 48]} /></mesh>
          {outline ? <mesh material={ol} scale={1.07}><sphereGeometry args={[r, 32, 24]} /></mesh> : null}
        </group>
      ))}
    </group>
  );
};

// ---------- Looks3D: the SAME bear rendered as an ad (studio), a cartoon (Toy Story) and a film (Spider-Man) ----------
export const Looks3D: React.FC<{dur: number; b?: Record<string, number>}> = ({dur, b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const k1 = bt(b, 'ad', fps, 0.3), k2 = bt(b, 'toy', fps, 2), k3 = bt(b, 'cine', fps, 4);
  const look = f >= k3 ? 'cine' : f >= k2 ? 'toy' : 'ad';
  const mats = useMemo(() => ({
    ad: {body: new THREE.MeshPhysicalMaterial({color: '#C98B54', roughness: 0.32, clearcoat: 0.6, sheen: 1, sheenColor: new THREE.Color('#FFD9B0')}),
      muzzle: new THREE.MeshPhysicalMaterial({color: '#F1D6B8', roughness: 0.4}), eye: new THREE.MeshPhysicalMaterial({color: '#111', roughness: 0.05, clearcoat: 1})},
    toy: {body: new THREE.MeshToonMaterial({color: '#F27BB1'}), muzzle: new THREE.MeshToonMaterial({color: '#FFD3E6'}), eye: new THREE.MeshToonMaterial({color: '#2A1A2E'})},
    cine: {body: new THREE.MeshStandardMaterial({color: '#5A4636', roughness: 0.75}), muzzle: new THREE.MeshStandardMaterial({color: '#8C735E', roughness: 0.8}),
      eye: new THREE.MeshStandardMaterial({color: '#050505', roughness: 0.1, metalness: 0.4})},
  }), []);
  const m = (mats as any)[look];
  const bg = look === 'ad' ? '#EDEFF4' : look === 'toy' ? '#8FD3FF' : '#07080D';
  const lab = look === 'ad' ? ['إعلان', 'Studio render'] : look === 'toy' ? ['كارتون', 'زي Toy Story'] : ['فيلم سينما', 'زي Spider-Man'];
  const p = spr(f, fps, look === 'ad' ? k1 : look === 'toy' ? k2 : k3, 220, 13);
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 1920, opacity: out(f, dur) * Math.min(1, f / 6)}}>
      <div style={{position: 'absolute', left: W / 2 - 400, top: L.stageTop, width: 800, height: 640, borderRadius: 40, overflow: 'hidden', boxShadow: '0 30px 60px rgba(0,0,0,0.5)'}}>
        <ThreeCanvas width={800} height={640} camera={{position: [0, 0.3, 4.2], fov: 38}} gl={{antialias: true}}>
          <Env bg={bg} />
          {look === 'ad' ? <><ambientLight intensity={0.5} /><directionalLight position={[2, 4, 5]} intensity={2.4} /><directionalLight position={[-3, 2, 2]} intensity={1} /></> : null}
          {look === 'toy' ? <><ambientLight intensity={0.9} /><directionalLight position={[3, 5, 4]} intensity={2.2} /></> : null}
          {look === 'cine' ? <><ambientLight intensity={0.05} /><pointLight position={[-2.5, 1, -1]} intensity={40} color="#FF2244" /><pointLight position={[2.5, 1.5, -1]} intensity={40} color="#2266FF" />
            <spotLight position={[0, 4, 3]} intensity={30} angle={0.5} penumbra={0.8} color="#FFE2B8" /></> : null}
          <Bear {...m} outline={look === 'toy'} rot={Math.sin(f / 40) * 0.5} />
          {look === 'ad' ? <mesh position={[0, -1.02, 0]} rotation={[-Math.PI / 2, 0, 0]}><circleGeometry args={[3, 64]} /><meshStandardMaterial color="#F7F8FB" roughness={0.6} /></mesh> : null}
        </ThreeCanvas>
        {look === 'cine' ? <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg, #000 0 9%, transparent 9% 91%, #000 91%)'}} /> : null}
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: L.stageTop + 660, display: 'flex', justifyContent: 'center', gap: 16, direction: 'rtl', transform: `scale(${0.7 + 0.3 * p})`}}>
        <span style={{fontFamily: AR, fontWeight: 900, fontSize: 60, color: S.ink, background: S.yellow, padding: '0 22px 8px', borderRadius: 16}}>{lab[0]}</span>
        <span style={{fontFamily: EN, fontWeight: 800, fontSize: 40, color: '#fff', alignSelf: 'center'}}>{lab[1]}</span>
      </div>
    </div>
  );
};

// ---------- Rot3D: a 3D chair that turns around when he says "تلفّها" (beat spin) ----------
export const Rot3D: React.FC<{dur: number; b?: Record<string, number>; t?: string}> = ({dur, b, t = '3D = أوبجكت تقدر تلفّه'}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ks = bt(b, 'spin', fps, 1);
  const spin = f < ks ? 0.5 : 0.5 + (f - ks) / 14;
  const wood = useMemo(() => new THREE.MeshStandardMaterial({color: '#B5793F', roughness: 0.55}), []);
  const seat = useMemo(() => new THREE.MeshStandardMaterial({color: '#E0475E', roughness: 0.5}), []);
  const box = (p: [number, number, number], s: [number, number, number], m: THREE.Material, k: number) => (
    <mesh key={k} position={p} material={m}><boxGeometry args={s} /></mesh>
  );
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 1920, opacity: out(f, dur) * Math.min(1, f / 6)}}>
      <div style={{position: 'absolute', left: W / 2 - 330, top: L.stageTop - 10, width: 660, height: 620}}>
        <ThreeCanvas width={660} height={620} camera={{position: [0, 1.2, 4.6], fov: 40}} gl={{antialias: true, alpha: true}}>
          <Env />
          <ambientLight intensity={0.4} />
          <directionalLight position={[3, 5, 4]} intensity={2.5} />
          <group rotation={[0, spin, 0]} position={[0, -0.4, 0]}>
            {box([0, 0, 0], [1.4, 0.16, 1.3], seat, 1)}
            {box([0, 0.85, -0.6], [1.4, 1.5, 0.14], seat, 2)}
            {[[-0.6, -0.6, -0.55], [0.6, -0.6, -0.55], [-0.6, -0.6, 0.55], [0.6, -0.6, 0.55]].map((p, i) => box(p as [number, number, number], [0.14, 1.1, 0.14], wood, 10 + i))}
          </group>
        </ThreeCanvas>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: L.stageTop + 640, textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 56, color: '#fff', direction: 'rtl'}}>
        {t} {f >= ks ? <span style={{color: S.yellow}}>↻</span> : null}</div>
    </div>
  );
};
