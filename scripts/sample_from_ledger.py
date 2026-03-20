#!/usr/bin/env python3
"""Create deterministic primary and replacement annotation packs from a ledger."""

from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path


SEED = 20260319
CORPORA = ("ewt", "gum")

HELDOUT_PER_CORPUS = 40
CORE_PRIMARY_PER_CORPUS = 60
PERIPHERAL_PRIMARY_PER_CORPUS = 40
FOIL_PRIMARY_PER_CORPUS = 60

STREAM_PRIORITY = (
    "core_be",
    "peripheral_get",
    "peripheral_reduced_embedded",
    "peripheral_manual_probe",
    "foil_copular_participle",
    "foil_participial_modifier",
    "foil_perfect",
)

PERIPHERAL_PRIMARY_CYCLE = (
    "peripheral_manual_probe",
    "peripheral_get",
    "peripheral_manual_probe",
    "peripheral_reduced_embedded",
    "peripheral_manual_probe",
)
PERIPHERAL_REPLACEMENT_CYCLE = (
    "peripheral_get",
    "peripheral_manual_probe",
    "peripheral_reduced_embedded",
    "peripheral_manual_probe",
)

FOIL_PRIMARY_CYCLE = (
    "foil_perfect",
    "foil_participial_modifier",
    "foil_perfect",
    "foil_participial_modifier",
    "foil_copular_participle",
    "foil_perfect",
)
FOIL_REPLACEMENT_CYCLE = (
    "foil_copular_participle",
    "foil_participial_modifier",
    "foil_perfect",
    "foil_participial_modifier",
    "foil_perfect",
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def stream_set(row: dict[str, str]) -> set[str]:
    return {part for part in row.get("provisional_streams", "").split(";") if part}


def clean_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen = set()
    cleaned = []
    for row in rows:
        key = row["candidate_id"]
        if key in seen:
            continue
        seen.add(key)
        if not row.get("provisional_streams", "").strip():
            continue
        if not row.get("sent_id", "").strip():
            continue
        if not row.get("sentence", "").strip():
            continue
        if not row.get("sentence_marked", "").strip():
            continue
        cleaned.append(row)
    return cleaned


def shuffled(rows: list[dict[str, str]], seed: int, salt: str) -> list[dict[str, str]]:
    keyed = list(rows)
    rng = random.Random(f"{seed}:{salt}")
    rng.shuffle(keyed)
    return keyed


def unique_concat(*groups: list[dict[str, str]]) -> list[dict[str, str]]:
    out = []
    seen = set()
    for group in groups:
        for row in group:
            key = row["candidate_id"]
            if key in seen:
                continue
            seen.add(key)
            out.append(row)
    return out


def select_prefix(rows: list[dict[str, str]], n: int) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    return rows[:n], rows[n:]


def annotate_pack(rows: list[dict[str, str]], sample_set: str) -> list[dict[str, str]]:
    packed = []
    for rank, row in enumerate(rows, start=1):
        new_row = dict(row)
        new_row["sample_set"] = sample_set
        new_row["sample_rank"] = str(rank)
        packed.append(new_row)
    return packed


def corpus_rows(rows: list[dict[str, str]], corpus: str) -> list[dict[str, str]]:
    return [row for row in rows if row["corpus"] == corpus]


def require_count(rows: list[dict[str, str]], n: int, label: str, corpus: str) -> None:
    if len(rows) < n:
        raise SystemExit(
            f"Sampling failed for {corpus} {label}: need {n}, found {len(rows)} eligible rows"
        )


def require_unique_ids(rows: list[dict[str, str]], label: str) -> None:
    ids = [row["candidate_id"] for row in rows]
    duplicates = len(ids) - len(set(ids))
    if duplicates:
        raise SystemExit(f"Sampling failed for {label}: found {duplicates} duplicate candidate_ids")


def analytic_stream(row: dict[str, str]) -> str:
    streams = stream_set(row)
    for stream in STREAM_PRIORITY:
        if stream in streams:
            return stream
    return ""


def with_sampling_stream(row: dict[str, str], stream: str) -> dict[str, str]:
    new_row = dict(row)
    new_row["sampling_stream"] = stream
    return new_row


def stream_queues(rows: list[dict[str, str]], corpus: str, seed: int) -> dict[str, list[dict[str, str]]]:
    queues = {stream: [] for stream in STREAM_PRIORITY}
    for row in corpus_rows(rows, corpus):
        stream = analytic_stream(row)
        if not stream:
            continue
        queues[stream].append(with_sampling_stream(row, stream))
    for stream, group in list(queues.items()):
        queues[stream] = shuffled(group, seed, f"{corpus}:{stream}")
    return queues


def take_from_cycle(
    queues: dict[str, list[dict[str, str]]],
    cycle: tuple[str, ...],
    target: int,
    corpus: str,
    label: str,
) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    if target <= 0:
        return selected

    while len(selected) < target:
        progressed = False
        for stream in cycle:
            queue = queues.get(stream, [])
            if not queue:
                continue
            selected.append(queue.pop(0))
            progressed = True
            if len(selected) >= target:
                break
        if not progressed:
            raise SystemExit(
                f"Sampling failed for {corpus} {label}: cycle exhausted before target {target}"
            )
    return selected


def drain_cycle(
    queues: dict[str, list[dict[str, str]]],
    cycle: tuple[str, ...],
) -> list[dict[str, str]]:
    total = sum(len(queue) for queue in queues.values())
    return take_from_cycle(queues, cycle, total, "global", "replacement queue")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--seed", default=SEED, type=int)
    args = parser.parse_args()

    rows = clean_rows(read_rows(args.input))
    if not rows:
        raise SystemExit("No ledger rows found after cleaning")
    all_fieldnames = list(rows[0].keys())
    for extra in ["sampling_stream", "sample_set", "sample_rank"]:
        if extra not in all_fieldnames:
            all_fieldnames.append(extra)

    primary_rows: list[dict[str, str]] = []
    replacement_rows: list[dict[str, str]] = []
    heldout_ids = set()

    for corpus in CORPORA:
        crows = corpus_rows(rows, corpus)
        require_count(crows, HELDOUT_PER_CORPUS, "heldout", corpus)
        heldout = shuffled(crows, args.seed, f"{corpus}:heldout")[:HELDOUT_PER_CORPUS]
        heldout = [with_sampling_stream(row, analytic_stream(row)) for row in heldout]
        primary_rows.extend(annotate_pack(heldout, "heldout"))
        heldout_ids.update(row["candidate_id"] for row in heldout)

    remaining = [row for row in rows if row["candidate_id"] not in heldout_ids]

    for corpus in CORPORA:
        queues = stream_queues(remaining, corpus, args.seed)

        require_count(queues["core_be"], CORE_PRIMARY_PER_CORPUS, "core queue", corpus)
        require_count(queues["peripheral_get"], 8, "peripheral get queue", corpus)
        require_count(queues["peripheral_reduced_embedded"], 8, "peripheral reduced queue", corpus)
        require_count(queues["peripheral_manual_probe"], 24, "peripheral manual queue", corpus)
        require_count(queues["foil_perfect"], 30, "foil perfect queue", corpus)
        require_count(queues["foil_participial_modifier"], 15, "foil modifier queue", corpus)
        require_count(queues["foil_copular_participle"], 1, "foil copular queue", corpus)

        core_primary, core_rest = select_prefix(queues["core_be"], CORE_PRIMARY_PER_CORPUS)

        peripheral_queues = {
            "peripheral_get": list(queues["peripheral_get"]),
            "peripheral_reduced_embedded": list(queues["peripheral_reduced_embedded"]),
            "peripheral_manual_probe": list(queues["peripheral_manual_probe"]),
        }
        per_primary = take_from_cycle(
            peripheral_queues,
            PERIPHERAL_PRIMARY_CYCLE,
            PERIPHERAL_PRIMARY_PER_CORPUS,
            corpus,
            "peripheral primary queue",
        )
        per_rest = drain_cycle(peripheral_queues, PERIPHERAL_REPLACEMENT_CYCLE)

        foil_queues = {
            "foil_perfect": list(queues["foil_perfect"]),
            "foil_participial_modifier": list(queues["foil_participial_modifier"]),
            "foil_copular_participle": list(queues["foil_copular_participle"]),
        }
        foil_primary = take_from_cycle(
            foil_queues,
            FOIL_PRIMARY_CYCLE,
            FOIL_PRIMARY_PER_CORPUS,
            corpus,
            "foil primary queue",
        )
        foil_rest = drain_cycle(foil_queues, FOIL_REPLACEMENT_CYCLE)

        primary_rows.extend(annotate_pack(core_primary, "analytic_core_candidate"))
        primary_rows.extend(annotate_pack(per_primary, "analytic_peripheral_candidate"))
        primary_rows.extend(annotate_pack(foil_primary, "analytic_foil_candidate"))

        replacement_rows.extend(annotate_pack(core_rest, "analytic_core_replacement"))
        replacement_rows.extend(annotate_pack(per_rest, "analytic_peripheral_replacement"))
        replacement_rows.extend(annotate_pack(foil_rest, "analytic_foil_replacement"))

    require_unique_ids(primary_rows, "primary pack")
    require_unique_ids(replacement_rows, "replacement queue")
    require_unique_ids(primary_rows + replacement_rows, "combined packs")

    primary_rows = shuffled(primary_rows, args.seed, "primary_blind_order")
    replacement_rows = shuffled(replacement_rows, args.seed, "replacement_blind_order")

    write_rows(args.output_dir / "primary_annotation_pack.csv", primary_rows, all_fieldnames)
    write_rows(args.output_dir / "replacement_queue.csv", replacement_rows, all_fieldnames)


if __name__ == "__main__":
    main()
