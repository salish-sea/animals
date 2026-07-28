# ADR-0015: Bulk imports are reviewed as a transformation, not as rows

- **Status:** Proposed
- **Date:** 2026-07-28
- **Audience:** Scientific and informatics reviewers — the sections below are split, so each can read their half.

## Context

[ADR-0001](0001-tsv-in-git-as-source-of-truth.md) rests entirely on the reviewable diff:
a curator can see that a pull request changes one animal's birth year, which is why the
register is text in git rather than a database.

The first real use of the register is importing the Bigg's designation sheet — 510
individuals, 132 matrilines, and about 1,700 rows across four files. **Nobody reads that
in a pull request.** So either the premise gets a stated exception, or the register stays
empty, which is failure mode #2 in [background.md](../docs/background.md).

## Decision

**A bulk import is reviewed as a transformation.** The importing script is committed, and
*it* is the artefact that gets scrutinised; the rows it produces are its output.

Three conditions make that honest:

1. **The script is deterministic and idempotent.** Re-running it against an updated source
   mints identifiers only for genuinely new animals and appends no duplicates. Anyone can
   reproduce the output from the input.
2. **Every imported row carries its `source_id`**, so an import is distinguishable from
   curation forever, and revocable as a set.
3. **The script encodes every judgement it makes, in comments**, because those judgements
   are what a reviewer is actually checking.

## What this means for the data

The judgements in `bin/import_biggs.py` are the part worth a domain reviewer's attention.
None of them is obviously right:

- **Matrilines are derived from the designation prefix.** `T023`, `T023D`, `T023C3` are all
  placed in a group labelled `T023s`. The sheet itself groups differently — blank rows
  separate sub-blocks, and a "Known as the Motley Crew" heading spans several of them. See
  [Q22](../docs/open-questions.md).
- **"Known as …" headings become a `common` name on the derived matriline**, rather than a
  new rank. `Motley Crew`, `Secret Agents`, `Gretzky's`. This is the least confident
  decision in the import.
- **Birth years become EDTF.** `≤1966` → `../1966`; `<1969` → `../1968`, because "before
  1969" excludes it. Anything else containing a year becomes approximate (`1979~`) rather
  than being silently dropped.
- **A death with no date becomes `../2026-07`** — "no later than the sheet snapshot",
  which is exactly what the sheet tells us, rather than inventing a date.
- **`F?` becomes `U`**, with the original preserved in a note, because a hedge may not live
  in a field the schema treats as certain.
- **`T099B1?` is registered as `T099B1`** with a note. The sheet hedges the *designation*
  of a 2024 calf, not the animal's existence. Registering it and noting the provisionality
  is the design working as intended: when the designation firms up, the label changes and
  the identifier does not ([ADR-0011](0011-label-is-a-preferred-name.md)).

**Rights.** Per D-21 in `salishsea-io/docs/rights-policy.md` §7.1, the factual content is
uncopyrightable and freely usable. The "Story Behind the Nickname" column is creative prose
and **the script never reads it**. The sheet's maintainer is credited in `sources.tsv`, and
naming provenance rides on each nickname's note. D-21 also says the sheet is not to be
republished wholesale as a product — whether a release artefact of this register crosses
that line is [Q24](../docs/open-questions.md), and it is unresolved.

## Implementation

- Identifiers come from dedicated blocks — Bigg's matrilines from `SSA:0002000`,
  individuals from `SSA:0010000` — purely so the hand-written seed stays legible when
  scanning the file. Nothing may parse them ([ADR-0002](0002-opaque-permanent-identifiers.md)).
- Assignment is by sorted designation, and an identifier already assigned to a label is
  reused, so the mapping is stable across runs.
- The import is a normal pull request. The **diff of the script** is the review; the data
  diff is checked by CI and spot-checked by a human.
- An imported row is never edited by the script afterwards. Corrections are ordinary
  curation, and they change the row's `source_id` to reflect who now stands behind it.

## Consequences

- ADR-0001's premise is weakened in exactly one place, deliberately and visibly. Ordinary
  curation is still one reviewable row at a time.
- A bad transformation produces hundreds of bad rows. Two things limit the damage: the
  schema rejects malformed data at load ([ADR-0013](0013-distribution.md)), and
  `source_id` makes the whole import identifiable and reversible.
- The register goes from 20 rows to 661 in one commit, so from here on "read the whole
  file" stops being a review strategy.
- **Almost everything is now unverified in a second sense**: not `SEED`, but derived by a
  script from a community spreadsheet nobody has checked against a catalogue. That is a
  better starting point than empty, and it is not the same as curated.

## Alternatives considered

- **Hand-entering 510 animals.** Preserves the premise exactly and will not happen.
- **Importing individuals only, no derived groups.** Genuinely tempting, because the
  grouping is the least certain part. Rejected because tagging `Bigg's T090s` on a bout is
  the actual use case, and a register with no matrilines cannot serve it. The groups are
  marked as derived and Q22 asks for confirmation.
- **Treating the sheet as an upstream mirror**, kept verbatim in its own files and
  translated at read time. That is the anti-corruption pattern from salishsea-io's decision
  008, and it is the right shape for a source we do not control. Rejected here because the
  register *is* the curated layer — mirroring inside it would just defer the same
  judgements to every read.

## Open questions

- What happens when the sheet updates and a designation has *changed*? The script reuses
  identifiers by label, so a renamed animal would be minted as a new entity and the old one
  orphaned rather than deprecated. Reconciliation on update is not implemented.
- Should there be a `bin/` check that flags imported rows whose source row has since
  disappeared from the sheet?
