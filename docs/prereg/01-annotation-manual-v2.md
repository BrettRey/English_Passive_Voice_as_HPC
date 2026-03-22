# Annotation Manual (v2)

## Purpose

This manual freezes the coding decisions for the confirmatory passive study. The cue set is organized into three levels: form (observable morphosyntactic properties), meaning (semantic judgments about the predicate), and derived theory outputs. The form/meaning split ensures that boundary cases where form and meaning come apart are recorded as dissociations rather than forced into a single category.

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

### Form / Construction Cues

1. `participial_form`
2. `licensing_marker`
3. `constructional_environment`
4. `local_subject_present`
5. `by_pp_present`
6. `stranded_preposition`

### Meaning Cues

7. `event_implied`
8. `agent_implied`
9. `predicand_as_undergoer`

### Derived

10. `peripheral_subtype`
11. `family_status`
12. `notes`

## Coding Order

Code each row in this order:

1. verify the predicate token and sentence context
2. decide whether the row is `exclude`
3. code the six form cues
4. code the three meaning cues
5. derive `peripheral_subtype` from the cue pattern
6. assign `family_status` from the decision table below

Do not assign `family_status` first and backfill cues to match it.

## Form Cue Definitions

### 1. Participial Form

Values:

1. `past_participle`
2. `gerund_participial`
3. `none`

Use `past_participle` when the head is a past-participial form (e.g., *stolen*, *held*, *put*).

Use `gerund_participial` when the head is a gerund-participial form (e.g., *painting* in "the house needs painting").

Use `none` when the head is not a participial form. This applies to comparison items (middles, ergatives, tough-constructions) and to parser errors.

### 2. Licensing Marker

Values:

1. `be`
2. `passive_get`
3. `causative_get_have`
4. `subordinator_or_adjunct`
5. `modifier_position`
6. `absent_other`

This field records what licenses the participial predicate in its position. It is not a theoretical claim about auxiliary status.

Use `be` when a form of *be* directly licenses the participial predicate.

Use `passive_get` when a form of *get* directly licenses the participial predicate and the subject of *get* is the undergoer (e.g., "I got pulled to ultrasound"). The subject of *get* is the patient, not the causer.

Use `causative_get_have` when a form of *get*, *have*, or *need* licenses the participial predicate in a causative or resultative construction, where the subject of the licensing verb is the causer or possessor, not the patient (e.g., "let's get this done", "have the test done").

Use `subordinator_or_adjunct` when the participial predicate is licensed by a subordinator such as *as* or by its position in a clausal adjunct (e.g., "as shown in figure 2", "frightened by the noise, the cat ran").

Use `modifier_position` when the participial predicate is licensed by its position as a prenominal or postnominal modifier (e.g., "screened workers", "the channel pointed out by Mr. Rohatgi").

Use `absent_other` when no licensing marker is identifiable or the construction falls outside the categories above.

Tie-breaker:

If both `be` and `get` appear, code the marker that directly licenses the participial predicate under analysis.

### 3. Constructional Environment

Values:

1. `clausal_predication`
2. `bare_infinitival_complement`
3. `to_infinitival_complement`
4. `gerund_participial_clause`
5. `adjunct_participial_clause`
6. `object_predicative_complement`
7. `reduced_modifier`

This field names the construction in which the participial predicate appears. It does not invoke a finite/non-finite binary.

Use `clausal_predication` when the participial predicate is the main predication of its own clause, whether that clause is a matrix clause or a subordinate clause with its own subject and predicate structure (e.g., "the car was stolen", "the car that was stolen").

Use `bare_infinitival_complement` when the participial predicate is inside a bare infinitival complement of another verb (e.g., "do not be put off" where *be put off* is the bare infinitival complement of imperative *do*; "do you get charged" where *get charged* is the bare infinitival complement of interrogative *do*).

Use `to_infinitival_complement` when the participial predicate is inside a to-infinitival complement (e.g., "they want to be held").

Use `gerund_participial_clause` when the participial predicate is inside a gerund-participial clause (e.g., "in being arranged so that...").

Use `adjunct_participial_clause` when the participial predicate heads a clausal adjunct, including *as*-clauses (e.g., "as shown in figure 2", "frightened by the noise, the cat ran").

Use `object_predicative_complement` when the participial predicate functions as a predicative complement of an object in a causative or resultative construction (e.g., "have the test done", "get this done", "we needed it rushed").

Use `reduced_modifier` when the participial predicate functions as a prenominal or postnominal modifier without its own clausal structure (e.g., "screened workers", "named avenues").

### 4. Local Subject Present

Values:

1. `yes`
2. `no`

Use `yes` when the participial predicate has an overt subject or subject-like element in its local clause.

Use `no` when there is no overt local subject. This includes reduced modifiers, adjunct participial clauses without an overt subject, and imperatives where the subject is implicit.

### 5. By-PP Present

Values:

1. `yes`
2. `no`

Use `yes` when there is an overt *by*-PP in the local clause of the participial predicate, regardless of whether it is agentive. The semantic judgment (is it agentive?) belongs in `agent_implied`.

Use `no` when there is no *by*-PP.

### 6. Stranded Preposition

Values:

1. `yes`
2. `no`

Use `yes` when there is a retained or stranded preposition whose complement corresponds to the predicand (e.g., "this bed was slept in").

Use `no` otherwise.

## Meaning Cue Definitions

The three meaning cues target the **predicate's semantic contribution**, not the sentence-level meaning. Composition with the auxiliary, tense, subject, and discourse context may yield a different sentence-level interpretation. Code the predicate.

### 7. Event Implied

Values:

1. `yes`
2. `no`
3. `unclear`

Use `yes` when the predicate, in this token, implies that an event or process occurred or is occurring. The predicate contributes event semantics.

Use `no` when the predicate describes a state, disposition, or lexicalized property with no event implication. The predicate contributes state or property semantics.

Use `unclear` when the predicate is genuinely ambiguous between event and state readings after inspecting the local context. Do not use `unclear` as a default; use it only when both readings remain available.

### 8. Agent Implied

Values:

1. `yes`
2. `no`
3. `unclear`

Use `yes` when an agent or causer is understood as part of the predicate's meaning, whether or not the agent is overtly expressed. A short passive like "the car was stolen" implies an agent even without a *by*-phrase.

Use `no` when no agent or causer is part of the understood meaning. This includes lexicalized adjectives ("an exaggerated setup"), pure states ("the door is open"), and ergative/anticausative constructions where the event happens without an external cause ("the glass broke").

Use `unclear` when the agent implication is genuinely indeterminate.

This cue is independent of `by_pp_present`. A *by*-phrase may be present without being agentive (instrumental *by*), and an agent may be implied without any *by*-phrase.

### 9. Predicand As Undergoer

Values:

1. `yes`
2. `no`
3. `unclear`

The predicand is the element the participial predicate is predicated of. This may be a surface subject, the head noun of a reduced modifier, or the object in a causative construction. It is not always a syntactic subject.

Use `yes` when the predicand is understood as the affected participant, theme, or undergoer of the predicate.

Use `no` when the predicand is not an undergoer. This includes cases where the predicand is an agent, a location, or an entity characterized by a property without being affected.

Use `unclear` when the role cannot be characterized confidently.

Note: this cue is not passive-specific. Middles ("the butter spreads easily"), ergatives ("the door opened"), and tough-constructions ("this book is easy to read") can all have predicands as undergoers. The form cues distinguish these from passives.

## Peripheral Subtype

Derived from the cue pattern after coding. Use one of:

1. `none`
2. `get`
3. `prepositional`
4. `reduced_or_embedded`
5. `stative_adjectival`
6. `comparison_construction`
7. `other`

Use `get` when `licensing_marker = passive_get`.

Use `prepositional` when `stranded_preposition = yes`.

Use `reduced_or_embedded` when the passive-family reading survives but `constructional_environment` is not `clausal_predication` (i.e., the participial predicate is in a complement, adjunct, or modifier environment).

Use `stative_adjectival` when `event_implied = no` and the row is still plausibly adjacent to a passive alternation.

Use `comparison_construction` for items from middles, ergatives, tough-constructions, needs-washing, and other non-passive comparison items.

Use `none` when none of the above apply.

Use `other` rarely.

## Family Status

Use one of four values:

1. `core`
2. `peripheral`
3. `foil`
4. `exclude`

### Decision Table

Assign `exclude` if the row cannot be coded responsibly because of parser corruption, missing context, duplicate identity, or severe sentence degradation.

Assign `core` when all are true:

1. `participial_form = past_participle`
2. `licensing_marker = be`
3. `constructional_environment = clausal_predication`
4. `predicand_as_undergoer = yes`
5. `peripheral_subtype = none`

A row can remain `core` even when `event_implied = unclear` or `agent_implied = unclear` if the form profile is unambiguously passive.

Assign `peripheral` when all are true:

1. the row is not `exclude`
2. `participial_form = past_participle`
3. the row preserves a serious passive-family analysis (multiple form and meaning cues are present in their passive-typical values)
4. `peripheral_subtype != none`

Assign `foil` to the remaining analyzable rows, including: active perfects, clearly lexicalized adjectival participles, resultatives, comparison-construction items, and other participial predicates without a stable passive-family analysis.

## Worked Cases

| Example | participial_form | licensing_marker | constructional_env | local_subj | by_pp | stranded_prep | event | agent | undergoer | peripheral_subtype | family_status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `The car was stolen by teenagers.` | past_participle | be | clausal_predication | yes | yes | no | yes | yes | yes | none | core |
| `He got fired after the argument.` | past_participle | passive_get | clausal_predication | yes | no | no | yes | yes | yes | get | peripheral |
| `This bed was slept in.` | past_participle | be | clausal_predication | yes | no | yes | yes | yes | yes | prepositional | peripheral |
| `The report submitted yesterday...` | past_participle | modifier_position | reduced_modifier | no | no | no | yes | yes | yes | reduced_or_embedded | peripheral |
| `The door is closed.` | past_participle | be | clausal_predication | yes | no | no | unclear | no | unclear | stative_adjectival | peripheral |
| `She has finished the report.` | past_participle | absent_other | clausal_predication | yes | no | no | yes | no | no | none | foil |
| `They want to be held.` | past_participle | be | to_infinitival_complement | no | no | no | yes | yes | yes | reduced_or_embedded | peripheral |
| `Do not be put off by...` | past_participle | be | bare_infinitival_complement | no | yes | no | yes | yes | yes | reduced_or_embedded | peripheral |
| `Have the test done.` | past_participle | causative_get_have | object_predicative_complement | no | no | no | yes | unclear | yes | reduced_or_embedded | peripheral |
| `As shown in figure 2.` | past_participle | subordinator_or_adjunct | adjunct_participial_clause | no | no | no | unclear | unclear | unclear | reduced_or_embedded | peripheral |
| `Screened workers` | past_participle | modifier_position | reduced_modifier | no | no | no | yes | yes | yes | reduced_or_embedded | peripheral |
| `Named avenues` | past_participle | modifier_position | reduced_modifier | no | no | no | no | no | yes | stative_adjectival | peripheral |
| `A realistic but exaggerated setup` | past_participle | modifier_position | reduced_modifier | no | no | no | no | no | no | none | foil |
| `The butter spreads easily.` | none | absent_other | clausal_predication | yes | no | no | no | no | yes | comparison_construction | foil |
| `The door opened.` | none | absent_other | clausal_predication | yes | no | no | yes | no | yes | comparison_construction | foil |
| `Twenty people died.` | none | absent_other | clausal_predication | yes | no | no | yes | no | yes | comparison_construction | foil |
| `This book is easy to read.` | none | absent_other | clausal_predication | yes | no | no | unclear | unclear | yes | comparison_construction | foil |
| `The house needs painting.` | gerund_participial | absent_other | clausal_predication | yes | no | no | yes | yes | yes | comparison_construction | foil |

## Hard-Case Defaults

Use these defaults to avoid silent drift:

1. if a `passive_get` row lacks a stable promoted non-agentive predicand, recode `licensing_marker = absent_other` and prefer `foil`
2. if a stranded preposition is present with a promoted complement, code `stranded_preposition = yes`
3. if the predicate is in a complement, adjunct, or modifier environment but the passive-family reading survives, use `reduced_or_embedded`
4. if `event_implied = no` but a passive alternation remains plausible, prefer `stative_adjectival`
5. if the row is merely participial with no serious passive-family analysis, prefer `foil`
6. if event implication is genuinely open after predicate-level inspection, use `unclear`
7. if form cues are fully passive-typical but a meaning cue is `unclear`, keep the row `core`; meaning cues are not definitional gates
8. code meaning cues for the **predicate**, not the sentence; do not let compositional sentence-level cues override the predicate-level judgment

## Comparison Items

The item set includes tokens from non-passive constructions that share meaning and IS properties with passives but use different formal means. These are coded on all cues and receive `family_status = foil` and `peripheral_subtype = comparison_construction`.

Comparison constructions:

1. **Middle**: "the butter spreads easily" (patient as subject, agent suppressed, dispositional)
2. **Unaccusative / anticausative**: "the door opened", "20 people died" (undergoer subject, no passive morphology; often misdescribed in public discussion as passive voice)
3. **Tough-construction**: "this book is easy to read" (patient promoted to matrix subject, agent generic)
4. **Needs-washing**: "the house needs painting" (patient as subject, gerund-participial complement, agent implied)
5. **Get + adjective**: "he got drunk" (get + predicate frame, no passive semantics)

These test whether the form cues define the passive cluster boundary. The model should show that the form cluster holds together even when the meaning cues partially overlap with non-passives.

## Reliability Procedure

Before confirmatory fitting:

1. annotate a fit-gate pilot batch of 100 rows:
   25 `core` and 25 `foil` candidates from EWT, plus 25 `core` and 25 `foil` candidates from GUM
2. annotate a separate 16-row boundary mini-pilot: 8 passive-boundary rows (1 `get`, 1 `reduced_or_embedded`, and 2 manual-probe rows per corpus) plus 8 fixed comparison-construction items
3. keep the coder-facing sheets blind to `candidate_id`; use the generated `pilot_item_id` instead
4. wait at least 14 days
5. re-annotate both pilots blind to the first pass
6. compute kappa for each form cue and meaning cue, and for `family_status`
7. compute `peripheral_subtype` kappa on the boundary mini-pilot

Targets:

1. `kappa >= 0.80` for each form cue
2. `kappa >= 0.70` for each meaning cue (semantic judgments are expected to be harder)
3. `kappa >= 0.80` for `family_status`
4. `kappa >= 0.70` for `peripheral_subtype`

If a meaning cue fails the reliability threshold:

1. tighten the manual
2. re-run the pilot
3. if it still fails, keep the cue descriptive only and drop it from the confirmatory model

If `family_status` fails while the individual cues are stable, revise the decision table before full annotation and log the change explicitly.

## Information Structure Layer (Deferred)

The following cues are proposed for a future layer, contingent on providing sufficient discourse context with each item:

1. `promoted_referent_activation` = active / accessible / new / unclear
2. `by_phrase_information_status` = older / same / newer / absent / unclear
3. `topic_continuity` = yes / no / unclear

These are not part of the Study 1 confirmatory annotation. They require context windows that isolated sentences cannot provide.
