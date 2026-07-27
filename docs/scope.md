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

## What this repository is

A **register**: a list of the individual animals and the groups they belong to, each
with a permanent identifier, in the Salish Sea and adjacent waters.

It has three parts, deliberately kept separate:

| Part | Files | Changes when |
|---|---|---|
| The roster | `data/entities.tsv`, `membership.tsv`, `status.tsv`, `names.tsv` | An animal is born, dies, or is recatalogued |
| The definitions | `definitions/`, `data/ranks.tsv` | The community refines what a word means |
| The crosswalks | `data/mappings.tsv` | An external catalogue is linked or relinked |

## What this repository is *not*

These are hard boundaries, not "later" items. Each one, if crossed, turns the register
into a competing database that will drift from the sources it depends on.

- **Not a sightings or occurrence database.** Nothing here records that an animal was
  somewhere at a time. Occurrences live in OrcaSound and SalishSea.io and point *at*
  this register.
- **Not a photo-ID catalogue.** No images, no fin matching. We record that the Center
  for Whale Research says J35 exists; we do not duplicate their catalogue.
- **Not a replacement for CWR, MERS, DFO, or finwave.** Those are the authorities. This
  register mirrors the parts two named systems need and points back.
- **Not a health, genealogy, or life-history database.** Membership and life status
  only. Parentage is implied by matriline membership and not recorded separately.
- **Not the sound vocabulary.** Signal types (calls, whistles, clicks, S01–S42) live in
  [orcasound/signals-srkw](https://github.com/orcasound/signals-srkw). See "Relationship
  to signals-srkw" below.

## In scope, geographically and taxonomically

Marine mammals whose identity matters to a Salish Sea hydrophone moderator. In practice,
initially:

- *Orcinus orca* — Southern Residents and Bigg's, resolved to ecotype, pod, matriline
  and individual. Northern Residents and offshores are in scope but unpopulated.
- *Megaptera novaeangliae* (humpback) — individuals where a catalogue exists.
- Pinnipeds and other species at the species level only, via `taxon_id`, with no
  register entities of their own until someone needs them.

## Relationship to signals-srkw

The sound vocabulary is a separate repository with a different community of authorship,
and should stay separate.

One thing needs fixing between them. `signals-srkw/labels.md` currently *copies* the
ecotype and pod labels (`SRKW`, `J`, `K`, `L`, `JK`, `JKL`) into its own context-label
section. That is a fork of this register living inside the sound vocabulary, and the two
will drift. Those labels should become references to entity identifiers here.

Note also that `JK` and `JKL` encode a *set* as a single label. Multiple identifiers
should be applied instead — see [ADR-0009](../decisions/0009-uncertainty-on-the-annotation.md).

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
