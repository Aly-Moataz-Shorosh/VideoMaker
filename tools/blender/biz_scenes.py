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


# ---------------------------------------------------------------- scenes
def scene_tower(N):
    lights(1.0, (0, 0, 3)); ground(9)
    pal = [BLUE, OLIVE, PAPER, BLUE, OLIVE]
    mats = [windows(f'c{i}', c, lit=[MUSTARD, PAPER, ORANGE][i % 3], strength=1.4) for i, c in enumerate(pal)]
    # glowing streets on the ground (a little city map)
    st_o, st_b = mat('sto', ORANGE, emit=3.0), mat('stb', BLUE, emit=3.0)
    for i in range(-4, 5):
        mesh_obj(f'sx{i}', cube(17.5, 0.06, 0.02, (0, i * 2.0 + 1.0, 0.01)), st_o if i % 2 else st_b, smooth=False)
        mesh_obj(f'sy{i}', cube(0.06, 17.5, 0.02, (i * 2.0 + 1.0, 0, 0.01)), st_b if i % 2 else st_o, smooth=False)
    blocks = []
    for i in range(90):
        ang = random.uniform(0, 2 * math.pi); r = random.uniform(1.9, 8.2)
        x, y = r * math.cos(ang), r * math.sin(ang)
        if any(math.hypot(x - b[0], y - b[1]) < 1.05 for b in blocks): continue
        h = random.uniform(0.6, 2.4) * (1.25 - r / 10)
        ob = mesh_obj(f'b{i}', cube(0.8, 0.8, 1, (0, 0, 0.5), bevel=0.03), mats[i % len(mats)], (x, y, 0), smooth=False)
        blocks.append((x, y, h, ob, random.uniform(0, 26)))
    gold = mat('gold', GOLD, metal=1.0, rough=0.18, coat=0.9)
    win = mat('win', (1, 0.86, 0.55), emit=4.0)
    floors = []
    for k in range(14):
        fl = mesh_obj(f'f{k}', cube(1.5 - k * 0.04, 1.5 - k * 0.04, 0.62, (0, 0, 0.31), bevel=0.04), gold, (0, 0, k * 0.66), smooth=False)
        band = mesh_obj(f'w{k}', cube(1.52 - k * 0.04, 1.52 - k * 0.04, 0.12, (0, 0, 0.36)), win, (0, 0, k * 0.66), smooth=False)
        floors.append((fl, band))
    spire = mesh_obj('spire', cyl(0.18, 0.0, 1.4, 16, (0, 0, 0.7)), gold, (0, 0, 14 * 0.66))
    coin = mesh_obj('coin', cyl(0.95, 0.95, 0.18, 64), mat('coinm', GOLD, metal=1.0, rough=0.15, emit=0.5), (0, 0, 0))
    dol = text('$', 1.3, 0.05, mat('dol', (0.5, 0.28, 0.04), metal=0.6, rough=0.3), (0, 0, 0))
    dol.parent = coin; dol.location = (0, 0, 0.1); dol.rotation_euler = (0, 0, 0)
    TOP = 14 * 0.66 + 1.4
    # up-lights washing the gold tower from its base + a hot light at the coin
    ups = [spot(f'up{i}', (2.2 * math.cos(a), 2.2 * math.sin(a), 0.2), (0, 0, 6), 0, 22, (1, 0.75, 0.4)) for i, a in enumerate([0.6, 2.7, 4.8])]
    coin_l = bpy.data.objects.new('coinL', bpy.data.lights.new('coinL', 'POINT')); coin_l.data.color = (1, 0.8, 0.45); sc.collection.objects.link(coin_l)
    # small coins spiralling up around the tower at the end
    cm = mat('smallc', GOLD, metal=1.0, rough=0.2, emit=0.3)
    small = [mesh_obj(f'sc{i}', cyl(0.22, 0.22, 0.05, 32), cm, (0, 0, -5)) for i in range(16)]

    def at(f):
        for x, y, h, ob, d in blocks:
            k = back(ease(f, 2 + d, 18 + d)); ob.scale = (1, 1, max(0.001, h * k))
        for k, (fl, band) in enumerate(floors):
            p = back(ease(f, 60 + k * 6, 70 + k * 6))
            for o in (fl, band): o.scale = (1, 1, max(0.001, p)); o.hide_render = p <= 0.001
        p = back(ease(f, 60 + 14 * 6, 72 + 14 * 6)); spire.scale = (1, 1, max(0.001, p)); spire.hide_render = p <= 0.001
        for L in ups: L.data.energy = 2600 * ease(f, 58, 80)
        c = back(ease(f, 150, 172), 2.2)
        coin.location = (0, 0, TOP + 1.4 * c + 0.12 * math.sin(f / 9)); coin.scale = (c + 1e-3,) * 3
        coin.rotation_euler = (math.pi / 2, 0, f / 12); coin.hide_render = c <= 0.001
        coin_l.location = (0, -1.2, TOP + 1.4); coin_l.data.energy = 600 * c
        for i, o in enumerate(small):
            t = (f - 160 - i * 4) / 60.0
            if t <= 0: o.hide_render = True; continue
            o.hide_render = False
            a = i * 2.4 + t * 5; r = 2.4 - 0.6 * min(1, t)
            o.location = (r * math.cos(a), r * math.sin(a), 0.5 + t * 9); o.rotation_euler = (t * 7, t * 4, a)
        # camera: 1) overhead over the city map, swooping down while orbiting  2) street level, low angle, wide lens:
        # cranes up with the floors (the tower towers over us)  3) pulls back to the coin, lens back to normal
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


def lerp_(k, a, b): return a + (b - a) * k


def scene_road(N):
    lights(1.4, (7, 2, 1.5))
    asph = mat('asph', (0.09, 0.10, 0.14), rough=0.35, coat=0.6)  # wet-looking night asphalt (reflects the lamps)
    mesh_obj('road', cube(30, 3.0, 0.12, (7, 0, -0.06)), asph, smooth=False)
    mesh_obj('pave', cube(30, 6.0, 0.2, (7, 4.5, -0.1)), mat('pave', (0.16, 0.17, 0.22), rough=0.6), smooth=False)
    dash = mat('dash', MUSTARD, emit=1.6)
    for i in range(26): mesh_obj(f'd{i}', cube(0.7, 0.12, 0.03, (0, 0, 0.015)), dash, (-6 + i * 1.2, 0, 0), smooth=False)
    side = mat('side', NAVY, rough=0.4)
    mesh_obj('kerb', cube(30, 0.25, 0.25, (7, 1.6, 0.12)), side, smooth=False)
    # street lamps: pole + glowing head + a real point light each (pools of warm light on the wet road)
    pole_m, bulb_m = mat('pole', (0.2, 0.22, 0.27), metal=0.8, rough=0.3), mat('bulb', (1, 0.82, 0.5), emit=12)
    for i in range(8):
        x = -3 + i * 3.4
        mesh_obj(f'lp{i}', cyl(0.05, 0.05, 2.6, 12, (0, 0, 1.3)), pole_m, (x, 1.75, 0))
        mesh_obj(f'lh{i}', sphere(0.14, 16, 10), bulb_m, (x, 1.45, 2.55))
        P = bpy.data.objects.new(f'pl{i}', bpy.data.lights.new(f'pl{i}', 'POINT')); P.data.energy = 140; P.data.color = (1, 0.78, 0.45)
        P.location = (x, 1.3, 2.4); sc.collection.objects.link(P)
    # stop 1: kiosk with a striped awning + a small rocket next to it
    k_body = mesh_obj('kiosk', cube(1.6, 1.2, 1.3, (0, 0, 0.65), bevel=0.04), windows('kb', PAPER, lit=MUSTARD, scale=2.0, strength=1.2), (0, 2.6, 0), smooth=False)
    stripes = [mesh_obj(f'aw{i}', cube(0.32, 1.45, 0.08, (0, 0, 0)), mat(f'awm{i}', ORANGE if i % 2 else PAPER), (-0.64 + i * 0.32, 2.3, 1.42),
                        (math.radians(-18), 0, 0), smooth=False) for i in range(5)]
    rocket = []
    rb = mat('rb', PAPER, rough=0.25, coat=0.8); rr = mat('rr', ORANGE, rough=0.3)
    RX, RY = 1.6, 2.3
    rocket.append(mesh_obj('rbody', cyl(0.22, 0.22, 1.0, 32, (0, 0, 0.5)), rb, (RX, RY, 0)))
    rocket.append(mesh_obj('rnose', cyl(0.22, 0.0, 0.45, 32, (0, 0, 1.22)), rr, (RX, RY, 0)))
    rocket.append(mesh_obj('rwin', sphere(0.09, 16, 10, (0, -0.2, 0.68)), mat('rw', BLUE, emit=2.0), (RX, RY, 0)))
    for i in range(3):
        an = i * 2 * math.pi / 3
        fin = cube(0.06, 0.32, 0.4, (0.25 * math.cos(an), 0.25 * math.sin(an), 0.2)); rocket.append(mesh_obj(f'fin{i}', fin, rr, (RX, RY, 0), (0, 0, an)))
    flame = mesh_obj('flame', cyl(0.18, 0.0, 0.7, 24, (0, 0, -0.35)), mat('fl', MUSTARD, emit=9), (RX, RY, 0), (math.pi, 0, 0))
    fl_light = bpy.data.objects.new('flL', bpy.data.lights.new('flL', 'POINT')); fl_light.data.color = (1, 0.6, 0.25); sc.collection.objects.link(fl_light)
    smoke_m = mat('smoke', (0.8, 0.8, 0.82), rough=0.9, coat=0)
    puffs = [mesh_obj(f'pf{i}', sphere(0.3, 16, 10), smoke_m, (RX, RY, -3)) for i in range(14)]
    # stop 2: a 3-floor shop that grows with a bar chart behind it (the level), then its shutter rolls down and it greys
    shop_m = windows('shop', BLUE, lit=MUSTARD, scale=2.6, strength=1.6)
    shop = mesh_obj('shop', cube(2.2, 1.6, 2.4, (0, 0, 1.2), bevel=0.05), shop_m, (7, 2.8, 0), smooth=False)
    sign_m = mat('sg', MUSTARD, emit=2.5)
    sign = mesh_obj('sign', cube(1.8, 0.1, 0.35, (0, 0, 0)), sign_m, (7, 1.95, 2.1), smooth=False)
    shutter = mesh_obj('shutter', cube(1.6, 0.06, 1.0, (0, 0, -0.5)), mat('sh', (0.55, 0.57, 0.62), metal=0.8, rough=0.3), (7, 1.94, 1.75), smooth=False)
    bars = [mesh_obj(f'bar{i}', cube(0.5, 0.5, 1.0, (0, 0, 0.5), bevel=0.03), mat(f'barm{i}', [OLIVE, MUSTARD, ORANGE, OLIVE][i], emit=0.3), (5.9 + i * 0.75, 4.6, 0), smooth=False)
            for i in range(4)]
    bh = [1.0, 1.9, 2.9, 3.6]
    # stop 3: new building, glowing door (its light spills on the road), arrow jumping from stop 2
    new = mesh_obj('new', cube(2.4, 1.8, 3.0, (0, 0, 1.5), bevel=0.05), windows('nw', OLIVE, lit=PAPER, scale=2.4, strength=1.8), (14, 2.9, 0), smooth=False)
    door = mesh_obj('door', cube(0.8, 0.08, 1.3, (0, 0, 0.65)), mat('dr', MUSTARD, emit=8), (14, 1.98, 0), smooth=False)
    door_l = area('doorL', (14, 1.6, 0.9), (14, -1, 0), 0, 1.2, (1, 0.8, 0.45))
    arrow_m = mat('arr', ORANGE, emit=3.0)
    arc = []
    for i in range(16):
        t = i / 15; x = 8.3 + 4.4 * t; z = 3.0 + 1.8 * math.sin(math.pi * t)
        arc.append(mesh_obj(f'a{i}', sphere(0.11, 12, 8), arrow_m, (x, 2.4, z)))
    head = mesh_obj('ahead', cyl(0.28, 0.0, 0.5, 24), arrow_m, (12.75, 2.4, 3.0), (0, math.radians(140), 0))
    flag = [mesh_obj('pole', cyl(0.04, 0.04, 2.0, 12, (0, 0, 1.0)), mat('pl', PAPER), (-1.6, 1.9, 0)),
            mesh_obj('flag', cube(0.7, 0.04, 0.45, (0.37, 0, 1.75)), mat('flg', ORANGE, emit=0.8), (-1.6, 1.9, 0), smooth=False)]

    def pop(obs, f, a, b):
        p = back(ease(f, a, b))
        for o in obs:
            o.scale = (max(1e-3, p),) * 3; o.hide_render = p <= 1e-3
        return p

    def at(f):
        pop(flag, f, 0, 14); pop([k_body] + stripes, f, 8, 24)
        up = max(0, f - 44) ** 1.8 * 0.0035
        for o in rocket: o.location.z = up
        flame.location.z = up; flame.scale = (1, 1, 0.6 + 0.4 * math.sin(f * 1.7)) if f > 36 else (1e-3,) * 3
        flame.hide_render = f <= 36
        fl_light.location = (RX, RY - 0.4, up - 0.2); fl_light.data.energy = 900 * ease(f, 36, 44) * (0.85 + 0.15 * math.sin(f * 2.3))
        for i, o in enumerate(puffs):  # smoke: puffs born at the pad, grow, drift sideways and sink away
            t = (f - 38 - i * 3) / 40.0
            if t <= 0 or t >= 1: o.hide_render = True; continue
            o.hide_render = False
            o.location = (RX + (i % 2 * 2 - 1) * (0.3 + 1.6 * t) * (0.6 + 0.4 * (i % 3)), RY + 0.2 * math.sin(i), 0.15 + 0.5 * t)
            o.scale = (0.4 + 2.2 * t * (1 - 0.4 * t),) * 3
        pop(rocket, f, 18, 30)
        g = back(ease(f, 112, 134)); shop.scale = (1, 1, max(1e-3, g)); shop.hide_render = g <= 1e-3
        pop([sign], f, 128, 140)
        for i, b in enumerate(bars):
            p = back(ease(f, 122 + i * 7, 136 + i * 7)); b.scale = (1, 1, max(1e-3, bh[i] * p)); b.hide_render = p <= 1e-3
        c = ease(f, 198, 220)
        shutter.scale = (1, 1, max(1e-3, 1.6 * c)); shutter.hide_render = c <= 1e-3
        grey = ease(f, 208, 230)
        bsdf(shop_m).inputs['Emission Strength'].default_value = 1.6 * (1 - grey)
        bsdf(sign_m).inputs['Emission Strength'].default_value = 2.5 * (1 - grey) * (1 if f < 208 or (f // 3) % 4 else 0.2)  # the sign flickers off
        col = [BLUE[i] * (1 - grey) + 0.3 * grey for i in range(3)]
        bsdf(shop_m).inputs['Base Color'].default_value = (*lin(col), 1)
        for i, o in enumerate(arc):
            p = ease(f, 212 + i * 2, 218 + i * 2); o.scale = (max(1e-3, p),) * 3; o.hide_render = p <= 1e-3
        pop([head], f, 244, 254)
        n = back(ease(f, 226, 250)); new.scale = (1, 1, max(1e-3, n)); new.hide_render = n <= 1e-3
        pop([door], f, 246, 258); door_l.data.energy = 900 * ease(f, 248, 260)
        # camera: low tracking shot along the road (stop 1 -> 2 -> 3), focus pulls to each stop, a crane-up reveal at the end
        x = 0.8 + 6.2 * E2(f, 60, 125) + 7.0 * E2(f, 212, 252)
        k = E2(f, 254, N)
        tx = x + 0.6 - 7.0 * k
        look((x - 2.6 - 3.0 * k, -5.6 - 7 * k, 1.4 + 6.0 * k), (tx, 2.4, 1.3 + 0.6 * k), lens=28 + 6 * k, focus=(x + 0.6, 2.6, 1.3), f=f)
    return at


def scene_crowd(N):
    lights(0.7, (0, 0, 1))
    ground(11)
    bm = cyl(0.2, 0.12, 0.42, 16, (0, 0, 0.21)); bm2 = sphere(0.14, 14, 10, (0, 0, 0.56))
    me = bpy.data.meshes.new('pawn'); bm.to_mesh(me); bm.free()
    me2 = bpy.data.meshes.new('pawn2'); bm2.to_mesh(me2); bm2.free()
    bmm = bmesh.new(); bmm.from_mesh(me); bmm.from_mesh(me2); bmm.to_mesh(me); bmm.free()
    for poly in me.polygons: poly.use_smooth = True
    pm = mat('pawn', (1, 1, 1), rough=0.4, obj_color=True, emit=0.0); bsdf(pm).inputs['Emission Strength'].default_value = 0.35
    me.materials.append(pm)
    pal = [ORANGE, BLUE, OLIVE, MUSTARD, PAPER]
    pawns = []
    for i in range(20):
        for j in range(20):
            if (i, j) == (10, 10): continue
            x, y = (i - 9.5) * 0.85 + random.uniform(-0.12, 0.12), (j - 9.5) * 0.85 + random.uniform(-0.12, 0.12)
            ob = link(f'p{i}_{j}', me, (x, y, 0)); ob.rotation_euler = (0, 0, random.uniform(0, 6.3))
            ob.color = (0.12, 0.13, 0.16, 1)
            pawns.append((ob, math.hypot(x, y), pal[(i * 7 + j * 3) % 5]))
    gold = mat('goldp', GOLD, metal=1.0, rough=0.16, emit=0.6)
    gp = link('gold', me.copy(), (0.43, 0.43, 0)); gp.data.materials.clear(); gp.data.materials.append(gold); gp.scale = (1.6,) * 3
    ped = mesh_obj('ped', cyl(0.42, 0.5, 1.0, 48, (0, 0, 0.5)), mat('pedm', PAPER, rough=0.3, coat=0.7), (0.43, 0.43, 0))
    halo = mesh_obj('halo', cyl(0.75, 0.75, 0.03, 64), mat('halo', GOLD, emit=6), (0.43, 0.43, 0))
    sp = spot('Spot', (0.43, 0.43, 11), (0.43, 0.43, 0), 4200, 14, (1, 0.85, 0.5), 0.25)
    G = (0.43, 0.43)

    def at(f):
        h = 3.2 * back(ease(f, 4, 36), 1.2)
        ped.scale = (1, 1, max(1e-3, h)); gp.location.z = h; halo.location.z = h + 0.01
        gp.rotation_euler = (0, 0, f / 22)
        dim = ease(f, 200, 250)
        bsdf(gold).inputs['Emission Strength'].default_value = 0.6 * (1 - 0.6 * dim)
        sp.data.energy = 4200 * (1 - 0.75 * dim)
        for ob, r, c in pawns:  # the many light up in a wave from the centre outwards
            k = ease(f, 190 + r * 6, 205 + r * 6)
            ob.color = (*[0.12 + (lin(c)[i] - 0.12) * k for i in range(3)], 1)
        top = (G[0], G[1], h + 0.6)
        # 1) close on the golden one  2) DOLLY ZOOM (vertigo): camera backs off while the lens zooms in -> the golden one stays the
        # same size, the crowd behind swells  3) crane up high over everyone as they light up
        k = E2(f, 36, 120)
        dist = 3.0 + 13.0 * k
        lens = 22 * dist / 3.0  # keep size: focal length grows with distance
        el = math.radians(8 + 4 * k)
        k3 = E2(f, 140, 290)
        dist = dist + 2.0 * k3
        lens = lens * (1 - k3) + 42 * k3
        el = el + math.radians(48) * k3
        az = math.radians(-62 + 30 * k3)
        tgt = (G[0] * (1 - k3), G[1] * (1 - k3), top[2] * (1 - k3) + 0.3 * k3)
        look((tgt[0] + dist * math.cos(el) * math.cos(az), tgt[1] + dist * math.cos(el) * math.sin(az), tgt[2] + dist * math.sin(el)), tgt, lens=lens, focus=top, f=f, shake=0.015)
    return at


def scene_three(N):
    lights(0.8, (0, 0, 2))
    floor = mat('floor', NAVY, rough=0.18, coat=0.9)
    mesh_obj('floor', cube(26, 10, 0.2, (0, 2, -0.1)), floor, smooth=False)
    line = mesh_obj('line', cube(1, 0.12, 0.04, (0.5, 0, 0.02)), mat('ln', MUSTARD, emit=4), (-8, -1.6, 0), smooth=False)
    T = A.tex or '.'
    cards = []
    names = [('courzerve.jpg', 'Courzerve', BLUE), ('kikos.jpg', "Kiko's Snacks", ORANGE), ('fpl.jpg', 'FPL Champ', OLIVE)]
    for k, (img, nm, col) in enumerate(names):
        x = -5.2 + k * 5.2
        frame = mesh_obj(f'cf{k}', cube(3.3, 0.22, 3.3, (0, 0.12, 0), bevel=0.06), mat(f'cfm{k}', PAPER, rough=0.4, coat=0.6), (x, 0, 2.2), smooth=False)
        pic = mesh_obj(f'cp{k}', plane_uv(3.0, 3.0), mat(f'cpm{k}', (1, 1, 1), tex=os.path.join(T, img)), (x, -0.005, 2.2), smooth=False)
        pic.parent = frame; pic.location = (0, -0.005, 0)
        badge = mesh_obj(f'bd{k}', cyl(0.48, 0.48, 0.16, 48), mat(f'bdm{k}', col, rough=0.3, emit=0.4), (x - 1.55, -0.25, 3.75), (math.pi / 2, 0, 0))
        num = text(str(k + 1), 0.7, 0.04, mat(f'nm{k}', PAPER, emit=0.8), (x - 1.55, -0.36, 3.73))
        lab = text(nm, 0.42, 0.03, mat(f'lb{k}', PAPER, emit=0.6), (x, -0.3, 0.25))
        dot = mesh_obj(f'dot{k}', cyl(0.18, 0.18, 0.06, 32), mat(f'dt{k}', col, emit=4), (x, -1.6, 0.05))
        light = spot(f'cs{k}', (x + 0.4, -4.5, 7.5), (x, 0, 1.6), 0, 26, (1, 0.9, 0.75), 0.35)  # each card gets its own light pool
        cards.append((frame, badge, num, lab, dot, x, light))
    arr_m = mat('arr', ORANGE, emit=3.0)
    arrows = []
    for k in range(2):
        x0 = -5.2 + k * 5.2 + 1.9; pts = []
        for i in range(9):
            t = i / 8; pts.append(mesh_obj(f'ar{k}{i}', sphere(0.08, 10, 8), arr_m, (x0 + 1.4 * t, -0.4, 3.0 + 0.9 * math.sin(math.pi * t))))
        arrows.append(pts)

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
            fr.location.z += 0.06 * math.sin((f + k * 20) / 16) * p
            light.data.energy = 3200 * ease(f, a0 - 4, a0 + 8)
        for k, pts in enumerate(arrows):
            for i, o in enumerate(pts):
                p = ease(f, 188 + k * 16 + i * 2, 194 + k * 16 + i * 2); o.scale = (max(1e-3, p),) * 3; o.hide_render = p <= 1e-3
        # camera: arcs around each new card (focus pulled to it), then a wide pull back to all three
        cx = -5.2 + 5.2 * E2(f, 50, 72) + 5.2 * E2(f, 84, 106)
        k = E2(f, 116, 176)
        cx = cx * (1 - k)
        orb = math.radians(-10 + 20 * E2(f, 20, 116)) * (1 - k) + math.radians(12) * math.sin(max(0, f - 176) / 70.0) * k  # slow arc after the pull back
        dist = 7.5 + 6.0 * k
        look((cx + 0.6 + dist * math.sin(orb) - 0.8 * k, -dist * math.cos(orb), 3.0 + 1.8 * k), (cx + 0.3 * k, 0, 2.1), lens=38 - 2 * k, focus=(cx, 0, 2.2), f=f)
    return at


SCENES = {'tower': scene_tower, 'road': scene_road, 'crowd': scene_crowd, 'three': scene_three}
at = SCENES[A.scene](A.frames)
os.makedirs(A.out, exist_ok=True)
frames = [A.still] if A.still >= 0 else range(A.frames)
# the animation lives in at(f); as a frame handler it also runs on the motion-blur sub-frames, so the blur is real
bpy.app.handlers.frame_change_pre.append(lambda scn, *a: at(scn.frame_current + scn.frame_subframe))
sc.frame_start, sc.frame_end = 0, max(1, A.frames)
for f in frames:
    sc.frame_set(f)
    sc.render.filepath = os.path.join(A.out, f'{f:04d}.png')
    bpy.ops.render.render(write_still=True)
    print('frame', f, flush=True)
