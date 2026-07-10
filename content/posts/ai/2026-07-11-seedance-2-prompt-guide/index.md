+++
date = '2026-07-11T10:00:00+08:00'
draft = false
title = 'Seedance 2.0 Prompt Guide: Best Practices & Failure Modes'
description = 'How to write Seedance 2.0 prompts that work: a five-slot formula, @reference tagging rules, six failure modes, and what transfers to Veo 3 and Sora 2.'
toc = true
tags = ['Seedance', 'AI Video', 'ByteDance', 'Prompt Engineering', 'Video Generation']
keywords = ['seedance prompt guide', 'seedance 2.0 tutorial', 'bytedance video ai prompts', 'how to write seedance prompts', 'seedance 2.0 reference video', 'seedance vs veo 3 prompts', 'seedance prompt formula']

[[params.faqItems]]
question = "How do I write prompts for Seedance 2.0?"
answer = "Use five slots in order: subject, action, scene, camera, style/audio. Keep it to 60-100 words, front-load what matters most, use exactly one primary camera move, and put spoken dialogue in double quotes for automatic lip-sync."

[[params.faqItems]]
question = "How do @image and @video references work in Seedance 2.0?"
answer = "You can attach up to 9 images, 3 videos, and 3 audio files (12 total) and cite them as @image1, @video1, @audio1 in the prompt. Always state what each reference is for — 'reference @video1 for camera movement only' — because a naked @video1 with no role assignment is the single most common failure."

[[params.faqItems]]
question = "Why do my Seedance 2.0 videos ignore half my prompt?"
answer = "Instruction adherence decays by position: the first 2-3 instructions are followed reliably, and a prompt with 8 requirements typically lands only 4-5. Cut the prompt to 60-100 words and move the non-negotiable instructions to the front."

[[params.faqItems]]
question = "Do Seedance 2.0 prompt techniques work on Veo 3 or Sora 2?"
answer = "Camera vocabulary (dolly, orbit, tracking shot) and quoted dialogue transfer well. The @multi-reference system, audio references, beat-synced editing, prompt-based video editing, and reliable on-screen text are Seedance-specific and do not transfer."

[[params.faqItems]]
question = "How much does Seedance 2.0 cost per video?"
answer = "As of July 2026, roughly ¥1 (~$0.14) per 15-second clip via Volcano Engine's API, or about $0.68/second at 1080p through fal.ai. Dreamina and CapCut offer free daily credits, which is enough for learning the prompt patterns in this guide."
+++

![Seedance 2.0 prompt guide — five-slot formula and reference tagging for ByteDance's video model](cover.webp)

ByteDance published an official prompt guide for Seedance 2.0 in late March 2026. It is genuinely useful — and it is also a dictionary, not a course. It tells you that a slogan formula exists, that you can reference videos for camera movement, that subtitles can sync to a voiceover. What it never tells you is *when* to use which technique, what happens when you stack them wrong, and which of your hard-earned habits from Veo 3 or Sora 2 will actively hurt you here.

This Seedance 2.0 prompt guide is the judgment layer on top of that dictionary. I wrote a [full teardown of Seedance 2.0's architecture](/posts/ai/2026-03-29-seedance-2-bytedance-ai-video/) when it topped the [Artificial Analysis](https://artificialanalysis.ai/text-to-video) leaderboard in March; this article is the companion piece about actually driving the thing. My core claim, condensed: **a Seedance 2.0 prompt is a job assignment, not a description.** Text handles semantics — who does what. References handle standards — exactly how things look and move. Most failed generations I've seen trace back to confusing those two jobs, not to insufficient adjectives.

## The Five-Slot Prompt Formula (and What Each Slot Buys You)

The official formula is `subject + motion + environment + camera + aesthetics + audio`, with everything after motion marked optional. That's accurate but under-specified — it reads like a shopping list, and people respond by stuffing every slot to the brim. After enough iterations, I've compressed it into a template with explicit budgets:

```text
[SUBJECT]  who or what, 1-2 concrete attributes, no more
[ACTION]   one primary verb chain, with physical consequences
[SCENE]    place + light, one sentence
[CAMERA]   exactly ONE primary move, optionally with an end state
[STYLE/AUDIO]  visual treatment + named sounds ("no music" if unwanted)
```

```mermaid
flowchart LR
    subgraph CORE["Mandatory core"]
        A["Subject<br/>who / what<br/>+ 1-2 attributes"] --> B["Action<br/>one verb chain<br/>with consequences"]
    end
    subgraph LAYERS["Optional layers — front-load what matters"]
        C["Scene<br/>place + light"] --> D["Camera<br/>ONE primary move"] --> E["Style / Audio<br/>look + named sounds"]
    end
    B --> C
```

Three rules make this template work, and none of them appear in the official guide:

**Budget 60-100 words total.** ByteDance's own team, when asked in the guide's comment thread whether there's a recommended prompt length, answered "no." The community converged on one anyway: adherence to instructions decays sharply by position. The first two or three instructions are followed almost every time; by the time you've written eight requirements, you'll land four or five. A short prompt with one clear motion beats a long prompt with competing ambitions — I've verified this enough times that I now treat prompt trimming as the first debugging step, before touching anything else.

**Verbs beat adjectives.** "A stunning, cinematic, beautiful dancer" gives the model nothing to animate. "A dancer dropping into a low spin, the skirt flaring, then snapping upright" gives it a physical sequence with consequences. The [fal.ai prompting guide](https://fal.ai/learn/tools/seedance-2-0-prompting-guide) makes the same point about describing outcomes: "leaves scatter *on each impact*" resolves to concrete motion; "leaves scatter" resolves to a screensaver.

**One camera move per clip.** Seedance 2.0 understands professional camera vocabulary — dolly, pan, orbit, crane, tracking shot, Hitchcock zoom, locked-off — and follows it cleanly. It does not gracefully arbitrate between two camera instructions in the same clip. "Fixed shot" plus "orbit the subject" in one prompt produces jitter, drift, or an ugly compromise between both. If you need two moves, that's two shots, and Seedance handles multi-shot natively with explicit "cut to" markers.

Here's the difference in practice:

| | Weak prompt | Strong prompt |
|---|---|---|
| **Subject** | "a beautiful woman" | "a woman in her 30s, dark hair, charcoal wool coat" |
| **Action** | "walking, looking amazing, cinematic vibes" | "walks past rain-wet storefronts, stops, exhales visibly in the cold air" |
| **Camera** | "dynamic camera, epic movement, orbiting and zooming" | "slow push-in from a 45° angle, ending in a medium close-up" |
| **Audio** | *(unspecified — model adds random score)* | "light rain, distant traffic, muffled jazz from inside the shop, no music" |
| **Result** | Generic stock footage with a soundtrack you didn't ask for | The shot you storyboarded |

That last row's audio note matters more than it looks: Seedance 2.0 generates audio jointly with video in one forward pass — its signature capability — and an unspecified audio slot defaults to a musical score. If you don't want music, you have to say so. Silence is a direction, not an absence.

## Text vs. References: The Decision That Determines Everything Else

Seedance 2.0 accepts up to 9 reference images, 3 reference videos, and 3 audio tracks — 12 files total — cited inline as `@image1`, `@video1`, `@audio1`. No competing model accepts anywhere near this (Sora 2 takes one image; audio references don't exist anywhere else). The official guide documents the mechanics. What it skips is the decision rule for when to describe something in text versus when to attach a file.

The rule I use: **text is for spatial decisions, references are for temporal and identity decisions.** What the world contains, where the light comes from, what mood you want — text handles that fine. But a camera move's exact easing, a dance's rhythm, a character's face across angles — text can only approximate these, while a reference *contains* them. Describing a Hitchcock zoom in words gets you a plausible Hitchcock zoom; attaching a clip of one gets you *that* zoom.

| You want to control... | Use | Why |
|---|---|---|
| Who's in the scene, what happens | Text | Semantics is what language is for |
| A character's exact face/outfit across shots | @image (multi-view set) | Identity drifts in text; images anchor it |
| A specific camera move's feel | @video | The clip contains the timing; words approximate it |
| Choreography, gesture cadence | @video | Same — rhythm doesn't survive translation to text |
| Music, beat-synced cuts | @audio | Seedance cuts and paces to the actual waveform |
| A logo or product's precise look | @image | Text-described logos render as fiction |
| Mood, light, atmosphere | Text (or @image at low strength) | Cheap to describe, no anchoring needed |

Two operational rules on top of this:

**Every reference needs a stated job.** The single most common failure in community threads — and the official guide's own examples confirm this pattern by contrast — is the naked reference: "reference @video1" with no role. Reference *what* about video1? The camera? The action? The color grade? Write it explicitly: "@image1 as the character's appearance, reference @video1 for camera movement only, @audio1 for background rhythm." Unassigned references make the model guess, and it guesses everything at once, contaminating your shot with the reference clip's lighting, framing, and pacing when you only wanted its choreography.

**Keep reference strength at 70-80%.** The default is 75% and it's well chosen. I covered the full sweep in [the teardown](/posts/ai/2026-03-29-seedance-2-bytedance-ai-video/), but the short version: at 90-100% your character becomes a cardboard cutout — technically faithful, unable to adapt pose and lighting naturally. Below 60%, identity drifts. Maxing every reference to 100% "for safety" is the reference-system equivalent of adjective-stuffing, and it fails the same way.

## On-Screen Text: The Technique Nobody Else Can Copy

Legible text inside generated video has been the industry's shared embarrassment — signs, screens, and titles come out as alien glyphs on essentially every model. Seedance 2.0 is the first one where prompting for text is a real workflow rather than a prayer, across T2V, I2V, and reference-based generation. The official guide breaks it into three techniques, and having tested all three, I'd rank them by reliability:

**Subtitles (most reliable).** The pattern: `subtitles appear at the bottom of the frame, matching the voiceover: "..."` — and because audio and video are generated in one pass, the sync is genuine, not post-hoc. One constraint the guide only implies: keep each spoken line short. Long monologues drift out of lip-sync; the fix is splitting the speech across cuts, giving each cut a sentence.

**Slogans/titles (reliable with the formula).** The official formula is worth memorizing because every element is load-bearing: `"text content" + when it appears + where it appears + how it enters + styling (color, style)`. Example from the guide, translated: *"...the frame gradually blurs, and the text 'Joy is Seedance' appears in the center of the frame."* Omit the timing and the text may sit there the whole clip; omit the position and it lands wherever. If your brand requires an exact logotype rather than "text in roughly the right style," don't prompt it — attach the logo as an @image reference.

**Speech bubbles (fun, less predictable).** `[Character] says: "...", a speech bubble appears beside them containing the line` — great for comic-style content, more variance in bubble placement and style.

The universal constraint: **use common words and skip special symbols.** Rare glyphs and decorative punctuation are where the alien-glyph problem sneaks back in. And write your prompt in the same language as the text you want rendered — a prompt in English asking for on-screen Chinese (or vice versa) noticeably raises the garbling rate.

## Video References and Prompt-Based Editing: Where Seedance Stops Being a Generator

Section 2.3 and 2.4 of the official guide are, in my judgment, the actual moat — and the sections most people skip because they look advanced. They turn Seedance 2.0 from a text-to-video generator into something closer to a promptable video editor:

- **Action reference**: transplant choreography from a clip onto your character — "the singer in @video1 replaced by the man in @image1, movements exactly following the original video."
- **Camera reference**: steal a camera move wholesale — "follow all camera movements from @video1." Combined with vocabulary like "one continuous take, no cuts," this is how you get shots that text alone won't produce.
- **Effects reference**: replicate a transition or particle effect from a reference clip onto new content.
- **Element add/remove/change**: modify an existing video by prompt — change a character's hair color, add a shark surfacing behind a swimmer, flip a scene's emotional register mid-clip.
- **Extension, forward and backward**: extend an existing clip, with the guide recommending per-second breakdowns for anything over 8 seconds ("seconds 1-5: light slides across the table... seconds 11-15: the text 'Lucky Coffee' fades in").
- **Track completion**: bridge two or three separate clips into one continuous sequence — "the particle horse in @video1 gradually solidifies... transitioning into @video2."

The per-second breakdown deserves emphasis because it generalizes: **for any clip longer than 8 seconds, structure the prompt as a timeline, not a description.** A single block of prose describing 15 seconds of action forces the model to invent its own pacing. "Seconds 1-5 / 6-10 / 11-15" hands it a shot plan. This one habit fixed more of my long-clip generations than any other change.

## Six Failure Modes the Official Guide Won't Warn You About

Every technique above has a corresponding way to crash. These six account for nearly every broken generation I've produced or seen dissected in community threads — the [dexhunter/seedance2-skill](https://github.com/dexhunter/seedance2-skill) repo, which reverse-engineered the official guide into an agent skill, corroborates most of them:

| # | Failure mode | Symptom | Fix |
|---|---|---|---|
| 1 | Instruction overflow | 8 requirements written, 4-5 honored, seemingly at random | Cut to 60-100 words; front-load the non-negotiables |
| 2 | Naked @references | Reference clip's lighting/framing bleeds into your shot | Assign every reference an explicit job ("for camera movement only") |
| 3 | Stacked camera moves | Jitter, drift, mid-clip direction changes | One primary move per clip; use "cut to" for the rest |
| 4 | Mixed-language prompts, rare glyphs | On-screen text garbles; semantics get muddy | One language per prompt, matched to the on-screen text; common words only |
| 5 | Scene cramming | 3 locations demanded of a 5-second clip → smeared morphing | Match complexity to duration; per-second timeline above 8s |
| 6 | Reference strength maxed / real faces | Cardboard characters; identifiable-face uploads get blocked outright | 70-80% strength; use illustrated or generated character sheets |

Number 4 deserves a note because it's the one that most often bites bilingual users: Chinese-English mixed prompts *mostly* work for semantics, but the moment on-screen text is involved, mixing languages in the prompt measurably raises the garble rate. Pick the language of your target text and write the whole prompt in it.

Number 6's second half is a policy constraint, not a quality one: after the IP disputes I covered in the teardown, Seedance blocks generation from clearly identifiable real faces. Plan your character pipeline around generated or illustrated reference sheets from the start, rather than discovering the block mid-project.

## What Transfers to Veo 3 and Sora 2 — and What Doesn't

If you work across models — and at current pricing spreads, you probably should — it matters which habits are portable. As of July 2026, here's my transfer map:

| Technique | Seedance 2.0 | Veo 3 | Sora 2 |
|---|---|---|---|
| Camera vocabulary (dolly, orbit, tracking) | Native | Excellent — arguably best-in-class precision | Good |
| Subject + action + consequence structure | Native | Transfers fully | Transfers fully |
| Quoted dialogue → lip-sync | Native, one pass | Yes, native audio | Approximate; audio is post-hoc |
| @multi-reference (9 img / 3 vid / 3 audio) | **Unique** | Up to ~3 image ingredients in Flow | Single image |
| Audio file as rhythm/beat reference | **Unique** | No | No |
| Multi-shot in one generation ("cut to") | Native | Limited | Via storyboard tool, different syntax |
| On-screen text (slogans, subtitles) | Workable | Garbles | Garbles |
| Prompt-based video editing (add/remove/extend) | Native | Extend only | Remix, different mental model |

The pattern: **the grammar transfers, the vocabulary of control doesn't.** Structure your prompt as subject-action-scene-camera anywhere and you'll do fine. But everything involving references, on-screen text, audio direction, and editing is Seedance dialect. In the reverse direction, the habit Veo 3 users bring that hurts most on Seedance is over-writing — Veo 3 rewards elaborate, hyper-specified prompts, while Seedance's instruction-position decay punishes them. Sora 2 users bring the opposite problem: trusting the model's creative liberties. Seedance follows orders more literally, which means vague orders produce literal, boring output rather than a pleasant surprise.

## From Storyboard to Final Cut: The Workflow That Uses All of It

The techniques only compound when you run them as a pipeline. Here's the workflow I've settled on for multi-shot pieces:

```mermaid
flowchart TB
    S1["1 · Storyboard<br/>break the story into shots, each ≤15s"] --> S2["2 · Reference pack<br/>multi-view character sheet (images)<br/>+ camera/audio reference clips"]
    S2 --> S3["3 · Anchor shot<br/>generate the shot that locks<br/>character + look + palette"]
    S3 --> S4["4 · Remaining shots<br/>anchor output becomes a<br/>@video reference for consistency"]
    S4 --> S5{"Shot approved?"}
    S5 -- "no — change ONE variable" --> S4
    S5 -- "yes" --> S6["5 · Bridge gaps<br/>extension + track completion"]
    S6 --> S7["6 · Assemble<br/>cuts, titles, grading in CapCut"]
```

Three judgments embedded in that diagram, in order of how much pain they save:

**Generate the anchor shot first, then feed it back.** Character consistency across shots is Seedance's headline feature, but it's not automatic — it's earned by making your best shot the reference for every subsequent one. The anchor shot is the one where character, wardrobe, and palette all land; from then on, it rides along as `@video1` and the model treats it as ground truth.

**Change one variable per iteration.** When a shot misses, the instinct is to rewrite the whole prompt. Resist it. Adjust the camera *or* the action *or* the reference strength, regenerate, and compare. At roughly ¥1 per 15-second clip, iteration is nearly free in money but not in time — disciplined single-variable changes converge in 3-4 rounds where shotgun rewrites wander for ten.

**Build the reference pack before generating anything.** The multi-view character sheet is the highest-leverage asset in the pipeline, and it's an image-generation problem, not a video one. I use [Seedream — ByteDance's image-side sibling model](/posts/ai/2026-07-10-seedream-5-pro/) for character sheets since the aesthetic transfers cleanly into Seedance; for a local, free alternative, my [Draw Things + Claude Code pipeline](/posts/ai/2026-02-16-claude-code-draw-things-workflow/) produces serviceable multi-view sets on a Mac.

## How to Access Seedance 2.0 (and What Prompting Practice Costs)

For readers outside China, the access map is genuinely confusing, so briefly: **CapCut** (the international 剪映) is the zero-friction entry — free daily generations, no Chinese phone number, but limited reference controls. **[Dreamina](https://dreamina.jianying.com/)** (international 即梦) exposes the full @reference system on a daily credit allowance and is where I'd practice everything in this guide. For APIs, **Volcano Engine Ark** requires a Chinese phone number; **BytePlus ModelArk** is the international route ByteDance slated for Q2 2026; and **[fal.ai](https://fal.ai/learn/tools/seedance-2-0-prompting-guide)** works today with a credit card.

On cost, the numbers worth knowing: as of July 2026, a 15-second clip runs roughly ¥1 (~$0.14) via Volcano Engine — about 5-10x cheaper than Sora 2 (~$1.50) or Veo 3 (~$0.75) for equivalent length. Via fal.ai, 1080p costs about $0.68/second, with 720p and 480p cheaper. The practical implication for learning: a full evening of disciplined single-variable iteration costs less than a coffee, which is exactly why the "change one variable" workflow is viable here and painful on Sora 2.

## The Takeaway

If you remember one thing: **assign jobs, don't write descriptions.** Text gets semantics, references get standards, every reference gets an explicit role, every clip gets one camera move, and anything over 8 seconds gets a timeline. The official guide gives you the vocabulary; the judgment about what goes where is what separates a generation queue full of near-misses from a shot list that converges.

Start with the five-slot template, keep it under 100 words, and steal the anchor-shot workflow even if you ignore everything else — consistency is the thing viewers actually notice, and it's the thing none of Seedance's competitors can currently match at this price.

## Related Reading

- [Seedance 2.0 Deep Dive: How ByteDance Built the #1 AI Video Model](/posts/ai/2026-03-29-seedance-2-bytedance-ai-video/) — the architecture teardown this guide builds on
- [Seedream 5 Pro: ByteDance's Image Model](/posts/ai/2026-07-10-seedream-5-pro/) — the image-side sibling, ideal for building reference packs
- [Claude Code + Draw Things: A Local Image Generation Pipeline](/posts/ai/2026-02-16-claude-code-draw-things-workflow/) — free local alternative for character sheets
- [Draw Things Ultimate Guide](/posts/ai/2026-02-15-draw-things-ultimate-guide/) — local image generation on Apple Silicon
