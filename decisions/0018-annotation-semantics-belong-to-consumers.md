# ADR-0018: Annotation semantics belong to the consuming systems

- **Status:** Proposed
- **Date:** 2026-07-29
- **Audience:** Scientific and informatics reviewers — the sections below are split, so each can read their half.

## Context

This repository has said four times that it does not own annotation semantics.
[ADR-0009](0009-uncertainty-on-the-annotation.md) says the decision "constrains
**consumers**, not this repository" and does "**not** make this repository the owner of
annotation semantics". [Q5](../docs/open-questions.md) was declined on the grounds that
how an occurrence records what a moderator picked "is that consumer's annotation design".
[Q7](../docs/open-questions.md) was declined and its one surviving requirement handed to
"the annotation schema's, not the register's".

And yet: ADR-0009 carries a five-column table specifying an annotation, the
[walkthrough](../docs/walkthrough.md) renders four annotation rows with a header row of
column names, and [Q18](../docs/open-questions.md) is filed against this repository's
author as a piece of work to be done "before either system has data". A reader arriving
cold would reasonably conclude this is where the annotation shape is defined, because it
is the only place it is written down at any length.

The pull is structural rather than careless. The walkthrough's job is to trace one real
record end to end, and a trace has to pass through an annotation to reach a consumer. Its
findings are real and register-scoped — the register needs no location concept, `certainty`
and `evidence` are not register columns — but producing them required sketching the thing
being refused.

**There is a home, and it is not hypothetical.** SalishSea.io's decision
[013](https://github.com/salish-sea/salishsea-io/blob/main/docs/decisions/013-orcasound-acoustic-occurrences.md)
defines an acoustic occurrence as one curated biophony bout and states that identity
arrives as structured upstream tags rather than parsed prose. Underneath it,
`public.identifications` has shipped: one row per claim, with `evidence` (what the claim
rests on), `method` (how it was captured), `status` (`candidate` / `validated` /
`rejected`), `is_present` for absence claims, `asserted_by_party_id`, and a subject that
is exactly one of an individual or a social group. That is a working annotation model with
data in it. This register has a sketch with none.

## Decision

**This register owns identity. The consuming systems own annotation.**

Identity is which animals and groups exist, what they are called, what the words for them
mean, and how they nest. Annotation is what an occurrence is, and how a claim that
particular animals were present at one is recorded — its evidence, its method, its
confidence, its verification state, whether it asserts presence or absence.

The register makes exactly two claims on an annotation, and they are requirements rather
than schema:

1. **It cites a register identifier**, not a name — because a name is not identity
   ([ADR-0011](0011-label-is-a-preferred-name.md)).
2. **Anything derived from the register records the edition it was derived from**, so the
   derivation can be audited or rebuilt
   ([ADR-0013](0013-distribution.md), [ADR-0014](0014-a-publication-not-a-service.md)).
   Note this is deliberately *narrower* than "record the edition on every annotation",
   which is what an earlier draft of this record asked for. The claim itself needs no
   edition: under [ADR-0010](0010-identifiers-are-never-reused.md) an identifier's meaning
   never changes, so a stored identifier is already self-sufficient, and asking for the
   edition alongside it double-counts a guarantee the register has already made. What is
   genuinely edition-dependent is a *derived* fact — an ancestor, a closure, an index — and
   that is a property of the materialization, not of the moderator's claim.

How those two facts are spelled, and everything else about the row they sit in, is the
consuming system's design.

## What this means for the data

Nothing in `data/` changes, and no definition changes. What changes is what a reviewer
should read as normative here: the columns of an annotation are not, and never were.

One thing the register does still owe consumers, and it is a warning rather than a column:
**a biophony bout may be about no animal at all, so the absence of tags is not the absence
of animals.** An unreviewed record and a reviewed-and-empty record are indistinguishable
otherwise, which matters to anyone reading the data ecologically. That warning belongs
here because it is about how to read the register's silence.

## Implementation

- **ADR-0009 keeps its negative half and gives up its positive half.** Banning hedge terms
  from the vocabulary is a register decision and stands. The five-column table is now
  explicitly illustrative — it exists to show that the hedge has somewhere to go, which is
  what makes the ban defensible, and it points at the real model rather than competing
  with it.
- **The walkthrough's Step 2 is illustration.** It shows a plausible annotation so the
  trace can continue, marked as such.
- **[Q18](../docs/open-questions.md) is reduced to a pointer.** Its substance — carrying
  the confidence/verification split into a working shape, and allowing a signal to be
  recorded with no animal named — is work for SalishSea.io's decision record, filed there.
  It is not an open question about this register.
- Nothing in `dist/` or `schema.sql` is affected; the register has never emitted an
  annotation.

### Three divergences this makes visible, and whose they are

Naming them is the point of writing this down. Each is now the aggregator's to settle, and
none is a defect here:

- **`confidence` is a `REAL` there; ADR-0009 argued for a three-value enum**, on the
  grounds that a numeric probability implies a precision a listening moderator does not
  have. That argument is still worth making — but it is an argument to make in the
  aggregator's decision record, not a rule this repository gets to impose. Note the two may
  not even conflict: a CV match has a real score and a moderator does not.
- **`is_present` records absence.** ADR-0009 left "how are negative and absence claims
  recorded?" deliberately open. It is answered over there, and that answer should be
  adopted rather than re-derived.
- **A subject is required** — exactly one of an individual or a social group. So Q7's
  surviving requirement, that a signal be recordable with no animal named, is satisfied
  structurally rather than by a nullable column: it is an occurrence with zero
  identifications. Worth confirming that the interface actually permits that, because a
  form that demands a tag produces the same bad data as a schema that does.

## Consequences

- **This repository can no longer be cited as the specification for `certainty` or
  `evidence`.** Anything needing that specification cites SalishSea.io's decision record.
  If someone implements from ADR-0009's table, that is now a documentation bug here.
- **The walkthrough is weaker as a self-contained artefact.** A reader who wants the real
  annotation shape has to follow a link into another repository. Accepted: the alternative
  is two specifications by the same author that will drift, which is the exact failure
  [ADR-0012](0012-relationship-to-the-salishsea-io-catalogue.md) exists to prevent.
- **OrcaSound is external to both** and neither repository decides its schema. The most
  either can publish is a recommendation, in
  [orcasound/orcasite#1001](https://github.com/orcasound/orcasite/issues/1001). ADR-0012's
  closing open question already says this; this record does not change it.
- **ADR-0012's fifth finding is discharged by relocation rather than by answer.** "This
  register must be at least as expressive as the catalogue it is displacing" was the bill
  it accepted; on annotation semantics the bill is void, because the register is not
  displacing the catalogue there. It still stands on identity and membership.

## Alternatives considered

- **Keep owning annotation semantics here.** The register has no consumer, no annotation
  data, and no way to test a shape against a real interface. The aggregator has all three
  and has already shipped one. Ownership without the ability to be wrong in public is not
  ownership; it is speculation with a version number.
- **Move the walkthrough and the integration strategy to
  [`orgs/salish-sea/discussions`](https://github.com/orgs/salish-sea/discussions).**
  Rejected for the record, accepted for the argument. A discussion thread has no status
  field, no supersession, no `CODEOWNERS`, and no diff — the four properties
  [ADR-0001](0001-tsv-in-git-as-source-of-truth.md) and
  [ADR-0006](0006-valid-time-in-data-assertion-time-in-git.md) exist to secure. Moving the
  most contested design into the one medium with none of them inverts the thing that makes
  this repository reviewable. Discussions are the right venue for *reaching* a decision —
  particularly the domain questions addressed to reviewers who will never open a pull
  request — and the wrong venue for holding one.
- **A third repository for cross-cutting integration design.** A real option if the
  annotation shape had no owner. It has one, so a third repository would add a boundary
  without removing an ambiguity.

## Where the findings go

Relocating ownership does not stop this repository *generating* material the annotation
design needs — tracing a record, resolving a deprecation, or minting a new kind of entity
all turn up things a consumer has to know. That material accumulates in
[`salishsea-io/docs/design-notes/occurrence-identification-findings.md`](https://github.com/salish-sea/salishsea-io/blob/main/docs/design-notes/occurrence-identification-findings.md),
appended as things surface rather than held until a decision is ready.

It is a findings file, not a specification, and it lives on the consuming side on purpose:
notes kept here would re-become the thing this record exists to stop. Ten findings are in it
already. The one with a deadline is how a `split` deprecation reaches an identification that
was `validated` before the split — the existing status enum has no state for "the moderator
was right and the entity has since moved", and its values are locked.

The file has already earned its keep by contradicting this record: its first finding
asserted that an annotation needs the edition to stay interpretable, and working the cases
through showed ADR-0010 had already provided that. Requirement 2 above is the corrected
version.

## Open questions

- Q18's substance has to actually land in SalishSea.io's **decision** record — as an
  amendment to 013 or a successor. The findings file above is a holding place, not that;
  a note nobody has to act on is easier to keep than a decision. Filing it is this author's
  job wearing the other hat, which is precisely the kind of obligation that gets dropped.
- Does OrcaSound get a written recommendation, and from which repository? Two projects
  independently telling a third what its annotation schema should be is worse than one.
