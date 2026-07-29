# ADR-0014: The register is a publication, not a service

- **Status:** Proposed
- **Date:** 2026-07-28
- **Audience:** Scientific and informatics reviewers — the sections below are split, so each can read their half.

## Context

This effort began with a proposal in
[orcasound/orcasite#1001](https://github.com/orcasound/orcasite/issues/1001) that
SalishSea.io act as a **source of taxonomic authority** for apps like OrcaSound:

> Salish Sea would take a request from an app for taxonomy of the Salish Sea ecoregion,
> query all relevant sources for the latest standardized labels (understanding both source
> and receiver data schemes), and provide only the requested resulting taxonomy.

That is a runtime service: an app asks, the service fans out to the current authorities
for each ecotype, and answers.

This register is a different shape, and the difference is deliberate. It is worth being
explicit about, because the redirect is not obvious from reading the files.

## Decision

**The register is published, not served.** It is a set of files with editions, fetched and
held by consumers, not an endpoint queried at runtime.

## What this means for the science

Nothing about the *content* changes. The register still resolves ecotype, pod, matriline
and individual; it still expects to draw on CWR for Southern Residents, and on MERS,
finwave or DFO for Bigg's; the community still agrees what the terms mean. The vision in
#1001 is what this implements.

What changes is *when* the fanning-out happens. Rather than querying the authorities when
an app asks, a curator reconciles them when the authorities publish — after the annual
census, when a calf is confirmed — and the result is a dated edition that consumers hold.

Four reasons that matters, in rough order of weight:

1. **A bout tagged in 2025 must still mean what it meant in 2025.** If the taxonomy is
   fetched live, the meaning of an old annotation changes silently under it whenever an
   upstream source revises — a service returns current labels and a current hierarchy, and
   there is no state of it to cite. An edition is a thing a consumer can pin, verify by
   digest, and rebuild a derived fact from years later.

   The load-bearing word is *derived*. A stored identifier is already stable on its own
   under [ADR-0010](0010-identifiers-are-never-reused.md); what needs an edition to be
   reproducible is everything computed from it — the closure, an ancestor, an index. An
   earlier version of this reason claimed the point was recording `register_edition`
   alongside every tag, which over-claimed; see
   [ADR-0018](0018-annotation-semantics-belong-to-consumers.md). The decision is unaffected,
   because a live service can offer no citable state to derive from at all.
2. **Nothing goes down.** A service is a runtime dependency: if it is slow, or its API
   key rotates, or its host lapses, the moderator interface degrades. A file that has
   already been fetched does not.
3. **Reconciling sources is a judgement, not a lookup.** When CWR and a Bigg's catalogue
   disagree, something has to decide. Doing that inside a request means deciding silently
   and differently every time; doing it in a pull request means a person decides once,
   visibly, with a note about why.
4. **It costs nothing to run.** No uptime, no keys, no bill — which matters for something
   maintained partly on volunteer effort.

## Implementation

- Consumers hold the register: fetched at a pinned edition, loaded into their own
  database. See [ADR-0013](0013-distribution.md).
- Editions are CalVer tags with permanent asset URLs. There is no endpoint.
- A convenience API over the published editions remains possible later, and would be a
  *layer*, not the source. If one is ever built it must report which edition it served.
- Live querying of upstream authorities is a **curation-time** activity — a script that
  helps a curator prepare a pull request — not a request-time one.

## Consequences

- Consumers are stale between editions, by design. *How* stale is a function of release
  cadence, which is demand-driven rather than fixed: several a day while the register is
  under active development, and in steady state as often as something changes — a
  census-driven roster moves a few times a year, plus corrections whenever they arrive.
  Cadence is stated in [ADR-0013](0013-distribution.md); what matters here is only that
  staleness between editions is a design property and not a defect.
- A newly confirmed calf is not taggable until an edition ships. This is the sharpest cost
  and the reason for the provisional tier in
  [ADR-0001](0001-tsv-in-git-as-source-of-truth.md): a curator can merge a `SEED` row and
  cut an edition the same day.
- Understanding both source and receiver data schemes — the translation work #1001
  described — still has to happen. It moves into curation and into `mappings.tsv`.

## Alternatives considered

- **The service as originally proposed.** Fresher, and a genuinely nicer developer
  experience for a consumer that wants one call. Rejected on reason 1 above: it cannot
  make a 2025 annotation reinterpretable in 2030, because it has no notion of what it said
  in 2025.
- **Both — publication plus a service reading from it.** Still available and still
  reasonable. Deferred because nobody needs it yet, and because building the service first
  would have made the edition semantics an afterthought.
