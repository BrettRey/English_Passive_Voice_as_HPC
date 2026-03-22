#!/usr/bin/env python3
"""Build a deterministic Study 1 fit-gate supplement when usable core/foil counts fall short."""

from __future__ import annotations

import argparse
import csv
import random
from collections import Counter
from pathlib import Path


SEED = 20260320
CORPORA = ("ewt", "gum")
CLASSES = ("core", "foil")

ANNOTATION_COLUMNS = (
    "participial_form",
    "licensing_marker",
    "constructional_environment",
    "local_subject_present",
    "by_pp_present",
    "stranded_preposition",
    "event_implied",
    "agent_implied",
    "predicand_as_undergoer",
    "peripheral_subtype",
    "family_status",
    "notes",
)

BLIND_FIELDS = [
    "pilot_item_id",
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
    out = list(rows)
    random.Random(f"{seed}:{salt}").shuffle(out)
    return out


def build_blind_rows(rows: list[dict[str, str]], seed: int, salt: str) -> list[dict[str, str]]:
    blinded = []
    for order, row in enumerate(shuffled(rows, seed, salt), start=1):
        new = {field: row.get(field, "") for field in BLIND_FIELDS}
        for field in ANNOTATION_COLUMNS:
            new[field] = ""
        new["pilot_order"] = str(order)
        blinded.append(new)
    return blinded


def attach_orders(rows: list[dict[str, str]], seed: int, prefix: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    blind = build_blind_rows(rows, seed, f"{prefix}:blind")
    order_lookup = {row["pilot_item_id"]: row["pilot_order"] for row in blind}
    keyed = []
    for row in rows:
        new = dict(row)
        new["pilot_order"] = order_lookup[row["pilot_item_id"]]
        keyed.append(new)
    return keyed, blind


def used_candidate_ids(pilot_key_rows: list[dict[str, str]]) -> set[str]:
    return {row["candidate_id"] for row in pilot_key_rows}


def usable_counts(pilot_key_rows: list[dict[str, str]], annotated_rows: list[dict[str, str]]) -> Counter[tuple[str, str]]:
    ann_by_id = {row["pilot_item_id"]: row for row in annotated_rows}
    counts: Counter[tuple[str, str]] = Counter()
    for row in pilot_key_rows:
        pilot_id = row["pilot_item_id"]
        if pilot_id not in ann_by_id:
            continue
        family = ann_by_id[pilot_id].get("family_status", "")
        if family in CLASSES:
            counts[(row["pilot_corpus"], family)] += 1
    return counts


def deficit_table(counts: Counter[tuple[str, str]], target: int) -> dict[tuple[str, str], int]:
    deficits: dict[tuple[str, str], int] = {}
    for corpus in CORPORA:
        for label in CLASSES:
            deficits[(corpus, label)] = max(0, target - counts.get((corpus, label), 0))
    return deficits


def candidate_sort_key(row: dict[str, str]) -> tuple[int, int, int]:
    # Prefer overtly prototypical passives first so the supplement restores usable binary counts efficiently.
    return (
        -int(row.get("has_obl_agent", "0") or 0),
        -int(row.get("has_nsubj_pass", "0") or 0),
        int(row.get("sample_rank", "0") or 0),
    )


def sample_set_for(label: str) -> str:
    return "analytic_core_candidate" if label == "core" else "analytic_foil_candidate"


def select_supplement_rows(
    primary_rows: list[dict[str, str]],
    used_ids: set[str],
    deficits: dict[tuple[str, str], int],
) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    selected_ids = set()
    for corpus in CORPORA:
        for label in CLASSES:
            need = deficits[(corpus, label)]
            if need <= 0:
                continue
            eligible = [
                row for row in primary_rows
                if row.get("corpus") == corpus
                and row.get("sample_set") == sample_set_for(label)
                and row.get("candidate_id") not in used_ids
                and row.get("candidate_id") not in selected_ids
            ]
            eligible = sorted(eligible, key=candidate_sort_key)
            if len(eligible) < need:
                raise SystemExit(
                    f"Supplement build failed for {corpus} {label}: need {need}, found {len(eligible)}"
                )
            for row in eligible[:need]:
                new = dict(row)
                new["pilot_pack"] = "fit_gate_supplement"
                new["pilot_corpus"] = corpus
                new["pilot_class"] = label
                new["pilot_stream"] = row.get("sampling_stream", "")
                new["supplement_reason"] = f"restore_{label}_usable_count"
                selected.append(new)
                selected_ids.add(row["candidate_id"])
    return selected


def assign_item_ids(rows: list[dict[str, str]], prefix: str) -> list[dict[str, str]]:
    out = []
    for idx, row in enumerate(rows, start=1):
        new = dict(row)
        new["pilot_item_id"] = f"{prefix}{idx:03d}"
        out.append(new)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--pilot-key", required=True, type=Path)
    parser.add_argument("--annotated-pilot", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--target-per-corpus", default=25, type=int)
    parser.add_argument("--seed", default=SEED, type=int)
    args = parser.parse_args()

    primary_rows = read_rows(args.input)
    pilot_key_rows = read_rows(args.pilot_key)
    annotated_rows = read_rows(args.annotated_pilot)

    counts = usable_counts(pilot_key_rows, annotated_rows)
    deficits = deficit_table(counts, args.target_per_corpus)
    selected = select_supplement_rows(
        primary_rows=primary_rows,
        used_ids=used_candidate_ids(pilot_key_rows),
        deficits=deficits,
    )
    selected = assign_item_ids(selected, "FS")
    keyed, blind = attach_orders(selected, args.seed, "study1_pilot_supplement")

    output_dir = args.output_dir
    if keyed:
        write_rows(output_dir / "study1_pilot_supplement_key.csv", keyed, list(keyed[0].keys()))
        write_rows(output_dir / "study1_pilot_supplement_blind.csv", blind, BLIND_FIELDS + ["pilot_order"])

    manifest = [
        "Study 1 fit-gate supplement",
        f"seed={args.seed}",
        f"target_per_corpus={args.target_per_corpus}",
    ]
    for corpus in CORPORA:
        for label in CLASSES:
            manifest.append(
                f"{corpus} {label}: usable={counts.get((corpus, label), 0)} deficit={deficits[(corpus, label)]}"
            )
    manifest.append(f"supplement_total={len(selected)}")
    (output_dir / "study1_pilot_supplement_manifest.txt").write_text(
        "\n".join(manifest) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
