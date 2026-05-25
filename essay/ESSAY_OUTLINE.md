# Essay Outline: Time To Build

Narrative spine for the interactive visual essay. This is the gate before the production build (Step 2 of the `DESIGN.md` next steps). Not UI, not code — the argument and the order it lands in.

Data source: `yc-oss/api` (reproducible evidence layer). ExploreYC is product inspiration only. All numbers below trace to `analysis/spike-yc-waves/REPORT.md` and its CSV/JSON outputs.

---

## Thesis Sentence

> YC history shows several founder waves, but generative AI / agents is unusual: YC founders are treating it as both a company category and a capability layer across many other categories.

One sentence, no hedging. What it deliberately does **not** claim: that this is the biggest opportunity in startup history, that AI lives inside *every* category, or that the outcomes are proven. The essay earns the founder-attention claim and stays honest about the outcome question.

### The narrative fork (the essay's spine, not a footnote)

> AI / agents has a strong founder-formation signal right now. The outcome question is still open: does it mature like fintech and commerce, stay narrower like crypto, or become such a broad substrate that "AI company" stops being a useful label?

The fork is what makes the thesis defensible. The essay shows a strong *formation* signal, then refuses to fake *outcome* evidence it doesn't have. That refusal is what earns the reader's trust.

---

## The Shareable "Whoa" Moment

**Chapter 4's reveal: the indexed growth curve of generative AI / agents pulling away from prior YC waves, then splitting to show it isn't one sector — it's concentrated in B2B and dev tools, but also visible across fintech, healthcare, and consumer/media/education.**

The tweet this is designed to produce is not "cool chart." It is permission: *"This is the thing I'm sending anyone who asks me if this is a real moment to build into."* The screenshot must land in under 5 seconds with no caption: a single line pulling away from the pack, annotated with one number (broad mode, 46.5% of Spring 2026), is the `og:image`.

Why this moment and not the stacked area: the stacked area is pretty but its big `Other` bucket and mutually-exclusive categories blunt the "faster and broader" claim. The indexed curve says "faster" in one glance; the sector split says "broader" in the next.

---

## Chart Inventory (mapped to the spike's recommendation)

| Role | Chart | Source artifact |
| --- | --- | --- |
| Main proof | Indexed growth curves (broad, strict toggle) | `indexed_growth_broad.png` |
| Trust companion | Small multiples per wave | `small_multiples_broad.png` |
| Historical context | Stacked area | `stacked_area_broad.png` |
| "Capability" claim | GenAI cross-sector bars / mosaic | `genai_broad_background_sectors.png` |
| The fork | Outcome-proxy bars (mature cohorts ≤2020) | `outcome_proxy_broad_through_2020.png` |

---

## The Six Chapters

Each chapter lists: the chart, what the reader believes walking in, and what they believe walking out. The before→after deltas are the actual design target — if a chapter doesn't move the belief, it gets cut.

### Chapter 1 — Hook: "Waves have come before"

- **Chart:** Stacked area of all waves across 46 batches, animating in. Minimal text, full-bleed. The AI band is visible but not yet explained.
- **Before:** "Maybe now is special, maybe it just feels that way. Everyone says their moment is the big one."
- **After:** "YC's 20-year history is genuinely made of distinct waves — this is a real pattern, not hype. I want to see where the current one fits."
- **Job:** Establish that founder waves are a real, observable thing before making any claim about *this* one. Disarm the reader's "every generation thinks it's special" reflex by showing the prior waves first.

### Chapter 2 — The durable waves: commerce and fintech

- **Chart:** Small multiples spotlighting Mobile-Enabled Commerce / Marketplaces (broad peak 40.0% in Winter 2011) and Fintech (broad peak 26.9% in Summer 2021). A light outcome annotation: fintech's mature-cohort top-company rate of 5.8%.
- **Before:** "Waves exist, but do they actually produce anything, or just noise?"
- **After:** "Real platform shifts created durable companies. Commerce and fintech are the bar a wave has to clear — and outcomes take years to show up, so I should be patient about judging young waves."
- **Job:** Set the durable-wave benchmark *and* pre-load the caveat that outcomes lag formation. This is what makes the fork honest later.

### Chapter 3 — The cautionary wave: crypto

- **Chart:** Small multiple for Crypto / Web3, shown against commerce and fintech. The punchline number: crypto never crosses 10% of any batch (broad peak 7.3%, Summer 2022).
- **Before:** "Crypto was huge — surely it's one of the biggest YC waves."
- **After:** "Inside YC, crypto was narrower than its cultural footprint. A loud wave is not automatically a broad founder wave. This essay is willing to complicate its own story."
- **Job:** Build trust by letting the chart undercut a popular assumption. Crucial framing: crypto's mature outcome proxies aren't catastrophic (20.8% public/acquired) — the honest critique is "narrower than the hype," not "it failed." A reader who sees the essay resist an easy dunk will trust the AI chapter more.

### Chapter 4 — The current wave: category AND capability layer (the reveal)

- **Chart:** Indexed growth curve — generative AI / agents pulling ahead of prior waves — then a transition into the cross-sector bar/mosaic. Strict/broad toggle visible here so the reader controls the conservative vs. current view.
- **Before:** "There are a lot of AI startups right now."
- **After:** "It's not just *more* AI companies — generative AI / agents is one of the strongest and fastest-forming recent waves in the public YC data, especially under the broad classification, AND it's showing up across B2B (46.8%), dev tools (23.8%), fintech (11.1%), healthcare (8.1%), and consumer/media/education (6.7%). It's a company category and a capability layer at the same time."
- **Job:** Deliver the thesis. Two beats: (1) "faster" via the breakaway curve, (2) "broader" via the sector split. The strict/broad toggle is the integrity move — strict peaks at 23.4% (Winter 2023), broad reaches 46.5% (Spring 2026). Showing both says the signal survives a conservative tag-only read, while the broader read better captures how recent companies describe themselves.
- **This is the shareable moment.**

#### Suggested on-screen copy

Main screen:

> This is the shift.  
> AI / agents is no longer just a YC category.  
> It is becoming a building block inside other categories.

Curve annotation:

> Broad read: 46.5% of Spring 2026 matched GenAI / agents signals  
> Strict read: smaller, but still a visible wave

Cross-sector screen:

> Not just "AI startups."  
> B2B, dev tools, fintech, healthcare, and consumer companies are using the same new primitive.

Quiet caveat:

> Strict reads tags. Broad also reads descriptions. The real signal lives between them.

### Chapter 5 — The fork: open question, honestly drawn

- **Chart:** Outcome-proxy bars, mature cohorts through 2020 only, with young cohorts visibly grayed out / withheld. Fintech/commerce, crypto, and "substrate" framed as three possible futures.
- **Before:** "Okay, the AI wave is real and broad — so it's obviously going to be huge."
- **After:** "The formation signal is strong; outcomes are not known, and can't be yet. The real question is whether AI / agents matures like fintech/commerce, stays narrower like crypto, or becomes so widely adopted that 'AI company' stops being the right category. I respect that this essay won't fake the answer."
- **Job:** Convert the data's biggest weakness (no mature outcome data for 2023–2026 cohorts) into the essay's most credible moment. The fork is a feature: it's the difference between an argument and a pitch.

#### Suggested on-screen copy

Opening screen:

> This is where the data stops pretending.

Main fork:

> YC batch composition can show where founders are rushing.  
> It cannot yet show which 2024-2026 companies will endure.

Fork labels:

> Path A: fintech / commerce  
> Broad formation becomes durable companies.

> Path B: crypto  
> A loud wave stays narrower than its cultural footprint.

> Path C: substrate  
> AI becomes so normal that the best "AI companies" stop looking like AI companies at all.

Closing line:

> The leading indicator is flashing. The outcome evidence has not had time to exist.

### Chapter 6 — The call: the window is open

- **Chart:** Callback to the Chapter 4 indexed curve, now with a "you are here" marker at the current batch.
- **Before:** "Interesting. So what?"
- **After:** "Formation waves are when founders commit before the market settles. The evidence says this is one of the fastest and broadest recent YC founder-attention waves. If I'm going to build, the leading indicator says this is a real moment — and I know exactly what the data does and doesn't promise."
- **Job:** Turn the argument into action without overclaiming. CTA: apply to YC / start building, plus a link to deeper exploration (the backlogged agent/explorer fork). The call rests on the strong *formation* signal — never on an *outcome* claim, which is open.

---

## Belief Arc (one line)

Skeptic ("now just feels special") → "waves are real" (1) → "real waves build durable things, slowly" (2) → "loud does not always mean broad; I trust this source" (3) → "AI is unusually fast and cross-sector" (4) → "the formation signal is strong, outcomes are honestly open" (5) → "the leading indicator says this is a real moment to build into" (6).

---

## Key Caveats (must appear in the essay, not buried in an appendix)

These are load-bearing for credibility. Recommended placement noted.

1. **Metadata drift.** YC tags and one-liners are *current* public profile data, not a frozen record of what each company called itself during its batch. Some old companies now carry AI language, which can make the wave look like it started earlier than it did. → Disclose inline at the Chapter 4 reveal (the strict/broad toggle is the visible form of this caveat).
2. **Strict vs. broad is a real range, not a trick.** Strict uses exact tags and industries, so it likely undercounts recent agent companies. Broad adds keyword matching on name, one-liner, and description, so it may overcount because current profile language drifts toward AI. The truth is somewhere in the band. → The toggle itself carries this; one sentence of explanation on first use.
3. **Exclusive wave assignment hides overlap.** Each company is counted in exactly one wave by precedence (GenAI first), so a fintech-with-an-AI-agent counts as GenAI. This is what *enables* the stacked area but it understates fintech and overstates the AI headline slightly. → Footnote-style panel near Chapter 4.
4. **Formation ≠ outcomes.** Batch composition shows founder attention, speed, concentration, and spread. It does not prove market size, durability, revenue, valuation, or success. → This is the entire premise of Chapter 5; state it explicitly there.
5. **Outcome proxies are lagging and favor old cohorts.** `top_company`, `Public`, `Acquired`, `Inactive` are crude and meaningless for 2024–2026 companies. → Enforced by showing only ≤2020 mature cohorts in Chapter 5; say so on the chart.
6. **Early batches are tiny and noisy.** Pre-2011 percentages swing on small numbers. → Annotate the left edge of the timeline; don't lean on early-era magnitudes for hard claims.

---

## What Would Break This Essay (failure modes to design against)

- **Overclaiming in Chapter 4.** If the headline reads "AI is in every category," a skeptic finds the 46.8%-B2B concentration and discards the whole piece. Say "many major categories," show the actual split.
- **Hiding the fork.** If Chapter 5 is cut to a caveat panel, the essay becomes a pitch and loses the data-skeptical reader (a stated success criterion). The fork is a chapter, not a footnote.
- **Leading with outcomes.** Outcome-proxy bars as the hook would invite "you can't prove that" immediately. They belong in Chapter 5, after formation is established.
- **Stacked area as the proof chart.** Its `Other` bucket and exclusive categories make "faster and broader" hard to read in 5 seconds. It's context (Ch.1), not proof (Ch.4).

---

## Open Questions Resolved Here (from DESIGN.md)

- **Thesis sentence (Q1):** finalized above — "a company category and a capability layer across many other categories," fork explicit.
- **Methodology in essay vs. appendix (Q2):** the strict/broad *toggle* lives in the main essay (Ch.4) as an interactive integrity move; the full methodology note goes to an appendix link.
- **Fork as full chapter or caveat panel (Q3):** full chapter (Ch.5). It's the credibility keystone.
- **"Cost of waiting" section (Q4):** cut from v1. YC directory data can't support it; it needs outcome/funding data from outside the public directory. Backlog.

---

## Next Step

This outline gates the production build (Step 4 in `DESIGN.md`). Before building: a 1-2 hour reference study (Step 3 — Nicky Case pacing, The Pudding format, Ciechanowski embedded-sim craft) to produce a one-paragraph style note. Then port the spike's batch-by-wave percentages to the JSON schema and build the scroll prototype with indexed growth as the primary chart.
