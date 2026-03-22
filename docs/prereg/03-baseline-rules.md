# Baseline Rules

## Purpose

This artifact freezes the deterministic competitors.

The confirmatory comparison is:

1. strict checklist baseline
2. stronger rule-based comparator
3. Bayesian cue-bundle model

The deterministic baselines operate on annotated rows plus the extraction metadata
that remains attached to them. They are meant to approximate strong
surface-oriented checklists, not to reuse the gold functional cue
`licensing_marker`.

This wording is deliberate. An earlier v2 draft defined the checklist over the
annotated field `licensing_marker`; the pilot fake-data gate showed that this
made the comparator too gold-like and effectively perfect on the initial
core/foil pilot. Before preregistration, the baseline was corrected to use
overt surface `be/get` material instead.

## Required Input Columns

The baseline script expects:

1. `participial_form`
2. `local_subject_present`
3. `event_implied`
4. `aux_pass_lemmas`
5. `aux_lemmas`
6. `cop_lemmas`

The recommended full schema is in `templates/passive_annotation_template.csv`.

Use a merged analysis table here, not the bare blind annotation working sheet.
The script needs the retained extraction metadata columns listed above.

## Strict Checklist Baseline

A row is predicted `1` by the strict checklist if and only if all are true:

1. a surface form of `be` or `get` appears in `aux_pass_lemmas`, `aux_lemmas`, or `cop_lemmas`
2. `participial_form` is `past_participle`
3. `local_subject_present` is `yes`

Otherwise predict `0`.

This keeps the strict checklist genuinely surface-oriented. It uses overt
`be/get` material and basic form cues, so it can overgenerate on copular and
other passive-looking foils rather than inheriting the analyst's functional
`licensing_marker` judgment.

## Stronger Rule-Based Comparator

A row is predicted `1` by the stronger comparator if and only if all are true:

1. the strict checklist returns `1`
2. `event_implied` is not `no`

Otherwise predict `0`.

`unclear` counts as allowed here. The stronger comparator excludes only clearly non-eventive rows.

## Truth Table

| surface_be/get_present | participial_form | local_subject_present | event_implied | strict_checklist | stronger_rule |
|---|---|---|---|---|---|
| `yes` | `past_participle` | `yes` | `yes` | `1` | `1` |
| `yes` | `past_participle` | `yes` | `unclear` | `1` | `1` |
| `yes` | `past_participle` | `no` | `unclear` | `0` | `0` |
| `no` | `past_participle` | `yes` | `yes` | `0` | `0` |
| `yes` | `past_participle` | `yes` | `no` | `1` | `0` |

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
