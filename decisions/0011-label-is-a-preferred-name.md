# ADR-0011: The label is a preferred name, not a display string

- **Status:** Proposed
- **Date:** 2026-07-27
- **Audience:** Scientific and informatics reviewers — the sections below are split, so each can read their half.

## Context

`entities.tsv` has a `label` column, and until now the repository has quietly used it
for three different jobs without saying which one was primary:

1. **A handle for maintaining this repository** — the thing that makes `SSA:0000030`
   legible in a pull request diff. This was the stated justification in
   [ADR-0002](0002-opaque-permanent-identifiers.md).
2. **A claim about the entity's canonical name** — implied by `names.tsv` being defined
   as holding "alternates only", which makes `label` the preferred one.
3. **A string to show a user** — implied by [walkthrough.md](../docs/walkthrough.md)
   and by the README.

These are not the same thing, and the third one is a mistake. A register cannot know
whether a consumer needs a dropdown entry, a map pin, a sentence fragment, a chart axis,
or twenty characters on a phone. No single string serves all of those, and a register
that pretends otherwise ends up holding another system's UI copy.

## Decision

**`label` is a preferred name** — the register's assertion of the canonical designation
for an entity, in the sense of SKOS `prefLabel`. It is **input to display, not display.**

Consumers compose their own presentation from `label`, `kind`, `rank`, `names.tsv`, and
membership context. OrcaSound deciding that its bout-tagging dropdown reads
`J17s — matriline, J pod` is entirely OrcaSound's business, and the register neither
supplies nor constrains that string.

## What this means for the data

The register's claim is *"the canonical designation for this entity is `J17s`"*. It is
not *"show `J17s`"*.

That distinction is why [Q13](../docs/open-questions.md) — whether matrilines should be
labelled `J17s` or `T090 matriline` — is a genuine editorial question for the scientific
reviewers rather than a UI preference. You are being asked what the community's canonical
written form is. What appears in a pick list is a separate question, and answering it is
not your job.

It also sets the bar for `names.tsv`: everything that is *a* name for the entity but not
*the* name goes there, typed as `common`, `historical`, or `hidden`.

## Implementation

`label` is explicitly **not**:

- **Not a display string.** See above. Consumers compose.
- **Not an integration key.** Nothing may join, match, or key on `label` — it is mutable
  by design, which is the entire point of [ADR-0002](0002-opaque-permanent-identifiers.md).
  Integrators key on `entity_id`, always.
- **Not localised.** `names.tsv` has a `language` column; `label` does not, so it is
  implicitly English. This is a real gap rather than a decision — see Open questions.
- **Not guaranteed unique.** Two entities may share a designation legitimately (a
  matriline and its matriarch, [ADR-0003](0003-one-identifier-space.md)). Anything that
  assumes uniqueness is wrong.

Diff readability — the original justification in ADR-0002 — survives as a *by-product*
rather than the definition. It is, however, the reason `label` lives in `entities.tsv`
next to the identifier rather than as another row in `names.tsv`: a preferred name
denormalised into the entity row is what makes the register reviewable by the people who
have to review it.

## Consequences

- **Labels are not unique, and that is now documented as expected rather than as a
  defect.** A matriline and its matriarch may legitimately share a designation, so bare
  labels collide. That is a fact about the data and the register owns it; what to display
  instead is presentation, and the next bullet applies to it like anything else.
- The register can stay silent on presentation questions it has no basis to answer:
  truncation, capitalisation in running prose, sort order, disambiguation. All consumer
  concerns.
- Changing a label is cheap and has no migration cost, because nothing keys on it. This
  only remains true if the "not an integration key" rule is actually honoured — if a
  consumer starts matching on labels, it silently stops being true.
- Two consumers may display the same entity differently. That is acceptable, and
  preferable to the register guessing.

## Alternatives considered

- **`label` holds the bare designation (`J17`, `J`), with a per-rank rendering pattern in
  `ranks.tsv`** (`"the {label}s"` for matrilines, `"{label} pod"` for pods). Arguably
  purer: the plural is derivable from designation + rank, so storing `J17s` stores a
  derived form. Rejected on three grounds — the derivation rules are per-rank and
  exception-prone, ecotype names (`Southern Resident`) aren't derivable at all, and a
  bare `J` as a pod label makes the file unreviewable. It also just relocates
  presentation logic into the register with extra steps.

- **`label` as an explicit display string**, with the register owning presentation.
  Rejected as the error this ADR exists to correct.

- **No `label` column at all**, with the preferred name living in `names.tsv` as
  `type = preferred`. Structurally cleanest and normalised. Rejected because it makes
  every diff in `entities.tsv` a wall of opaque identifiers, which defeats
  [ADR-0001](0001-tsv-in-git-as-source-of-truth.md)'s entire reason for existing.

## Open questions

- **Localisation.** `label` has no language dimension. If a Spanish-language vocabulary
  ever appears — which has been raised for humpback signal labels — the register has no
  way to express a preferred name per language. Adding a `language` column to `label`,
  or promoting preferred names into `names.tsv` with a language, are both possible. See
  [open-questions.md](../docs/open-questions.md) Q14.
- Should validation warn when a consumer-facing artefact in `dist/` is generated in a
  form that looks like a display string? Probably over-thinking it.
