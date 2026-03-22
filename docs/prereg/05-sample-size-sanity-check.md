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
2. `participial_form`: 2
3. `licensing_marker`: 5
4. `constructional_environment`: 6
5. `local_subject_present`: 1
6. `by_pp_present`: 1
7. `stranded_preposition`: 1
8. `event_implied`: 2
9. `agent_implied`: 2
10. `predicand_as_undergoer`: 2

Maximum total:

1. 22 coefficients

At `n = 120` training rows per direction, this is roughly `5.5` rows per coefficient before any benefit from regularizing priors.

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
3. the restructured cue set is more interpretable, but it is also larger

## Fake-Data Gate

Before full annotation is locked, run a bounded fake-data adequacy check using the pilot-coded rows.

Procedure:

1. annotate and reliability-check an initial 100-row pilot with 25 `core` and 25 `foil` rows from each corpus
2. if reclassification to `peripheral` leaves a corpus below 25 usable `core` or `foil` rows, draw a deterministic supplement from unused candidates of the affected class and annotate it once
3. fit the preregistered Bayesian logistic model to the usable pilot `core + foil` rows, including any supplement rows drawn under step 2
4. use posterior draws from that pilot fit as generating parameters for at least 200 simulated datasets at the planned per-corpus quotas
5. in each simulated dataset, refit the preregistered model and evaluate the strict and stronger checklist comparisons under the same transfer setup
6. record how often the simulated study would satisfy the preregistered Brier criteria
7. if either gate estimate lands within `0.02` of its decision threshold, rerun the gate at `1000` simulations and use that higher-resolution estimate for the preregistration decision

Operational command:

```bash
Rscript scripts/run_study1_fake_data_gate.R \
  --pilot-key data/pilot/study1_pilot_key.csv \
  --annotated-pilot annotations/study1_pilot_first_pass_annotated.csv \
  --output-dir data/fake_data_gate
```

If a supplement was needed, add:

```bash
  --supplement-key data/pilot/study1_pilot_supplement_key.csv \
  --supplement-annotated annotations/study1_pilot_supplement_annotated.csv \
```

Expected outputs:

1. `data/fake_data_gate/study1_fake_data_gate_summary.csv`
2. `data/fake_data_gate/study1_fake_data_gate_simulations.csv`
3. `data/fake_data_gate/study1_fake_data_gate_pilot_counts.csv`

Proceed with the current quotas only if both are true:

1. at least 75% of simulated datasets satisfy the strict-checklist criterion in both transfer directions
2. at least 60% of simulated datasets satisfy the stronger-rule criterion in both transfer directions

The `200`-simulation run is the minimum gate. It is adequate for clear passes or clear failures, but it is not the final decision surface for near-threshold cases. In the current v2 pilot, the corrected surface-based baseline produced a borderline `200`-simulation result (`strict_pass_rate = 0.745`, `stronger_pass_rate = 0.835`), so the gate was rerun at `1000` simulations. That higher-resolution rerun yielded `strict_pass_rate = 0.788` and `stronger_pass_rate = 0.844`, which is the result that governs the preregistration decision.

If either condition fails, do not file the preregistration unchanged. Raise `core + foil` quotas, reduce predictor complexity, or both.

The separate 16-row boundary mini-pilot is for subtype reliability only. It consists of 8 passive-boundary rows plus 8 fixed comparison-construction items, and it does not replace the 100-row `core + foil` fit-gate pilot used in the fake-data adequacy check. If fit-gate reclassification creates a usable-count shortfall, the deterministic supplement above repairs the gate input without changing the reliability basis.

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
