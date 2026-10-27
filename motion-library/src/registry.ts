import React from 'react';
import {z} from 'zod';
import {KeywordPop, keywordPopSchema} from './templates/KeywordPop';
import {SidePicture, sidePictureSchema} from './templates/SidePicture';
import {SubscribePress, subscribePressSchema} from './templates/SubscribePress';
import {Captions, captionsSchema} from './templates/Captions';
import {PortalWorld, portalWorldSchema} from './templates/PortalWorld';
import {Counter, counterSchema} from './templates/Counter';
import {BarChart, barChartSchema} from './templates/BarChart';
import {StepsList, stepsListSchema} from './templates/StepsList';
import {IconPop, iconPopSchema} from './templates/IconPop';
import {SectionTransition, sectionTransitionSchema} from './templates/SectionTransition';
import {CtaEndcard, ctaEndcardSchema} from './templates/CtaEndcard';
import {BrandClip, brandClipSchema} from './templates/BrandClip';
import {ScreenUi, screenUiSchema} from './templates/ScreenUi';
import {CommentCta, commentCtaSchema} from './templates/CommentCta';
import {ThresholdWave, thresholdWaveSchema} from './templates/ThresholdWave';
import {TrimHandles, trimHandlesSchema} from './templates/TrimHandles';
import {AudioCrossfade, audioCrossfadeSchema} from './templates/AudioCrossfade';
import {GreenClip, greenClipSchema} from './templates/GreenClip';
import {EgyptCrowd, egyptCrowdSchema} from './templates/EgyptCrowd';
import {JudgeScene, judgeSceneSchema} from './templates/JudgeScene';
import {LogoFlow, logoFlowSchema} from './templates/LogoFlow';
import {SameWord, sameWordSchema} from './templates/SameWord';
import {CreditsDrain, creditsDrainSchema} from './templates/CreditsDrain';
import {PhoneTour, phoneTourSchema} from './templates/PhoneTour';
import {EntaTerm, entaTermSchema} from './enta/EntaTerm';
import {EntaPhotos, entaPhotosSchema} from './enta/EntaPhotos';
import {EntaStickers, entaStickersSchema, EntaBubble, entaBubbleSchema, EntaName, entaNameSchema, EntaGlitch, entaGlitchSchema, EntaLeak, entaLeakSchema, EntaNote, entaNoteSchema} from './enta/EntaPop';
import {EntaPipeline, entaPipelineSchema, EntaClash, entaClashSchema, EntaDeadEnd, entaDeadEndSchema} from './enta/Board';
import {EntaRender, entaRenderSchema, EntaMerge, entaMergeSchema} from './enta/Board2';
import {EntaFlavours, entaFlavoursSchema, EntaDrawer, entaDrawerSchema} from './enta/Board3';
import {BizOpen, bizOpenSchema} from './enta/BizOpen';
import {BizFree, bizFreeSchema} from './enta/BoardBiz';
import {QaWhat, qaWhatSchema, QaReq, qaReqSchema, QaEyes, qaEyesSchema, QaTypes, qaTypesSchema, QaLogin, qaLoginSchema, QaApi, qaApiSchema, QaPerf, qaPerfSchema, QaRoad, qaRoadSchema, QaJoker, qaJokerSchema, QaIstqb, qaIstqbSchema, QaAi, qaAiSchema, QaProd, qaProdSchema, QaDemand, qaDemandSchema} from './enta/BoardQA';

// Single list of templates: id (= catalog id) -> component, schema, preview length, has 9:16.
export type Entry = {C: React.FC<any>; schema: z.ZodTypeAny; frames: number; v: boolean};
export const registry: Record<string, Entry> = {
  keyword_pop: {C: KeywordPop, schema: keywordPopSchema, frames: 75, v: true},
  side_picture: {C: SidePicture, schema: sidePictureSchema, frames: 120, v: true},
  subscribe_press: {C: SubscribePress, schema: subscribePressSchema, frames: 120, v: true},
  captions: {C: Captions, schema: captionsSchema, frames: 90, v: true},
  portal_world: {C: PortalWorld, schema: portalWorldSchema, frames: 90, v: false},
  counter: {C: Counter, schema: counterSchema, frames: 90, v: true},
  bar_chart: {C: BarChart, schema: barChartSchema, frames: 120, v: true},
  steps_list: {C: StepsList, schema: stepsListSchema, frames: 120, v: true},
  icon_pop: {C: IconPop, schema: iconPopSchema, frames: 45, v: true},
  section_transition: {C: SectionTransition, schema: sectionTransitionSchema, frames: 90, v: false},
  cta_endcard: {C: CtaEndcard, schema: ctaEndcardSchema, frames: 120, v: true},
  brand_clip: {C: BrandClip, schema: brandClipSchema, frames: 60, v: false},
  screen_ui: {C: ScreenUi, schema: screenUiSchema, frames: 120, v: true},
  comment_cta: {C: CommentCta, schema: commentCtaSchema, frames: 120, v: true},
  threshold_wave: {C: ThresholdWave, schema: thresholdWaveSchema, frames: 210, v: true},
  trim_handles: {C: TrimHandles, schema: trimHandlesSchema, frames: 180, v: true},
  audio_crossfade: {C: AudioCrossfade, schema: audioCrossfadeSchema, frames: 180, v: true},
  green_clip: {C: GreenClip, schema: greenClipSchema, frames: 240, v: false},
  egypt_crowd: {C: EgyptCrowd, schema: egyptCrowdSchema, frames: 300, v: false},
  judge_scene: {C: JudgeScene, schema: judgeSceneSchema, frames: 640, v: false},
  logo_flow: {C: LogoFlow, schema: logoFlowSchema, frames: 120, v: false},
  same_word: {C: SameWord, schema: sameWordSchema, frames: 120, v: false},
  credits_drain: {C: CreditsDrain, schema: creditsDrainSchema, frames: 160, v: false},
  phone_tour: {C: PhoneTour, schema: phoneTourSchema, frames: 300, v: true},
  // show "انت بتشتغل ايه" (docs/22)
  enta_term: {C: EntaTerm, schema: entaTermSchema, frames: 150, v: false},
  enta_photos: {C: EntaPhotos, schema: entaPhotosSchema, frames: 120, v: false},
  enta_stickers: {C: EntaStickers, schema: entaStickersSchema, frames: 60, v: false},
  enta_bubble: {C: EntaBubble, schema: entaBubbleSchema, frames: 75, v: false},
  enta_name: {C: EntaName, schema: entaNameSchema, frames: 150, v: false},
  enta_glitch: {C: EntaGlitch, schema: entaGlitchSchema, frames: 8, v: false},
  enta_leak: {C: EntaLeak, schema: entaLeakSchema, frames: 40, v: false},
  enta_note: {C: EntaNote, schema: entaNoteSchema, frames: 120, v: false},
  enta_pipeline: {C: EntaPipeline, schema: entaPipelineSchema, frames: 200, v: false},
  enta_clash: {C: EntaClash, schema: entaClashSchema, frames: 200, v: false},
  enta_deadend: {C: EntaDeadEnd, schema: entaDeadEndSchema, frames: 200, v: false},
  enta_render: {C: EntaRender, schema: entaRenderSchema, frames: 260, v: false},
  enta_merge: {C: EntaMerge, schema: entaMergeSchema, frames: 220, v: false},
  enta_flavours: {C: EntaFlavours, schema: entaFlavoursSchema, frames: 160, v: false},
  enta_drawer: {C: EntaDrawer, schema: entaDrawerSchema, frames: 240, v: false},
  biz_free: {C: BizFree, schema: bizFreeSchema, frames: 300, v: false},
  biz_open: {C: BizOpen, schema: bizOpenSchema, frames: 300, v: false},
  qa_what: {C: QaWhat, schema: qaWhatSchema, frames: 240, v: false},
  qa_req: {C: QaReq, schema: qaReqSchema, frames: 240, v: false},
  qa_eyes: {C: QaEyes, schema: qaEyesSchema, frames: 240, v: false},
  qa_types: {C: QaTypes, schema: qaTypesSchema, frames: 240, v: false},
  qa_login: {C: QaLogin, schema: qaLoginSchema, frames: 420, v: false},
  qa_api: {C: QaApi, schema: qaApiSchema, frames: 260, v: false},
  qa_perf: {C: QaPerf, schema: qaPerfSchema, frames: 200, v: false},
  qa_road: {C: QaRoad, schema: qaRoadSchema, frames: 300, v: false},
  qa_joker: {C: QaJoker, schema: qaJokerSchema, frames: 300, v: false},
  qa_istqb: {C: QaIstqb, schema: qaIstqbSchema, frames: 300, v: false},
  qa_ai: {C: QaAi, schema: qaAiSchema, frames: 300, v: false},
  qa_prod: {C: QaProd, schema: qaProdSchema, frames: 260, v: false},
  qa_demand: {C: QaDemand, schema: qaDemandSchema, frames: 200, v: false},
};
