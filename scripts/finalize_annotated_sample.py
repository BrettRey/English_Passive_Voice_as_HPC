#!/usr/bin/env python3
"""Finalize the preregistered sample from annotated primary and replacement rows."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CORE_TARGET = 60
FOIL_TARGET = 60
PERIPHERAL_TARGET = 40
HELDOUT_TARGET = 40
CORPORA = ("ewt", "gum")

SAMPLE_SET_ORDER = {
    "analytic_core_candidate": 0,
    "analytic_core_replacement": 1,
    "analytic_peripheral_candidate": 0,
    "analytic_peripheral_replacement": 1,
    "analytic_foil_candidate": 0,
    "analytic_foil_replacement": 1,
    "heldout": 0,
}

PERIPHERAL_MINIMA = {
    "get": 4,
    "prepositional": 4,
    "reduced_embedded": 4,
    "stative_adjectival": 4,
}


def read_rows(paths: list[Path]) -> list[dict[str, str]]:
    rows = []
    for path in paths:
        with path.open(newline="", encoding="utf-8") as handle:
            rows.extend(csv.DictReader(handle))
    return rows


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def require_unique_ids(rows: list[dict[str, str]], label: str) -> None:
    ids = [row["candidate_id"] for row in rows]
    duplicates = len(ids) - len(set(ids))
    if duplicates:
        raise SystemExit(f"Finalization failed for {label}: found {duplicates} duplicate candidate_ids")


def rank_key(row: dict[str, str]) -> tuple[int, int]:
    return SAMPLE_SET_ORDER.get(row["sample_set"], 99), int(row["sample_rank"])


def corpus_class_rows(rows: list[dict[str, str]], corpus: str, family_status: str, sample_prefix: str) -> list[dict[str, str]]:
    return sorted(
        [
            row for row in rows
            if row.get("corpus") == corpus
            and row.get("family_status") == family_status
            and row.get("sample_set", "").startswith(sample_prefix)
        ],
        key=rank_key,
    )


def first_n(rows: list[dict[str, str]], n: int) -> list[dict[str, str]]:
    return rows[:n]


def select_peripheral(rows: list[dict[str, str]], corpus: str) -> list[dict[str, str]]:
    eligible = corpus_class_rows(rows, corpus, "peripheral", "analytic_peripheral_")
    selected = []
    used = set()

    for subtype, minimum in PERIPHERAL_MINIMA.items():
        subtype_rows = [row for row in eligible if row.get("peripheral_subtype") == subtype and row["candidate_id"] not in used]
        for row in subtype_rows[:minimum]:
            selected.append(row)
            used.add(row["candidate_id"])

    for row in eligible:
        if len(selected) >= PERIPHERAL_TARGET:
            break
        if row["candidate_id"] in used:
            continue
        selected.append(row)
        used.add(row["candidate_id"])

    return selected[:PERIPHERAL_TARGET]


def require_exact(rows: list[dict[str, str]], n: int, label: str, corpus: str) -> None:
    if len(rows) < n:
        raise SystemExit(f"Finalization failed for {corpus} {label}: need {n}, found {len(rows)}")


def require_peripheral_minima(rows: list[dict[str, str]], corpus: str) -> None:
    subtype_counts = {}
    for row in rows:
        subtype = row.get("peripheral_subtype", "")
        subtype_counts[subtype] = subtype_counts.get(subtype, 0) + 1
    for subtype, minimum in PERIPHERAL_MINIMA.items():
        if subtype_counts.get(subtype, 0) < minimum:
            raise SystemExit(
                f"Finalization failed for {corpus} peripheral subtype {subtype}: "
                f"need {minimum}, found {subtype_counts.get(subtype, 0)}"
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary", required=True, type=Path)
    parser.add_argument("--replacement", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    rows = read_rows([args.primary, args.replacement])
    if not rows:
        raise SystemExit("No rows found")
    require_unique_ids(rows, "annotated input")
    fieldnames = list(rows[0].keys())

    final_rows = []

    for corpus in CORPORA:
        heldout_rows = sorted(
            [
                row for row in rows
                if row.get("corpus") == corpus
                and row.get("sample_set") == "heldout"
                and row.get("family_status") != "exclude"
            ],
            key=rank_key,
        )
        require_exact(heldout_rows, HELDOUT_TARGET, "heldout", corpus)
        final_rows.extend(first_n(heldout_rows, HELDOUT_TARGET))

    for corpus in CORPORA:
        core_rows = first_n(corpus_class_rows(rows, corpus, "core", "analytic_core_"), CORE_TARGET)
        require_exact(core_rows, CORE_TARGET, "core", corpus)

        peripheral_rows = select_peripheral(rows, corpus)
        require_exact(peripheral_rows, PERIPHERAL_TARGET, "peripheral", corpus)
        require_peripheral_minima(peripheral_rows, corpus)

        foil_rows = first_n(corpus_class_rows(rows, corpus, "foil", "analytic_foil_"), FOIL_TARGET)
        require_exact(foil_rows, FOIL_TARGET, "foil", corpus)

        final_rows.extend(core_rows)
        final_rows.extend(peripheral_rows)
        final_rows.extend(foil_rows)

    require_unique_ids(final_rows, "final sample")
    write_rows(args.output, final_rows, fieldnames)


if __name__ == "__main__":
    main()
