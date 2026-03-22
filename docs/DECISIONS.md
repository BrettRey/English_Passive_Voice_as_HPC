# Decisions

## 2026-03-19

### Framing

1. The paper will be aligned with the HPC book's maintenance view rather than with a generic fuzziness argument.
2. The target claim is that English passive voice is a maintained, projectible construction family or cluster.
3. The paper must distinguish:
   - the linguistic passive
   - the pedagogical or metalinguistic category `passive`
   - passive-heavy academic prose as a register effect rather than the category itself

### Evidence

1. Pullum 2014 is a core descriptive source for heterogeneity and folk/expert mismatch.
2. Pullum alone is not enough for the paper's main contribution; the real argumentative lift comes from the maintenance/projectibility framework.
3. No participant-based data collection will be used.
   This was later superseded by the addition of Study 2 external validation.
4. A quantitative section is allowed only if it uses existing corpora or datasets and remains compact.

### Empirical Direction

1. If quantitative evidence is added, it should test projectibility more than full homeostasis, since corpora can support transfer/generalization claims better than strong perturbation claims.
2. The empirical target should be narrower than Pullum's full descriptive inventory.
3. The cleanest likely design is a hybrid paper: theory-first, with one bounded corpus section.

## 2026-03-20

### Cue Restructuring: Form / Meaning Split

**Context.** The boundary pilot (16 items, 4 annotators: Brett, Opus-1, Opus-2 naive, base) exposed systematic disagreements clustering in the semantically loaded and mixed-level columns (`eventive_stative`, `promotion_type`, `subject_role_profile`, `peripheral_subtype`). Pairwise agreement ranged from 88--97% on 144 cells, with disagreements concentrated in items where coders were uncertain whether a column was asking about form or meaning.

**Root cause.** The original 7-cue scheme conflated linguistic levels. `peripheral_subtype` mixed morphosyntactic (`get`), syntactic (`reduced_embedded`, `prepositional`), and semantic (`stative_adjectival`) criteria in a single column. `agent_realization` mixed a form question (is there a *by*-PP?) with a semantic one (is it agentive?). `eventive_stative` was ostensibly semantic but coders reached for syntactic diagnostics to answer it. When form and meaning came apart (the boundary cases the study targets), coders had to resolve the conflict within a single cell, producing the observed disagreements.

**The middle-construction test.** "The butter spreads easily" shares meaning-level properties with passives (predicand as undergoer, agent suppression) and IS properties (patient as topic, topic continuity) but has zero passive morphosyntax. Under the old scheme, three of seven cues could not distinguish a middle from a passive. This showed that those cues were tracking voice alternations generally, not the passive specifically. The form cues (participle + auxiliary + *by*-phrase) are what define the passive cluster; the meaning and IS properties explain why the cluster is maintained.

**Decision.** Restructure the cue set into level-pure layers:

#### Form / construction cues (6 cues, observable)

1. `participial_form` = past_participle / gerund_participial / none
2. `licensing_marker` = be / passive_get / causative_get_have / subordinator_or_adjunct / modifier_position / absent_other
3. `constructional_environment` = clausal_predication / bare_infinitival_complement / to_infinitival_complement / gerund_participial_clause / adjunct_participial_clause / object_predicative_complement / reduced_modifier
4. `local_subject_present` = yes / no
5. `by_pp_present` = yes / no
6. `stranded_preposition` = yes / no

#### Meaning cues (3 cues, judgment-based, predicate-level)

7. `event_implied` = yes / no / unclear
8. `agent_implied` = yes / no / unclear
9. `predicand_as_undergoer` = yes / no / unclear

#### Derived (theory outputs)

10. `peripheral_subtype` — derived from cue pattern
11. `family_status` = core / peripheral / foil / exclude

#### Information structure cues (deferred to future layer)

Proposed but not included in Study 1 unless context windows are committed:

- `promoted_referent_activation` = active / accessible / new / unclear
- `by_phrase_information_status` = older / same / newer / absent / unclear
- `topic_continuity` = yes / no / unclear

Lambrecht would not approve coding these from isolated sentences.

### Old-to-New Column Mapping

| Old column | Disposition | New column(s) |
|---|---|---|
| `auxiliary_type` | replaced | `licensing_marker` |
| `participial_predicate` | replaced | `participial_form` (three-way) |
| `agent_realization` | decomposed | `by_pp_present` (form) + `agent_implied` (meaning) |
| `promotion_type` | decomposed | `stranded_preposition` (form) + `predicand_as_undergoer` (meaning) |
| `eventive_stative` | replaced | `event_implied` (predicate-level, not sentence-level) |
| `syntactic_environment` | replaced | `constructional_environment` (names constructions, not finite/non-finite) |
| `subject_role_profile` | replaced | `predicand_as_undergoer` |
| `peripheral_subtype` | kept as derived | emergent from cue pattern |

### Finite / Non-Finite Distinction Abandoned

The binary `finite-clause` / `nonfinite-or-reduced` is dropped. This is consistent with the SIEG second-edition revision. Replaced by `constructional_environment`, which names construction types (clausal predication, bare infinitival complement, to-infinitival complement, gerund-participial clause, adjunct participial clause, object predicative complement, reduced modifier) without invoking finite/non-finite as an analytical primitive.

CGEL (p. 51) classifies imperatives and subjunctives as finite despite using the plain form. The old binary could not handle this cleanly (BP007 "do not be put off" caused a 5-column cascade). The new scheme codes BP007 as bare_infinitival_complement (the *be*-clause is the complement of imperative *do*) without needing to decide whether the clause is finite.

### Pilot Adjudication: Specific Items

**BP001 "to be held":** Changed from core / none to peripheral / reduced_embedded. The *be*-clause is a to-infinitival complement of *want*, lacking a finite passive profile. Three independent coders incorrectly promoted this to core; the base annotation was right. Under the new scheme: constructional_environment = to_infinitival_complement, licensing_marker = be.

**BP007 "do not be put off":** Kept as peripheral. The *be*-clause is a bare infinitival complement of imperative *do*. The passive structure is complete (be + participle + *by*-phrase) but the constructional environment is non-matrix. Under the new scheme: constructional_environment = bare_infinitival_complement, licensing_marker = be.

**BP009 "get this done":** Causative *get* + NP + verbal participle. The *get* is causative, not a passive marker. *Done* is a verbal participle (not adjectival, despite the existence of adjectival *done* evidenced by *seems done*), but *do* does not entail *done*, so the active paraphrase is unstable. Under the new scheme: licensing_marker = causative_get_have, constructional_environment = object_predicative_complement.

**BP011 "exaggerated":** Flipped to foil. Coordination with the pure adjective *realistic* confirms lexicalized adjectival status. Three of four annotators coded foil.

### Comparison Constructions Added

The study should include items from constructions that share meaning and IS properties with passives but use different formal means. These test whether the form cues genuinely define the passive cluster boundary.

| Construction | Example | Form overlap | Meaning overlap | IS overlap |
|---|---|---|---|---|
| Middle | "the butter spreads easily" | low | high | high |
| Unaccusative / anticausative | "the door opened", "20 people died" | low | medium | high |
| Tough-construction | "this book is easy to read" | low | medium | high |
| Needs-washing | "the house needs painting" | low (gerund_participial, not past_participle) | high | high |
| Get + adjective | "he got drunk" | medium | low | medium |

These are not passive candidates. They are comparison items that let the model show the form cluster holds together even when the meaning/IS cues overlap with non-passives. The needs-washing construction is where `participial_form = gerund_participial` does real work: the construction IS participial, but the wrong participle for passive.

### HPC Architecture

The restructuring supports the paper's theoretical claim:

- **Form cues** define the property **cluster** (what makes something specifically passive).
- **Meaning cues** track the functional pressures that **maintain** the cluster (patient promotion, agent suppression, undergoer status). These are shared with middles, ergatives, tough-constructions, and needs-washing.
- **IS cues** (when available) track the discourse-level payoff that keeps the cluster in use (topic management, information packaging). Also shared across voice alternations.

The places where form and meaning come apart are the boundary cases. Instead of the coder resolving the dissociation into a single category, the model sees the raw pattern across levels.

### v2 Scheme Reliability Test

A naive Opus agent annotated the 16-item boundary pilot blind using only the v2 manual. Results:

- **Form cues**: 96/96 cells correct (100%). Zero disagreements.
- **Meaning cues**: ~47/48 cells (~98%). Two debatable cells on items without worked cases.
- **family_status**: 16/16 correct (100%).
- **peripheral_subtype**: 16/16 correct (100%) on items with worked cases.

Compared to v1 (88--97% pairwise agreement, 12--16 disagreements per pair), the restructuring eliminated all level-mixing disagreements. Residual variance is confined to genuine semantic judgment calls on meaning cues.

**Decision.** Use Opus v2 annotations as the pre-filled first pass for both boundary pilot and 100-row fit-gate pilot. Author reviews and corrects rather than coding blind. Two cells flagged for review: BP001 predicand_as_undergoer (no vs. yes), BP014 agent_implied (yes vs. unclear).

### Baseline Comparator Correction

The first v2 baseline rewrite made a substantive mistake. It defined the
deterministic checklist in terms of the annotated field `licensing_marker`
rather than overt surface material. That made the comparator too close to the
gold structural judgment. On the corrected v2 fit-gate pilot, the strict and
stronger baselines were perfect on the observed `core`/`foil` rows, and the
fake-data gate failed decisively.

This was treated as a design problem, not as a result to finesse. The fix was
to redefine the deterministic baselines over surface `be/get` material from the
retained extraction metadata (`aux_pass_lemmas`, `aux_lemmas`, `cop_lemmas`)
plus the minimal annotated convenience cues. That restores what the comparator
is supposed to be: a strong checklist that can still overgenerate on
passive-looking foils, not a recoding of the analyst's own functional label.

**Decision.** Be explicit about this in the prereg packet and appendix. The
change was made before preregistration, in response to the pilot fake-data
gate, and should be described as a correction to comparator design rather than
as a post hoc analytical win.

The corrected comparator then produced a near-threshold fake-data result rather
than a clean failure. At the minimum `200` simulations, the gate landed at
`strict_pass_rate = 0.745` and `stronger_pass_rate = 0.835`, missing the strict
criterion by one simulated pass. That was treated as Monte Carlo resolution
rather than as decisive evidence. The gate was rerun at `1000` simulations,
yielding `strict_pass_rate = 0.788` and `stronger_pass_rate = 0.844`, so the
v2 design clears the preregistered adequacy check under the corrected
surface-based baseline.

**Decision.** The packet should say explicitly that `200` simulations is the
minimum gate and that near-threshold cases are resolved by a higher-simulation
rerun rather than by ad hoc interpretation.

### Paper Appendix

An appendix will describe and explain the cue restructuring process: what the original scheme looked like, what the pilot exposed, the middle-construction test case, and how the form/meaning split was motivated. This provides a methodological contribution beyond the empirical results.

## 2026-03-22

### Reliability Timing

The v2 packet is now on `master` with the corrected surface-based baseline, the
passing `1000`-simulation fake-data gate, and the regenerated pilot materials.
The remaining preregistration blocker is the second blind pass and reliability
check.

**Decision.** Do not start the second blind pass early. Keep the prefilled
second-pass sheets frozen and wait until 2026-04-05 so the manual's `14`-day
lag is actually satisfied. Treat 2026-04-05 as a hard follow-up date for the
100-row fit-gate second pass, the 16-row boundary second pass, and immediate
reliability scoring.
