# Literature Priority

Checked on 2026-03-19 against two local stores:

1. shared literature: `/Users/brettreynolds/Documents/LLM-CLI-projects/literature`
2. local Mendeley holdings: `/Users/brettreynolds/Documents/Mendeley Desktop`

The point of this note is to stop indiscriminate collection. Much of the load-bearing literature is already local. The immediate task is to read what is already on disk, then fetch only the genuinely missing items.

## Read First

These are the load-bearing items for the current paper shape.

| Status | Item | Role in paper | Local location |
|---|---|---|---|
| have in shared | Boyd 1999, *Homeostasis, species and higher taxa* | core HPC framework | `LLM-CLI-projects/literature/boyd1999.pdf` |
| have in shared | Boyd 1991, *Realism, anti-foundationalism and the enthusiasm for natural kinds* | original HPC statement | `LLM-CLI-projects/literature/boyd1991.pdf` |
| have in shared | Slater 2015, *Natural Kindness* | HPC vs SPC pressure point | `LLM-CLI-projects/literature/slater2015.pdf` |
| have in shared | Wilson, Barker & Brigandt 2007, *When traditional essentialism fails* | worked HPC example for messy categories | `LLM-CLI-projects/literature/wilson_barker_brigandt_2007_when_traditional_essentialism_fails.pdf` |
| have in shared | Pullum 2014, *Fear and loathing of the English passive* | descriptive problem statement | `LLM-CLI-projects/literature/pullum2014-fear-and-loathing-of-the-english-passive.pdf` |
| have in repo | Pullum notes already made | current project-specific notes | `docs/pullum-2014-passive-notes.md` |
| have in shared | Huddleston & Pullum 2002, *The Cambridge Grammar of the English Language* | primary grammar reference | `LLM-CLI-projects/literature/huddlestonpullum2002.pdf` and `LLM-CLI-projects/literature/00-CGEL.pdf` |
| have in shared | Quirk et al. 1985, *A Comprehensive Grammar of the English Language* | fair classical checklist baseline | `LLM-CLI-projects/literature/quirk-et-al-1985-comprehensive-grammar-of-the-english-language.pdf` |
| have in shared | Goldberg 2006, *Constructions at Work* | construction-family framing | `LLM-CLI-projects/literature/goldberg2006-constructions-at-work.pdf` |
| have in shared | Croft 2001, *Radical Construction Grammar* | backup constructional category theory | `LLM-CLI-projects/literature/croft2001.pdf` |
| have in shared | Bresnan, Cueni, Nikitina & Baayen 2007, *Predicting the Dative Alternation* | direct methodological precedent for cue-bundle prediction | `LLM-CLI-projects/literature/bresnan-etal-2007-predicting-the-dative-alternation.pdf` |
| have in shared | Gelman et al. 2020, *Bayesian workflow* | model-checking and workflow backbone | `LLM-CLI-projects/literature/gelman-etal-2020-bayesian-workflow.pdf` |
| have in shared | Bürkner 2017, *brms: An R Package for Bayesian Multilevel Models Using Stan* | implementation reference | `LLM-CLI-projects/literature/burkner2017-brms-jss.pdf` |

## Conditional Reads

Only fetch or prioritize these if the corresponding cue or boundary case remains in the paper.

| Status | Item | Use condition | Notes |
|---|---|---|---|
| need to fetch | Wasow 1977, *Transformations and the Lexicon* | if the verbal vs adjectival passive boundary stays central | cited as a chapter in *Formal Syntax* |
| need to fetch | Reed 2011, *Get-passives* | if `get` passives remain in the peripheral probe set | verified DOI: `10.1515/tlir.2011.002` |
| need to fetch | Fleisher 2006, *The origin of passive get* | if the `get`-passive discussion needs a historical or reanalysis account | verified DOI: `10.1017/S1360674306001912` |
| need to fetch | Embick 2004, *On the Structure of Resultative Participles in English* | if adjectival/resultative participles remain a serious lower-boundary foil | verified DOI: `10.1162/0024389041402634` |
| need to fetch | Seoane 2012, *Givenness and Word Order: A Study of Long Passives...* | only if a discourse-givenness cue stays in the confirmatory model or theory section | verified chapter DOI: `10.1093/acprof:oso/9780199860210.003.0007` |
| have in shared | Zeldes 2017, *The GUM corpus: creating multilayer resources in the classroom* | if the corpus section remains in the main paper | `LLM-CLI-projects/literature/zeldes2017-gum-corpus.pdf` |
| have in shared | Silveira et al. 2014, *A Gold Standard Dependency Corpus for English* | if EWT extraction and corpus justification are described in the paper | `LLM-CLI-projects/literature/silveira-etal-2014-gold-standard-dependency-corpus-for-english.pdf` |
| have in shared | Vehtari, Gelman & Gabry 2017, *Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC* | if model-comparison discussion goes beyond brief mention | `LLM-CLI-projects/literature/vehtari-gelman-gabry-2017-loo-waic.pdf` |

## Defer Unless Needed For Objections

These are useful, but they are not required before outline-writing.

| Status | Item | Why defer | Local location |
|---|---|---|---|
| have in shared | Miller 2021, *Words, Species, and Kinds* | closest linguistic-kind precedent, but not needed to define the paper's core architecture | `LLM-CLI-projects/literature/miller2021.pdf` |
| have in shared | Aarts 2007, *Syntactic Gradience* | useful for gradience comparison, but secondary to HPC/SPC choice | `LLM-CLI-projects/literature/aarts2007.pdf` |
| have in shared | O'Connor 2019, *Games and kinds* | hostile background, better saved for objection management | `LLM-CLI-projects/literature/oconnor2019games.pdf` |
| have in shared | Haspelmath 2010 and related material | broad anti-natural-kind pressure on grammar categories, but too wide for the current drafting stage | `LLM-CLI-projects/literature/haspelmath2010.pdf` |
| have in shared | Kendig & Grey 2021 | useful once the paper decides how hard it is leaning into mechanism vs projectibility | `LLM-CLI-projects/literature/kendig_grey_2020_epistemic_value_natural_kinds_bjps_axz004.pdf` |
| have in shared | Khalidi material | alternative natural-kind framework, but not needed unless the paper has to defend HPC against nearby rivals in depth | `LLM-CLI-projects/literature/khalidi2013.pdf` and `LLM-CLI-projects/literature/khalidi2017.pdf` |

## Recommended Next Move

Do this in order:

1. Read the local `Read First` set that is already on disk.
2. Do not fetch the remaining boundary-case packet until the cue inventory is fully locked.
3. For unresolved boundary-case items, search the institutional library by exact title or DOI rather than by topic keywords.
4. Convert this note into a section-by-section reading order tied to `main.tex`.

## Practical Implication

The literature task is now bounded.

What still needs to be acquired before drafting is now mostly the lower-boundary packet, not the backbone.

The unresolved items are concentrated in exactly the part of the paper that is still theoretically optional:

1. verbal vs adjectival boundary
2. `get`-passive boundary
3. discourse-givenness support if that cue survives
