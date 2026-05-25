#!/usr/bin/env python3
"""Build production JSON data artifacts from the disposable YC wave spike."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPIKE_OUTPUT = ROOT / "analysis" / "spike-yc-waves" / "output"
PROCESSED = ROOT / "data" / "processed"

WAVES = [
    "Web / Social / UGC",
    "Mobile-Enabled Commerce / Marketplaces",
    "Fintech",
    "Crypto / Web3",
    "Generative AI / Agents",
    "Other",
]

MODE_NOTES = {
    "strict": (
        "Tag-only strict read: exact tags, industries, industry, and "
        "subindustry matches only. It likely undercounts recent agent companies."
    ),
    "broad": (
        "Description-aware broad read: strict classification plus conservative "
        "keyword matching on company name, one-liner, and long description. "
        "It better captures current language but is more exposed to metadata drift."
    ),
}

METHODOLOGY_NOTES = [
    (
        "Each company is assigned to exactly one headline wave so stacked area "
        "charts sum to 100% per batch."
    ),
    (
        "Wave precedence is Generative AI / Agents, Crypto / Web3, Fintech, "
        "Mobile-Enabled Commerce / Marketplaces, Web / Social / UGC, then Other."
    ),
    (
        "Generic AI, artificial intelligence, machine learning, computer vision, "
        "robotics, and drug discovery are not enough by themselves to classify a "
        "company as Generative AI / Agents."
    ),
    (
        "Batch composition is treated as a leading indicator of founder attention, "
        "not proof of market size, revenue, valuation, or durable outcomes."
    ),
]

CAVEATS = [
    (
        "YC public tags and one-liners are current profile metadata, not frozen "
        "batch-time descriptions. Older companies can carry newer AI language."
    ),
    (
        "Strict mode likely undercounts newer agent companies; broad mode may "
        "overcount because current profile language drifts toward AI."
    ),
    (
        "Exclusive wave assignment hides overlap. For example, fintech companies "
        "with agent products are counted as Generative AI / Agents because that "
        "wave has precedence."
    ),
    (
        "Outcome proxies are lagging and incomplete. They favor older cohorts and "
        "should not be used to judge 2024-2026 companies."
    ),
    "Early YC batches are tiny, so early percentages are noisy.",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def int_field(row: dict[str, str], key: str) -> int:
    return int(row[key])


def float_field(row: dict[str, str], key: str) -> float:
    return float(row[key])


def load_summary() -> dict:
    return json.loads((SPIKE_OUTPUT / "summary.json").read_text(encoding="utf-8"))


def build_batch_index(rows_by_mode: dict[str, list[dict[str, str]]]) -> dict[str, dict]:
    seen: dict[str, dict] = {}
    for rows in rows_by_mode.values():
        for row in rows:
            batch = row["batch"]
            if batch not in seen:
                seen[batch] = {
                    "batch": batch,
                    "batch_code": row["batch_code"],
                    "year": int_field(row, "year"),
                    "season": row["season"],
                    "season_order": int_field(row, "season_order"),
                    "total_companies": int_field(row, "total_companies"),
                }

    ordered = sorted(seen.values(), key=lambda item: (item["year"], item["season_order"]))
    for index, item in enumerate(ordered):
        item["batch_order"] = index
    return {item["batch"]: item for item in ordered}


def build_waves_by_batch(summary: dict) -> dict:
    rows_by_mode = {
        "strict": read_csv(SPIKE_OUTPUT / "wave_by_batch_strict.csv"),
        "broad": read_csv(SPIKE_OUTPUT / "wave_by_batch_broad.csv"),
    }
    batch_index = build_batch_index(rows_by_mode)

    records = []
    for mode, rows in rows_by_mode.items():
        for row in rows:
            batch = batch_index[row["batch"]]
            records.append(
                {
                    "mode": mode,
                    "batch_order": batch["batch_order"],
                    "batch": row["batch"],
                    "batch_code": row["batch_code"],
                    "year": int_field(row, "year"),
                    "season": row["season"],
                    "season_order": int_field(row, "season_order"),
                    "wave": row["wave"],
                    "count": int_field(row, "count"),
                    "pct": float_field(row, "pct"),
                    "total_companies": int_field(row, "total_companies"),
                }
            )

    records.sort(
        key=lambda row: (
            row["mode"],
            row["batch_order"],
            WAVES.index(row["wave"]) if row["wave"] in WAVES else 999,
        )
    )

    return {
        "schema_version": 1,
        "description": (
            "Batch-level headline wave composition for the static essay. "
            "Rows include both strict and broad classification modes."
        ),
        "source_snapshot": summary["source"]["last_updated"],
        "classification_modes": MODE_NOTES,
        "waves": WAVES,
        "batches": sorted(batch_index.values(), key=lambda item: item["batch_order"]),
        "rows": records,
    }


def build_genai_cross_sector(summary: dict) -> dict:
    rows = [
        {
            "mode": "broad",
            "sector": row["sector"],
            "count": int_field(row, "count"),
            "pct_of_genai_broad": float_field(row, "pct_of_genai_broad"),
        }
        for row in read_csv(SPIKE_OUTPUT / "genai_broad_background_sectors.csv")
    ]
    total = sum(row["count"] for row in rows)
    return {
        "schema_version": 1,
        "description": (
            "Background sector shares among companies classified as Generative AI / "
            "Agents in broad mode. Intended for the cross-sector capability chart."
        ),
        "source_snapshot": summary["source"]["last_updated"],
        "mode": "broad",
        "classification_note": MODE_NOTES["broad"],
        "total_genai_companies": total,
        "rows": rows,
    }


def normalize_outcome_row(row: dict[str, str]) -> dict:
    cohort_filter = row["cohort_filter"]
    return {
        "mode": row["mode"],
        "cohort_filter": cohort_filter,
        "cohort_label": (
            "Mature cohorts through 2020"
            if cohort_filter == "through_2020"
            else "All included batches"
        ),
        "max_cohort_year": 2020 if cohort_filter == "through_2020" else None,
        "includes_recent_incomplete_cohorts": cohort_filter != "through_2020",
        "lagging_incomplete": True,
        "wave": row["wave"],
        "company_count": int_field(row, "company_count"),
        "top_company_count": int_field(row, "top_company_count"),
        "top_company_rate": float_field(row, "top_company_rate"),
        "public_count": int_field(row, "public_count"),
        "public_rate": float_field(row, "public_rate"),
        "acquired_count": int_field(row, "acquired_count"),
        "acquired_rate": float_field(row, "acquired_rate"),
        "public_or_acquired_count": int_field(row, "public_or_acquired_count"),
        "public_or_acquired_rate": float_field(row, "public_or_acquired_rate"),
        "inactive_count": int_field(row, "inactive_count"),
        "inactive_rate": float_field(row, "inactive_rate"),
    }


def build_outcome_proxies(summary: dict) -> dict:
    input_files = [
        "outcome_proxy_by_wave_strict_all.csv",
        "outcome_proxy_by_wave_broad_all.csv",
        "outcome_proxy_by_wave_strict_through_2020.csv",
        "outcome_proxy_by_wave_broad_through_2020.csv",
    ]
    rows = []
    for filename in input_files:
        rows.extend(normalize_outcome_row(row) for row in read_csv(SPIKE_OUTPUT / filename))

    rows.sort(
        key=lambda row: (
            row["mode"],
            row["cohort_filter"],
            WAVES.index(row["wave"]) if row["wave"] in WAVES else 999,
        )
    )
    return {
        "schema_version": 1,
        "description": (
            "Crude outcome proxies by wave. These are lagging, incomplete public "
            "signals and are intended only for the essay's outcome-fork chapter."
        ),
        "source_snapshot": summary["source"]["last_updated"],
        "classification_modes": MODE_NOTES,
        "proxy_fields": [
            "top_company",
            "status = Public",
            "status = Acquired",
            "status = Inactive",
        ],
        "cohort_filters": {
            "through_2020": (
                "Mature cohorts only, used for the primary outcome-proxy chart."
            ),
            "all_included_batches": (
                "All included batches, retained for appendix/context. This includes "
                "young cohorts whose outcomes are not mature."
            ),
        },
        "lagging_incomplete": True,
        "caveat": (
            "Do not interpret these as final success rates, especially for "
            "2021-2026 cohorts."
        ),
        "rows": rows,
    }


def build_metadata(summary: dict) -> dict:
    wave_rows = read_csv(SPIKE_OUTPUT / "wave_by_batch_broad.csv")
    batch_index = build_batch_index({"broad": wave_rows})
    included_batches = sorted(batch_index.values(), key=lambda item: item["batch_order"])

    return {
        "schema_version": 1,
        "description": "Source, snapshot, methodology, and caveats for processed data.",
        "source": {
            "name": "yc-oss/api",
            "api_url": summary["source"]["yc_oss_api"],
            "repo_url": summary["source"]["yc_oss_readme"],
            "snapshot_timestamp": summary["source"]["last_updated"],
            "downloaded_companies": summary["source"]["downloaded_companies"],
            "included_companies": summary["source"]["included_companies"],
            "included_batch_count": summary["source"]["included_batches"],
            "excluded_batch_labels": summary["source"]["excluded_batches"],
        },
        "included_batch_labels": [item["batch"] for item in included_batches],
        "included_batches": included_batches,
        "classification_modes": MODE_NOTES,
        "waves": WAVES,
        "methodology_notes": METHODOLOGY_NOTES,
        "caveats": CAVEATS,
        "outcome_proxy_note": (
            "Outcome proxies use public yc-oss/api fields only: top_company and "
            "status values Public, Acquired, and Inactive. They are lagging and "
            "incomplete, so mature cohorts through 2020 should be the primary view."
        ),
        "spike_inputs": {
            "summary": "analysis/spike-yc-waves/output/summary.json",
            "wave_by_batch": [
                "analysis/spike-yc-waves/output/wave_by_batch_strict.csv",
                "analysis/spike-yc-waves/output/wave_by_batch_broad.csv",
            ],
            "genai_cross_sector": (
                "analysis/spike-yc-waves/output/genai_broad_background_sectors.csv"
            ),
            "outcome_proxies": [
                "analysis/spike-yc-waves/output/outcome_proxy_by_wave_strict_all.csv",
                "analysis/spike-yc-waves/output/outcome_proxy_by_wave_broad_all.csv",
                "analysis/spike-yc-waves/output/outcome_proxy_by_wave_strict_through_2020.csv",
                "analysis/spike-yc-waves/output/outcome_proxy_by_wave_broad_through_2020.csv",
            ],
        },
    }


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    summary = load_summary()

    artifacts = {
        "waves_by_batch.json": build_waves_by_batch(summary),
        "genai_cross_sector.json": build_genai_cross_sector(summary),
        "outcome_proxies.json": build_outcome_proxies(summary),
        "metadata.json": build_metadata(summary),
    }
    for filename, payload in artifacts.items():
        write_json(PROCESSED / filename, payload)

    print(f"Wrote {len(artifacts)} processed data artifacts to {PROCESSED}")


if __name__ == "__main__":
    main()
