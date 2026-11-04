# pod

**Status:** working (usable and in force, but not yet confirmed by a domain expert).

## Working definition

A stable set of related matrilines that travel together for most of the year and share
a substantial part of their call repertoire. Used for resident killer whales.

## Source

Working definition, editors of this repository, 2026-07. The published definition is
narrower, and is about travel alone:

> A pod was defined as the largest cohesive group of individuals within a community that
> travelled together for the majority of time (i.e. the largest group that travelled
> together for at least 50% of the time […]).

— Bigg, M. A., P. F. Olesiuk, G. M. Ellis, J. K. B. Ford and K. C. Balcomb III (1990).
Social organization and genealogy of resident killer whales (*Orcinus orca*) in the
coastal waters of British Columbia and Washington State. *Reports of the International
Whaling Commission*, Special Issue 12: 383–405. [PDF, hosted by the Center for Whale
Research](https://whaleresearch.com/_files/ugd/760f65_1cc40ca4cba843ea9d2c47c0df5cbf62.pdf),
section 3.2. The same paper found that a pod's members are related and share a dialect,
which is why this register's definition mentions both. It also names a level this register
does not hold: a *subpod*, "a group of individuals that temporarily fragments from its pod
to travel separately". Needs expert confirmation.

## Scope notes

- J, K and L pods are the Southern Resident pods.
- **Bigg's do not use this rank.** Any assumption that every orca has a pod will produce
  wrong or empty data for every Bigg's animal — this is one of the three cases driving
  [ADR-0004](../decisions/0004-rank-is-an-open-vocabulary.md).
- An individual whose matriline is unrecorded may be given a membership edge directly to
  a pod.

## What it is not

**Not a travelling unit on a given day.** Animals are heard in subsets and in mixed
groups. "J pod was heard" is an annotation about a bout; "J17 is in J pod" is a claim
about descent. See [membership.md](membership.md).

## Open questions

- Bigg et al. define a pod by who travels together; this register places a whale by
  descent ([membership.md](membership.md)). The two agree while whales stay with their
  families, and part where one doesn't, as L87 did for some 15 years. Is that a
  difference a curator needs a rule for? This is Q15
  ([#11](https://github.com/salish-sea/animals/issues/11)).
- Are L pod's subgroups stable enough to warrant register entities of their own?
- What does a moderator mean by "J pod" on a bout — the whole pod, or any member of it?
  The `signals-srkw` vocabulary uses the second reading. This register needs an answer
  because the reading decides what a membership edge asserts. If annotations elsewhere
  settle on a different one, that mismatch is worth knowing about — but it is not this
  file's to legislate.
