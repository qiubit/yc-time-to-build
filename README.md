# The Golden Window

An interactive visual essay in progress about startup waves in Y Combinator history, and why the current generative AI / agents wave may be unusually fast, broad, and cross-sector.

The project starts from a simple question:

> Is now actually a special time to build, or does it only feel that way?

The plan is to use public YC company data to compare past founder waves, including mobile-enabled commerce, fintech, crypto, and generative AI / agents. The goal is not to build a neutral company explorer. The goal is a thesis-driven visual essay where the data either earns the argument or forces the thesis to change.

## Status

Draft design stage.

Current focus:

- validate the wave taxonomy;
- choose a reproducible public data source;
- build a disposable data prototype;
- test whether the AI wave looks unusually fast and broad before writing production code.

## Project Docs

- [DESIGN.md](./DESIGN.md) — product thesis, data model, wave definitions, essay arc, and build plan.
- [CHANGELOG.md](./CHANGELOG.md) — high-level project evolution notes for a later build/postmortem blog post.

## Tentative Stack

- Static site
- D3.js
- Scrollama.js
- Build-time JSON data
- Playwright for generating social preview imagery
- GitHub Pages for v1 deployment

## Data Direction

ExploreYC is the product inspiration. For the reproducible v1 chart, the current plan is to use a public YC-derived dataset such as [`yc-oss/api`](https://github.com/yc-oss/api), or fall back to a direct scrape of YC's public company directory if needed.

The project treats YC batch composition as evidence of founder attention and category timing, not as proof of market size or eventual startup outcomes.
