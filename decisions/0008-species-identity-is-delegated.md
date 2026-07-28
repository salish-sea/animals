# ADR-0008: Species identity is delegated, not minted

- **Status:** Proposed
- **Date:** 2026-07-27
- **Audience:** Scientific and informatics reviewers — the sections below are split, so each can read their half.

## Context

Species have stable, maintained, widely-adopted identifiers already. Ecotypes, pods,
matrilines and individuals do not. Minting our own species identifiers would duplicate
solved work and create a crosswalk burden forever.

A search of the [Ontology Lookup Service](https://www.ebi.ac.uk/ols4/) confirms the
asymmetry:

- *Orcinus orca* is `NCBITaxon:9733`, and also has SNOMED and MeSH identifiers.
- **Nothing exists for killer whale ecotypes, pods, matrilines, or individuals**, and
  nothing exists for the acoustic signal types either. The nearest hits for the sound
  side are `GO:0071625` / `NBO:0000037` "vocalization behavior" — a behaviour class, not
  a catalogue of call types.

## Decision

Species identity is referenced, never minted. `entities.tsv` carries a `taxon_id`
pointing at an external authority. The register is an authority only for what no
external authority provides: ecotype and below.

## What this means for the data

The register is doing two different jobs and it is worth seeing which is which:

- **Crosswalk** at the species level — we are just pointing at NCBI or WoRMS.
- **Authority** at the ecotype/pod/matriline/individual level — nobody else publishes
  these as identifiers, so if we get them wrong, there is nothing to check against.

The second is where curation effort should go. The first should be nearly free.

Note that **an ecotype is not a taxonomic rank**. `SSA:0000001` (Southern Resident) is
recorded as `skos:broadMatch` to *Orcinus orca* — narrower than the species, but not a
subspecies and not making any claim about formal taxonomy. That distinction matters if
anything here is ever exported to GBIF.

### Delegating an identifier is not the same as refusing an entity

This decision was read, initially by its own author, as "the register holds nothing at
species level". That reading blocks about 30% of the OrcaSound biophony corpus: humpbacks,
sea lions, fish, and — most often — **an orca heard too faintly to resolve to an ecotype**,
which is a routine moderator outcome rather than an edge case.

The reading is wrong. This ADR forbids **minting a species identifier**. It does not forbid
a **register entity that references one**:

```
SSA:0000900   taxon   Orcinus orca   NCBITaxon:9733
```

`SSA:0000900` is a taggable stand-in for "an animal of this species, not resolved further".
It mints no taxonomy — NCBI still owns the species concept, and the entity carries a
pointer to it.

"An orca, ecotype undetermined" then needs no new concept at all: it is `SSA:0000900`
with no ecotype tagged alongside it. Uncertainty about *which* ecotype stays out of the
vocabulary, exactly as [ADR-0009](0009-uncertainty-on-the-annotation.md) requires.

## Implementation

- Entities of `kind = taxon` carry a `taxon_id` and no `rank` — ranks are social levels,
  and a species is not one ([ADR-0004](0004-rank-is-an-open-vocabulary.md)). Validation
  enforces both.
- Ecotypes are members of their species taxon, which roots the membership graph and lets a
  matriline roll up to a species even while the ecotype/community question
  ([Q1](../docs/open-questions.md)) is unresolved.
- Taxon entities have no life status. They are kinds, not animals.
- `taxon_id` uses `NCBITaxon:` CURIEs. NCBI was chosen over WoRMS because OLS resolves
  it directly and it is what the OBO ecosystem uses; WoRMS is recorded in `sources.tsv`
  as a parallel authority and a WoRMS crosswalk can be added to `mappings.tsv` when
  something needs it.
- Group entities inherit their `taxon_id` explicitly rather than by inference, so a
  consumer never has to walk the membership graph just to learn the species.
- Ecotype→species relationships are `skos:broadMatch` in `mappings.tsv`, not
  `exactMatch`.

## Consequences

- No species curation burden, and no risk of our species list drifting from consensus.
- A dependency on NCBI's identifiers being stable. They are, and they are not going
  anywhere.
- Species-level tagging works via `kind = taxon` entities, which closes
  [competency question O1](../docs/competency-questions.md).
- The register now holds entities that are *kinds*, not collections of individuals.
  Anything iterating over entities must handle three kinds, not two.
- iNaturalist is deliberately *not* the taxonomic authority here, despite being named
  first in the originating discussion. It is a good audience and a reasonable crosswalk
  target, but it is crowd-edited and its taxonomy shifts. A crosswalk to iNat taxon
  identifiers can be added to `mappings.tsv` if a consumer needs one.

## Alternatives considered

- **WoRMS as primary.** Arguably more apt for marine taxa and actively curated by marine
  specialists. The choice is close and reversible; NCBI wins on tooling only.
- **Minting our own species entities for uniformity**, so every entity is a register
  entity. Rejected — pure duplication with a permanent synchronisation cost.

## Open questions

- If anything is ever published to GBIF or OBIS, how is an ecotype expressed in Darwin
  Core? There may be no clean answer, which would be worth knowing before promising it.
