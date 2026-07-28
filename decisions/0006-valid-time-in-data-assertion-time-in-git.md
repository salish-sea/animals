# ADR-0006: Valid time in the data, assertion time in git history

- **Status:** Proposed
- **Date:** 2026-07-27
- **Audience:** Informatics — implementation detail. Safe to skip if you're reviewing the science.

## Context

Two different clocks run through this data and conflating them is the classic way to
make a register unable to answer either kind of question.

- **Valid time** — when something was true in the world. J50 died in September 2018.
- **Assertion time** — when someone recorded it. The Center for Whale Research declared
  her deceased some days later.

Systems that model neither cannot reproduce a historical view. Systems that model both
in the schema (full bitemporality) are notoriously heavy for the value delivered.

## Decision

Split by the *kind* of change:

- **Things that genuinely change in the world** — an animal dies, a matriline splits,
  a Bigg's whale disperses — get explicit valid-time columns in the data
  (`status.effective`, `membership.start`/`end`), and are recorded as new rows, never
  by editing an existing one.

- **Things that were always true and we simply had wrong** — a misassigned sex, a
  refined birth year, a corrected label — are plain columns, edited in place. **Git
  history is the assertion-time axis.**

`status.tsv` additionally carries `asserted_on`, for when the *upstream source* made the
claim — which is distinct from both of the above, and is the only one of the three that
git cannot recover.

## Implementation

- `git log -L` over a row range gives "when did we come to believe this" for any field,
  with the pull request providing the reasoning. That is a complete assertion-time audit
  trail for zero schema cost.
- **This makes ADR-0001's no-rewrite rule load-bearing.** Force-pushing `main` or
  rebasing merged history destroys the assertion-time axis irrecoverably. Branch
  protection is not a nicety here.
- `status.tsv` is append-only. A correction to a status claim is a new row, not an edit;
  validation rejects deletions of existing status rows in a diff.
- Three timestamps end up available for a status claim: `effective` (world),
  `asserted_on` (source), and the commit date (us). That is the full picture and only
  two of them cost a column.

## Consequences

- "What did the register say on date D" is `git checkout` at date D — exact, and free.
- "What did identifier X mean when this bout was tagged" is answerable, which is why
  consumers record `register_edition` on each annotation.
- Querying history means shelling out to git rather than issuing a query. Acceptable —
  it is a rare, offline operation, not something a page render does.
- Anyone who clones without full history loses the assertion-time axis. Shallow clones
  are fine for consumers reading current state, not for auditing.
- If the register ever migrates off git, this axis has to be materialised first. Worth
  remembering before any such migration, not after.

## Alternatives considered

- **Full bitemporality in the schema** — `valid_from`, `valid_to`, `recorded_from`,
  `recorded_to` on every table. Correct, complete, and roughly doubles the width of
  every file for a register that a handful of people will edit a few times a month.
  Rejected on cost.
- **No temporal modelling at all**, deriving everything from the current state. Cannot
  answer "who was alive in 2017", which is competency question C4, asked by a real
  consumer.
- **An `updated_at` column.** The worst of both: costs a column, records less than git
  already does, and goes stale whenever someone forgets to touch it.

## Open questions

- Should `dist/` artefacts embed the commit SHA they were built from? Probably yes —
  it makes an exported snapshot self-describing and costs one line.
