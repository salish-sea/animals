# ADR-0028: Bigg's mothers are read off their designations, until a source states them

- **Status:** Proposed
- **Date:** 2026-11-25
- **Audience:** Scientific reviewers — this records 375 Bigg's mothers that no source states, on the strength of the naming convention. Informatics reviewers — it adds rows to `parentage.tsv` and nothing else; the Bigg's import writes them.
- **Amends:** [ADR-0016](0016-parentage.md), which says the Bigg's sheet supplies no parentage and leaves the Bigg's without any.

## Context

By convention, a Bigg's designation names a whale's mother: a calf's designation is its mother's with one letter or number added, so T065A5 is a calf of T065A, and T065A a calf of T065 ([matriline.md](../definitions/matriline.md): "a designation does encode maternal descent"). Bay Cetology assigns the designations. No one has checked the convention against a catalogue that states mothers, because no such catalogue is published.

[ADR-0016](0016-parentage.md) declined to read that chain. The sheet "supplies 510 individuals and no parentage at all", and the register would not make the inference itself. So the Bigg's have had no mothers, although the register already reads the same chain for their membership: the 73 nested sub-lineages (`T073As` inside `T073s`) are read off the designations ([ADR-0015](0015-bulk-import.md), [Q22](https://github.com/salish-sea/animals/issues/13)), and so is the matriarch of each line ([ADR-0024](0024-a-matriline-names-its-matriarch.md)).

That left a consumer holding a copy. SalishSea.io's catalogue has the same 375 mothers, worked out by the same rule when it was seeded, and its [decision 070](https://github.com/salish-sea/salishsea-io/blob/main/docs/decisions/070-southern-residents-are-generated-from-the-register.md) can't generate its Bigg's rows from the register until the register holds them.

No source we can cite states Bigg's mothers. Finwave, which Bay Cetology runs, shows none on a whale's page, and its January 2025 export of the Bigg's whales had no field for them. Whether its database holds them, and under what licence, is being asked (salishsea-io bd `salish-otnp`).

## Decision

**The register records each Bigg's whale's mother as its designation names her, with the sheet as the source and a note saying the mother was read off the designation.** [`bin/import_biggs.py`](../bin/import_biggs.py) writes them: a whale's mother is its designation with the last letter or number removed (`T065A5` → `T065A`, `T036B1A` → `T036B1`).

- **Only where the mother is a registered whale not sexed male.** A calf whose mother has no row in the sheet gets no mother: absent means "not recorded" (ADR-0016). A founder (`T065`) has none, since nothing precedes her designation.
- **The current designation decides, not a former one.** T122 was designated T46A until she was renamed on reappearing after 13 years. Her designation now names no mother, so none is recorded. Bay Cetology renaming her is its own statement, and the register follows it.
- **A designation the importer can't parse gets no mother.** Two letters in a row (`T073AB1`) could be read more than one way, so the importer claims nothing, as it already does for membership.
- **These rows give way to a source that states mothers.** When one is imported, a row it confirms takes that source, and a row it contradicts is corrected, with this record's rule named in the note. Neither the rule nor its rows are a second opinion against a real source.

The import wrote 375 mothers. They are exactly the 375 pairs in SalishSea.io's catalogue.

## Consequences

- **The check between parentage and membership proves nothing for the Bigg's.** ADR-0016 keeps the two asserted separately so each can catch the other's mistakes. For the Bigg's, both are now read off the same designation, so they agree by construction, and the validator's warning that a mother and calf are in different matrilines can't fire for them. A source that states either one is what restores the check.
- **A wrong designation is now also a wrong mother.** If Bay Cetology designated a calf under the wrong mother, the register says so twice, in the line and in the parentage. That was already true of the line, and the note on each row says where the claim comes from.
- **SalishSea.io can read Bigg's mothers from the register** and drop its own copy, as decision 070 plans.

## Alternatives considered

- **Keep the Bigg's without mothers until a source states them.** This is ADR-0016's position. It leaves the convention's claim in two places that disagree in what they say: the register's lines say T065A5 descends from T065A, and its parentage says nothing. Meanwhile, consumers keep a copy of the same inference. Rejected: the inference is made either way, and it is better made once, here, with its basis written on every row.
- **Record them under a source of their own, such as `EDITORS`, rather than `BIGGS-SHEET`.** The designations are the sheet's, and the rule is no more the editors' than the sub-lineage rule is. The note carries the distinction, as the matriarchs' notes do.
