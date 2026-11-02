# ADR-0027: In Darwin Core, the register's animals and groups are Organisms, not a checklist, and each identifier resolves to a page about its entity

- **Status:** Accepted, 2026-11-02, by Peter Abrahamsen as maintainer. No scientific reviewer has reviewed it.
- **Date:** 2026-11-02
- **Audience:** Scientific reviewers — this says how a whale, a matriline, a pod and an ecotype are each described to GBIF and to anyone else reading Darwin Core, and it answers [ADR-0008](0008-species-identity-is-delegated.md)'s question about ecotypes. Informatics reviewers — it adds a page generator, chooses where each identifier's address lands, and records how the register would map to a Darwin Core Data Package.
- **Answers:** the open question in [ADR-0008](0008-species-identity-is-delegated.md), "how is an ecotype expressed in Darwin Core?"
- **Makes:** the later choice [ADR-0026](0026-identifiers-resolve-through-w3id.md) left open, of sending each identifier's address to a page about its entity.

## Context

The question was whether the register could be published through Darwin Core as a checklist. On GBIF, a checklist is a dataset of names. Each row is a scientific name, which GBIF matches to its backbone taxonomy and indexes for name lookup. The register holds 1,078 entities, and 56 of them are taxa. The rest are 740 individual animals and 282 groups: 274 matrilines, 3 pods, a clan, a community and 3 ecotypes. As rows in a checklist, `J35` and `J17s` would be claimed as names for kinds of organism. GBIF would flag them as names it cannot parse, and they could reach the name-matching services other people depend on.

Darwin Core has a class for what the register does hold. It defines an **Organism** as "a particular organism or defined group of organisms considered to be taxonomically homogeneous", and gives "a specific wolf pack" as an example. Its own example of an `organismName` is "J pod". An occurrence record names its organism in `organismID`. [ADR-0026](0026-identifiers-resolve-through-w3id.md) already tells a consumer to publish an identifier's w3id.org address there, and SalishSea.io plans to (its issue salish-1bb, "Emit organismID and register archive with GBIF/OBIS").

What Darwin Core lets a publisher send to GBIF is narrower than what it can describe:

- **A Darwin Core Archive**, the format GBIF ingests today, is built around occurrences, taxa or sampling events. No archive can be built around organisms, so there is no GBIF dataset type for a list of animals and groups ([dwc.tdwg.org/schemas](https://dwc.tdwg.org/schemas/), schemas issued 2026-10-13).
- **The Darwin Core Data Package** was ratified on 26 May 2026 ([TDWG's announcement](https://www.tdwg.org/news/2026/dwc-additions-ratified/)), and its table schemas were published on 2026-10-22 ([tdwg/dwc#1037](https://github.com/tdwg/dwc/issues/1037)). Version 1.0 has an [`organism`](http://rs.tdwg.org/dwc-dp/1.0/table-schemas/organism.json) table, an [`organism-relationship`](http://rs.tdwg.org/dwc-dp/1.0/table-schemas/organism-relationship.json) table for one organism's relationship to another, and an [`organism-assertion`](http://rs.tdwg.org/dwc-dp/1.0/table-schemas/organism-assertion.json) table for facts about an organism. Those three hold nearly everything the register says. GBIF's [2026 work programme](https://docs.gbif.org/2026-work-programme/en/) lists ingesting these packages as planned work. A search on 2026-11-02 found nothing saying GBIF accepts them yet.

Two constraints apply to anything that publishes the register's rows. The data is not licensed for redistribution ([README](../README.md#licence)), and GBIF requires CC0, CC BY or CC BY-NC. And 714 entities come from the community-maintained Bigg's sheet. SalishSea.io's rights assessment of that sheet (D-21) says it is not to be "republished wholesale as a product", and whether a release of this register does so is [Q24](https://github.com/salish-sea/animals/issues/15), still open.

## Decision

**The register is not published as a Darwin Core checklist, in whole or in part.** Its individuals and groups are not names. Its taxon entities could form a valid checklist, but it would republish NCBI's taxonomy and the register's common names. It would also be a list of the taxa two projects talk about, gulls included, not a list of the animals of a region. Saying that a taxon is present in the Salish Sea would be a claim about sightings, which [ADR-0007](0007-no-observations.md) keeps out.

**Every individual and every group is a Darwin Core Organism.**

| Register | Darwin Core |
|---|---|
| An individual, such as J35 | an Organism with `organismScope` `multicellular organism`, Darwin Core's own example value |
| A group, such as J pod or J17s | an Organism whose `organismScope` is the group's rank: `matriline`, `pod`, `clan`, `community` or `ecotype` |
| `entity_id` | `organismID`, in the w3id.org form: `https://w3id.org/salish-sea/animals/0000020` |
| `label` | `organismName` |
| `taxon_id` | an Identification of the organism: `taxonID` and `scientificName`, with NCBI's classification from `dist/classification.tsv` |
| membership | a relationship from member to group, `member of` |
| a mother, from `parentage` | a relationship from offspring to parent, `offspring of`, one of Darwin Core's example values |
| a matriline's matriarch | a relationship from matriline to whale, `named for` |
| `sex`, `born`, life status | assertions about the organism; a status's `effective` date is the assertion's `assertionEffectiveDate` |
| `source_id` | the agent behind the relationship or assertion: `relationshipAccordingTo`, `assertionBy` |

**Taxon entities are not Organisms.** `SSA:0000900`, *Orcinus orca*, stands in for "a killer whale not resolved further", so that a moderator can tag one ([ADR-0008](0008-species-identity-is-delegated.md)). It is not a particular animal or a defined group of animals, and the register mints no taxon. Its page says which NCBI taxon it stands in for and gives NCBI's classification verbatim ([ADR-0022](0022-taxonomic-hierarchy-is-ncbis-excerpted.md)). An occurrence that records one has its taxon in its taxon fields and nothing to put in `organismID`.

**This answers ADR-0008's question.** An ecotype is expressed as an Organism whose scope is `ecotype`, not as a taxon, and the occurrence's taxon stays *Orcinus orca*. That answer is weaker for ecotypes than for other groups; see the open questions.

**Each identifier's address resolves to a static page about its entity.** [`bin/build_pages.py`](../bin/build_pages.py) writes one page per identifier, retired ones included. Each page says what the entity is, what it is a member of, its direct members, its mother and offspring, its names, its crosswalks, and the source of each claim. Each page also carries, as JSON-LD, what Darwin Core can say about an Organism on its own: its identifier, name, scope and taxon, the groups it belongs to and its mother. A program that follows an `organismID` out of a GBIF occurrence finds a description it can read. Sex, birth, life status and sources are on the page but not in the JSON-LD, because Darwin Core records them as assertions and relationships in separate tables, which a single page has no form for. The pages are built from a release tag and say which. They are static files on GitHub Pages for this repository, so the register stays a publication, not a service ([ADR-0014](0014-a-publication-not-a-service.md)). The w3id.org redirect then sends each address to its page with `303 See Other`, as ADR-0026 provided.

**The pages are not deployed publicly until Q24 is answered.** The repository and its releases already make every row public, so a page reveals nothing new. But a website with a page per animal is the clearest case of what D-21 rules out: the Bigg's sheet republished as a product. Q24's owner decides. Until then the pages are built and reviewed privately, and the redirect keeps landing on the README.

**A Darwin Core Data Package for GBIF waits** until GBIF ingests them and the licence question is settled. The mapping above is recorded now so that the export, when it comes, is a transformation of `register.db` and decides nothing new.

## What this means for the data

- No row changes. This record decides how existing rows are described outside the register.
- A pod is published as a defined group of organisms, which is what Darwin Core means. A matriline is published the same way. Membership is genealogical ([ADR-0005](0005-membership-is-genealogical.md)), so `member of` in this register means descent, not travelling together. Each group's page says so, because Darwin Core's `member of` carries no such meaning on its own.
- A page lists a group's direct members and never counts them ([ADR-0017](0017-no-counts.md)).
- Hidden names are left off the pages. A hidden name matches in search and is never displayed ([ADR-0011](0011-label-is-a-preferred-name.md)).

## Implementation

- `python3 bin/build_pages.py --out build/pages` writes the site. It loads `data/` through `bin/validate.py`'s own loader and refuses to build if the register does not validate. `build/` is ignored by git, because a thousand generated pages would bury every data diff.
- **Not done yet**, because each waits on Q24: a workflow that builds the pages on a release tag and deploys them to GitHub Pages, and a pull request to [perma-id/w3id.org](https://github.com/perma-id/w3id.org) that changes the redirect from the README to `https://salish-sea.github.io/animals/<digits>/`.

## Consequences

- An `organismID` in a GBIF occurrence becomes a link to a description of the animal or group, readable by people and by programs. That is the register's main contribution to biodiversity data, and it needs no GBIF dataset of its own.
- Retired identifiers keep a page that names their replacement, so an old occurrence record still leads somewhere useful ([ADR-0010](0010-identifiers-are-never-reused.md)).
- The register stays out of GBIF's name index, where its entities do not belong.
- The register gains a second generated product beside `dist/`, one that is built but not committed. A change to the pages is reviewed through the generator's diff, as an import is reviewed through its script's ([ADR-0015](0015-bulk-import.md)).

## Alternatives considered

- **A checklist of all entities.** Rejected for the reasons in Context: individuals and social groups are not names.
- **A checklist of the 56 taxon entities only.** Valid but nearly empty of value, since it republishes NCBI. Rejected as not worth a dataset. It remains possible later and nothing here prevents it.
- **Wait for GBIF to accept Darwin Core Data Packages and publish nothing until then.** Rejected because it serves nobody in the meantime, while the pages serve every occurrence that cites the register as soon as Q24 allows.
- **Send each address to SalishSea.io's profile page for the entity**, which ADR-0026 mentioned. Rejected for the reason ADR-0026 rejected addresses on a SalishSea.io domain: the register is meant to outlive any one consumer. A page here can link to the consumer's page.
- **Pages generated into `dist/` and committed.** Rejected because of the size of the diff. Everything on a page is already derivable from `dist/` and `data/`.

## Open questions

- **Is an ecotype a "defined group of organisms"?** A pod or a community is a group whose members the register lists. An ecotype such as Bigg's spans the North Pacific, and the register lists only part of it. Putting an ecotype's identifier in an occurrence's `organismID` would say the occurrence is of the whole ecotype rather than of some of its animals. Under [ADR-0018](0018-annotation-semantics-belong-to-consumers.md), how SalishSea.io records "Bigg's killer whales, individuals unknown" is SalishSea.io's choice. This record publishes ecotypes as organisms so their pages exist, and does not tell consumers to put them in `organismID`. A scientific reviewer may well say an ecotype should not be an Organism at all.
- **Where do membership dates go in a data package?** `membership.starts` and `ends` are valid time ([ADR-0006](0006-valid-time-in-data-assertion-time-in-git.md)). Darwin Core's `relationshipEstablishedDate` is the time at which a relationship was established, which reads as when it began but is ambiguous. No row has either date yet.
- **Does publishing pages answer Q24?** This record assumes the pages are gated by it and leaves the answer to its owner.
- **When does GBIF accept Darwin Core Data Packages?** Check before building the export.
