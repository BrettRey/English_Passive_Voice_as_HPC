# Baseline Rules

## Purpose

This artifact freezes the deterministic competitors.

The confirmatory comparison is:

1. strict checklist baseline
2. stronger rule-based comparator
3. Bayesian cue-bundle model

The deterministic baselines operate on annotated rows, not raw corpus strings.

## Required Input Columns

The baseline script expects:

1. `auxiliary_type`
2. `participial_predicate`
3. `has_nsubj_pass` when available
4. `promotion_type` as fallback only if `has_nsubj_pass` is unavailable
5. `eventive_stative`

The recommended full schema is in `templates/passive_annotation_template.csv`.

## Strict Checklist Baseline

A row is predicted `1` by the strict checklist if and only if all are true:

1. `auxiliary_type` is `be` or `get`
2. `participial_predicate` is `yes`
3. a promoted-subject signal is present

The promoted-subject signal is defined as:

1. `has_nsubj_pass = 1` if that extraction column is present
2. otherwise `promotion_type` is `direct-object-promotion` or `oblique-stranding-promotion`

Otherwise predict `0`.

This keeps the strict checklist as surface-oriented as the available annotation permits. It does not require the full cue bundle or the final `family_status` label.

## Stronger Rule-Based Comparator

A row is predicted `1` by the stronger comparator if and only if all are true:

1. the strict checklist returns `1`
2. `eventive_stative` is not `stative`

Otherwise predict `0`.

`ambiguous` counts as allowed here. The stronger comparator excludes only clearly non-eventive rows.

## Why Promotion Counts This Way

The promoted-subject condition is not restricted to direct-object promotion only.

A row satisfies the condition if it has a promoted non-agentive subject, including:

1. direct-object promotion
2. oblique-stranding promotion

That makes the baseline stronger and avoids building in an artificial bias against prepositional passives.

## Truth Table

| auxiliary_type | participial_predicate | promoted-subject signal | eventive_stative | strict_checklist | stronger_rule |
|---|---|---|---|---|---|
| `be` | `yes` | `yes` | `eventive` | `1` | `1` |
| `get` | `yes` | `yes` | `eventive` | `1` | `1` |
| `be` | `yes` | `yes` | `ambiguous` | `1` | `1` |
| `be` | `yes` | `no` | `ambiguous` | `0` | `0` |
| `none-other` | `yes` | `yes` | `eventive` | `0` | `0` |
| `be` | `yes` | `yes` | `stative` | `1` | `0` |

## Executable Form

Use:

```bash
python scripts/apply_checklist_baselines.py \
  --input annotations/passive_annotations.csv \
  --output annotations/passive_annotations_with_baselines.csv
```

The script adds:

1. `strict_checklist`
2. `stronger_rule`

These are numeric `0/1` predictions and should be treated as deterministic probabilities in Brier-score comparisons.

## Non-Confirmatory Uses

The baseline outputs may also be used for:

1. confusion tables
2. classwise error inspection
3. peripheral-case profiling

But those uses are secondary to the preregistered transfer comparison.
