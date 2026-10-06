# ADR-0024: A matriline names its matriarch, in a table of its own

- **Status:** Proposed
- **Date:** 2026-10-06
- **Audience:** Scientific reviewers — this records which whale each matriline is named for, and it declines to name a male. Informatics reviewers — it adds a table, `data/matriarchs.tsv`, and four checks.

## Context

`J17s` and `J17` are two entities on purpose ([ADR-0003](0003-one-identifier-space.md)): the matriline outlives the whale. Nothing in the data said they were connected. The only link was that one label is the other plus `s`, and nothing may key on a label ([ADR-0011](0011-label-is-a-preferred-name.md)). That cost two things ([#48](https://github.com/salish-sea/animals/issues/48)):

- **A consumer keeps its own copy.** SalishSea.io stores the matriarch as `social_groups.anchor_individual_id`, and its [decision 051](https://github.com/salish-sea/salishsea-io/blob/main/docs/decisions/051-group-hierarchy-is-the-registers.md) lists it among the things that "stay ours, because the register does not hold them".
- **The rule both importers state could not be checked.** "Every female with a recorded calf heads a matriline, nested inside her mother's" ([ADR-0023](0023-southern-residents-from-noaas-census-file.md)) held when #47 merged, but the only way to confirm it was matching labels.

## Decision

**The register records which whale a matriline is named for, in `data/matriarchs.tsv`**, one row per matriline:

```
matriline_id  matriarch_id  source_id  note
SSA:0000030   SSA:0000105   NOAA-NWFSC          ← J17s is named for J17
```

**A table rather than a column on `entities.tsv`.** The column was the first idea and is the more obvious design. Two things decided against it:

1. **It would break a consumer on the next release.** SalishSea.io's loader checks each published file's header and refuses an edition whose columns have changed. A new file is ignored until that consumer chooses to read it.
2. **ADR-0016's argument applies unchanged.** Mothers are edges, not columns, so that each claim carries its own source and a correction is a one-row diff. A matriarch is the same kind of claim.

**Absent means not recorded**, as it does for parentage. Seven Bigg's lineages (`T002s`, `T012s`, `T049s`, `T086s`, `T121s`, `T168s`, `T221s`) are named for a founder the sheet has no row for, so they have no matriarch row.

**A male is never a matriarch.** 36 Bigg's "lineages" are named for a whale the sheet sexes male, and each holds that male and no one else. They exist because the Bigg's import gives every T-number a group ([ADR-0015](0015-bulk-import.md)). No matriarch is recorded for them. Whether they should be groups at all is a question about that import, and is left open here.

## What this means for the data

- 231 rows: 69 Southern Resident lines, every one named for a registered female, and 162 Bigg's lines. That is every registered namesake not sexed male. The 16 whose sex the sheet leaves blank are included.
- Nothing about who is in a matriline changes. The table names a line's matriarch; membership still says who belongs.
- It answers "which whale is this matriline named for?" and the reverse, without parsing a label. It does not answer whether a line outlives its matriarch, or what a line is called when its matriarch is unidentified. Both stay open in [definitions/matriline.md](../definitions/matriline.md). Recording "J17s is named for J17" is true whichever way they are answered.

## Implementation

`PRIMARY KEY (matriline_id)` and `UNIQUE (matriarch_id)`: one matriarch per line, one line per matriarch. The validator adds four checks:

| Check | Kind |
|---|---|
| The line is a group of rank `matriline`; the matriarch is an individual | error |
| The matriarch is not sexed `M` | error |
| The matriarch is a member of her own line | error |
| A recorded mother heads a line, and a daughter's line sits inside her mother's | warning |

The last is the importers' nesting rule. It is a warning because NOAA files some calves under a different founding lineage from their mother's, and the Southern Resident import places those in their pod on purpose.

Both importers write the rows: `bin/import_srkw.py` for every line it derives, and `bin/import_biggs.py` reading the matriarch off the designation, as it reads the lineage. Re-running either adds only rows not already present.

## Consequences

- SalishSea.io can read the matriarch from the register and drop `anchor_individual_id`, which is its decision to make.
- `entities.tsv` is unchanged, so no consumer's loader breaks.
- The 36 single-male Bigg's groups are counted and explained here and in `bin/import_biggs.py`, but the data does not mark them. In `matriarchs.tsv` they look the same as the seven lineages whose founder is unregistered: both simply have no row. Telling them apart takes the label, so if they are to be dealt with, it is by a change to the Bigg's import, not by reading this table.

## Alternatives considered

- **A `matriarch_id` column on `entities.tsv`.** Rejected above: it breaks a header-checking consumer, and it gives up per-claim provenance.
- **Declare the `label` + `s` convention supported.** Cheap, and exactly the label-keying ADR-0011 rules out. It would also break the first time a line is renamed and its matriarch is not.
- **Leave it.** Consumers keep deriving the link themselves, and the nesting rule stays unchecked.
