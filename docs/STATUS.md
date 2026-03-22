# Project Status

Date: 2026-03-22

## Current State

The preregistration packet is now in its v2 cue-scheme form and is pushed on
`master` at commit `8802f21`. Study 1's corrected surface-based fake-data gate
has passed at the canonical documented path
[`data/fake_data_gate/`](data/fake_data_gate), with the decisive rerun at
`1000` simulations clearing both thresholds.

The only remaining preregistration blocker is the delayed second blind pass and
reliability check. Per the manual, that pass is intentionally deferred until
2026-04-05 so the `14`-day lag is real rather than nominal.

## Completed

1. Replaced the mixed v1 annotation scheme with the v2 form/meaning split and migrated the prereg packet, template, pilot builder, scorer, and fake-data gate workflow.
2. Added comparison-construction items, including `Twenty people died.`, to the boundary mini-pilot and manual.
3. Corrected the deterministic baselines so they use overt surface `be/get` material rather than the gold functional field `licensing_marker`.
4. Built and annotated the v2 fit-gate pilot, boundary mini-pilot, and deterministic fit-gate supplement.
5. Ran the corrected fake-data gate twice: a borderline `200`-simulation pass-rate estimate and a decisive `1000`-simulation rerun that passes.
6. Synced bibliography handling back to the house-style pattern: central `references.bib` symlink plus local `references-local.bib`.
7. Committed and pushed the full v2 packet state at `8802f21`.

## Immediate Open Work

1. On or after 2026-04-05, complete [annotations/study1_pilot_v2_second_pass_prefilled.csv](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/English_Passive_Voice_as_HPC/annotations/study1_pilot_v2_second_pass_prefilled.csv).
2. On or after 2026-04-05, complete [annotations/study1_boundary_pilot_v2_second_pass_prefilled.csv](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/English_Passive_Voice_as_HPC/annotations/study1_boundary_pilot_v2_second_pass_prefilled.csv).
3. Run `scripts/score_reliability_kappa.py` on both second-pass files and inspect the resulting reliability CSVs.
4. If reliability thresholds pass, cut the preregistration release and file preregistration #2 from the frozen state.
5. If a meaning cue misses threshold, tighten the manual and rerun the pilot per the preregistered procedure.

## Known Repo State

Intentional tracked state:

1. `references.bib` is a symlink to the central house-style bibliography. Project-only additions belong in [references-local.bib](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/English_Passive_Voice_as_HPC/references-local.bib).
2. The canonical passing fake-data outputs are in [data/fake_data_gate](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/English_Passive_Voice_as_HPC/data/fake_data_gate).
3. The corrected `200`-simulation exploratory rerun is preserved in [data/fake_data_gate_surface_baseline](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/English_Passive_Voice_as_HPC/data/fake_data_gate_surface_baseline), and the old gold-like baseline outputs are preserved in [data/fake_data_gate_legacy_gold_baseline](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/English_Passive_Voice_as_HPC/data/fake_data_gate_legacy_gold_baseline).

Current intentional untracked paths:

1. [artifacts](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/English_Passive_Voice_as_HPC/artifacts)
2. [data/fake_data_gate_smoke3](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/English_Passive_Voice_as_HPC/data/fake_data_gate_smoke3)
3. [data/passive_candidates_zeldes.csv](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/English_Passive_Voice_as_HPC/data/passive_candidates_zeldes.csv)
