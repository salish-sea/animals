# ADR-0003: One identifier space for individuals and groups

- **Status:** Proposed
- **Date:** 2026-07-27
- **Audience:** Both

## Context

The register holds two kinds of thing: individual animals, and groups of animals
(ecotypes, clans, pods, matrilines). They could live in separate files with separate
identifier series, or share one.

Membership relates both: an individual belongs to a matriline, and a matriline belongs
to a pod. Both are "X is inside Y".

## Decision

One file, `entities.tsv`, one identifier series, and a `kind` column distinguishing
`individual` from `group`. `membership.tsv` has one shape — `member_id`, `group_id` —
regardless of what kind of thing sits at either end.

## What this means for the data

A consequence worth stating plainly, because it looks like a bug: **a matriline and the
whale it is named after are two different entries.**

```
SSA:0000030   group        matriline   J17    ← the matriline
SSA:0000105   individual               J17    ← the whale
```

Both are labelled `J17` and that is correct. Whale researchers use one name for both,
context making it obvious which is meant, and there is nothing wrong with that in
speech. A register cannot rely on context: "J17 was born in 1977" and "J17 travels with
J pod" are claims about different things, and the matriline will outlive the whale.

This is also why the identifiers are opaque
([ADR-0002](0002-opaque-permanent-identifiers.md)) — a slug scheme would have to encode
the distinction in the string, and every consumer would have to parse it correctly
forever.

## Implementation

- `kind` is `individual` or `group`. `rank` is populated for groups and empty for
  individuals.
- `membership.tsv` is uniform: any entity may appear in either column. Validation
  enforces that `group_id` refers to a row with `kind = group`.
- Validation warns when two entities share a label, because most of the time that's a
  mistake — but does not reject, because in the matriline case it is correct. The
  warning is suppressed when the two differ in `kind`.

## Consequences

- Ancestor lookup is one algorithm over one table, whatever the ranks involved.
- Adding a rank later needs no schema change ([ADR-0004](0004-rank-is-an-open-vocabulary.md)).
- Type confusion becomes possible: nothing structurally prevents tagging a bout with a
  matriline where an individual was meant. Consumers should filter by `kind` in their
  UI rather than relying on the register to prevent it.
- Duplicate labels will confuse autocomplete unless the UI shows `rank` alongside. This
  is a real UX cost of the decision and should be handled in OrcaSound's picker.

## Alternatives considered

- **Separate `individuals.tsv` and `groups.tsv`.** Cleaner conceptually; forces
  `membership.tsv` into either two files or a polymorphic column with a type tag, which
  is the same thing with more ceremony.
- **Making a matriline a property of an individual** (`J17.matriline = "J17"`). Collapses
  the two entities and is genuinely simpler until a matriline outlives its matriarch,
  splits, or is renamed — all of which happen.

## Open questions

- Should `rank` be required for groups? Currently yes by validation, but a group with no
  agreed rank is plausible (an unnamed travelling unit) and there is no way to record it.
