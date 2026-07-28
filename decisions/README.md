# Decision records

One file per decision. Each records what was decided, why, and what was given up.
Superseded records are kept, marked `Superseded by ADR-NNNN`, never deleted — the
reasoning is the point, not the conclusion.

Every record carries an **Audience** line naming who needs to read it. The line spells
the audiences out rather than saying "both", so a record is legible on its own and so
that adding an audience later costs nothing but naming it.

Currently:

- **Scientific reviewers** — the decision changes what the data means. Needs domain
  expertise, not software judgement.
- **Informatics reviewers** — implementation only. Safe to skip if you're reviewing the
  science.

A record may name either, or both. Moderators who apply the vocabulary, and people
implementing a downstream consumer, are plausible future audiences; neither has a record
addressed to it yet.

**All records are currently `Proposed`.** Nothing has been ratified.

| # | Decision | Audience |
|---|---|---|
| [0001](0001-tsv-in-git-as-source-of-truth.md) | TSV files in git are the source of truth | Informatics reviewers |
| [0002](0002-opaque-permanent-identifiers.md) | Opaque, permanent identifiers with an adjacent label | Scientific + informatics |
| [0003](0003-one-identifier-space.md) | One identifier space for individuals and groups | Scientific + informatics |
| [0004](0004-rank-is-an-open-vocabulary.md) | Rank is an open vocabulary, not a fixed hierarchy | Scientific reviewers |
| [0005](0005-membership-is-genealogical.md) | Membership is genealogical; association is occurrence data | Scientific + informatics |
| [0006](0006-valid-time-in-data-assertion-time-in-git.md) | Valid time in the data, assertion time in git history | Informatics reviewers |
| [0007](0007-no-observations.md) | The register holds no observations | Scientific + informatics |
| [0008](0008-species-identity-is-delegated.md) | Species identity is delegated, not minted | Scientific + informatics |
| [0009](0009-uncertainty-on-the-annotation.md) | Uncertainty belongs on the annotation, not in the vocabulary | Scientific + informatics |
| [0010](0010-identifiers-are-never-reused.md) | Identifiers are never deleted or reused | Informatics reviewers |
| [0011](0011-label-is-a-preferred-name.md) | The label is a preferred name, not a display string | Scientific + informatics |

## Template

```markdown
# ADR-NNNN: Title

- **Status:** Proposed
- **Date:** YYYY-MM-DD
- **Audience:** <name each audience, followed by a short gloss of what that means
                for them — never "both", so the line stands on its own>

## Context
## Decision
## What this means for the data        (when scientific reviewers are an audience)
## Implementation                      (when informatics reviewers are an audience)
## Consequences
## Alternatives considered
## Open questions
```
