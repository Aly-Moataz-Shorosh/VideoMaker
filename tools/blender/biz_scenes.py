# Blender 5.2 scenes for the opening of "انت بتشتغل ايه" — رواد الأعمال ep01 (guest Karim Tamer, 2026-10-27).
# Aly's camera was a tiny Meet self-view while he introduced the department and the guest (0:17-2:03) -> the opening is
# carried by 3D scenes of his words (Aly: "ممكن تعمل شغل ب blender برده علشان يكون في ابهار"):
#   tower  = the big success stories (chairman, businessman, big numbers): a city, one gold tower shoots up, coin on top
#   road   = who we host instead: starters (kiosk + rocket), people who reached a level then closed (shutter), and went into
#            something else (new glowing building)
#   crowd  = 400 people, ONE golden on a pedestal (the rare extreme story) -> the camera pulls back and the many light up
#   three  = Karim's 3 projects as cards on a timeline (Courzerve -> Kiko's Snacks -> FPL Champ), numbered, arrows between
# Same way as sound_scenes.py: bpy data API, animated by setting values per frame, EEVEE, transparent film -> PNG frames.
# v2 (Aly: cinematic): DOF following the subject, real motion blur (frame handler), handheld drift, crane/swoop/dolly-zoom moves,
# teal-orange lighting, lit windows, glowing streets, lamps, smoke, a light pool per card.
# Composition leaves the LEFT third free (Aly's camera sits there): camera shift_x pushes the subject right.
#   blender -b --factory-startup -P biz_scenes.py -- --scene tower --frames 240 --out <dir> [--still 120] [--tex <dir>]
import bpy, bmesh, math, sys, os, argparse, random
import numpy as np

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument('--scene', required=True)
ap.add_argument('--frames', type=int, default=240)
ap.add_argument('--out', required=True)
ap.add_argument('--still', type=int, default=-1)
ap.add_argument('--tex', default='')
ap.add_argument('--res', type=int, nargs=2, default=[1920, 1080])
ap.add_argument('--samples', type=int, default=32)
ap.add_argument('--start', type=int, default=0)  # resume a crashed render from this frame
A = ap.parse_args(a)
random.seed(7)

# show palette (docs/22: orange / blue / olive / mustard on dark) + gold
ORANGE, BLUE, OLIVE, MUSTARD = (0.88, 0.39, 0.18), (0.36, 0.55, 0.75), (0.56, 0.60, 0.36), (0.91, 0.71, 0.29)
PAPER, NAVY, GOLD = (0.94, 0.90, 0.82), (0.07, 0.09, 0.13), (1.0, 0.72, 0.22)
lin = lambda c: tuple(x ** 2.2 for x in c)
sm = lambda x: 0 if x <= 0 else 1 if x >= 1 else x * x * (3 - 2 * x)
def ease(f, a, b): return sm((f - a) / max(1e-6, b - a))
def back(x, s=1.7):  # overshoot ease-out (pop)
    if x <= 0: return 0
    if x >= 1: return 1
    x -= 1; return x * x * ((s + 1) * x + s) + 1

sc = bpy.context.scene
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
sc.render.engine = 'BLENDER_EEVEE'
sc.render.resolution_x, sc.render.resolution_y = A.res
sc.render.film_transparent = True
sc.render.fps = 30
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGBA'
try: sc.eevee.taa_render_samples = A.samples
except Exception: pass
try: sc.eevee.use_raytracing = True
except Exception: pass
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - Punchy'
except TypeError: pass
w = bpy.data.worlds.new('W'); sc.world = w
bg = next(n for n in w.node_tree.nodes if n.type == 'BACKGROUND')
bg.inputs['Color'].default_value = (0.03, 0.04, 0.07, 1); bg.inputs['Strength'].default_value = 0.7


def mat(name, color, metal=0.0, rough=0.4, emit=0.0, coat=0.3, obj_color=False, tex=None):
    m = bpy.data.materials.new(name)
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    p.inputs['Base Color'].default_value = (*lin(color), 1)
    p.inputs['Metallic'].default_value = metal
    p.inputs['Roughness'].default_value = rough
    p.inputs['Coat Weight'].default_value = coat
    if emit:
        p.inputs['Emission Color'].default_value = (*lin(color), 1)
        p.inputs['Emission Strength'].default_value = emit
    if obj_color:  # per-object colour (ob.color) -> base + glow
        oi = nt.nodes.new('ShaderNodeObjectInfo')
        nt.links.new(oi.outputs['Color'], p.inputs['Base Color'])
        nt.links.new(oi.outputs['Color'], p.inputs['Emission Color'])
        p.inputs['Emission Strength'].default_value = emit or 0.25
    if tex:  # picture on the card front: base colour + a little emission so it reads like the real post
        im = nt.nodes.new('ShaderNodeTexImage'); im.image = bpy.data.images.load(tex)
        nt.links.new(im.outputs['Color'], p.inputs['Base Color'])
        nt.links.new(im.outputs['Color'], p.inputs['Emission Color'])
        p.inputs['Emission Strength'].default_value = 0.55
        p.inputs['Roughness'].default_value = 0.5
    return m


def bsdf(m): return next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')


def mesh_obj(name, bm, m, loc=(0, 0, 0), rot=(0, 0, 0), smooth=True):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    if smooth:
        for poly in me.polygons: poly.use_smooth = True
    ob = bpy.data.objects.new(name, me); ob.data.materials.append(m)
    ob.location, ob.rotation_euler = loc, rot
    sc.collection.objects.link(ob)
    return ob


def link(name, me, loc=(0, 0, 0)):
    ob = bpy.data.objects.new(name, me); ob.location = loc; sc.collection.objects.link(ob); return ob


def sphere(r=1.0, seg=24, ring=16, at=(0, 0, 0)):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=ring, radius=r)
    bmesh.ops.translate(bm, vec=at, verts=bm.verts); return bm


def cyl(r1, r2, depth, seg=48, at=(0, 0, 0)):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r1, radius2=r2, depth=depth)
    bmesh.ops.translate(bm, vec=at, verts=bm.verts); return bm


def cube(x, y, z, at=(0, 0, 0), bevel=0.0):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(x, y, z), verts=bm.verts)
    if bevel: bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=3, affect='EDGES', profile=0.5)
    bmesh.ops.translate(bm, vec=at, verts=bm.verts); return bm


def plane_uv(wd, ht):  # front-facing picture plane (normal -Y, towards the camera), UVs 0..1
    bm = bmesh.new(); uv = bm.loops.layers.uv.new()
    v = [bm.verts.new(p) for p in [(-wd / 2, 0, -ht / 2), (wd / 2, 0, -ht / 2), (wd / 2, 0, ht / 2), (-wd / 2, 0, ht / 2)]]
    f = bm.faces.new(v)
    for lp, c in zip(f.loops, [(0, 0), (1, 0), (1, 1), (0, 1)]): lp[uv].uv = c
    f.normal_update()
    if f.normal.y > 0: f.normal_flip()
    return bm


def text(body, size=1.0, extrude=0.06, m=None, loc=(0, 0, 0), align='CENTER'):
    cu = bpy.data.curves.new('T', 'FONT'); cu.body = body; cu.size = size; cu.extrude = extrude
    cu.align_x = align; cu.align_y = 'CENTER'; cu.bevel_depth = 0.01
    ob = bpy.data.objects.new('T_' + body, cu); ob.data.materials.append(m); ob.location = loc
    ob.rotation_euler = (math.pi / 2, 0, 0)  # stand up, face -Y (camera)
    sc.collection.objects.link(ob); return ob



# ---------------------------------------------------------------- cinematic camera (Aly 2026-10-27: "الاضاءة و الحركة و تحريك
# الكاميرا كله يكون مبدع و بروفيشنال جدا") — depth of field that follows the subject, motion blur, a slight handheld drift,
# lens changes (wide crane shots, a dolly zoom), every move eased in/out.
cam = bpy.data.objects.new('Cam', bpy.data.cameras.new('Cam')); sc.collection.objects.link(cam); sc.camera = cam
cam.data.lens = 40
cam.data.shift_x = -0.17  # subject to the right two thirds; Aly's camera sits on the left
cam.data.clip_start = 0.05; cam.data.clip_end = 400
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 2.2
cam.data.dof.aperture_blades = 7
try:
    sc.render.use_motion_blur = True
    sc.render.motion_blur_shutter = 0.45
except Exception: pass


def eio(x):  # ease in-out cubic (camera moves)
    x = max(0.0, min(1.0, x)); return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2
def E2(f, a, b): return eio((f - a) / max(1e-6, b - a))


def look(cam_loc, target=(0, 0, 0), lens=None, focus=None, f=0, shake=0.02):
    # handheld: two slow sines per axis (never a jitter), tiny
    n = np.array([math.sin(f / 23.0) + 0.6 * math.sin(f / 9.7 + 1), math.sin(f / 29.0 + 2) + 0.5 * math.sin(f / 11.3), math.sin(f / 19.0 + 4)]) * shake
    loc = np.array(cam_loc, float) + n
    cam.location = loc
    d = np.array(target, float) - loc
    cam.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi / 2)
    if lens: cam.data.lens = lens
    cam.data.dof.focus_distance = float(np.linalg.norm(np.array(focus if focus is not None else target, float) - loc))


def area(nm, loc, target, e, size, col):
    L = bpy.data.objects.new(nm, bpy.data.lights.new(nm, 'AREA')); L.data.energy = e; L.data.size = size; L.data.color = col
    L.location = loc; sc.collection.objects.link(L)
    d = np.array(target, float) - np.array(loc, float); L.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi / 2)
    return L


def spot(nm, loc, target, e, ang, col, blend=0.4):
    L = bpy.data.objects.new(nm, bpy.data.lights.new(nm, 'SPOT')); L.data.energy = e; L.data.spot_size = math.radians(ang); L.data.spot_blend = blend
    L.data.color = col; L.location = loc; sc.collection.objects.link(L)
    d = np.array(target, float) - np.array(loc, float); L.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi / 2)
    return L


def lights(scale=1.0, c=(0, 0, 1.5)):
    # teal-orange film look: warm key front-right, strong orange rim behind-left, cool blue back-right, soft top
    area('Key', (c[0] + 8, c[1] - 9, c[2] + 9), c, 1500 * scale, 5, (1, 0.9, 0.78))
    area('RimO', (c[0] - 9, c[1] + 8, c[2] + 4), c, 1900 * scale, 4, (1, 0.5, 0.22))
    area('RimB', (c[0] + 9, c[1] + 9, c[2] + 3), c, 1300 * scale, 4, (0.35, 0.6, 1))
    area('Top', (c[0], c[1], c[2] + 14), c, 500 * scale, 10, (0.85, 0.9, 1))


def ground(r=10, z=0.0):
    g = mesh_obj('Ground', cyl(r, r, 0.25, 128, (0, 0, z - 0.125)), mat('ground', NAVY, rough=0.22, coat=0.8))
    mesh_obj('Rim', cyl(r + 0.06, r + 0.06, 0.08, 128, (0, 0, z - 0.06)), mat('rim', ORANGE, emit=2.2))  # top below the ground: only the edge glows
    return g


def windows(name, base, lit=MUSTARD, scale=3.2, strength=2.0):
    # building facade: base colour + a grid of lit windows (brick texture on object coordinates -> emission)
    m = mat(name, base, rough=0.5)
    nt = m.node_tree; p = bsdf(m)
    tc = nt.nodes.new('ShaderNodeTexCoord'); br = nt.nodes.new('ShaderNodeTexBrick')
    br.inputs['Scale'].default_value = scale; br.inputs['Mortar Size'].default_value = 0.035
    br.inputs['Color1'].default_value = (*lin(lit), 1); br.inputs['Color2'].default_value = (*[x * 0.25 for x in lin(lit)], 1)
    br.inputs['Mortar'].default_value = (0, 0, 0, 1)
    try: br.offset = 0.0
    except Exception: pass
    nt.links.new(tc.outputs['Object'], br.inputs['Vector'])
    nt.links.new(br.outputs['Color'], p.inputs['Emission Color'])
    p.inputs['Emission Strength'].default_value = strength
    return m


# ---------------------------------------------------------------- v3 look (Aly 2026-10-27: "more professional or realistic and less
# childish… ال 3d مش متقن كفاية"): real shapes (lathe-turned chess pieces, coins, mics, lamp posts), physically based materials
# (marble, onyx, gold, glass, brushed steel, walnut, wet asphalt), soft studio light + a thin volumetric haze, muted palette.
# Same timings / camera moves as v2 (they are on Aly's words).
def lerp_(k, a, b): return a + (b - a) * k


def pbr(name, col, metal=0.0, rough=0.3, coat=0.0, trans=0.0, ior=1.45, sss=0.0, emit=0.0, emit_col=None, obj_glow=False):
    m = mat(name, col, metal=metal, rough=rough, coat=coat)
    p = bsdf(m)
    if trans:
        p.inputs['Transmission Weight'].default_value = trans; p.inputs['IOR'].default_value = ior
    if sss:
        p.inputs['Subsurface Weight'].default_value = sss
    if emit:
        p.inputs['Emission Color'].default_value = (*lin(emit_col or col), 1); p.inputs['Emission Strength'].default_value = emit
    if obj_glow:  # per-object glow colour (ob.color) -> emission: a piece "lights up" without changing its stone
        oi = m.node_tree.nodes.new('ShaderNodeObjectInfo')
        m.node_tree.links.new(oi.outputs['Color'], p.inputs['Emission Color'])
        p.inputs['Emission Strength'].default_value = 1.0
    return m


def lathe(profile, seg=64):  # turned shape from a (radius, z) profile, bottom -> top; r = 0 closes an end
    bm = bmesh.new(); rings = []
    for r, z in profile:
        rings.append([bm.verts.new((0, 0, z))] if r < 1e-4 else
                     [bm.verts.new((r * math.cos(2 * math.pi * i / seg), r * math.sin(2 * math.pi * i / seg), z)) for i in range(seg)])
    for a, b in zip(rings[:-1], rings[1:]):
        if len(a) == 1 and len(b) == 1: continue
        for i in range(seg):
            j = (i + 1) % seg
            if len(a) == 1: bm.faces.new((a[0], b[j], b[i]))
            elif len(b) == 1: bm.faces.new((a[i], a[j], b[0]))
            else: bm.faces.new((a[i], a[j], b[j], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm


def arc(cz, r, a0, a1, n=10):
    return [(max(0.0, r * math.cos(math.radians(a))), cz + r * math.sin(math.radians(a))) for a in np.linspace(a0, a1, n)]


# Staunton-style pawn (h ~0.95) and king (h ~1.95)
PAWN = [(0, 0), (0.40, 0), (0.40, 0.045), (0.37, 0.075), (0.385, 0.105), (0.32, 0.14), (0.26, 0.19), (0.22, 0.25), (0.185, 0.34),
        (0.16, 0.44), (0.145, 0.51), (0.23, 0.545), (0.235, 0.575), (0.16, 0.6), (0.12, 0.63)] + arc(0.78, 0.17, -45, 90, 12)
KING = [(0, 0), (0.5, 0), (0.5, 0.06), (0.46, 0.1), (0.475, 0.14), (0.4, 0.18), (0.33, 0.25), (0.27, 0.34), (0.225, 0.56), (0.195, 0.86),
        (0.185, 1.05), (0.3, 1.1), (0.31, 1.14), (0.2, 1.18), (0.22, 1.3), (0.3, 1.47), (0.335, 1.54), (0.3, 1.585), (0.12, 1.62), (0, 1.64)]


QUEEN = [(0, 0), (0.5, 0), (0.5, 0.06), (0.46, 0.1), (0.475, 0.14), (0.4, 0.18), (0.33, 0.25), (0.27, 0.34), (0.22, 0.56), (0.18, 0.86),
         (0.17, 1.03), (0.29, 1.08), (0.30, 1.12), (0.19, 1.16), (0.2, 1.26), (0.27, 1.42), (0.33, 1.52), (0.31, 1.55), (0.22, 1.56),
         (0.16, 1.6), (0.08, 1.63), (0, 1.64)]


def queen(name, m, loc, s=1.0):  # Staunton queen: coronet of 9 small balls on the rim + a ball on top (Aly: "خليه الوزير")
    obs = [mesh_obj(name, lathe([(r * s, z * s) for r, z in QUEEN]), m, loc)]
    for k in range(9):
        a = 2 * math.pi * k / 9
        obs.append(mesh_obj(f'{name}p{k}', sphere(0.05 * s, 16, 10, (0.31 * s * math.cos(a), 0.31 * s * math.sin(a), 1.575 * s)), m, loc))
    obs.append(mesh_obj(name + 'ball', sphere(0.085 * s, 24, 16, (0, 0, 1.72 * s)), m, loc))
    return obs


def king(name, m, loc, s=1.0):
    obs = [mesh_obj(name, lathe([(r * s, z * s) for r, z in KING]), m, loc)]
    obs.append(mesh_obj(name + 'cv', cube(0.07 * s, 0.07 * s, 0.32 * s, (0, 0, 1.78 * s), bevel=0.008), m, loc, smooth=False))
    obs.append(mesh_obj(name + 'ch', cube(0.24 * s, 0.07 * s, 0.07 * s, (0, 0, 1.82 * s), bevel=0.008), m, loc, smooth=False))
    return obs


def coin_bm(r=0.95, t=0.16):  # coin with a raised rim
    return lathe([(0, -t / 2), (r - 0.02, -t / 2), (r, -t / 2 + 0.02), (r, t / 2 - 0.02), (r - 0.02, t / 2), (r - 0.09, t / 2), (r - 0.11, t / 2 - 0.025),
                  (0, t / 2 - 0.025)], 96)


def haze(d=0.012):  # thin volumetric air — OFF: with a transparent film it greyed the whole frame (covers Aly + the board bg)
    return
    nt = w.node_tree
    vs = nt.nodes.new('ShaderNodeVolumeScatter'); vs.inputs['Density'].default_value = d
    out = next(n for n in nt.nodes if n.type == 'OUTPUT_WORLD'); nt.links.new(vs.outputs[0], out.inputs['Volume'])
    for k, v in (('volumetric_end', 70.0), ('volumetric_samples', 48), ('use_volumetric_shadows', True)):
        try: setattr(sc.eevee, k, v)
        except Exception: pass


def studio(scale=1.0, c=(0, 0, 1.5)):  # soft key, warm rim, cool back, big top softbox — no candy colours
    area('Key', (c[0] + 7, c[1] - 8, c[2] + 8), c, 2200 * scale, 7, (1, 0.94, 0.86))
    area('Rim', (c[0] - 8, c[1] + 7, c[2] + 5), c, 2000 * scale, 5, (1, 0.72, 0.45))
    area('Back', (c[0] + 8, c[1] + 8, c[2] + 4), c, 1200 * scale, 5, (0.62, 0.74, 1))
    area('Top', (c[0], c[1], c[2] + 12), c, 900 * scale, 12, (0.95, 0.96, 1))


def facade(name, base=(0.05, 0.06, 0.075), lit=(1, 0.8, 0.5), scale=9.0, strength=1.5, seed=0):
    # dark reflective glass + a window grid where only some windows are lit (brick cells x noise)
    m = pbr(name, base, metal=0.35, rough=0.08, coat=1.0)
    nt = m.node_tree; p = bsdf(m)
    tc = nt.nodes.new('ShaderNodeTexCoord'); br = nt.nodes.new('ShaderNodeTexBrick'); nz = nt.nodes.new('ShaderNodeTexNoise')
    br.inputs['Scale'].default_value = scale; br.inputs['Mortar Size'].default_value = 0.035  # regular window grid with frames (mortar is in brick space: 0.14 swallowed every window)
    br.inputs['Color1'].default_value = (1, 1, 1, 1); br.inputs['Color2'].default_value = (1, 1, 1, 1); br.inputs['Mortar'].default_value = (0, 0, 0, 1)
    nz.inputs['Scale'].default_value = 3.0 + 0.7 * seed  # calm patches of lit / dark windows (not QR-like noise)
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position = 0.52; ramp.color_ramp.elements[1].position = 0.55
    # lit/dark patches (noise -> ramp black..lit colour) feed the brick's two colours; the mortar stays black = window frames
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1); ramp.color_ramp.elements[1].color = (*lin(lit), 1)
    # walls: the brick grid runs along (x + y) horizontally and z vertically (object coords as they are gave vertical stripes)
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); add = nt.nodes.new('ShaderNodeMath'); add.operation = 'ADD'; com = nt.nodes.new('ShaderNodeCombineXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs[0]); nt.links.new(sep.outputs['X'], add.inputs[0]); nt.links.new(sep.outputs['Y'], add.inputs[1])
    nt.links.new(add.outputs[0], com.inputs['X']); nt.links.new(sep.outputs['Z'], com.inputs['Y'])
    br.inputs['Brick Width'].default_value = 0.32; br.inputs['Row Height'].default_value = 0.42
    nt.links.new(com.outputs[0], br.inputs['Vector']); nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    # each window lit or dark at random (the brick node picks Color1 / Color2 per brick, Bias = how many are dark) — real night towers
    br.inputs['Color1'].default_value = (*lin(lit), 1); br.inputs['Color2'].default_value = (0.0, 0.0, 0.0, 1)
    br.inputs['Bias'].default_value = 0.45
    nt.links.new(br.outputs['Color'], p.inputs['Emission Color'])
    p.inputs['Emission Strength'].default_value = strength
    return m


GOLD_M = lambda n='gold': pbr(n, (1.0, 0.77, 0.36), metal=1.0, rough=0.13)
MARBLE = lambda n='marble': pbr(n, (0.93, 0.92, 0.89), rough=0.14, coat=0.9, sss=0.12)
ONYX = lambda n='onyx': pbr(n, (0.03, 0.032, 0.038), rough=0.08, coat=1.0)
STEEL = lambda n='steel': pbr(n, (0.56, 0.57, 0.58), metal=1.0, rough=0.28)  # blender-skills pbr-values: iron/steel
WALNUT = lambda n='walnut': pbr(n, (0.22, 0.12, 0.07), rough=0.32, coat=0.7)


def scene_podcast(N):
    # "أغلب البودكاستات بتستضيف… ضيف مشهور": a real-looking studio — acoustic panels, LED strips, an ON AIR neon, a walnut desk, two
    # broadcast mics on boom arms; the host = a marble pawn, the famous guest = a gold king under a spot (haze shows the beam).
    # Camera glides, then pushes onto the king's cross: the gold fills the frame -> cut to the gold tower.
    studio(0.6, (0, 0.8, 1.3)); haze(0.02)
    mesh_obj('floor', cyl(7, 7, 0.2, 96, (0, 0, -0.1)), pbr('fl', (0.06, 0.06, 0.07), rough=0.2, coat=0.8))
    panel = pbr('panel', (0.09, 0.09, 0.11), rough=0.85)
    for ix in range(12):
        for iz in range(5):
            mesh_obj(f'ap{ix}_{iz}', cube(0.68, 0.12, 0.84, (0, 0, 0), bevel=0.03), panel, (-4.1 + ix * 0.74, 3.2, 0.5 + iz * 0.9), smooth=False)
    led_o, led_b = pbr('lo', (1, 0.55, 0.25), emit=8), pbr('lb', (0.4, 0.6, 1), emit=6)
    mesh_obj('led1', cube(9, 0.04, 0.04, (0, 3.1, 4.6)), led_o, smooth=False)
    mesh_obj('led2', cube(9, 0.04, 0.04, (0, 3.1, 0.06)), led_b, smooth=False)
    onair_box = mesh_obj('oab', cube(1.7, 0.1, 0.62, (0, 0, 0), bevel=0.04), pbr('oabm', (0.06, 0.02, 0.02), rough=0.3, coat=0.6), (-2.3, 3.05, 3.4), smooth=False)
    onair = text('ON AIR', 0.36, 0.03, pbr('oa', (1, 0.12, 0.08), emit=0.0), (-2.3, 2.98, 3.4))
    mesh_obj('desk', cube(3.6, 1.1, 0.1, (0, 0, 0.8), bevel=0.03), WALNUT(), smooth=False)
    mesh_obj('deskb', cube(3.0, 0.6, 0.78, (0, 0.15, 0.39), bevel=0.03), pbr('db', (0.05, 0.05, 0.06), rough=0.4), smooth=False)
    host = mesh_obj('host', lathe([(r * 1.55, z * 1.55) for r, z in PAWN]), MARBLE('hm'), (-1.05, 0.85, 0.02))
    gold = GOLD_M('gk')
    guest = queen('guest', gold, (1.05, 0.85, 0.02), 1.0)
    grille = pbr('grille', (0.08, 0.08, 0.09), metal=0.7, rough=0.45)
    for i, (x, a) in enumerate([(-0.6, 0.35), (0.6, -0.35)]):
        mesh_obj(f'mb{i}', lathe([(0, 0), (0.07, 0), (0.07, 0.3), (0.085, 0.32), (0.085, 0.42), (0.07, 0.44), (0, 0.46)], 32), grille, (x, 0.45, 1.25), (0.7, 0, a))
        mesh_obj(f'arm{i}', cyl(0.018, 0.018, 0.9, 12, (0, 0, 0.45)), STEEL(f'st{i}'), (x + (0.35 if x > 0 else -0.35), 0.75, 0.85), (0.6, 0, -0.7 if x > 0 else 0.7))
    sp = spot('gs', (1.05, -0.8, 6.5), (1.05, 0.85, 1.0), 4200, 14, (1, 0.86, 0.6), 0.25)
    spot('hs', (-1.05, -0.8, 6.5), (-1.05, 0.85, 0.8), 1500, 16, (0.75, 0.82, 1), 0.35)
    CR = (1.05, 0.85, 1.7)

    def at(f):
        bsdf(onair.data.materials[0]).inputs['Emission Strength'].default_value = 2.6 + 0.6 * math.sin(f / 3)  # red stays red (AgX bleaches very bright red)
        bsdf(gold).inputs['Emission Strength'].default_value = 0.0
        sp.data.energy = 4200 + 14000 * E2(f, N - 26, N)
        k = E2(f, 0, N - 30); k2 = E2(f, N - 34, N)
        cam_p = (lerp_(k, -3.6, -1.4) + 2.4 * k2, lerp_(k, -7.4, -5.4) + 4.9 * k2, lerp_(k, 2.4, 2.0) + 0.1 * k2)
        tgt = (lerp_(k, 0.0, 0.6) + 0.45 * k2, 0.85, lerp_(k, 1.3, 1.5) + 0.35 * k2)
        look(cam_p, tgt, lens=32 + 58 * k2, focus=CR if k > 0.4 else (0, 0.85, 1.2), f=f)
    return at


def scene_tower(N):
    # the big success stories: a night city of glass towers (lit windows), glowing avenues, one GOLD skyscraper with metal fins rises
    # floor by floor, a minted gold coin with $ on top, coins spiralling up
    studio(1.0, (0, 0, 3)); haze(0.008)
    mesh_obj('Ground', cyl(9, 9, 0.25, 128, (0, 0, -0.125)), pbr('asph', (0.035, 0.037, 0.045), rough=0.22, coat=0.7))
    mesh_obj('Rim', cyl(9.06, 9.06, 0.08, 128, (0, 0, -0.06)), pbr('rim', (1, 0.6, 0.3), emit=1.6))
    st = pbr('street', (1, 0.78, 0.5), emit=1.6)
    for i in range(-4, 5):
        mesh_obj(f'sx{i}', cube(17.5, 0.035, 0.012, (0, i * 2.0 + 1.0, 0.006)), st, smooth=False)
        mesh_obj(f'sy{i}', cube(0.035, 17.5, 0.012, (i * 2.0 + 1.0, 0, 0.006)), st, smooth=False)
    mats = [facade(f'fc{i}', lit=[(1, 0.8, 0.5), (0.85, 0.9, 1), (1, 0.9, 0.7)][i % 3], seed=i) for i in range(3)]
    roof = pbr('roof', (0.12, 0.12, 0.13), rough=0.6)
    blocks = []
    for i in range(110):
        ang = random.uniform(0, 2 * math.pi); r = random.uniform(1.9, 8.3)
        x, y = r * math.cos(ang), r * math.sin(ang)
        if any(math.hypot(x - b[0], y - b[1]) < 0.95 for b in blocks): continue
        h = random.uniform(0.6, 2.8) * (1.3 - r / 10)
        wdt = random.choice([0.6, 0.7, 0.8])
        ob = mesh_obj(f'b{i}', cube(wdt, wdt, 1, (0, 0, 0.5), bevel=0.012), mats[i % 3], (x, y, 0), smooth=False)
        rt = mesh_obj(f'r{i}', cube(wdt * 0.4, wdt * 0.3, 0.12, (0, 0, 0.06)), roof, (x, y, 0), smooth=False)
        blocks.append((x, y, h, ob, rt, random.uniform(0, 26)))
    gold = GOLD_M('gold'); band = pbr('band', (1, 0.88, 0.62), emit=3.5); fin = pbr('fin', (0.95, 0.72, 0.35), metal=1.0, rough=0.25)
    floors = []
    for k in range(14):
        wd = 1.5 - k * 0.045
        fl = mesh_obj(f'f{k}', cube(wd, wd, 0.62, (0, 0, 0.31), bevel=0.02), gold, (0, 0, k * 0.66), smooth=False)
        bd = mesh_obj(f'w{k}', cube(wd + 0.01, wd + 0.01, 0.05, (0, 0, 0.6)), band, (0, 0, k * 0.66), smooth=False)
        fins = [mesh_obj(f'fn{k}_{j}', cube(0.035, 0.035, 0.62, (0, 0, 0.31)), fin, ((wd / 2 + 0.01) * sx, (wd / 2 + 0.01) * sy, k * 0.66), smooth=False)
                for j, (sx, sy) in enumerate([(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1.0), (0, -1.0), (1.0, 0), (-1.0, 0)])]
        floors.append([fl, bd] + fins)
    spire = mesh_obj('spire', lathe([(0.2, 0), (0.12, 0.3), (0.04, 1.2), (0, 1.45)], 32), gold, (0, 0, 14 * 0.66))
    coin = mesh_obj('coin', coin_bm(), pbr('coinm', (1, 0.79, 0.4), metal=1.0, rough=0.12), (0, 0, 0))
    dol = text('$', 1.2, 0.03, pbr('dol', (1, 0.79, 0.4), metal=1.0, rough=0.22), (0, 0, 0))
    dol.parent = coin; dol.location = (0, 0, 0.055); dol.rotation_euler = (0, 0, 0)
    TOP = 14 * 0.66 + 1.4
    ups = [spot(f'up{i}', (2.2 * math.cos(a), 2.2 * math.sin(a), 0.2), (0, 0, 6), 0, 20, (1, 0.8, 0.5), 0.3) for i, a in enumerate([0.6, 2.7, 4.8])]
    coin_l = bpy.data.objects.new('coinL', bpy.data.lights.new('coinL', 'POINT')); coin_l.data.color = (1, 0.82, 0.5); sc.collection.objects.link(coin_l)
    cm = pbr('smallc', (1, 0.79, 0.4), metal=1.0, rough=0.18)
    small = [mesh_obj(f'sc{i}', coin_bm(0.22, 0.04), cm, (0, 0, -5)) for i in range(16)]

    def at(f):
        for x, y, h, ob, rt, d in blocks:
            k = back(ease(f, 2 + d, 18 + d)); ob.scale = (1, 1, max(0.001, h * k)); rt.location.z = h * k; rt.hide_render = k < 0.05
        for k, obs in enumerate(floors):
            p = back(ease(f, 60 + k * 6, 70 + k * 6))
            for o in obs: o.scale = (1, 1, max(0.001, p)); o.hide_render = p <= 0.001
        p = back(ease(f, 60 + 14 * 6, 72 + 14 * 6)); spire.scale = (1, 1, max(0.001, p)); spire.hide_render = p <= 0.001
        for L in ups: L.data.energy = 3000 * ease(f, 58, 80)
        c = back(ease(f, 150, 172), 2.2)
        coin.location = (0, 0, TOP + 1.4 * c + 0.12 * math.sin(f / 9)); coin.scale = (c + 1e-3,) * 3
        coin.rotation_euler = (math.pi / 2, 0, f / 12); coin.hide_render = c <= 0.001
        coin_l.location = (0, -1.2, TOP + 1.4); coin_l.data.energy = 700 * c
        for i, o in enumerate(small):
            t = (f - 160 - i * 4) / 60.0
            if t <= 0: o.hide_render = True; continue
            o.hide_render = False
            a = i * 2.4 + t * 5; r = 2.4 - 0.6 * min(1, t)
            o.location = (r * math.cos(a), r * math.sin(a), 0.5 + t * 9); o.rotation_euler = (t * 7, t * 4, a)
        top = min(TOP, 0.66 * max(0.0, (f - 60) / 6.0))
        k1 = E2(f, 0, 62)
        ang = math.radians(-120 + 70 * E2(f, 0, N))
        dist = lerp_(k1, 6.0, 10.5); hgt = lerp_(k1, 24.0, 1.1)
        k2 = E2(f, 62, 160); k3 = E2(f, 175, N)
        hgt += 5.5 * k2 - 1.0 * k3
        dist += 3.2 * k3
        tz = lerp_(k1, 0.0, 1.8) + (top + 0.6) * 0.62 * k2 + 2.4 * k3
        lens = lerp_(k1, 30, 20) + 6 * k3
        look((dist * math.cos(ang), dist * math.sin(ang), hgt), (0, 0, tz), lens=lens, focus=(0, 0, max(1.0, tz)), f=f)
    return at


def scene_road(N):
    # night street, wet asphalt reflecting lamp posts; stop 1 = a small shop + a sleek rocket lifting off; stop 2 = a store reaches a
    # level (glass bars), then its steel shutter rolls down and the lights die; stop 3 = a new modern building, its door glows
    studio(1.2, (7, 2, 1.5)); haze(0.014)
    mesh_obj('road', cube(30, 3.0, 0.12, (7, 0, -0.06)), pbr('asph', (0.025, 0.027, 0.032), rough=0.06, coat=1.0), smooth=False)
    mesh_obj('pave', cube(30, 6.0, 0.2, (7, 4.5, -0.1)), pbr('pave', (0.2, 0.2, 0.21), rough=0.7), smooth=False)
    mesh_obj('kerb', cube(30, 0.22, 0.2, (7, 1.6, 0.1)), pbr('kerb', (0.4, 0.4, 0.41), rough=0.6), smooth=False)
    dash = pbr('dash', (0.95, 0.85, 0.6), rough=0.5, emit=0.4)
    for i in range(26): mesh_obj(f'd{i}', cube(0.7, 0.1, 0.012, (0, 0, 0.006)), dash, (-6 + i * 1.2, 0, 0), smooth=False)
    steel = STEEL('pole'); bulb = pbr('bulb', (1, 0.85, 0.6), emit=14)
    for i in range(8):
        x = -3 + i * 3.4
        mesh_obj(f'lp{i}', lathe([(0.09, 0), (0.07, 0.1), (0.045, 0.3), (0.04, 2.6), (0, 2.62)], 24), steel, (x, 1.75, 0))
        mesh_obj(f'la{i}', cube(0.05, 0.4, 0.04, (0, -0.2, 2.6)), steel, (x, 1.75, 0), smooth=False)
        mesh_obj(f'lh{i}', cube(0.22, 0.32, 0.06, (0, 0, 0), bevel=0.01), bulb, (x, 1.38, 2.56), smooth=False)
        P = bpy.data.objects.new(f'pl{i}', bpy.data.lights.new(f'pl{i}', 'SPOT')); P.data.energy = 600; P.data.spot_size = math.radians(70)
        P.data.color = (1, 0.8, 0.55); P.location = (x, 1.38, 2.5); P.rotation_euler = (0, 0, 0); sc.collection.objects.link(P)
    # stop 1: a small shop (dark frame, lit glass front, fabric awning) + a sleek rocket
    shop1 = [mesh_obj('k1', cube(1.7, 1.2, 1.4, (0, 0, 0.7), bevel=0.02), pbr('k1m', (0.1, 0.1, 0.11), rough=0.4), (0, 2.6, 0), smooth=False),
             mesh_obj('k1g', cube(1.4, 0.02, 0.9, (0, 0, 0.62)), pbr('k1g', (1, 0.82, 0.55), emit=1.3), (0, 1.99, 0), smooth=False)]
    shop1 += [mesh_obj(f'aw{i}', cube(0.36, 1.2, 0.03, (0, 0, 0)), pbr(f'awm{i}', (0.72, 0.28, 0.14) if i % 2 else (0.9, 0.86, 0.78), rough=0.8),
                       (-0.72 + i * 0.36, 2.05, 1.5), (math.radians(-22), 0, 0), smooth=False) for i in range(5)]
    RX, RY = 1.6, 2.3
    rocket = [mesh_obj('rbody', lathe([(0, 0), (0.17, 0), (0.2, 0.15), (0.2, 0.8), (0.17, 1.0), (0.1, 1.18), (0, 1.3)], 48), pbr('rb', (0.92, 0.92, 0.93), rough=0.12, coat=1), (RX, RY, 0)),
              mesh_obj('rwin', lathe([(0, 0), (0.07, 0.0), (0.07, 0.02), (0, 0.03)], 32), pbr('rw', (0.4, 0.6, 1), metal=0.8, rough=0.05, emit=1.0), (RX, RY - 0.2, 0.7), (math.pi / 2, 0, 0))]
    for i in range(3):
        an = i * 2 * math.pi / 3
        rocket.append(mesh_obj(f'fin{i}', cube(0.025, 0.3, 0.38, (0.22 * math.cos(an), 0.22 * math.sin(an), 0.2), bevel=0.008), pbr(f'fm{i}', (0.72, 0.28, 0.14), metal=0.3, rough=0.3), (RX, RY, 0), (0, 0, an), smooth=False))
    flame = mesh_obj('flame', lathe([(0, 0), (0.15, 0.05), (0.1, 0.4), (0, 0.75)], 24), pbr('fl', (1, 0.7, 0.35), emit=12), (RX, RY, 0), (math.pi, 0, 0))
    fl_light = bpy.data.objects.new('flL', bpy.data.lights.new('flL', 'POINT')); fl_light.data.color = (1, 0.6, 0.3); sc.collection.objects.link(fl_light)
    smoke_m = pbr('smoke', (0.7, 0.7, 0.72), rough=0.95)
    puffs = [mesh_obj(f'pf{i}', sphere(0.3, 20, 12), smoke_m, (RX, RY, -3)) for i in range(16)]
    # stop 2: a real STORE (Aly 2026-10-27: "المحل اللي اتقفل مش باين انه محل حط تفاصيل اكتر") — brick ground floor with a lit display
    # window (shelves + products), a glass door with a handle, striped fabric awning, a lit SHOP sign, an OPEN neon that turns into
    # CLOSED; it grows with the glass bars (the level), then a ribbed steel shutter rolls down over the whole front and the lights die.
    # PBR values from tools/external/blender-skills (blender-pbr-materials/references/pbr-values.md): brick, steel, glass, fabric.
    root = bpy.data.objects.new('storeRoot', None); root.location = (7, 2.8, 0); sc.collection.objects.link(root)
    def part(name, bm, m, loc, rot=(0, 0, 0), smooth=False):
        o = mesh_obj(name, bm, m, loc, rot, smooth=smooth); o.parent = root; return o
    FYs = -0.8                                   # store front (relative to root), faces -Y
    brick = pbr('brick', (0.3, 0.085, 0.045), rough=0.85)
    part('upper', cube(2.4, 1.6, 1.25, (0, 0, 1.3 + 0.625), bevel=0.02), facade('stf', scale=7.0, strength=1.3), (0, 0, 0))
    part('cornice', cube(2.5, 1.7, 0.08, (0, 0, 1.3)), STEEL('corn'), (0, 0, 0))
    for sx in (-1, 1):
        part(f'pier{sx}', cube(0.22, 1.6, 1.3, (sx * 1.09, 0, 0.65)), brick, (0, 0, 0))
    part('back', cube(2.0, 0.05, 1.3, (0, 0.75, 0.65)), pbr('inback', (0.85, 0.7, 0.5), emit=0.0), (0, 0, 0))
    inside_l = pbr('inl', (1, 0.82, 0.55), emit=2.8)
    part('inglow', cube(1.95, 0.02, 1.2, (0, 0.72, 0.65)), inside_l, (0, 0, 0))
    frm = pbr('sfrm', (0.06, 0.06, 0.065), metal=0.8, rough=0.35)
    glass = pbr('glass', (1, 1, 1), rough=0.02, trans=1.0, ior=1.5)
    # display window (left 2/3) + door (right 1/3)
    # (no glass pane: EEVEE transmission went dark and hid the lit shelves — the frames read as a window)
    for x in (-0.95, 0.31, 0.98):
        part(f'mul{x}', cube(0.05, 0.06, 1.12, (x, FYs, 0.6)), frm, (0, 0, 0))
    part('wtop', cube(2.0, 0.06, 0.05, (0, FYs, 1.15)), frm, (0, 0, 0))
    part('wsill', cube(1.3, 0.12, 0.12, (-0.32, FYs, 0.12)), frm, (0, 0, 0))
    part('door', cube(0.62, 0.02, 1.05, (0.645, FYs + 0.6, 0.55)), pbr('dark', (0.03, 0.03, 0.035), rough=0.3), (0, 0, 0))  # dark shop depth behind the door frame
    part('handle', cyl(0.012, 0.012, 0.35, 12, (0, 0, 0)), STEEL('hdl'), (0.42, FYs - 0.04, 0.6))
    # shelves with products behind the glass
    shelf_m = pbr('shelf', (0.35, 0.22, 0.12), rough=0.5)
    prod = [pbr(f'pr{i}', c, rough=0.4, coat=0.4) for i, c in enumerate([(0.72, 0.18, 0.1), (0.9, 0.75, 0.3), (0.2, 0.4, 0.7), (0.85, 0.85, 0.82), (0.3, 0.55, 0.3)])]
    for si, z in enumerate((0.3, 0.6, 0.9)):
        part(f'sh{si}', cube(1.15, 0.22, 0.025, (-0.32, -0.5, z)), shelf_m, (0, 0, 0))
        for k in range(7):
            m_ = prod[(k + si * 2) % 5]; px = -0.82 + k * 0.165
            if (k + si) % 3 == 0: part(f'can{si}{k}', cyl(0.04, 0.04, 0.12, 16, (px, -0.5, z + 0.072)), m_, (0, 0, 0), smooth=True)
            else: part(f'box{si}{k}', cube(0.1, 0.07, 0.15 + 0.04 * (k % 2), (px, -0.5, z + 0.09 + 0.02 * (k % 2)), bevel=0.005), m_, (0, 0, 0))
    open_m = pbr('open', (0.25, 1, 0.4), emit=3.0); closed_m = pbr('closed', (1, 0.12, 0.08), emit=0.0)
    o_open = text('OPEN', 0.17, 0.01, open_m, (7 - 0.55, 2.8 + FYs + 0.04, 0.95)); o_open.parent = root; o_open.location = (-0.55, FYs + 0.04, 0.95)
    o_closed = text('CLOSED', 0.15, 0.01, closed_m, (0, 0, 0)); o_closed.parent = root; o_closed.location = (-0.55, FYs + 0.04, 0.95)
    # awning (striped fabric with sheen) + lit SHOP sign
    for i in range(8):
        aw = pbr(f'aw{i}', (0.62, 0.16, 0.08) if i % 2 else (0.88, 0.85, 0.78), rough=0.9)
        try: bsdf(aw).inputs['Sheen Weight'].default_value = 0.4
        except Exception: pass
        part(f'aw{i}', cube(0.27, 0.55, 0.02, (0, 0, 0)), aw, (-0.945 + i * 0.27, FYs - 0.22, 1.24), (math.radians(-24), 0, 0))
    sign_m = pbr('sgn', (1, 0.82, 0.5), emit=3.0)
    part('signbox', cube(1.5, 0.08, 0.26, (0, 0, 0), bevel=0.01), pbr('sb', (0.08, 0.08, 0.09), metal=0.6, rough=0.3), (0, FYs - 0.06, 1.48))
    sign = text('SHOP', 0.2, 0.015, sign_m, (0, 0, 0)); sign.parent = root; sign.location = (0, FYs - 0.11, 1.48)
    slats = [part(f'sl{i}', cyl(0.03, 0.03, 2.05, 12, (0, 0, 0)), STEEL(f'slm{i}'), (0, FYs - 0.1, 1.14 - i * 0.066), (0, math.pi / 2, 0)) for i in range(17)]
    shutter_box = part('shbox', cube(2.1, 0.14, 0.1, (0, FYs - 0.1, 1.19)), STEEL('shb'), (0, 0, 0))
    store_glass = inside_l
    bars = [mesh_obj(f'bar{i}', cube(0.42, 0.42, 1.0, (0, 0, 0.5), bevel=0.02), pbr(f'barm{i}', (0.9, 0.95, 1), rough=0.03, trans=0.9, emit=0.6, emit_col=(1, 0.8, 0.5)),
                     (5.9 + i * 0.75, 4.6, 0), smooth=False) for i in range(4)]
    bh = [1.0, 1.9, 2.9, 3.6]
    new = mesh_obj('new', cube(2.4, 1.8, 3.2, (0, 0, 1.6), bevel=0.02), facade('nwf', base=(0.06, 0.08, 0.1), lit=(0.85, 0.92, 1), scale=4.5, strength=1.8), (14, 2.9, 0), smooth=False)
    door = mesh_obj('door', cube(0.8, 0.04, 1.4, (0, 0, 0.7)), pbr('dr', (1, 0.85, 0.6), emit=9), (14, 1.98, 0), smooth=False)
    door_l = area('doorL', (14, 1.6, 0.9), (14, -1, 0), 0, 1.2, (1, 0.82, 0.55))
    arrow_m = pbr('arr', (1, 0.78, 0.4), metal=1.0, rough=0.15, emit=1.5)
    arc_ = [mesh_obj(f'a{i}', sphere(0.09, 16, 10), arrow_m, (8.3 + 4.4 * (i / 15), 2.4, 3.0 + 1.8 * math.sin(math.pi * i / 15))) for i in range(16)]
    head = mesh_obj('ahead', lathe([(0, 0), (0.24, 0), (0, 0.45)], 32), arrow_m, (12.75, 2.4, 3.0), (0, math.radians(140), 0))
    flag = [mesh_obj('pole', lathe([(0.03, 0), (0.025, 2.0), (0, 2.02)], 16), steel, (-1.6, 1.9, 0)),
            mesh_obj('flag', cube(0.7, 0.02, 0.45, (0.37, 0, 1.75)), pbr('flg', (0.72, 0.28, 0.14), rough=0.8), (-1.6, 1.9, 0), smooth=False)]

    def pop(obs, f, a, b):
        p = back(ease(f, a, b))
        for o in obs: o.scale = (max(1e-3, p),) * 3; o.hide_render = p <= 1e-3
        return p

    def at(f):
        pop(flag, f, 0, 14); pop(shop1, f, 8, 24)
        up = max(0, f - 44) ** 1.8 * 0.0035
        for o in rocket: o.location.z = up + (0.7 if o.name == 'rwin' else 0)
        flame.location.z = up; flame.scale = (1, 1, 0.6 + 0.4 * math.sin(f * 1.7)) if f > 36 else (1e-3,) * 3
        flame.hide_render = f <= 36
        fl_light.location = (RX, RY - 0.4, up - 0.2); fl_light.data.energy = 900 * ease(f, 36, 44) * (0.85 + 0.15 * math.sin(f * 2.3))
        for i, o in enumerate(puffs):  # smoke balls looked childish (review 2026-10-27) -> off
            o.hide_render = True; continue
            t = (f - 38 - i * 3) / 40.0
            if t <= 0 or t >= 1: o.hide_render = True; continue
            o.hide_render = False
            o.location = (RX + (i % 2 * 2 - 1) * (0.3 + 1.6 * t) * (0.6 + 0.4 * (i % 3)), RY + 0.2 * math.sin(i), 0.15 + 0.5 * t)
            o.scale = (0.4 + 2.2 * t * (1 - 0.4 * t),) * 3
        pop(rocket, f, 18, 30)
        g = back(ease(f, 112, 134))
        root.scale = (1, 1, max(1e-3, g))
        for o in root.children: o.hide_render = g <= 1e-3
        cl = f >= 214  # OPEN -> CLOSED
        o_open.hide_render = cl or g <= 1e-3; o_closed.hide_render = (not cl) or g <= 1e-3
        bsdf(closed_m).inputs['Emission Strength'].default_value = 3.0 if cl else 0.0
        for i, b in enumerate(bars):
            p = back(ease(f, 122 + i * 7, 136 + i * 7)); b.scale = (1, 1, max(1e-3, bh[i] * p)); b.hide_render = p <= 1e-3
        c = ease(f, 198, 220)
        for i, sl in enumerate(slats): sl.hide_render = g <= 1e-3 or c * 17 < i + 0.5
        grey = ease(f, 208, 230)
        bsdf(store_glass).inputs['Emission Strength'].default_value = 3.0 * (1 - grey)
        bsdf(sign_m).inputs['Emission Strength'].default_value = 3.0 * (1 - grey) * (1 if f < 208 or (f // 3) % 4 else 0.2)
        for i, o in enumerate(arc_):
            p = ease(f, 212 + i * 2, 218 + i * 2); o.scale = (max(1e-3, p),) * 3; o.hide_render = p <= 1e-3
        pop([head], f, 244, 254)
        n = back(ease(f, 226, 250)); new.scale = (1, 1, max(1e-3, n)); new.hide_render = n <= 1e-3
        pop([door], f, 246, 258); door_l.data.energy = 900 * ease(f, 248, 260)
        x = 0.8 + 6.2 * E2(f, 60, 125) + 7.0 * E2(f, 212, 252)
        k = E2(f, 254, N)
        tx = x + 0.6 - 7.0 * k
        look((x - 2.6 - 3.0 * k, -5.6 - 7 * k, 1.4 + 6.0 * k), (tx, 2.4, 1.3 + 0.6 * k), lens=28 + 6 * k, focus=(x + 0.6, 2.6, 1.3), f=f)
    return at


def scene_crowd(N):
    # a giant chess board: 300 marble / onyx pawns, ONE gold king on a marble pedestal under a spot (the rare extreme story).
    # Dolly zoom on the king, then a crane up as the pawns light up warm from the centre outwards (the many = us).
    studio(0.7, (0, 0, 1)); haze(0.012)
    sq = 0.85; n = 20
    bm = bmesh.new()
    for i in range(n):
        for j in range(n):
            x0, y0 = (i - n / 2) * sq, (j - n / 2) * sq
            vs = [bm.verts.new((x0, y0, 0)), bm.verts.new((x0 + sq, y0, 0)), bm.verts.new((x0 + sq, y0 + sq, 0)), bm.verts.new((x0, y0 + sq, 0))]
            fc = bm.faces.new(vs); fc.material_index = (i + j) % 2
    me = bpy.data.meshes.new('board'); bm.to_mesh(me); bm.free()
    board_o = bpy.data.objects.new('board', me); sc.collection.objects.link(board_o)
    me.materials.append(pbr('bw', (0.8, 0.78, 0.74), rough=0.18, coat=0.8)); me.materials.append(pbr('bb', (0.05, 0.05, 0.06), rough=0.12, coat=1.0))
    mesh_obj('edge', cube(n * sq + 0.4, n * sq + 0.4, 0.25, (0, 0, -0.125)), WALNUT('edge'), smooth=False)
    pm_w, pm_b = pbr('pw', (0.93, 0.92, 0.89), rough=0.14, coat=0.9, sss=0.12, obj_glow=True), pbr('pb', (0.04, 0.04, 0.05), rough=0.08, coat=1.0, obj_glow=True)
    mw, mb = bpy.data.meshes.new('pawnw'), bpy.data.meshes.new('pawnb')
    for me_, m_ in ((mw, pm_w), (mb, pm_b)):
        b_ = lathe([(r * 0.78, z * 0.78) for r, z in PAWN], 40); b_.to_mesh(me_); b_.free()
        for poly in me_.polygons: poly.use_smooth = True
        me_.materials.append(m_)
    pawns = []
    for i in range(n):
        for j in range(n):
            if (i, j) in ((10, 10), (9, 10), (10, 9), (9, 9)) or random.random() < 0.22: continue
            x, y = (i - n / 2 + 0.5) * sq, (j - n / 2 + 0.5) * sq
            ob = link(f'p{i}_{j}', mw if (i + j) % 2 else mb, (x, y, 0)); ob.color = (0, 0, 0, 1)
            pawns.append((ob, math.hypot(x, y)))
    gold = GOLD_M('goldk')
    G = (0.0, 0.0)
    ped = mesh_obj('ped', lathe([(0.75, 0), (0.75, 0.08), (0.62, 0.14), (0.55, 0.2), (0.55, 1.0), (0.62, 1.06), (0.68, 1.12), (0, 1.12)], 64), MARBLE('pedm'), (0, 0, 0))
    kg = queen('queen', gold, (0, 0, 0), 0.85)
    sp = spot('Spot', (0.4, -0.6, 11), (0, 0, 2), 7000, 12, (1, 0.86, 0.6), 0.2)

    def at(f):
        h = 3.2 * back(ease(f, 4, 36), 1.2)
        ped.scale = (1, 1, max(1e-3, h / 1.12))
        for o in kg: o.location.z = h; o.rotation_euler = (0, 0, f / 30)
        dim = ease(f, 200, 250)
        sp.data.energy = 7000 * (1 - 0.7 * dim)
        for ob, r in pawns:
            k = ease(f, 190 + r * 6, 205 + r * 6)
            ob.color = (1.0 * k * 0.9, 0.55 * k * 0.9, 0.25 * k * 0.9, 1)
        top = (G[0], G[1], h + 1.1)
        k = E2(f, 36, 120)
        dist = 3.0 + 13.0 * k
        lens = 22 * dist / 3.0
        el = math.radians(8 + 4 * k)
        k3 = E2(f, 140, 290)
        dist = dist + 2.0 * k3
        lens = lens * (1 - k3) + 42 * k3
        el = el + math.radians(48) * k3
        az = math.radians(-62 + 30 * k3)
        tgt = (G[0], G[1], top[2] * (1 - k3) + 0.3 * k3)
        look((tgt[0] + dist * math.cos(el) * math.cos(az), tgt[1] + dist * math.cos(el) * math.sin(az), tgt[2] + dist * math.sin(el)), tgt, lens=lens, focus=top, f=f, shake=0.015)
    return at


def scene_three(N):
    # Karim's 3 projects as framed prints in brushed-steel frames on a black glossy floor, each lit by its own spot when it rises
    studio(0.7, (0, 0, 2)); haze(0.012)
    mesh_obj('floor', cube(26, 10, 0.2, (0, 2, -0.1)), pbr('floor', (0.02, 0.022, 0.026), rough=0.05, coat=1.0), smooth=False)
    line = mesh_obj('line', cube(1, 0.05, 0.02, (0.5, 0, 0.01)), pbr('ln', (1, 0.8, 0.45), emit=4), (-8, -1.6, 0), smooth=False)
    T = A.tex or '.'
    cards = []
    names = [('courzerve.jpg', 'Courzerve'), ('kikos.jpg', "Kiko's Snacks"), ('fpl.jpg', 'FPL Champ')]
    for k, (img, nm) in enumerate(names):
        x = -5.2 + k * 5.2
        frame = mesh_obj(f'cf{k}', cube(3.36, 0.16, 3.36, (0, 0.08, 0), bevel=0.03), STEEL(f'cfm{k}'), (x, 0, 2.2), smooth=False)
        mat_ = mesh_obj(f'mt{k}', cube(3.12, 0.02, 3.12, (0, 0, 0)), pbr(f'mtm{k}', (0.95, 0.94, 0.9), rough=0.8), (x, -0.005, 2.2), smooth=False)
        pic = mesh_obj(f'cp{k}', plane_uv(2.9, 2.9), mat(f'cpm{k}', (1, 1, 1), tex=os.path.join(T, img)), (x, -0.025, 2.2), smooth=False)
        for o in (mat_, pic): o.parent = frame; o.location = (0, -0.03 if o is mat_ else -0.045, 0)
        disc = mesh_obj(f'bd{k}', coin_bm(0.42, 0.1), GOLD_M(f'bdm{k}'), (x - 1.55, -0.25, 3.75), (math.pi / 2, 0, 0))
        num = text(str(k + 1), 0.55, 0.02, pbr(f'nm{k}', (0.12, 0.08, 0.04), metal=0.5, rough=0.3), (x - 1.55, -0.33, 3.73))
        lab = text(nm, 0.36, 0.02, pbr(f'lb{k}', (0.92, 0.92, 0.9), rough=0.3, emit=0.4), (x, -0.3, 0.25))
        dot = mesh_obj(f'dot{k}', cyl(0.14, 0.14, 0.03, 32), pbr(f'dt{k}', (1, 0.8, 0.45), emit=4), (x, -1.6, 0.03))
        light = spot(f'cs{k}', (x + 0.4, -4.5, 7.5), (x, 0, 1.6), 0, 24, (1, 0.92, 0.8), 0.3)
        cards.append((frame, disc, num, lab, dot, x, light))
    arr_m = pbr('arr', (1, 0.8, 0.45), metal=1.0, rough=0.15, emit=1.0)
    arrows = [[mesh_obj(f'ar{k}{i}', sphere(0.06, 12, 8), arr_m, (-5.2 + k * 5.2 + 1.9 + 1.4 * (i / 8), -0.4, 3.0 + 0.9 * math.sin(math.pi * i / 8))) for i in range(9)] for k in range(2)]

    def at(f):
        line.scale = (max(1e-3, 16.4 * ease(f, 0, 30)), 1, 1)
        for k, (fr, bd, num, lab, dot, x, light) in enumerate(cards):
            a0 = 26 + k * 34
            p = back(ease(f, a0, a0 + 22), 1.3)
            fr.location.z = -1.6 + 3.8 * p; fr.rotation_euler = (0, 0, math.radians(70 * (1 - ease(f, a0, a0 + 26))))
            fr.hide_render = p <= 1e-3
            for o in fr.children: o.hide_render = fr.hide_render
            q = back(ease(f, a0 + 18, a0 + 30)); bd.scale = num.scale = (max(1e-3, q),) * 3; bd.hide_render = num.hide_render = q <= 1e-3
            r = ease(f, a0 + 22, a0 + 34); lab.scale = (max(1e-3, r),) * 3; lab.hide_render = r <= 1e-3
            d = back(ease(f, a0 - 6, a0 + 6)); dot.scale = (max(1e-3, d),) * 3
            fr.location.z += 0.04 * math.sin((f + k * 20) / 16) * p
            light.data.energy = 3600 * ease(f, a0 - 4, a0 + 8)
        for k, pts in enumerate(arrows):
            for i, o in enumerate(pts):
                p = ease(f, 188 + k * 16 + i * 2, 194 + k * 16 + i * 2); o.scale = (max(1e-3, p),) * 3; o.hide_render = p <= 1e-3
        cx = -5.2 + 5.2 * E2(f, 50, 72) + 5.2 * E2(f, 84, 106)
        k = E2(f, 116, 176)
        cx = cx * (1 - k)
        orb = math.radians(-10 + 20 * E2(f, 20, 116)) * (1 - k) + math.radians(5) * math.sin(max(0, f - 176) / 70.0) * k
        dist = 7.5 + 12.5 * k
        tx = cx + 0.9 * k
        look((tx + 0.6 * (1 - k) + dist * math.sin(orb), -dist * math.cos(orb), 3.0 + 2.2 * k), (tx, 0, 2.1), lens=38 - 6 * k, focus=(cx, 0, 2.2), f=f)
    return at


def scene_podcity(N):
    # ONE continuous shot (Aly 2026-10-27: "البودكاست ده جوا شقة في عمارة و نخرج من العمارة نلاقي نفسنا في المدينة"):
    # inside an apartment studio (host = marble pawn, famous guest = gold queen, mics, panels, ON AIR) -> the camera backs out through
    # the window, out of the building, rises over the night city and turns to the gold tower that climbs floor by floor ("ملايين")
    # and gets its coin. Clip starts at 31.4 s; floors from frame 140 (36.1 s), coin ~222 (38.8 s).
    studio(1.0, (0, 0, 3))
    mesh_obj('Ground', cyl(9, 9, 0.25, 128, (0, 0, -0.125)), pbr('asph', (0.035, 0.037, 0.045), rough=0.22, coat=0.7))
    mesh_obj('Rim', cyl(9.06, 9.06, 0.08, 128, (0, 0, -0.06)), pbr('rim', (1, 0.6, 0.3), emit=1.6))
    st = pbr('street', (1, 0.78, 0.5), emit=1.6)
    for i in range(-4, 5):
        mesh_obj(f'sx{i}', cube(17.5, 0.035, 0.012, (0, i * 2.0 + 1.0, 0.006)), st, smooth=False)
        mesh_obj(f'sy{i}', cube(0.035, 17.5, 0.012, (i * 2.0 + 1.0, 0, 0.006)), st, smooth=False)
    BX, BY, ZR, RH = 4.6, -5.0, 1.6, 0.9          # studio building centre, room floor height, room height
    W2_, D2_ = 1.3, 1.1                            # half width / half depth of the building
    FY = BY - D2_                                  # front face (towards the camera exit, -Y)
    mats = [facade(f'fc{i}', lit=[(1, 0.8, 0.5), (0.85, 0.9, 1), (1, 0.9, 0.7)][i % 3], seed=i) for i in range(3)]
    roof = pbr('roof', (0.12, 0.12, 0.13), rough=0.6)
    blocks = []
    for i in range(120):
        ang = random.uniform(0, 2 * math.pi); r = random.uniform(1.9, 8.3)
        x, y = r * math.cos(ang), r * math.sin(ang)
        if any(math.hypot(x - b[0], y - b[1]) < 0.95 for b in blocks) or (abs(x - BX) < 2.2 and abs(y - BY) < 2.6) or (abs(x - BX) < 1.6 and y < BY): continue
        h = random.uniform(0.6, 2.8) * (1.3 - r / 10)
        wdt = random.choice([0.6, 0.7, 0.8])
        mesh_obj(f'b{i}', cube(wdt, wdt, h, (0, 0, h / 2), bevel=0.012), mats[i % 3], (x, y, 0), smooth=False)
        mesh_obj(f'r{i}', cube(wdt * 0.4, wdt * 0.3, 0.12, (0, 0, h + 0.06)), roof, (x, y, 0), smooth=False)
        blocks.append((x, y))
    # --- the studio building: solid floors below / above the apartment, a front wall with a big window opening
    fm = facade('studiob', lit=(1, 0.82, 0.55), scale=6.0, seed=5)  # bigger windows: we fly right past this facade
    mesh_obj('sb_low', cube(2 * W2_, 2 * D2_, ZR, (0, 0, ZR / 2), bevel=0.01), fm, (BX, BY, 0), smooth=False)
    top_h = 4.2 - (ZR + RH)
    mesh_obj('sb_top', cube(2 * W2_, 2 * D2_, top_h, (0, 0, ZR + RH + top_h / 2), bevel=0.01), fm, (BX, BY, 0), smooth=False)
    wallm = pbr('wallm', (0.07, 0.07, 0.08), rough=0.7)
    mesh_obj('sb_back', cube(2 * W2_, 0.08, RH, (0, D2_ - 0.04, ZR + RH / 2)), wallm, (BX, BY, 0), smooth=False)
    for sx in (-1, 1):
        mesh_obj(f'sb_side{sx}', cube(0.08, 2 * D2_, RH, (sx * (W2_ - 0.04), 0, ZR + RH / 2)), wallm, (BX, BY, 0), smooth=False)
    win_w, win_h, sill = 1.7, 0.62, 0.12
    frame_m = pbr('frame', (0.15, 0.15, 0.16), metal=0.8, rough=0.3)
    side_w = (2 * W2_ - win_w) / 2
    for sx in (-1, 1):
        mesh_obj(f'fw{sx}', cube(side_w, 0.1, RH, (sx * (W2_ - side_w / 2), -D2_ + 0.05, ZR + RH / 2)), fm, (BX, BY, 0), smooth=False)
    mesh_obj('fw_sill', cube(win_w, 0.1, sill, (0, -D2_ + 0.05, ZR + sill / 2)), fm, (BX, BY, 0), smooth=False)
    mesh_obj('fw_lint', cube(win_w, 0.1, RH - sill - win_h, (0, -D2_ + 0.05, ZR + sill + win_h + (RH - sill - win_h) / 2)), fm, (BX, BY, 0), smooth=False)
    for k, x in enumerate([-win_w / 2, -win_w / 6, win_w / 6, win_w / 2]):   # mullions
        mesh_obj(f'mul{k}', cube(0.025, 0.04, win_h, (x, -D2_ + 0.02, ZR + sill + win_h / 2)), frame_m, (BX, BY, 0), smooth=False)
    # --- inside: panels, LED strips, ON AIR, desk, host pawn, gold queen, mics (studio scaled 0.25 to fit the room)
    S_ = 0.25
    panel = pbr('panel', (0.09, 0.09, 0.11), rough=0.85)
    for ix in range(10):
        for iz in range(3):
            mesh_obj(f'ap{ix}_{iz}', cube(0.2, 0.03, 0.24, (0, 0, 0), bevel=0.01), panel, (BX - 1.0 + ix * 0.222, BY + D2_ - 0.1, ZR + 0.18 + iz * 0.26), smooth=False)
    mesh_obj('led1', cube(2.4, 0.015, 0.015, (0, 0, 0)), pbr('lo', (1, 0.55, 0.25), emit=8), (BX, BY + D2_ - 0.12, ZR + RH - 0.06), smooth=False)
    mesh_obj('led2', cube(2.4, 0.015, 0.015, (0, 0, 0)), pbr('lb', (0.4, 0.6, 1), emit=6), (BX, BY + D2_ - 0.12, ZR + 0.03), smooth=False)
    mesh_obj('oab', cube(0.42, 0.03, 0.15, (0, 0, 0), bevel=0.01), pbr('oabm', (0.06, 0.02, 0.02), rough=0.3), (BX - 0.6, BY + D2_ - 0.13, ZR + 0.7), smooth=False)
    onair = text('ON AIR', 0.09, 0.008, pbr('oa', (1, 0.12, 0.08), emit=2.6), (BX - 0.6, BY + D2_ - 0.15, ZR + 0.7))
    mesh_obj('floorin', cube(2 * W2_ - 0.16, 2 * D2_ - 0.12, 0.02, (0, 0, ZR + 0.01)), pbr('fl', (0.16, 0.1, 0.07), rough=0.35, coat=0.6), (BX, BY, 0), smooth=False)
    DY = BY + 0.25
    mesh_obj('desk', cube(0.9, 0.28, 0.025, (0, 0, ZR + 0.2), bevel=0.008), WALNUT(), (BX, DY, 0), smooth=False)
    mesh_obj('deskb', cube(0.75, 0.15, 0.19, (0, 0.04, ZR + 0.1), bevel=0.008), pbr('db', (0.05, 0.05, 0.06), rough=0.4), (BX, DY, 0), smooth=False)
    mesh_obj('host', lathe([(r * 1.55 * S_, z * 1.55 * S_) for r, z in PAWN]), MARBLE('hm'), (BX - 0.26, DY + 0.22, ZR + 0.01))
    gold = GOLD_M('gq')
    queen('guest', gold, (BX + 0.26, DY + 0.22, ZR + 0.01), S_)
    grille = pbr('grille', (0.08, 0.08, 0.09), metal=0.7, rough=0.45)
    for i, (x, a) in enumerate([(-0.15, 0.35), (0.15, -0.35)]):
        mesh_obj(f'mb{i}', lathe([(0, 0), (0.018, 0), (0.018, 0.075), (0.021, 0.08), (0.021, 0.105), (0.018, 0.11), (0, 0.115)], 24), grille,
                 (BX + x, DY + 0.1, ZR + 0.31), (0.7, 0, a))
    room_l = area('roomL', (BX, BY - 0.2, ZR + RH - 0.05), (BX, BY + 0.2, ZR), 60, 1.2, (1, 0.9, 0.78))
    q_spot = spot('qs', (BX + 0.26, BY - 0.6, ZR + RH - 0.05), (BX + 0.26, DY + 0.22, ZR + 0.3), 120, 22, (1, 0.86, 0.6), 0.3)
    spot('hs', (BX - 0.26, BY - 0.6, ZR + RH - 0.05), (BX - 0.26, DY + 0.22, ZR + 0.25), 50, 24, (0.75, 0.82, 1), 0.35)
    # --- the gold tower (centre) rises later, coin + small coins as in the tower scene
    band = pbr('band', (1, 0.88, 0.62), emit=3.5); fin = pbr('fin', (0.95, 0.72, 0.35), metal=1.0, rough=0.25); tg = GOLD_M('tgold')
    floors = []
    for k in range(14):
        wd = 1.5 - k * 0.045
        obs = [mesh_obj(f'f{k}', cube(wd, wd, 0.62, (0, 0, 0.31), bevel=0.02), tg, (0, 0, k * 0.66), smooth=False),
               mesh_obj(f'w{k}', cube(wd + 0.01, wd + 0.01, 0.05, (0, 0, 0.6)), band, (0, 0, k * 0.66), smooth=False)]
        obs += [mesh_obj(f'fn{k}_{j}', cube(0.035, 0.035, 0.62, (0, 0, 0.31)), fin, ((wd / 2 + 0.01) * sx, (wd / 2 + 0.01) * sy, k * 0.66), smooth=False)
                for j, (sx, sy) in enumerate([(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1.0), (0, -1.0), (1.0, 0), (-1.0, 0)])]
        floors.append(obs)
    spire = mesh_obj('spire', lathe([(0.2, 0), (0.12, 0.3), (0.04, 1.2), (0, 1.45)], 32), tg, (0, 0, 14 * 0.66))
    coin = mesh_obj('coin', coin_bm(), pbr('coinm', (1, 0.79, 0.4), metal=1.0, rough=0.12), (0, 0, 0))
    dol = text('$', 1.2, 0.03, pbr('dol', (1, 0.79, 0.4), metal=1.0, rough=0.22), (0, 0, 0))
    dol.parent = coin; dol.location = (0, 0, 0.055); dol.rotation_euler = (0, 0, 0)
    TOP = 14 * 0.66 + 1.4
    ups = [spot(f'up{i}', (2.2 * math.cos(a), 2.2 * math.sin(a), 0.2), (0, 0, 6), 0, 20, (1, 0.8, 0.5), 0.3) for i, a in enumerate([0.6, 2.7, 4.8])]
    coin_l = bpy.data.objects.new('coinL', bpy.data.lights.new('coinL', 'POINT')); coin_l.data.color = (1, 0.82, 0.5); sc.collection.objects.link(coin_l)
    cm = pbr('smallc', (1, 0.79, 0.4), metal=1.0, rough=0.18)
    small = [mesh_obj(f'sc{i}', coin_bm(0.22, 0.04), cm, (0, 0, -5)) for i in range(16)]
    F0, CN = 140, 222
    QT = (BX + 0.26, DY + 0.22, ZR + 0.32)       # the queen (focus inside)
    cam.data.shift_x = -0.17

    def at(f):
        for k, obs in enumerate(floors):
            p = back(ease(f, F0 + k * 5, F0 + 9 + k * 5))
            for o in obs: o.scale = (1, 1, max(0.001, p)); o.hide_render = p <= 0.001
        p = back(ease(f, F0 + 14 * 5, F0 + 11 + 14 * 5)); spire.scale = (1, 1, max(0.001, p)); spire.hide_render = p <= 0.001
        for L in ups: L.data.energy = 3000 * ease(f, F0 - 2, F0 + 20)
        c = back(ease(f, CN, CN + 22), 2.2)
        coin.location = (0, 0, TOP + 1.4 * c + 0.12 * math.sin(f / 9)); coin.scale = (c + 1e-3,) * 3
        coin.rotation_euler = (math.pi / 2, 0, f / 12); coin.hide_render = c <= 0.001
        coin_l.location = (0, -1.2, TOP + 1.4); coin_l.data.energy = 700 * c
        for i, o in enumerate(small):
            t = (f - CN - 10 - i * 4) / 60.0
            if t <= 0: o.hide_render = True; continue
            o.hide_render = False
            a = i * 2.4 + t * 5; r = 2.4 - 0.6 * min(1, t)
            o.location = (r * math.cos(a), r * math.sin(a), 0.5 + t * 9); o.rotation_euler = (t * 7, t * 4, a)
        # camera: 1) inside, slow push towards the guest  2) backs out through the window  3) rises over the city, turns to the tower
        #         4) follows the tower up to the coin
        k1 = E2(f, 0, 64)
        inside = (BX - 0.12 + 0.05 * k1, FY + 0.45 + 0.12 * k1, ZR + 0.42)
        k2 = E2(f, 64, 118)
        outside = (BX - 0.05, FY - 2.6, ZR + 0.55)
        k3 = E2(f, 118, 205)
        over = (BX + 3.6, BY - 9.5, 5.6)
        top = min(TOP, 0.66 * max(0.0, (f - F0) / 5.0))
        k4 = E2(f, 205, N)
        p1 = [lerp_(k2, a_, b_) for a_, b_ in zip(inside, outside)]
        p2 = [lerp_(k3, a_, b_) for a_, b_ in zip(p1, over)]
        p3 = [lerp_(k4, a_, b_) for a_, b_ in zip(p2, (BX + 5.0, BY - 11.5, 4.2 + 0.4 * top))]
        room_t = (BX + 0.05, DY + 0.2, ZR + 0.3)
        city_t = (0, 0, 1.2 + 0.55 * top)
        tgt = [lerp_(k3, a_, b_) for a_, b_ in zip(room_t, city_t)]
        lens = lerp_(k2, 26, 30) + 4 * k3
        foc = QT if k3 < 0.5 else (0, 0, max(1.0, tgt[2]))
        look(p3, tgt, lens=lens, focus=foc, f=f, shake=0.012 if k2 < 0.5 else 0.02)
        cam.data.shift_x = lerp_(k3, 0.0, -0.17)   # inside the room: centred; over the city: subject right of Aly's frame
    return at


SCENES = {'podcity': scene_podcity, 'podcast': scene_podcast, 'tower': scene_tower, 'road': scene_road, 'crowd': scene_crowd, 'three': scene_three}
at = SCENES[A.scene](A.frames)
os.makedirs(A.out, exist_ok=True)
frames = [A.still] if A.still >= 0 else range(A.start, A.frames)
# the animation lives in at(f); as a frame handler it also runs on the motion-blur sub-frames, so the blur is real
bpy.app.handlers.frame_change_pre.append(lambda scn, *a: at(scn.frame_current + scn.frame_subframe))
sc.frame_start, sc.frame_end = 0, max(1, A.frames)
for f in frames:
    sc.frame_set(f)
    sc.render.filepath = os.path.join(A.out, f'{f:04d}.png')
    bpy.ops.render.render(write_still=True)
    print('frame', f, flush=True)
