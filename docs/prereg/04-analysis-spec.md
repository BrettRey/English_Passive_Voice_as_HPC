# Study 1 Confirmatory Corpus Analysis Specification

This file governs `Study 1` only.

The companion external-validation experiment is preregistered in `06-external-validation-study.md`.

## Confirmatory Question

Does a probabilistic cue-bundle account of the English passive family generalize better across corpora than deterministic checklist baselines do?

## Data Partitions

Use two corpora:

1. EWT
2. GUM

Use four row classes:

1. `core`
2. `peripheral`
3. `foil`
4. `exclude`

## Binary Fit Label

Define:

1. `passive_family_binary = 1` for `core`
2. `passive_family_binary = 0` for `foil`
3. `passive_family_binary = NA` for `peripheral` and `exclude`

The confirmatory fit is binary. Peripheral rows are not forced into the fit target.

## Predictors

The confirmatory predictor set is:

1. `auxiliary_type`
2. `participial_predicate`
3. `agent_realization`
4. `promotion_type`
5. `eventive_stative`
6. `syntactic_environment`
7. `subject_role_profile`

## Reference Levels

Use treatment coding with the most foil-like level as reference where possible:

1. `auxiliary_type = none-other`
2. `participial_predicate = no`
3. `agent_realization = none`
4. `promotion_type = none-unclear`
5. `eventive_stative = stative`
6. `syntactic_environment = nonfinite-or-reduced`
7. `subject_role_profile = unclear-other`

## Model

Fit a Bayesian logistic regression:

`logit(P(passive_family_binary_j = 1)) = beta_0 + sum_i beta_i x_ji`

Priors:

1. `beta_0 ~ Normal(0, 2.5)`
2. `beta_k ~ Normal(0, 2.5)` for all slope terms

Implementation target:

1. `brms` or `cmdstanr`

Sampler defaults:

1. 4 chains
2. 2000 warmup iterations per chain
3. 2000 post-warmup iterations per chain
4. `adapt_delta = 0.95`

Escalate `adapt_delta` to `0.99` before changing anything else if divergences appear.

## Confirmatory Fit Directions

Fit exactly two models:

1. train on EWT `core + foil`, test on GUM `core + foil`
2. train on GUM `core + foil`, test on EWT `core + foil`

In each direction, apply the fitted model without refitting to:

1. the held-out `peripheral` rows in the target corpus
2. the naturalistic held-out slice in the target corpus

## Deterministic Comparators

Compute:

1. `strict_checklist`
2. `stronger_rule`

using `scripts/apply_checklist_baselines.py`.

Treat their `0/1` outputs as deterministic probabilities for Brier-score comparison.

## Primary Metric

Primary confirmatory metric:

1. Brier score

Compute primary Brier comparisons only on rows with non-missing `passive_family_binary`, that is:

1. `core`
2. `foil`

Do not compute confirmatory Brier on `peripheral` rows.

## Secondary Summaries

Secondary summaries are preregistered but subordinate:

1. accuracy on `core` vs `foil`
2. calibration plots
3. error breakdown by corpus
4. probability distribution on `peripheral` rows
5. results on the naturalistic held-out slice restricted to rows with non-missing binary labels

## Primary Estimands

For each transfer direction `d` and deterministic baseline `b`, define:

`Delta_{d,b} = Brier_{d,b} - Brier_{d,bayes}`

Positive values favor the Bayesian cue-bundle model.

Compute `Brier_{d,bayes}` for each posterior draw on the target corpus. The deterministic baselines remain fixed, so each comparison yields a posterior distribution over `Delta_{d,b}`.

## Peripheral Evaluation

Peripheral rows are evaluated by gradedness, not by binary accuracy.

Define the middle-region indicator:

`mid(p) = 1` if `p` falls in `[0.2, 0.8]`, else `0`.

Use posterior-mean predicted probabilities from the transferred Bayesian model.

The preregistered gradedness criteria are:

1. at least 60% of pooled `peripheral` rows have `mid(p) = 1`
2. the `peripheral` middle-region rate exceeds the `core` middle-region rate by at least `0.20`
3. the `peripheral` middle-region rate exceeds the `foil` middle-region rate by at least `0.20`
4. at least 3 of the 4 preregistered peripheral subtypes with usable counts exceed both the pooled `core` and pooled `foil` middle-region rates

Also report:

1. median peripheral probability
2. interquartile range
3. comparison to core and foil distributions
4. middle-region rate by peripheral subtype

## Naturalistic Slice Evaluation

For the naturalistic held-out slice:

1. compute Brier only on rows coded `core` or `foil`
2. report peripheral probabilities descriptively
3. report the proportion of exclusions

This keeps the main target binary while preserving the boundary-case probe.

## Success Criteria

Projectibility is supported only if all are true:

1. for both transfer directions, `Pr(Delta_{d,strict_checklist} > 0.01) >= 0.90`
2. for both transfer directions, `Pr(Delta_{d,stronger_rule} > 0.005) >= 0.80`
3. on the pooled naturalistic held-out rows with non-missing binary labels, `Pr(Delta_{pooled,strict_checklist} > 0) >= 0.80`
4. on the pooled naturalistic held-out rows with non-missing binary labels, `Pr(Delta_{pooled,stronger_rule} > 0) >= 0.67`
5. the preregistered gradedness criteria in the peripheral evaluation section all hold
6. at least 80% of pooled `core` rows have posterior-mean predicted probability above `0.8`
7. at least 80% of pooled `foil` rows have posterior-mean predicted probability below `0.2`

If criterion 1 fails in either direction, do not claim confirmatory projectibility support.

If criteria 1 through 4 hold but the gradedness criteria fail, the study may support transfer but not the stronger boundary-structure claim.

## Study 1 Linguistic Payoffs

If the success criteria hold, `Study 1` will support only these corpus-level linguistic inferences:

1. a cue-bundle analysis projects more reliably across corpora than a short checklist does, so passive-family membership is not exhausted by `be/get + participle + promoted subject`
2. boundary cases are not just undifferentiated model uncertainty: preregistered peripheral subtypes occupy the model's middle region more often than either canonical passives or foils do
3. passive-family extension from canonical `be` passives to at least some `get`, prepositional, reduced, or stative-adjacent cases is empirically better modeled as graded transfer than as deterministic inclusion across corpora

Claims about independent structural licensing or discourse-fit payoffs are reserved for `Study 2`. They are not licensed by `Study 1` alone.

If the success criteria do not hold, the paper will not claim that the corpus study confirms an HPC-style projectibility advantage.

## Diagnostics

Minimum fit checks:

1. `Rhat < 1.01`
2. no unresolved divergent transitions
3. no obviously pathological posterior predictive behavior on the binary target

## Pre-Registered Deviations

Only the following deviations are allowed without rewriting the study design:

1. if a cue fails the reliability threshold, drop it from the confirmatory model and keep it descriptive only
2. if a predictor has zero variance in a training corpus, drop it for that direction and report the invariance
3. if corpus extraction produces fewer valid rows than the quota after screening, continue down the same corpus stream before considering any broader revision

Any other change should be logged explicitly as a prereg deviation.

## Exploratory Analyses

These are allowed, but must be labeled exploratory:

1. cue importance rankings
2. alternate threshold displays
3. supplementary mixed-effects or hierarchical variants
4. broader analyses using OANC or other corpora
