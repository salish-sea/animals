# ADR-0023: Southern Residents are imported from NOAA's census file

- **Status:** Proposed
- **Date:** 2026-09-29
- **Audience:** Scientific reviewers — this chooses the source for every Southern Resident animal and their mothers, and it states how its disagreements with other accounts are handled. Informatics reviewers — it adds a source, an import script and a refresh.

## Context

The register's Southern Residents are illustrative. There are five individuals (J17, J35, J50, J57, L87), two matrilines (J17s, L32s) and the three pods, all `SEED`, and `sources.tsv` says every `SEED` row "must be replaced or confirmed by a curator before first release". Some of them are already wrong: J17 is recorded as alive.

Consumers are waiting on this branch. SalishSea.io wants Southern Resident profile pages, and it reads animals only from this register ([its decision 051](https://github.com/salish-sea/salishsea-io/blob/main/docs/decisions/051-group-hierarchy-is-the-registers.md)). Bout tagging needs the whole tree ([ADR-0012](0012-relationship-to-the-salishsea-io-catalogue.md)).

The authority, the Center for Whale Research (CWR), publishes no open roster. Its ID guide is a paid or members-only PDF, and its site reserves reproduction rights. Our `CWR` source row reads `not-yet-requested`. A search for a public, reusable catalogue on 2026-09-29 found one candidate that is complete and current.

## Decision

**Southern Resident individuals, their mothers, sex and birth and death years are imported from `orca.csv` in NOAA Northwest Fisheries Science Center's [`noaa-nwfsc/srkw-status`](https://github.com/noaa-nwfsc/srkw-status), by a script under [ADR-0015](0015-bulk-import.md).** The first import pins commit `ba0b8c40e422aa9f5afcf845a0697b4d7d15701f` (2026-02-03). A new `sources.tsv` row, `NOAA-NWFSC`, stands behind every row it produces.

The file is the census table behind NOAA's population projections and 5-year status reviews. It has one row per whale catalogued since the census began, with `animal`, `birth`, `death`, `pod`, `matriline`, `mom` and `sexF1M2`. Births run through 2025. Every mother it names is itself a row in the file. Its README says the content is a U.S. government work, in the public domain in the United States (17 U.S.C. §105). It also carries a GPL-3 license, which covers the package's code and cannot attach to public-domain facts. salishsea-io's rights policy records this as [D-22](https://github.com/salish-sea/salishsea-io/blob/main/docs/rights-policy.md).

The judgements the script makes, which are what a reviewer should check:

1. **Parentage comes from `mom`**, as `mother` edges in `parentage.tsv` ([ADR-0016](0016-parentage.md)). The file names no fathers.
2. **Matrilines are derived from parentage, not read from `matriline`.** NOAA's `matriline` column names a founding lineage, which is coarser than a matriline here. For example, it files J35 under J9, while the register has her in J17s. The column is used as a check: a derived matriline that falls outside NOAA's founding lineage is flagged, not written. Which females anchor a matriline is itself a judgement the script must state. The Bigg's import met the same problem from the other side (Q22).
3. **`pod` becomes membership in the existing pod entities.** `J001`, `K001` and `L001` are NOAA's codes for J, K and L pods, not animals. They map to `SSA:0000020`–`22`.
4. **`sexF1M2` maps as 1 → `F`, 2 → `M`, and 0 → blank** (not known), not `U`, because the file does not say whether 0 means unknown or unrecorded.
5. **A death year becomes `presumed_dead`**, effective in that year. The file does not separate whales missing from the census from those found dead, and a disappearance is how most Southern Resident deaths are known. A `dead` status needs a second source naming a carcass or necropsy.
6. **Disagreements are kept, not settled.** Where NOAA and a published account differ, NOAA's value is written and the other claim goes in the row's `note` with its source. For example, NOAA gives K47's mother as K36, and the Puget Sound Institute (27 July 2026) gives K43. Settling it is curation, done later as its own change.
7. **The `SEED` identifiers are reused.** J17, J35, J50, J57 and L87 keep `SSA:0000101`–`105`, and J17s and L32s keep `SSA:0000030`–`31`. Their rows are rewritten with `source_id = NOAA-NWFSC`. Identifiers are permanent ([ADR-0010](0010-identifiers-are-never-reused.md)), and consumers already link to them. The Bigg's import reuses an identifier by label. Here the match has to go through the fold ([ADR-0019](0019-names-are-compared-by-folding.md)), because the `SEED` labels are unpadded (`J35`) and NOAA's are not (`J035`).

**Not from this file:** names. Nicknames stay `SEED` until a naming source is chosen, most likely The Whale Museum's naming facts on salishsea-io's D-21 terms, with Wikidata (CC0) as a crosswalk. Also missing are calves born after early 2026, which arrive with the next refresh.

## Why

It is the only complete, current and reusable roster found:

| Source | Coverage | Mothers | Current to | Reuse |
|---|---|---|---|---|
| NOAA `srkw-status` | every whale since the census began | nearly all post-1970 births | 2025 births | public domain |
| [Wikidata](https://www.wikidata.org/wiki/Q56143220) | a minority, few born after 2015 | under half | patchy | CC0 |
| [The Whale Museum](https://whalemuseum.org/collections/meet-the-whales) | named whales | in prose | current | all rights reserved |
| [Orca Network](https://orcanetwork.org/resources/srkw-births-and-deaths/) | births and deaths since 1990 | in prose | December 2025 | all rights reserved; misfiles J61, omits J60 |
| CWR ID guide | whole population | yes | 2025 | paid; reproduction needs consent |

Its data are CWR's own census observations, made under NOAA contract. So taking the file takes the authority's facts as the government has already published them. It does not route around CWR. CWR is credited as the observer in the `NOAA-NWFSC` row's note. Asking CWR is still worthwhile for what the file lacks (photos, guide content, confirmation of disputed mothers), and does not gate the import.

## Consequences

- Every Southern Resident becomes `NOAA-NWFSC`-sourced: unverified in ADR-0015's second sense, derived by a script, but from a government census rather than a community spreadsheet.
- The file lags the census by months. Refreshing it is a re-run against a new pinned commit, and it mints identifiers only for new designations. It needs a stated cadence, at least once after each annual census.
- Designations arrive zero-padded (`J035`). The Bigg's labels are padded too (`T090s`), so following that precedent relabels the `SEED` whales from `J35` to `J035`. The unpadded spelling survives as a name, and the two compare equal under the fold.
- Consumers that key on identifiers see the five `SEED` whales' facts change in place, and J17 becomes `presumed_dead`.

## Alternatives considered

- **Wait for CWR's permission and import its guide.** The permission has not been asked for, and the facts are already public.
- **Wikidata as the source.** CC0, but it is missing most recent calves and most mothers. It is the right crosswalk target (`skos:exactMatch` to Q-ids), not the roster.
- **Scraping The Whale Museum or Orca Network.** Both reserve all rights, and neither gives birth years and mothers as data.
- **Reading NOAA's `matriline` column as membership.** It is a founding lineage, not a matriline, so reading it would put J35 in J9s.

## Open questions

- Does NOAA's `death` year include whales presumed dead, or only confirmed deaths? The mapping in (5) is written to be safe either way.
- Which females anchor a derived matriline: every female with a surviving descendant, or only those the census names as matriarchs?
