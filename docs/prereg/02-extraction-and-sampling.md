# Extraction And Sampling Protocol

## Corpus Paths

Use the local UD English treebanks at:

1. `/Users/brettreynolds/Documents/LLM-CLI-projects/corpora/ud-english/ewt`
2. `/Users/brettreynolds/Documents/LLM-CLI-projects/corpora/ud-english/gum`

Use all three splits in each treebank:

1. `train`
2. `dev`
3. `test`

For this project, the original UD split labels are storage partitions, not analytic train/test partitions. The confirmatory transfer distinction is corpus identity, not treebank split.

## Extraction Unit

The extraction unit is one predicate head token.

Each candidate row is uniquely identified by:

1. `candidate_id`
2. `corpus`
3. `split`
4. `sent_id`
5. `head_id`

## Candidate Ledger

Build the ledger with:

```bash
python scripts/extract_ud_passive_candidates.py \
  --ewt-root /Users/brettreynolds/Documents/LLM-CLI-projects/corpora/ud-english/ewt \
  --gum-root /Users/brettreynolds/Documents/LLM-CLI-projects/corpora/ud-english/gum \
  --output data/passive_candidate_ledger.csv
```

The extractor writes one row per candidate with:

1. token identifiers and source file
2. marked sentence text
3. parent and child dependency snapshot
4. passive-relevant UD cues
5. one or more provisional stream tags

Rows with no usable provisional stream tags are not written.

## Broad Inclusion Signature

A token enters the candidate ledger if any of the following is true:

1. its features include `Voice=Pass`
2. it is participial and has `aux:pass` or `nsubj:pass`
3. it is participial with a `be` or `get` copular configuration
4. it is participial with perfect `have`
5. it is participial in `acl`, `acl:relcl`, or `amod`

This is intentionally broader than the analysis set. The ledger is a reproducible candidate pool, not the final study sample.

## Provisional Extraction Streams

Each ledger row may carry more than one stream tag.

### Core Stream

Assign `core_be` when all are true:

1. `Voice=Pass` is present on the head
2. at least one dependent is `nsubj:pass`
3. at least one `aux:pass` dependent has lemma `be`

### Peripheral Streams

Assign `peripheral_get` when all are true:

1. `Voice=Pass` is present
2. at least one dependent is `nsubj:pass`
3. at least one `aux:pass` dependent has lemma `get`

Assign `peripheral_reduced_embedded` when all are true:

1. `Voice=Pass` is present
2. the head is in `acl`, `acl:relcl`, or `amod`
3. there is no finite `be` or `get` passive auxiliary directly licensing the clause

Assign `peripheral_manual_probe` when the row is passive-like but does not already belong to `core_be`, `peripheral_get`, or `peripheral_reduced_embedded`.

This stream is the search space for manually identified prepositional passives and stative/adjectival passive-adjacent cases.

### Foil Streams

Assign `foil_perfect` when all are true:

1. the head is participial
2. an `aux` dependent has lemma `have`
3. the head lacks `Voice=Pass`
4. the head lacks `aux:pass`

Assign `foil_copular_participle` when all are true:

1. the head is participial
2. it has a `cop` dependent with lemma `be` or `get`
3. the head lacks `Voice=Pass`
4. it lacks `aux:pass`

Assign `foil_participial_modifier` when all are true:

1. the head is participial
2. the head is in `acl`, `acl:relcl`, or `amod`
3. the head lacks `Voice=Pass`
4. it lacks `aux:pass`

## Deduplication And Pre-Sampling Exclusions

Deduplicate on `candidate_id`.

Before sampling, drop rows only if any of the following holds:

1. duplicate `candidate_id`
2. empty `provisional_streams`
3. missing `sent_id`
4. malformed or empty sentence text
5. obvious metadata artifact rather than sentence content

Do not exclude difficult linguistic cases at this stage.

Before annotation begins, run a manual-probe richness check:

```bash
python scripts/check_manual_probe_pool.py \
  --input data/passive_candidate_ledger.csv
```

This report is a sanity gate, not an automatic subtype classifier. Use it to confirm that the `peripheral_manual_probe` pool is large and structurally varied enough to make the preregistered prepositional and stative/adjectival minima plausible before annotation effort is committed. In particular, inspect the bare-participial no-auxpass counts alongside the `obl` and `nsubj:pass` heuristics before locking the annotation schedule.

## Randomization Policy

Use one global seed:

1. `20260319`

Sampling is deterministic once the ledger is fixed.

## Sampling Script

Build the annotation packs with:

```bash
python scripts/sample_from_ledger.py \
  --input data/passive_candidate_ledger.csv \
  --output-dir data/prereg_sampling
```

The script must fail loudly if any preregistered queue cannot meet its target before annotation.

Outputs:

1. `data/prereg_sampling/primary_annotation_pack.csv`
2. `data/prereg_sampling/replacement_queue.csv`

Each row keeps the ledger fields and adds:

1. `sample_set`
2. `sample_rank`
3. `sampling_stream`

The written file order is deliberately reshuffled after sampling. `sample_rank`, not spreadsheet row order, governs later replacement and finalization.

## Naturalistic Held-Out Slice

The sampler draws this slice first.

Per corpus target:

1. 40 rows from EWT
2. 40 rows from GUM

Procedure:

1. shuffle the deduplicated ledger within corpus using the fixed seed
2. draw 40 rows per corpus without class balancing
3. label them `sample_set = heldout`
4. remove them from later analytic sampling

The held-out target remains fixed at 40 rows per corpus after annotation. If exclusions reduce the usable held-out slice below 40 for either corpus, the finalizer must fail and the shortfall must be logged as a prereg deviation rather than silently changing the held-out size.

This slice reflects prevalence within the passive-adjacent candidate space, not within all English clauses.

## Stratified Analytic Candidate Packs

After held-out removal, the sampler draws analytic candidate packs.

Before any analytic draw, each remaining row is assigned to exactly one exclusive `sampling_stream` by this precedence order:

1. `core_be`
2. `peripheral_get`
3. `peripheral_reduced_embedded`
4. `peripheral_manual_probe`
5. `foil_copular_participle`
6. `foil_participial_modifier`
7. `foil_perfect`

This precedence prevents a single row from entering more than one analytic queue.

Per corpus targets in the primary pack:

1. 60 rows from `core_be`
2. 40 rows from the combined peripheral queues
3. 60 rows from the combined foil queues

The primary analytic `sample_set` labels are:

1. `analytic_core_candidate`
2. `analytic_peripheral_candidate`
3. `analytic_foil_candidate`

The replacement queue preserves the same within-stream order with:

1. `analytic_core_replacement`
2. `analytic_peripheral_replacement`
3. `analytic_foil_replacement`

The peripheral primary queue is not built by raw concatenation. It uses this fixed weighted cycle over the exclusive peripheral subqueues:

1. `peripheral_manual_probe`
2. `peripheral_get`
3. `peripheral_manual_probe`
4. `peripheral_reduced_embedded`
5. `peripheral_manual_probe`

If enough rows are available, this yields 24 manual-probe rows, 8 `get` rows, and 8 reduced/embedded rows per corpus in the 40-row primary peripheral pack. This front-loads the only available pre-annotation source for prepositional and stative/adjectival cases while preserving a replacement reserve of scarce `get` rows.

The peripheral replacement queue then continues from the leftover exclusive subqueues with this fixed cycle:

1. `peripheral_get`
2. `peripheral_manual_probe`
3. `peripheral_reduced_embedded`
4. `peripheral_manual_probe`

This keeps all peripheral source types reachable early during replacement rather than burying manual-probe rows behind a long reduced/embedded tail.

The foil primary queue is also diversity-weighted. It uses this fixed cycle over the exclusive foil subqueues:

1. `foil_perfect`
2. `foil_participial_modifier`
3. `foil_perfect`
4. `foil_participial_modifier`
5. `foil_copular_participle`
6. `foil_perfect`

The foil replacement queue continues from the leftovers with this fixed cycle:

1. `foil_copular_participle`
2. `foil_participial_modifier`
3. `foil_perfect`
4. `foil_participial_modifier`
5. `foil_perfect`

Known constraint:

`foil_copular_participle` is expected to be the smallest foil source, partly because some treebank rows that are foil-like on linguistic inspection still carry `Voice=Pass` and therefore do not enter that stream. The foil cycles degrade gracefully if the copular queue is exhausted, but any resulting underrepresentation of copular participles should be reported explicitly rather than discovered post hoc.

## Annotation And Replacement Workflow

1. annotate the full primary pack first
2. mark unusable rows as `exclude`, not by deleting them
3. if any analytic class or peripheral subtype minimum is not met after primary annotation, continue annotation down the same-corpus replacement queue in `sample_rank` order
4. do not borrow rows across corpora automatically

If the replacement queue is exhausted before a class target or peripheral subtype minimum is met, stop and record a prereg deviation instead of improvising a new draw.

## Finalization Script

Freeze the final sample with:

```bash
python scripts/finalize_annotated_sample.py \
  --primary annotations/primary_annotation_pack_annotated.csv \
  --replacement annotations/replacement_queue_annotated.csv \
  --output data/final_preregistered_sample.csv
```

The finalizer must fail loudly if any held-out target, analytic target, or peripheral subtype minimum is not satisfied.

## Final Target Counts

Per corpus:

1. 60 `core`
2. 40 `peripheral`
3. 60 `foil`

Combined totals:

1. 120 `core`
2. 80 `peripheral`
3. 120 `foil`
4. plus the 80-row naturalistic held-out slice

## Peripheral Subtype Minima

The final analytic sample must include, per corpus:

1. at least 4 `get`
2. at least 4 `prepositional`
3. at least 4 `reduced_embedded`
4. at least 4 `stative_adjectival`

These minima are enforced during finalization. Additional peripheral rows are filled in `sample_rank` order.

## Blindness During Annotation

During pass-1 cue coding, hide the following columns from the coder where practical:

1. `corpus`
2. `split`
3. `source_file`
4. `provisional_streams`
5. `sampling_stream`
6. `sample_set`
7. `sample_rank`

The coder should primarily see:

1. `sentence_marked`
2. `sentence`
3. `head_form`
4. `head_children`
5. the stable `candidate_id`

If corpus or stream information must be revealed to rescue a row from `exclude`, note that in `notes`.
