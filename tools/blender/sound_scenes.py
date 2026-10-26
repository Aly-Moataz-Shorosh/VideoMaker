# Blender 5.2 version of the audio-course 3D concept scenes (Aly 2026-10-26: "امثلة ب blender" next to the three.js ones).
# Same ideas as motion-library/src/course/sound3d.tsx: wave ribbon, stone in water, air molecules (+ struck metal bar), mic diaphragm,
# speaker cone. Built from code (bpy data API, no operators), animated by setting every frame, EEVEE, transparent film -> PNG frames.
#   blender -b --factory-startup -P sound_scenes.py -- --scene mic --frames 300 --out E:/.../frames/mic [--still 120]
import bpy, bmesh, math, sys, os, argparse
import numpy as np

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument('--scene', required=True)
ap.add_argument('--frames', type=int, default=90)
ap.add_argument('--out', required=True)
ap.add_argument('--still', type=int, default=-1)  # render only this frame (check)
ap.add_argument('--bar', action='store_true')
ap.add_argument('--res', type=int, nargs=2, default=[1080, 1920])  # whole phone screen (Aly 2026-10-26); the first clips (short 07) were 1040 1000
A = ap.parse_args(a)

TEAL, VIOLET, GOLD = (0.18, 0.90, 0.71), (0.55, 0.36, 0.96), (0.97, 0.75, 0.25)
lin = lambda c: tuple(x ** 2.2 for x in c)  # sRGB-ish -> linear

sc = bpy.context.scene
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
sc.render.engine = 'BLENDER_EEVEE'
sc.render.resolution_x, sc.render.resolution_y = A.res
sc.render.film_transparent = True
sc.render.fps = 30
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGBA'
try: sc.eevee.taa_render_samples = 32
except Exception: pass
try: sc.eevee.use_raytracing = True
except Exception: pass
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - Punchy'
except TypeError: pass
w = bpy.data.worlds.new('W'); sc.world = w
bg = next(n for n in w.node_tree.nodes if n.type == 'BACKGROUND')
bg.inputs['Color'].default_value = (0.02, 0.04, 0.09, 1); bg.inputs['Strength'].default_value = 0.6


def mat(name, color, metal=0.0, rough=0.35, emit=0.0, coat=0.6, obj_color=False, alpha=1.0):
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
    if obj_color:  # per-object colour (ob.color) drives base + a little glow: molecules light up where the air is dense
        oi = nt.nodes.new('ShaderNodeObjectInfo')
        nt.links.new(oi.outputs['Color'], p.inputs['Base Color'])
        nt.links.new(oi.outputs['Color'], p.inputs['Emission Color'])
        p.inputs['Emission Strength'].default_value = 0.35
    if alpha < 1:
        p.inputs['Alpha'].default_value = alpha
    return m


def mesh_obj(name, bm, m, loc=(0, 0, 0), rot=(0, 0, 0), smooth=True):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    if smooth:
        for poly in me.polygons: poly.use_smooth = True
    ob = bpy.data.objects.new(name, me); ob.data.materials.append(m)
    ob.location, ob.rotation_euler = loc, rot
    sc.collection.objects.link(ob)
    return ob


def sphere(r=1.0, seg=24, ring=16):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=ring, radius=r); return bm


def cyl(r1, r2, depth, seg=48, cap=True):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=cap, cap_tris=False, segments=seg, radius1=r1, radius2=r2, depth=depth); return bm


def cube(x, y, z):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(x, y, z), verts=bm.verts); return bm


def torus(R, r, seg=48, ring=12):
    bm = bmesh.new()
    vs = []
    for i in range(seg):
        a1 = 2 * math.pi * i / seg
        row = []
        for j in range(ring):
            a2 = 2 * math.pi * j / ring
            row.append(bm.verts.new(((R + r * math.cos(a2)) * math.cos(a1), (R + r * math.cos(a2)) * math.sin(a1), r * math.sin(a2))))
        vs.append(row)
    for i in range(seg):
        for j in range(ring):
            bm.faces.new((vs[i][j], vs[(i + 1) % seg][j], vs[(i + 1) % seg][(j + 1) % ring], vs[i][(j + 1) % ring]))
    return bm


# camera + lights (Blender is Z-up: the scene's "up" = +Z, depth = +Y away from camera)
cam = bpy.data.objects.new('Cam', bpy.data.cameras.new('Cam')); sc.collection.objects.link(cam); sc.camera = cam
cam.data.sensor_fit = 'VERTICAL'; cam.data.angle = math.radians(38)
if A.res[1] > A.res[0]:  # portrait: keep the same width of the scene as the 1040x1000 clips, the extra height = room above/below
    cam.data.sensor_fit = 'HORIZONTAL'; cam.data.angle = math.radians(39)


def look(cam_loc, target=(0, 0, 0)):
    cam.location = cam_loc
    d = np.array(target) - np.array(cam_loc)
    cam.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi / 2)


for nm, loc, e, col in [('Key', (6, -8, 9), 900, (1, 0.97, 0.92)), ('Fill', (-8, -4, 2), 300, (0.62, 0.78, 1)), ('Rim', (0, 9, 6), 600, (0.6, 0.5, 1))]:
    L = bpy.data.objects.new(nm, bpy.data.lights.new(nm, 'AREA')); L.data.energy = e; L.data.size = 6; L.data.color = col
    L.location = loc; sc.collection.objects.link(L)
    d = -np.array(loc, float); L.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi / 2)


class Air:
    """Block of air molecules; longitudinal wave along x (each one moves back and forth: dense / thin bands)."""
    def __init__(self, nx=22, ny=4, nz=6, x0=-4.6, x1=4.6, origin=(0, 0, 0), k=2.2, w=5.0):
        self.k, self.w = k, w
        self.m = mat('Mol', (1, 1, 1), rough=0.3, coat=0.8, obj_color=True)
        me = bpy.data.meshes.new('mol'); b = sphere(0.14, 14, 10); b.to_mesh(me); b.free()
        for p in me.polygons: p.use_smooth = True
        me.materials.append(self.m)
        self.obs = []
        for i in range(nx):
            for j in range(ny):
                for l in range(nz):
                    bx = x0 + i / (nx - 1) * (x1 - x0)
                    ob = bpy.data.objects.new('m', me); sc.collection.objects.link(ob)
                    self.obs.append((ob, bx, origin[1] + (j - (ny - 1) / 2) * 0.55, origin[2] + (l - (nz - 1) / 2) * 0.55))
        self.ox = origin[0]

    def set(self, t, amp):
        for ob, bx, by, bz in self.obs:
            A_ = amp(bx)
            ph = self.k * bx - self.w * t
            ob.location = (self.ox + bx + A_ * math.sin(ph), by, bz)
            dense = max(0.0, -math.cos(ph)) if A_ > 0 else 0.0
            c = [VIOLET[q] + (TEAL[q] - VIOLET[q]) * dense for q in range(3)]
            ob.color = (*lin(c), 1)


S = A.scene
upd = None
# Whole phone screen (1080x1920, Aly review 1 2026-10-26): the band covers the top ~16 %, his captions sit at ~73-81 %, so the subject is
# framed a little ABOVE the middle (shift_y) and the frame is filled top to bottom (taller air blocks, a full-height mic on a stand,
# a tall speaker cabinet, water to the horizon). The 1040x1000 box version of these scenes is in git history (commit ae52a8e).
cam.data.shift_y = -0.05
if S == 'wave':
    look((4.2, -18.5, 3.0), (0, 0, 0))
    cu = bpy.data.curves.new('wave', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.24; cu.bevel_resolution = 6
    sp = cu.splines.new('POLY'); sp.points.add(119)
    ob = bpy.data.objects.new('wave', cu); sc.collection.objects.link(ob); cu.materials.append(mat('Teal', TEAL, rough=0.25, emit=2.5, coat=1))

    def upd(f):
        t = f / 30; grow = min(1, f / 30)
        for i, p in enumerate(sp.points):
            x = -5 + 10 * i / 119 * grow
            p.co = (x, 0.9 * math.cos(x * 1.6 - t * 4), 2.1 * math.sin(x * 1.6 - t * 4) * math.exp(-(x + 5) * 0.04), 1)
        ob.rotation_euler = (0, 0, -0.3 + 0.1 * math.sin(t / 2))

elif S == 'ripple':
    # looking down at the water (it fills the screen and fades away at the horizon); the stone falls from FAR above (Aly review 1)
    look((0, -9, 15), (0, 2.5, -0.5))
    N = 320
    bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=N, y_segments=N, size=36)
    water = mesh_obj('water', bm, mat('Water', (0.16, 0.56, 0.82), rough=0.12, coat=0.7, metal=0.0))
    rim = bpy.data.objects['Rim']; rim.location = (0, 40, 3); rim.data.size = 40; rim.data.energy = 14000; rim.data.color = (0.55, 0.85, 1)
    rim.rotation_euler = (math.radians(95), 0, math.pi)
    bpy.data.objects['Key'].location = (13, -3, 7); bpy.data.objects['Key'].data.energy = 1600
    me = water.data
    base = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get('co', base); base = base.reshape(-1, 3)
    r = np.hypot(base[:, 0], base[:, 1])
    stone = mesh_obj('stone', sphere(0.55, 8, 6), mat('Stone', (0.54, 0.56, 0.6), rough=0.9, coat=0), smooth=False)
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.0
    try:  # fade the water to transparent far away (alpha blend), centred a bit behind the splash so the near water stays solid
        mw = water.data.materials[0]; mw.surface_render_method = 'BLENDED'
        p = next(n for n in mw.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
        tc = mw.node_tree.nodes.new('ShaderNodeTexCoord'); gr = mw.node_tree.nodes.new('ShaderNodeTexGradient'); gr.gradient_type = 'SPHERICAL'
        mp = mw.node_tree.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (0.055, 0.055, 0.055); mp.inputs['Location'].default_value = (0, -0.1, 0)
        mw.node_tree.links.new(tc.outputs['Object'], mp.inputs['Vector']); mw.node_tree.links.new(mp.outputs['Vector'], gr.inputs['Vector'])
        mw.node_tree.links.new(gr.outputs['Fac'], p.inputs['Alpha'])
    except Exception as e:
        print('fade off', e)

    def upd(f):
        t = f / 30; drop = 1.5; H0 = 12.0
        z = np.zeros_like(r)
        for k in range(8):  # a new stone every 3.5 s keeps rings on screen the whole piece
            tt = t - drop - 3.5 * k; front = tt * 3.2
            if tt > 0:
                m_ = r < front
                z[m_] += 0.5 * np.sin((r[m_] - front) * 2.4) * np.exp(-r[m_] * 0.14) * np.exp(-(front - r[m_]) * 0.22)
        co = base.copy(); co[:, 2] = z
        me.vertices.foreach_set('co', co.ravel()); me.update()
        tl = (t - drop) % 3.5 if t >= drop else t - drop  # time since the last stone hit
        tn = 3.5 - tl if t >= drop else drop - t           # time until the next stone hits
        sz = H0 * (tn / drop) ** 2 if tn < drop else (-1.5 - tl * 0.6 if tl < 1 else H0 + 6)
        stone.location = (0, 0, sz); stone.hide_render = sz < -1.4
        stone.rotation_euler = (t * 2.1, t * 1.3, 0)

elif S == 'molecules':
    look((2.4, -17.5, 1.6), (-0.6, 0, 0))
    bar = A.bar
    air = Air(nz=13, x0=-3.8 if bar else -4.6)
    if bar:
        metal = mesh_obj('bar', cube(0.35, 2.6, 7.8), mat('Metal', (0.8, 0.83, 0.87), metal=1, rough=0.22))
        stick = mesh_obj('stick', cyl(0.11, 0.11, 3.4, 12), mat('Wood', (0.55, 0.35, 0.17), rough=0.8, coat=0))

    def upd(f):
        t = f / 30; hit = 1.0 if bar else 0.3; front = max(0, (t - hit) * 3.5)
        air.set(t, lambda x: 0.22 if x + 4.6 < front else 0)
        if bar:
            sh = 0.08 * math.sin(t * 60) * math.exp(-(t - hit) * 0.8) if t > hit else 0
            metal.location = (-4.9 + sh, 0, 0)
            st = min(1, t / hit)
            stick.location = (-5.9 - 1.4 * (1 - st), 0, 2.2 + 1.2 * (1 - st)); stick.rotation_euler = (0, 0.9 - 0.9 * st, 0)

elif S == 'mic':
    # a COMPLETE studio mic (Aly review 1): side-address capsule with a wire grille and the gold diaphragm inside, body, shock mount,
    # stand + base, cable to a laptop that draws what the diaphragm records. The wave comes from the left at head height.
    look((4.2, -16, 0.6), (-0.4, 0, -0.4))
    HZ = 3.4  # head height
    air = Air(nx=12, ny=4, nz=6, x0=-4.8, x1=-0.6, origin=(0, 0, HZ))
    metal = mat('Grille', (0.79, 0.82, 0.86), metal=1, rough=0.3)
    dark = mat('Body', (0.14, 0.17, 0.22), metal=0.6, rough=0.35)
    gr = mesh_obj('grille', sphere(1.25, 22, 14), metal, loc=(1.1, 0, HZ)); gr.scale = (1, 1, 1.35)
    wm = gr.modifiers.new('wire', 'WIREFRAME'); wm.thickness = 0.035
    band = mesh_obj('band', torus(1.27, 0.09), metal, loc=(1.1, 0, HZ - 1.45))
    dia = mesh_obj('dia', cyl(0.85, 0.85, 0.05), mat('Gold', GOLD, metal=0.7, rough=0.25, emit=1.3), loc=(1.1, 0, HZ), rot=(0, math.pi / 2, 0))
    ring = mesh_obj('ring', torus(0.9, 0.05), mat('GoldR', GOLD, metal=0.8, rough=0.3), loc=(1.1, 0, HZ), rot=(0, math.pi / 2, 0))
    body = mesh_obj('body', cyl(1.05, 0.85, 3.6, 40), dark, loc=(1.1, 0, HZ - 3.3))
    dot = mesh_obj('logo', cyl(0.18, 0.18, 0.05, 24), mat('Dot', GOLD, metal=0.8, emit=0.8), loc=(1.1, -1.0, HZ - 2.3), rot=(math.pi / 2, 0, 0))
    clip = mesh_obj('clip', cyl(0.95, 0.95, 0.35, 40), metal, loc=(1.1, 0, HZ - 3.2))
    yoke = mesh_obj('yoke', cube(0.12, 0.12, 1.4), metal, loc=(1.1, 0, HZ - 3.75))
    pole = mesh_obj('pole', cyl(0.12, 0.12, 4.6, 16), metal, loc=(1.1, 0, HZ - 6.7))
    base_ = mesh_obj('base', cyl(1.7, 1.9, 0.25, 48), dark, loc=(1.1, 0, HZ - 9.1))
    # laptop on the left at the bottom: screen facing the camera + the recorded line
    lapz = HZ - 7.6
    scr = mesh_obj('screen', cube(3.6, 0.1, 2.2), mat('Screen', (0.05, 0.08, 0.15), rough=0.4, emit=0.3), loc=(-2.6, 0, lapz + 1.1))
    lid = mesh_obj('lid', cube(3.8, 0.08, 2.4), mat('Lid', (0.5, 0.53, 0.58), metal=0.8, rough=0.35), loc=(-2.6, 0.09, lapz + 1.1))
    kb = mesh_obj('kb', cube(3.8, 2.4, 0.12), mat('Kb', (0.5, 0.53, 0.58), metal=0.8, rough=0.35), loc=(-2.6, -1.1, lapz - 0.05))
    cab = bpy.data.curves.new('cable', 'CURVE'); cab.dimensions = '3D'; cab.bevel_depth = 0.06
    sc_ = cab.splines.new('BEZIER'); sc_.bezier_points.add(1)
    for bp, co_, hl, hr in [(sc_.bezier_points[0], (1.1, 0.3, HZ - 4.6), (1.1, 0.3, HZ - 4.0), (1.1, 0.4, HZ - 6.5)),
                            (sc_.bezier_points[1], (-0.7, -0.6, lapz + 0.1), (0.2, -0.3, lapz - 0.5), (-1.0, -0.7, lapz + 0.2))]:
        bp.co, bp.handle_left, bp.handle_right = co_, hl, hr
    cob = bpy.data.objects.new('cable', cab); sc.collection.objects.link(cob); cab.materials.append(mat('CableM', (0.08, 0.08, 0.1), rough=0.6, coat=0))
    cu = bpy.data.curves.new('rec', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.05; sp = cu.splines.new('POLY'); sp.points.add(89)
    line = bpy.data.objects.new('rec', cu); sc.collection.objects.link(line); cu.materials.append(mat('Line', TEAL, emit=4))

    def upd(f):
        t = f / 30; front = t * 3.2
        air.set(t, lambda x: 0.2 if x + 6 < front else 0)
        hit = front > 6.2
        d = 0.22 * math.sin(2.2 * 1.3 - 5 * t) * (1 if hit else 0)
        dia.location = (1.1 + d, 0, HZ); ring.location = (1.1 + d * 0.3, 0, HZ)
        rec = max(0, t - 2.1)
        for i, p in enumerate(sp.points):
            u = i / 89; age = u * min(rec, 3)
            p.co = (-4.1 + u * 3.0, -0.1, lapz + 1.1 + (0.45 * math.sin(1.3 * 2.2 - 5 * (t - age)) if rec > 0 else 0), 1)
        line.hide_render = rec <= 0

elif S == 'speaker':
    # a COMPLETE speaker (Aly review 1): tall cabinet, woofer (cone + gold surround + dust cap), tweeter, port, feet; the woofer pushes
    # the air to the right, the same wave again
    look((6.5, -15.5, 1.2), (0.9, 0, 0))
    air = Air(nx=15, ny=4, nz=12, x0=0.4, x1=5.2, origin=(0.5, 0, -0.4))
    cabm = mat('Box', (0.1, 0.13, 0.2), rough=0.5, coat=0.4)
    box = mesh_obj('box', cube(2.4, 3.2, 7.2), cabm, loc=(-2.4, 0, 0))
    FX = -1.2  # front face
    woofer_z, tw_z = -1.4, 2.2
    cone = mesh_obj('cone', cyl(1.3, 0.15, 0.8, 48, cap=False), mat('Cone', (0.42, 0.47, 0.56), rough=0.45), loc=(FX - 0.3, 0, woofer_z), rot=(0, -math.pi / 2, 0))
    surround = mesh_obj('surr', torus(1.36, 0.1), mat('GoldR', GOLD, metal=0.8, rough=0.3), loc=(FX - 0.02, 0, woofer_z), rot=(0, math.pi / 2, 0))
    frame = mesh_obj('frame', torus(1.55, 0.07), mat('Frame', (0.3, 0.32, 0.36), metal=0.9, rough=0.3), loc=(FX + 0.02, 0, woofer_z), rot=(0, math.pi / 2, 0))
    dome = mesh_obj('dome', sphere(0.32), mat('Gold', GOLD, metal=0.8, rough=0.25, emit=0.6), loc=(FX + 0.05, 0, woofer_z))
    tw = mesh_obj('tw', sphere(0.42), mat('Tw', (0.75, 0.78, 0.82), metal=1, rough=0.2), loc=(FX - 0.15, 0, tw_z))
    twr = mesh_obj('twr', torus(0.6, 0.07), mat('Frame2', (0.3, 0.32, 0.36), metal=0.9, rough=0.3), loc=(FX + 0.02, 0, tw_z), rot=(0, math.pi / 2, 0))
    port = mesh_obj('port', torus(0.35, 0.08), mat('Port', (0.05, 0.05, 0.07), rough=0.6), loc=(FX + 0.02, 0, -3.2), rot=(0, math.pi / 2, 0))
    for k, yy in enumerate((-1.2, 1.2)):
        mesh_obj(f'foot{k}', cyl(0.25, 0.3, 0.3, 16), cabm, loc=(-2.4, yy, -3.75))

    def upd(f):
        t = f / 30; c = 0.18 * math.sin(5 * t); front = max(0, (t - 0.5) * 3.2)
        cone.location = (FX - 0.3 + c, 0, woofer_z); dome.location = (FX + 0.05 + c, 0, woofer_z)
        air.set(t, lambda x: 0.2 if (x - 0.4 < front and x > 0.4) else 0)
else:
    raise SystemExit('unknown scene ' + S)

os.makedirs(A.out, exist_ok=True)
frames = [A.still] if A.still >= 0 else range(A.frames)
for f in frames:
    sc.frame_set(f + 1)
    upd(f)
    bpy.context.view_layer.update()
    sc.render.filepath = os.path.join(A.out, f'{f:04d}.png')
    bpy.ops.render.render(write_still=True)
print('@@JSON@@{"ok": true, "scene": "%s", "frames": %d, "out": "%s"}' % (S, len(list(frames)), A.out.replace('\\', '/')))
