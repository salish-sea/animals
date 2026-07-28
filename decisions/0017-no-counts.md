# ADR-0017: The register publishes no counts of animals

- **Status:** Proposed
- **Date:** 2026-07-28
- **Audience:** Scientific reviewers — this refuses a number people will ask for, and the reasons are ones you can check. Informatics reviewers — it is a rule about what may be generated into `dist/`.

## Context

A count of a group's living members is derivable from what is already here: join
`membership` to `current_status` and count. It costs nothing to generate, a public-facing
display wants it (O5 in [competency-questions.md](../docs/competency-questions.md)), and
"it is free, so why not" is the natural answer.

[Q6](../docs/open-questions.md) asked it properly: derive it, publish it, or refuse?

## Decision

**The register publishes no count of animals.** Not as a column, not as a view in
`dist/`, not in prose in this repository.

Four reasons, in order of how much they matter:

1. **The roster is knowingly incomplete, so a count is not stale — it is wrong, with no
   error bar.** Northern Residents and offshores are in scope and unpopulated
   ([scope.md](../docs/scope.md)); the Bigg's import is 510 rows nobody has verified. A
   count reads the register's silence as data, which is the failure
   [ADR-0009](0009-uncertainty-on-the-annotation.md) already names in the other
   direction: the absence of tags is not the absence of animals, and the absence of a row
   is not the absence of an animal.

2. **The derivable count is not the count a reader would think they were getting.**
   [ADR-0005](0005-membership-is-genealogical.md) makes membership genealogical, so a
   matriline's count is a count of *descent*. Asked "how many animals are in J pod",
   almost everyone means the travelling group — which this register deliberately cannot
   answer. A number published under a label that invites the wrong reading is worse than
   no number.

3. **CWR publishes the census, and this register is not a replacement for it**
   (scope.md). An SRKW population figure is quoted, consequential, and occasionally
   political. A second figure, differing because a birth has not yet been ingested, sets
   the register against the source it depends on. That drift is the specific failure the
   scope boundaries exist to prevent.

4. **Staleness between editions is a design property**
   ([ADR-0014](0014-a-publication-not-a-service.md)). That is tolerable for identity,
   which changes rarely and visibly. It is not tolerable for a number that will be read
   as current.

**Derivability is not publication.** A consumer that needs a count can compute one and
own the claim — with its own caveats, its own currency, and its own name on it. This is
the pattern [ADR-0011](0011-label-is-a-preferred-name.md) already sets: the register
stays silent on questions it has no basis to answer.

## What this does not cover

`dist/structure.md` reports how many entities exist at each rank, and will continue to.
That is not a count of animals — it is a diagnostic about the register's own shape, which
is what makes a break in the graph visible at a glance.

The distinction is the subject of the sentence:

| Claim | Subject | Allowed |
|---|---|---|
| "134 matriline entities are recorded here" | the register | Yes |
| "J pod has 25 members" | the world | No |
| "3 individuals in this file are unreachable from any taxon" | the register | Yes |

A consumer computing a count from the published data is doing nothing wrong. This ADR
binds what *this repository* asserts.

## Consequences

- O5 stops being an open modelling question and becomes a refusal with a reason.
- ADR-0005's instruction that a published count "must be labelled as such" is superseded
  in part: there is no published count to label. The guidance survives as advice to
  consumers, who now own the labelling problem along with the number.
- **The request will recur**, and each instance will be reasonable — a dashboard tile, a
  profile page, a README line. As with [ADR-0007](0007-no-observations.md), the value of
  writing this down is that the refusal cites a decision rather than a preference.
- Nothing in `bin/` or `schema.sql` changes today. This is a rule about what may be added,
  and it is cheapest to state before something is added.

## Alternatives considered

- **Publish the count with a caveat.** Rejected: caveats do not survive quotation. The
  number gets lifted into a headline, a slide or a dashboard tile, and the caveat stays
  behind.
- **Publish a count only for groups whose roster is verified complete.** Coherent, and the
  right shape if this is ever revisited. Rejected now because no group clears that bar —
  every row is `SEED` or an unverified import.
- **Say nothing and let consumers derive it.** That is the decision. The ADR exists so the
  refusal is citable rather than re-argued.

## Open questions

- The objection here is empirical, not principled: reasons 1 and 4 would weaken
  considerably if a population's roster were ever complete and verified against the
  census. **What would make one count as complete enough to revisit this?** That is a
  question for the scientific reviewers, and it is the precondition for reopening.
