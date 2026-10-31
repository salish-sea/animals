# ADR-0026: An identifier's global form is a w3id.org address, and the Bioregistry request is withdrawn

- **Status:** Proposed.
- **Date:** 2026-10-31
- **Audience:** Informatics reviewers — this changes how an identifier is written outside the register, not what any identifier means.
- **Supersedes:** [ADR-0021](0021-ssa-is-a-registered-prefix.md) where it requests a Bioregistry prefix. Its decision to keep `SSA` stands.

## Context

[ADR-0021](0021-ssa-is-a-registered-prefix.md) kept `SSA:` as the prefix and asked the [Bioregistry](https://bioregistry.io/) to register it ([biopragmatics/bioregistry#2028](https://github.com/biopragmatics/bioregistry/issues/2028), filed 2026-08-13). Eleven weeks later the request has had no review. Its curator labelled it "feels like AI" on 2026-09-09, and has since marked it blocked by a proposed policy on generative AI ([bioregistry#2158](https://github.com/biopragmatics/bioregistry/issues/2158)). That policy bars posts written with generative AI, and says that requests for resources built with significant help from it may be rejected without discussion. This register is such a resource, and the request was drafted by an agent. It is unlikely to succeed.

That raised the prior question: what was the registration for? A prefix registry gives a short prefix one meaning across everyone who uses compact identifiers, and records where identifiers with that prefix resolve. `SSA:0000020` needs that, because "SSA" means nothing on its own: to a stranger it could be this register, the Social Security Administration, or the Sjögren's syndrome antigen. A full web address needs none of it. DNS already says who owns the name, and the address says where to look. A registry earns its place when many parties mint identifiers under prefixes nobody owns. This register has one authority, so a domain can do the job.

ADR-0021 weighed exactly this, `w3id.org` addresses, and called it "the most future-proof" option. It rejected it only because every identifier in `data/` would change and the TSV files would grow wider. That cost assumed the address would replace the stored form. It does not have to.

## Decision

**The global form of a register identifier is `https://w3id.org/salish-sea/animals/` followed by its seven digits.** `SSA:0000020` and `https://w3id.org/salish-sea/animals/0000020` name the same entity.

**`SSA:` stays the compact form.** The files in `data/` keep writing it, and consumers that already store it, such as Orcasound's tags since 2026-09-25, keep storing it. The register states the expansion itself, in its README, so the meaning of the prefix no longer depends on an outside registry. A consumer that publishes an identifier beyond its own systems, as a Darwin Core `organismID` would, should publish the full address.

**The address is held at w3id.org, not on a domain of our own.** A domain lasts as long as someone renews it, and [ADR-0010](0010-identifiers-are-never-reused.md) promises these identifiers indefinitely. If this project changed hands or lapsed, a lapsed domain could be bought by someone else, and every identifier would then point at them. w3id.org is held by the W3C Permanent Identifier Community Group, and a redirect there changes by a pull request to [perma-id/w3id.org](https://github.com/perma-id/w3id.org). It runs no server of ours, so the register stays a publication, not a service ([ADR-0014](0014-a-publication-not-a-service.md)).

**The redirect starts simple.** Every address under `https://w3id.org/salish-sea/animals/` redirects to the README's section on identifiers. The redirect is `303 See Other`, which w3id.org recommends when an address names a thing and the target is a document about it; unlike a permanent `301`, which w3id.org discourages, it can be changed later. Sending each identifier to a page about that entity, such as a SalishSea.io profile page, is a later choice. It changes only the redirect, never the identifiers.

**The Bioregistry request is withdrawn.** Peter withdraws it on bioregistry#2028, in his own words, as that project's policy asks.

## Alternatives considered

- **Keep waiting on the Bioregistry.** Costs nothing now, but the request is blocked on a policy that discourages it, and a registration would give our consumers nothing the register can't state itself. None of them reads the Bioregistry: not SalishSea.io, not Orcasound, not GBIF.
- **Addresses on a domain we hold**, such as `https://salishsea.io/animals/0000020`. Simpler, and SalishSea.io already serves pages keyed by these identifiers. Rejected because the identifiers would then last only as long as that domain stays in the right hands, and the register is meant to outlive any one consumer.
- **`https://w3id.org/ssa/`.** Shorter, and it matches the prefix. Rejected because it puts the semantically crowded "SSA" into the global form as well, and a `salish-sea` directory leaves room for anything else the organisation publishes.
- **Store the full address in `data/` and ask consumers to migrate.** Rejected for the reasons ADR-0021 gave: wider files, and a migration in every system that stores an identifier, for no gain in meaning.

## Consequences

- **ADR-0021 is superseded where it requests the registration.** Its Status line points here. Its check that `SSA` collides with no registered prefix still stands.
- **ADR-0002's open question and Q10** say the prefix was registered or requested; they now point here.
- **The README states the expansion**, under "Identifiers", and the redirect lands there.
- **A pull request to perma-id/w3id.org** adds `ids/salish-sea/.htaccess`, with Peter as its maintainer.
- **SalishSea.io's issue tracking the Bioregistry request** (`salish-8vr.13`) closes, as superseded by this record.

## Reference

The record this supersedes: [ADR-0021](0021-ssa-is-a-registered-prefix.md). Identifier shape: [ADR-0002](0002-opaque-permanent-identifiers.md). Permanence: [ADR-0010](0010-identifiers-are-never-reused.md). Publication, not service: [ADR-0014](0014-a-publication-not-a-service.md). Q10 in [open-questions.md](../docs/open-questions.md). The w3id.org service: [w3id.org](https://w3id.org/), [perma-id/w3id.org](https://github.com/perma-id/w3id.org).
