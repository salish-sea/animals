# ADR-0002: Opaque, permanent identifiers with an adjacent label

- **Status:** Proposed
- **Date:** 2026-07-27
- **Audience:** Scientific and informatics reviewers — the sections below are split, so each can read their half.

## Context

Every entity needs an identifier that other systems store. The obvious choice is a
readable slug: `pod-j`, `ecotype-srkw`, `matriline-t090`. It is what most projects do,
and it is what most projects later regret.

## Decision

Identifiers are `SSA:` followed by a zero-padded number: `SSA:0000020`. They carry no
meaning. The entity's preferred name lives in the adjacent `label` column of the same row
and may change freely without affecting identity.

What `label` is *for* — a preferred name, not a display string and not an integration key
— is [ADR-0011](0011-label-is-a-preferred-name.md). This record only relies on the fact
that it is mutable and that identity does not depend on it.

## What this means for the data

The number is not an accession number, a catalogue number, or anything a whale
researcher would recognise. It is deliberately arbitrary, and it exists so that the
*name* can change without breaking anything.

The reason matters here, because it is counter-intuitive: **a meaningful identifier
becomes a lie when the thing it describes changes.** If `matriline-t090` is stored in
five thousand OrcaSound records and that matriline is later found to be two matrilines,
or is renamed, the identifier now says something false — and correcting it means a
migration across every system that ever stored it. An arbitrary number cannot become
false, because it never claimed anything.

This is why Gene Ontology terms are `GO:0006915` rather than `apoptosis`, and it is a
large part of why annotations made in 1999 are still readable.

The cost is real: you cannot read `SSA:0000020` and know what it is. Which is why —

## Implementation

- **The `label` column sits immediately beside `entity_id` in every file where it
  helps.** A diff reads `SSA:0000101 individual  J35 …`, not a bare number. This is the
  standard mitigation and it is why opaque identifiers do not make review impossible.
  Note that diff readability is a *by-product* of the preferred name being there, not the
  reason the column exists — see [ADR-0011](0011-label-is-a-preferred-name.md).
- In `membership.tsv`, where both columns are identifiers, the `note` field carries the
  human reading. It is prose, not a field with semantics — though validation does make one
  best-effort keyword check against it, see
  [ADR-0005](0005-membership-is-genealogical.md).
- Numbers are assigned sequentially from blocks by kind, purely for legibility when
  scanning a file: `0000001+` ecotypes, `0000010+` communities and clans, `0000020+`
  pods, `0000030+` matrilines, `0000101+` individuals. **These blocks carry no
  semantics** and nothing may parse them. They exist so a human scanning the file has a
  rough sense of place, and they will run out, which is fine.
- Once an identifier appears in a merged commit it is permanent. See
  [ADR-0010](0010-identifiers-are-never-reused.md).

## Consequences

- Labels, spellings, and preferred names become cheap to change. `Transient` → `Bigg's`
  is a one-cell edit, not a migration.
- Consumers must join to display anything, so every consumer needs the register loaded,
  not just referenced.
- Debugging is harder. A log line with `SSA:0000104` in it requires a lookup.
- Nobody will ever type an identifier by hand, which means autocomplete is not a nicety
  — it is the only usable interface. It must read **both** `entities.tsv` (preferred
  names) and `names.tsv` (alternates); searching only the latter misses every preferred
  name, including `T090s`.

## Alternatives considered

- **Readable slugs (`pod:j`).** Rejected as above. Worth noting that they are also
  ambiguous in a way that bites early: `T090` is both an individual and the matriline
  named after her, so `matriline-t090` and `individual-t090` differ by a prefix that is
  easy to get wrong. See [ADR-0003](0003-one-identifier-space.md).
- **UUIDs.** Maximally safe, entirely unreadable, and 36 characters of noise in every
  diff. Sequential integers are just as opaque in the ways that matter and far kinder to
  a reviewer.
- **Reusing an upstream catalogue's identifiers (CWR's, finwave's).** Rejected: it makes
  our identity depend on theirs, breaks when two sources disagree, and would mean we
  cannot register an entity no upstream source has catalogued. Those identifiers are
  recorded as crosswalks in `mappings.tsv` instead.

## Open questions

- Is `SSA` free as a prefix? Not yet checked against Bioregistry — see
  [open-questions.md](../docs/open-questions.md) Q10.
- Zero-padding to 7 digits assumes fewer than 10 million entities. Obviously fine, but
  the padding width is a formatting decision that is annoying to change later.
