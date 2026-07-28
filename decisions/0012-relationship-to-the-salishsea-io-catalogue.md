# ADR-0012: This register is authoritative; the SalishSea.io catalogue reconciles toward it

- **Status:** Proposed
- **Date:** 2026-07-27
- **Audience:** Scientific and informatics reviewers — the sections below are split, so each can read their half.

## Context

SalishSea.io already ships a marine-mammal catalogue in production: `individuals`,
`social_groups`, `designations`, `group_memberships`, `nicknames` and `parties`, seeded
from a 649-row Bigg's identification file, with public profile pages for individuals,
matrilines and ecotypes.

**Both are the work of the same author.** This is not two projects negotiating; it is one
person's quick first pass at the problem and their later, more deliberate one. The
catalogue was built without a design process; this register was designed without reference
to the catalogue. Neither is a counterparty to the other, and framing the reconciliation
as a negotiation would be a category error — the only real question is which model is
better, one piece at a time.

The two models disagree:

| Concept | This register | SalishSea.io |
|---|---|---|
| Ranks | ecotype, community, clan, pod, matriline | ecotype, clan, pod, matriline, `named_group` |
| Membership | Genealogical only ([ADR-0005](0005-membership-is-genealogical.md)) | `membership_basis` ∈ maternal, **association**, curated |
| Parentage | Out of scope ([ADR-0007](0007-no-observations.md)) | `mother_id` / `father_id`; **matrilines are derived from it** |
| Life status | alive, presumed_dead, dead, unknown | alive, deceased, presumed_deceased, unknown |
| Taxon | `NCBITaxon:9733` | `inaturalist.taxa` 41521 |
| Identity | Opaque `SSA:` identifiers | `primary_designation` (`T065A`), used in public URLs |

## Decision

**This register is the authority for animal identity in the Salish Sea, and the
SalishSea.io catalogue reconciles toward it.** The catalogue is a consumer, and its schema
is expected to migrate rather than to be crosswalked to indefinitely.

Recorded so the direction is not rediscovered or reversed by accident — the author holds
both repositories, so nothing external enforces it.

## What this means for the data

Where the two models differ, **this register's model wins on identity and membership**,
and the catalogue changes. But the differences are not simply errors to be deleted. Each
one exists because real data demanded it, and each is therefore a **finding this register
must answer** before the migration can happen:

- **`membership_basis = association`** exists because published catalogue rosters are
  associational. [ADR-0005](0005-membership-is-genealogical.md) declares membership
  genealogical without telling a curator what to do when the source roster disagrees.
  Unresolved — see [Q15](../docs/open-questions.md).
- **`mother_id`** exists because matrilines are *derived* from parentage rather than
  asserted by hand. This register claims parentage is "implied by matriline membership",
  which is false — a matriline spans generations, and membership implies descent from the
  matriarch, not from a mother. See [Q16](../docs/open-questions.md).
- **`normalize_designation()`** exists because 649 T-codes have inconsistent zero-padding
  (`T065A5` vs `T65A5`), hyphenation and plural forms. This register assumes exact string
  matching against hand-enumerated names. See [Q17](../docs/open-questions.md).
- **`named_group`** exists because real travelling groups have names and no rank
  ("Motley Crew"). This register's validator *requires* a rank on every group.
- **`identification_status` separate from evidence** exists because a moderator's
  confidence and a curator's later verification are different facts.
  [ADR-0009](0009-uncertainty-on-the-annotation.md) conflates them. See
  [Q18](../docs/open-questions.md).

Treating these as requirements rather than as divergence is the point of this record. A
model that cannot express what the earlier attempt already expresses is not more
considered; it is just younger. Where the earlier pass got something right, the win is to
notice and adopt it — not to defend the newer model.

## Implementation

- `salishsea-io` is **not** a row in `sources.tsv`, because it is not a source of
  authority. The upstream catalogues it derived its data from (the Bigg's nickname
  spreadsheet, and whatever MERS/finwave material fed it) belong there, and do not yet
  appear.
- The 649-row Bigg's file is a **seed candidate**, not a source. Importing it is
  [Q19](../docs/open-questions.md) — bulk import is not currently a supported operation,
  and the reviewable-diff premise of [ADR-0001](0001-tsv-in-git-as-source-of-truth.md)
  does not survive a several-thousand-row pull request without a stated exception.
- Migration direction is one-way. Until the catalogue migrates, crosswalk rows in
  `mappings.tsv` are the interim bridge, and they are expected to be temporary.
- The rights analysis in `salishsea-io/docs/rights-policy.md` (and its decision 004) is
  the same author's prior work on the same question, and it already covers the Bigg's
  nickname material specifically. [Q9](../docs/open-questions.md) was written as though
  from scratch; most of it is answered and should be ported, not re-asked.

## Consequences

- SalishSea.io absorbs migration cost — new identifiers, changed URLs (its public routes
  key on `primary_designation`, which its own schema marks as changeable via
  `designations.superseded_by`), and a rank-vocabulary reconciliation.
- Public URLs keyed on a designation are a live violation of
  [ADR-0011](0011-label-is-a-preferred-name.md)'s "nothing may key on a label". That rule
  is currently stated as a hypothetical risk; it is a present fact and the migration has
  to address it.
- This register acquires an obligation it did not have yesterday: it must be at least as
  expressive as the catalogue it is displacing. The five findings above are the bill.
- Being the authority means being maintained. This sharpens
  [Q8](../docs/open-questions.md) rather than answering it.

## Alternatives considered

- **Reframe this repository as a crosswalk and definitions layer over the SalishSea.io
  catalogue**, leaving identity where it already lives. Coherent, and cheaper in the
  short run. Rejected: the catalogue's modelling was a quick first pass, and the
  considered model should be the one that survives.
- **Two peer authorities with a maintained crosswalk.** Rejected — it is the outcome this
  record exists to prevent, and it is the expensive one.

## Open questions

- **Does this register count as an "upstream source" under SalishSea.io's decision 008?**
  That record establishes an anti-corruption layer: per-source schemas are verbatim
  mirrors, their semantics must never reach `public.*`, and native concepts are coined and
  translated at the boundary. Applied literally to this register, it reproduces exactly
  the divergence this ADR exists to prevent — a native catalogue with its own semantics
  beside the register.

  The argument that it does *not* apply: everything decision 008 defends against —
  undocumented fields, unstable vocabulary, no change process, no deprecation story — is
  the set of properties this register is being built to have. A governed publication with
  permanent identifiers and `replaced_by` semantics is structurally closer to that repo's
  `dwc` export contract than to a scraped API. That suggests a third category alongside
  mirrors and native domain: **shared contracts**, of which `dwc` is already one.

  This is a change to SalishSea.io's governing principle rather than a schema migration,
  and it is a prerequisite for the decision above rather than a consequence of it.

- What is the migration sequence, and does the catalogue migrate before or after the
  first OrcaSound bout is tagged? Tagging against identifiers that later change would
  defeat the purpose.
- **OrcaSound is the genuinely external party here** — a separate project with its own
  contributors — and this record says nothing about what it should do. Whether it has
  latent modelling that nobody has read is a live question; discovering one such
  repository is what prompted this ADR.
