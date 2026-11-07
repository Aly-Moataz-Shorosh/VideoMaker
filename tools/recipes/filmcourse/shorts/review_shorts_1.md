# Aly's review of the 20 film-course shorts (2026-11-07) — collect ALL notes first, execute only after he says he is done

## 01 power stairs ("حلو اوي")
- At "دي اللي نزلت" (~0:56 in the short, and in the hook): the BLACK one (McGonagall) must go DOWN a step, not the pink.
- At "وطلعت": the pink goes up (already right).
- The scene all along = each one climbs in turn; only the END is different: black goes down, pink goes up.
- Fix in the body AND in the hook.

## 04 split diopter
- Several words are cut in the middle -> cut only before a word starts or after it ends (check every piece edge on the waveform + words).
- He gave ANOTHER example from الجزيرة and played a video of it -> bring that clip in (find it after ~3429 s: the film clip he plays).
- The hook shows the TILT SHIFT diagram (screen at src ~3436) -> unrelated: the hook must show the Split diopter / الجزيرة example only.

## 05 cut meaning
- The train: better motion — it must move logically, at an angle / in perspective along the tracks (not a flat emoji sliding). Consider a proper animated (3D/Blender-like) train.
- His round webcam: his face is cut in the circle -> enlarge (take a wider square of the webcam so his whole face fits) — applies to ALL shorts.
- Caption at ~0:17: he said "فيلم سيفن.. اللقطة اللي فاتت.. مش عارف انتو عارفينه ولا لا" (fix the caption).
- When he says it wasn't there at the beginning of cinema -> add WHEN the cut-for-meaning idea appeared (Kuleshov effect, ~1910s-1920s) with a verified source.
- At ~0:40 "لغة يا جماعة": he is commenting on a scene -> show THAT scene (the clip he played before 1658 s), the first scene.

## 02 chroma
- Remove "أمي" from the title: band title = "كروما من طرحة" (also the .txt titles; check labels/ladder text that say "طرحة أمي").

## 06 camera moves ("الموشن حلو خليه")
- Add a REAL Dolly zoom scene (a film example) so people understand; keep my MoveScene motion.
- In the dolly-zoom animation the character should be growing (he says "المفروض الشخصية تكون بتكبر") — re-check: in a true dolly zoom the subject keeps its size and the background changes; follow his note but explain with the real example. Ask him in one line if unclear.
- Empty area in the scene (under "الكاميرا شايفة كده", red box) -> fill it (no empty glass).
- While he explains the tripod moves, the tripod is NOT visible in my circle -> during the tripod demo show his webcam as a RECTANGLE the size of the frame (not the circle) so the tripod shows.
- Cut "نزل بعد ما عملت الكورس ده بكتير" (3562.8-3569.4); start from "كان فيه مشهد بيفضل ينقل كده كده" (~3569.4).

## 07 focus ("الموشن حلو")
- From the middle of the short on, he explains ON real pictures/videos (his screen: depth-of-field diagram 3237-3255, deep-focus astronaut 3267, soft/rack-focus clips 3285-3363) -> show THOSE while he talks (screen pieces, zoomed; keep the FocusScene only where he has nothing on screen).

## 08 video is a language — IMPORTANT ("الفيديو ده مهم و عايزه يوصل")
What he wants to say (rebuild the short around it, motion for each part):
- Beauty has TWO kinds.
  - In writing: (1) beauty of FORM — the shape of the writing (beautiful Arabic calligraphy, beautiful hieroglyphs); tools = brush, colours.
    (2) beauty of CONTENT — the words, the meaning and how it is delivered; tools = grammar (النحو) and rhetoric (البلاغة).
  - Same in video: (1) aesthetic eloquence in picture + music, like the film الست and الفيل الأزرق; tools = beautiful colours, sound, image,
    painting with light, movement, the pleasure that keeps you watching. (2) eloquence of CONTENT: deliver a good meaning in a good, deep way,
    using cinema tools in service of the MEANING (not only attention and pleasure): camera movement, shot size, the cut -> to deliver a message.
- He recorded TWO extra videos explaining this: 20261107_075021.mp4 and 20261107_075352.mp4 (screenshot shows them inside "_claude/Aly Shorosh - Content Creator";
  NOT found yet on disk under E:/root/output/_claude, Downloads, Videos, Desktop -> ask him for the path when executing).
- Use his new recordings + the course script; he allows ElevenLabs with HIS voice only to add a missing word (keep it minimal; never a whole AI line).

## 09 shot sizes (and ALL shorts)
- His face is not centred in the circle and part of the circle is empty/black (the webcam box position differs per part of the course).
  -> find the webcam box + his face PER PIECE (tools/face_pos.py or a detector on the proxy), centre the face, crop only inside the box.

## 10 script describes everything
- The hook is not the best -> pick a more beautiful moment.
- Not understandable: whenever he describes something from the script, SHOW it from the scene we analysed (Ibrahim El Abyad sc 55/56,
  project "2026-11-06 youtube sceneAnalysis ibrahimLabyad", assets motion_public/ibrahim) — the shot that was made + the way it was said,
  script line next to the matching film moment (like the scene-analysis style 20: script left / film right).
- 10 too: his face is cut in the circle, the slide shows in the corner (white area) -> wider + centred crop inside the webcam box only (same fix as 09, all shorts).

## 11 sequence / scene / shot
- His circle is small/cut again (same webcam fix).
- Caption: he said "اقطع لسان جوز بنتي" -> fix in the hook AND the body.
- From 0:30 to 1:10.15 what is on screen doesn't match what he says -> show the matching shots from the film (find them in the Ibrahim El Abyad analysis project).
- End card / CTA: TWO videos this time — the full course (youtu.be/S-tSUtClTOg) AND the Ibrahim El Abyad scene analysis (youtu.be/NWtPI7aiefw), each with thumbnail + QR.

## 12 framing
- His voice and picture are OUT OF SYNC: cause = the webcam pieces use src=2570 while the voice starts at 2566.6 -> his own face pieces must use src = a (never a different src when HE is on screen). Check every short for pieces where src != a and his face shows.
- Circle small again (webcam fix).
- When he says the basketball example -> show the basketball shot from the first video (BBC/basketball clip at ~330-360 s, camera in place of the ball).
- Too short: he gives examples for each shot type (single/two/three/crowd/OTS/POV pictures + the clips he played 2584-2606 and the Parasite / StudioBinder examples) -> include his examples.
- The 180-degree rule is missing -> add his explanation (2606-2613 + what follows ~2613-2700: 180 rule video he played; use only his voice, explain with motion: two people, the line, camera stays on one side, breaking it = chaos/power change).

## 13 process
- Circle small again (webcam fix).
- Caption: he said "في الـ Post-production" (not "في البوست النوش").
- The part where he talks about PRE-production is missing -> add it (919-955 "لازم تكون محضّر.. كل مشهد هيتصور إزاي والزاوية وحجم الكادر.." and 1010.3-1021.3 "في الـ Pre-production ادّي له حقه").
- The 5 steps card is cramped -> give it more room (bigger cards / use the whole stage).
- Also show the picture he explains on (his PROCESS slide: Pre-production / Production / Post-production lists) while he talks.

## 14 animation types
- While he talks about TRADITIONAL the screen shows 2D -> every piece must show the slide/clip of the type he is naming at that moment (use src = a, or the exact slide time: traditional ~579-584, 2D ~587-603, 3D ~603-616, motion graphics ~619-635, stop motion ~635-658). Show the clips he names.

## 15 visual literacy
- Circle: his face small + black empty area (webcam fix, per-piece box).

## 16 composition
- 'طويل على الفاضي' (long and empty) and the OTHER composition types are missing -> cover the rest of the rules from his cheat sheet on screen
  (Photography Composition – the first 10 rules: rule of thirds, leading lines, symmetry, framing, negative space, balance, patterns/repetition,
  fill the frame, depth, colour...) with motion + the example images from the 9-tips video he played (no third-party voice); keep it tight.

## 17 good filmmaker
- He comments on the basketball video but the video itself is missing before it -> show the basketball video he played (~331-347 s) IN FULL (with its own sound) before his comment. Same logic for the BBC World Cup video before his comment on it.

## 18 aspect ratio
- 'حاسه ممل' (boring) -> more motion: e.g. the same film shot re-framed live in 4:3 / 16:9 / 9:16 / 1:1 (what gets cut), old square films vs wide, a phone rotating from landscape to portrait, real platform examples; faster pace, stronger hook.

## 19 animation vs film
- Picture doesn't follow what he says (I used fixed src=509 etc.) -> src = a everywhere (his real screen at that moment) + zoom onto the exact item he names on his drawing (2D, 3D, traditional, motion graphics, stop motion, VFX, film) at the word, with a label.

## 20 camera gear
- Caption + txt: he said 'Camera gear' (not 'كاميرا كير').
- Rushed ('متكروت') -> don't squeeze: keep his full sentences and pauses, include the parts I cut (remote button, track, stabilizer/gimbal, handheld, waterproof case; drone line only with a verified source or as he said it marked weak).
- Show each thing he names correctly at that moment (src = a + zoom on the pictured item; tripod, remote, track/dolly, gimbal, waterproof case).

# Review 2 (2026-11-07) - collect all notes first, execute only after he says he is done

## 04 split diopter
- "انت بوظته": he liked the FIRST version (archive_v2/04_split_diopter = fs_data2 short 4). Go back to it EXACTLY and only ADD the new الجزيرة scene (raw 3458.3-3474.4). Do not change anything else (keep the old hook, crops, scenes). Keep the word-gap cut fix only if it does not change the look.

## 05 cut meaning
- At ~0:25 (the FactCard about Kuleshov): show the experiment VIDEO itself (Mozzhukhin face + soup / coffin / woman). Find a free/public-domain copy (Wikimedia Commons) and show it with the card.

## 06 camera moves
- The tripod is NOT visible in his webcam rectangle (crop cut the left side) -> show the whole webcam width where the tripod is.
- He did NOT ask to put his video OVER the motion: the MoveScene motion must stay visible -> show his webcam rectangle WITH the motion (e.g. in place of / beside the "الكاميرا شايفة كده" preview), not instead of it.
- Do not keep the words "Once upon a time.." (he thinks the clip is La La Land): cut those words; the clip he plays at ~3582-3600 = La La Land (2016)? check, tag accordingly.
- The sentence "انت بتزق الكاميرا.." is said TWICE at the end -> keep it once.
- The last frame (boxing / Raging Bull) is not the best -> pick another dolly-zoom shot from the examples he played (3730-3830).

## 08 two beauties
- Too much text ("محدش هيقرا كل ده") -> PICTURES instead of text lists (real calligraphy, hieroglyphs, posters/frames of الست and الفيل الأزرق, light painting, camera move...).
- "الفيديو مبقاش له اي معنى": better to use the video(s) he gave (his 2 new recordings 20261107_075021 / 075352 — still not found on disk; ask for the path / to put them in input).

## 10 script
- Hook far too long -> short punchy hook (a few seconds).
- Script AND scene TOGETHER on screen all the time (script page/lines + the matching film shot side by side or stacked, like style 20 scene-analysis), not some parts only scene and others only script.

## 12 framing
- No hook: start directly with the topic (drop the hook piece + the rewind label).

## 13 process
- No hook: start directly (drop the hook piece + rewind label).

## 15 visual literacy
- Add the clip where Youssef Chahine talks (course ~1366-1385, "We work with a visual language", with its own sound) and a shot of Martin Scorsese talking (~1416-1461, raw with sound, short).

## 16 composition
- REMOVE short 16 completely (archive the file, do not delete; series becomes 19 -> renumber? ask/keep numbers: move later shorts up or leave a gap — decide: renumber 17-20 to 16-19 and TOTAL 19).
- Keep the order: put a NEW reel in slot 16 instead (no renumbering). Candidate (not used by any other short): his breakdown of the scene from the film "زي النهاردة" (CH28 ~4048-4414 s: jump cuts, over-the-shoulder, fast whip pan, sound effects / clock and fridge sounds, CH29 ~4414-4500).

## 18 aspect ratio
- At the end, while he says YouTube the frame shows the vertical one -> key the ratios on his exact words: "التلفزيون 4:3 / 16:9" ~1171.8-1175.8, "اليوتيوب.. لاند اسكيب" 1186.2 = 16:9, "تقلب بموبايل" 1189.0 = 9:16, "استجرام.. مربع او ريل" 1190.8 = 1:1 then 9:16.

## 19 animation vs film
- No hook.
- "محتاج يتظبط احسن": measure the real positions of each item on his drawing (gridded frame at ~509 s and ~466 s) and zoom exactly on each word as he says it, with a clear label; smoother pace.

## 20 camera gear (and ALL FactCards: 05 too)
- When I put the source card, the picture disappeared (empty stage) -> NEVER remove the picture: keep his screen / the drone picture he showed (~3856-3862 small drone image) in the card, and put the FactCard ON TOP of it (bottom part), not alone.

# Review 3 (2026-11-07)

## 06 camera moves
- "الكاميرا شايفة كده" preview is too small/hidden (his webcam inset pushed it) -> give the preview its room; move the text notes BELOW (empty area under the card).
- The drawn camera motion must follow his REAL move in the webcam (same direction + timing of each tilt/pan he does).
- ~1:21: the La La Land clip shown is a static shot -> show the part where the camera pans left-right (whip pan between them, ~3586-3600).
- End (dolly zoom): the real example video is missing -> show the dolly-zoom film clip at the end too (not only the hook).

## 08 two beauties
- When he says "بيوت شعر": show famous poems / classic verses (calligraphed famous verses).
- Layout: a line splitting LEFT / RIGHT (الشكل vs المحتوى); put the content (pictures/motion) and HIS VIDEO stacked one over the other (use the empty top area, red arrow) — not only a small circle.
- After الأفوكاتو he says سمك لبن تمر هندي -> bring a scene from it (missing).
- When he says الفيل الأزرق -> use a scene from الفيل الأزرق 2.
- I cut too much -> keep his recording (075352) as it was, whole (no big cuts; only tiny breath/silence trims).
- At ~1:44 there is a silence -> no silent gaps.
- Some pictures were unrelated: every picture must match what he says, NO picture used twice, + motion graphics that express his words.
