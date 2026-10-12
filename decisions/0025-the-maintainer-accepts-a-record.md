# ADR-0025: The maintainer accepts a record, and its Status line says whether a scientist has reviewed it

- **Status:** Accepted, 2026-10-12, by Peter Abrahamsen as maintainer. No scientific reviewer has reviewed it.
- **Date:** 2026-10-12
- **Audience:** Scientific reviewers — this changes what "Accepted" means: it no longer says that a scientist has agreed. Informatics reviewers — it changes the Status line every record carries.
- **Supersedes:** the section "How a record becomes Accepted" in [the decisions README](README.md), added 2026-07-27.

## Context

Since 2026-07-27 the rule has been that a record is Proposed when merged and becomes Accepted only when the reviewers its Audience line names have been asked and have had two weeks to object. Silence from reviewers nobody asked did not count.

Eleven weeks later, one record of 24 is Accepted ([ADR-0023](0023-southern-residents-from-noaas-census-file.md)). No other record was ever put to a scientific reviewer. The people CODEOWNERS names for that role have limited time, and the maintainer does not expect a review of 23 records to happen. Waiting longer will not change that.

So every other record reads Proposed, whether it describes how the register has worked for months (TSV files in git, [ADR-0001](0001-tsv-in-git-as-source-of-truth.md); dated releases, [ADR-0014](0014-a-publication-not-a-service.md)) or a choice still in doubt. A reader, or a consumer such as SalishSea.io deciding what it can rely on, cannot tell the two apart. The old rule meant to make that difference visible and ended up hiding it. It was written against failure mode 3 in [background.md](../docs/background.md), a change process too slow to use, and became an instance of it.

## Decision

- **A record is Proposed when merged**, as before.
- **It becomes Accepted when the maintainer accepts it**, by a commit that changes its Status line to "Accepted, *date*, by *name* as maintainer". The maintainer accepts a record once its content agrees with the data and with the other records.
- **A record whose Audience includes scientific reviewers says in its Status line whether one has reviewed it**: "No scientific reviewer has reviewed it" until one has, and who and when once one has, as ADR-0023's line already does.
- **Anyone can reopen an Accepted record by objecting**, in an issue or a pull request. A scientific reviewer's objection always reopens it. A reopened record goes back to Proposed, with a line naming the objection, until an amendment or a new record resolves it.
- **Questions that need a scientist stay where they are**: in each record's Open questions, and in [docs/open-questions.md](../docs/open-questions.md), which names who should answer each one.
- **Superseded records** keep their file and gain a pointer, as before.

This record does not change how definitions move from `working` to `agreed` ([definitions/README.md](../definitions/README.md)).

## Consequences

- "Accepted" now means the maintainer stands behind a record, not that the field has agreed to it. The Status line says which, so a reader does not have to guess.
- The other 23 records are accepted in the same change, after the corrections an audit on 2026-10-12 found (for example, [ADR-0021](0021-ssa-is-a-registered-prefix.md) said the prefix was registered, and [ADR-0004](0004-rank-is-an-open-vocabulary.md)'s example of a whale placed directly in a pod no longer was).
- What is given up: the old rule's pressure to ask the reviewers before calling anything settled. What is kept: a scientist's objection still reopens a record, and a review, once given, is recorded on the record it covers.

## Alternatives considered

- **Keep the rule, and accept only the records addressed to informatics reviewers alone** (0001, 0006, 0010, 0013, 0021). The maintainer can accept those under the old rule. It would leave 18 records Proposed indefinitely, which is the situation this record exists to end.
- **Announce all the records to Scott Veirs and Dave Bain at once and treat two weeks of silence as acceptance.** That counts silence from people who are not reading as agreement, which the old rule rightly refused to do.
