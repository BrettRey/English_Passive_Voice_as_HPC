# Annotation Manual

## Purpose

This manual freezes the coding decisions for the confirmatory passive study. The goal is not to encode every subtlety of the English passive. The goal is to apply the same bounded set of decisions consistently enough that both the deterministic baselines and the cue-bundle model remain genuinely testable.

## Unit Of Annotation

Annotate one predicate token per row.

The stable row key is:

1. `candidate_id`
2. `corpus`
3. `split`
4. `sent_id`
5. `head_id`

The predicate token is normally the participial head surfaced by the extraction ledger. If the ledger surfaces an obvious parser error, either:

1. code the row from the actual marked sentence and note the parser issue, or
2. mark the row `exclude` if the token cannot be coded responsibly

## Visible Context And Blindness

During pass-1 coding, the coder should primarily see:

1. `candidate_id`
2. `head_form`
3. `sentence_marked`
4. `sentence`
5. `head_children`

Hide the following fields where practical during pass 1:

1. `corpus`
2. `split`
3. `source_file`
4. `provisional_streams`
5. `sample_set`
6. `sample_rank`

Only unblind corpus or stream information if the row would otherwise be marked `exclude`. If unblinding is used, note it in `notes`.

## Required Columns

Use the schema in `templates/passive_annotation_template.csv`.

The required analytic columns are:

1. `family_status`
2. `peripheral_subtype`
3. `auxiliary_type`
4. `participial_predicate`
5. `agent_realization`
6. `promotion_type`
7. `eventive_stative`
8. `syntactic_environment`
9. `subject_role_profile`
10. `notes`

## Two-Pass Coding Order

Code each row in this order:

1. verify the predicate token and sentence context
2. decide whether the row is `exclude`
3. code the seven cues
4. code `peripheral_subtype`
5. assign `family_status` from the decision table below

Do not assign `family_status` first and backfill the cues to match it.

## Peripheral Subtype

Use one of:

1. `none`
2. `get`
3. `prepositional`
4. `reduced_embedded`
5. `stative_adjectival`
6. `other`

This field is not the confirmatory target. It records the kind of boundary case, if any, after cue coding.

Use `get` only when a form of `get` directly licenses the participial predicate and the row still supports a serious passive-family analysis. Lexical `get` cases that fail the passive-family cues should remain `none` and usually end up as `foil`.

Use `prepositional` only when the promoted subject corresponds to the complement of a retained or stranded preposition.

Use `reduced_embedded` only when the passive-family reading survives in a reduced or embedded environment without a straightforward finite passive profile.

Use `stative_adjectival` only when the row is stative or adjectival but still plausibly adjacent to a passive alternation.

Use `other` rarely. Reserve it for passive-adjacent boundary cases that preserve multiple passive-family cues but do not fit the four preregistered subtypes.

## Family Status

Use one of four values:

1. `core`
2. `peripheral`
3. `foil`
4. `exclude`

### Decision Table

Assign `exclude` if the row cannot be coded responsibly because of parser corruption, missing context, duplicate identity, or severe sentence degradation.

Assign `core` when all are true:

1. `participial_predicate = yes`
2. `promotion_type` is `direct-object-promotion` or `oblique-stranding-promotion`
3. `eventive_stative` is `eventive` or `ambiguous`
4. `peripheral_subtype = none`

Assign `peripheral` when all are true:

1. the row is not `exclude`
2. `participial_predicate = yes`
3. the row preserves a serious passive-family analysis
4. either `peripheral_subtype != none` or the row is passive-like but structurally reduced enough that it should not count as `core`

Assign `foil` to the remaining analyzable rows, including perfects, clearly lexical adjectival participles, resultatives, and other participial predicates without a stable promoted non-agentive participant.

The `peripheral_subtype` field is coded before `family_status`. A boundary subtype is not supposed to be inferred from the final class label.

## Cue Definitions

### 1. Auxiliary Type

Values:

1. `be`
2. `get`
3. `none-other`

Use `be` when the auxiliary directly licensing the participial predicate is a form of `be`.

Use `get` when the auxiliary directly licensing the participial predicate is a form of `get`.

Use `none-other` when:

1. there is no overt passive auxiliary
2. the auxiliary is not `be` or `get`
3. the row is a perfect, modifier, or copular participial foil

Tie-breaker:

If both `be` and `get` appear, code the auxiliary that directly licenses the participial predicate under analysis.

### 2. Participial Predicate

Values:

1. `yes`
2. `no`

Use `yes` when the candidate head is functioning as a past-participial predicate or reduced predicative modifier.

This cue is morphosyntactic, not passive-specific. Perfect-participle foils can still receive `participial_predicate = yes` if the extracted head is genuinely functioning as the participial predicate under analysis.

Use `no` when sentence inspection shows that the extracted token is not the predicate under analysis.

### 3. Agent Realization

Values:

1. `by-phrase`
2. `other-overt-agentive`
3. `none`

Use `by-phrase` when the external argument is overtly realized with canonical `by`.

Use `other-overt-agentive` when an external argument is overtly recoverable but not realized with canonical `by`.

Use `none` when there is no overt external argument.

Tie-breaker:

If an oblique phrase is plausibly instrumental rather than agentive, code `none`.

### 4. Promotion Type

Values:

1. `direct-object-promotion`
2. `oblique-stranding-promotion`
3. `none-unclear`

Use this decision order:

1. identify the surface subject or subject-like element
2. ask whether it corresponds to the verb's internal complement or the complement of a retained preposition
3. use `none-unclear` only if neither promotion analysis is stable

Use `direct-object-promotion` when the subject corresponds to the straightforward internal argument or patient/theme complement.

Use `oblique-stranding-promotion` when the subject corresponds to the complement of a retained or stranded preposition.

Use `none-unclear` when:

1. no promoted participant is identifiable
2. the row is purely adjectival or resultative
3. the subject is expletive or abstract `it`
4. the active paraphrase needed to recover promotion becomes too unstable

Tie-breaker:

Prefer the shortest one-clause active paraphrase possible. Do not rely on long, theory-loaded paraphrases if the surface syntax does not support them.

### 5. Eventive vs Stative

Values:

1. `eventive`
2. `stative`
3. `ambiguous`

Use the diagnostics in this order:

1. does the sentence describe something happening rather than merely a state obtaining
2. does a simple eventive active paraphrase remain natural
3. are eventive diagnostics such as agentive modification or a natural `by`-phrase compatible
4. does the sentence instead primarily describe a resulting state, disposition, or lexical property

Use `eventive` when the row clearly describes an event or process.

Use `stative` when the row clearly describes a state, condition, or lexicalized adjective rather than an event.

Use `ambiguous` when eventive and stative readings both remain genuinely available after sentence-level inspection.

Tie-breaker:

If the evidence is mixed, choose `ambiguous`, not `stative`.

### 6. Syntactic Environment

Values:

1. `finite-clause`
2. `nonfinite-or-reduced`

Use `finite-clause` when the predicate is licensed by overt finite inflection, including finite subordinate clauses.

Use `nonfinite-or-reduced` when the predicate is infinitival, gerundive, reduced, modifier-like, or otherwise lacks a finite clause profile.

### 7. Subject Role Profile

Values:

1. `patient-theme-like`
2. `locative-oblique-like`
3. `unclear-other`

Use `patient-theme-like` when the subject or promoted element behaves like the affected participant, theme, or undergoer.

Use `locative-oblique-like` when the subject corresponds to a locative or other oblique complement, especially in prepositional passives.

Use `unclear-other` when:

1. the subject is expletive or abstract
2. the role cannot be characterized confidently from the sentence
3. the row is too lexicalized or adjectival for a stable role profile

Tie-breaker:

Use the surface subject's role in the shortest plausible active counterpart. Do not force finer role distinctions than the sentence supports.

## Worked Cases

| Example | family_status | peripheral_subtype | auxiliary_type | participial_predicate | agent_realization | promotion_type | eventive_stative | syntactic_environment | subject_role_profile |
|---|---|---|---|---|---|---|---|---|---|
| `The car was stolen by teenagers.` | `core` | `none` | `be` | `yes` | `by-phrase` | `direct-object-promotion` | `eventive` | `finite-clause` | `patient-theme-like` |
| `He got fired after the argument.` | `peripheral` | `get` | `get` | `yes` | `none` | `direct-object-promotion` | `eventive` | `finite-clause` | `patient-theme-like` |
| `This bed was slept in.` | `peripheral` | `prepositional` | `be` | `yes` | `none` | `oblique-stranding-promotion` | `eventive` | `finite-clause` | `locative-oblique-like` |
| `The report submitted yesterday was missing a page.` | `peripheral` | `reduced_embedded` | `none-other` | `yes` | `none` | `direct-object-promotion` | `eventive` | `nonfinite-or-reduced` | `patient-theme-like` |
| `The door is closed.` | `peripheral` | `stative_adjectival` | `be` | `yes` | `none` | `none-unclear` | `ambiguous` | `finite-clause` | `unclear-other` |
| `She has finished the report.` | `foil` | `none` | `none-other` | `yes` | `none` | `none-unclear` | `eventive` | `finite-clause` | `unclear-other` |

## Hard-Case Defaults

Use these defaults to avoid silent drift:

1. if a `get` row lacks a stable promoted non-agentive participant, leave `peripheral_subtype = none` and prefer `foil`
2. if a row preserves a stranded preposition with a promoted complement, use `prepositional` and `oblique-stranding-promotion`
3. if a row is reduced or modifier-like but still clearly passive-adjacent, prefer `peripheral` over `core`
4. if a row is stative but still plausibly tied to a passive alternation, prefer `stative_adjectival` plus `peripheral`
5. if a row is merely participial with no serious passive-family analysis, prefer `foil`
6. if eventivity remains open after sentence-level inspection, use `ambiguous`

## Reliability Procedure

Before confirmatory fitting:

1. annotate a fit-gate pilot batch of 100 rows:
   25 `core` and 25 `foil` candidates from EWT, plus 25 `core` and 25 `foil` candidates from GUM
2. annotate a separate 16-row boundary mini-pilot:
   per corpus, 2 `peripheral_get`, 2 `peripheral_reduced_embedded`, and 4 `peripheral_manual_probe` candidates
3. keep the coder-facing sheets blind to `candidate_id`; use the generated `pilot_item_id` instead
4. wait at least 14 days
5. re-annotate both pilots blind to the first pass
6. compute kappa for each confirmatory cue and for `family_status` on the 100-row fit-gate pilot
7. compute `peripheral_subtype` kappa on the 16-row boundary mini-pilot

Targets:

1. `kappa >= 0.80` for each confirmatory cue
2. `kappa >= 0.80` for `family_status`
3. `kappa >= 0.70` for `peripheral_subtype`

Operational commands:

```bash
python scripts/build_study1_pilot.py \
  --input data/prereg_sampling/primary_annotation_pack.csv \
  --output-dir data/pilot

python scripts/score_reliability_kappa.py \
  --first annotations/study1_pilot_first_pass_annotated.csv \
  --second annotations/study1_pilot_second_pass_annotated.csv \
  --output data/pilot/study1_pilot_reliability.csv \
  --require-thresholds

python scripts/score_reliability_kappa.py \
  --first annotations/study1_boundary_pilot_first_pass_annotated.csv \
  --second annotations/study1_boundary_pilot_second_pass_annotated.csv \
  --output data/pilot/study1_boundary_pilot_reliability.csv \
  --fields peripheral_subtype \
  --require-thresholds
```

If `eventive_stative`, `promotion_type`, or `subject_role_profile` fails:

1. tighten the manual
2. re-run the 100-row check
3. if it still fails, drop that cue from the confirmatory model and keep it descriptive only

If `family_status` fails while the individual cues are stable, revise the decision table before full annotation and log the change explicitly.
