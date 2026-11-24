"""Higgsfield image-to-video requests for the 34 C shots of shotlist_v2 (bundle المقترح). One take per shot, no retries.
Start frame = approved keyframe (keyframes_final). Kling 4.0 i2v 1080p 6 s (22.5) ; flex shots = Seedance 2.5 720p 5 s (35, no audio).
C11 song shots without their own keyframe reuse another world's keyframe with a different, faster camera move.
Writes work/clips_v1.json (all requests + cost) and work/clips_v1_batch{1,2,3}.json (12 per call).
Usage (project folder): python -X utf8 work/scripts/clips_v1.py"""
import json

kf = json.load(open("work/keyframes_v1.json", encoding="utf-8"))
fin = json.load(open("assets/ai/higgsfield/keyframes_final/keyframes_final.json", encoding="utf-8"))
JOB = {it["index"]: it["job_id"] for it in kf["items"]}
JOB.update({int(k): v for k, v in fin["new_job_ids"].items()})
JOB[162] = "5708dc55-238f-4d61-b443-482559203e86"           # approved test v6
REUSE = {204: 112, 207: 53, 210: 115, 213: 6}              # C11 shots without own keyframe
FLEX = {26, 53, 112, 162, 216}
ALY = {6, 9, 19, 26, 28, 115, 117, 162, 168, 201, 210, 213}   # shots whose start frame shows Aly
KEEP_ALY = " Keep the man's face, body and black t-shirt exactly as in the start image. Smooth cinematic motion, no morphing, no text, no logos."
KEEP_SCENE = " Keep the scene, style and composition of the start image. Smooth cinematic motion, no morphing, do not add people, no text, no logos."
M = {
    6: "Slow dolly-in from outside the glass canopy into the cockpit; the holographic HUD flickers on; the pilot turns his head slightly toward the camera.",
    9: "Slow push-in on the pilot's face; holographic icons of the six aircraft parts rotate and glow; subtle cockpit vibration.",
    19: "Pictures fly around him in a spiral like birds; he points at one and smiles; gentle camera orbit; sparkles pop where pictures appear.",
    22: "The paper ribbon flows into the frame and the painting fills with color from left to right; slow push-in.",
    25: "The four panels animate one after another: background swaps to a beach, an object is erased with a sparkle, the frame expands outward, a watercolor wash spreads.",
    26: "Steadicam moving backward in front of him as he walks toward the camera through the crowd; carriages pass behind him; dust in the warm light.",
    28: "Watercolor brush strokes animate and settle as he walks forward; paper texture stays visible; gentle handheld drift.",
    29: "Slow crane up revealing the whole market street and the minarets; people and carriages move below.",
    31: "A beam of light travels from the blue first frame to the amber last frame and fills the middle with motion streaks; slow lateral dolly.",
    32: "The sun sets, street lamps light up one by one, long shadows stretch; very slow push-in.",
    53: "Wireframe hologram lines turn into solid stone from left to right; camera glides slowly along the bridge toward the lions; reflections ripple on the Nile.",
    56: "Slow drone glide along the bridge at golden hour; sailboats drift on the Nile; traffic and pedestrians move.",
    99: "Tiny robots work at their consoles, green code rain falls on the screens; slow tilt-shift push-in toward the main robot.",
    102: "The robot's mechanical hands move: one opens the folder, one types, one moves the magnifier; the green check mark pulses.",
    105: "Conveyor belts move; the toy robots pass a film strip along the line; the scissors robot cuts it; slow lateral track.",
    112: "The light cables ignite one after another along the six jet modules, sparks jump, the whole aircraft starts to glow; slow orbit around it.",
    115: "Books fly around him, open and glow; he turns his head following them, delighted; gentle push-in.",
    117: "A stream of colorful light flows from the open book into his hand and swirls up his arm; sparkles; slight push-in.",
    162: "Low-angle slow push-in; the holographic chart bars grow, light coins orbit around him; volumetric haze drifts.",
    165: "Hologram bars grow and coins stack up on the floating invoice; slow sideways dolly past the vault door.",
    168: "Bullet-time moment: almost frozen action, the camera slowly orbits around the hand-off of the glowing module, dust particles hang in the air.",
    171: "Slow push-in toward the completed jet; hangar lights switch on row by row; the silhouette stays still.",
    183: "The jet streaks low over Cairo at sunset; the camera tracks alongside it; the Nile shines below.",
    186: "The torch flame flickers; the hand lifts from the rock wall, revealing a fresh red ochre handprint beside the painted animals.",
    189: "The scribe draws a careful line on the papyrus with the reed brush; the oil lamp flickers.",
    192: "The painter adds the final brush stroke to the portrait; candles flicker; slow push-in.",
    195: "The animator flips the stack of drawings and the character appears to move; lamp light; slight push-in.",
    198: "Glowing particles rise from the tablet and form floating images around her; the neon city glows outside.",
    201: "The six glowing parts orbit him and lock together into a shining aircraft above; he raises his arms; camera pulls back.",
    204: "Fast orbit around the glowing jet modules on the beat; sparks fly.",
    207: "Fast crane up over the glowing hologram bridge; city lights flicker on.",
    210: "Whip pan through the flying glowing books; he laughs and reaches out.",
    213: "Fast pull-back from the cockpit to reveal the whole jet in the hangar.",
    216: "Drone pull-out: the jet rolls out of the giant hangar doors into the sunrise; the whole facility appears below.",
}
shots = [r for r in json.load(open("work/shotlist_v2.json", encoding="utf-8")) if r["type"] == "C"]
reqs, total = [], 0.0
for r in shots:
    n = r["n"]; src = REUSE.get(n, n)
    if n in FLEX:
        p = {"model": "seedance_2_5", "mode": "omni_reference", "resolution": "720p", "duration": 5, "generate_audio": False,
             "aspect_ratio": "16:9", "prompt": M[n] + (KEEP_ALY if n in ALY else KEEP_SCENE), "medias": [{"value": JOB[src], "role": "start_image"}]}
        cost = 35.0
    else:
        p = {"model": "kling4_0", "mode": "image-to-video", "resolution": "1080p", "duration": 6, "aspect_ratio": "16:9",
             "prompt": M[n] + (KEEP_ALY if n in ALY else KEEP_SCENE), "medias": [{"value": JOB[src], "role": "start_image"}]}
        cost = 22.5
    total += cost
    reqs.append({"index": n, "chapter": r["chapter"], "shot_start": r["start"], "shot_dur": r["dur"], "keyframe": src, "cost": cost, "params": p})
json.dump({"total_cost": total, "requests": reqs}, open("work/clips_v1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for b in range(0, len(reqs), 12):
    json.dump([{"index": q["index"], "params": q["params"]} for q in reqs[b:b + 12]],
              open(f"work/clips_v1_batch{b // 12 + 1}.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(reqs), "clips, total", total, "credits")
