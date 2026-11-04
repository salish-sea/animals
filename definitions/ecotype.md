# ecotype

**Status:** working (usable and in force, but not yet confirmed by a domain expert).

## Working definition

A genetically and behaviourally distinct form of a species, made up of one or more
populations, that differs consistently from the species' other forms in prey preference,
vocal repertoire, social structure, and morphology, and does not interbreed with them
despite overlapping in range.

## Source

Working definition, editors of this repository, 2026-07, paraphrasing the standard usage
for *Orcinus orca*. Amended 2026-11-04 to say that an ecotype is made up of populations
rather than being one (Q27). Needs a citation to a specific source and expert
confirmation.

## Scope notes

- In scope for the Salish Sea: resident (`SSA:0000003`), Bigg's (`SSA:0000002`), and
  offshore when it is populated. [Q1](../docs/open-questions.md) settled this in favour
  of the strict reading: the residents are **one** ecotype containing two communities,
  Northern and Southern, rather than two ecotypes. Common usage speaks of SRKW and NRKW
  as separate ecotypes; the register does not, and a consumer rendering "ecotype" as a
  category will show *Resident* where a moderator might expect *SRKW*.
- **An ecotype can hold several populations.** The resident ecotype holds the Northern
  and Southern Residents, which are separate populations (Q1). The Bigg's ecotype holds
  the West Coast Transients and the Gulf of Alaska, Aleutian and Bering Sea transients,
  which are separate stocks. So T419, T420 and T421, which belong to the Alaskan stock,
  are members of Bigg's (`SSA:0000002`) like the West Coast Transients (Q27). The
  register has no rank for a stock. Add one when an observer needs to record a stock
  rather than an ecotype or a matriline; until then, the three whales sit directly in
  Bigg's, because their matriline is not known.
- An ecotype is **not a formal taxonomic rank**, which is exactly why it needs an
  identifier here — no external taxonomy will provide one. See
  [ADR-0008](../decisions/0008-species-identity-is-delegated.md).
- Recorded as `skos:broadMatch` to the species in `mappings.tsv`, never `exactMatch`.
- Resident and Bigg's are also `skos:closeMatch` to iNaturalist's *Orcinus orca ater* and
  *O. o. rectipinnus*. Close rather than exact, because an ecotype and a subspecies are
  different kinds of thing that here cover the same animals — and the equation is the
  Society for Marine Mammalogy's, quoted in the rows themselves, not the register's. It is
  what lets a consumer holding an iNaturalist record of a "Resident Killer Whale" find this
  entity. **A community never gets this mapping**: *ater* is every resident, and the
  Southern Residents are one population among them.

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

- Do humpbacks or other in-scope species have populations that warrant the same
  treatment, or is this rank orca-only?
