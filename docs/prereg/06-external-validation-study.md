# Study 2 External Validation

## Purpose

`Study 2` tests whether the graded passive-family predictions from `Study 1` track independent linguistic behavior that is not used in the corpus labels or checklist rules.

The point of `Study 2` is not to refit the passive family again. The point is to ask whether out-of-corpus passive-family probabilities predict:

1. structural licensing behavior associated with verbal passives
2. discourse-fit behavior associated with passive information packaging

This is the purpose-indexed payoff that the HPC framing requires.

## Relation To Study 1

For each `Study 2` item, derive three preregistered predictors from `Study 1`:

1. `study1_transferred_prob`
   The posterior-mean passive-family probability from the model trained on the opposite corpus.
   Use the GUM-trained model for EWT-origin items and the EWT-trained model for GUM-origin items.
2. `strict_checklist`
3. `stronger_rule`

`Study 2` therefore does not use same-corpus fitted probabilities. It uses the transferred predictions that `Study 1` claims are projectible.

## Item Bank

Build a frozen `Study 2` item bank of `108` base items:

1. `18` `core`
2. `18` `foil`
3. `18` `get`
4. `18` `prepositional`
5. `18` `reduced_embedded`
6. `18` `stative_adjectival`

Balance across EWT and GUM as closely as possible.

If the finalized `Study 1` analytic sample does not supply enough editable items for a subtype, continue annotation down the same-corpus replacement queues before recording a prereg deviation.

## Source Pool

Select `Study 2` items from manually annotated rows only:

1. the final `Study 1` analytic sample
2. annotated replacement rows from the same corpus and same broad queue if more items are needed

Each `Study 2` item must map to exactly one `candidate_id`.

Do not use unannotated rows.

## Editability Rules

An item is eligible for the `Study 2` bank only if all are true:

1. the sentence can be lightly normalized into readable experimental English without changing the construction type
2. the target predicate remains recoverable after trimming local clutter
3. no world knowledge or private named-entity context is needed to understand the judgment prompt
4. a structural probe can be written without changing the target construction
5. two short discourse contexts can be written without rewriting the target sentence itself

Allowed edits:

1. punctuation cleanup
2. contraction expansion or normalization
3. replacement of incidental names with neutral labels
4. trimming of non-essential adjuncts

Disallowed edits:

1. changing passive to active or vice versa in the target sentence
2. changing the construction subtype used for sampling
3. adding or deleting core argument-structure material in the target sentence

## Item-Bank Schema

Freeze the stimulus bank in `templates/external_validation_item_bank.csv`.

Each row must include:

1. `stimulus_id`
2. `source_candidate_id`
3. `origin_corpus`
4. `group_label`
5. `base_sentence`
6. `base_sentence_marked`
7. `structural_probe_type`
8. `structural_probe_text`
9. `discourse_context_patient`
10. `discourse_context_agent`
11. `include_structural`
12. `include_discourse`
13. `study1_transferred_prob`
14. `strict_checklist`
15. `stronger_rule`
16. `notes`

## Task A: Structural Licensing

### Question

Do transferred passive-family probabilities predict independent judgments about whether the target sentence supports a verbal-passive-style structural continuation?

### Materials

Use all `108` banked items.

Each item receives exactly one frozen structural continuation:

1. `by_phrase`
   Add a short canonical `by` phrase when semantically coherent.
2. `agentive_adverb`
   Add an agentive adverb such as `deliberately`, `carefully`, or `intentionally` when a `by` phrase would be awkward or overly lexicalized.

The target sentence itself remains unchanged. Only the continuation is added.

### Participant Task

Participants rate the naturalness of the full sentence plus continuation on a `1` to `7` scale.

Scale anchors:

1. `1 = completely unnatural`
2. `7 = completely natural`

### Lists

Use two deterministic lists of `54` items each.

Each list must contain:

1. `9` `core`
2. `9` `foil`
3. `9` `get`
4. `9` `prepositional`
5. `9` `reduced_embedded`
6. `9` `stative_adjectival`

### Participant Target

Target `72` participants total:

1. `36` per list

Minimum analyzable total after exclusions:

1. `60`

## Task B: Discourse Fit

### Question

Do transferred passive-family probabilities predict when the target sentence fits better after patient-given context than after agent-given context?

### Materials

Use all `108` banked items.

Each item receives two short frozen contexts:

1. `patient_given`
   The patient, theme, or promoted participant is already discourse-given; the agent is new, absent, or backgrounded.
2. `agent_given`
   The agent or source is discourse-given; the patient or promoted participant is not established as the discourse topic.

The target sentence remains the same across both contexts.

### Participant Task

Participants read the short context and then rate the naturalness of the target sentence as the next sentence on a `1` to `7` scale.

### Lists

Use four deterministic lists of `54` items each.

Construction:

1. split the `108` items into two balanced halves of `54`
2. each half is shown on two lists
3. the second list for a half reverses the context assignment for every item

This gives each item both context conditions across participants while keeping each participant at `54` judgments.

### Participant Target

Target `96` participants total:

1. `24` per list

Minimum analyzable total after exclusions:

1. `80`

## Participant Eligibility

For both tasks:

1. age `18` or older
2. self-identified native or near-native English speaker
3. located in an English-dominant country or with equivalent long-term English exposure
4. no prior participation in the other list of the same task

## Participant Exclusions

Exclude a participant from confirmatory analysis if any of the following holds:

1. incomplete submission
2. failed both attention checks in the task
3. duplicate participation detected by platform ID
4. completion time below one third of the median task time
5. response-stringing with identical ratings on more than `90%` of trials

## Structural Predictions

The preregistered subtype expectations are:

1. `core` should show the highest compatibility with structural licensing probes
2. `foil` should show the lowest compatibility
3. `get` and `prepositional` should pattern above `foil` and closer to `core`
4. `reduced_embedded` should pattern above `foil` but below `core` on average
5. `stative_adjectival` should remain lower than `core`, and may overlap the lower peripheral range

## Discourse Predictions

The preregistered subtype expectations are:

1. `core` should show a positive patient-given context advantage
2. `get`, `prepositional`, and `reduced_embedded` should also show positive patient-given context advantage
3. `foil` should show little or no patient-given advantage
4. `stative_adjectival` may show weaker or mixed context advantage and is not required to pattern like `core`

## Models

Treat ratings as approximately continuous on the `1` to `7` scale.

### Task A Model

Fit a Bayesian multilevel Gaussian model:

`rating_ij = alpha + beta_1 * study1_transferred_prob_j + beta_2 * probe_type_j + u_i + v_j + error_ij`

where:

1. `u_i` is a varying intercept for participant
2. `v_j` is a varying intercept for item

Fit two comparison models by replacing `study1_transferred_prob_j` with:

1. `strict_checklist`
2. `stronger_rule`

### Task B Model

Fit a Bayesian multilevel Gaussian model:

`rating_ij = alpha + beta_1 * patient_context_ij + beta_2 * study1_transferred_prob_j + beta_3 * patient_context_ij * study1_transferred_prob_j + u_i + v_j + error_ij`

Fit two comparison models by replacing `study1_transferred_prob_j` with:

1. `strict_checklist`
2. `stronger_rule`

## Success Criteria

`Study 2` supports the external-payoff claim only if all are true:

1. in Task A, `Pr(beta_1 > 0) >= 0.95`
2. in Task B, `Pr(beta_3 > 0) >= 0.95`
3. in Task A, the `study1_transferred_prob` model outpredicts both checklist comparison models by positive PSIS-LOO difference
4. in Task B, the `study1_transferred_prob` interaction model outpredicts both checklist comparison models by positive PSIS-LOO difference
5. the estimated mean structural-probe rating for `core` exceeds `foil` by at least `0.75`
6. the estimated patient-given context advantage for `core` exceeds `foil` by at least `0.50`

If criteria `1` through `4` hold but one of `5` or `6` fails, treat the external validation as partial support rather than full confirmation.

## Interpretation

If both `Study 1` and `Study 2` succeed, the paper may claim:

1. the passive-family cue bundle projects across corpora
2. the same transferred probabilities predict independent structural licensing behavior
3. the same transferred probabilities predict independent discourse-fit behavior

If `Study 1` succeeds but `Study 2` fails, narrow the paper's claim to corpus projectibility only.

If `Study 2` succeeds on structural licensing but not discourse fit, claim structural extension only and do not overstate discourse payoffs.

## Deterministic List Building

Build the participant lists with:

```bash
python scripts/build_external_validation_lists.py \
  --input stimuli/external_validation_item_bank.csv \
  --output-dir stimuli/external_validation_lists
```

The script must:

1. fail loudly if the bank is not exactly balanced by `group_label`
2. write two structural lists of `54` items each
3. write four discourse lists of `54` items each
4. preserve fixed deterministic assignment under the global seed
