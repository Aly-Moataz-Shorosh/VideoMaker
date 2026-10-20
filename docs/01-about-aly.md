# About Aly (project context)

- Aly Shorosh, content creator from Cairo, Egypt. CS graduate, works as software quality control.
- Big professional experience in graphics, media and video production (Premiere, After Effects, DaVinci).
- Interests/topics: geography, history, religion, sports, self-development, relationships, philosophy,
  general knowledge, explainers.
- Goal: publish a new long video every Friday; grow the formal public accounts to earn from content.

## Public accounts
- YouTube (main): https://www.youtube.com/@AlyShorosh (gmail: alyshorosh@gmail.com)
- Instagram: https://www.instagram.com/alyshorosh
- Facebook (profile in Professional mode, not a page): https://www.facebook.com/aly.shorosh/
- TikTok: https://www.tiktok.com/@alyshorosh
- LinkedIn: https://www.linkedin.com/in/shorosh/
- Behance: http://be.net/shorosh
- Personal (background only): https://www.facebook.com/aly.moataz.3 , https://www.youtube.com/@aloka1997

## His PC
- CPU: Intel i9-10850K (10 cores / 20 threads) — strong, does most of the work.
- RAM: 32 GB.
- GPU: GTX 1050 Ti (4 GB) — weak for AI. Consequences:
  - No local LLM (Ollama etc.) — not practical.
  - Speech-to-text (faster-whisper) runs on CPU (int8). Roughly video length or more; fine unattended.
  - Remotion renders on CPU (headless Chrome) — fine with this CPU.

## Existing automations (same style to follow; READ ONLY, never modify)
Root: `E:\root\output\_claude\Aly Shorosh - Content Creator\automations\`
- `reels-publisher\` — Python + SQLite + local dashboard (127.0.0.1:8770). Schedules Reels/Shorts on
  YouTube, Instagram, Facebook, TikTok via each site's own scheduler (Playwright + dedicated Chrome).
  Reels live in numbered folders `01_Ready\R0012` → `02_Archive`. Future link: Shorts cut from long
  videos can be dropped here.
- `instagram-comment-dm\` — Python + SQLite + dashboard (127.0.0.1:8765). Comment keyword → public
  reply + DM, hourly via Task Scheduler.
Shared style: Python + SQLite + small local dashboard, numbered folders, free only, simple code,
Aly reviews in a calm UI.

## Locations
- Suggested home of this project: `E:\root\output\_claude\Aly Shorosh - Content Creator\automations\video-maker\`
- Earlier Codex attempt (read only): `E:\root\output\Youtube\Aly Shorosh New\_Ai Video Maker`
