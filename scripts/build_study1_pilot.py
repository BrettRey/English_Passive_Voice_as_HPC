#!/usr/bin/env python3
"""Build deterministic blinded materials for the Study 1 reliability pilots."""

from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path


SEED = 20260319
CORPORA = ("ewt", "gum")

FIT_TARGETS = {
    ("ewt", "analytic_core_candidate"): 25,
    ("ewt", "analytic_foil_candidate"): 25,
    ("gum", "analytic_core_candidate"): 25,
    ("gum", "analytic_foil_candidate"): 25,
}

BOUNDARY_TARGETS = {
    ("ewt", "peripheral_get"): 2,
    ("ewt", "peripheral_reduced_embedded"): 2,
    ("ewt", "peripheral_manual_probe"): 4,
    ("gum", "peripheral_get"): 2,
    ("gum", "peripheral_reduced_embedded"): 2,
    ("gum", "peripheral_manual_probe"): 4,
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


def require_count(rows: list[dict[str, str]], target: int, label: str) -> None:
    if len(rows) < target:
        raise SystemExit(f"Pilot build failed for {label}: need {target}, found {len(rows)}")


def build_blind_rows(rows: list[dict[str, str]], seed: int, salt: str) -> list[dict[str, str]]:
    blinded = []
    for order, row in enumerate(shuffled(rows, seed, salt), start=1):
        new = {field: row.get(field, "") for field in BLIND_FIELDS}
        for field in ANNOTATION_COLUMNS:
            new[field] = ""
        new["pilot_order"] = str(order)
        blinded.append(new)
    return blinded


def attach_orders(rows: list[dict[str, str]], seed: int, prefix: str) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    first = build_blind_rows(rows, seed, f"{prefix}:first")
    second = build_blind_rows(rows, seed, f"{prefix}:second")
    first_order = {row["pilot_item_id"]: row["pilot_order"] for row in first}
    second_order = {row["pilot_item_id"]: row["pilot_order"] for row in second}
    keyed = []
    for row in rows:
        new = dict(row)
        new["pilot_order_first"] = first_order[row["pilot_item_id"]]
        new["pilot_order_second"] = second_order[row["pilot_item_id"]]
        keyed.append(new)
    return keyed, first, second


def select_fit_rows(rows: list[dict[str, str]], seed: int) -> list[dict[str, str]]:
    selected = []
    for (corpus, sample_set), target in FIT_TARGETS.items():
        eligible = [
            row for row in rows
            if row.get("corpus") == corpus and row.get("sample_set") == sample_set
        ]
        require_count(eligible, target, f"{corpus} {sample_set}")
        chosen = shuffled(eligible, seed, f"fit:{corpus}:{sample_set}")[:target]
        for row in chosen:
            new = dict(row)
            new["pilot_pack"] = "fit_gate"
            new["pilot_corpus"] = corpus
            new["pilot_class"] = "core" if sample_set == "analytic_core_candidate" else "foil"
            new["pilot_stream"] = row.get("sampling_stream", "")
            selected.append(new)
    return sorted(selected, key=lambda row: row["candidate_id"])


def select_boundary_rows(rows: list[dict[str, str]], seed: int) -> list[dict[str, str]]:
    selected = []
    for (corpus, stream), target in BOUNDARY_TARGETS.items():
        eligible = [
            row for row in rows
            if row.get("corpus") == corpus
            and row.get("sample_set") == "analytic_peripheral_candidate"
            and row.get("sampling_stream") == stream
        ]
        require_count(eligible, target, f"{corpus} {stream}")
        chosen = shuffled(eligible, seed, f"boundary:{corpus}:{stream}")[:target]
        for row in chosen:
            new = dict(row)
            new["pilot_pack"] = "boundary_probe"
            new["pilot_corpus"] = corpus
            new["pilot_class"] = "peripheral"
            new["pilot_stream"] = stream
            selected.append(new)
    return sorted(selected, key=lambda row: row["candidate_id"])


def assign_item_ids(rows: list[dict[str, str]], prefix: str) -> list[dict[str, str]]:
    out = []
    for idx, row in enumerate(rows, start=1):
        new = dict(row)
        new["pilot_item_id"] = f"{prefix}{idx:03d}"
        out.append(new)
    return out


def write_pack(output_dir: Path, stem: str, rows: list[dict[str, str]], seed: int) -> None:
    keyed, first, second = attach_orders(rows, seed, stem)
    keyed_fields = list(keyed[0].keys())
    write_rows(output_dir / f"{stem}_key.csv", keyed, keyed_fields)
    write_rows(output_dir / f"{stem}_first_pass_blind.csv", first, BLIND_FIELDS + ["pilot_order"])
    write_rows(output_dir / f"{stem}_second_pass_blind.csv", second, BLIND_FIELDS + ["pilot_order"])


def manifest_lines(fit_rows: list[dict[str, str]], boundary_rows: list[dict[str, str]], seed: int) -> list[str]:
    lines = [
        "Study 1 reliability pilots",
        f"seed={seed}",
        "fit_gate targets: 25 core + 25 foil per corpus",
        "boundary_probe targets: 2 get + 2 reduced_embedded + 4 manual_probe per corpus",
        f"fit_gate_total={len(fit_rows)}",
        f"boundary_probe_total={len(boundary_rows)}",
    ]
    for corpus in CORPORA:
        fit_corpus = [row for row in fit_rows if row["pilot_corpus"] == corpus]
        core_count = sum(row["pilot_class"] == "core" for row in fit_corpus)
        foil_count = sum(row["pilot_class"] == "foil" for row in fit_corpus)
        boundary_corpus = [row for row in boundary_rows if row["pilot_corpus"] == corpus]
        lines.append(f"{corpus} fit_gate: core={core_count} foil={foil_count}")
        stream_counts: dict[str, int] = {}
        for row in boundary_corpus:
            stream = row["pilot_stream"]
            stream_counts[stream] = stream_counts.get(stream, 0) + 1
        lines.append(
            f"{corpus} boundary_probe: "
            f"get={stream_counts.get('peripheral_get', 0)} "
            f"reduced={stream_counts.get('peripheral_reduced_embedded', 0)} "
            f"manual={stream_counts.get('peripheral_manual_probe', 0)}"
        )
    return lines


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--seed", default=SEED, type=int)
    args = parser.parse_args()

    rows = read_rows(args.input)
    fit_rows = assign_item_ids(select_fit_rows(rows, args.seed), "FG")
    boundary_rows = assign_item_ids(select_boundary_rows(rows, args.seed), "BP")

    output_dir = args.output_dir
    write_pack(output_dir, "study1_pilot", fit_rows, args.seed)
    write_pack(output_dir, "study1_boundary_pilot", boundary_rows, args.seed)
    (output_dir / "study1_pilot_manifest.txt").write_text(
        "\n".join(manifest_lines(fit_rows, boundary_rows, args.seed)) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
