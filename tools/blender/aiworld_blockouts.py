"""Grey BLOCKOUTS for «عالم الـ AI كله» (RUN_v9, 2026-11-20): exact motion + camera, no look.
Later: last frame PNG / the mp4 -> Higgsfield (start frame / video-to-video) puts the look on top (Tip 6).
Usage:
  blender --background --factory-startup --python tools/blender/aiworld_blockouts.py -- <scene> <out_dir> [engine]
  scene: jet | lab | bridge      engine: WORKBENCH (default, fast) | EEVEE
Writes <out_dir>/<scene>_blockout.mp4 (1280x720, 25 fps) + <scene>_last.png (1920x1080)."""
import bpy, math, sys, os
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["jet", "."]
SCENE, OUT = argv[0], argv[1]
ENGINE = argv[2] if len(argv) > 2 else "WORKBENCH"
os.makedirs(OUT, exist_ok=True)
FPS = 25

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS


def mat(name, rgb, emit=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*rgb, 1)
    if emit:
        b.inputs["Emission Color"].default_value = (*rgb, 1)
        b.inputs["Emission Strength"].default_value = emit
    return m


GREY, DARK, CYAN, GOLD = mat("grey", (0.62, 0.64, 0.68)), mat("dark", (0.12, 0.13, 0.16)), mat("cyan", (0.2, 0.85, 1.0), 4), mat("gold", (1.0, 0.72, 0.25), 3)


def add(kind, loc, scale=(1, 1, 1), rot=(0, 0, 0), m=GREY, name=None):
    fn = {"cube": bpy.ops.mesh.primitive_cube_add, "cyl": bpy.ops.mesh.primitive_cylinder_add,
          "sphere": bpy.ops.mesh.primitive_uv_sphere_add, "cone": bpy.ops.mesh.primitive_cone_add,
          "torus": bpy.ops.mesh.primitive_torus_add}[kind]
    fn(location=loc, rotation=rot)
    o = bpy.context.active_object
    o.scale = scale
    if name:
        o.name = name
    o.data.materials.append(m)
    return o


def key(o, f, loc=None, rot=None, scale=None):
    if loc is not None:
        o.location = loc; o.keyframe_insert("location", frame=f)
    if rot is not None:
        o.rotation_euler = rot; o.keyframe_insert("rotation_euler", frame=f)
    if scale is not None:
        o.scale = scale; o.keyframe_insert("scale", frame=f)


def camera(path, look, frames):
    """path: list of (frame, location); camera always looks at `look` (empty, may move)."""
    bpy.ops.object.empty_add(location=look)
    tgt = bpy.context.active_object
    bpy.ops.object.camera_add()
    cam = bpy.context.active_object
    cam.data.lens = 32
    c = cam.constraints.new("TRACK_TO"); c.target = tgt; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
    for f, p in path:
        key(cam, f, loc=p)
    sc.camera = cam
    sc.frame_start, sc.frame_end = 1, frames
    return cam, tgt


def floor():
    add("cube", (0, 0, -0.05), (40, 40, 0.05), m=DARK)


def sun(angle=50, rot_z=30, f_end=None, rot_z_end=None, energy=4):
    bpy.ops.object.light_add(type="SUN", rotation=(math.radians(angle), 0, math.radians(rot_z)))
    s = bpy.context.active_object; s.data.energy = energy
    if f_end:
        key(s, 1, rot=(math.radians(angle), 0, math.radians(rot_z)))
        key(s, f_end, rot=(math.radians(84), 0, math.radians(rot_z_end)))
    return s


# ---------------------------------------------------------------------------------------------------
if SCENE == "jet":  # fighter jet (generic, original) -> exploded view = 6 families, MCP wires light up
    N = 150
    floor()
    parts = {
        "body": add("cyl", (0, 0, 2), (0.45, 0.45, 3.2), rot=(0, math.radians(90), 0)),
        "nose": add("cone", (3.9, 0, 2), (0.45, 0.45, 0.8), rot=(0, math.radians(90), 0)),
        "cockpit": add("sphere", (1.8, 0, 2.4), (0.9, 0.35, 0.3), m=CYAN),
        "wing_l": add("cube", (-0.2, 1.9, 2), (1.2, 1.6, 0.06), rot=(0, 0, math.radians(-18))),
        "wing_r": add("cube", (-0.2, -1.9, 2), (1.2, 1.6, 0.06), rot=(0, 0, math.radians(18))),
        "tail": add("cube", (-2.8, 0, 2.8), (0.6, 0.06, 0.8)),
    }
    out_dirs = {"body": (0, 0, 1.2), "nose": (2.2, 0, 0.8), "cockpit": (0.8, 0, 2.2), "wing_l": (0, 2.4, 0.6),
                "wing_r": (0, -2.4, 0.6), "tail": (-2.2, 0, 1.6)}
    for i, (k, o) in enumerate(parts.items()):
        p0 = o.location.copy(); r0 = o.rotation_euler.copy()
        key(o, 30, loc=p0, rot=r0)
        d = Vector(out_dirs[k])
        key(o, 75 + i * 3, loc=p0 + d, rot=(r0.x + 0.4 * (i % 2), r0.y + 0.25, r0.z + 0.5 * (1 - 2 * (i % 2))))
        key(o, N, loc=p0 + d * 1.15)
    # MCP "wires": thin glowing cylinders from the centre (Claude) to each part, they grow after the split
    for i, (k, o) in enumerate(parts.items()):
        tgt = o.location + Vector(out_dirs[k]) * 1.1
        mid = (Vector((0, 0, 3.4)) + tgt) / 2
        v = tgt - Vector((0, 0, 3.4))
        w = add("cyl", mid, (0.025, 0.025, v.length / 2), m=CYAN)
        w.rotation_euler = v.to_track_quat("Z", "Y").to_euler()
        key(w, 1, scale=(0.025, 0.025, 0)); key(w, 95 + i * 6, scale=(0.025, 0.025, 0)); key(w, 110 + i * 6, scale=(0.025, 0.025, v.length / 2))
    add("sphere", (0, 0, 3.4), (0.35, 0.35, 0.35), m=GOLD, name="claude_core")
    sun()
    camera([(1, (9, -6, 2.6)), (60, (7, -7, 3.2)), (150, (3, -9, 8))], (0, 0, 2.6), N)

elif SCENE == "lab":  # high-tech lab: robot arm places a part, macro push-in
    N = 125
    floor()
    add("cube", (0, 0, 0.9), (2.4, 1.2, 0.08), m=GREY)                       # table
    for x in (-2.2, 2.2):
        for y in (-1.0, 1.0):
            add("cyl", (x, y, 0.45), (0.06, 0.06, 0.45), m=DARK)
    base = add("cyl", (1.6, 0, 1.15), (0.3, 0.3, 0.17), m=DARK)
    arm1 = add("cube", (1.6, 0, 1.75), (0.09, 0.09, 0.55))
    arm2 = add("cube", (1.15, 0, 2.25), (0.5, 0.07, 0.07))
    claw = add("cone", (0.65, 0, 2.05), (0.12, 0.12, 0.18), rot=(math.pi, 0, 0), m=CYAN)
    part = add("cube", (0.65, 0, 1.75), (0.18, 0.18, 0.12), m=GOLD)
    socket = add("torus", (-0.6, 0, 1.0), (0.25, 0.25, 0.25), m=CYAN)
    for o, a, b in ((arm2, (1.15, 0, 2.25), (0.55, 0, 2.05)), (claw, (0.65, 0, 2.05), (-0.6, 0, 1.55)),
                    (part, (0.65, 0, 1.75), (-0.6, 0, 1.06))):
        key(o, 10, loc=a); key(o, 95, loc=b)
    key(socket, 95, scale=(0.25, 0.25, 0.25)); key(socket, 105, scale=(0.4, 0.4, 0.4)); key(socket, 115, scale=(0.25, 0.25, 0.25))
    # holo screens
    for i, x in enumerate((-1.6, 0, 1.6)):
        add("cube", (x, 1.6, 2.2), (0.6, 0.02, 0.35), m=CYAN)
    sun(angle=60, rot_z=-40, energy=3)
    camera([(1, (3.5, -3.8, 2.6)), (125, (0.2, -1.6, 1.45))], (-0.3, 0, 1.2), N)

elif SCENE == "bridge":  # Qasr al-Nil style bridge (generic blockout: arches + pedestals as boxes) rises piece by piece
    N = 150
    add("cube", (0, 0, -0.3), (40, 8, 0.2), m=mat("water", (0.1, 0.25, 0.4)))      # river
    add("cube", (0, 11, 0), (40, 3, 0.4), m=DARK); add("cube", (0, -11, 0), (40, 3, 0.4), m=DARK)  # banks
    pieces = []
    for i in range(7):  # deck spans + arches across the river (along Y)
        y = -7.5 + i * 2.5
        d = add("cube", (0, y, 1.2), (1.6, 1.25, 0.12))
        a = add("torus", (0, y, 0.2), (1.2, 1.2, 1.2), rot=(0, math.radians(90), 0), m=GREY)
        a.scale = (1.0, 1.25, 1.0)
        pieces += [a, d]
    for s in (-1, 1):  # pedestals on both ends
        for x in (-1.4, 1.4):
            pieces.append(add("cube", (x, s * 9.6, 1.0), (0.35, 0.6, 0.6), m=GOLD))
    for i, o in enumerate(pieces):
        p = o.location.copy()
        key(o, 1, loc=(p.x, p.y, p.z - 6)); key(o, 6 + i * 3, loc=(p.x, p.y, p.z - 6)); key(o, 20 + i * 3, loc=p)
    sun(angle=35, rot_z=10, f_end=N, rot_z_end=110, energy=4)
    path = [(f, (14 * math.cos(math.radians(-60 + f * 0.9)), 14 * math.sin(math.radians(-60 + f * 0.9)), 5 + f * 0.02)) for f in range(1, N + 1, 15)]
    camera(path, (0, 0, 1), N)
else:
    raise SystemExit(f"unknown scene {SCENE}")

# --- render ---------------------------------------------------------------------------------------
if ENGINE == "WORKBENCH":
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.display.shading.light = "STUDIO"
    sc.display.shading.color_type = "MATERIAL"
    sc.display.shading.show_shadows = True
    sc.display.shading.show_cavity = True
else:
    sc.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in bpy.types.RenderEngine.bl_rna.properties["bl_idname"].enum_items.keys() else "BLENDER_EEVEE"
w = bpy.data.worlds.new("w"); w.color = (0.02, 0.025, 0.04); sc.world = w
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1280, 720, 100
if hasattr(sc.render.image_settings, "media_type"):  # Blender 5.x: video is a media type
    sc.render.image_settings.media_type = "VIDEO"
sc.render.image_settings.file_format = "FFMPEG"
sc.render.ffmpeg.format = "MPEG4"; sc.render.ffmpeg.codec = "H264"; sc.render.ffmpeg.constant_rate_factor = "MEDIUM"
sc.render.filepath = os.path.join(OUT, f"{SCENE}_blockout.mp4")
bpy.ops.render.render(animation=True)
# last frame, full HD PNG (start frame for Higgsfield later)
sc.frame_set(sc.frame_end)
if hasattr(sc.render.image_settings, "media_type"):
    sc.render.image_settings.media_type = "IMAGE"
sc.render.image_settings.file_format = "PNG"
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.render.filepath = os.path.join(OUT, f"{SCENE}_last.png")
bpy.ops.render.render(write_still=True)
print("DONE", SCENE)
