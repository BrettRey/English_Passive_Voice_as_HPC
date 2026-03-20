#!/usr/bin/env python3
"""Build the frozen Study 2 item bank from a screened candidate pool."""

from __future__ import annotations

import argparse
import csv
import random
from collections import Counter, defaultdict
from pathlib import Path


SEED = 20260319
GROUPS = [
    "core",
    "foil",
    "get",
    "prepositional",
    "reduced_embedded",
    "stative_adjectival",
]
CORPORA = ["ewt", "gum"]
TARGET_PER_GROUP = 18
TARGET_PER_CORPUS = 9
MAX_FALLBACK_IMBALANCE = 2


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def shuffled(rows: list[dict[str, str]], salt: str) -> list[dict[str, str]]:
    out = list(rows)
    random.Random(f"{SEED}:{salt}").shuffle(out)
    return out


def eligible_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in rows if row.get("screen_status", "").strip() == "eligible"]


def require_unique_source_ids(rows: list[dict[str, str]]) -> None:
    ids = [row["source_candidate_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("Screened Study 2 pool must have unique source_candidate_id values")


def select_group(rows: list[dict[str, str]], group: str) -> list[dict[str, str]]:
    grouped = {corpus: [] for corpus in CORPORA}
    for row in rows:
        if row["group_label"] == group and row["origin_corpus"] in grouped:
            grouped[row["origin_corpus"]].append(row)

    for corpus in CORPORA:
        grouped[corpus] = shuffled(grouped[corpus], f"{group}:{corpus}")

    counts = {corpus: len(grouped[corpus]) for corpus in CORPORA}
    if sum(counts.values()) < TARGET_PER_GROUP:
        raise SystemExit(
            f"Study 2 item-bank build failed for {group}: need {TARGET_PER_GROUP} eligible rows, found {sum(counts.values())}"
        )

    if all(counts[corpus] >= TARGET_PER_CORPUS for corpus in CORPORA):
        target_counts = {corpus: TARGET_PER_CORPUS for corpus in CORPORA}
    else:
        scarce = min(CORPORA, key=lambda corpus: counts[corpus])
        rich = max(CORPORA, key=lambda corpus: counts[corpus])
        scarce_count = counts[scarce]
        if scarce_count < TARGET_PER_CORPUS - 1:
            raise SystemExit(
                f"Study 2 item-bank build failed for {group}: corpus balance would exceed 10/8 fallback"
            )
        target_counts = {
            scarce: scarce_count,
            rich: TARGET_PER_GROUP - scarce_count,
        }
        allowed_pairs = {(9, 9), (10, 8), (8, 10)}
        actual_pair = (target_counts[CORPORA[0]], target_counts[CORPORA[1]])
        if actual_pair not in allowed_pairs:
            raise SystemExit(
                f"Study 2 item-bank build failed for {group}: corpus balance would exceed 10/8 fallback"
            )

    selected = []
    for corpus in CORPORA:
        need = target_counts[corpus]
        available = grouped[corpus]
        if len(available) < need:
            raise SystemExit(
                f"Study 2 item-bank build failed for {group} {corpus}: need {need}, found {len(available)}"
            )
        selected.extend(available[:need])
    return selected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    rows = read_rows(args.input)
    if not rows:
        raise SystemExit("No rows found in Study 2 screening pool")

    require_unique_source_ids(rows)
    screened = eligible_rows(rows)
    if not screened:
        raise SystemExit("No eligible rows found in Study 2 screening pool")

    selected = []
    for group in GROUPS:
        selected.extend(select_group(screened, group))

    selected = sorted(selected, key=lambda row: (row["group_label"], row["origin_corpus"], row["source_candidate_id"]))

    for idx, row in enumerate(selected, start=1):
        row["stimulus_id"] = f"S{idx:03d}"
        row["selection_rank"] = str(idx)
        row["screen_exclusion_reason"] = row.get("screen_exclusion_reason", "")

    counts = Counter((row["group_label"], row["origin_corpus"]) for row in selected)
    for group in GROUPS:
        total = sum(counts[(group, corpus)] for corpus in CORPORA)
        if total != TARGET_PER_GROUP:
            raise SystemExit(
                f"Study 2 item-bank build failed for {group}: selected {total}, expected {TARGET_PER_GROUP}"
            )

    fieldnames = list(selected[0].keys())
    required_front = [
        "stimulus_id",
        "source_candidate_id",
        "origin_corpus",
        "group_label",
        "screen_status",
        "screen_exclusion_reason",
        "selection_rank",
    ]
    ordered = required_front + [field for field in fieldnames if field not in required_front]
    write_rows(args.output, selected, ordered)


if __name__ == "__main__":
    main()
