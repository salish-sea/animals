# Changelog

Started at the first commit rather than at the first release: a changelog begun late has
to be reconstructed, and this is what consumers read to find out what changed.

Entries that affect consumers — new, deprecated, or renamed identifiers — belong under
**Register**. Everything else is **Design**.

## Unreleased

### Design
- Initial scaffold: scope, competency questions, walkthrough, glossary, background,
  open questions, twelve decision records, six definitions, and a validator.
- All decision records are `Proposed`. No definition is `agreed`.

### Register
- Added `kind = taxon` entities for *Orcinus orca*, humpback, Steller sea lion, California
  sea lion and harbour seal, plus ecotype→species membership edges. These are what a
  moderator tags when an orca is heard too faintly to place in an ecotype — roughly 30% of
  the biophony corpus previously had nothing to tag.
- `status.tsv` gains a `recorded` column and a stated precedence rule, so a retracted
  life-status claim is resolvable. Consumers must order by `(recorded, effective)`.
- Reviewed by two independent passes (consistency, gaps); corrections applied and the
  remaining design questions filed as Q15–Q21 rather than resolved silently.
- Seed data only. Every row carries `source_id = SEED`, meaning **unverified** — the
  seed exists to make the schema concrete and to give the walkthrough something to
  point at. It must be replaced or confirmed by a curator before any consumer relies
  on it.
