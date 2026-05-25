# Processed Data

Static JSON artifacts for the D3/Scrollama essay. These files are generated from
`analysis/spike-yc-waves/output/*.csv` and `summary.json` using:

```sh
python3 scripts/build_processed_data.py
python3 scripts/validate_processed_data.py
```

## Files

- `waves_by_batch.json` - batch-level wave composition for strict and broad
  classification modes. Intended for the stacked area context chart, indexed
  growth curves, small multiples, and the strict/broad toggle.
- `genai_cross_sector.json` - broad-mode background sector shares for companies
  classified as Generative AI / Agents. Intended for the Chapter 4 cross-sector
  bar or mosaic chart.
- `outcome_proxies.json` - lagging and incomplete public outcome proxies by wave
  for both all included batches and mature cohorts through 2020. Intended for
  the outcome-fork chapter, with `through_2020` as the primary chart view.
- `metadata.json` - source URL, snapshot timestamp, included/excluded batches,
  classification notes, methodology notes, and caveats for visible sourcing and
  an appendix/methodology panel.

These artifacts intentionally avoid per-company records so the static site can
load quickly and keep the essay focused on aggregate evidence.
