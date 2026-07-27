# Decision records

One file per decision. Each records what was decided, why, and what was given up.
Superseded records are kept, marked `Superseded by ADR-NNNN`, never deleted — the
reasoning is the point, not the conclusion.

Every record carries an **Audience** line:

- `Science` — the decision changes what the data means. Needs expert review.
- `Informatics` — implementation only. Safe to skip if you're reviewing the science.
- `Both` — sectioned, so each reviewer can read their half.

**All records are currently `Proposed`.** Nothing has been ratified.

| # | Decision | Audience |
|---|---|---|
| [0001](0001-tsv-in-git-as-source-of-truth.md) | TSV files in git are the source of truth | Informatics |
| [0002](0002-opaque-permanent-identifiers.md) | Opaque, permanent identifiers with an adjacent label | Both |
| [0003](0003-one-identifier-space.md) | One identifier space for individuals and groups | Both |
| [0004](0004-rank-is-an-open-vocabulary.md) | Rank is an open vocabulary, not a fixed hierarchy | Science |
| [0005](0005-membership-is-genealogical.md) | Membership is genealogical; association is occurrence data | Both |
| [0006](0006-valid-time-in-data-assertion-time-in-git.md) | Valid time in the data, assertion time in git history | Informatics |
| [0007](0007-no-observations.md) | The register holds no observations | Both |
| [0008](0008-species-identity-is-delegated.md) | Species identity is delegated, not minted | Both |
| [0009](0009-uncertainty-on-the-annotation.md) | Uncertainty belongs on the annotation, not in the vocabulary | Both |
| [0010](0010-identifiers-are-never-reused.md) | Identifiers are never deleted or reused | Informatics |

## Template

```markdown
# ADR-NNNN: Title

- **Status:** Proposed
- **Date:** YYYY-MM-DD
- **Audience:** Science | Informatics | Both

## Context
## Decision
## What this means for the data        (when Audience includes Science)
## Implementation                      (when Audience includes Informatics)
## Consequences
## Alternatives considered
## Open questions
```
