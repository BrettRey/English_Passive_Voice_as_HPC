#!/usr/bin/env python3
"""Build deterministic participant lists for the Study 2 external-validation tasks."""

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
STRUCTURAL_PER_GROUP = 18
DISCOURSE_PER_GROUP = 18


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


def require_group_balance(rows: list[dict[str, str]], per_group: int, label: str) -> None:
    counts = Counter(row["group_label"] for row in rows)
    for group in GROUPS:
        if counts.get(group, 0) != per_group:
            raise SystemExit(
                f"{label} bank must contain exactly {per_group} rows for {group}; found {counts.get(group, 0)}"
            )


def split_evenly(rows: list[dict[str, str]], chunk_count: int, salt: str) -> list[list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["group_label"]].append(row)

    chunks = [[] for _ in range(chunk_count)]
    for group in GROUPS:
        gro = shuffled(grouped[group], f"{salt}:{group}")
        if len(gro) % chunk_count != 0:
            raise SystemExit(f"Cannot split {group} evenly into {chunk_count} chunks")
        for idx, row in enumerate(gro):
            chunks[idx % chunk_count].append(row)
    return chunks


def structural_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in rows if row.get("include_structural", "").strip() == "1"]


def discourse_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in rows if row.get("include_discourse", "").strip() == "1"]


def assign_structural_lists(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    require_group_balance(rows, STRUCTURAL_PER_GROUP, "Structural")
    halves = split_evenly(rows, 2, "structural")
    out = []
    for list_idx, half in enumerate(halves, start=1):
        for order, row in enumerate(shuffled(half, f"structural:list{list_idx}"), start=1):
            new = dict(row)
            new["task"] = "structural"
            new["list_id"] = f"structural_{list_idx}"
            new["context_condition"] = ""
            new["presentation_order"] = str(order)
            out.append(new)
    return out


def assign_discourse_lists(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    require_group_balance(rows, DISCOURSE_PER_GROUP, "Discourse")
    halves = split_evenly(rows, 2, "discourse")
    out = []
    for half_idx, half in enumerate(halves, start=1):
        ordered = shuffled(half, f"discourse:half{half_idx}")
        base_assignments = {}
        for group in GROUPS:
            group_rows = [row for row in ordered if row["group_label"] == group]
            for idx, row in enumerate(group_rows):
                base_assignments[row["stimulus_id"]] = "patient_given" if idx % 2 == 0 else "agent_given"

        for flip_idx, flip in enumerate([False, True], start=1):
            list_id = f"discourse_{(half_idx - 1) * 2 + flip_idx}"
            list_rows = []
            for row in ordered:
                base = base_assignments[row["stimulus_id"]]
                context = base if not flip else ("agent_given" if base == "patient_given" else "patient_given")
                new = dict(row)
                new["task"] = "discourse"
                new["list_id"] = list_id
                new["context_condition"] = context
                list_rows.append(new)

            for order, row in enumerate(shuffled(list_rows, f"{list_id}:order"), start=1):
                row["presentation_order"] = str(order)
                out.append(row)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    rows = read_rows(args.input)
    if not rows:
        raise SystemExit("No rows found in item bank")

    ids = [row["stimulus_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("Stimulus IDs must be globally unique")

    fieldnames = list(rows[0].keys())
    for extra in ["task", "list_id", "context_condition", "presentation_order"]:
        if extra not in fieldnames:
            fieldnames.append(extra)

    structural = assign_structural_lists(structural_rows(rows))
    discourse = assign_discourse_lists(discourse_rows(rows))

    combined = structural + discourse
    write_rows(args.output_dir / "all_lists.csv", combined, fieldnames)

    by_list: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in combined:
        by_list[row["list_id"]].append(row)
    for list_id, list_rows in by_list.items():
        write_rows(args.output_dir / f"{list_id}.csv", list_rows, fieldnames)


if __name__ == "__main__":
    main()
