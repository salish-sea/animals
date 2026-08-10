# ADR-0020: Localised preferred names are `names.tsv` rows, added when they exist

- **Status:** Proposed
- **Date:** 2026-08-09
- **Audience:** Informatics reviewers — this settles a schema question by narrowing it,
  and defers the (additive) implementation until there is a row to hold. Scientific
  reviewers — one premise is yours to check: most of what this register calls a name is
  notation, not language.

## Context

[Q14](https://github.com/salish-sea/animals/issues/10) asked how preferred names are
localised. `names.tsv` has a `language` column; `entities.tsv.label` does not, and
[ADR-0011](0011-label-is-a-preferred-name.md) recorded the gap: "the preferred name is
implicitly English." The prompt was Spanish-language signal labels raised for a future
humpback vocabulary, with the same pressure assumed to apply here. The options on the
table were a language dimension on `label`, or moving preferred names into `names.tsv`
and accepting the hit to diff readability.

The premise overstates the gap. Of 668 entities, roughly 650 are labelled with
designations — `J35`, `T065A5`, `J17s` — which are notation, the same in every language.
Nicknames (`Tahlequah`, `Gull`) are proper names and mostly travel unchanged too. The
labels that are actually *in* a language are the handful of ecotypes, communities and
taxa: "Southern Resident", "Bigg's killer whale", the bird families. A language dimension
on `label` would be empty or meaningless for 97% of rows; the Spanish preferred name of
J35 is J35.

Two facts about where the demand really lives. The Spanish pressure attaches to signal
labels, which are the signals repository's vocabulary, not this one — nothing here is
waiting on it. The likelier localisation demand for *this* register is Coast Salish
names — qwe'lhol'mechen for the Southern Residents is the kind of name a partner would
reasonably want displayed — and `names.tsv` can record such names **today**, as
`type = common` with a language. The only thing Q14 actually gates is marking one of
them preferred.

## Decision

**`label` stays exactly as it is** — the canonical designation, language-neutral for
most entities, and the diff-readability handle. Both of its jobs are structural, and
neither gains anything from a language dimension.

**A localised preferred name, when one exists, is a `names.tsv` row**: `type =
preferred`, with the existing `language` column saying for whom. The dimension is
sparse by design — a row exists only where a genuinely language-bound preferred name
does. At most one `preferred` row per `(entity, language)`; never in the default
language, and never duplicating the label, because `label` *is* the preferred name
wherever no row says otherwise.

Display is a fallback, not a translation table: a consumer shows the `preferred` row in
the viewer's language if there is one, else `label`. As with everything under ADR-0011,
that is input to display — composition stays the consumer's.

## Implementation

**Nothing changes today.** The change is additive and waits for the first real row:

- `preferred` joins the `type` CHECK in `schema.sql`, with uniqueness on
  `(entity_id, language)` where `type = 'preferred'`.
- The existing validator rule that `names.tsv` never duplicates the label already covers
  the degenerate case.
- `searchable_name` and the fold ([ADR-0019](0019-names-are-compared-by-folding.md))
  need nothing: localised names flow into matching for free, exactly as `common` rows
  do now.

Deferring costs nothing precisely because the shape is decided: no existing row moves,
so there is no migration to get ahead of — which was the only urgency Q14 claimed.

## Consequences

- Q14 closes without schema churn, and without the diff-readability hit ADR-0011
  already rejected: `entities.tsv` is untouched, and preferred names stay beside their
  identifiers.
- Coast Salish and other localised names have a home *now* (`common` + language) and a
  stated promotion path when a community's preferred form is established.
- ADR-0011's "Not localised" caveat is discharged: `label` is not "implicitly English"
  but deliberately language-neutral, with localisation expressed beside it rather than
  inside it.
- [Q13](https://github.com/salish-sea/animals/issues/9) — the canonical written form
  for matrilines — is untouched; it is about what the label says, not what language it
  says it in.

## Alternatives considered

- **A `language` column on `label`.** Rejected: meaningless for the ~650 entities whose
  labels are notation, and it burdens the handle job — the column that makes a PR diff
  legible — with a dimension no diff reader needs.
- **Moving preferred names into `names.tsv` wholesale** (`type = preferred` for every
  entity). Structurally cleanest, and already rejected by ADR-0011 for making
  `entities.tsv` a wall of opaque identifiers. This ADR takes the narrow version: only
  the rows that carry information `label` cannot.
- **Per-language label columns** (`label_en`, `label_es`, …). Unbounded, and wrong for
  the same sparsity reason.

## Open questions

- Language tags are bare codes (`en`) today. If a Coast Salish name lands, the tag
  should be settled then — BCP 47 has codes for Lushootseed (`lut`) and other Salishan
  languages — with the choice recorded where `names.tsv` documents its columns.
