# matriline

**Status:** working (usable and in force, but not yet confirmed by a domain expert).

## Working definition

A female and her surviving descendants, travelling as a unit. The most stable social
grouping in killer whale society, and the only rank in this register used by every
ecotype in scope.

## Source

Working definition, editors of this repository, 2026-07. The term comes from Bigg et al.,
who first defined the group by travel and then showed from family trees that it is a line
of descent:

> an intra-pod group consists of a cohesive group of individuals within a subpod that
> always travels in close proximity. […] The genealogical trees indicate that intra-pod
> groups are matrilines. A matrilineal group typically comprises of 2-3 generations
> (range 1-4; mean=2.3) and a generalized matrilineal group consists of a grandmother,
> her adult son, her adult daughter and the offspring of her daughter.

— Bigg, M. A., P. F. Olesiuk, G. M. Ellis, J. K. B. Ford and K. C. Balcomb III (1990).
Social organization and genealogy of resident killer whales (*Orcinus orca*) in the
coastal waters of British Columbia and Washington State. *Reports of the International
Whaling Commission*, Special Issue 12: 383–405. [PDF, hosted by the Center for Whale
Research](https://whaleresearch.com/_files/ugd/760f65_1cc40ca4cba843ea9d2c47c0df5cbf62.pdf),
abstract. Needs expert confirmation.

## Scope notes

- Named for the matriarch, which means **the matriline and the whale it is named after
  are two different entities in the register**. The matriline `J17s` is `SSA:0000030`;
  the whale `J17` is `SSA:0000105`. See
  [ADR-0003](../decisions/0003-one-identifier-space.md). Which whale a line is named for
  is recorded in `data/matriarchs.tsv`, not left to the label
  ([ADR-0024](../decisions/0024-a-matriline-names-its-matriarch.md)).
- **The register labels matrilines in the plural** — `J17s`, `T090s` — following ordinary
  community usage. The bare designation and the `<id> matriline` form are recorded as
  `hidden` names so either resolves in autocomplete.
- Used for both residents and Bigg's.
- **Matrilines nest.** `T073As` is a member of `T073s`, and both have rank `matriline`.
  The register holds 73 such Bigg's sub-lineages, and they are **read off designations,
  not off parentage**: a letter-suffixed animal heads one when other registered animals are
  named after her (`T073A1` after `T073A`). By convention a designation does encode
  maternal descent, which is why this is a reasonable reading — but nobody has checked
  these against a catalogue, `parentage.tsv` does not hold the Bigg's, and two of the 73
  heads (`T064B1`, `T075C`) are not even sexed in the source. They were minted ahead of
  [Q22](https://github.com/salish-sea/animals/issues/13), which asks whether they are real
  groups. Record the narrowest one you are sure of.
- **Southern Resident matrilines nest by the same rule, read off parentage instead.**
  Every female NOAA's census names as a mother heads a matriline inside her mother's,
  unless NOAA files the two under different founding lineages:
  `J35s` is in `J17s`, which is in `J5s`. 69 of them, derived by
  [`bin/import_srkw.py`](../bin/import_srkw.py) under
  [ADR-0023](../decisions/0023-southern-residents-from-noaas-census-file.md). A female with
  no recorded mother heads a top-level matriline in her pod. Which of these the community
  would actually call a matriline is the same open question as Q22.
- **Those nested lines are finer than the published matrilineal group.** Bigg et al.'s
  group is a family that travels together, usually two or three generations. When a
  daughter's family starts travelling apart from her mother's, it becomes a new group.
  The register instead starts a line at every mother, whether or not her family travels
  apart. The Orca Behavior Institute's roster uses the published kind: it puts J62 in
  `J19s`, where the register has her in `J41s`, inside `J19s`. Recording the finer line is
  still true of the coarser one, so a consumer that wants the published kind can walk up
  the nesting. Which kind a `matriline` in this register should be is part of Q22.

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
