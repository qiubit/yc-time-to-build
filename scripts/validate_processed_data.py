#!/usr/bin/env python3
"""Validate processed JSON artifacts for the static YC wave essay."""

from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

REQUIRED_FILES = [
    "waves_by_batch.json",
    "genai_cross_sector.json",
    "outcome_proxies.json",
    "metadata.json",
]

WAVE_ROW_FIELDS = {
    "mode",
    "batch_order",
    "batch",
    "batch_code",
    "year",
    "season",
    "season_order",
    "wave",
    "count",
    "pct",
    "total_companies",
}

OUTCOME_ROW_FIELDS = {
    "mode",
    "cohort_filter",
    "cohort_label",
    "max_cohort_year",
    "includes_recent_incomplete_cohorts",
    "lagging_incomplete",
    "wave",
    "company_count",
    "top_company_count",
    "top_company_rate",
    "public_count",
    "public_rate",
    "acquired_count",
    "acquired_rate",
    "public_or_acquired_count",
    "public_or_acquired_rate",
    "inactive_count",
    "inactive_rate",
}


def load_json(filename: str) -> dict:
    path = PROCESSED / filename
    if not path.exists():
        raise AssertionError(f"Missing required file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def assert_required_fields(row: dict, required: set[str], label: str) -> None:
    missing = sorted(required - set(row))
    if missing:
        raise AssertionError(f"{label} missing required fields: {', '.join(missing)}")


def assert_rate(value: float, label: str) -> None:
    if not isinstance(value, (int, float)) or math.isnan(value):
        raise AssertionError(f"{label} is not a numeric rate")
    if value < -1e-12 or value > 1 + 1e-12:
        raise AssertionError(f"{label} is outside [0, 1]: {value}")


def validate_waves_by_batch(payload: dict) -> None:
    rows = payload.get("rows")
    if not isinstance(rows, list) or not rows:
        raise AssertionError("waves_by_batch.json must include non-empty rows")

    totals: dict[tuple[str, str], dict[str, float]] = defaultdict(
        lambda: {"count": 0, "pct": 0.0, "total_companies": None}
    )
    modes = set()
    for index, row in enumerate(rows):
        assert_required_fields(row, WAVE_ROW_FIELDS, f"waves_by_batch row {index}")
        modes.add(row["mode"])
        assert_rate(row["pct"], f"waves_by_batch row {index} pct")
        if row["count"] < 0 or row["total_companies"] <= 0:
            raise AssertionError(f"waves_by_batch row {index} has invalid counts")
        expected_pct = row["count"] / row["total_companies"]
        if abs(row["pct"] - expected_pct) > 1e-12:
            raise AssertionError(
                f"waves_by_batch row {index} pct does not match count / total_companies"
            )
        key = (row["mode"], row["batch"])
        totals[key]["count"] += row["count"]
        totals[key]["pct"] += row["pct"]
        totals[key]["total_companies"] = row["total_companies"]

    if modes != {"strict", "broad"}:
        raise AssertionError(f"Expected strict and broad modes, found: {sorted(modes)}")

    for key, aggregate in totals.items():
        if aggregate["count"] != aggregate["total_companies"]:
            raise AssertionError(f"{key} counts do not sum to total_companies")
        if abs(aggregate["pct"] - 1.0) > 1e-9:
            raise AssertionError(f"{key} percentages do not sum to 1.0")


def validate_genai_cross_sector(payload: dict) -> None:
    rows = payload.get("rows")
    if payload.get("mode") != "broad":
        raise AssertionError("genai_cross_sector.json must be broad mode")
    if not isinstance(rows, list) or not rows:
        raise AssertionError("genai_cross_sector.json must include non-empty rows")
    total_count = payload.get("total_genai_companies")
    if not isinstance(total_count, int) or total_count <= 0:
        raise AssertionError("genai_cross_sector.json has invalid total_genai_companies")

    count_sum = 0
    pct_sum = 0.0
    for index, row in enumerate(rows):
        for field in ("mode", "sector", "count", "pct_of_genai_broad"):
            if field not in row:
                raise AssertionError(f"genai row {index} missing {field}")
        if row["mode"] != "broad":
            raise AssertionError(f"genai row {index} must be broad mode")
        assert_rate(row["pct_of_genai_broad"], f"genai row {index} pct_of_genai_broad")
        count_sum += row["count"]
        pct_sum += row["pct_of_genai_broad"]

    if count_sum != total_count:
        raise AssertionError("genai sector counts do not sum to total_genai_companies")
    if abs(pct_sum - 1.0) > 1e-9:
        raise AssertionError("genai sector percentages do not sum to 1.0")


def validate_outcome_proxies(payload: dict) -> None:
    rows = payload.get("rows")
    if not isinstance(rows, list) or not rows:
        raise AssertionError("outcome_proxies.json must include non-empty rows")

    seen_filters = set()
    seen_modes = set()
    for index, row in enumerate(rows):
        assert_required_fields(row, OUTCOME_ROW_FIELDS, f"outcome row {index}")
        seen_modes.add(row["mode"])
        seen_filters.add(row["cohort_filter"])
        if row["lagging_incomplete"] is not True:
            raise AssertionError(f"outcome row {index} must mark lagging_incomplete")
        if row["company_count"] <= 0:
            raise AssertionError(f"outcome row {index} has invalid company_count")
        for count_field in (
            "top_company_count",
            "public_count",
            "acquired_count",
            "public_or_acquired_count",
            "inactive_count",
        ):
            if row[count_field] < 0 or row[count_field] > row["company_count"]:
                raise AssertionError(f"outcome row {index} has invalid {count_field}")
        for rate_field in (
            "top_company_rate",
            "public_rate",
            "acquired_rate",
            "public_or_acquired_rate",
            "inactive_rate",
        ):
            assert_rate(row[rate_field], f"outcome row {index} {rate_field}")

    if seen_modes != {"strict", "broad"}:
        raise AssertionError(f"Expected strict and broad outcome modes: {seen_modes}")
    if seen_filters != {"through_2020", "all_included_batches"}:
        raise AssertionError(f"Unexpected outcome cohort filters: {seen_filters}")


def validate_metadata(payload: dict) -> None:
    source = payload.get("source", {})
    for field in (
        "api_url",
        "repo_url",
        "snapshot_timestamp",
        "included_companies",
        "excluded_batch_labels",
    ):
        if field not in source:
            raise AssertionError(f"metadata source missing {field}")
    if not payload.get("included_batch_labels"):
        raise AssertionError("metadata missing included_batch_labels")
    if not payload.get("methodology_notes"):
        raise AssertionError("metadata missing methodology_notes")
    if not payload.get("caveats"):
        raise AssertionError("metadata missing caveats")


def main() -> int:
    payloads = {filename: load_json(filename) for filename in REQUIRED_FILES}
    validate_waves_by_batch(payloads["waves_by_batch.json"])
    validate_genai_cross_sector(payloads["genai_cross_sector.json"])
    validate_outcome_proxies(payloads["outcome_proxies.json"])
    validate_metadata(payloads["metadata.json"])
    print("Processed data validation passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
