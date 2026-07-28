# ADR-0007: The register holds no observations

- **Status:** Proposed
- **Date:** 2026-07-27
- **Audience:** Both — the sections below are split, so each reviewer can read their half.

## Context

The pressure to add observation data will be constant and each individual request will
be reasonable. "Just record the last confirmed sighting date." "Just add which
hydrophones this pod is usually heard at." "Just note who they were travelling with."

Each addition is small. The cumulative effect is that the register becomes a third
sightings database — one that competes with its own upstream sources, drifts from them,
and has to be kept current from data it does not own.

## Decision

The register records **identity, membership, life status, names, and crosswalks**.
Nothing that is a property of an *encounter* — a time, a place, an observer, a
behaviour, a co-occurrence — belongs here.

## What this means for the data

The dividing line, stated so it can be applied without a judgement call:

> If the claim needs a date and a place to be meaningful, it is an occurrence and lives
> in the consuming systems.

Applied:

| Claim | Where |
|---|---|
| J35 exists and is a Southern Resident | Register |
| J35 is female, born ~1998 | Register |
| J50 is presumed dead as of Sept 2018 | Register — a life-status change, not an encounter |
| J pod was heard at Orcasound Lab on 2025-09-04 | OrcaSound |
| L87 was travelling with J pod in 2015 | OrcaSound / SalishSea.io |
| J35 was photographed near Lime Kiln | Neither — belongs to the photo-ID catalogue |

Life status is the edge case worth understanding: a death is dated, but it is a change
to the animal, not a record of an encounter. The date on which the animal was *last
seen* would be an occurrence, and is not recorded.

## Implementation

- No table has a location column, an observer column, or an encounter identifier.
- `status.tsv` is the only table with a real-world date, and it holds life status only —
  not "last seen".
- New columns proposed on any table should be tested against the rule above in review.

## Consequences

- The register stays small: hundreds of rows, not millions. It can be loaded whole by
  any consumer, which is what makes the no-API decision viable.
- It stays cheap to maintain. Roster changes happen on a census cadence, a few times a
  year, not continuously.
- Some questions become two-system joins. "Which bouts involved animals that were alive
  at the time" needs both the register and OrcaSound. Acceptable.
- Requests to add occurrence data will keep coming and will need to be refused
  repeatedly. That is what this ADR is for — so the refusal cites a decision rather than
  a preference.

## Alternatives considered

- **Allow "last confirmed sighting" only.** The most persuasive request, and the one
  most likely to be granted by accident. Rejected because keeping it accurate requires
  ingesting sightings continuously, which is the entire slope.
- **A separate `occurrences.tsv` in the same repository.** Keeps the boundary visible
  while allowing the data. Rejected: same maintenance burden, and it competes with
  SalishSea.io, which already does this properly.

## Open questions

- Humpback and pinniped identity may only be resolvable *through* occurrence context.
  If so, in-scope species may need a different treatment than orcas — see
  [open-questions.md](../docs/open-questions.md) O1.
