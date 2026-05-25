# Style Note: Time To Build

A short reference study to inform the production build (Step 3 in `DESIGN.md`). It distills three formats — Nicky Case's playable explanations, The Pudding's editorial scrollytelling, and Bartosz Ciechanowski's embedded explanations — into concrete guidance for *this* essay. Not UI, not code: the rules the build should follow and the traps it should avoid.

The essay's job, set by `ESSAY_OUTLINE.md`: walk a skeptic from "now just feels special" to "the leading indicator says build now" across six chapters, with the Chapter 4 indexed-growth reveal as the shareable moment and the Chapter 5 fork as the credibility keystone.

---

## The three references, in one line each

- **Nicky Case** (*The Evolution of Trust*, *Parable of the Polygons*) — pacing through participation. Short text beats, one idea per screen, the reader *does* something small before the next idea arrives. Warmth and plain language carry a rigorous argument.
- **The Pudding** (*editorial scrollytelling*) — a sticky visual on one side, narrative text scrolling past on the other, each text step triggering one specific change to the visual. Journalistic discipline: the chart is the evidence, the prose is the argument, sourcing is visible.
- **Bartosz Ciechanowski** (*Cameras and Lenses*, *Mechanical Watch*) — embedded, manipulable diagrams. You don't watch the explanation, you operate it. Generous whitespace, slow confident pacing, every interaction teaches one mechanism. Craft so high the reader trusts the author by default.

What we take from each: Case's *belief-moving pacing*, The Pudding's *sticky-chart choreography and sourcing discipline*, Ciechanowski's *one-interaction-one-idea restraint and visual calm*. What we leave: Case's game-like length (we're shorter and more argumentative), Ciechanowski's physics-sim depth (our interactions are light), The Pudding's neutrality (we have a thesis and say so).

---

## Pacing

- **One idea per scroll step.** Every step changes exactly one thing in the visual or adds one claim. If a step does two things, split it. This is the shared rule across all three references and the single most important one.
- **Six chapters, ~3–6 steps each.** Target a 6–9 minute read. The outline's belief arc is the pacing skeleton — each chapter must land its before→after delta, and a step that doesn't move the belief gets cut (the outline says this; enforce it).
- **Text beats are short.** 1–3 sentences per step, Case-style. The reader should never face a wall of prose beside a static chart. Long-form caveats live in expandable panels or the appendix, not the scroll spine.
- **Earn the reveal with a slow build.** Chapters 1–3 are setup that makes Chapter 4 hit. Don't rush to the AI curve — the breakaway only feels dramatic because commerce, fintech, and crypto established the baseline. Ciechanowski's confidence comes from not rushing.
- **One breath before the fork.** Chapter 4 (reveal) → Chapter 5 (fork) is the essay's emotional turn: from "wow" to "but honestly we don't know yet." Give it a deliberate pause — a near-empty transition screen, a single line. Don't let the fork arrive while the reader is still celebrating the reveal.
- **Pace the share moment to be screenshot-stable.** The Chapter 4 indexed curve must hold a clean, captioned-by-the-chart-itself frame long enough to screenshot. Don't animate through the money frame so fast it can't be captured.

---

## Visual Hierarchy

- **The chart is the page; text is the guide.** The Pudding model: one sticky visual holds the viewport, narrative scrolls beside (desktop) or above/below in steps (mobile). The reader's eye lives on the data.
- **Highlight by de-emphasis.** When a chapter is about one wave, gray the others to context lines rather than adding loud colors. Attention comes from contrast, not saturation. (Ciechanowski's diagrams isolate the active part by dimming the rest.)
- **One color system, used consistently.** Each wave gets one fixed color for the whole essay so the reader builds muscle memory: the AI line is the same hue in Chapter 1's stacked area, Chapter 4's reveal, and Chapter 6's callback. Never recolor a wave between chapters.
- **One number per moment.** The reveal carries a single annotated figure (broad 46.5%, Spring 2026), not a stat dump. Supporting numbers appear on demand (hover/tap), not all at once.
- **Generous whitespace; let the chart breathe.** Resist filling margins. Calm layout reads as confidence and makes the data legible at a glance — the 5-second-comprehension success criterion depends on it.
- **Annotations live on the chart, not in a legend far away.** Label the AI line where it breaks away; label crypto's ceiling at the 10% line. The reader shouldn't hunt a legend to decode the point.

---

## Interaction

- **Default to scroll-driven, not click-driven.** The Pudding pattern: scrolling *is* the interaction; each scroll step advances the visual. The reader gets the whole argument by doing nothing but scrolling — interactivity is enhancement, not a gate.
- **The one real control is the strict/broad toggle (Chapter 4).** This is the essay's signature interaction and its integrity move at once: the reader switches the conservative lower bound (strict, 23.4% peak) against the current broad read (46.5% peak) and watches the AI line move. Make it feel like *you* checking the author's honesty, Case-style — participation that builds trust.
- **Hover/tap reveals detail, never hides essential meaning.** Batch counts, exact percentages, company examples surface on demand. But the core claim must read with zero interaction (mobile, screenshot, scroll-past-fast all have to work).
- **Every interaction teaches one thing.** Ciechanowski's rule: no decorative interactivity. If a control doesn't change what the reader believes, cut it. The toggle changes belief (shows the range is real); a parallax flourish does not.
- **Respect the lurker and the screenshotter.** Many readers won't touch anything and many will only see a screenshot. The essay must fully land for both. Interactivity is the bonus layer for the engaged reader, never the load-bearing one.
- **Reduced-motion and mobile are first-class.** Honor `prefers-reduced-motion` (static states that still tell the story). Mobile gets the stacked step-card pattern, not a cramped side-by-side. The audience is Twitter — most arrivals are phones.

---

## Tone

- **Confident thesis, honest evidence.** Unlike The Pudding's neutrality, we have an argument and state it plainly (the outline's thesis sentence). But every claim stays on the defensible side: formation is proven, outcomes are open. Confidence about *what the data shows*, humility about *what it can't*.
- **Plain, warm, direct — Case's register.** Second person ("you"), short sentences, no jargon wall. "Waves have come before" not "Historical cohort analysis reveals cyclical founder-attention patterns." The reader is a smart peer, not a student.
- **Let the chart make the point; don't oversell in prose.** The Pudding discipline: state what the chart shows, then stop. If the prose has to insist the data is impressive, the chart isn't doing its job — fix the chart.
- **Caveats in the same voice as claims.** Don't switch to defensive legalese for the methodology notes. "These tags are today's labels, not what companies called themselves back then — so we show you both reads and let you decide" is on-voice. Honesty stated warmly reads as strength.
- **Earn the call to action.** Chapter 6 can be motivating without being a pitch, because it rests only on the proven formation claim. "The leading indicator says now" — not "you'll definitely win."

---

## What To Avoid

- **AI slop / generic dashboard aesthetic.** No purple gradients, no glassmorphism, no emoji-bullet "key insights," no chart-junk. The references all read as authored, crafted objects. This should look like The Pudding, not a BI tool.
- **The stacked area as proof.** The outline already calls this out: its `Other` bucket and exclusive categories blur "faster and broader." It's Chapter 1 context only. The proof chart is the indexed growth curve.
- **Overclaiming at the reveal.** "AI is in every category" breaks the essay (the outline's #1 failure mode). Say "many major categories" and show the actual sector split (B2B 46.8% concentration included).
- **Burying or skipping the fork.** Chapter 5 stays a full chapter. Cutting it to a caveat panel turns the essay into a pitch and loses the skeptic — a stated success criterion.
- **Decorative interactivity and motion for its own sake.** Every animation must encode a data change. Scroll-jacking, surprise autoplay, and parallax-for-vibes all erode the Ciechanowski-style trust we're borrowing.
- **Walls of text beside a static chart.** If a step's prose outweighs its visual change, the pacing is broken. Split the step or move the prose to an expandable.
- **Recoloring or relabeling waves between chapters.** Breaks the muscle memory that lets the reveal land in 5 seconds.
- **Hiding the data source.** The Pudding always shows its work. `yc-oss/api`, the snapshot date, and the strict/broad method get a visible, linked methodology note — credibility depends on it, and one success criterion is a data-skeptic accepting the methodology.
- **Heavy weight that breaks the load budget.** The references stay fast; so must we (DESIGN.md: <300KB uncompressed, <2s load). No heavyweight chart libraries beyond the planned D3 + Scrollama, no unoptimized hero media.

---

## One-paragraph summary (the deliverable Step 3 asked for)

Build it like The Pudding choreographed it, paced like Nicky Case, and crafted like Ciechanowski: a sticky chart that the narrative scrolls past one idea at a time, each scroll step changing exactly one thing, with short warm second-person prose that states a confident thesis but lets the chart carry the proof. The waves keep fixed colors across all six chapters so the Chapter 4 breakaway reads in five seconds; the lone real interaction is the strict/broad toggle, which doubles as the essay's honesty (the reader checks the author's work). Slow the build through Chapters 1–3 so the reveal lands, pause before the Chapter 5 fork so the turn from "wow" to "we don't know yet" registers, and keep everything legible with zero interaction for the lurker and the screenshotter. Avoid dashboard slop, decorative motion, overclaiming at the reveal, and any move that hides the data source — calm, sourced, one-idea-per-screen craft is what earns the share.
