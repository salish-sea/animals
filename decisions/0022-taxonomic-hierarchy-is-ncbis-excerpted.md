# ADR-0022: The taxonomic hierarchy is NCBI's, excerpted — not curated here

- **Status:** Proposed
- **Date:** 2026-09-20
- **Amends:** [ADR-0008](0008-species-identity-is-delegated.md), which anticipated a
  `taxonomic_parent` relation and warned what it would cost.
- **Audience:** Informatics reviewers, and anyone publishing occurrences from the register.

## Context

[ADR-0008](0008-species-identity-is-delegated.md) made the register a forest — one tree per
species, no shared root — and said plainly that taxonomic kinship "is NCBI's to publish".
That was right, and it left consumers with nowhere to get it. The register's 40 taxon
entities are flat: nothing here says *Orcinus orca* is a dolphin, or that a harbour seal and
a Steller sea lion are both pinnipeds.

SalishSea.io found the gap from the other side on 2026-09-20. It had moved its animal
*names* to the register and assumed the rest followed. It had not: every occurrence still
takes its species, its rank and its ancestry from a mirror of iNaturalist's taxonomy —
which ADR-0008 says is "deliberately *not* the taxonomic authority". Three things there
need a tree and had only that one to use:

- the DarwinCore export's `kingdom` … `genus` columns;
- "is this a pinniped?", for the haul-out pages;
- rolling a record up to its species.

So the register said the authority was NCBI while its only consumer, for want of anything
else, treated iNaturalist as one.

## Decision

**The register publishes NCBI's lineage for every taxon it points at, as an excerpt it
fetches and never edits.**

`data/taxonomic_parent.tsv` holds one row per node on the path from each `taxon_id` to
NCBI's root: the node's `NCBITaxon:` identifier, its parent's, and NCBI's own rank and
scientific name. [`bin/import_taxonomy.py`](../bin/import_taxonomy.py) writes it. Nobody
else does.

This is delegation carried one step further, not abandoned. The register still mints no
species identifier and still holds no opinion about taxonomy. It now also *reports* what
the authority it delegated to says.

## What this means for the data

- **No `SSA:` identifier is minted.** Delphinidae is `NCBITaxon:9726` and nothing else. A
  family is not an entity, cannot be tagged, and has no names here.
- **The whole lineage is kept, unranked clades included.** A killer whale has 28 ancestors
  and 14 of them have no rank (Boreoeutheria, Whippomorpha…). Dropping them would be
  editing NCBI's tree. `dist/classification.tsv` does the filtering a consumer usually
  wants.
- **Names and ranks are verbatim, and two of them will surprise people.** NCBI's kingdom
  for animals is **`Metazoa`**, not `Animalia`. Its order for a whale is **`Artiodactyla`**,
  with `Cetacea` an infraorder beneath it. Those are NCBI's positions and are reported as
  such. A consumer that must publish `Animalia` — GBIF's backbone says so — maps that one
  value on its own side and records why; the register does not quietly correct its
  authority.
- **Subsumption stays apart from membership.** ADR-0008's warning holds: one closure over
  both would answer "what groups is J35 a member of?" with `Mammalia`. They are separate
  tables and separate views, and `dist/ancestor.tsv` is unchanged.
- **`rank` here is not the `rank` table.** That table holds social levels
  ([ADR-0004](0004-rank-is-an-open-vocabulary.md)). This column holds NCBI's word.
- **The excerpt must be whole.** `entities.taxon_id` is now a foreign key into it, so a
  new `taxon_id` fails validation until the importer has fetched its lineage. The
  validator also checks that every parent has a row, that there is one root, that nothing
  loops, and that no row is a leftover nothing descends to.

Two views do the consuming once ([ADR-0013](0013-distribution.md)):

- **`dist/taxon_ancestor.tsv`** — the closure. A taxon is its own ancestor at depth 0, so
  "is this a pinniped?" is one test against Phocidae or Otariidae whether the entity is a
  species or the family itself.
- **`dist/classification.tsv`** — `kingdom`, `phylum`, `class`, `order`, `family`, `genus`
  for each taxon entity. Empty where the entity sits above that rank: Laridae has no genus.

## Implementation

- The importer is reviewed as a transformation ([ADR-0015](0015-bulk-import.md)): its
  judgements are in its header, the rows are its output, and re-running it against an
  unchanged NCBI writes nothing.
- No date is recorded per row, which is what makes that true. When the excerpt was last
  taken is `retrieved_on` on the `NCBI` row of `sources.tsv`, which `--apply` stamps; a
  dry run and `--check` write nothing at all.
- One request to NCBI's E-utilities covers every taxon the register holds.
- `--check` exits non-zero when NCBI's lineage has moved. **It is not yet wired into the
  weekly drift job**, which today asks only whether each `taxon_id` still resolves. Until
  it is, a reclassification upstream is noticed when someone next runs the importer.

## Consequences

- A consumer can stop treating iNaturalist as a taxonomic authority without curating a
  tree of its own, which is the thing this record exists to make possible.
- **A contested placement is NCBI's to defend, and a reclassification is a re-fetch.** If
  Resident and Bigg's killer whales are split into species, the lineage above them does
  not change at all; ADR-0008's `taxon_id` rewrite then needs the two new identifiers to
  exist at NCBI first, exactly as before.
- The register depends on NCBI's E-utilities being reachable *to regenerate* the excerpt.
  Not to build, validate or release: the file is committed.
- The register now holds rows about things that are not entities. That is new, and it is
  confined to one table that says so.
- About 126 rows for 40 taxa. It grows with the number of distinct lineages, not with the
  number of animals.

## Alternatives considered

- **A curated `taxonomic_parent` between register entities** — the obvious reading of
  ADR-0008's sketch. Rejected: it needs `SSA:` identifiers for Delphinidae and Mammalia,
  which is minting taxonomy; it needs ranks on taxon entities, which ADR-0004 withholds;
  and every contested placement becomes this register's to adjudicate.
- **Leave it to consumers.** What happened by default, and how iNaturalist came to be one
  consumer's authority against the register's stated design.
- **Publish only the six DarwinCore ranks.** Smaller, and enough for the export. Rejected
  because "is this a pinniped?" needs a superfamily or two families, not a rank column, and
  because choosing which of NCBI's nodes to keep is a judgement the excerpt avoids making.
- **GBIF's backbone instead of NCBI.** It is what the export's consumer matches against
  and it says `Animalia`. Rejected for now because ADR-0008 already chose NCBI for
  `taxon_id`, and an identifier from one authority with a lineage from another is two
  delegations that can disagree. If `taxon_id` ever moves, this moves with it.

## Open questions

- Should the weekly drift job run `bin/import_taxonomy.py --check`? Almost certainly; it is
  left out of this change only to keep a workflow edit separate.
- Does any consumer need NCBI's *common* names? Not so far: names are the register's own
  ([ADR-0011](0011-label-is-a-preferred-name.md)).
