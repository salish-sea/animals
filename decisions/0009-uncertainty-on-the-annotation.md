# ADR-0009: Uncertainty belongs on the annotation, not in the vocabulary

- **Status:** Proposed
- **Date:** 2026-07-27
- **Audience:** Scientific and informatics reviewers — the sections below are split, so each can read their half.

## Context

A real OrcaSound bout is named:

```
SRKW signals at PT (J+K +L? pods)
```

The moderator is confident about J and K, and hedging about L. A controlled vocabulary
that offers only flat terms gives them two options, both bad:

1. Drop the hedge — silent data loss, and the register now asserts L pod was present.
2. Invent `L?` as a distinct term — the vocabulary now contains modality, and every
   consumer must know that `L?` and `L` are the same animals at different confidence.

Option 2 is the one that happens by default, and it compounds: `L?`, `L??`,
`probably-L`, and eventually a term list where half the entries are hedges.

## Decision

The register contains **entities only**. Confidence, hedging, and evidence are
properties of the *act of identification* and live on the annotation in the consuming
system.

An annotation carries at minimum:

| Column | Values |
|---|---|
| `entity_id` | An identifier from this register |
| `certainty` | `certain` \| `probable` \| `possible` |
| `evidence` | `moderator-acoustic` \| `photo-id-confirmed` \| `inferred-from-sighting` \| `automated-detector` |
| `asserted_by`, `asserted_at` | Who and when |
| `register_edition` | Which edition of this register they were reading |

There will never be an `L?` entity, an `unconfirmed` entity, or a `false-positive`
entity.

## What this means for the data

The `+L?` becomes a `possible` on the L pod row, and downstream consumers get to decide
what to do with it — SalishSea.io might render it differently, or drop it from a map
while keeping it in a search index. **That choice only exists because the hedge was
preserved rather than flattened.**

Two related patterns fall out of the same principle:

- **Compound terms are banned here, for the same reason.** A single label meaning "J and
  K" is the vocabulary encoding a *set*: it explodes combinatorially, and it still cannot
  express "J pod plus the T090s". Two annotations express that without either problem.
  The `signals-srkw` vocabulary does currently carry `JK`, `JL` and `JKL` — that is its
  own call, and it is noted here only because a moderator working across both will meet
  the two conventions side by side.

- **Negative claims are mostly not this register's problem, and saying so is the
  contribution.** The originating issue asked for `unconfirmed` and `false-positive` tags.
  In the live data those turn out to be three different things, only one of which touches
  the register:

  | Real bout | What it is | Where it belongs |
  |---|---|---|
  | `OrcaHello FP at Bush Point` | The detector fired on nothing | A bout-level flag in OrcaSound. Never a tag — it names no animal. |
  | `Passing boat noise`, category `biophony` | A wrong value in a field that already exists | Fix `bout.category`. Not a vocabulary question at all. |
  | `Mystery squeaks at Port Townsend` | There is a signal; nobody knows whose | Tag at the level you are sure of — which needs a `taxon` entity, and those now exist ([ADR-0008](0008-species-identity-is-delegated.md)). |

  The register's whole contribution is one warning to consumers: **a biophony bout may be
  about no animal at all, so the absence of tags must never be read as the absence of
  animals.** An unreviewed bout and a reviewed-and-empty bout are indistinguishable
  otherwise, which matters to anyone using the data ecologically.

## Implementation

- This ADR constrains **consumers**, not this repository — there is nothing to enforce
  here. It is recorded here because the vocabulary's shape depends on it: banning hedge
  terms is only defensible if the hedge has somewhere else to go.
- It does **not** make this repository the owner of annotation semantics. An earlier pass
  at the same problem, in the SalishSea.io catalogue, separates the asserter's confidence
  from the dataset's verification status — a distinction the table above collapses, and a
  real gap: a moderator's `possible` that a curator later confirms has nowhere to land.
  The earlier model is better on that point and this one should adopt it. See
  [Q18](../docs/open-questions.md).
- `certainty` is a three-value enum on purpose. A numeric probability implies a
  precision a listening moderator does not have.
- Validation rejects any entity label matching `\?$` or resembling a hedge, as a
  backstop.

## Consequences

- OrcaSound's tag join needs columns, so the originating issue's claim that this needs
  "only slug conventions and a moderator habit" is not quite right: a schema change is
  required. How large it is, and what it costs them, is theirs to say.
- **A certainty column is worth exactly as much as the affordance that fills it.** If
  recording a hedge is more work than omitting one, everything arrives as `certain` — and
  that is worse than free text, because it looks like data. This register carries the risk
  (it is why hedge terms are banned here, and why the hedge needs somewhere to go) but the
  interface that answers it is the consuming system's design, not ours.
- The register stays clean: every entity is an animal or a group of animals, always.

## Alternatives considered

- **Certainty as a separate parallel vocabulary** (`confidence:possible` as its own tag).
  Keeps the schema flat, but the confidence is then unattached to the term it qualifies
  — unusable on a bout with three animals at different confidence, which is exactly the
  case that prompted this.
- **Free text alongside structured tags, with no certainty column.** This is the status
  quo, and it does preserve the information — but only for a human reader.

## Open questions

- Is three certainty levels the right number, and are those the right three? Should be
  tested against how Scott actually hedges in existing bout names before being fixed.
- How are negative and absence claims recorded? Deliberately unanswered above.
