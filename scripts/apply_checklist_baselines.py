#!/usr/bin/env python3
"""Apply deterministic passive checklist baselines to an annotated CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def norm(value: str) -> str:
    return value.strip().lower().replace("_", "-")


STRICT_AUX = {"be", "get"}
PROMOTED = {"direct-object-promotion", "oblique-stranding-promotion"}


def promoted_subject_signal(row: dict[str, str]) -> bool:
    nsubj_pass = row.get("has_nsubj_pass", "").strip()
    if nsubj_pass in {"0", "1"}:
        return nsubj_pass == "1"
    promotion = norm(row.get("promotion_type", ""))
    return promotion in PROMOTED


def strict_checklist(row: dict[str, str]) -> int:
    aux = norm(row.get("auxiliary_type", ""))
    participial = norm(row.get("participial_predicate", ""))
    return int(aux in STRICT_AUX and participial == "yes" and promoted_subject_signal(row))


def stronger_rule(row: dict[str, str]) -> int:
    if not strict_checklist(row):
        return 0
    eventive = norm(row.get("eventive_stative", ""))
    return int(eventive != "stative")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    with args.input.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        for col in ["strict_checklist", "stronger_rule"]:
            if col not in fieldnames:
                fieldnames.append(col)

        rows = []
        for row in reader:
            row["strict_checklist"] = str(strict_checklist(row))
            row["stronger_rule"] = str(stronger_rule(row))
            rows.append(row)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
