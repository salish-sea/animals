# ADR-0003: One identifier space for individuals and groups

- **Status:** Proposed
- **Date:** 2026-07-27
- **Audience:** Scientific and informatics reviewers — the sections below are split, so each can read their half.

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
SSA:0000030   group        matriline   J17s   ← the matriline
SSA:0000105   individual               J17    ← the whale
```

The matriline takes the **plural** form — `J17s`, `T090s` — which is how the community
ordinarily writes it. The bare designation (`J17`, `T090 matriline`) is recorded in
`names.tsv` as a `hidden` name, so a curator typing either form finds the right entity.

**The plural convention is a display choice, not the thing that keeps them apart.** This
distinction matters, because it is tempting to conclude that distinct labels solve the
problem. They do not, for three reasons:

- The convention is not universal. Catalogues write `T090 matriline`; a curator may
  reasonably enter the bare form.
- It does not extend to other ranks. A pod is `J pod`, not `Js` — though "the Js" does
  appear in bout names and is recorded as a hidden name.
- Labels are mutable by design ([ADR-0002](0002-opaque-permanent-identifiers.md)). If
  the naming convention changed tomorrow, identity must not change with it.

The matriline and the matriarch are separate entities because they are separate things:
"J17 was born in 1977" and "J17s travel with J pod" are claims about different subjects,
and the matriline will outlive the whale. Whale researchers rely on context to tell them
apart, which works fine in speech. A register cannot.

This is also why the identifiers are opaque — a slug scheme would have to encode the
distinction in the string, and every consumer would have to parse it correctly forever.

## Implementation

- `kind` is `individual` or `group`. `rank` is populated for groups and empty for
  individuals.
- `membership.tsv` is uniform: any entity may appear in either column. Validation
  enforces that `group_id` refers to a row with `kind = group`.
- Validation warns when two entities share a label at the same `kind` and `rank`, which
  is almost always a mistake. It does not warn across kinds, because a matriline and its
  matriarch legitimately share a designation even when the display labels differ.

## Consequences

- Ancestor lookup is one algorithm over one table, whatever the ranks involved.
- Adding a rank later needs no schema change ([ADR-0004](0004-rank-is-an-open-vocabulary.md)).
- Type confusion becomes possible: nothing structurally prevents tagging a bout with a
  matriline where an individual was meant. Consumers should filter by `kind` in their
  UI rather than relying on the register to prevent it.
- Autocomplete must still show `kind` and `rank` alongside the label. The plural
  convention separates the two entities on *display*, but not in *search*: `J17` is the
  individual's primary label and also a hidden name on the matriline, so a curator typing
  it sees both and needs the rank to choose. That is the desired behaviour — they may
  well have meant either — but it means the picker cannot present a bare label alone.

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
