# matriline

**Status:** working (usable and in force, but not yet confirmed by a domain expert).

## Working definition

A female and her surviving descendants, travelling as a unit. The most stable social
grouping in killer whale society, and the only rank in this register used by every
ecotype in scope.

## Source

Working definition, editors of this repository, 2026-07. Needs a citation and expert
confirmation.

## Scope notes

- Named for the matriarch, which means **the matriline and the whale it is named after
  are two different entities in the register**. The matriline `J17s` is `SSA:0000030`;
  the whale `J17` is `SSA:0000105`. See
  [ADR-0003](../decisions/0003-one-identifier-space.md).
- **The register labels matrilines in the plural** — `J17s`, `T090s` — following ordinary
  community usage. The bare designation and the `<id> matriline` form are recorded as
  `hidden` names so either resolves in autocomplete.
- Used for both residents and Bigg's.

## What it is not

**Not the matriarch.** The distinction is invisible in speech and load-bearing in data:
the matriline outlives the whale, and "J17 was born in 1977" and "J17s travel with J pod"
are claims about different entities. The plural label makes this visible most of the
time, but the register does not depend on it — see ADR-0003.

## Open questions

- Does a matriline persist as the same entity after the matriarch dies, or does it
  become a new group? This determines whether fission is a temporal change or a
  deprecation. See [membership.md](membership.md).
- How are Bigg's matrilines named when the matriarch is unidentified?
- Is the plural the canonical written form, or does it read as informal where a
  catalogue would write "T090 matriline"? A question about the community's usage, not
  about UI — see [open-questions.md](../docs/open-questions.md) Q13.
