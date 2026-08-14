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

- In scope for the Salish Sea: resident, Bigg's, offshore — **or** Southern Resident,
  Northern Resident, Bigg's, offshore, depending on [Q1](../docs/open-questions.md). In
  the stricter reading the residents are one ecotype containing two communities; in common
  usage SRKW and NRKW are spoken of as separate ecotypes. Unresolved.
- An ecotype is **not a formal taxonomic rank**, which is exactly why it needs an
  identifier here — no external taxonomy will provide one. See
  [ADR-0008](../decisions/0008-species-identity-is-delegated.md).
- Recorded as `skos:broadMatch` to the species in `mappings.tsv`, never `exactMatch`.

## What it is not

**Not a subspecies**, and no claim about formal taxonomy is intended or should be
inferred. If ecotypes are formally described as subspecies or species in future, that
becomes a crosswalk change, not a restructuring — which is no longer hypothetical:
resident and Bigg's killer whales have been proposed as *Orcinus ater* and *Orcinus
rectipinnus*. NCBI Taxonomy has not adopted them (checked 2026-07-28), so `NCBITaxon:9733`
remains correct for everything here.

**Not a community.** See [community.md](community.md) and open question Q1 — these two
may in fact be redundant in this register.

## Open questions

- Is an ecotype a *population*, as the definition above says, or something that contains
  several? The register now holds three animals from the Alaskan transient stock
  (`SSA:0010510`–`SSA:0010512`) under Bigg's, beside 132 West Coast Transient matrilines,
  so the strict reading makes that membership false and the loose reading makes this
  definition wrong. (Q27)
- Should the register distinguish ecotype from community at all? (Q1)
- Do humpbacks or other in-scope species have populations that warrant the same
  treatment, or is this rank orca-only?
