# ADR-0010: Identifiers are never deleted or reused

- **Status:** Proposed
- **Date:** 2026-07-27
- **Audience:** Informatics reviewers — implementation detail. Safe to skip if you're reviewing the science.

## Context

Once an identifier is stored by an external system, deleting it breaks that system
silently — the reference resolves to nothing, or worse, to whatever was assigned the
number next. Catalogues do change: two entries turn out to be the same animal, a
matriline is found to be two, an entry was a mistake.

## Decision

An identifier that has appeared in a merged commit is permanent. Entities are
**deprecated**, never removed, and never reassigned to a different entity.

Deprecation records one of two pointers, following OBO Foundry practice:

- **`replaced_by`** — exactly one successor, unambiguously the same thing. A consumer
  may substitute automatically.
- **`consider`** — one or more candidates requiring human judgement. A consumer must
  **not** substitute automatically.

## Implementation

`data/deprecations.tsv`:

| Column | Meaning |
|---|---|
| `entity_id` | The deprecated identifier |
| `reason` | `merged` \| `split` \| `erroneous` \| `renamed` |
| `replaced_by` | Single identifier, or empty |
| `consider` | Space-separated identifiers, or empty |
| `date`, `source_id`, `note` | Provenance |

Validation enforces:

- Exactly one of `replaced_by` / `consider` is populated.
- Every referenced identifier exists in `entities.tsv`.
- A deprecated identifier is never itself a `replaced_by` or `consider` target, so a
  successor is always live and a consumer never has to chase a chain.
- No identifier present in git history is ever absent from `entities.tsv` — removal is
  never permitted, with or without a deprecation row. Enforced in CI rather than in
  `bin/validate.py`, and only against the pull-request base, so branch protection is what
  actually makes this hold.

Deprecated entities **stay in `entities.tsv`** and keep resolving to a label. They are
excluded from autocomplete and from new annotations, but a 2025 record referencing one
still renders.

## Consequences

- Every stored reference stays resolvable indefinitely. This is the property that makes
  twenty-year-old Gene Ontology annotations still readable, and it is worth the file
  growth.
- Consumers can migrate deprecations mechanically for `replaced_by` and queue the rest.
  This split is the practical difference between a deprecation costing an afternoon and
  costing a curator a month.
- `entities.tsv` accumulates rows that are no longer current. At this scale, irrelevant.
- Mistakes are permanent in the sense that the identifier is burned. Minting a fresh
  number costs nothing, so this is not a real cost.

## Alternatives considered

- **Deleting erroneous entries** that were never published. Tempting, and safe *if* you
  can be certain nothing consumed them — which you cannot, once the repository is
  public and consumers can pin any commit. Not worth the exception.
- **A single `replaced_by` with a confidence value** instead of two columns. Loses the
  bright line between "safe to automate" and "needs a human", which is the entire value
  of the pattern.

## Open questions

- Should deprecated entities be dropped from `dist/` artefacts, or included with a flag?
  Including them is more useful and slightly larger. Leaning include.
