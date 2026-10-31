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
implementing a downstream consumer, are plausible future audiences. One record so far,
[ADR-0022](0022-taxonomic-hierarchy-is-ncbis-excerpted.md), also addresses anyone publishing
occurrences from the register.

## How a record becomes Accepted

[ADR-0025](0025-the-maintainer-accepts-a-record.md) sets the rule. It replaced, on
2026-10-12, the rule in force since 2026-07-27, under which a record became Accepted only
after the reviewers its Audience line names had been asked and had two weeks to object.

- A record is **Proposed** when merged.
- It becomes **Accepted** when the maintainer accepts it, by a commit that changes its
  Status line to "Accepted, *date*, by *name* as maintainer". The maintainer accepts a
  record once its content agrees with the data and with the other records.
- A record whose Audience includes scientific reviewers says in its Status line whether one
  has reviewed it: "No scientific reviewer has reviewed it" until one has, and who and when
  once one has.
- Anyone can reopen an Accepted record by objecting, in an issue or a pull request, and a
  scientific reviewer's objection always reopens it. A reopened record goes back to
  Proposed until an amendment or a new record resolves the objection.
- **Superseded** records keep their file and gain a pointer.

Definitions still follow their own rule, `working` → `agreed`, which ADR-0025 does not
change; see [definitions/README.md](../definitions/README.md).

**Every record is Accepted. Only ADR-0023 has been reviewed by a scientific reviewer**:
Scott Veirs approved it on 2026-10-06. The maintainer accepted the others on 2026-10-12,
after an audit corrected facts in them that had gone out of date. Each record addressed to
scientific reviewers says in its Status line that none has reviewed it.

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
| [0012](0012-relationship-to-the-salishsea-io-catalogue.md) | This register is authoritative; the SalishSea.io catalogue reconciles toward it | Scientific + informatics |
| [0013](0013-distribution.md) | The schema is the validation; releases carry the artefacts | Informatics reviewers |
| [0014](0014-a-publication-not-a-service.md) | The register is a publication, not a service | Scientific + informatics |
| [0015](0015-bulk-import.md) | Bulk imports are reviewed as a transformation, not as rows | Scientific + informatics |
| [0016](0016-parentage.md) | The register records parentage, as edges rather than columns | Scientific + informatics |
| [0017](0017-no-counts.md) | The register publishes no counts of animals | Scientific + informatics |
| [0018](0018-annotation-semantics-belong-to-consumers.md) | Annotation semantics belong to the consuming systems | Scientific + informatics |
| [0019](0019-names-are-compared-by-folding.md) | Names are compared by folding, never rewritten | Scientific + informatics |
| [0020](0020-localised-preferred-names-are-name-rows.md) | Localised preferred names are `names.tsv` rows, added when they exist | Scientific + informatics |
| [0021](0021-ssa-is-a-registered-prefix.md) | `SSA` is kept, and a Bioregistry prefix is requested (request superseded by 0026) | Informatics reviewers |
| [0022](0022-taxonomic-hierarchy-is-ncbis-excerpted.md) | The taxonomic hierarchy is NCBI's, excerpted by script — not curated here (amends 0008) | Informatics reviewers |
| [0023](0023-southern-residents-from-noaas-census-file.md) | Southern Residents are imported from NOAA NWFSC's public-domain census file (salishsea-io's D-22); matrilines derived from mothers, disagreements noted not settled, SEED identifiers reused (amends 0016 for Southern Residents) | Scientific + informatics |
| [0024](0024-a-matriline-names-its-matriarch.md) | A matriline names its matriarch, in a table of its own | Scientific + informatics |
| [0025](0025-the-maintainer-accepts-a-record.md) | The maintainer accepts a record, and its Status line says whether a scientist has reviewed it | Scientific + informatics |
| [0026](0026-identifiers-resolve-through-w3id.md) | An identifier's global form is a w3id.org address, and the Bioregistry request is withdrawn | Informatics reviewers |

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
