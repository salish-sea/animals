# pod

**Status:** working (usable and in force, but not yet confirmed by a domain expert).

## Working definition

A stable set of related matrilines that travel together for most of the year and share
a substantial part of their call repertoire. Used for resident killer whales.

## Source

Working definition, editors of this repository, 2026-07. Needs a citation and expert
confirmation.

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

- Are L pod's subgroups stable enough to warrant register entities of their own?
- What does a moderator mean by "J pod" on a bout — the whole pod, or any member of it?
  The `signals-srkw` vocabulary uses the second reading. This register needs an answer
  because the reading decides what a membership edge asserts. If annotations elsewhere
  settle on a different one, that mismatch is worth knowing about — but it is not this
  file's to legislate.
