"""Blender: a generated GLB (image -> 3D) on a turntable, for the «صورة ← موديل 3D» example (v5 note 21).
blender -b -P work/scripts/glb_turntable.py -- in.glb out_dir  (frames PNG; ffmpeg makes the mp4)"""
import bpy, sys, math, os
from mathutils import Vector
a = sys.argv[sys.argv.index("--") + 1:]; src, out = a[0], a[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
mn = Vector((1e9,) * 3); mx = Vector((-1e9,) * 3)
for o in objs:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c); mn = Vector(map(min, mn, w)); mx = Vector(map(max, mx, w))
ctr = (mn + mx) / 2; size = max(mx - mn)
piv = bpy.data.objects.new("pivot", None); bpy.context.scene.collection.objects.link(piv); piv.location = ctr
for o in objs:
    if o.parent is None: o.parent = piv; o.matrix_parent_inverse = piv.matrix_world.inverted()
cam_d = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cam_d); bpy.context.scene.collection.objects.link(cam)
cam.location = ctr + Vector((0, -size * 1.9, size * 0.55)); bpy.context.scene.camera = cam
tr = cam.constraints.new("TRACK_TO"); tr.target = piv; tr.track_axis = "TRACK_NEGATIVE_Z"; tr.up_axis = "UP_Y"
for nm, loc, e in (("key", (size, -size, size * 1.5), 900), ("fill", (-size * 1.5, -size * 0.5, size), 300), ("rim", (0, size * 1.6, size), 600)):
    ld = bpy.data.lights.new(nm, "AREA"); ld.energy = e * max(1, size) ** 2 / 4; ld.size = size
    lo = bpy.data.objects.new(nm, ld); lo.location = ctr + Vector(loc); bpy.context.scene.collection.objects.link(lo)
    t = lo.constraints.new("TRACK_TO"); t.target = piv; t.track_axis = "TRACK_NEGATIVE_Z"; t.up_axis = "UP_Y"
sc = bpy.context.scene; sc.frame_start, sc.frame_end = 1, 150
piv.rotation_euler = (0, 0, 0); piv.keyframe_insert("rotation_euler", frame=1)
piv.rotation_euler = (0, 0, math.radians(360)); piv.keyframe_insert("rotation_euler", frame=151)
for fc in piv.animation_data.action.fcurves if piv.animation_data.action and hasattr(piv.animation_data.action, "fcurves") else []:
    for k in fc.keyframe_points: k.interpolation = "LINEAR"
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.02, 0.03, 0.07, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.6
sc.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items] else "BLENDER_EEVEE"
sc.render.resolution_x, sc.render.resolution_y = 1280, 720; sc.render.fps = 25
sc.render.image_settings.file_format = "PNG"; sc.render.filepath = os.path.join(out, "f_")
bpy.ops.render.render(animation=True)
