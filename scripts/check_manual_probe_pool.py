#!/usr/bin/env python3
"""Summarize the manual-probe pool before annotation begins."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


CORPORA = ("ewt", "gum")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def stream_set(row: dict[str, str]) -> set[str]:
    return {part for part in row.get("provisional_streams", "").split(";") if part}


def heuristics(rows: list[dict[str, str]]) -> dict[str, int]:
    return {
        "manual_probe_total": len(rows),
        "with_nsubj_pass": sum(row.get("has_nsubj_pass") == "1" for row in rows),
        "with_be_auxpass": sum("be" in row.get("aux_pass_lemmas", "").split(";") for row in rows),
        "with_get_auxpass": sum("get" in row.get("aux_pass_lemmas", "").split(";") for row in rows),
        "with_case_child": sum(":case:" in row.get("head_children", "") for row in rows),
        "with_obl_child": sum(":obl:" in row.get("head_children", "") for row in rows),
        "bare_participial_no_auxpass": sum(
            row.get("participle_like") == "1"
            and row.get("aux_pass_lemmas") == "_"
            and row.get("cop_lemmas") == "_"
            for row in rows
        ),
        "bare_xcomp_or_root_no_auxpass": sum(
            row.get("participle_like") == "1"
            and row.get("aux_pass_lemmas") == "_"
            and row.get("cop_lemmas") == "_"
            and row.get("head_deprel") in {"xcomp", "root", "conj", "advcl"}
            for row in rows
        ),
    }


def print_counter(label: str, counter: Counter[str], limit: int = 10) -> None:
    print(label)
    for key, value in counter.most_common(limit):
        print(f"  {key}: {value}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()

    rows = read_rows(args.input)
    if not rows:
        raise SystemExit("No ledger rows found")

    for corpus in CORPORA:
        corpus_rows = [row for row in rows if row.get("corpus") == corpus]
        manual_probe = [row for row in corpus_rows if "peripheral_manual_probe" in stream_set(row)]
        print(f"\n[{corpus}]")
        for key, value in heuristics(manual_probe).items():
            print(f"{key}: {value}")
        print_counter("head_deprel", Counter(row.get("head_deprel", "") for row in manual_probe))
        print_counter("aux_pass_lemmas", Counter(row.get("aux_pass_lemmas", "") for row in manual_probe))
        print_counter("parent_deprel", Counter(row.get("parent_deprel", "") for row in manual_probe))


if __name__ == "__main__":
    main()
