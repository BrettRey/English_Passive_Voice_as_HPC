#!/usr/bin/env python3
"""Compare two annotated Study 1 pilot passes and report Cohen's kappa."""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter
from pathlib import Path


FIELDS = (
    "auxiliary_type",
    "participial_predicate",
    "agent_realization",
    "promotion_type",
    "eventive_stative",
    "syntactic_environment",
    "subject_role_profile",
    "family_status",
    "peripheral_subtype",
)

THRESHOLDS = {
    "auxiliary_type": 0.80,
    "participial_predicate": 0.80,
    "agent_realization": 0.80,
    "promotion_type": 0.80,
    "eventive_stative": 0.80,
    "syntactic_environment": 0.80,
    "subject_role_profile": 0.80,
    "family_status": 0.80,
    "peripheral_subtype": 0.70,
}


def join_key(rows: list[dict[str, str]]) -> str:
    if rows and "pilot_item_id" in rows[0]:
        return "pilot_item_id"
    return "candidate_id"


def read_rows(path: Path) -> tuple[str, dict[str, dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    key_field = join_key(rows)
    return key_field, {row[key_field]: row for row in rows}


def cohen_kappa(first: list[str], second: list[str]) -> float:
    if not first or len(first) != len(second):
        return math.nan
    n = len(first)
    observed = sum(a == b for a, b in zip(first, second)) / n
    first_counts = Counter(first)
    second_counts = Counter(second)
    labels = set(first_counts) | set(second_counts)
    expected = sum((first_counts[label] / n) * (second_counts[label] / n) for label in labels)
    if math.isclose(1.0 - expected, 0.0):
        return 1.0 if math.isclose(observed, 1.0) else 0.0
    return (observed - expected) / (1.0 - expected)


def format_float(value: float) -> str:
    if math.isnan(value):
        return "nan"
    return f"{value:.3f}"


def selected_fields(raw: str | None) -> tuple[str, ...]:
    if not raw:
        return FIELDS
    requested = tuple(field.strip() for field in raw.split(",") if field.strip())
    unknown = [field for field in requested if field not in FIELDS]
    if unknown:
        raise SystemExit("Unknown reliability field(s): " + ", ".join(unknown))
    return requested


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", required=True, type=Path)
    parser.add_argument("--second", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fields", help="Comma-separated subset of fields to score")
    parser.add_argument("--require-thresholds", action="store_true")
    args = parser.parse_args()

    first_key, first_rows = read_rows(args.first)
    second_key, second_rows = read_rows(args.second)

    if first_key != second_key:
        raise SystemExit(
            f"Reliability scoring failed: first file uses {first_key}, second file uses {second_key}"
        )

    if set(first_rows) != set(second_rows):
        only_first = sorted(set(first_rows) - set(second_rows))[:5]
        only_second = sorted(set(second_rows) - set(first_rows))[:5]
        raise SystemExit(
            f"Reliability scoring failed: {first_key} sets differ. "
            f"only_first={only_first} only_second={only_second}"
        )

    results = []
    failures = []
    fields = selected_fields(args.fields)

    for field in fields:
        paired = [
            (first_rows[candidate_id].get(field, "").strip(), second_rows[candidate_id].get(field, "").strip())
            for candidate_id in sorted(first_rows)
        ]
        usable = [(a, b) for a, b in paired if a and b]
        missing = len(paired) - len(usable)
        first_values = [a for a, _ in usable]
        second_values = [b for _, b in usable]
        kappa = cohen_kappa(first_values, second_values)
        agreement = (
            sum(a == b for a, b in usable) / len(usable)
            if usable
            else math.nan
        )
        threshold = THRESHOLDS[field]
        passed = (not math.isnan(kappa)) and kappa >= threshold
        if not passed:
            failures.append(field)
        results.append(
            {
                "field": field,
                "n_compared": str(len(usable)),
                "n_missing": str(missing),
                "agreement": format_float(agreement),
                "kappa": format_float(kappa),
                "threshold": f"{threshold:.2f}",
                "pass": "yes" if passed else "no",
            }
        )

    fieldnames = ["field", "n_compared", "n_missing", "agreement", "kappa", "threshold", "pass"]
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    header = "field,n_compared,n_missing,agreement,kappa,threshold,pass"
    print(header)
    for row in results:
        print(",".join(row[field] for field in fieldnames))

    if args.require_thresholds and failures:
        raise SystemExit(
            "Reliability thresholds not met for: " + ", ".join(failures)
        )


if __name__ == "__main__":
    main()
