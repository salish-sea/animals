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

- In scope for the Salish Sea: Southern Resident, Northern Resident, Bigg's, offshore.
- An ecotype is **not a formal taxonomic rank**, which is exactly why it needs an
  identifier here — no external taxonomy will provide one. See
  [ADR-0008](../decisions/0008-species-identity-is-delegated.md).
- Recorded as `skos:broadMatch` to the species in `mappings.tsv`, never `exactMatch`.

## What it is not

**Not a subspecies**, and no claim about formal taxonomy is intended or should be
inferred. If ecotypes are formally described as subspecies or species in future, that
becomes a crosswalk change, not a restructuring.

**Not a community.** See [community.md](community.md) and open question Q1 — these two
may in fact be redundant in this register.

## Open questions

- Should the register distinguish ecotype from community at all? (Q1)
- Do humpbacks or other in-scope species have populations that warrant the same
  treatment, or is this rank orca-only?
