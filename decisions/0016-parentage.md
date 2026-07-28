# ADR-0016: The register records parentage, as edges rather than columns

- **Status:** Proposed
- **Date:** 2026-07-28
- **Audience:** Scientific reviewers — this adds a claim the register makes about animals, so the modelling is yours to check. Informatics reviewers — it adds a table and five checks.

## Context

The register used to claim, in [scope.md](../docs/scope.md) and
[competency-questions.md](../docs/competency-questions.md), that parentage was implied by
matriline membership. **It is not.** A matriline spans three or four generations, so an
edge into one says "descended from the matriarch", not "child of". J57's mother is J35,
and no walk of `membership.tsv` recovers that. Until now the fact survived only in a
free-text `note` on `entities.tsv` that the validator ignores.

The false claim was corrected when it was found. What stayed open was
[Q16](../docs/open-questions.md): record parentage, or declare it out of scope and stop
implying it.

Two things pressed on the answer. [ADR-0007](0007-no-observations.md) exists to refuse new
facts, and it should be tested against rather than argued around. And SalishSea.io already
records `mother_id` / `father_id`, which [ADR-0012](0012-relationship-to-the-salishsea-io-catalogue.md)
lists as one of five findings this register must answer before that catalogue can migrate
to it.

## Decision

**The register records parentage**, in `data/parentage.tsv`, one row per child and role.

It does not breach ADR-0007, and the way to see that is to apply that ADR's own test
rather than to reason about the spirit of it:

> If the claim needs a date and a place to be meaningful, it is an occurrence and lives
> in the consuming systems.

"J57's mother is J35" needs neither. It is the same kind of fact as "J35 is female, born
~1998", which ADR-0007's own table already places in the register. The test was written to
be applied without a judgement call, and it returns a clean answer here.

**Parentage is recorded as edges, not as columns on `entities.tsv`** — which is where
SalishSea.io puts it, and is the more obvious design.

1. **Provenance is per claim.** `entity.source_id` covers a whole row. Maternity generally
   comes from a census; paternity comes from genetic study, which is a different source
   entirely. A column would silently attribute the parentage claim to whoever supplied the
   animal, and [ADR-0001](0001-tsv-in-git-as-source-of-truth.md) is built on knowing who
   said what.
2. **`membership.tsv` is already an edge table** with its own `source_id` and `note`.
   Parentage is an edge. Modelling it twice differently would be the arbitrary choice.
3. **A correction stays reviewable.** A changed row in a small table reads as a diff; a
   changed cell in a 661-row entity table does not.
4. It is strictly more expressive than the two columns it has to be at least as expressive
   as (ADR-0012).

## What this means for the data

**Neither parentage nor membership is derived from the other.** Both are asserted, and
that is deliberate: it is what makes them checkable against each other. A calf is born
into its mother's matriline, so mother and child should share one — and when they do not,
either the parentage is wrong, the membership is wrong, or the matriline has been split.
All three are worth a curator's attention, and deriving either fact from the other would
silence exactly the disagreement worth seeing.

**Parentage will be sparse for a long time, and that is expected.** It ships with one row.
The Bigg's designation sheet imported in [ADR-0015](0015-bulk-import.md) supplies 510
individuals and no parentage at all: T-number lineage groups animals without stating who
bore whom, which is [Q22](../docs/open-questions.md). Sparse is not the same as wrong —
absent parentage means "not recorded", never "no mother".

`father` is a role from the start even though almost nothing will carry it. Paternity in
this population is known only where someone has done the genetics, and leaving the role
out would mean a schema change the first time a curator has one.

**A parentage fact now lives in one place.** J57's note on `entities.tsv` said "Calf of
J35"; that note is gone, because a fact held in a table *and* in prose is the hazard
[ADR-0005](0005-membership-is-genealogical.md) describes for `end` versus `status.tsv` —
one copy gets corrected and the other silently does not. The exception is L87, whose
mother L32 is not in the register at all: an edge needs both endpoints, so recording it
means first minting a dead animal, which is a roster addition a curator should make
deliberately rather than a side effect of this change. Their note says so explicitly.

## Implementation

```
child_id  parent_id  role  source_id  note
```

- **`PRIMARY KEY (child_id, role)`** — one mother, one father. Two sources disagreeing is
  a curation question settled before publication ([Q3](../docs/open-questions.md)); the
  register carries an answer, not an argument.
- **`child_kind` and `parent_kind`** are denormalised into the database so composite
  foreign keys can state "only animals have parents, and only animals are parents". This
  is the same trick `membership.group_kind` uses and the same wart ADR-0013 admits to:
  curators never maintain them, the build populates them, and the TSV has five columns.

Five checks, and it is worth noting which the schema gets for free:

| Check | Where |
|---|---|
| Parent and child are both individuals | `schema.sql`, composite FK |
| Nobody is their own parent | `schema.sql`, `CHECK` |
| Nobody has two mothers | `schema.sql`, `PRIMARY KEY` |
| Nobody is transitively their own ancestor | recursive CTE |
| A mother is not sexed `M`, a father not `F` | query |
| A parent is not born after their child | Python — EDTF |

The birth-order check compares only dates that open with a plain year. `../1966` means "no
later than 1966" and there is nothing to compare; guessing would be worse than staying
quiet.

**The matriline check is a warning, not an error.** Matrilines that grow large are
eventually split, and after a fission a mother and her calf can legitimately sit in
different ones. Making it an error would force curators to suppress a real phenomenon.

## Consequences

- "Who is this animal's mother?" leaves the *deliberately unanswerable* list in
  `competency-questions.md`, where it never belonged once the reasoning behind it turned
  out to be false.
- `scope.md`'s "Membership and life status only" was accurate and is now not. Amended
  there.
- One of ADR-0012's five findings is answered. The remaining four are unchanged.
- **The register can now be wrong in a way it could not be before.** It can assert a
  parentage that contradicts its own membership. The cross-check surfaces that, which is
  a gain over the previous state, where the same contradiction was unrepresentable because
  half of it lived in a `note`.
- Parentage is not sensitive in the way health data is — CWR publishes birth and lineage
  annually — so [Q9](../docs/open-questions.md) is not reopened by this.

## Alternatives considered

- **`mother_id` / `father_id` on `entities.tsv`.** What SalishSea.io does, and simpler.
  Rejected on provenance: one `source_id` per row cannot carry a paternity that came from
  a genetic study and an existence that came from a census.
- **Deriving matrilines from parentage**, which is SalishSea.io's model and arguably the
  better one. Rejected *for now*, on data rather than on principle: parentage is sparse
  and Bigg's have effectively none, so derived matrilines would be empty precisely where
  the roster is largest. Reconsiderable once parentage is dense. The cross-check is the
  cheap version of the same idea and keeps both claims independent.
- **Declaring parentage out of scope** and deleting the implication. Coherent, and it was
  half of Q16. Rejected: the register would then be less expressive than the catalogue it
  is displacing, which ADR-0012 does not allow, and matrilines would stay
  unverifiable against anything.

## Open questions

- Should the maternal line ship as a closure in `dist/`, the way `ancestor.tsv` does for
  membership? Not worth generating for one row; revisit when parentage is dense.
- Does the Bigg's sheet's lineage grouping encode mother-calf pairs a curator could
  recover? That is the same evidence [Q22](../docs/open-questions.md) is about, read for a
  different purpose.
- Paternity is genetically derived and maternity is observed. Does that difference need an
  evidence column, or is `source_id` enough to carry it?
