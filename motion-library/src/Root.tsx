import React from 'react';
import {Composition} from 'remotion';
import {registry} from './registry';
import {Edit, editSchema} from './Edit';
import {FilmShort, filmShortSchema} from './film/FilmShort';
import {Course, courseSchema} from './course/Course';
import {CourseShort, courseShortSchema} from './course/Short';
import {StageShort, stageShortSchema} from './stage/StageShort';
import {MeetShort, meetShortSchema} from './enta/MeetShort';

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
    <Composition id="stage-short" component={StageShort} schema={stageShortSchema} defaultProps={stageShortSchema.parse({})}
      fps={30} width={1080} height={1920} durationInFrames={90}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * 30))})} />
    <Composition id="meet-short" component={MeetShort} schema={meetShortSchema} defaultProps={meetShortSchema.parse({})}
      fps={30} width={1080} height={1920} durationInFrames={90}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.duration * 30))})} />
  </>
);
