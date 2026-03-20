#!/usr/bin/env python3
"""Build deterministic blinded materials for the Study 1 reliability pilot."""

from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path


SEED = 20260319
CORPORA = ("ewt", "gum")
PILOT_TARGETS = {
    ("ewt", "analytic_core_candidate"): 25,
    ("ewt", "analytic_foil_candidate"): 25,
    ("gum", "analytic_core_candidate"): 25,
    ("gum", "analytic_foil_candidate"): 25,
}

ANNOTATION_COLUMNS = (
    "family_status",
    "peripheral_subtype",
    "auxiliary_type",
    "participial_predicate",
    "agent_realization",
    "promotion_type",
    "eventive_stative",
    "syntactic_environment",
    "subject_role_profile",
    "notes",
)

BLIND_FIELDS = [
    "candidate_id",
    "sentence_marked",
    "sentence",
    "head_form",
    "head_children",
    *ANNOTATION_COLUMNS,
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def shuffled(rows: list[dict[str, str]], seed: int, salt: str) -> list[dict[str, str]]:
    keyed = list(rows)
    rng = random.Random(f"{seed}:{salt}")
    rng.shuffle(keyed)
    return keyed


def require_count(rows: list[dict[str, str]], target: int, corpus: str, sample_set: str) -> None:
    if len(rows) < target:
        raise SystemExit(
            f"Pilot build failed for {corpus} {sample_set}: need {target}, found {len(rows)}"
        )


def pilot_class(sample_set: str) -> str:
    return "core" if sample_set == "analytic_core_candidate" else "foil"


def build_blind_rows(rows: list[dict[str, str]], seed: int, salt: str) -> list[dict[str, str]]:
    shuffled_rows = shuffled(rows, seed, salt)
    blind_rows = []
    for order, row in enumerate(shuffled_rows, start=1):
        blind = {field: row.get(field, "") for field in BLIND_FIELDS}
        for field in ANNOTATION_COLUMNS:
            blind[field] = ""
        blind["pilot_order"] = str(order)
        blind_rows.append(blind)
    return blind_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--seed", default=SEED, type=int)
    args = parser.parse_args()

    rows = read_rows(args.input)
    selected: list[dict[str, str]] = []

    for (corpus, sample_set), target in PILOT_TARGETS.items():
        eligible = [
            row
            for row in rows
            if row.get("corpus") == corpus and row.get("sample_set") == sample_set
        ]
        require_count(eligible, target, corpus, sample_set)
        chosen = shuffled(eligible, args.seed, f"pilot:{corpus}:{sample_set}")[:target]
        for row in chosen:
            keyed = dict(row)
            keyed["pilot_corpus"] = corpus
            keyed["pilot_class"] = pilot_class(sample_set)
            selected.append(keyed)

    selected = sorted(selected, key=lambda row: row["candidate_id"])

    keyed_fields = list(selected[0].keys()) + ["pilot_order_first", "pilot_order_second"]
    first_pass_ids = [row["candidate_id"] for row in build_blind_rows(selected, args.seed, "pilot:first")]
    second_pass_ids = [row["candidate_id"] for row in build_blind_rows(selected, args.seed, "pilot:second")]
    first_order = {candidate_id: idx for idx, candidate_id in enumerate(first_pass_ids, start=1)}
    second_order = {candidate_id: idx for idx, candidate_id in enumerate(second_pass_ids, start=1)}
    for row in selected:
        row["pilot_order_first"] = str(first_order[row["candidate_id"]])
        row["pilot_order_second"] = str(second_order[row["candidate_id"]])

    manifest_lines = [
        "Study 1 reliability pilot",
        f"seed={args.seed}",
        "targets: 25 core + 25 foil per corpus",
        f"total_rows={len(selected)}",
    ]
    for corpus in CORPORA:
        corpus_rows = [row for row in selected if row["pilot_corpus"] == corpus]
        core_count = sum(row["pilot_class"] == "core" for row in corpus_rows)
        foil_count = sum(row["pilot_class"] == "foil" for row in corpus_rows)
        manifest_lines.append(f"{corpus}: core={core_count} foil={foil_count}")

    first_blind = build_blind_rows(selected, args.seed, "pilot:first")
    second_blind = build_blind_rows(selected, args.seed, "pilot:second")

    output_dir = args.output_dir
    write_rows(output_dir / "study1_pilot_key.csv", selected, keyed_fields)
    write_rows(
        output_dir / "study1_pilot_first_pass_blind.csv",
        first_blind,
        BLIND_FIELDS + ["pilot_order"],
    )
    write_rows(
        output_dir / "study1_pilot_second_pass_blind.csv",
        second_blind,
        BLIND_FIELDS + ["pilot_order"],
    )
    (output_dir / "study1_pilot_manifest.txt").write_text(
        "\n".join(manifest_lines) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
