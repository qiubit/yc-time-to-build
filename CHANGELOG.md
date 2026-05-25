# Changelog

High-level notes on how this project evolves. This is meant to support a later blog post about the iteration process, not to duplicate commit history.

## 2026-05-25

### Reframed the Core Thesis

- Started from a broad claim: the agentic AI wave is the biggest startup opportunity since the internet.
- Tightened the claim into something the data can plausibly support: YC history shows several founder waves, and generative AI / agents may be unusually fast, broad, and cross-sector.
- Added an explicit distinction between what YC batch composition can show (founder attention, concentration, speed, cross-sector spread) and what it cannot prove by itself (durable opportunity, market size, startup outcomes).

### Critiqued the Initial Design

- Evaluated `DESIGN.md` as a pre-build gate rather than a generic concept note.
- Identified the biggest risks:
  - the thesis was too strong for the available data;
  - "agentic AI," "AI/ML," and "AI-native" were being mixed together;
  - a stacked area chart alone might not prove "larger, faster, broader";
  - taxonomy work was likely the real project risk;
  - the "cost of waiting" section likely required outcome data outside YC's public directory.

### Validated and Revised the Wave Set

- Replaced the initial comparator set of mobile, SaaS, and crypto with a more defensible set:
  - Web / Social / UGC as a prologue wave;
  - Mobile-Enabled Commerce / Marketplaces as the main historical durable-company benchmark;
  - Fintech as a clean measurable durable-company benchmark;
  - Crypto / Web3 as a hype benchmark rather than a durable-company benchmark;
  - Generative AI / Agents as the thesis wave.
- Demoted SaaS / B2B from a headline wave to background context because it behaves more like the substrate of modern YC than a clean rise-peak-fade wave.
- Reframed mobile as mobile-enabled commerce / marketplaces because the important companies were often tagged as commerce, marketplace, delivery, logistics, or local services rather than "mobile."

### Clarified Data Sources

- Corrected the meaning of ExploreYC: it refers to the live product at https://www.exploreyc.com/, not necessarily a clean open dataset.
- Added `yc-oss/api` as the preferred reproducible data layer for v1 if ExploreYC does not expose a stable normalized dataset.
- Added methodology caveats around using current/public YC tags and one-liners, since they are not a frozen record of how companies described themselves during their YC batches.
- Added a required sensitivity check: compare strict tag-only classification against broader tag + one-liner keyword classification.

### Updated `DESIGN.md`

- Rewrote the problem statement and "What Makes This Cool" sections around a more defensible thesis.
- Added a `Validated Wave Set` section.
- Updated the data model from category-first to wave-first.
- Added v1 wave definitions and background-sector categories for cross-sector spread.
- Rewrote the proposed essay arc around durable waves, cautionary crypto, and the current generative AI / agents wave.
- Updated open questions, success criteria, next steps, and the final assignment to match the new direction.
