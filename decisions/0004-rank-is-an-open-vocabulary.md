# ADR-0004: Rank is an open vocabulary, not a fixed hierarchy

- **Status:** Proposed
- **Date:** 2026-07-27
- **Audience:** Science — this decision changes what the data *means*. Needs domain expertise, not software judgement.

## Context

It is tempting to model the social structure as a fixed ladder:

```
ecotype → clan → pod → matriline → individual
```

and give each level its own column or table. That is how the Southern Residents are
usually described, and it would make several queries trivial.

It is wrong for the register, because the ladder is not the same for every population.

## Decision

`rank` is an open list in `data/ranks.tsv`. Nothing in the schema requires a particular
sequence of ranks, a particular depth, or that every population use every rank. The
hierarchy is expressed entirely by `membership.tsv` edges.

## What this means for the data

Three facts drive this, and reviewers should check all three:

1. **Bigg's have no pods.** They have matrilines and an ecotype, and the structure above
   that is not organised the way resident society is. Any schema with a mandatory `pod`
   column has to lie about every Bigg's whale.

2. **"Clan" and "community" may or may not be useful ranks.** Both are in the seed data;
   see [open-questions.md](../docs/open-questions.md) Q1 and Q2. If moderators never tag
   at those levels, they should be dropped — a rank nobody uses is dead weight that
   still has to be maintained.

3. **The depth is not uniform even within an ecotype.** A Southern Resident individual
   whose matriline is not recorded can still be placed in a pod. `SSA:0000103` in the
   seed data is exactly this case: a membership edge straight to J pod, skipping the
   matriline level.

The general principle: **the register records what is known, at whatever level it is
known.** A fixed hierarchy forces curators to either invent intermediate groups they
have no evidence for, or leave the whole animal out.

## Implementation

- Ranks are rows in `ranks.tsv`, each with a definition file and an `applies_to` note.
- Adding a rank is a pull request against `ranks.tsv` plus a definition. No code change.
- Validation checks that every `rank` used in `entities.tsv` exists in `ranks.tsv`, and
  that every rank has a definition file that exists. It does **not** check that
  membership edges respect any ordering between ranks, because there is no canonical
  ordering to check against.

## Consequences

- A membership edge can skip levels, and consumers must not assume a fixed depth when
  walking ancestors.
- Nothing prevents a nonsensical edge (a pod inside a matriline). The register trusts
  curators here rather than encoding a structure that would need exceptions.
- Comparing across ecotypes is harder: "the group one level above the individual" means
  a matriline for Bigg's and possibly a matriline or a pod for residents. Consumers that
  want a consistent display level need their own rule.

## Alternatives considered

- **Fixed columns on `entities.tsv`** (`ecotype`, `pod`, `matriline`). Fast to query,
  denormalised, and it breaks on the first Bigg's whale and on every animal with partial
  information.
- **A closed rank enum with an ordering, and validation against it.** Would catch
  genuinely malformed edges. Rejected because defining the ordering requires answering
  Q1 and Q2 first, and because the exceptions look likely to outnumber the rule.
  Revisitable once the science questions settle.

## Open questions

- Should there be *any* structural validation of edges — even something weak, like
  "an individual may not contain anything"? That much seems safe and is not yet
  implemented.
