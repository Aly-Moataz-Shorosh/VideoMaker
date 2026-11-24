---
name: aly-reach-method
description: "Aly Shorosh's reach method for scripts and shorts, learned from his Homus content course (references/Homus, studied 2026-11-24): the funnel A/B/C (reach/trust/action) with his split 55/35/10, engagement signals (full watch, rewatch, share, save, comment), proven formats + series, hook = promise (visual > text > verbal, bad/better/best ladder, pause test), body keep/one-up/new promise, 22 scripting techniques, pre-post score /50, clean exit, CTA templates, and the optimization loop after every 10 posts (ratios, outliers, comments, hypotheses). Use it whenever Aly asks to write or improve a script (سكريبت، هوك، فيديو طويل، شورت، ريل), to cut shorts from a long video (حولي الفيديو لشورتس، اطلع شورتس), to script AND generate an AI video (style 27 / avatar / twin / HeyGen), to plan ideas, series or a posting calendar, or to analyse how his posted videos performed (ريتش، مشاهدات، تحليل، reach, views) — even if he doesn't say Homus."
---

# Aly's reach method (Homus, adapted to Aly)

Talk to Aly in simple Egyptian Arabic, short, step by step. This skill adds REACH to his existing rules; it never overrides them.
His voice, shows, sourcing and feedback live in the content skill
(`E:/root/output/_claude/Aly Shorosh - Content Creator/.claude/skills/aly-content-assistant/`); video production rules live in
`aly-video-motion` + video-maker `docs/`. When they conflict, Aly's own past feedback wins.

## The model in 10 lines (details: `references/method.md`)
1. Not every video is for views: **views ≠ sales**. Viewer wants stimulation, creator wants money, platform wants session time — serve all 3.
2. Platforms test a video on a small batch and push it if it passes; the heaviest signals (course model) are **rewatch > full watch >
   share > comment > like**. Build for finished watches and rewatches first, shares second.
3. **Watch decision ≠ buy decision** → a mix of 3 types: **A** reach (strangers, zero context, fast) · **B** trust (useful, how-to,
   behind the scenes, tests) · **C** action (proof + the full video / course / keyword / services).
4. **Aly's split now = 55% A / 35% B / 10% C** (his Homus report: awareness is the bottleneck, health 31/100). Re-decide quarterly.
5. Performance (course model) = idea 40% + script 40% + production 20% → ~75% of the work happens before filming/generating.
6. Don't chase new ideas: take **proven FORMATS** (format ≠ topic), make them his, and turn every good format into a **series** (5-10 eps).
7. Script = **hook grabs, body keeps, CTA directs**. Hook = a PROMISE (explicit or implicit); **visual > text > verbal**.
8. Body: **keep / one-up / new promise**; pacing, zero redundancy, constant stimulation; micro-hook every 10-15 s; clean exit.
9. After every ~10 posts: **ratios > numbers**, outliers, comment research, 3 hypotheses, next 10 videos each testing ONE variable.
10. «رأيك في طز» — taste doesn't decide, tests do. Repeat formats; never repeat content or hooks.

## Route the job
| Aly asks for | Do |
|---|---|
| A script (short or long), hooks, improve his notes | `references/scripting.md` + `references/techniques.md` (+ his voice from the content skill) |
| Shorts from a long video | `references/shorts-from-long.md` (with aly-video-motion's shorts rules) |
| Script AND generate a video with AI (style 27, twin, vertical AI short) | `references/ai-video.md` → then video-maker docs/33, 36, 37 |
| Ideas, series, reference research, weekly/monthly plan | `references/ideation-and-calendar.md` |
| «الفيديوهات عملت كام / ليه ده جاب وده لأ / حلل» | `references/optimization.md` + `scripts/reach_batch.py` |
| What exactly the course said | `references/method.md` (full digest; the original files are in video-maker `references/Homus/`) |

## Non-negotiables (his rules + the method)
- Every script starts with the **card**: type A/B/C · format · series · idea in one sentence · promise · target signal · test variable.
- 3 hooks on the bad → better → best ladder, each with its FIRST FRAME and ≤ 6 words on screen; pause test; he picks.
- One video = one promise (stack 2-3 promises inside the hook, but ONE video topic). A second topic = another episode.
- Hooks and titles are bold but TRUE; every fact follows his sourcing rules; real numbers or none (no invented specificity).
- Pre-post score /50 (hook, value, clarity, curiosity, shareability) shown before production; < 35 → rework first.
- Shorts: ask one or several first; he picks from a table before anything is built; never ≥ 3:00; no repeated hook/content
  (`check_overlap.py`); the hook is never the short's own first line; CTA by type.
- Paid generation (HeyGen / ElevenLabs / Higgsfield): script locked + credit cost said BEFORE generating; wait for «نفذ».
- History / tech / design topics never packaged as a definition or «تاريخ الـ…»: attach them to a decision, an identity («احنا»),
  a mistake, a surprise or a transformation (definitions were the losers in every worked case).

## Output defaults
- Script → the card, 3 hooks (ladder), the beats with `==مرئي==`, `[ميكرو هوك]`, `[إثبات]`, `[لوب مفتوح]/[لوب مقفول]`, CTA, score /50,
  and (for long videos) the shorts list. Arabic, his notation, keywords/beats unless he wants a full spoken script (AI twin = full lines).
- Shorts plan → one table: # · title · type · format · hook · signal · score/50 · motion % · length; best first; then WAIT.
- Analysis → the reach_batch report + patterns, comment research, 3 hypotheses, next-10 table.

## Learning
When Aly reacts to a script, a short or real numbers, write the lesson in one line, apply it, and add durable ones to the content skill's
`feedback-log.md`. If the method itself changes (new Homus episode, e.g. M2 EP4 filming/editing), update `references/method.md`.
Master copy of this skill = video-maker `.claude/skills/aly-reach-method/` (git). Copies: Content Creator `.claude/skills/` and
`claude-code-setup/skills/` (+ zip for claude.ai) — update all after a change.
