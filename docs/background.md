# Background: lessons from other projects

**Audience: informatics, but the first section is for everyone.** This document exists
because the failure mode we are most likely to hit is not a modelling error. It is
building something correct that nobody uses and nobody maintains.

## The graveyard

Shared vocabularies have been built for decades, mostly under the "semantic web" and
"ontology" banners. The large majority are dead: published once, never updated, cited by
nobody, still resolving to a 404 or a parked domain.

The survivors have one thing in common. **A system that people needed refused to work
without the vocabulary.**

| Survivor | What forced adoption |
|---|---|
| [Gene Ontology](https://geneontology.org/) | Model-organism databases couldn't publish curated gene-function annotations without it |
| [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy/) | You cannot submit a sequence without a taxon id |
| [Darwin Core](https://dwc.tdwg.org/) | GBIF and OBIS reject non-conforming data, and museums need to be in GBIF |
| [WoRMS](https://www.marinespecies.org/) | Marine taxonomy has no viable alternative |
| SNOMED CT / ICD | Billing and regulation |

The ones that died were published *first*, and hoped adoption would follow.

### What that means for us

The honest test: **what breaks if this register stops being maintained?**

Today the answer is "SalishSea.io's map degrades back to parsing bout names." That is a
real dependency but a thin one. It is not GBIF-rejects-your-data.

Two consequences we should act on:

1. **Stay subordinate to the consuming systems for as long as possible.** This should
   read as a directory that two apps depend on, not as a project with its own website,
   its own governance body, and its own conference talk. The moment it acquires an
   independent identity it joins the graveyard cohort. Let the consumers demand
   independence; don't grant it pre-emptively.
2. **Ship it into a real system early, even half-done.** A vocabulary that has never
   been used by a production system has never been tested. The first fifty bouts tagged
   from it will teach us more than another month of design.

## What we are borrowing from OBO and the Gene Ontology

The [OBO Foundry](https://obofoundry.org/) is a community of biological ontologies with
shared conventions. We are taking its **policies** and leaving its **formalism**.

### Taken

- **Identifier hygiene.** Numeric, opaque, prefixed, permanent. Never deleted, never
  reused, never repurposed. This is why GO annotations written in 1999 are still
  interpretable. → [ADR-0002](../decisions/0002-opaque-permanent-identifiers.md),
  [ADR-0010](../decisions/0010-identifiers-are-never-reused.md)

- **The two-tier obsolescence pointer.** An obsolete term carries either `replaced_by`
  (an unambiguous substitution a consumer may apply automatically) or `consider` (one or
  more candidates requiring human judgement). This one extra column is the difference
  between a deprecation costing an afternoon and costing a curator a month.
  → `data/deprecations.tsv`

- **Definitions carry their source.** Every OBO definition has an attribution. It stops
  a curator from inventing a definition and forgetting they did. "Working definition,
  <name>, 2026-07" is a perfectly good source — it just has to be visibly that.
  → `definitions/`, `data/sources.tsv`

- **Evidence codes on the annotation, not the term.** The under-appreciated lesson: GO's
  durability rests as much on its *annotation* format as its ontology. Every GO
  annotation states how the claim was arrived at, and cites a reference. Ours is a small
  closed set: `moderator-acoustic`, `photo-id-confirmed`, `inferred-from-sighting`,
  `automated-detector`. → [walkthrough.md](walkthrough.md)

- **GitHub issues as the term-request queue**, with a template, and the identifier
  minted only on merge. GO has run this way for years at a scale far beyond ours.
  → `.github/ISSUE_TEMPLATE/`

- **Competency questions** as the test of whether the model is done.
  → [competency-questions.md](competency-questions.md)

### Deliberately not taken

- **OWL, reasoners, description logics.** No inference we need justifies the tooling.
  Ancestor lookup is a graph walk over one small file.
- **Upper-ontology alignment (BFO and friends).** Months of work; no payoff at this
  scale.
- **The OBO file format and ROBOT tooling.** TSV in git is reviewable by the people who
  need to review it. `.obo` is not.
- **OBO Foundry registration.** Maybe someday. Not a prerequisite for being useful.

## Other things worth stealing

- **[SSSOM](https://mapping-commons.github.io/sssom/)** (Simple Standard for Sharing
  Ontological Mappings) — a flat TSV for crosswalks with a match predicate
  (`exactMatch` / `closeMatch` / `broadMatch`), a justification, and a confidence. This
  is exactly the "link our identifiers to finwave's and CWR's" problem. We follow its
  column names; we are not claiming conformance. → `data/mappings.tsv`

- **[SKOS](https://www.w3.org/TR/skos-reference/)** — for the distinction between a
  preferred label, an alternate label, and a *hidden* label. Hidden labels are the trick
  that makes autocomplete work without endorsing every spelling. → `data/names.tsv`

- **[Darwin Core](https://dwc.tdwg.org/)** — `identificationQualifier` and
  `identificationVerificationStatus` already solve the `+L?` problem, and SalishSea.io
  will likely want DwC-shaped output for OBIS/GBIF eventually. Worth conforming to at
  the *export* boundary rather than internally.

- **[EDTF](https://www.loc.gov/standards/datetime/)** (Extended Date/Time Format) — lets
  `1998`, `2020-09`, `1995/1998` and `1998?` all live in one column. Ages are usually
  estimated ranges, and a plain date column destroys that on entry.

- **[Architecture Decision Records](https://adr.github.io/)** — the `decisions/`
  directory. Cheap, and they are what stop a settled question from being relitigated
  every six months by whoever joined most recently.

## Failure modes we should expect

Ranked by how likely they are to actually kill this, most likely first.

1. **Nobody owns it.** The roster goes stale after a birth season, consumers notice it's
   wrong, they stop trusting it, and it's over. This is the single most common cause of
   death in this space, and it is a staffing problem wearing a governance costume. See
   `CODEOWNERS` and [open-questions.md](open-questions.md) Q8.
2. **Moderators route around it.** If the pick list is slower than typing, or the term
   they need isn't there and there's no fast way to get it added, they go back to free
   text — and the data acquires a silent bias toward whichever terms were easy to find.
3. **The change process is too slow.** A calf confirmed in November that can't be tagged
   until February trains people not to bother. Hence the provisional tier
   ([ADR-0001](../decisions/0001-tsv-in-git-as-source-of-truth.md)) and the escape hatch.
4. **Definitions stay vague.** Two curators apply a term differently, nobody notices,
   and the resulting inconsistency is invisible in the data and unfixable by script.
   This is the one failure mode where prevention is much cheaper than cure.
5. **Scope creep into occurrences.** The register starts holding sightings, drifts from
   its upstream authorities, and becomes a third database nobody trusts.

Modelling errors are not on this list. They are recoverable — see
[ADR-0006](../decisions/0006-valid-time-in-data-assertion-time-in-git.md) and the rule
that consumers keep the moderator's raw text forever.
