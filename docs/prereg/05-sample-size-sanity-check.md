# Sample-Size Sanity Check

## Purpose

This is not a full power analysis. It is a bounded sanity check to make sure the current confirmatory design is not obviously underbuilt.

## Availability Check

Local corpus counts show that candidate availability is not the bottleneck.

Observed passive-related marker counts:

| Corpus | `Voice=Pass` | `nsubj:pass` | `aux:pass` | `obl:agent` |
|---|---:|---:|---:|---:|
| EWT | 3261 | 3292 | 3294 | 796 |
| GUM | 3334 | 3411 | 3537 | 883 |

The study is therefore annotation-limited, not corpus-limited.

## Current Planned Design

Planned totals:

1. 320 stratified analytic rows
2. 80 naturalistic held-out rows

Per corpus analytic targets:

1. 60 `core`
2. 40 `peripheral`
3. 60 `foil`

That means the binary training set in each transfer direction is:

1. 60 `core`
2. 60 `foil`
3. total `n = 120`

## Model Complexity Check

Maximum coefficient count under the current coding scheme:

1. intercept: 1
2. `auxiliary_type`: 2
3. `participial_predicate`: 1
4. `agent_realization`: 2
5. `promotion_type`: 2
6. `eventive_stative`: 2
7. `syntactic_environment`: 1
8. `subject_role_profile`: 2

Maximum total:

1. 13 coefficients

At `n = 120` training rows per direction, this is roughly `9.2` rows per coefficient before any benefit from regularizing priors.

## Interpretation

This is acceptable as a lower bound, but it is not generous.

Why it is still defensible:

1. the priors are regularizing
2. the target is binary
3. some cues may be near-invariant and therefore drop from the effective fit
4. the main claim is comparative transfer against deterministic baselines, not fine-grained coefficient estimation

Why caution remains warranted:

1. some predictor levels may be sparse within one corpus
2. the fit set per direction is smaller than the total annotated sample makes it look

## Fake-Data Gate

Before full annotation is locked, run a bounded fake-data adequacy check using the pilot-coded rows.

Procedure:

1. annotate and reliability-check an initial 100-row pilot with 25 `core` and 25 `foil` rows from each corpus
2. fit the preregistered Bayesian logistic model to the pilot `core + foil` rows
3. use posterior draws from that pilot fit as generating parameters for at least 200 simulated datasets at the planned per-corpus quotas
4. in each simulated dataset, refit the preregistered model and evaluate the strict and stronger checklist comparisons under the same transfer setup
5. record how often the simulated study would satisfy the preregistered Brier criteria

Proceed with the current quotas only if both are true:

1. at least 75% of simulated datasets satisfy the strict-checklist criterion in both transfer directions
2. at least 60% of simulated datasets satisfy the stronger-rule criterion in both transfer directions

If either condition fails, do not file the preregistration unchanged. Raise `core + foil` quotas, reduce predictor complexity, or both.

## Decision Rule

Proceed with the current 400-row total only if all of the following hold after ledger construction and pilot annotation:

1. each corpus yields at least 60 usable `core` rows
2. each corpus yields at least 60 usable `foil` rows
3. no more than one predictor is invariant within a training corpus
4. no essential non-reference level is effectively absent from both corpora
5. the fake-data gate above is passed

If any of those fails:

1. increase the `core + foil` quotas before full annotation, or
2. simplify the confirmatory predictor set before fitting

## Preferred But Optional Expansion

A stronger version of the design would raise the analytic sample to:

1. 160 `core`
2. 80 `peripheral`
3. 160 `foil`
4. plus the same 80-row naturalistic slice

That would yield `n = 160` binary training rows per transfer direction if balanced across corpora.

This expansion is preferred, not required. The current design remains the minimum viable prereg target.
