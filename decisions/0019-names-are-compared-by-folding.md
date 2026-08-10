# ADR-0019: Names are compared by folding, never rewritten

- **Status:** Proposed
- **Date:** 2026-08-09
- **Audience:** Informatics reviewers — this is the matching rule every consumer
  implements, with published, executable test cases. Scientific reviewers — one clause is
  a domain judgement rather than typography: a plural designation names a matriline, not
  its matriarch, so the rule refuses to treat `T090s` and `T090` as the same string.

## Context

[C2](../docs/competency-questions.md) asks: a moderator typed `T090s` / `J-35` /
`Biggs` — which entity is that? It was marked answerable, but only by exact string match
against hand-enumerated rows in `names.tsv`, and for 649 Bigg's individuals with
inconsistent zero-padding (`T065A5` vs `T65A5`), hyphenation and apostrophes, enumerating
every spelling is unbounded. SalishSea.io already ships `normalize_designation()` in SQL
doing this; OrcaSound would need the same rule. Two implementations that disagree is
precisely the failure this register exists to prevent
([Q17](https://github.com/salish-sea/animals/issues/12)).

The word "normalization" smuggled in a second question: whether the register should
*rewrite* what it publishes. It should not, and the confusion between the two is what kept
Q17 open. What matching needs is a rule for when two spellings name the same entity. What
the register publishes — labels with their capitals, their zero-padding, their
apostrophes — is the canonical written form, and no rule here touches it.

## Decision

**The register publishes a comparison rule, called the fold.** To decide whether a typed
string names an entity, compare `fold(query)` against `fold(name)` for every published
name — `dist/searchable_name.tsv` is all of them in one place. Nothing stored or
displayed is ever rewritten: `T090` keeps its zero, `Bigg's` keeps its apostrophe.

The fold is exactly four steps, in order:

1. Lowercase.
2. Delete apostrophes (`'` U+0027, `’` U+2019) and hyphens (`-` U+002D).
3. Collapse each run of whitespace to a single space; trim the ends.
4. Replace each maximal run of digits with its decimal value — which drops leading
   zeros, and turns a run of only zeros into `0`.

And one refusal: **a trailing `s` never folds.** That is not typography. `T090s` names
the matriline and `T090` its matriarch — distinct entities by design
([ADR-0003](0003-one-identifier-space.md)) — and a fold that merges them answers C2 with
the wrong animal. Nothing is lost by refusing: the plural *is* the matriline's label, so
it already matches exactly.

**The test cases are published as [`dist/fold_test.tsv`](../dist/fold_test.tsv)**,
generated from the same table `bin/validate.py` tests itself against. A conforming
implementation reproduces the `folded` column from the `input` column, exactly. When the
rule ever gains a step, the cases gain rows in the same commit.

**And the guarantee that makes the rule safe to publish: folding may not merge what
exact spelling keeps apart.** The validator errors when two entities share a folded form
without sharing an identical raw string. That is the register's half of the bargain — a
consumer that implements the fold correctly can never resolve a spelling variant to an
entity that exact spelling would have kept distinct.

## What this means for the data

- **Exact ambiguity is allowed, and honest.** 126 bare designations name two entities
  today — `T090` is both a hidden name on the matriline (because catalogues write "the
  T090s" and "T090" for the family) and the label of the matriarch; `Gull` is both a
  nickname of T097 and the common name of Laridae. The fold does not create these and
  does not resolve them. C2's honest answer is sometimes *two candidates*, and an
  autocomplete shows both, distinguished by rank. Ambiguity the vocabulary actually has
  is surfaced, never adjudicated by string manipulation.
- **The enumeration burden Q17 complained about is gone.** Case, padding, hyphen and
  apostrophe variants need no rows. Hidden rows that only served matching (`Biggs`)
  remain valid and harmless — a plain-substring consumer still benefits — but no curator
  needs to add another.

## Implementation

- `fold()` lives in [`bin/validate.py`](../bin/validate.py) with its case table, and
  three checks run on every build: the function reproduces the published cases; no folded
  form merges entities that share no exact spelling; and the C2 trio resolves —
  `T090s` → `SSA:0000040`, `J-35` → `SSA:0000101`, `Biggs` → `SSA:0000002`, pinned to
  permanent identifiers ([ADR-0010](0010-identifiers-are-never-reused.md)) so the
  "answerable: yes" in competency-questions.md is a tested claim, not an asserted one.
- The rule is implementable in SQL (`lower`, `regexp_replace`), which is where
  SalishSea.io's `normalize_designation()` already lives.
- **What SalishSea.io changes when it reconciles** ([ADR-0012](0012-relationship-to-the-salishsea-io-catalogue.md)):
  its function *pads* (`T65A5` → `T065A5`) where the fold *strips* (`t65a5`). For case and
  zeros the two agree on every equivalence class, so no identification moves; the
  direction is all that differs, and stripping wins because it needs no field width —
  `J35` and `T065A5` pad differently, but they strip the same way. The one substantive
  change: its trailing-`s` handling must not survive into matching, for the
  matriline-vs-matriarch reason above.

## Consequences

- C2 stops being answerable-by-enumeration and becomes answerable-by-rule, and the
  acceptance test demanded by [competency-questions.md](../docs/competency-questions.md)
  ("each should eventually have a query in `bin/`") now exists for it.
- Consumers own their matching code but not the rule. Conformance is mechanical: run your
  implementation over `fold_test.tsv` and diff.
- A new alternate name can now collide with an existing entity's folded form. That is a
  build error at the pull request, which is the cheapest possible place to discover it —
  the curator decides whether the name is wrong or the ambiguity is real (in which case
  it must be exact, not fold-only).

## Alternatives considered

- **Normalize the stored labels.** Rejected: the label is the preferred written form
  ([ADR-0011](0011-label-is-a-preferred-name.md)), and the catalogues this register cites
  write `T090`, not `T90`.
- **Enumerate every spelling in `names.tsv`.** Unbounded — Q17's original complaint. Case
  × padding × hyphen × apostrophe multiplies; a rule handles the product for free.
- **Fold the trailing `s` too.** Rejected on data, not taste: it merges 126
  matriline/matriarch pairs that are distinct entities. This is the clause SalishSea.io's
  implementation gets wrong for the register's purposes.
- **Publish a folded-form → identifier lookup in `dist/`.** Rejected: a consumer must
  fold the *query* anyway, so the table cannot spare anyone the implementation; it would
  duplicate `searchable_name.tsv` under a second spelling and invite treating folded
  forms as identifiers, which they are not. The test cases are the artefact worth
  publishing.
- **Adopt SalishSea.io's padding direction.** Rejected as width-dependent (pad to what,
  for `J35`?). Same classes, simpler function.

## Open questions

- The fold deletes exactly three characters and no more. The day a query arrives with an
  en-dash for a hyphen, or a name carries a diacritic, the rule gains a step — decided
  then, with rows added to `fold_test.tsv` first, so the change is visible to every
  consumer as a diff.
