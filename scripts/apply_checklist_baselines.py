#!/usr/bin/env python3
"""Apply deterministic passive checklist baselines to an annotated CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def norm(value: str) -> str:
    return value.strip().lower().replace("_", "-")


REQUIRED_COLUMNS = (
    "participial_form",
    "local_subject_present",
    "event_implied",
    "aux_pass_lemmas",
    "aux_lemmas",
    "cop_lemmas",
)


def has_surface_be_or_get(row: dict[str, str]) -> bool:
    for field in ("aux_pass_lemmas", "aux_lemmas", "cop_lemmas"):
        values = {
            part.strip()
            for part in norm(row.get(field, "")).split(";")
            if part.strip() and part.strip() != "-"
        }
        if {"be", "get"} & values:
            return True
    return False


def strict_checklist(row: dict[str, str]) -> int:
    participial = norm(row.get("participial_form", ""))
    local_subject = norm(row.get("local_subject_present", ""))
    return int(
        participial == "past-participle"
        and has_surface_be_or_get(row)
        and local_subject == "yes"
    )


def stronger_rule(row: dict[str, str]) -> int:
    if not strict_checklist(row):
        return 0
    eventive = norm(row.get("event_implied", ""))
    return int(eventive != "no")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    with args.input.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        missing = [col for col in REQUIRED_COLUMNS if col not in fieldnames]
        if missing:
            raise SystemExit(
                "Baseline application failed: input is missing required v2 columns: "
                + ", ".join(missing)
            )
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
