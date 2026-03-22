#!/usr/bin/env python3
"""Prefill deterministic v2 pilot cues so annotation can focus on judgments."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


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

COMPARISON_PREFILLS = {
    "cmp-middle-001": {
        "participial_form": "none",
        "licensing_marker": "absent_other",
        "constructional_environment": "clausal_predication",
        "local_subject_present": "yes",
        "by_pp_present": "no",
        "stranded_preposition": "no",
        "peripheral_subtype": "comparison_construction",
        "family_status": "foil",
    },
    "cmp-middle-002": {
        "participial_form": "none",
        "licensing_marker": "absent_other",
        "constructional_environment": "clausal_predication",
        "local_subject_present": "yes",
        "by_pp_present": "no",
        "stranded_preposition": "no",
        "peripheral_subtype": "comparison_construction",
        "family_status": "foil",
    },
    "cmp-unacc-001": {
        "participial_form": "none",
        "licensing_marker": "absent_other",
        "constructional_environment": "clausal_predication",
        "local_subject_present": "yes",
        "by_pp_present": "no",
        "stranded_preposition": "no",
        "peripheral_subtype": "comparison_construction",
        "family_status": "foil",
    },
    "cmp-unacc-002": {
        "participial_form": "none",
        "licensing_marker": "absent_other",
        "constructional_environment": "clausal_predication",
        "local_subject_present": "yes",
        "by_pp_present": "no",
        "stranded_preposition": "no",
        "peripheral_subtype": "comparison_construction",
        "family_status": "foil",
    },
    "cmp-tough-001": {
        "participial_form": "none",
        "licensing_marker": "absent_other",
        "constructional_environment": "clausal_predication",
        "local_subject_present": "yes",
        "by_pp_present": "no",
        "stranded_preposition": "no",
        "peripheral_subtype": "comparison_construction",
        "family_status": "foil",
    },
    "cmp-tough-002": {
        "participial_form": "none",
        "licensing_marker": "absent_other",
        "constructional_environment": "clausal_predication",
        "local_subject_present": "yes",
        "by_pp_present": "no",
        "stranded_preposition": "no",
        "peripheral_subtype": "comparison_construction",
        "family_status": "foil",
    },
    "cmp-needs-001": {
        "participial_form": "gerund_participial",
        "licensing_marker": "absent_other",
        "constructional_environment": "clausal_predication",
        "local_subject_present": "yes",
        "by_pp_present": "no",
        "stranded_preposition": "no",
        "peripheral_subtype": "comparison_construction",
        "family_status": "foil",
    },
    "cmp-getadj-001": {
        "participial_form": "none",
        "licensing_marker": "absent_other",
        "constructional_environment": "clausal_predication",
        "local_subject_present": "yes",
        "by_pp_present": "no",
        "stranded_preposition": "no",
        "peripheral_subtype": "comparison_construction",
        "family_status": "foil",
    },
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def norm(value: str) -> str:
    return value.strip().lower()


def has_local_subject(row: dict[str, str]) -> bool:
    children = row.get("head_children", "")
    return (
        row.get("has_nsubj_pass") == "1"
        or ":nsubj:" in children
        or ":nsubj:pass:" in children
        or children.startswith("nsubj:")
        or children.startswith("nsubj:pass:")
    )


def has_by_pp(row: dict[str, str]) -> bool:
    children = row.get("head_children", "")
    return row.get("has_obl_agent") == "1" or "obl:agent" in children


def participial_form(row: dict[str, str]) -> str | None:
    xpos = norm(row.get("xpos", ""))
    feats = row.get("feats", "")
    if xpos == "vbg" or "VerbForm=Ger" in feats:
        return "gerund_participial"
    if xpos == "vbn" or row.get("participle_like") == "1":
        return "past_participle"
    return None


def prefill_fit_gate_form(key_row: dict[str, str]) -> dict[str, str]:
    stream = key_row.get("pilot_stream", "")
    filled = {
        "participial_form": participial_form(key_row) or "",
        "by_pp_present": "yes" if has_by_pp(key_row) else "no",
        "stranded_preposition": "no",
    }

    if stream == "core_be":
        filled.update(
            licensing_marker="be",
            constructional_environment="clausal_predication",
            local_subject_present="yes",
        )
    elif stream == "foil_perfect":
        filled.update(
            licensing_marker="absent_other",
            constructional_environment="clausal_predication",
            local_subject_present="yes",
            by_pp_present="no",
        )
    elif stream == "foil_copular_participle":
        filled.update(
            licensing_marker="be",
            constructional_environment="clausal_predication",
            local_subject_present="yes",
        )
    elif stream == "foil_participial_modifier":
        filled.update(
            licensing_marker="modifier_position",
            constructional_environment="reduced_modifier",
            local_subject_present="no",
        )
    return filled


def prefill_boundary_form(key_row: dict[str, str]) -> dict[str, str]:
    stream = key_row.get("pilot_stream", "")
    filled = {
        "participial_form": participial_form(key_row) or "",
        "by_pp_present": "yes" if has_by_pp(key_row) else "no",
    }

    if stream == "peripheral_get":
        filled.update(
            licensing_marker="passive_get",
            constructional_environment="clausal_predication",
            local_subject_present="yes" if has_local_subject(key_row) else "",
            stranded_preposition="no",
        )
    elif stream == "peripheral_reduced_embedded":
        if key_row.get("head_deprel") in {"amod", "acl", "acl:relcl"}:
            filled.update(
                licensing_marker="modifier_position",
                constructional_environment="reduced_modifier",
                local_subject_present="no",
                stranded_preposition="no",
            )
        elif norm(key_row.get("parent_form", "")) in {"get", "have", "need"}:
            filled.update(
                licensing_marker="causative_get_have",
                constructional_environment="object_predicative_complement",
                local_subject_present="no",
                stranded_preposition="no",
            )
    elif stream == "peripheral_manual_probe":
        children = key_row.get("head_children", "")
        if "mark:as" in children:
            filled.update(
                licensing_marker="subordinator_or_adjunct",
                constructional_environment="adjunct_participial_clause",
                local_subject_present="no",
                stranded_preposition="no",
            )
        elif norm(key_row.get("parent_form", "")) in {"get", "have", "need"}:
            filled.update(
                licensing_marker="causative_get_have",
                constructional_environment="object_predicative_complement",
                local_subject_present="no",
                stranded_preposition="no",
            )
        elif key_row.get("aux_pass_lemmas") == "be" and "nsubj:pass" in children:
            filled.update(
                licensing_marker="be",
                constructional_environment="clausal_predication",
                local_subject_present="yes",
            )
    return filled


def prefill_row(blind_row: dict[str, str], key_row: dict[str, str]) -> dict[str, str]:
    out = dict(blind_row)
    candidate_id = key_row.get("candidate_id", "")
    sample_set = key_row.get("sample_set", "")

    if candidate_id in COMPARISON_PREFILLS:
        for field, value in COMPARISON_PREFILLS[candidate_id].items():
            if not out.get(field):
                out[field] = value
        return out

    if sample_set in {"analytic_core_candidate", "analytic_foil_candidate"}:
        filled = prefill_fit_gate_form(key_row)
    else:
        filled = prefill_boundary_form(key_row)

    for field, value in filled.items():
        if value and not out.get(field):
            out[field] = value
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blind", required=True, type=Path)
    parser.add_argument("--key", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    blind_rows = read_rows(args.blind)
    key_rows = read_rows(args.key)
    key_by_id = {row["pilot_item_id"]: row for row in key_rows}

    missing = [row["pilot_item_id"] for row in blind_rows if row["pilot_item_id"] not in key_by_id]
    if missing:
        raise SystemExit("Prefill failed: missing key rows for " + ", ".join(missing[:5]))

    prefilled = [prefill_row(row, key_by_id[row["pilot_item_id"]]) for row in blind_rows]
    write_rows(args.output, prefilled, list(blind_rows[0].keys()))


if __name__ == "__main__":
    main()
