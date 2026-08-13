# ADR-0021: `SSA` is kept, and claimed as a Bioregistry prefix

- **Status:** Proposed
- **Date:** 2026-08-13
- **Audience:** Informatics reviewers — this settles a naming question with a registry
  check and a registration; nothing about the data changes.

## Context

[ADR-0002](0002-opaque-permanent-identifiers.md) chose `SSA:` for "Salish Sea Animals" and
admitted in its own open questions that the prefix had never been checked against
[Bioregistry](https://bioregistry.io/) or anywhere else. Q10 ([#7](https://github.com/salish-sea/animals/issues/7))
held that gap open, and stated its own deadline: *cheap to change now, expensive after the
first external system stores one.*

That moment has arrived. SalishSea.io is asking OrcaSound to store register identifiers on
bout tags — a column and a migration in orcasite, in
[orcasound/orcasite#1001](https://github.com/orcasound/orcasite/issues/1001). Once that
lands, `SSA:` is in a third party's database and renaming it is a coordinated migration
rather than a `sed`.

## Decision

**Keep `SSA:`, and register it in the Bioregistry.**

Registering converts "nobody has taken it" into "we hold it on the record". The two are
easily confused and only one of them survives someone else registering `ssa` next year.

## The check

Run 2026-08-13. `SSA` is unclaimed everywhere it could have been claimed:

| Registry | Size | Result |
|---|---|---|
| [Bioregistry](https://bioregistry.io/) | 2,759 prefixes | absent — `/api/registry/ssa` returns 404, and no prefix *or* synonym so much as begins with "ssa" |
| [N2T](https://n2t.net/) | 4,110 prefixes | absent |
| [identifiers.org](https://registry.identifiers.org/) | — | absent |
| [prefix.cc](https://prefix.cc/) | — | absent (404) |

One caveat worth recording rather than burying: prefix.cc's HTTPS certificate has expired,
so it is at best semi-maintained, and its silence is weak evidence. Bioregistry and N2T are
the ones carrying the weight here, and Bioregistry is the one that matters — it is the
metaregistry the others are increasingly read through, and it is already where this
repository's *external* prefixes come from (`NCBITaxon:` in `entities.tsv`,
`inaturalist.taxon:` in `mappings.tsv`, per
[ADR-0008](0008-species-identity-is-delegated.md)). We cite its prefixes and have none of
our own; that asymmetry is the thing being fixed.

**The collisions that do exist are semantic, not structural.** Anti-**SSA**/Ro (Sjögren's
syndrome antigen A) is routine in biomedicine, and a general reader may think of the Social
Security Administration or Sub-Saharan Africa. None is a registered prefix and none can
collide with ours mechanically. This is accepted rather than dismissed: an identifier that
reads like something else is a mild, permanent cost, and it is the price of a short prefix.

## Registration

Requested as a new prefix on [biopragmatics/bioregistry](https://github.com/biopragmatics/bioregistry):

| Field | Value |
|---|---|
| Prefix | `ssa` (Bioregistry prefixes are lowercase; every one of its 2,759 is) |
| Preferred prefix | `SSA` — the form this repository writes and consumers store |
| Name | Salish Sea Animals |
| Homepage | `https://github.com/salish-sea/animals` |
| Description | A register of individual marine mammals and the social groups they belong to in the Salish Sea |
| Example | `SSA:0000001` |
| Pattern | `^\d{7}$` |
| URI format | none — see below |
| Contact | P. Abrahamsen |

**No URI format, and that is not a defect.** [ADR-0014](0014-a-publication-not-a-service.md)
says this register is a publication, not a service; there is no resolver to point at and we
are not acquiring one to satisfy a form. This is ordinary in the registry: **1,151 of 2,759
Bioregistry entries have no URI format and no providers at all**, and 95 use a GitHub
repository as their homepage. The entry asserts that the prefix means *these* identifiers,
which is exactly the claim we want on the record, and nothing more.

A pleasing accident, given ADR-0002 argued from Gene Ontology: `GO`'s pattern is also
`^\d{7}$`.

## Alternatives considered

- **Check, find it free, and register nothing.** The cheapest option and the one Q10
  literally asked for — it only asked whether the prefix was *free*. Rejected because the
  answer decays: an unregistered prefix is available to the next person who wants it, and
  the whole point of [ADR-0010](0010-identifiers-are-never-reused.md) is that our
  identifiers are supposed to be interpretable indefinitely. A registration is the cheapest
  thing that makes "free today" mean something tomorrow.
- **Rename to something unmistakable** — `ssanimals`, `salishsea.animal`. Genuinely more
  defensive, and this was the last cheap moment to do it. Rejected because the anti-SSA/Ro
  clash is a reading problem, not a resolution problem, and reading is not what these
  identifiers are for: ADR-0002 spent its argument establishing that `SSA:0000020` is
  meant to be opaque and to travel beside a `label`. Trading a short prefix for a long one
  to improve the legibility of a string nobody is supposed to read is a bad trade.
- **`w3id.org` IRIs** — `https://w3id.org/salish-sea/animals/0000001`. Community-run, free,
  redirectable by pull request, globally unambiguous, and no server to operate. A real
  option and the most future-proof one. Rejected for now on scope: it changes every
  identifier in `data/`, it makes the TSVs materially wider, and
  [ADR-0013](0013-distribution.md) already supplies the stable addresses this repository
  promised. Worth revisiting if the register is ever consumed as linked data, which is the
  case where a bare CURIE genuinely hurts.
- **Adopt an upstream catalogue's prefix.** Nothing fits — ADR-0002 already rejected
  depending on upstream identity, and no existing prefix covers "individual whales and
  their social groups".

## Consequences

- **ADR-0002's open question is discharged**, and its bullet is updated to point here.
- **The prefix is now effectively frozen.** Renaming after a registration is worse than
  renaming after none — there is a public entry to deprecate as well as consumers to
  migrate. That is the intended effect.
- **#1001 can name the prefix as settled** rather than hedging that the namespace is being
  finalised, which is the reason this was resolved now and not later.
- **A registration invites curation.** Bioregistry's maintainers may ask for a resolver, a
  license statement, or a contact; those are answerable, and the review is a benefit rather
  than a cost. If the entry is declined outright, the prefix and the data are unaffected —
  we would simply be back to "free but unclaimed", with the request itself as a dated
  public record of the claim.

## Reference

Q10 ([#7](https://github.com/salish-sea/animals/issues/7)). Identifier shape:
[ADR-0002](0002-opaque-permanent-identifiers.md). Permanence:
[ADR-0010](0010-identifiers-are-never-reused.md). Publication not service:
[ADR-0014](0014-a-publication-not-a-service.md). Distribution:
[ADR-0013](0013-distribution.md). External prefixes we already consume:
[ADR-0008](0008-species-identity-is-delegated.md).
