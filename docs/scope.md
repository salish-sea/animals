# Scope and intent

**Audience: everyone.** This is the document to disagree with first. If the scope is
wrong, nothing downstream can be right.

## The problem

Two systems need to say the same things about the same animals.

[OrcaSound](https://live.orcasound.net) records *bouts* — human-curated stretches of
hydrophone audio. A moderator listens, recognises what they hear, and types a name:
`J pod NB in Haro`, `Humpback mimics Bigg's?`, `SRKW signals at PT (J+K +L? pods)`.

[SalishSea.io](https://salishsea.io) maps marine-mammal occurrences and wants to show
those bouts alongside visual sightings.

Today the only way for the second system to learn what the first one heard is to
pattern-match the free-text name. That is fragile, lossy, and it throws away the part
that was expensive to produce: the moderator's judgement.

The fix is a shared, stable set of identifiers for the animals and groups both systems
talk about — and a small amount of agreement about what those identifiers mean.

**The goal is one roster where there are currently two and a half**: this register, the
catalogue inside SalishSea.io, and OrcaSound's free-text tags. The two consumers are not
alike, though. This repository and SalishSea.io are two interfaces onto the same data —
the data and the interactive interface — kept in separate repositories only because
curating a register by pull request and developing an application are such different
processes. OrcaSound is a genuinely separate project with its own audience and purpose,
organizationally adjacent, consuming a released artefact. See
[ADR-0012](../decisions/0012-relationship-to-the-salishsea-io-catalogue.md).

## What this repository is

A **register**: a list of the individual animals and the groups they belong to, each
with a permanent identifier, in the Salish Sea and adjacent waters.

It has three parts, deliberately kept separate:

| Part | Files | Changes when |
|---|---|---|
| The roster | `data/entities.tsv`, `membership.tsv`, `parentage.tsv`, `status.tsv`, `names.tsv` | An animal is born, dies, or is recatalogued |
| The definitions | `definitions/`, `data/ranks.tsv` | The community refines what a word means |
| The crosswalks | `data/mappings.tsv` | An external catalogue is linked or relinked |

## What this repository is *not*

These are hard boundaries, not "later" items. Each one, if crossed, turns the register
into a competing database that will drift from the sources it depends on.

- **Not a sightings or occurrence database.** Nothing here records that an animal was
  somewhere at a time. Occurrences live in OrcaSound and SalishSea.io and point *at*
  this register.
- **Not a record of what is *absent*.** A `biophony` bout may be about no animal at all —
  `OrcaHello FP at Bush Point` is a real one, and so is `Passing boat noise`. The register
  cannot express that and should not try. The warning consumers need is that **the absence
  of tags is not the absence of animals**: an unreviewed bout and a reviewed-and-empty
  bout look identical from here.
- **Not a photo-ID catalogue.** No images, no fin matching. We record that the Center
  for Whale Research says J35 exists; we do not duplicate their catalogue.
- **Not a replacement for CWR, MERS, DFO, or finwave.** Those are the upstream
  authorities. This register mirrors the parts two named systems need and points back.
  (SalishSea.io's own catalogue is *downstream*, not an authority — see below.)
- **Not a health or life-history database.** Membership, life status and parentage.
  Parentage is recorded because it is identity rather than encounter, and because it is
  *not* recoverable from membership: a matriline spans generations, so membership implies
  descent from the matriarch, not from a mother. See
  [ADR-0016](../decisions/0016-parentage.md). Health, condition and reproductive state
  stay out.
- **Not the sound vocabulary.** Signal types (calls, whistles, clicks, S01–S42) live in
  [orcasound/signals-srkw](https://github.com/orcasound/signals-srkw). See "Relationship
  to signals-srkw" below.

## In scope, geographically and taxonomically

Animals whose identity matters to a Salish Sea hydrophone moderator. Marine mammals
first — but a shore-mounted hydrophone also hears birds, and OrcaHello moderators
already tag them (orcahello#550, the Orcasound label dictionary), so soniferous birds
are in scope at taxon level. In practice, initially:

- *Orcinus orca* — Southern Residents and Bigg's, resolved to ecotype, pod, matriline
  and individual. Northern Residents and offshores are in scope but unpopulated.
- *Megaptera novaeangliae* (humpback) — individuals where a catalogue exists.
- Pinnipeds and other in-scope species as `kind = taxon` entities — taggable stand-ins
  for "an animal of this species, not resolved further", including an orca heard too
  faintly to place in an ecotype. See
  [ADR-0008](../decisions/0008-species-identity-is-delegated.md).
- Birds, as `kind = taxon` entities under the same delegation. The level follows what a
  moderator can actually hear: pigeon guillemot resolves to species; "gull" is the
  family; "bird" is the class *Aves*, the acoustic analogue of the unplaceable orca.
  No individuals, no groups — birds get no register-side structure unless tagging
  practice demands it.

## Relationship to the SalishSea.io catalogue

SalishSea.io already ships a marine-mammal catalogue in production — individuals, social
groups, designations, memberships and nicknames, seeded from a 649-row Bigg's file, with
public profile pages. This register was designed without reference to it.

**This register is authoritative for animal identity; that catalogue reconciles toward
it.** It is a consumer with an existing schema to migrate, not a peer authority. See
[ADR-0012](../decisions/0012-relationship-to-the-salishsea-io-catalogue.md).

The differences are not simply errors, though. Each exists because real data demanded it
— associational rosters, parentage-derived matrilines, designation normalization, named
groups with no rank — and each is a requirement this register must meet before the
migration is possible. They are tracked as Q15–Q19; parentage is answered by
[ADR-0016](../decisions/0016-parentage.md), and the rest remain open.

## Relationship to signals-srkw

The sound vocabulary is a separate repository with a different community of authorship,
and should stay separate.

There is one place the two touch. `signals-srkw/labels.md` currently *copies* the ecotype
and pod labels (`SRKW`, `J`, `K`, `L`, `JK`, `JKL`) into its own context-label section.
That is a second copy of this register's labels, and two copies drift — which is the
failure this register exists to prevent. Referencing entity identifiers would close it.
Whether to do that, and when, belongs to that repository; what this register can do is
make identifiers stable enough to be worth referencing, and say plainly that the copy
exists.

Note also that `JK` and `JKL` encode a *set* as a single label, which this register will
not do — see [ADR-0009](../decisions/0009-uncertainty-on-the-annotation.md) for the
reasoning. If the two vocabularies ever do converge, that is **migration work, not
prevention**: `JKL at Sunset Bay` and `JKL calls fall S25E2 day 2` are live bout names
today.

## Success criteria

This effort has worked if, in a year:

1. A moderator tagging a bout picks from this register and rarely needs free text.
2. SalishSea.io ingests OrcaSound bouts without parsing a single name string.
3. When an animal dies or a matriline splits, one edit here propagates to both systems.
4. Someone outside either project can read the register and understand it.

It has failed if the register goes stale, or if moderators route around it. Both
failures are more likely than a modelling error, and
[docs/background.md](background.md) is about why.

## Status

Everything here is **proposed**. No decision in `decisions/` has been ratified, no row
in `data/` is verified, and the identifier prefix is not yet registered. See
[docs/open-questions.md](open-questions.md).
