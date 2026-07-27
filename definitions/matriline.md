# matriline

**Status:** working

## Working definition

A female and her surviving descendants, travelling as a unit. The most stable social
grouping in killer whale society, and the only rank in this register used by every
ecotype in scope.

## Source

Working definition, editors of this repository, 2026-07. Needs a citation and expert
confirmation.

## Scope notes

- Named for the matriarch, which means **the matriline and the whale it is named after
  share a label and are two different entities in the register**. J17 the matriline is
  `SSA:0000030`; J17 the whale is `SSA:0000105`. See
  [ADR-0003](../decisions/0003-one-identifier-space.md).
- Used for both residents and Bigg's.
- The plural form ("the T090s") is recorded as a `hidden` name so it resolves in
  autocomplete.

## What it is not

**Not the matriarch.** The distinction is invisible in speech and load-bearing in data:
the matriline outlives the whale, and "J17 was born in 1977" and "J17 travels with J pod"
are claims about different entities.

## Open questions

- Does a matriline persist as the same entity after the matriarch dies, or does it
  become a new group? This determines whether fission is a temporal change or a
  deprecation. See [membership.md](membership.md).
- How are Bigg's matrilines named when the matriarch is unidentified?
