"""Rough cut v3 PLAN (Aly's 22 notes, review_rough_v2_notes.md): one visual per sentence, from the words themselves.
Each scene starts at a sentence id ("at") or at an avatar clip window ("av": shot n, the clip shows him saying exactly
those words). A scene ends where the next one starts. Kinds (motion = Remotion, full frame, NO boxed cards, NO captions):
  AV    his avatar clip (generated studio, note 2) + motion BESIDE him (chips/logos/numbers on the word, never on his face)
  CLIP  a generated clip (Higgsfield id) on the sentence that talks about what is in it + label chip beside
  MAP6  the jet = the 6 families, shown ONCE, then a small HUD that lights the current part (note 6)
  LOGOS logos pop ON their words (auto from the text, note 8)
  KT    kinetic text: the key phrase types in, gold pill on the key word (glass look, style 10)
  WEB   real screenshot of the official page (research/evidence_shots_v1, marked) in a browser frame, zoom on the marked line
  NUM   a number counts up on its word
  VID   his real YouTube video: thumbnail + QR (+ a few seconds of it) (note 10)
  ICON  Fluent 3D icons for generic things, one per word
  FLOW  a chain of real pictures with Arabic arrows (←)
  SPLIT two real sides (before/after, A vs B)
  BTS   behind the scenes of OUR making (real files: keyframes, face tests, prompts, Blender blockout)
  LYR   song line in big kinetic type on the beat over the clip of THAT line (note 18/19)
  STEP  tutorial step: big step number + the real screen/command of that step
"""
P = [
 # ---------------- C00 hook ----------------
 dict(av=1, k="AV", d="علي في الستوديو المتولّد (ملاحظة 2). على «الوش ده / الصوت ده / المكان ده» 3 علامات تطلع جنبه، وعلى «المكان» الستوديو يتفكك نقط لثانية ويرجع"),
 dict(at="S001.5", k="BTS", d="من ورا الكواليس: البرومبت بيتكتب ← صورة الستوديو بتطلع ← بتتحرك فيديو، وتحتها «AI بإشراف علي شُرُش» مرة واحدة بس (ملاحظة 20)"),
 dict(at="S002.1", k="NUM", d="جدول القناة: آخر فيديو من 3 سنين، والسنين بتعدي فاضية (0 فيديو)"),
 dict(at="S002.2", k="NUM", d="«28» يطلع مع كلمة «ثمانية وعشرين» بالظبط (ملاحظة 1)، وعلى «أربع منصات» لوجوهات يوتيوب/إنستجرام/فيسبوك/تيك توك بأسماء حساباتك + سكرين إحصائيات فيسبوك (ملاحظة 4)"),
 dict(av=4, k="AV", d="«إزاي؟ ده اللي هنشوفه» علي بيتكلم + علامة استفهام تطلع جنبه"),
 dict(at="S002.5", k="CLIP", d="لمحة سريعة: «عالم الـ AI كله» = 3 كليبات من العوالم (الطيارة، المعمل، الكوبري)، «خطوة خطوة» = أرقام خطوات، «أغنية» = إيد على حيطة الكهف + سطر من الأغنية بالدهبي (ملاحظة 5)", clip=[6, 102, 903, 186]),
 # ---------------- C01 the jet = 6 families ----------------
 dict(at="S003.1", k="CLIP", d="«طيارة حربية» = الكاميرا داخلة على القمرة (dolly)", clip=[6]),
 dict(at="S003.2", k="CLIP", d="الطيارة متركّبة، وقطعة بتطلع منها فتنوّر أحمر = «لو قطعة ناقصة مش هتطير»", clip=[901]),
 dict(at="S003.3", k="MAP6", d="الطيارة رسمة موشن متفككة 6 قطع: كل قطعة تنوّر واسمها يطلع على كلمتها (التوليد، LLMs/agents، السكريبتات، MCP، skills، الإنسان)، وعلى «صور وفيديو وصوت ومزيكا وثري دي» 5 أيقونات تطلع جوه قطعة التوليد. الخريطة دي بتتعرض مرة واحدة بس"),
 dict(at="S004.7", k="CLIP", d="«نفك الطيارة قطعة قطعة» = علي في القمرة والقطع الست بتلف حواليه", clip=[9]),
 # ---------------- C02 generation ----------------
 dict(av=12, k="AV", d="الخريطة الصغيرة فوق: قطعة 1 «التوليد» تنوّر. علي بيقول القاعدة، وجنبه 3 خانات تطلع على كلماتها: موديل ≠ أداة ≠ workflow، وتحت «موديل» لوجوهات Seedance / Kling / Veo على أساميها"),
 dict(at="S005.4", k="WEB", d="«الأداة هي الموقع»: متصفح فيه صفحة Higgsfield الحقيقية وبعدها HeyGen، والموديل chip صغيرة جوه المتصفح"),
 dict(at="S005.5", k="FLOW", d="الـ workflow بحاجاتنا الحقيقية: صورة (keyframe) ← فيديو (الكليب بتاعها) ← صوت (موجة صوتك)"),
 dict(av=15, k="AV", d="«الموديل بيرسم إزاي؟ اتدرب على ملايين الأمثلة» + جنبه شبكة صور صغيرة كتير بتتملا وعداد «ملايين»"),
 dict(at="S006.3", k="BTS", d="diffusion حقيقي: دوشة نقط ← صورة الطيارة بتاعتنا خطوة خطوة (عداد الخطوات)"),
 dict(at="S006.4", k="KT", d="3 أسئلة تطلع على كلماتها مع أيقونة لكل سؤال: إيه الموديل؟ / إيه الـ input؟ / إيه الـ workflow؟"),
 dict(av=18, k="VID", d="علي بيقول «عندي فيديو كامل…» وجنبه ثمبنيل «عايز تبدأ تعمل فيديوهات AI؟» + QR (youtu.be/H5oOZypINf0)", vid="H5oOZypINf0"),
 # C02a images
 dict(at="S007.1", k="CLIP", d="«الصور» = صور بتتولد وتطير حواليه", clip=[19]),
 dict(at="S007.2", k="SPLIT", d="نوعين: «كلام مكتوب يبقى صورة» = برومبت بيتكتب ← صورة / «صورة تبقى صورة» = صورة ← صورة متعدلة (keyframes بتوعنا)"),
 dict(at="S007.4", k="CLIP", d="4 تعديلات كل واحد ينوّر على كلمته: غيّر الخلفية / امسح حاجة / كمّل برا الكادر / ستايل تاني", clip=[25]),
 dict(at="S007.5", k="LOGOS", d="Nano Banana / GPT Image / Seedream / Higgsfield على أساميهم"),
 dict(at="S008.1", k="BTS", d="«الشخصية تفضل هي هي»: تستات وشّك الحقيقية من الفيديو ده (من غير دقن ← شعر ← الأوضة ← الـ character sheet) جنب بعض"),
 dict(at="S008.3", k="ICON", d="الحلول على كلماتها: Soul ID (لوجو Higgsfield) / صور مرجع / LoRA"),
 dict(at="S008.4", k="ICON", d="أدوات صغيرة بتوفر يوم: تكبير (صورة بتتكبر وتفضل حادة) / شيل خلفية / لوجوهات وفيكتور / ثمبنيلز", clip=[22]),
 # C02b video
 dict(at="S009.1", k="CLIP", d="«الفيديو عيلة كاملة» = علي ماشي في قاهرة 1897", clip=[26]),
 dict(at="S009.2", k="SPLIT", d="«كلام مكتوب يبقى فيديو» / «صورة تبقى فيديو» = الـ keyframe بتاعنا ← نفس الكليب وهو بيتحرك"),
 dict(at="S009.3", k="CLIP", d="start frame و end frame: أول صورة (زرقا) وآخر صورة (دهبي) والكليب بيملا اللي بينهم، وبعده الشمس بتغرب في نفس الشارع = الفريم الأخير", clip=[31, 32]),
 dict(at="S009.4", k="CLIP", d="حركات الكاميرا (ملاحظة 13): dolly = كليب 6 / orbit = كليب 204 / crane = كليب 29، كل واحد على كلمته + رسمة صغيرة لمسار الكاميرا", clip=[6, 204, 29]),
 dict(at="S009.6", k="LOGOS", d="Seedance / Kling / Veo / Wan / MiniMax على أساميهم"),
 dict(at="S010.1", k="SPLIT", d="video to video: نفس الحركة قبل وبعد (كليب 26 ← كليب 28 بستايل تاني)", clip=[26, 28]),
 dict(at="S010.3", k="WEB", d="صفحة Genjutsu الحقيقية: «من 4 لـ 30 ثانية» و«30 صورة مرجع» يتعلّموا على الكلمة + عدادين"),
 dict(at="S010.5", k="ICON", d="تطويل (تايملاين بيطول) / تكبير (4K) / فريمات أكتر (24 ← 60 fps حركة بتنعم)"),
 dict(at="S010.7", k="VID", d="ثمبنيل فيديو Genjutsu + QR، وبعده الفيلم القصير + QR", vid=["8d4jkySoXe4", "PJTcdeSiDUI"]),
 # C02c face & body
 dict(at="S011.1", k="BTS", d="«اللي إنت شايفه دلوقتي»: الكادر يصغر ويبان إنه جوه شاشة HeyGen (من ورا الكواليس)"),
 dict(at="S011.2", k="WEB", d="صفحة HeyGen الحقيقية: «15 ثانية» تتعلّم + عداد 15 ث"),
 dict(at="S011.4", k="BTS", d="looks: نفس الوش بلبس/مكان تاني = صور الـ looks اللي عملناها فعلاً"),
 dict(av=36, k="AV", d="«ومكان تاني… lipsync» علي + جنبه موجة صوت والبق بيتحرك عليها"),
 dict(at="S012.1", k="BTS", d="تجاربنا الحقيقية: تست الصورة الواحدة (حركة زيادة) / الـ lipsync على فيديو حقيقي / الـ twin = الأحسن ✓"),
 dict(av=39, k="AV", d="«والـ twin كان الأحسن… دبلجة» علي + جنبه نفس الجملة بـ 3 لغات بتتبدل"),
 dict(at="S012.8", k="KT", d="القاعدة: «وش أي حد وصوته.. بموافقته بس» + أيقونة قفل/توقيع"),
 # C02d voice
 dict(at="S013.1", k="ICON", d="«الصوت»: الموجة بتاعة صوتك 3D بتلف (ملاحظة: الصوت اللي بتسمعه = حقيقي متولّد)"),
 dict(at="S013.2", k="KT", d="text to speech: كلام بيتكتب ← موجة بتطلع منه"),
 dict(at="S013.4", k="ICON", d="voice clone: سريع (1–2 دقيقة) vs احترافي (½ ساعة – 3 ساعات) = شريطين بالطول"),
 dict(av=43, k="AV", d="«voice changer… voice design» علي + جنبه صوت بيتحول لصوت تاني (موجتين)"),
 dict(at="S013.8", k="ICON", d="voice design: وصف مكتوب ← صوت جديد"),
 dict(at="S014.1", k="ICON", d="مؤثرات صوتية / تنضيف دوشة / فصل الصوت عن المزيكا (الـ stems الحقيقية من أغنيتنا)"),
 dict(av=46, k="AV", d="«النسخ السريعة لسه بتبان AI… والصوت اللي إنت سامعه كسب» + جنبه 3 نسخ صوت وعلامة ✓ على واحدة"),
 # C02e music
 dict(at="S015.1", k="WEB", d="Suno: الكلمات + الستايل ← أغنية (صفحة Suno الحقيقية)"),
 dict(at="S015.3", k="BTS", d="تعديل جزء بالكلام: نفس اللي عملناه فعلاً (مكس B→A + تصليح «بيكسل») + الـ stems (الغنا لوحده / المزيكا لوحدها) موجات حقيقية"),
 dict(at="S015.7", k="LYR", d="«هنعمل أغنية بيه» = لمحة من الأغنية بالدهبي", clip=[186]),
 # C02f 3D
 dict(at="S016.1", k="ICON", d="صورة ← موديل 3D بيلف (موشن three.js بسيط)"),
 dict(at="S016.3", k="BTS", d="«Blender يحرّكه بالكود»: الكود بيتكتب والـ blockout الرمادي بيتحرك: الكاميرا بتطير / الشمس بتغرب / القطع بتتركب، كل واحدة على كلمتها"),
 dict(at="S016.5", k="LOGOS", d="three.js (مشهد 3D بيتبني في متصفح) + Gaussian splats (نقط بتبقى مكان)"),
 dict(at="S017.1", k="SPLIT", d="أحسن تريك: الـ blockout الرمادي بتاعنا (Blender) ← نفس اللقطة بعد التوليد (look)، قبل وبعد بـ wipe", clip=[903]),
 dict(at="S017.4", k="CLIP", d="«قبل وبعد دلوقتي» = الكوبري بعد التوليد", clip=[53]),
 # C02g understanding
 dict(at="S018.1", k="KT", d="«الـ AI اللي بيفهم مش بيولّد»: عين/ودن بدل فرشاة"),
 dict(at="S018.3", k="BTS", d="Whisper بتاعنا: موجة الصوت ← كلام بتوقيت كل كلمة (ملف التوقيت الحقيقي بتاع الفيديو ده) ← كابشن وشابترز"),
 dict(at="S018.4", k="ICON", d="OCR بيقرا لافتة / موديل بيوصف صورة / تحليل فيديو ثانية بثانية"),
]
P += [
 # ---------------- C29 sites tour (real pages) ----------------
 dict(at="S019.1", k="KT", d="«هنلف على المواقع» + «نوفمبر 2026» وختم «بيتغير كل شهر»"),
 dict(at="S019.3", k="WEB", d="HeyGen: Avatar 6 + «15 ثانية» (صفحة حقيقية heygen_15s)"),
 dict(av=62, k="AV", d="«Avatar 6… Looks» علي + جنبه صور الـ looks"),
 dict(at="S020.4", k="WEB", d="Video Agent (heygen_agent) + لوجو Seedance على كلمته، وبعدها ترجمة +175 لغة (heygen_175) + عداد"),
 dict(at="S021.1", k="WEB", d="LiveAvatar (heygen_live): مكالمة real time"),
 dict(av=66, k="AV", d="«HyperFrames… MCP بتاعهم… الأسعار» علي + جنبه لوجو HyperFrames وسلك Claude ← HeyGen"),
 dict(at="S021.7", k="NUM", d="أسعار HeyGen: مجاني / Creator $29 = 600 كريدت"),
 dict(at="S022.1", k="WEB", d="ElevenLabs 3 أقسام على كلماتها: ElevenCreative / ElevenAgents / ElevenAPI (eleven_creative / eleven_agent)"),
 dict(av=70, k="AV", d="«Studio Agent… Flows» علي + جنبه لوجو ElevenLabs"),
 dict(at="S022.7", k="WEB", d="Flows: nodes بتتوصل، وبعدين Music / SFX / Scribe (eleven_scribe)"),
 dict(at="S023.2", k="NUM", d="أسعار ElevenLabs: Starter $6 / Creator $22 / الـ clone الاحترافي من Creator (eleven_pvc_plan)"),
 dict(at="S024.1", k="LOGOS", d="Higgsfield «موديلات كتير تحت سقف واحد»: سقف وتحته Seedance 2.5 / Kling / MiniMax / Wan"),
 dict(av=74, k="AV", d="«Cinema Studio 4.0: الكاميرا والعدسة والإضاءة والحركة» علي + الأربعة يطلعوا جنبه على كلماتهم"),
 dict(at="S025.1", k="WEB", d="Genjutsu + Supercomputer + MCP لـ Claude (hf_genjutsu_len)، وبعدين «كل توليد بيقولك تكلفته قبل ما تدفع» = شاشة التكلفة"),
 dict(av=78, k="AV", d="«5 ثواني: Seedance 2.5 = 80 كريدت، Kling 4.0 = 16» علي + عمودين بيكبروا جنبه"),
 dict(at="S026.1", k="WEB", d="Suno: Simple / Custom / v6 · v6-mini · v6-wild (suno_v6)"),
 dict(av=82, k="AV", d="«Voices… Stems… Studio 2.0… Warner/BMG/Believe… Suno MCP» علي + جنبه لوجو Suno وصفحة الشركاء الحقيقية (suno_partners)"),
 dict(at="S027.1", k="LOGOS", d="Claude: claude.ai / Projects / Connectors / Skills / Claude in Chrome / Claude Code على كلماتهم"),
 dict(av=86, k="AV", d="«Pro $20 / Max $100 / Ultra $200… Codex من OpenAI» علي + الخطط جنبه (claude_pro)"),
 dict(at="S028.2", k="WEB", d="Codex skills (codex_skills) + تيرمينال فيه --oss + لوجوهات Ollama / LM Studio"),
 dict(at="S028.4", k="WEB", d="تصحيح: Gemini CLI ✕ ← Antigravity CLI (antigravity) + «extensions ← plugins»"),
 dict(av=90, k="AV", d="«الموديلات الصيني بقت قوية: Kimi / DeepSeek…» علي + خريطة الصين صغيرة جنبه واللوجوهات على أساميها"),
 dict(at="S029.3", k="LOGOS", d="موديلات الفيديو الصيني على الخريطة: Seedance (ByteDance) / Kling / Wan"),
 dict(at="S030.1", k="WEB", d="ComfyUI على جهازك: كانفاس nodes + templates + LTX 2.5 (ltx25) / Wan / Flux / Qwen"),
 dict(av=94, k="AV", d="«LTX 2.5… Comfy Cloud» علي + لوجو ComfyUI"),
 dict(at="S030.5", k="LOGOS", d="Adobe Firefly / Runway / Luma / CapCut"),
 dict(at="S031.1", k="LOGOS", d="«المجاني اللي الفيديو ده اتبنى بيه»: رف أدوات"),
 dict(av=98, k="AV", d="«Whisper / Remotion / HyperFrames / three.js / Blender / ffmpeg… ببلاش» علي + الرف جنبه والأدوات بتتحط عليه على أساميها"),
 # ---------------- C03 LLMs & agents ----------------
 dict(at="S032.1", k="MAP6", d="الخريطة: قطعة 2 «LLMs والـ agents» تنوّر"),
 dict(at="S032.3", k="CLIP", d="«بيفهم ويكتب ويخطط» = قاعة التحكم والكود بينزل", clip=[99]),
 dict(av=101, k="AV", d="«agent = LLM ليه إيدين: يفتح ملفات، يكتب كود…» علي + أيقونات الإيدين على كلماتها، وبعدين Claude Code / Codex / Antigravity CLI / Qwen Code"),
 dict(at="S033.1", k="CLIP", d="«الـ agent مش بيرسم الفيديو بنفسه… بيكتب كود بيستخدم libraries» = روبوتات صغيرة على سير بتقص شريط فيلم + سطر كود فوقها", clip=[105]),
 dict(av=104, k="AV", d="«Remotion / three.js / ffmpeg / Blender / Whisper» علي + كل لوجو على كلمته وتحته شغلته"),
 dict(at="S033.4", k="ICON", d="Claude in Chrome (متصفح بيتحرك لوحده) / ماوس وكيبورد / ساعة + قمر = «وإنت نايم»", clip=[102]),
 # ---------------- C04 smart scripts ----------------
 dict(at="S034.1", k="MAP6", d="الخريطة: قطعة 3 «السكريبتات» تنوّر"),
 dict(at="S034.2", k="LOGOS", d="After Effects / Premiere / Photoshop / Blender / DaVinci على كلماتهم"),
 dict(at="S034.3", k="VID", d="أمثلة القناة: «شيل الصمت بضغطة» + QR / الـ AI جوه فوتوشوب + QR / After Effects لكود", vid=["ZXQLSxYmLsw", "Ps7A-UXx-5g"]),
 # ---------------- C05 MCP ----------------
 dict(at="S035.1", k="MAP6", d="الخريطة: قطعة 4 «MCP» تنوّر، و«فيشة موحدة» = فيشة واحدة بتدخل في كل البرامج"),
 dict(at="S035.3", k="LOGOS", d="HeyGen / ElevenLabs / Higgsfield / Suno كل واحد بفيشة MCP + Blender / DaVinci Resolve (blender_mcp)"),
 dict(at="S035.5", k="BTS", d="«تكتب جملة وClaude يفتح الأداة»: المحادثة الحقيقية بتاعتنا، و«الفيديو ده نفسه»: Claude متوصل بـ 4 أدوات (سلك لكل لوجو)", clip=[112]),
 # ---------------- C06 skills ----------------
 dict(at="S036.1", k="CLIP", d="الخريطة: قطعة 5 «skills» تنوّر ← «كراسة خبرة» = الكتب بتطير وتتفتح، وملف SKILL.md بيتفتح", clip=[115]),
 dict(at="S036.3", k="LOGOS", d="«معيار مفتوح»: Claude Code / Codex / Antigravity"),
 dict(at="S036.5", k="BTS", d="الـ skills الحقيقية بتاعتنا: كتابة السكريبت / نشر الريلز / رد كومنتات إنستجرام", clip=[117]),
 # ---------------- C065 real experience ----------------
 dict(at="S037.1", k="KT", d="«تجربة حقيقية بالأرقام»، وبعدين software tester full-time + ساعة «مفيش وقت»"),
 dict(at="S037.3", k="BTS", d="3 سنين فاضية + 3 كورسات على الرف + إنترو «انت بتشتغل ايه» 2023 (حاجاتك الحقيقية)"),
 dict(av=121, k="AV", d="«اللي اتبنى بـ Claude Code… video maker و20 ستايل» علي + عينات الستايلات بتلف جنبه"),
 dict(at="S038.3", k="BTS", d="skill السكريبت ← publisher: 28/أسبوع على 4 منصات (داشبورد reels-publisher) ← أوتوميشن إنستجرام: كلمة في الكومنت ← اللينك في الرسايل"),
 dict(av=125, k="AV", d="«الفيديوهات القديمة بقت ليها حياة… كورس ساعتين ← 31 شورت» علي + عداد 31 وشبكة الشورتس الحقيقية جنبه"),
 dict(at="S039.3", k="NUM", d="474K مشاهدة في آخر شهر (داشبورد كل منصة، اليوزرات متغطية) + ريل Genjutsu = 253K على فيسبوك"),
 dict(at="S039.5", k="KT", d="شورت كل يوم + فيديو كل أسبوع (كالندر)"),
 dict(av=129, k="AV", d="«الأحسن إن الـ AI يكتب السكريبتات…» علي + كود ← سكريبت شغال جنبه"),
 dict(at="S040.4", k="CLIP", d="«مفيش مكان للـ ego… اركب الموجة»", clip=[117]),
 # ---------------- C07 tutorial ----------------
 dict(at="S041.1", k="KT", d="«ريل 30 ثانية من الصفر» + مكوناته على كلماتها: وش / صوت / ستوديو / لقطة سينمائية / كابشن / مزيكا"),
 dict(at="S041.4", k="STEP", d="خطوة 1: اشترك في Claude (claude_pro)"),
 dict(av=134, k="AV", d="خطوة 2–3: Claude Desktop / PowerShell + claude --version (cc_install)، وحسابات ElevenLabs / HeyGen / Higgsfield / Suno — علي + الأمر واللوجوهات جنبه"),
 dict(at="S042.3", k="STEP", d="خطوة 4: Settings ← Connectors ← Add custom connector ← لينك الـ MCP ← Connect (شاشات حقيقية بمربع على كل زرار)"),
 dict(av=138, k="AV", d="«ملف .mcp.json و /mcp… خطوة 5: الـ digital twin» علي + الملف جنبه"),
 dict(at="S043.3", k="STEP", d="خطوة 5: كليب قصير + فيديو موافقة، وخطوة 6: الـ look جوه الستوديو (الستوديو المتولّد بتاعنا)"),
 dict(av=142, k="AV", d="خطوة 7–9: فولدر + CLAUDE.md / البرومبت (عايز إيه، طوله، ستايله)"),
 dict(at="S044.3", k="FLOW", d="خطوة 9 بالترتيب الحقيقي: صوت ← Whisper ← وش ← لقطة Higgsfield ← مزيكا Suno ← Remotion + ffmpeg (ملفات المشروع ده)"),
 dict(at="S044.4", k="BTS", d="خطوة 10 المراجعة: الغلطات الحقيقية (الاسم / الصوت / الحركة) اتصلحت ✓"),
 dict(av=146, k="AV", d="خطوة 11 الـ export + «تكلفة الريل بالظبط» علي + الفاتورة جنبه"),
 # ---------------- C075 tips ----------------
 dict(at="S045.1", k="KT", d="«تريكات بتوفر وقت» + عداد التريك (1 من 15) في الركن طول الفصل"),
 dict(at="S045.2", k="BTS", d="1 الكابشن: Scribe / Whisper ← توقيت كل كلمة ← SRT ← CapCut / Premiere (ملف SRT الحقيقي بتاعنا)"),
 dict(at="S045.5", k="BTS", d="2 موشن شفاف: Remotion ← ProRes 4444 / WebM ← layer فوق الفيديو (الطبقات الشفافة اللي عملناها)"),
 dict(at="S046.1", k="SPLIT", d="3 الـ look جوه المكان vs أفاتار متركب على خلفية"),
 dict(at="S046.3", k="SPLIT", d="4 كلمة بتتنطق غلط ← غيّر الجملة («نص» ← «كلام مكتوب»، حصلت هنا فعلاً)"),
 dict(at="S046.5", k="SPLIT", d="5 آخر فريم = أول فريم في اللي بعده"),
 dict(at="S046.7", k="SPLIT", d="6 الحركة من Blender والشكل من التوليد (blockout المعمل ← look)", clip=[902]),
 dict(at="S047.1", k="BTS", d="7 ثبّت الشخصية: صور مرجع + ملف البرومبتات الحقيقي"),
 dict(at="S047.3", k="NUM", d="8 اسأل عن السعر الأول: نسخة رخيصة ← 4K في الآخر"),
 dict(at="S047.5", k="ICON", d="9 قص الصمت + شابترز من Whisper"),
 dict(at="S047.7", k="BTS", d="10 الـ stems: المزيكا بتوطى تحت الكلام (موجاتنا الحقيقية)"),
 dict(at="S048.1", k="NUM", d="11 صوت يوتيوب: loudnorm ← -14 LUFS"),
 dict(at="S048.3", k="SPLIT", d="12 من 16:9 لـ 9:16 + نفس الكابشن"),
 dict(at="S048.5", k="BTS", d="13 مكتبة اللوجوهات (الفولدر الحقيقي + مصدر كل لوجو)"),
 dict(at="S048.8", k="BTS", d="14–15 كارت الستايل (برومبت / موديل / ألوان) + تجربة على 3 لقطات رخيصة"),
 # ---------------- C08 money ----------------
 dict(at="S049.1", k="CLIP", d="«بكام؟» = باب الخزنة", clip=[162]),
 dict(at="S049.2", k="NUM", d="الفاتورة بتتملا سطر سطر على الكلام: Claude $20 / ElevenLabs $6 / HeyGen $29 / Suno $10 / Higgsfield كريدت + «نوفمبر 2026»", clip=[165]),
 dict(at="S050.1", k="LOGOS", d="المجاني: Whisper / Blender / Remotion / HyperFrames / ffmpeg / ComfyUI"),
 dict(at="S050.3", k="NUM", d="تكلفة الفيديو ده بالظبط بالكريدت والدولار (من cost_plan الحقيقي)"),
 # ---------------- C09 human ----------------
 dict(av=167, k="AV", d="الخريطة: قطعة 6 «الإنسان» تنوّر ← «الـ AI إيد سريعة… دور الإنسان» علي + إيد آلية وإيد إنسان جنبه"),
 dict(at="S051.3", k="ICON", d="دور الإنسان على كلماته: فكرة / ذوق واختيار من 1000 / مراجعة / مصادر / مسؤولية، فوق لحظة تسليم آخر قطعة (bullet-time)", clip=[168]),
 dict(av=170, k="AV", d="«مثال من الفيديو ده» علي + جنبه الغلطات الحقيقية اتصلحت"),
 dict(at="S052.2", k="BTS", d="المراجعة الحقيقية: الصوت اتجرب كذا مرة / الاسم اتصلح / المصادر (سكرينات evidence متعلّمة)"),
 # ---------------- C095 AI label ----------------
 dict(at="S053.1", k="WEB", d="يوتيوب مايو 2026: label تحت المشغل / على الشورت (yt_may2026 / yt_below / yt_overlay)"),
 dict(av=175, k="AV", d="«في الطويل تحت المشغل… C2PA» علي + الـ label جنبه (yt_c2pa)"),
 dict(at="S054.1", k="WEB", d="Meta / تيك توك (tiktok) / SynthID (synthid) — صفحات حقيقية"),
 dict(av=178, k="AV", d="«SynthID… قرارنا: نعلّم الفيديو إنه AI» علي + SynthID (synthid) وبعدين علامة ✓ جنبه"),
 dict(at="S054.6", k="KT", d="«أي وش أو صوت لحد حقيقي.. بموافقته بس»"),
 # ---------------- C10 how the song was made ----------------
 dict(at="S055.1", k="BTS", d="الكلمات اتكتبت (ملف song_v4 الحقيقي) / الستايل لـ Suno / 4 نسخ واتختارت واحدة / المكس B→A"),
 # ---------------- C11 the song: one clip per LINE (note 19) ----------------
 dict(song=True, k="LYR", d="كل سطر = كليبه على توقيت السطر: الجدار/الفحمة/النار/التور = 186 الكهف · حبر وورق وريشة = 189 ثم 192 · ماوس/Photoshop/After Effects/rendering = 195 و198 + شاشات موشن · بكتب جملة/صوت/طيارة/agents/MCP = 201 204 213 + لوجوهات · الكورس = مونتاج سريع على الإيقاع (183 207 210) · الكلام بخط كبير على الإيقاع، الشاشة كلها", clip=[186, 189, 192, 195, 198, 201, 204, 213, 183, 207, 210]),
 # ---------------- C12 outro ----------------
 dict(at="S057.1", k="MAP6", d="الطيارة كاملة (الـ 6 قطع منورين) في الهانجر والنور بيولع ← بتطلع من باب الهانجر للشروق = «ملخص»", clip=[171, 216]),
 dict(av=215, k="VID", d="علي بيعد الفيديوهات وكل واحد يطلع ثمبنيله + QR على اسمه (6 فيديوهات)", vid=["H5oOZypINf0", "PJTcdeSiDUI", "10UXB0cT4Ss", "8d4jkySoXe4", "ZXQLSxYmLsw", "Ps7A-UXx-5g"]),
 dict(at="S057.5", k="KT", d="«دوّر عليهم في القناة» + لوجو القناة"),
 dict(av=218, k="AV", d="«أنهي حتة في الخريطة عايزها فيديو؟» علي + الخريطة الصغيرة جنبه وكل قطعة بتنوّر"),
]
