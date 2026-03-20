# Revised Plan 2026-03-19

Operational preregistration artifacts for this plan live in `docs/prereg/README.md`.

## Core Thesis

The paper should argue that English passive voice is best treated as a maintained, projectible construction family with a robust verbal-passive core and structured margins. The point is not merely that passive diagnostics are messy. The point is that a cue-bundle account supports better grammatical and discourse generalizations than a short classical checklist does.

## Anti-Thesis

The main hostile alternative is this:

English passive is either:

1. a crisp category adequately captured by a small checklist, or
2. a loose label covering several unrelated constructions, in which case HPC is just rebranding heterogeneity.

The plan has to beat both horns.

## What The Paper Must Predict

The plan should commit to these predictions before drafting:

1. A probabilistic cue-bundle account should generalize better across corpora than a short classical checklist account.
2. Canonical verbal passives should receive high passive-family probabilities, clear non-passive foils should receive low probabilities, and boundary cases should occupy the middle region more often than either extreme.
3. The same small cue bundle should remain informative across corpora rather than collapsing into corpus-specific heuristics.
4. The transferred passive-family probabilities should predict independent structural-licensing and discourse-fit judgments better than deterministic checklist rules do.

These are the projectibility claims. If the paper cannot state them clearly, it will drift back into mechanisms or clustering as the payoff.

## Scope Protocol

The paper needs an explicit core/periphery/exclusion scheme.

### Core Target

The core empirical target is the English verbal passive family, especially finite and non-finite `be` passives with promoted internal arguments and optional agent suppression or agent expression.

### Peripheral Probe Set

These are not excluded from discussion, but they are treated as boundary cases rather than as definitional anchors:

1. `get` passives
2. prepositional passives
3. reduced or embedded passives
4. stative/adjectival participial predicates that are plausibly passive-adjacent

### Explicit Exclusions

These should not carry the main empirical burden:

1. pedagogical or style-guide uses of `passive`
2. passive-heavy academic prose as a register effect
3. constructions that merely contain a past participle but lack a serious passive analysis

The paper can discuss excluded cases, but they should not be smuggled into the evidence base.

## Theory Decision

The paper should be theory-plus-two-linked-tests, not theory-only and not a methods paper.

That means:

1. one bounded confirmatory corpus-transfer study
2. one bounded external-validation judgment study
3. no large-scale LLM annotation pipeline in the main paper
4. no custom mixed-membership model as the paper's main empirical contribution

If a richer latent-structure model is still interesting later, it can be parked as appendix or follow-on work.

## Confirmatory Corpus Design

### Corpora

Use two parsed English corpora that are already local and available in the workspace:

1. UD English EWT
2. UD English GUM

These give a real cross-corpus transfer test rather than a within-corpus register comparison only.

UD passive-specific labels such as `Voice=Pass`, `nsubj:pass`, `aux:pass`, and `obl:agent` may be used for candidate extraction, but they should not do the main argumentative work in the confirmatory model.

### Sampling Plan

Increase the initial target to 400 hand-coded tokens total.

Use two layers:

1. a stratified analytic sample of 320 tokens
2. a naturally distributed held-out slice of 80 tokens

The stratified analytic sample should contain:

1. 120 core verbal passives
2. 80 peripheral passive-adjacent cases
3. 120 non-passive foils

Balance these as closely as possible across EWT and GUM.

The naturally distributed held-out slice should be drawn from the same candidate-extraction streams but left at corpus prevalence rather than engineered class balance. Keep this slice untouched until final evaluation.

The reason for the two-layer design is simple:

1. the stratified sample makes boundary probing feasible
2. the naturalistic slice keeps the transfer claim from depending entirely on prevalence engineering

The peripheral set should include, where available:

1. `get` passives
2. prepositional passives
3. reduced or embedded passives
4. stative/adjectival participles that look passive-like on the surface

The foil set should include near misses that a loose descriptive account could confuse with passives:

1. copular adjectival participles
2. resultatives
3. active perfects
4. other participial predicates without a serious passive analysis

Before full annotation begins, run a quick fake-data or simulation check to see whether this sample size yields informative uncertainty for the planned cross-corpus comparison. If uncertainty is too wide, either:

1. increase the total sample
2. reduce cue complexity
3. simplify the confirmatory claim

### Frozen Cue Inventory

Keep the confirmatory feature set small enough to hand-code reliably across both corpora.

Proposed seven cues:

1. auxiliary type: `be` / `get` / none-other
2. participial predicate: yes / no
3. overt agent realization: `by` phrase / other overt agentive phrase / none
4. promotion type: direct-object promotion / oblique-stranding promotion / none-unclear
5. eventive vs stative reading: eventive / stative / ambiguous
6. syntactic environment: finite clause / non-finite or reduced clause
7. subject role profile: patient-theme like / locative-oblique like / unclear-other

This inventory is intentionally smaller than the earlier 12-feature proposal. It is meant to test projectibility without turning the paper into an annotation study.

### Subtype Inheritance Sketch

The plan should make the family structure explicit rather than leaving `construction family` as a slogan.

1. Canonical `be` passives anchor the core profile.
2. `get` passives inherit participial predication, promoted non-agentive subjecthood, and demoted external argument, but override auxiliary type and often sharpen eventive/affected readings.
3. Prepositional passives inherit participial predication and demoted external argument, but override the promotion cue by allowing oblique-stranding promotion.
4. Reduced or embedded passives inherit passive predication but override the finite-clause cue.
5. Stative/adjectival participles overlap in surface form but often fail on eventivity and promotion; they function as the nearest lower-boundary cases, not automatic family members.

This sketch should become a compact subtype-by-diagnostic table before drafting prose.

### Annotation Protocol

The feature set is not genuinely frozen until it has a coding manual.

Before confirmatory fitting:

1. write a short annotation manual with hard decision rules and tie-breakers for all seven cues
2. hide corpus identity and provisional class labels from the coder where possible during coding
3. in the operational prereg packet, use a 100-row fit-gate pilot plus a 16-row boundary mini-pilot instead of the earlier 50-token sketch
4. if a second blind human coder becomes available, use that as a stronger reliability check, but do not make the paper depend on it
5. set a minimum reliability target of kappa at or above 0.80 for each cue used in the confirmatory model

If `eventive vs stative`, `promotion type`, or `subject role profile` fail the reliability threshold, either tighten the rules or drop the cue from the confirmatory model.

## Statistical Comparison

### Primary Confirmatory Test

Compare two models:

1. explicit checklist baselines
2. a Bayesian cue-bundle model

The key outcome is cross-corpus generalization.

Train on EWT and test on GUM, then reverse the direction.

Do not train on peripheral cases in the main confirmatory fit. The confirmatory training data should be:

1. core passives
2. non-passive foils

Peripheral cases should be held out from training and used as a genuine probe of graded extension. This makes intermediate posterior probabilities on boundary cases informative rather than partly taught.

### Explicit Baselines

The baseline must be frozen now.

Use two deterministic rule-based comparators.

1. **Strict checklist baseline**
   A token counts as passive if and only if it has:
   `a.` auxiliary `be` or `get`
   `b.` participial predicate
   `c.` promoted non-agentive subject

2. **Stronger rule-based comparator**
   The same conjunction as above, plus exclusion of clearly stative/adjectival readings when the coding manual classifies the token as non-eventive.

These are intentionally strong rivals, not straw men.

### Bayesian Cue-Bundle Model

The main confirmatory model should be a Bayesian logistic regression, not a more elaborate latent-mixture model.

For token `j`:

`logit(P(passive_family_j = 1)) = beta_0 + sum_i beta_i x_ji`

where the `x_ji` values encode the frozen cue inventory using standard treatment coding for categorical predictors.

Use weakly regularizing priors:

1. `beta_0 ~ Normal(0, 2.5)`
2. `beta_k ~ Normal(0, 2.5)` for all slope terms

Fit the model separately in each transfer direction:

1. train on EWT core plus foils, test on GUM core plus foils
2. train on GUM core plus foils, test on EWT core plus foils

Then, in each direction, apply the trained model without refitting to:

1. the held-out peripheral cases
2. the naturalistic held-out slice

This keeps the primary question simple: does a probabilistic cue bundle travel better than a checklist, and what does it do at the margins?

### Primary Metric

Use Brier score as the primary confirmatory metric because it rewards calibrated probabilistic prediction and makes deterministic checklists comparable to the Bayesian model.

Secondary summaries can include:

1. accuracy on core versus foil discrimination
2. calibration plots
3. classwise error patterns
4. distribution of posterior probabilities on peripheral items

### Why This Better Matches The Paper

This design tests projectibility directly:

1. Can the cue bundle travel?
2. Does it outperform a classical definition?
3. Do boundary cases receive intermediate probabilities rather than forced all-or-none decisions?

That is closer to the paper's theoretical payoff than a full latent-mixture model is.

## External Validation Study

The corpus section should no longer carry the entire projectibility argument by itself.

Add a second, independent validation study with human judgments.

### Purpose

`Study 2` should test whether the transferred passive-family probabilities from `Study 1` predict linguistic behavior that is not used in the corpus labels:

1. structural licensing behavior associated with verbal passives
2. discourse-fit behavior associated with passive information packaging

This is the cleanest way to answer the circularity objection and to make the HPC payoff purpose-indexed rather than merely classificatory.

### Scope

Build a stimulus bank of `108` items:

1. 18 `core`
2. 18 `foil`
3. 18 `get`
4. 18 `prepositional`
5. 18 `reduced_embedded`
6. 18 `stative_adjectival`

Balance across EWT and GUM as closely as possible.

### Task A: Structural Licensing

Participants should judge whether a target sentence supports a verbal-passive-style continuation:

1. canonical `by` phrase where semantically coherent
2. agentive adverb continuation where a `by` phrase would be awkward

This gives an external target for the structural side of the passive family.

### Task B: Discourse Fit

Participants should judge the same target sentence after:

1. a patient-given context
2. an agent-given context

The discourse prediction is not that every boundary subtype behaves like the core. The prediction is that the transferred passive-family probabilities should track where patient-given packaging remains a good fit.

### Size

This should be a real companion study, not a token validation check.

Recommended size:

1. `Study 2A`: two lists of 54 items, 72 participants total
2. `Study 2B`: four lists of 54 items, 96 participants total

That is large enough to estimate subtype patterns without turning the paper into a participant-heavy methods project.

## What To Report

### Confirmatory

1. out-of-corpus Brier score for checklist versus cue-bundle model
2. posterior passive-family probabilities for core cases, foils, and peripheral cases
3. whether the peripheral set sits between the core and foil distributions rather than collapsing into one side
4. results on the naturally distributed held-out slice
5. external-validation results on structural licensing judgments
6. external-validation results on discourse-fit judgments

### Exploratory

If useful, report which cues remain most informative across corpora, but keep this subordinate to the transfer result.

## Falsifiers

The paper should state these explicitly.

1. If the cue-bundle model does not outperform both rule-based baselines on Brier score in cross-corpus transfer, the projectibility claim is weakened.
2. If the cue-bundle advantage disappears on the naturally distributed held-out slice, the projectibility claim is weakened.
3. If peripheral cases do not occupy an intermediate probability region, the graded-family claim is weakened.
4. If the informative cues are unstable across corpora, the maintenance/projectibility story is weakened.
5. If the evidence supports only a crisp core plus excluded non-members, the paper should say that honestly instead of forcing an HPC reading on every passive-adjacent construction.
6. If transferred passive-family probabilities do not predict external structural-licensing or discourse-fit behavior better than checklist rules, the paper should narrow its claim to corpus projectibility only.

## Success Criteria

The confirmatory section should pre-register what counts as support for projectibility.

Full projectibility support now requires both studies to succeed.

`Study 1` support requires all of the following:

1. the Bayesian cue-bundle model beats the strict checklist baseline on Brier score in both transfer directions
2. the Bayesian cue-bundle model also beats the stronger rule-based comparator in at least one transfer direction and does not lose clearly in the other
3. the cue-bundle advantage remains visible on the naturalistic held-out slice
4. at least 60% of peripheral tokens fall in the middle-probability region `[0.2, 0.8]`
5. at least 80% of core tokens fall above `0.8` and at least 80% of foil tokens fall below `0.2`

`Study 2` support requires:

1. transferred passive-family probabilities positively predict structural-licensing judgments
2. transferred passive-family probabilities positively predict patient-given discourse fit
3. those transferred probabilities outperform checklist rules on both external targets

These thresholds should be made explicit in the preregistration so the paper cannot move the goalposts after seeing the data.

## Linguistic Payoff Beyond Model Fit

The paper still needs to say what the combined two-study design buys linguistically, not just statistically.

The introduction and conclusion should commit to at least three non-model inferences:

1. passive-family membership should support better judgments about which borderline constructions are reasonable extensions of the passive family
2. passive-family membership should support better discourse predictions about where patient-given packaging remains acceptable
3. passive-family membership should support the claim that apparent boundary mess is structured enough to travel across corpora and into independent judgments rather than collapsing into corpus-specific definitions

Mechanisms matter only insofar as they explain why these inductive warrants hold. They are not the payoff of the paper.

## Drafting Consequences

The outline should change accordingly.

1. Introduction
   State the anti-thesis, the stronger thesis, and the three predictions.
2. Pullum and the descriptive problem
   Use Pullum to establish heterogeneity and folk misclassification.
3. Scope protocol
   Define core, periphery, and exclusions before importing HPC.
4. HPC framework
   Make projectibility the payoff, not a decorative add-on.
5. English passive as a cue-bundle construction family
   Present the frozen cue inventory and the logic of the family resemblance claim.
6. Study 1: bounded corpus transfer test
   Compare checklist versus cue-bundle transfer across EWT and GUM.
7. Study 2: external validation
   Test structural licensing and discourse-fit payoffs against independent judgments.
8. Discussion
   Separate linguistic passive from pedagogical `passive` and passive-heavy prose.
9. Conclusion
   State what the passive category lets us predict, and what the study does not show.

## Not For This Version

These are good ideas, but they should be kept out of the main paper unless the simple design works cleanly first:

1. large-scale LLM annotation
2. measurement-error models for LLM coders
3. mixed-membership or grade-of-membership latent models
4. a twelve-feature annotation scheme
5. an argument that every passive-adjacent construction is genuinely inside the same family
