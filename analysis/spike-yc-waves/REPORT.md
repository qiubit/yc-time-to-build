# YC Wave Validation Spike

Run date: 2026-05-25  
Status: disposable data prototype, not production UI

## Verdict

The thesis mostly survives, but the wording should be tightened.

Public YC company metadata supports the claim that generative AI / agents is an unusually fast and broad founder-attention wave. It does **not** cleanly support the literal phrase "inside every category." A safer thesis is:

> YC history shows several founder waves, but generative AI / agents is unusual because it is becoming both a category and a capability across many major YC categories.

## Data Source

Primary source: `yc-oss/api`

- API: https://yc-oss.github.io/api/companies/all.json
- Repo/readme: https://github.com/yc-oss/api
- Metadata timestamp in downloaded file: `2026-05-25T02:36:05.148Z`
- Downloaded companies: 5,926
- Included companies: 5,916
- Included batches: 46
- Excluded labels: `Unspecified`, `Summer 2026`, `Fall 2026`, `Winter 2027`

ExploreYC was inspected as product inspiration, but I did not find a stable, versioned open dataset suitable for this reproducible spike.

## Schema Notes

The `yc-oss/api` company records include the fields needed for this prototype:

- Identity and batch: `id`, `name`, `slug`, `batch`, `url`, `website`
- Descriptions: `one_liner`, `long_description`
- Taxonomy: `industry`, `subindustry`, `industries`, `tags`, `tags_highlighted`
- Status/proxy fields: `status`, `top_company`, `isHiring`, `nonprofit`, `team_size`
- Outcome-ish values present in this snapshot: `status = Active / Inactive / Acquired / Public`; no separate `exited` boolean was present.

Included snapshot status counts:

- Active: 4,077
- Inactive: 1,035
- Acquired: 781
- Public: 23
- Top company: 91

## Methodology

The script classifies each company into exactly one headline wave so the stacked area chart sums to 100% per batch. Precedence is:

1. Generative AI / Agents
2. Crypto / Web3
3. Fintech
4. Mobile-Enabled Commerce / Marketplaces
5. Web / Social / UGC
6. Other

Two classification modes were run:

- **Strict:** exact `tags`, `industries`, `industry`, and `subindustry` matches only.
- **Broad:** strict rules plus conservative keyword matching on `name`, `one_liner`, and `long_description`.

Generic `AI`, `Artificial Intelligence`, `Machine Learning`, computer vision, robotics, and drug discovery are **not** enough to classify a company as Generative AI / Agents.

## Wave Definitions

**Web / Social / UGC:** social, community, messaging, content, media, video, creator, reviews, UGC.

**Mobile-Enabled Commerce / Marketplaces:** marketplace, e-commerce, delivery, logistics, retail, restaurant tech, grocery, travel, local services, on-demand commerce.

**Fintech:** fintech, payments, banking, lending, credit, payroll, insurance, investing, asset management.

**Crypto / Web3:** crypto, blockchain, Web3, DeFi, NFT, DAO.

**Generative AI / Agents:** generative AI, AI assistants, conversational AI, AI agents, agentic software, copilots, LLM apps, ChatGPT/GPT language, voice AI, AI scribes/receptionists.

## Top Findings

1. **Strict mode shows a real GenAI / Agents wave, but probably undercounts recent agent companies.**  
   Strict GenAI / Agents peaks at **23.4% in Winter 2023**: 64 of 274 companies. It is **12.8% in Spring 2026**: 22 of 172 companies.

2. **Broad mode shows the current agent wave as the strongest recent composition shift.**  
   Broad GenAI / Agents reaches **46.5% in Spring 2026**: 80 of 172 companies. That exceeds broad fintech's peak of **26.9% in Summer 2021** and broad crypto's peak of **7.3% in Summer 2022**.

3. **Crypto is visibly narrow in YC batch composition.**  
   In both modes, Crypto / Web3 never reaches 10% of a batch. Its broad peak is **7.3% in Summer 2022**.

4. **Mobile-enabled commerce / marketplaces remains the best historical comparator.**  
   Broad mode gives it a high-water mark of **40.0% in Winter 2011**, while strict mode peaks at **34.8% in Winter 2013**. Early batch sizes were much smaller, so use this as a shape comparison rather than a hard magnitude comparison.

5. **The "capability inside categories" claim is directionally supported but concentrated.**  
   Among broad GenAI / Agent-classified companies, background sectors are:
   - B2B / Enterprise: 46.8%
   - Developer Tools / Infrastructure: 23.8%
   - Fintech: 11.1%
   - Healthcare: 8.1%
   - Consumer / Media / Education: 6.7%

   This supports "cross-sector," especially across B2B, developer tools, fintech, healthcare, and consumer/media/education. It does not justify "every category" literally.

## Crypto Fork vs Durable Wave Fork

The next strategic question is not "is there an AI/agents wave?" The data says yes. The next question is whether it matures like commerce/fintech or stays more like crypto: visible, important, but narrower and harder to translate into durable YC outcomes.

This spike now includes a crude outcome-proxy layer using only public fields available in `yc-oss/api`:

- `top_company`
- `status = Public`
- `status = Acquired`
- `status = Inactive`

These are lagging indicators and should not be used to judge 2024-2026 companies yet. To avoid over-reading young cohorts, the script emits both all-batch views and mature-cohort views through 2020.

Broad mode, all included batches:

| Wave | Companies | Top Company Rate | Public/Acquired Rate | Inactive Rate |
| --- | ---: | ---: | ---: | ---: |
| Web / Social / UGC | 670 | 1.6% | 20.6% | 29.6% |
| Mobile-Enabled Commerce / Marketplaces | 945 | 2.1% | 15.6% | 25.8% |
| Fintech | 937 | 2.3% | 14.2% | 13.0% |
| Crypto / Web3 | 171 | 1.2% | 15.2% | 17.5% |
| Generative AI / Agents | 1,072 | 0.1% | 5.0% | 5.4% |

Broad mode, mature cohorts only through 2020:

| Wave | Companies | Top Company Rate | Public/Acquired Rate | Inactive Rate |
| --- | ---: | ---: | ---: | ---: |
| Web / Social / UGC | 429 | 2.6% | 28.2% | 39.9% |
| Mobile-Enabled Commerce / Marketplaces | 579 | 3.3% | 21.6% | 34.2% |
| Fintech | 382 | 5.8% | 25.4% | 18.1% |
| Crypto / Web3 | 72 | 2.8% | 20.8% | 20.8% |
| Generative AI / Agents | 101 | 1.0% | 15.8% | 7.9% |

Interpretation:

- The formation signal for GenAI / Agents is strong, but the outcome signal is not mature enough to call.
- Fintech currently looks like the cleanest "successful wave" comparator in public YC fields: high top-company rate and relatively low inactive rate in mature cohorts.
- Commerce/marketplaces has many visible outcomes, but also high inactivity, partly because it includes older, noisier consumer/local/marketplace attempts.
- Crypto does not look like a giant YC batch-composition wave, but its mature-cohort outcome proxy is not obviously terrible in this simple data. The better critique is "narrower than the cultural hype," not "all failed."
- A production essay can frame AI/agents honestly as an open fork: the wave is unusually large and broad now; whether it becomes fintech-like or crypto-like requires outcome data over time.

## Caveats

- YC public tags and one-liners are current profile metadata, not frozen batch-time descriptions. Some old-batch companies now carry current AI/agent language, which can make the wave appear to start earlier than it really did.
- Strict tags are inconsistent for newer agent companies. Many recent companies describe agents or LLMs in one-liners but lack a `Generative AI` or `AI Assistant` tag.
- The exclusive wave assignment is useful for stacked area charts, but it hides overlap. For example, a fintech company with an AI-agent product becomes GenAI / Agents because that wave has precedence.
- Batch composition shows founder attention, speed, concentration, and spread. It does not prove market size, durability, revenue, valuation, or outcomes.
- Outcome proxies are lagging and incomplete. `top_company`, `Public`, and `Acquired` are useful signals, but they are not a full success metric and strongly favor older cohorts.
- Early YC batches are tiny; Web / Social / UGC and early commerce percentages are noisy.
- The downloaded data had tiny future/incomplete labels (`Summer 2026`, `Fall 2026`, `Winter 2027`) as of 2026-05-25. They were excluded.

## Chart Artifacts

- `output/stacked_area_strict.png`
- `output/stacked_area_broad.png`
- `output/indexed_growth_strict.png`
- `output/indexed_growth_broad.png`
- `output/small_multiples_strict.png`
- `output/small_multiples_broad.png`
- `output/genai_broad_background_sectors.png`
- `output/outcome_proxy_broad_all_included_batches.png`
- `output/outcome_proxy_broad_through_2020.png`

Data outputs:

- `output/wave_by_batch_strict.csv`
- `output/wave_by_batch_broad.csv`
- `output/classified_companies.csv`
- `output/genai_broad_background_sectors.csv`
- `output/outcome_proxy_by_wave_strict_all.csv`
- `output/outcome_proxy_by_wave_broad_all.csv`
- `output/outcome_proxy_by_wave_strict_through_2020.csv`
- `output/outcome_proxy_by_wave_broad_through_2020.csv`
- `output/summary.json`

## Best Chart Type For The Story

Use **indexed growth curves** as the main essay chart. They best communicate "this wave is moving faster" in one glance.

Use **small multiples** as the trust-building companion because they reveal each wave's shape without the stacked area's visual competition.

Use the **stacked area chart** for historical context, not as the core proof. It is attractive, but the mutually exclusive categories and large `Other` bucket make it less precise for the "AI as capability" claim.

For the "category and capability" claim, add a dedicated **GenAI cross-sector bar chart or mosaic** in production. The headline wave chart alone cannot carry that part of the thesis.

For the "crypto or durable wave?" question, use **outcome proxy bars only as a later chapter or caveat panel**, not as the hook. The honest story is that AI/agents has formation evidence now and outcome uncertainty by design.

## Recommendation

Proceed to the narrative outline, but revise the thesis sentence before production build:

> YC history shows several founder waves, but generative AI / agents is unusual because it is becoming both a category and a capability across many major startup categories.

Do not claim that YC data proves this is the biggest opportunity or that AI is literally inside every category. The data is strong enough for a founder-attention essay; it is not outcome evidence.
