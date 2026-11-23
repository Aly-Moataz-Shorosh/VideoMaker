import React from 'react';
import {Composition} from 'remotion';
import {MatchReel, matchReelSchema} from './match/MatchReel';
import {registry} from './registry';
import {Edit, editSchema} from './Edit';
import {FilmShort, filmShortSchema} from './film/FilmShort';
import {Course, courseSchema} from './course/Course';
import {CourseShort, courseShortSchema} from './course/Short';
import {StageShort, stageShortSchema} from './stage/StageShort';
import {UthReel, uthReelSchema} from './uth/UthReel';
import {MeetShort, meetShortSchema} from './enta/MeetShort';
import {SceneAnalysis, sceneAnalysisSchema} from './scene/SceneAnalysis';
import {AiWorldRough, aiWorldSchema, AiHud, aiHudSchema} from './aiworld/AiWorld';
import {AiWorldV3, aiV3Schema} from './aiworld/V3';
import {AiWorldV4, aiV4Schema} from './aiworld/V4';
import {AiWorldV5, aiV5Schema} from './aiworld/V5';
import {AiWorldV6, aiV6Schema} from './aiworld/V6';
import {AiWorldV7, aiV7Schema} from './aiworld/V7';
import {AiWorldV8, aiV8Schema, HandlesLayer} from './aiworld/V8';
import {AiWorldV9, aiV9Schema, HandlesLayer9} from './aiworld/V9';

// Every template: 16:9 composition `<id-with-dashes>` and, when v, 9:16 `<id>-v`.
export const Root: React.FC = () => (
  <>
    {Object.entries(registry).flatMap(([id, t]) => {
      const name = id.replace(/_/g, '-');
      const formats = [{s: '', w: 1920, h: 1080}, ...(t.v ? [{s: '-v', w: 1080, h: 1920}] : [])];
      return formats.map((f) => (
        <Composition key={name + f.s} id={name + f.s} component={t.C} schema={t.schema as any}
          defaultProps={t.schema.parse({}) as any} durationInFrames={t.frames} fps={30} width={f.w} height={f.h} />
      ));
    })}
    {/* Whole edit: duration from edit.json. edit-v = 9:16 (shorts), footage reframed around Aly. */}
    {[{id: 'edit', w: 1920, h: 1080}, {id: 'edit-v', w: 1080, h: 1920}].map((c) => (
      <Composition key={c.id} id={c.id} component={Edit} schema={editSchema} defaultProps={editSchema.parse({})}
        fps={30} width={c.w} height={c.h} durationInFrames={90}
        calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * props.fps))})} />
    ))}
    {/* Faceless-first film shorts (theodesy): props from projects/<code>/work/scripts/make_shorts.py */}
    <Composition id="film-short" component={FilmShort} schema={filmShortSchema} defaultProps={filmShortSchema.parse({})}
      fps={30} width={1080} height={1920} durationInFrames={90}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * props.fps))})} />
    {/* Long course (premiere pro course 2026-10-16): 16:9, 25 fps like his recordings. Props from make_course.py */}
    <Composition id="course" component={Course} schema={courseSchema} defaultProps={courseSchema.parse({})}
      fps={25} width={1920} height={1080} durationInFrames={90}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * props.fps)), fps: props.fps})} />
    {/* Vertical shorts series from the course (2026-10-18). Props from make_shorts.py */}
    <Composition id="course-short" component={CourseShort} schema={courseShortSchema} defaultProps={courseShortSchema.parse({})}
      fps={30} width={1080} height={1920} durationInFrames={90}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * props.fps)), fps: props.fps})} />
    {/* New Stage 19 lecture shorts (2026-10-18). Props from projects/<code>/work/scripts/make_short.py */}
    {/* Garrett Warren talk @ UTH Festival 2026 (2026-11-22). Props from projects/<code>/work/scripts/make_props.py */}
    <Composition id="uth-reel" component={UthReel} schema={uthReelSchema} defaultProps={uthReelSchema.parse({})}
      fps={30} width={1080} height={1920} durationInFrames={90}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * 30))})} />
    <Composition id="stage-short" component={StageShort} schema={stageShortSchema} defaultProps={stageShortSchema.parse({})}
      fps={30} width={1080} height={1920} durationInFrames={90}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * 30))})} />
    <Composition id="meet-short" component={MeetShort} schema={meetShortSchema} defaultProps={meetShortSchema.parse({})}
      fps={30} width={1080} height={1920} durationInFrames={90}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * 30))})} />
    {/* Live Playmobil match reel (2026-11-01). Props from projects/<code>/work/scripts/make_props.py */}
    <Composition id="match-reel" component={MatchReel} schema={matchReelSchema} defaultProps={matchReelSchema.parse({})}
      fps={30} width={1080} height={1920} durationInFrames={90}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * 30))})} />
    {/* Film scene analysis 16:9 (Ibrahim El Abyad 2026-11-06). Props from projects/<code>/work/scripts/make_props.py */}
    <Composition id="scene-analysis" component={SceneAnalysis} schema={sceneAnalysisSchema} defaultProps={sceneAnalysisSchema.parse({})}
      fps={30} width={1920} height={1080} durationInFrames={90}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * 30))})} />
    {/* «عالم الـ AI كله» 16:9 rough cut + transparent HUD layers (2026-11-20). Props from projects/<code>/work/scripts/make_props.py */}
    <Composition id="ai-world-rough" component={AiWorldRough} schema={aiWorldSchema} defaultProps={aiWorldSchema.parse({})}
      fps={25} width={1920} height={1080} durationInFrames={250}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * props.fps)), fps: props.fps,
        width: props.outW, height: Math.round(props.outW * 9 / 16)})} />
    {/* rough cut v3: one visual per sentence (Aly's 22 notes 2026-11-21). Props from projects/<code>/work/scripts/make_props_v3.py */}
    <Composition id="ai-world-v3" component={AiWorldV3} schema={aiV3Schema} defaultProps={aiV3Schema.parse({})}
      fps={25} width={1920} height={1080} durationInFrames={250}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * props.fps)), fps: props.fps,
        width: props.outW, height: Math.round(props.outW * 9 / 16)})} />
    {/* rough cut v6: Aly's 50 notes on v5 (2026-11-22) — new order, tree-map separators. Props: make_props_v6.py */}
    {/* rough cut v9: Aly's v8 notes (2026-11-23): kids on the separators, 6 lip-synced looks, handles bottom-left. Props: make_props_v9.py */}
    <Composition id="ai-world-v9" component={AiWorldV9} schema={aiV9Schema} defaultProps={aiV9Schema.parse({})}
      fps={25} width={1920} height={1080} durationInFrames={250}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * props.fps)), fps: props.fps,
        width: props.outW, height: Math.round(props.outW * 9 / 16)})} />
    <Composition id="ai-world-v9-handles" component={HandlesLayer9} defaultProps={{outW: 1920, duration: 10}}
      fps={25} width={1920} height={1080} durationInFrames={250}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * 25))})} />
    {/* rough cut v8: Aly's 55 notes on v7 (2026-11-23). Props: make_props_v8.py. + the handles layer alone (transparent) for his Premiere project */}
    <Composition id="ai-world-v8" component={AiWorldV8} schema={aiV8Schema} defaultProps={aiV8Schema.parse({})}
      fps={25} width={1920} height={1080} durationInFrames={250}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * props.fps)), fps: props.fps,
        width: props.outW, height: Math.round(props.outW * 9 / 16)})} />
    <Composition id="ai-world-v8-handles" component={HandlesLayer} defaultProps={{outW: 1920, duration: 10}}
      fps={25} width={1920} height={1080} durationInFrames={250}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * 25))})} />
    {/* rough cut v7: Aly's notes on v6 (2026-11-23): faces back, held boards, tree spacing, song logos. Props: make_props_v7.py */}
    <Composition id="ai-world-v7" component={AiWorldV7} schema={aiV7Schema} defaultProps={aiV7Schema.parse({})}
      fps={25} width={1920} height={1080} durationInFrames={250}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * props.fps)), fps: props.fps,
        width: props.outW, height: Math.round(props.outW * 9 / 16)})} />
    <Composition id="ai-world-v6" component={AiWorldV6} schema={aiV6Schema} defaultProps={aiV6Schema.parse({})}
      fps={25} width={1920} height={1080} durationInFrames={250}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * props.fps)), fps: props.fps,
        width: props.outW, height: Math.round(props.outW * 9 / 16)})} />
    {/* rough cut v5: Aly's v4 notes (2026-11-22) — explaining diagrams, one background, full-frame glitch, safe area. Props: make_props_v5.py */}
    <Composition id="ai-world-v5" component={AiWorldV5} schema={aiV5Schema} defaultProps={aiV5Schema.parse({})}
      fps={25} width={1920} height={1080} durationInFrames={250}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * props.fps)), fps: props.fps,
        width: props.outW, height: Math.round(props.outW * 9 / 16)})} />
    {/* rough cut v4: built on the «انت بتشتغل ايه» kit (Aly's v3 notes 2026-11-22). Props from projects/<code>/work/scripts/make_props_v4.py */}
    <Composition id="ai-world-v4" component={AiWorldV4} schema={aiV4Schema} defaultProps={aiV4Schema.parse({})}
      fps={25} width={1920} height={1080} durationInFrames={250}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * props.fps)), fps: props.fps,
        width: props.outW, height: Math.round(props.outW * 9 / 16)})} />
    <Composition id="ai-world-hud" component={AiHud} schema={aiHudSchema} defaultProps={aiHudSchema.parse({})}
      fps={25} width={1920} height={1080} durationInFrames={125}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * 25))})} />
  </>
);
