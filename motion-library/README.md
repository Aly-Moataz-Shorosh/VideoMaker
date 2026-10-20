Remotion motion library. `catalog.json` = single source of truth (see docs/05).
Identity rules: docs/11-brand-identity.md. Theme numbers: src/theme.json (copy of brand/theme.json).

- Preview in browser: `npm run studio`
- One still: `npx remotion still keyword-pop out/x.png --frame=40 --props='{"text":"..."}'`
- Overlay with alpha for Premiere: `npx remotion render side-picture out/x.mov --codec=prores --prores-profile=4444 --props=...`
- `previewBg` prop = test background only (Aly frame); leave empty for real overlays.
- Blocks: src/blocks (theme, anim, Base/Highlight). Templates: src/templates. Register in src/Root.tsx.
- Check a render without a video: `node stills.mjs edit-v <edit.json> <sheet.png> <frame> [<frame>...]` (one contact sheet).
- Premiere overlays for a whole edit (bundles once): `node overlays.mjs <comp> <props.json> <jobs.json>` — called by
  `tools/build_edit.py --overlays`.
- Templates added 2026-10-06 (recipe + props: docs/16-recipe-tutorial-short.md): `screen_ui`, `comment_cta`,
  `threshold_wave`, `trim_handles`, `audio_crossfade`. Explainer diagrams take phase frames (…At) from the plan.
