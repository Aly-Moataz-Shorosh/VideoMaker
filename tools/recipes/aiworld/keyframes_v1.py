"""Keyframe prompts v1 (bundle المقترح, step 3): 30 start images for the Higgsfield (C) shots of shotlist_v2.
index = shot n in shotlist_v2. Model nano_banana_2, 16:9, 1k (1.5 credits each). Writes work/keyframes_v1.json."""
import json

A, J, L, B = ("4e1cf9c8-617d-4fd6-bbc4-21035acbec56", "98e1910f-3bd6-4138-81a9-05b128a251c2",
              "7ea02ba1-6a81-49ec-b01e-643de8871463", "40c60646-a419-4917-87f7-624dd94788e7")
ALY = ("the same man as in the reference photo (bald head, short dark beard, dark navy blazer over a black t-shirt), "
       "same face")
NO = " No text, no letters, no logos, no watermark. 16:9 cinematic frame."
CIN = "Cinematic 3D render, dramatic teal and amber lighting, volumetric haze, shallow depth of field, high detail."
TOON = "Clean modern 2D cartoon illustration, bold flat colors, soft cel shading, thick outlines, playful."
TOY = ("Stylized toy 3D render, glossy plastic and soft rubber materials, miniature tilt-shift look, bright studio light, "
       "original characters.")
LIVE = "Photorealistic live-action film still, natural skin, 35mm lens, cinematic color grade, soft film grain."
K = [
    (6, "C01", [A, J], f"{CIN} Exterior of a futuristic fighter jet cockpit built in a high-tech hangar, camera outside the glass canopy looking in; {ALY} sits in the pilot seat, holographic HUD glowing on the canopy glass. Composition matches the grey blockout reference: the jet made of six separate modules."),
    (9, "C01", [A], f"{CIN} Inside a fighter jet cockpit, {ALY} at the controls looking at a holographic display that shows six glowing modular parts of the aircraft as abstract icons, blue rim light on his face."),
    (19, "C02a", [A], f"{TOON} A cartoon version of {ALY} stands in the middle of a floating gallery: dozens of freshly generated pictures (landscapes, portraits, animals, products) fly around him like birds, sparkles where each picture appears."),
    (22, "C02a", [], f"{TOON} Concept of text-to-image: a long handwritten ribbon of paper flows into a big picture frame and turns into a colorful painting of a sunny Egyptian village by the Nile."),
    (25, "C02a", [], f"{TOON} Concept of image editing: one photo of a cat on a sofa shown four times side by side, each with a different edit (new beach background, an object erased with a magic eraser, the picture extended beyond its frame, a watercolor style version)."),
    (26, "C02b", [A], f"{LIVE} {ALY} walks toward the camera down a busy Cairo street around 1897, recreated in color: horse carriages, wooden mashrabiya balconies, people in period clothes, dust in warm afternoon light. He wears his modern blazer, steadicam framing at chest height."),
    (28, "C02b", [A], f"Hand-painted watercolor illustration of the same scene: {ALY} walking down a historic Cairo street around 1897 with horse carriages and mashrabiya balconies, loose brush strokes, paper texture, warm palette."),
    (29, "C02b", [], f"{LIVE} Wide shot of a historic Cairo market street around 1897 recreated in color: minarets in the background, shops with cloth awnings, horse carriages, crowds, golden hour light, dust in the air."),
    (31, "C02b", [], f"{CIN} A sleek dark video-editing interface floating in 3D space: two large glowing frames (first frame on the left in blue, last frame on the right in amber), a light beam between them filling the middle with motion streaks."),
    (32, "C02b", [], f"{LIVE} The same historic Cairo street around 1897 at sunset, empty and calm, long shadows, lamps being lit, warm orange sky, final frame of a sequence."),
    (53, "C02f", [B], f"{CIN} A glowing blue hologram of Qasr El Nil bridge in Cairo at night with its stone lion statues, wireframe lines turning into solid stone, reflections on the Nile, city lights. Match the camera angle of the grey blockout reference."),
    (56, "C02f", [B], f"{LIVE} Photorealistic Qasr El Nil bridge over the Nile in Cairo at golden hour, stone lion statues at the entrance, traffic and pedestrians, warm light, exact same camera angle and composition as the grey blockout reference."),
    (99, "C03", [], f"{TOY} A miniature control room full of screens with green code raining down like digital rain; a small friendly robot character with big round eyes sits at the main desk directing other tiny robots."),
    (102, "C03", [], f"{TOY} A small robot character with extra mechanical hands works at a miniature desk: one hand opens a folder, one types on a tiny keyboard, one holds a magnifying glass over a screen showing a green check mark."),
    (105, "C03", [], f"{TOY} On a wooden desk, original toy machines work together like a factory line: a tiny film camera robot, a 3D cube robot, a pair of scissors robot cutting a film strip, and a microphone robot, connected by colorful conveyor belts."),
    (112, "C05", [J, L], f"{CIN} Inside a high-tech lab hangar, the six separate modules of a futuristic fighter jet float in place, connected by bright glowing light cables that light up one after another, sparks of energy, the whole aircraft starting to glow."),
    (115, "C06", [A], f"{TOON} A cartoon version of {ALY} stands in a magical library where open books fly around him, each book glowing a different color with a small symbol (a pen, a film reel, a music note, a gear)."),
    (117, "C06", [A], f"{TOON} A cartoon version of {ALY} reaches into an open glowing book and a stream of colorful light and sparkles flows from the pages into his hand, giving him a new power."),
    (162, "C08", [A], f"{CIN} Low-angle hero shot: {ALY} stands confidently in front of a giant round steel vault door, a holographic invoice floating beside him with glowing price bars, coins of light orbiting."),
    (165, "C08", [], f"{CIN} Close-up of a floating holographic invoice in front of a huge vault door, glowing bar segments and small coin icons stacking up, teal and gold light, shallow depth of field."),
    (168, "C09", [A, L], f"{LIVE} Frozen moment in a high-tech lab hangar: a real human hand gives the last glowing module of a futuristic jet to {ALY}, dust particles frozen in the air, dramatic rim light."),
    (171, "C09", [L], f"{LIVE} The completed futuristic fighter jet stands assembled in the middle of a high-tech lab hangar, a human silhouette in the foreground looking at it, cool blue light, epic wide shot."),
    (216, "C12", [J, L], f"{CIN} Aerial drone shot pulling back: the futuristic fighter jet rolls out of the giant lab hangar doors into a sunrise sky, the whole high-tech facility visible below, epic scale."),
    (183, "C11", [], f"{CIN} The futuristic fighter jet flies low over Cairo at sunset, the Nile river shining below, the city skyline in silhouette, motion blur, epic music-video feel."),
    (186, "C11", [], f"{LIVE} Inside a dark prehistoric cave lit by a torch, a human hand presses red ochre on the rock wall leaving a handprint beside painted animals, warm flickering light."),
    (189, "C11", [], f"{LIVE} An ancient Egyptian scribe sits cross-legged painting colorful figures on papyrus with a reed brush, oil lamp light, museum-quality recreation."),
    (192, "C11", [], f"{LIVE} A classical painter studio lit by candles, a painter at a wooden easel finishing a portrait, brushes and pigments on the table, chiaroscuro light."),
    (195, "C11", [], f"{LIVE} A 1930s animator draws on a glowing light table, stacks of pencil drawings of a cartoon character around him, warm lamp light, vintage film look."),
    (198, "C11", [], f"{LIVE} A modern digital artist draws on a graphic tablet at night, glowing particles rise from the screen and form floating images in the air around her, neon city outside the window."),
    (201, "C11", [A], f"{CIN} Finale: {ALY} stands in a modern studio with his arms open, six glowing modular parts orbit around him and lock together into a shining aircraft above, confetti of light."),
]
items = [{"index": n, "chapter": c, "refs": r, "prompt": p + NO} for n, c, r, p in K]
json.dump({"model": "nano_banana_2", "aspect_ratio": "16:9", "resolution": "1k", "cost_each": 1.5,
           "refs": {"aly_studio_look": A, "jet_last": J, "lab_last": L, "bridge_last": B}, "items": items},
          open("work/keyframes_v1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# batch request bodies (12 max per call)
for b in range(0, len(items), 12):
    req = [{"index": it["index"], "params": {"model": "nano_banana_2", "aspect_ratio": "16:9", "resolution": "1k",
            "prompt": it["prompt"], **({"medias": [{"value": m, "role": "image_references"} for m in it["refs"]]} if it["refs"] else {})}}
           for it in items[b:b + 12]]
    json.dump(req, open(f"work/keyframes_v1_batch{b // 12 + 1}.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(items))
