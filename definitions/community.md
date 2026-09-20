# community

**Status:** working (usable and in force, but not yet confirmed by a domain expert). Q1 settled that this rank is *not* redundant with ecotype.

## Working definition

The full set of resident killer whale pods that regularly associate with one another and
share a range, and which do not associate with other communities.

## Source

Working definition, editors of this repository, 2026-07. Needs expert confirmation.

## Scope notes

- The Southern Resident community comprises J, K and L pods.
- Applies to resident ecotypes. Bigg's social structure is not organised this way and
  this rank should not be used for them.

## What it is not

**Not the same as an ecotype.** A community sits *below* an ecotype: the resident
ecotype (`SSA:0000003`) contains the Northern Resident and Southern Resident communities,
among others. A community is defined by which pods associate with one another; an ecotype
by prey specialisation, genetics and morphology.

The register used to hold "Southern Resident" as an ecotype *and* "Southern Resident
community" as a community — one thing at two ranks, with the actual parent missing
entirely. [Q1](../docs/open-questions.md) settled it in favour of the strict reading:
`SSA:0000001` is deprecated to `SSA:0000010`, which is now labelled *Southern Resident*
and sits under the resident ecotype.

**Not a clan.** A community is defined by association, a clan by shared acoustic
repertoire. The Northern Resident community contains three clans; the Southern Resident
community contains one.

## Open questions

- ~~Does the register follow the strict convention (Resident ecotype containing a
  Southern Resident community) or the colloquial one (SRKW as an ecotype)?~~ **Answered
  by Q1: the strict convention.**
- Both ranks are kept, so what is the rule for which one a moderator picks? Q1 did not
  answer this, and it is now the live question: someone who means "the Southern Residents"
  should land on `SSA:0000010`, not on the resident ecotype above it.
