# Decisions (settled — don't re-argue unless Aly asks)

1. **AI decides, programs execute.** Claude only reads TEXT (transcript, JSON) and outputs small JSON
   decisions. Cutting, fetching images, rendering motion, building the timeline = free local programs.
2. **No step-by-step app control by AI per video** (e.g. driving After Effects through MCP for every
   video). Too many tokens and slow. AI may help BUILD templates once; filling them is automatic.
3. **Roles:** PC programs = execution. Claude = thinking (which sentences to cut, where visuals go, which
   motion + its text). Aly = reviews decisions in a simple page + final polish in Premiere.
4. **One LLM call per video** for the edit plan (input ~6–10k tokens for a 10–15 min video).
5. **LLM runs through Claude Code on Aly's existing subscription** (no extra cost). Gemini free tier is a
   fallback (rate limits; free-tier data may be used by Google). No local LLM (GPU too weak).
6. **Motion library engine: Remotion first, After Effects second.**
   - Remotion = motion written as code (React/TypeScript). Claude Code reads/writes/fixes it as plain
     text, data goes in as JSON props, renders from the command line, checked with one still PNG.
     Cheapest in tokens, consistent, good Arabic/RTL text via browser fonts. Free for individuals
     (re-check license terms if a company of >3 people ever uses it).
   - After Effects = .aep files are binary; AI can't read/edit them as text → expensive to create/modify
     by AI. Use AE only for special heavy-effect pieces Aly designs himself (can be data-filled later
     with nexrender, free/open-source).
   - Output for Premiere: transparent overlays as ProRes 4444 with alpha (.mov); full-screen pieces as
     normal video. Same templates must support 16:9 and 9:16.
7. **Arabic text costs more tokens than English** → docs/code/catalog in English; Aly-facing files
   (questions, UI text) in Arabic.
8. Speech-to-text: faster-whisper on CPU (int8), word timestamps. Runs unattended.
9. Green-screen stock elements: key once with FFmpeg → save with alpha in the library (no keying per video).
10. Build in phases; each phase useful on its own (`04-pipeline-plan.md`). Current focus: motion library.
