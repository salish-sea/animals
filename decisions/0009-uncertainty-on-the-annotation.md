# ADR-0009: Uncertainty belongs on the annotation, not in the vocabulary

- **Status:** Proposed
- **Date:** 2026-07-27
- **Audience:** Both — the sections below are split, so each reviewer can read their half.

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

- **Compound terms are also banned.** `signals-srkw` currently has `JK`, `JL`, `JKL` as
  single labels meaning "J and K", and so on. That is the vocabulary encoding a *set*.
  It explodes combinatorially, and it still cannot express "J pod plus the T090s". Apply
  two annotations instead.

- **Negative and absence claims need their own treatment.** "Not Bigg's" and "reviewed,
  nothing present" are not expressible as a tag, and absence of a tag must never be read
  as absence of the animal — an unreviewed bout and a reviewed-and-empty bout look
  identical otherwise. This matters if anyone ever uses the data ecologically. Not yet
  designed; flagged here so it is not solved accidentally with a term.

## Implementation

- This ADR constrains **consumers**, not this repository — there is nothing to enforce
  here. It lives here because both consumers need to implement it the same way, and this
  is the shared document.
- `certainty` is a three-value enum on purpose. A numeric probability implies a
  precision a listening moderator does not have.
- Validation rejects any entity label matching `\?$` or resembling a hedge, as a
  backstop.

## Consequences

- OrcaSound's tag join needs columns, so the originating issue's claim that this needs
  "only slug conventions and a moderator habit" is not quite right. A schema change is
  required, and it is small.
- Moderators need a certainty control in the UI. If it is awkward, they will not use it
  and everything will be recorded as `certain`, which is worse than free text. The
  control should default to `certain` and be one click away.
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
