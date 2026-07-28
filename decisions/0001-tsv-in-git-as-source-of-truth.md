# ADR-0001: TSV files in git are the source of truth

- **Status:** Proposed
- **Date:** 2026-07-27
- **Audience:** Informatics reviewers — implementation detail. Safe to skip if you're reviewing the science.

> **Amended by [ADR-0013](0013-distribution.md).** This record argued "TSV versus a
> database" as if it were one decision. It is two — what we *edit and review*, and what we
> *ship* — and everything below concerns only the first. TSV in git remains the source of
> truth; the shipped artefacts are SQLite and generated TSV.

## Context

The register has to be edited by a small number of people, reviewed by a mix of
scientists and software engineers, consumed by at least two applications, and remain
readable in ten years. Candidate substrates: a database with an admin UI, an
OWL/RDF ontology, a Google Sheet, or plain files in version control.

## Decision

Tab-separated files in `data/`, in a git repository, are normative. Everything else —
JSON, closure tables, SKOS, any future API — is generated into `dist/` and never
hand-edited.

Tab-separated rather than comma-separated: `note` fields are prose and will contain
commas. Quoting rules are the single most common source of malformed CSV, and TSV with a
hard prohibition on tabs inside fields avoids the problem entirely rather than solving
it.

## Implementation

- One file per relation. No file has an embedded list, JSON blob, or delimiter-within-a-
  field.
- A literal tab may never appear in a field. `bin/validate.py` enforces this.
- `dist/` is committed so consumers can fetch a raw URL without a build step, and CI
  fails when it differs from a fresh build. Built in
  [ADR-0013](0013-distribution.md).
- Editing is by pull request. Provisional entries may be merged with
  `source_id = SEED`, which validation flags as unverified but does not reject — the
  escape hatch matters more than purity. See "Provisional entries" below.

## Consequences

- Review happens as a readable diff. This is the whole point: a curator can see that a
  pull request changes one animal's birth year, which is impossible with a database dump
  and hard with an OWL file.
- Git history becomes the audit log for free, which
  [ADR-0006](0006-valid-time-in-data-assertion-time-in-git.md) then depends on.
  **Consequence: history must never be rewritten** — no force-push to `main`, no rebase
  of merged work.
- Referential integrity is not enforced by the substrate, so it must be enforced by CI.
- Concurrent edits to the same file conflict textually. At this scale, acceptable.
- There is no query language. Consumers load the whole thing; it is small and will stay
  small.

### Provisional entries

A curator who needs an identifier *today* can open a pull request adding a row with
`source_id = SEED` and merge it without waiting for expert ratification. Validation
warns; nothing breaks. This exists because the most likely way this register fails is
that the process is slower than typing free text — see
[background.md](../docs/background.md).

## Alternatives considered

- **A database with an admin UI.** Better editing ergonomics, worse review, and it makes
  the register a service that has to stay up. Rejected on the "stay subordinate" logic
  in [background.md](../docs/background.md).
- **OWL/RDF as the source form.** Buys reasoning we don't need and costs us reviewers we
  do need. Generating SKOS into `dist/` gets the interoperability without the tax.
- **A Google Sheet.** Genuinely tempting — Scott already maintains community data this
  way, and the editing experience is better than a pull request. Rejected because there
  is no review-before-merge, no history that survives a bad paste, and no way to
  reference a specific version. Worth revisiting as an *input* path if pull requests
  prove to be a real barrier for curators.

## Open questions

- If pull requests turn out to be too high a barrier for scientific curators, what is
  the lighter-weight input path? (A form that opens a PR? A sheet that syncs one way?)
