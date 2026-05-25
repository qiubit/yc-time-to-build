#!/usr/bin/env python3
"""Disposable YC wave validation spike.

Inputs:
  data/raw/yc-oss-companies-all.json
  data/raw/yc-oss-meta.json

Outputs:
  analysis/spike-yc-waves/output/*
"""

from __future__ import annotations

import csv
import json
import math
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parent / ".mplconfig"))

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SPIKE_DIR = ROOT / "analysis" / "spike-yc-waves"
RAW_COMPANIES = ROOT / "data" / "raw" / "yc-oss-companies-all.json"
RAW_META = ROOT / "data" / "raw" / "yc-oss-meta.json"
OUT = SPIKE_DIR / "output"

WAVES = [
    "Web / Social / UGC",
    "Mobile-Enabled Commerce / Marketplaces",
    "Fintech",
    "Crypto / Web3",
    "Generative AI / Agents",
    "Other",
]

COLORS = {
    "Web / Social / UGC": "#4E79A7",
    "Mobile-Enabled Commerce / Marketplaces": "#F28E2B",
    "Fintech": "#59A14F",
    "Crypto / Web3": "#B07AA1",
    "Generative AI / Agents": "#E15759",
    "Other": "#BAB0AC",
}

SEASON_ORDER = {
    "Winter": 0,
    "Spring": 1,
    "Summer": 2,
    "Fall": 3,
}

# The downloaded data includes tiny future placeholder batches as of 2026-05-25,
# plus one company with an Unspecified batch. Keep the spike on normal, public
# batch labels through the current/visible Spring 2026 batch.
EXCLUDED_BATCHES = {"Unspecified", "Summer 2026", "Fall 2026", "Winter 2027"}


STRICT_RULES = {
    "Generative AI / Agents": {
        "tags": {
            "Generative AI",
            "AI Assistant",
            "Conversational AI",
            "Smart Home Assistants",
        },
        "industries": set(),
    },
    "Crypto / Web3": {
        "tags": {
            "Crypto / Web3",
            "Blockchain",
            "Web3",
            "DeFi",
            "NFT",
            "DAO",
        },
        "industries": {
            "Banking and Exchange",
        },
    },
    "Fintech": {
        "tags": {
            "Fintech",
            "Payments",
            "Finance",
            "Insurance",
            "Neobank",
            "Investing",
            "Payroll",
            "Lending",
            "Credit",
            "Asset Management",
        },
        "industries": {
            "Fintech",
            "Finance and Accounting",
            "Payments",
            "Consumer Finance",
            "Credit and Lending",
            "Banking and Exchange",
            "Insurance",
            "Asset Management",
        },
    },
    "Mobile-Enabled Commerce / Marketplaces": {
        "tags": {
            "Marketplace",
            "E-commerce",
            "E-Commerce",
            "Delivery",
            "Logistics",
            "Supply Chain",
            "Retail",
            "Retail Tech",
            "Food Tech",
            "Grocery",
            "Restaurant Tech",
            "Travel",
            "Local Services",
            "Transportation",
            "Proptech",
            "Real Estate",
        },
        "industries": {
            "Retail",
            "Supply Chain and Logistics",
            "Food and Beverage",
            "Travel, Leisure and Tourism",
            "Transportation Services",
            "Housing and Real Estate",
            "Real Estate and Construction",
        },
    },
    "Web / Social / UGC": {
        "tags": {
            "Social",
            "Social Media",
            "Messaging",
            "Community",
            "Content",
            "Media",
            "Video",
            "Entertainment",
            "Creator Economy",
            "Reviews",
            "Blogging",
            "Photo Sharing",
            "News",
        },
        "industries": {
            "Social",
            "Content",
            "Gaming",
        },
    },
}

# Precedence makes the stacked chart sum to 100%. GenAI wins first because the
# thesis asks whether it cuts across otherwise normal categories.
PRECEDENCE = [
    "Generative AI / Agents",
    "Crypto / Web3",
    "Fintech",
    "Mobile-Enabled Commerce / Marketplaces",
    "Web / Social / UGC",
]

BROAD_KEYWORDS = {
    "Generative AI / Agents": [
        r"\bgenerative ai\b",
        r"\bgenai\b",
        r"\bgen ai\b",
        r"\bai agent(s)?\b",
        r"\bagentic\b",
        r"\bagentic ai\b",
        r"\bagent(s)?\b.*\bworkflow(s)?\b",
        r"\bautonomous agent(s)?\b",
        r"\bllm(s)?\b",
        r"\blarge language model(s)?\b",
        r"\bcopilot(s)?\b",
        r"\bco-pilot(s)?\b",
        r"\bai assistant(s)?\b",
        r"\bchatgpt\b",
        r"\bgpt[- ]?[345o]?\b",
        r"\bvoice ai\b",
        r"\bai scribe(s)?\b",
        r"\bai receptionist(s)?\b",
    ],
    "Crypto / Web3": [
        r"\bcrypto\b",
        r"\bblockchain\b",
        r"\bweb3\b",
        r"\bdefi\b",
        r"\bnft(s)?\b",
        r"\bdao(s)?\b",
    ],
    "Fintech": [
        r"\bfintech\b",
        r"\bpayment(s)?\b",
        r"\bbanking\b",
        r"\bbank(s)?\b",
        r"\blending\b",
        r"\bloan(s)?\b",
        r"\bpayroll\b",
        r"\binsurance\b",
        r"\binvesting\b",
        r"\basset management\b",
        r"\bcredit\b",
    ],
    "Mobile-Enabled Commerce / Marketplaces": [
        r"\bmarketplace(s)?\b",
        r"\be-?commerce\b",
        r"\bdelivery\b",
        r"\blogistics\b",
        r"\bsupply chain\b",
        r"\bgrocery\b",
        r"\brestaurant(s)?\b",
        r"\bretail\b",
        r"\btravel\b",
        r"\blocal service(s)?\b",
        r"\bon-?demand\b",
    ],
    "Web / Social / UGC": [
        r"\bsocial\b",
        r"\bcommunity\b",
        r"\bmessaging\b",
        r"\bchat\b",
        r"\buser generated\b",
        r"\bugc\b",
        r"\bcreator(s)?\b",
        r"\bcontent\b",
        r"\bmedia\b",
        r"\bvideo\b",
        r"\breview(s)?\b",
    ],
}

BACKGROUND_SECTOR_RULES = [
    ("Fintech", {"Fintech", "Payments", "Finance and Accounting", "Consumer Finance", "Credit and Lending", "Banking and Exchange", "Insurance", "Asset Management"}),
    ("Healthcare", {"Healthcare", "Healthcare IT", "Consumer Health and Wellness", "Healthcare Services", "Therapeutics", "Drug Discovery and Delivery", "Diagnostics", "Medical Devices"}),
    ("Developer Tools / Infrastructure", {"Engineering, Product and Design", "Infrastructure", "Security"}),
    ("B2B / Enterprise", {"B2B", "Operations", "Productivity", "Sales", "Marketing", "Human Resources", "Recruiting and Talent", "Office Management"}),
    ("Commerce / Marketplace / Logistics", {"Retail", "Supply Chain and Logistics", "Food and Beverage", "Travel, Leisure and Tourism", "Transportation Services"}),
    ("Consumer / Media / Education", {"Consumer", "Social", "Content", "Education", "Gaming", "Home and Personal"}),
    ("Industrials / Hard Tech", {"Industrials", "Manufacturing and Robotics", "Aviation and Space", "Climate", "Energy", "Agriculture", "Drones", "Automotive", "Industrial Bio", "Defense"}),
    ("Real Estate / Construction", {"Real Estate and Construction", "Housing and Real Estate", "Construction"}),
    ("Legal / Gov", {"Legal", "Government"}),
]


def load_data() -> tuple[list[dict], dict]:
    companies = json.loads(RAW_COMPANIES.read_text())
    meta = json.loads(RAW_META.read_text())
    return [row for row in companies if row["batch"] not in EXCLUDED_BATCHES], meta


def batch_parts(batch: str) -> tuple[int, int, str, str]:
    season, year_s = batch.split()
    year = int(year_s)
    order = SEASON_ORDER[season]
    code_prefix = {"Winter": "W", "Spring": "Sp", "Summer": "S", "Fall": "F"}[season]
    return year, order, season, f"{code_prefix}{str(year)[-2:]}"


def norm_values(row: dict) -> set[str]:
    return set(row.get("tags", [])) | set(row.get("industries", [])) | {row.get("industry", ""), row.get("subindustry", "")}


def text_blob(row: dict) -> str:
    return " ".join(
        str(row.get(k, ""))
        for k in ("name", "one_liner", "long_description")
    ).lower()


def has_keyword(wave: str, row: dict) -> bool:
    blob = text_blob(row)
    return any(re.search(pattern, blob, flags=re.I) for pattern in BROAD_KEYWORDS[wave])


def classify(row: dict, mode: str) -> str:
    values = norm_values(row)
    for wave in PRECEDENCE:
        rules = STRICT_RULES[wave]
        strict_hit = bool(values & rules["tags"]) or bool(values & rules["industries"])
        if strict_hit:
            return wave
        if mode == "broad" and has_keyword(wave, row):
            return wave
    return "Other"


def background_sector(row: dict) -> str:
    values = norm_values(row)
    for sector, terms in BACKGROUND_SECTOR_RULES:
        if values & terms:
            return sector
    return "Other"


def aggregate(companies: list[dict], classifications: dict[int, str]) -> list[dict]:
    totals = Counter(row["batch"] for row in companies)
    counts = Counter((row["batch"], classifications[row["id"]]) for row in companies)
    rows = []
    for batch in sorted(totals.keys(), key=batch_parts):
        year, season_order, season, code = batch_parts(batch)
        for wave in WAVES:
            count = counts[(batch, wave)]
            rows.append(
                {
                    "batch": batch,
                    "batch_code": code,
                    "year": year,
                    "season": season,
                    "season_order": season_order,
                    "total_companies": totals[batch],
                    "wave": wave,
                    "count": count,
                    "pct": count / totals[batch] if totals[batch] else 0,
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_stacked(rows: list[dict], mode: str) -> None:
    batches = sorted({r["batch"] for r in rows}, key=batch_parts)
    x = np.arange(len(batches))
    pct_by_wave = {
        wave: [next(r["pct"] for r in rows if r["batch"] == b and r["wave"] == wave) for b in batches]
        for wave in WAVES
    }
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.stackplot(
        x,
        [pct_by_wave[w] for w in WAVES],
        labels=WAVES,
        colors=[COLORS[w] for w in WAVES],
        alpha=0.9,
    )
    ax.set_title(f"YC Company Waves by Batch ({mode})")
    ax.set_ylabel("Share of launched companies")
    ax.set_ylim(0, 1)
    ax.set_yticks(np.linspace(0, 1, 6), [f"{int(v * 100)}%" for v in np.linspace(0, 1, 6)])
    ax.set_xticks(x[::3], [batch_parts(b)[3] for b in batches[::3]], rotation=45, ha="right")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(loc="upper left", ncols=2, fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / f"stacked_area_{mode}.png", dpi=180)
    plt.close(fig)


def plot_indexed(rows: list[dict], mode: str) -> None:
    batches = sorted({r["batch"] for r in rows}, key=batch_parts)
    x = np.arange(len(batches))
    fig, ax = plt.subplots(figsize=(14, 7))
    for wave in WAVES[:-1]:
        series = np.array([next(r["pct"] for r in rows if r["batch"] == b and r["wave"] == wave) for b in batches])
        first_idx = next((i for i, v in enumerate(series) if v >= 0.02), None)
        if first_idx is None:
            continue
        base = series[first_idx] or 1
        indexed = np.full_like(series, np.nan, dtype=float)
        indexed[first_idx:] = series[first_idx:] / base
        ax.plot(x, indexed, label=wave, color=COLORS[wave], linewidth=2.4)
        ax.scatter([first_idx], [1], color=COLORS[wave], s=25)
    ax.axhline(1, color="#666666", linewidth=1, alpha=0.4)
    ax.set_title(f"Indexed Growth Curves from First >=2% Batch ({mode})")
    ax.set_ylabel("Multiple of first >=2% batch share")
    ax.set_xticks(x[::3], [batch_parts(b)[3] for b in batches[::3]], rotation=45, ha="right")
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / f"indexed_growth_{mode}.png", dpi=180)
    plt.close(fig)


def plot_small_multiples(rows: list[dict], mode: str) -> None:
    batches = sorted({r["batch"] for r in rows}, key=batch_parts)
    x = np.arange(len(batches))
    fig, axes = plt.subplots(3, 2, figsize=(14, 10), sharex=True, sharey=True)
    axes = axes.flatten()
    for ax, wave in zip(axes, WAVES):
        series = [next(r["pct"] for r in rows if r["batch"] == b and r["wave"] == wave) for b in batches]
        ax.fill_between(x, series, color=COLORS[wave], alpha=0.25)
        ax.plot(x, series, color=COLORS[wave], linewidth=2)
        ax.set_title(wave, fontsize=10)
        ax.grid(axis="y", alpha=0.2)
        ax.set_ylim(0, max(0.72, max(series) * 1.15))
    for ax in axes[-2:]:
        ax.set_xticks(x[::4], [batch_parts(b)[3] for b in batches[::4]], rotation=45, ha="right")
    fig.suptitle(f"Small Multiples by Wave ({mode})", y=0.995)
    fig.tight_layout()
    fig.savefig(OUT / f"small_multiples_{mode}.png", dpi=180)
    plt.close(fig)


def plot_genai_sectors(sector_rows: list[dict]) -> None:
    rows = list(reversed(sector_rows))
    fig, ax = plt.subplots(figsize=(11, 6.5))
    labels = [r["sector"] for r in rows]
    values = [r["pct_of_genai_broad"] for r in rows]
    ax.barh(labels, values, color=COLORS["Generative AI / Agents"], alpha=0.85)
    ax.set_title("Broad GenAI / Agent Companies by Background Sector")
    ax.set_xlabel("Share of broad GenAI / Agent-classified companies")
    ax.set_xlim(0, max(values) * 1.18 if values else 1)
    ax.set_xticks(np.linspace(0, 0.5, 6), [f"{int(v * 100)}%" for v in np.linspace(0, 0.5, 6)])
    ax.grid(axis="x", alpha=0.25)
    for i, v in enumerate(values):
        ax.text(v + 0.006, i, f"{v:.1%}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "genai_broad_background_sectors.png", dpi=180)
    plt.close(fig)


def outcome_rows(companies: list[dict], classifications: dict[int, str], mode: str, max_year: int | None = None) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in companies:
        year, _, _, _ = batch_parts(row["batch"])
        if max_year is not None and year > max_year:
            continue
        grouped[classifications[row["id"]]].append(row)

    rows = []
    for wave in WAVES:
        group = grouped.get(wave, [])
        total = len(group)
        status_counts = Counter(row.get("status") for row in group)
        top_count = sum(1 for row in group if row.get("top_company"))
        public_count = status_counts.get("Public", 0)
        acquired_count = status_counts.get("Acquired", 0)
        inactive_count = status_counts.get("Inactive", 0)
        rows.append(
            {
                "mode": mode,
                "cohort_filter": f"through_{max_year}" if max_year is not None else "all_included_batches",
                "wave": wave,
                "company_count": total,
                "top_company_count": top_count,
                "top_company_rate": top_count / total if total else 0,
                "public_count": public_count,
                "public_rate": public_count / total if total else 0,
                "acquired_count": acquired_count,
                "acquired_rate": acquired_count / total if total else 0,
                "public_or_acquired_count": public_count + acquired_count,
                "public_or_acquired_rate": (public_count + acquired_count) / total if total else 0,
                "inactive_count": inactive_count,
                "inactive_rate": inactive_count / total if total else 0,
            }
        )
    return rows


def plot_outcome_proxy(rows: list[dict], mode: str, cohort_filter: str) -> None:
    waves = WAVES[:-1]
    selected = {r["wave"]: r for r in rows if r["wave"] in waves}
    x = np.arange(len(waves))
    top_rates = [selected[w]["top_company_rate"] for w in waves]
    exit_rates = [selected[w]["public_or_acquired_rate"] for w in waves]
    inactive_rates = [selected[w]["inactive_rate"] for w in waves]

    fig, ax = plt.subplots(figsize=(12, 6.5))
    width = 0.25
    ax.bar(x - width, top_rates, width, label="Top company", color="#4E79A7")
    ax.bar(x, exit_rates, width, label="Public or acquired", color="#59A14F")
    ax.bar(x + width, inactive_rates, width, label="Inactive", color="#E15759")
    ax.set_title(f"Outcome Proxies by Wave ({mode}, {cohort_filter})")
    ax.set_ylabel("Share of classified companies")
    ax.set_xticks(x, [w.replace(" / ", " /\n").replace("Mobile-Enabled ", "Mobile-\nEnabled ") for w in waves])
    ax.set_yticks(np.linspace(0, 0.5, 6), [f"{int(v * 100)}%" for v in np.linspace(0, 0.5, 6)])
    ax.set_ylim(0, max(0.5, max(top_rates + exit_rates + inactive_rates) * 1.2))
    ax.grid(axis="y", alpha=0.25)
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(OUT / f"outcome_proxy_{mode}_{cohort_filter}.png", dpi=180)
    plt.close(fig)


def pct_at(rows: list[dict], wave: str, batch: str) -> float:
    matches = [r for r in rows if r["batch"] == batch and r["wave"] == wave]
    return matches[0]["pct"] if matches else math.nan


def summary_for_mode(rows: list[dict], mode: str) -> dict:
    summary = {"mode": mode, "waves": {}}
    for wave in WAVES[:-1]:
        wave_rows = [r for r in rows if r["wave"] == wave]
        peak = max(wave_rows, key=lambda r: (r["pct"], r["count"]))
        first_2 = next((r for r in wave_rows if r["pct"] >= 0.02), None)
        first_10 = next((r for r in wave_rows if r["pct"] >= 0.10), None)
        first_20 = next((r for r in wave_rows if r["pct"] >= 0.20), None)
        summary["waves"][wave] = {
            "peak_batch": peak["batch"],
            "peak_pct": round(peak["pct"], 4),
            "peak_count": peak["count"],
            "first_batch_at_or_above_2pct": first_2["batch"] if first_2 else None,
            "first_batch_at_or_above_10pct": first_10["batch"] if first_10 else None,
            "first_batch_at_or_above_20pct": first_20["batch"] if first_20 else None,
            "spring_2026_pct": round(pct_at(wave_rows, wave, "Spring 2026"), 4),
        }
    return summary


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (SPIKE_DIR / ".mplconfig").mkdir(exist_ok=True)
    companies, meta = load_data()

    strict = {row["id"]: classify(row, "strict") for row in companies}
    broad = {row["id"]: classify(row, "broad") for row in companies}

    strict_rows = aggregate(companies, strict)
    broad_rows = aggregate(companies, broad)

    write_csv(OUT / "wave_by_batch_strict.csv", strict_rows)
    write_csv(OUT / "wave_by_batch_broad.csv", broad_rows)

    classified_rows = []
    for row in sorted(companies, key=lambda r: (*batch_parts(r["batch"])[:2], r["name"])):
        classified_rows.append(
            {
                "id": row["id"],
                "name": row["name"],
                "batch": row["batch"],
                "wave_strict": strict[row["id"]],
                "wave_broad": broad[row["id"]],
                "background_sector": background_sector(row),
                "industry": row.get("industry", ""),
                "industries": " | ".join(row.get("industries", [])),
                "tags": " | ".join(row.get("tags", [])),
                "one_liner": row.get("one_liner", ""),
                "status": row.get("status", ""),
                "top_company": row.get("top_company", False),
                "url": row.get("url", ""),
            }
        )
    write_csv(OUT / "classified_companies.csv", classified_rows)

    for mode, rows in (("strict", strict_rows), ("broad", broad_rows)):
        plot_stacked(rows, mode)
        plot_indexed(rows, mode)
        plot_small_multiples(rows, mode)

    strict_outcomes_all = outcome_rows(companies, strict, "strict")
    broad_outcomes_all = outcome_rows(companies, broad, "broad")
    strict_outcomes_mature = outcome_rows(companies, strict, "strict", max_year=2020)
    broad_outcomes_mature = outcome_rows(companies, broad, "broad", max_year=2020)
    write_csv(OUT / "outcome_proxy_by_wave_strict_all.csv", strict_outcomes_all)
    write_csv(OUT / "outcome_proxy_by_wave_broad_all.csv", broad_outcomes_all)
    write_csv(OUT / "outcome_proxy_by_wave_strict_through_2020.csv", strict_outcomes_mature)
    write_csv(OUT / "outcome_proxy_by_wave_broad_through_2020.csv", broad_outcomes_mature)
    plot_outcome_proxy(broad_outcomes_all, "broad", "all_included_batches")
    plot_outcome_proxy(broad_outcomes_mature, "broad", "through_2020")

    genai_broad = [row for row in companies if broad[row["id"]] == "Generative AI / Agents"]
    sector_counts = Counter(background_sector(row) for row in genai_broad)
    sector_rows = [
        {
            "sector": sector,
            "count": count,
            "pct_of_genai_broad": count / len(genai_broad) if genai_broad else 0,
        }
        for sector, count in sector_counts.most_common()
    ]
    write_csv(OUT / "genai_broad_background_sectors.csv", sector_rows)
    plot_genai_sectors(sector_rows)

    batch_totals = Counter(row["batch"] for row in companies)
    summary = {
        "source": {
            "yc_oss_api": "https://yc-oss.github.io/api/companies/all.json",
            "yc_oss_readme": meta.get("readme"),
            "last_updated": meta.get("last_updated"),
            "downloaded_companies": meta.get("companies", {}).get("all", {}).get("count"),
            "included_companies": len(companies),
            "included_batches": len(batch_totals),
            "excluded_batches": sorted(EXCLUDED_BATCHES),
        },
        "status_counts": dict(Counter(row.get("status") for row in companies)),
        "top_company_count": sum(1 for row in companies if row.get("top_company")),
        "mode_summaries": [
            summary_for_mode(strict_rows, "strict"),
            summary_for_mode(broad_rows, "broad"),
        ],
        "latest_batch": {
            "batch": "Spring 2026",
            "total_companies": batch_totals["Spring 2026"],
            "strict_wave_counts": dict(Counter(strict[row["id"]] for row in companies if row["batch"] == "Spring 2026")),
            "broad_wave_counts": dict(Counter(broad[row["id"]] for row in companies if row["batch"] == "Spring 2026")),
        },
        "genai_broad_background_sectors": sector_rows,
        "outcome_proxies": {
            "strict_all": strict_outcomes_all,
            "broad_all": broad_outcomes_all,
            "strict_through_2020": strict_outcomes_mature,
            "broad_through_2020": broad_outcomes_mature,
        },
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
