#!/usr/bin/env python3
"""Build a passive-adjacent candidate ledger from UD English EWT and GUM."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_feats(raw: str) -> dict[str, str]:
    if raw == "_" or not raw:
        return {}
    feats = {}
    for item in raw.split("|"):
        if "=" in item:
            key, value = item.split("=", 1)
            feats[key] = value
    return feats


def iter_conllu(path: Path):
    meta = {}
    tokens = []
    with path.open(encoding="utf-8", errors="ignore") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            if not line:
                if tokens:
                    yield meta, tokens
                meta = {}
                tokens = []
                continue
            if line.startswith("#"):
                if "=" in line:
                    key, value = line[1:].split("=", 1)
                    meta[key.strip()] = value.strip()
                continue
            cols = line.split("\t")
            if len(cols) != 10:
                continue
            token_id = cols[0]
            if "-" in token_id or "." in token_id:
                continue
            tokens.append(
                {
                    "id": int(token_id),
                    "form": cols[1],
                    "lemma": cols[2],
                    "upos": cols[3],
                    "xpos": cols[4],
                    "feats": parse_feats(cols[5]),
                    "head": cols[6],
                    "deprel": cols[7],
                    "deps": cols[8],
                    "misc": cols[9],
                }
            )
    if tokens:
        yield meta, tokens


def is_participle(token: dict) -> bool:
    return token["xpos"] == "VBN"


def is_finite(token: dict) -> bool:
    return token["feats"].get("VerbForm") == "Fin"


def normalize_streams(streams: set[str]) -> str:
    return ";".join(sorted(streams))


def sentence_text(meta: dict, tokens: list[dict]) -> str:
    if "text" in meta:
        return meta["text"]
    return " ".join(tok["form"] for tok in tokens)


def marked_sentence(tokens: list[dict], head_id: int) -> str:
    marked = []
    for tok in tokens:
        form = tok["form"]
        if tok["id"] == head_id:
            form = f"[[{form}]]"
        marked.append(form)
    return " ".join(marked)


def child_snapshot(children: list[dict]) -> str:
    if not children:
        return "_"
    return ";".join(
        f"{child['id']}:{child['deprel']}:{child['form']}" for child in sorted(children, key=lambda x: x["id"])
    )


def analyze_sentence(corpus: str, split: str, path: Path):
    for meta, tokens in iter_conllu(path):
        by_id = {tok["id"]: tok for tok in tokens}
        children = {tok["id"]: [] for tok in tokens}
        for tok in tokens:
            if tok["head"].isdigit():
                head_id = int(tok["head"])
                if head_id in children:
                    children[head_id].append(tok)

        sent = sentence_text(meta, tokens)
        sent_id = meta.get("sent_id", "")

        for tok in tokens:
            child_nodes = children.get(tok["id"], [])
            aux_pass = [c for c in child_nodes if c["deprel"] == "aux:pass"]
            aux_all = [c for c in child_nodes if c["deprel"] == "aux"]
            cop = [c for c in child_nodes if c["deprel"] == "cop"]
            has_nsubj_pass = any(c["deprel"] == "nsubj:pass" for c in child_nodes)
            has_obl_agent = any(c["deprel"] == "obl:agent" for c in child_nodes)
            has_voice_pass = tok["feats"].get("Voice") == "Pass"
            participle_like = is_participle(tok)
            aux_pass_lemma_set = {c["lemma"].lower() for c in aux_pass}
            aux_lemma_set = {c["lemma"].lower() for c in aux_all}
            cop_lemma_set = {c["lemma"].lower() for c in cop}
            aux_pass_lemmas = sorted(aux_pass_lemma_set)
            aux_lemmas = sorted(aux_lemma_set)
            cop_lemmas = sorted(cop_lemma_set)
            finite_aux_pass_beget = any(
                c["lemma"].lower() in {"be", "get"} and is_finite(c) for c in aux_pass
            )
            passive_like_signal = has_voice_pass or (
                participle_like and (bool(aux_pass) or has_nsubj_pass)
            )

            broad_candidate = any(
                [
                    passive_like_signal,
                    participle_like and bool(cop_lemma_set.intersection({"be", "get"})),
                    participle_like and "have" in aux_lemma_set,
                    participle_like and tok["deprel"] in {"acl", "acl:relcl", "amod"},
                ]
            )
            if not broad_candidate:
                continue

            streams = set()
            if has_voice_pass and has_nsubj_pass and "be" in aux_pass_lemma_set:
                streams.add("core_be")
            if has_voice_pass and has_nsubj_pass and "get" in aux_pass_lemma_set:
                streams.add("peripheral_get")
            if has_voice_pass and tok["deprel"] in {"acl", "acl:relcl", "amod"} and not finite_aux_pass_beget:
                streams.add("peripheral_reduced_embedded")
            if passive_like_signal:
                streams.add("passive_ledger")
            if participle_like and "have" in aux_lemma_set and not has_voice_pass and not aux_pass:
                streams.add("foil_perfect")
            if participle_like and cop_lemma_set.intersection({"be", "get"}) and not has_voice_pass and not aux_pass:
                streams.add("foil_copular_participle")
            if participle_like and tok["deprel"] in {"acl", "acl:relcl", "amod"} and not has_voice_pass and not aux_pass:
                streams.add("foil_participial_modifier")
            if passive_like_signal and not any(
                name in streams for name in {"core_be", "peripheral_get", "peripheral_reduced_embedded"}
            ):
                streams.add("peripheral_manual_probe")
            if not streams:
                continue

            parent = by_id.get(int(tok["head"])) if tok["head"].isdigit() and int(tok["head"]) in by_id else None
            candidate_id = f"{corpus}|{split}|{sent_id}|{tok['id']}"

            yield {
                "candidate_id": candidate_id,
                "corpus": corpus,
                "split": split,
                "source_file": path.name,
                "sent_id": sent_id,
                "head_id": tok["id"],
                "head_form": tok["form"],
                "head_lemma": tok["lemma"],
                "upos": tok["upos"],
                "xpos": tok["xpos"],
                "head_deprel": tok["deprel"],
                "feats": "|".join(f"{k}={v}" for k, v in sorted(tok["feats"].items())) or "_",
                "has_voice_pass": int(has_voice_pass),
                "has_nsubj_pass": int(has_nsubj_pass),
                "has_obl_agent": int(has_obl_agent),
                "aux_pass_lemmas": ";".join(aux_pass_lemmas) or "_",
                "aux_lemmas": ";".join(aux_lemmas) or "_",
                "cop_lemmas": ";".join(cop_lemmas) or "_",
                "participle_like": int(participle_like),
                "parent_id": parent["id"] if parent else "_",
                "parent_form": parent["form"] if parent else "_",
                "parent_deprel": parent["deprel"] if parent else "_",
                "head_children": child_snapshot(child_nodes),
                "provisional_streams": normalize_streams(streams),
                "sentence": sent,
                "sentence_marked": marked_sentence(tokens, tok["id"]),
            }


def write_rows(rows, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "candidate_id",
        "corpus",
        "split",
        "source_file",
        "sent_id",
        "head_id",
        "head_form",
        "head_lemma",
        "upos",
        "xpos",
        "head_deprel",
        "feats",
        "has_voice_pass",
        "has_nsubj_pass",
        "has_obl_agent",
        "aux_pass_lemmas",
        "aux_lemmas",
        "cop_lemmas",
        "participle_like",
        "parent_id",
        "parent_form",
        "parent_deprel",
        "head_children",
        "provisional_streams",
        "sentence",
        "sentence_marked",
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ewt-root", required=True, type=Path)
    parser.add_argument("--gum-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    rows = []
    for corpus, root in [("ewt", args.ewt_root), ("gum", args.gum_root)]:
        for split in ["train", "dev", "test"]:
            path = root / f"en_{corpus}-ud-{split}.conllu"
            rows.extend(analyze_sentence(corpus, split, path))

    write_rows(rows, args.output)


if __name__ == "__main__":
    main()
