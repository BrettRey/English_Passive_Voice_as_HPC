# Preregistration Packet

This folder turns the revised passive plan into concrete preregistration artifacts.

The packet currently contains:

1. `01-annotation-manual.md`
   Hard decision rules for the seven cues, family-status coding, exclusions, and reliability procedure.
2. `02-extraction-and-sampling.md`
   Exact corpus paths, candidate streams, sampling quotas, deduplication, exclusions, and seed policy.
3. `03-baseline-rules.md`
   The strict and stronger deterministic checklist comparators in prose and table form.
4. `04-analysis-spec.md`
   The confirmatory model formula, reference levels, metrics, evaluation flow, and deviation policy.
5. `05-sample-size-sanity-check.md`
   A bounded sample-size check using the current corpus counts and model complexity.
6. `06-external-validation-study.md`
   A companion judgment study that tests whether Study 1 probabilities predict independent structural and discourse behavior.

Support artifacts:

1. `scripts/extract_ud_passive_candidates.py`
   Builds a candidate ledger from EWT and GUM `.conllu` files.
2. `scripts/sample_from_ledger.py`
   Draws the held-out slice, analytic candidate packs, and deterministic replacement queue from the ledger.
3. `scripts/finalize_annotated_sample.py`
   Converts annotated primary and replacement rows into the frozen preregistered sample with quota checks.
4. `scripts/apply_checklist_baselines.py`
   Applies the deterministic checklist baselines to an annotated CSV.
5. `scripts/build_external_validation_lists.py`
   Builds deterministic participant lists for the structural and discourse tasks in Study 2.
6. `scripts/build_study1_pilot.py`
   Builds the deterministic 100-row Study 1 reliability pilot and blinded first/second-pass files.
7. `scripts/score_reliability_kappa.py`
   Compares two annotated pilot passes and reports kappa against the preregistered thresholds.
8. `templates/passive_annotation_template.csv`
   Minimal annotation sheet schema for the manual and scripts.
9. `templates/external_validation_item_bank.csv`
   Frozen schema for the Study 2 item bank after stimulus construction.

This packet is meant to be the operational bridge between:

1. the strategic plan in `docs/plans/REVISED-PLAN-2026-03-19.md`
2. a formal preregistration
3. the later manuscript sections in `main.tex`

The packet now defines two linked studies:

1. `Study 1`
   Cross-corpus transfer of the passive-family cue bundle against deterministic checklists.
2. `Study 2`
   External validation against independent human judgments on structural licensing and discourse fit.
