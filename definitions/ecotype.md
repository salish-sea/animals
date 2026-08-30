# ecotype

**Status:** working (usable and in force, but not yet confirmed by a domain expert).

## Working definition

A genetically and behaviourally distinct population within a species, differing
consistently in prey preference, vocal repertoire, social structure, and morphology, and
not interbreeding with other such populations despite overlapping in range.

## Source

Working definition, editors of this repository, 2026-07, paraphrasing the standard usage
for *Orcinus orca*. Needs a citation to a specific source and expert confirmation.

## Scope notes

- In scope for the Salish Sea: resident (`SSA:0000003`), Bigg's (`SSA:0000002`), and
  offshore when it is populated. [Q1](../docs/open-questions.md) settled this in favour
  of the strict reading: the residents are **one** ecotype containing two communities,
  Northern and Southern, rather than two ecotypes. Common usage speaks of SRKW and NRKW
  as separate ecotypes; the register does not, and a consumer rendering "ecotype" as a
  category will show *Resident* where a moderator might expect *SRKW*.
- An ecotype is **not a formal taxonomic rank**, which is exactly why it needs an
  identifier here — no external taxonomy will provide one. See
  [ADR-0008](../decisions/0008-species-identity-is-delegated.md).
- Recorded as `skos:broadMatch` to the species in `mappings.tsv`, never `exactMatch`.

## What it is not

**Not a subspecies**, and no claim about formal taxonomy is intended or should be
inferred. If ecotypes are formally described as subspecies or species in future, that
becomes a crosswalk change, not a restructuring — which is no longer hypothetical:
resident and Bigg's killer whales have been proposed as *Orcinus ater* and *Orcinus
rectipinnus*. The Society for Marine Mammalogy's Taxonomy Committee considered that
proposal in its [2024 annual
review](https://marinemammalscience.org/smm-news/taxonomy-committee-2024-annual-review/)
and **declined it**, citing possible episodic gene flow between the ecotypes and the need
for a global comparative analysis; it adopted Morin's names at *subspecies* rank instead,
provisionally. Neither NCBI Taxonomy nor WoRMS carries them at any rank (both rechecked
2026-08-29), so `NCBITaxon:9733` remains correct for everything here. ITIS and Catalogue
of Life do carry them, at species rank — the authorities disagree, and under ADR-0008
`taxon_id` records where they place a thing rather than which of them is right.

**Not a community.** See [community.md](community.md). Q1 confirmed the two ranks are
distinct and both needed: an ecotype contains communities.

## Open questions

- Is an ecotype a *population*, as the definition above says, or something that contains
  several? The register now holds three animals from the Alaskan transient stock
  (`SSA:0010510`–`SSA:0010512`) under Bigg's, beside 132 West Coast Transient matrilines,
  so the strict reading makes that membership false and the loose reading makes this
  definition wrong. (Q27)
- Do humpbacks or other in-scope species have populations that warrant the same
  treatment, or is this rank orca-only?
