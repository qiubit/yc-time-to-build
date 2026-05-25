# Changelog

High-level notes on how this project evolves. This is meant to support a later blog post about the iteration process, not to duplicate commit history.

## 2026-05-25

### Tightened the Pre-Build Editorial Spine

- Revised the thesis from "different" to a more specific claim: YC founders are treating generative AI / agents as both a company category and a capability layer across many other categories.
- Softened outcome-adjacent language from "formation is proven" to "the formation signal is strong."
- Reframed strict vs. broad classification as a range: strict likely undercounts recent agent companies, while broad may overcount because current public descriptions drift toward AI language.
- Strengthened the Chapter 5 fork from two paths to three: fintech/commerce-style durability, crypto-like narrowness, or a substrate future where "AI company" stops being a useful label.
- Added concrete on-screen copy for the Chapter 4 reveal and Chapter 5 fork before production UI begins.

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

### Ran the Disposable YC Wave Validation Spike

- Pulled `yc-oss/api` company data and built a reproducible prototype under `analysis/spike-yc-waves/`.
- Confirmed the public schema has the needed fields: company name, batch, industries, tags, one-liner, long description, `status`, and `top_company`.
- Ran strict tag/industry classification and broader tag/industry + description keyword classification.
- Found directional support for the GenAI / Agents thesis:
  - strict mode shows a real GenAI / Agents wave, peaking at 23.4% of Winter 2023;
  - broad mode shows a much larger current wave, reaching 46.5% of Spring 2026;
  - crypto remains narrow in YC batch composition, peaking below 10% in both modes.
- Tightened the thesis boundary: the data supports "across many major YC categories" better than the literal phrase "inside every category."
- Recommended indexed growth curves as the main essay chart, with small multiples and a GenAI cross-sector chart as supporting proof.
- Added an outcome-proxy layer for the next narrative question: whether AI/agents matures more like fintech/commerce or stays narrower like crypto. The available public fields can frame the fork with `top_company`, `Public`, `Acquired`, and `Inactive`, but cannot settle it for young cohorts.
