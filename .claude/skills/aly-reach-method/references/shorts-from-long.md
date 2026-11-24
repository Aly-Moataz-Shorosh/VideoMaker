# Cutting shorts from a long video — the reach method

Use when Aly says «حولي الفيديو ده لشورتس / اطلعلي شورتس من …». Goal: reach (A-type discovery) WITHOUT repeating ourselves.
Rules already in force stay in force (skill `aly-video-motion`, memories): ask ONE or SEVERAL first · ideas come from the video, never a fixed
count · he picks before anything is built · no short ≥ 3:00 · no two shorts with the same hook/content (`check_overlap.py`) · the hook is
never the sentence the short starts with after the rewind · each short self-contained (whole words, whole sentences, complete info) ·
captions only in shorts · CTA / thumbnail + QR rules.

## 1. Mine (from the transcript, never by watching frames)
Read the whole transcript (`transcribe.py` word times). List every candidate moment that can stand alone with ONE promise:
a surprising fact, a mistake + fix, a before/after or demo, a comparison, a strong opinion, a story with a turn, a number, a «secret»,
a funny/emotional reaction, a question people ask, a list/steps, a real result.

## 2. Classify each candidate (one row each)
| field | how |
|---|---|
| النوع | A reach (zero context needed, broad, relatable) · B trust (useful, needs some interest) · C action (proof/offer, points to the full video/course/keyword) |
| الفورمات | the proven shape it fits: 3 أخطاء · X ضد Y · قبل/بعد · هتصدقني لو قلتلك · ترتيب/tier · اللي محدش بيقولهولك · اتعمل ازاي · خرافة ولا حقيقة · حكاية · رقم حقيقي/التكلفة الحقيقية · سؤال وجواب · 101 |
| الوعد | one sentence; can I STACK a 2nd/3rd promise from the same piece (one-up)? |
| الهوك | 3 options (visual first frame + ≤ 6-word text + line), picked by the pause test; taken from LATER in the short, not its first line |
| الإشارة | the signal it should win: full watch / rewatch / share / save / comment (see `scripting.md` Step 0) |
| السكور | Hook, Value, Clarity, Curiosity, Shareability /10 each → /50 |
| موشن % | how much motion graphics it gets (his existing column) |
| الطول | target length (A: 20-60 s; B: 45-120 s; never ≥ 3:00) |
| متغير التجربة | what this short tests (hook type / format / length / CTA / face vs faceless) |

## 3. Choose the set (show Aly a table, wait for his pick)
- Keep only candidates ≥ 35/50. Drop anything that is the same promise/hook as another candidate (overlap check) — merge them instead.
- Mix by his ESMA **55% A / 35% B / 10% C** (awareness is his bottleneck). For 10 shorts ≈ 5-6 A, 3-4 B, 1 C. The C short is usually
  the one that sells the long video (strongest result + thumbnail + QR).
- Group by FORMAT: if one format gives ≥ 5 shorts, name it as a series (series band / numbered title). One-offs are fine for A.
- Present: `# | العنوان | النوع | الفورمات | الهوك المقترح | الإشارة | السكور/50 | موشن % | الطول`, best first, then ask which ones.

## 4. Build each short (the attention game)
- 0-3 s: the visual promise (strongest frame/result, pattern interrupt) + ≤ 6 words on screen + the hook line; then rewind («تعالى
  أوريك …») if the format needs it.
- Body: one point every few seconds, micro-hook every 10-15 s, one-up before the end, zero redundancy, nothing explained twice.
  Editing density like the Homus timelines: no pause/breath left, a change every 1.5-3 s (cut, zoom, label, picture on its word, layout
  change), a «ding»-type sfx on every step label, B-roll/screenshot exactly on the word.
- End: clean exit. Last value → one CTA line → end. If possible the last frame/line loops into the first (rewatch).
- CTA by type: A → a specific comment question / «ابعته لـ…» · B → «احفظه» / follow for the series · C → full video thumbnail + QR /
  Instagram keyword.

## 5. Posting order (the calendar)
Interleave the types (A B A C A B …), never two C in a row; the strongest A first (it tests the hook). Files are numbered in posting
order unless the series is a COURSE (course order) — his existing rule wins. .txt beside each short in his exact format (العناوين: /
الوصف + one #hashtag line / الكومنت المثبت:); the pinned comment carries the comment-CTA question.

## 6. After 10 shorts are live
Run the optimization loop (`optimization.md`, `scripts/reach_batch.py`): ratios, outliers, comment research, 3 hypotheses → the next
batch's test variables. Write what we learned into the feedback log so the next cut starts smarter.

## 7. Shorts from an AI-generated long video (style 27, aiFullVideoCost 2026-11-24)
- Aly: «مش عايز إطار horizontal جوه الـ vertical» — never put the 16:9 frame (or a camera crop of it) inside a 9:16 short when the video
  is motion + generated: RE-LAY OUT the boards natively for 9:16 and REGENERATE the full-frame generated clips in 9:16.
- Pipeline (project `work/scripts/`): `shorts_data.py` (cards + v11 pieces, posting order) → `shorts_cut.py` (word-edge snap; 'raw' keeps
  holds / music / results) → `shorts_vprops.py` (vertical packer: blocks in speaking order → rows → first free gap, hand-over when full,
  cards enlarged up to ×2.2 for the phone, grids scale as one picture, arrows redrawn, SEP parts trimmed, overlap safety net = 0) →
  comp `ai-world-vshort` (`motion-library/src/aiworld/VShort11.tsx`: title band hook → title → CTA, talking circle beside the title,
  word captions with English runs LTR, handles footer) → `shorts_stills.sh N "t…"` → `render_shorts.sh N…` (audio from the final mix,
  -16 LUFS, CRF 23) → `shorts_txt.py`. Full-frame clips: `shorts/vertical_clips.json` maps each 16:9 file to its 9:16 regeneration.
- No new voice is needed for hooks when the line already exists in the long video: cut it from later and play it first.
- Aly's layout notes on the vertical boards (2026-11-24): «2x3 matrix أحسن من الـ overlap الصغير» → 3+ pictures that come together =
  ONE clean matrix, same size (2 columns up to 6, more columns only when needed), never a small picture over others;
  «كبر شوية» → cards up to ×3, text pills ≥ 40-46 px, labels under pictures ≥ 32-36 px, a big group gets its own row.
