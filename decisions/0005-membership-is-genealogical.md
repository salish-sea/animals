# ADR-0005: Membership is genealogical; association is occurrence data

- **Status:** Proposed
- **Date:** 2026-07-27
- **Audience:** Both

## Context

"J17 is in J pod" and "L87 travels with J pod" both sound like membership. They are not
the same claim, and a register that treats them the same will produce answers nobody can
interpret.

The test case is real. L87 (Onyx) was born to L32 in L pod. After his mother died he
travelled with K pod, and later spent years travelling with J pod. Is L87 in L pod or
J pod?

## Decision

**Membership in this register is genealogical.** An individual belongs to the matriline
they were born into, for life. L87 is in L pod, permanently, and his travel with J pod
is not recorded here at all — it is a property of encounters, and belongs in OrcaSound
and SalishSea.io.

## What this means for the data

The everyday sense of "in J pod" is broader than the register's sense, and this will
surprise people. Two consequences to check:

- **A bout where L87 was heard travelling with J pod** should be annotated with J pod
  (what was heard) and, if the individual was identified, with L87. The register will
  then say L87 is an L pod animal, and *that is correct* — the apparent contradiction is
  the register reporting descent while the annotation reports an encounter. Both are
  true.
- **Group membership counts derived from this register are counts of descent, not of
  travelling units.** If anyone publishes such a count, it must be labelled as such. See
  [open-questions.md](../docs/open-questions.md) Q6.

The alternative — defining membership as observed association — was rejected because it
makes membership change constantly, makes it dependent on who was looking, and means the
register would have to ingest sighting data to stay current. That is the scope boundary
in [ADR-0007](0007-no-observations.md).

### Where the interval columns still earn their place

`membership.tsv` has `start` and `end` columns even though natal membership never ends
before death. Three reasons, in order of importance:

1. **Group-to-group edges genuinely change.** Matrilines fission when a matriarch dies
   and daughters' groups come to be recognised separately; a matriline can be reassigned
   between pods. Neither endpoint is an individual, so there is no lifespan to derive an
   end from.
2. **Bigg's disperse.** Residents are the unusual case — neither sex leaves the natal
   group. Bigg's offspring do leave, males especially, and females often after having
   calves of their own. Since both ecotypes are in scope, the schema has to accommodate
   the one where membership really does change mid-life.
3. L87-style cases, *if* a curator ever decides one is a genuine change of social unit
   rather than an association. Under this ADR they are not, but the column means that
   decision does not require a schema change.

## Implementation

- **Natal individual→group edges leave both columns empty.** Empty means "bounded by the
  individual's lifespan", and consumers evaluate membership as
  `interval ∩ lifespan`.
- **`end` is never used to record a death.** That is `status.tsv`'s job, and duplicating
  it in two files creates a consistency hazard where one copy can be corrected and the
  other silently not. Validation rejects a non-empty `end` on an individual edge whose
  note indicates death.
- A non-empty `end` on an individual edge therefore means dispersal, and nothing else.
- Dates are EDTF, so an approximate dispersal year is expressible.

## Consequences

- "Which individuals were in J pod at time T" is a join through `status.tsv` rather than
  a scan of one table. Slightly more work, one source of truth.
- The register cannot answer "who was travelling with whom", by design. Anyone who needs
  that is asking the wrong system.
- If the community's usage of "pod" turns out to be predominantly associational rather
  than genealogical, this decision inverts and a lot of documentation changes. Worth
  confirming early with the scientific reviewers.

## Alternatives considered

- **Membership as observed association.** Rejected above.
- **Two relation types in one table** (`member_of`, `travels_with`). Rejected: it puts
  occurrence data in the register through the back door, and `travels_with` has no
  meaningful value without a date and an observer — at which point it is a sighting
  record.
- **Dropping `start`/`end` entirely**, letting fission be handled by deprecating the old
  matriline identifier and minting new ones. Genuinely cleaner in some ways — it makes
  fission an identity event rather than a temporal one — but loses the ability to say
  "these were the same animals under a different name". Reconsiderable.

## Open questions

- Does "matriline membership" survive the matriarch's death, or does the group become
  something else? Affects how fission is recorded. Science question.
