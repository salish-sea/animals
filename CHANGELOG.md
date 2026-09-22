# Changelog

Started at the first commit rather than at the first release: a changelog begun late has
to be reconstructed, and this is what consumers read to find out what changed.

Entries that affect consumers — new, deprecated, or renamed identifiers — belong under
**Register**. Everything else is **Design**.

## Unreleased

Six search names, and no identifier added, moved or retired. The register's first names in a language other than English.

### Register
- **Four French and Spanish common names**, the labels Whale Alert uses in those languages: `Baleine grise` (fr, *Eschrichtius robustus*), `Ballena jorobada` (es, *Megaptera novaeangliae*), `Ballena azul` (es, *Balaenoptera musculus*), `Marsouin commun` (fr, *Phocoena phocoena*). They are the first non-English rows, added as [ADR-0020](decisions/0020-localised-preferred-names-are-name-rows.md) says localised names should be — as `names.tsv` rows, once they exist. A consumer choosing a display name by language (English first) is unaffected.
- **Two `hidden` spellings the fold cannot reach**: `Short finned pilot whale` (*Globicephala macrorhynchus*) and `Northern right-whale dolphin` (*Lissodelphis borealis*). [ADR-0019](decisions/0019-names-are-compared-by-folding.md)'s fold deletes a hyphen without inserting a space, so "short finned" and "Short-finned" do not meet under it.

These six complete what SalishSea.io's retired Maplify dictionary covered: with them, every label that dictionary translated resolves through the register instead.

## 2026.09.5 — 2026-09-22

Names a consumer's feed actually uses, and three animals it has actually reported. Three taxa minted; no identifier moved or retired.

### Register
- **Three taxa, `SSA:0000953`–`SSA:0000955`**: *Delphinapterus leucas* ("Beluga"), and the genera *Eubalaena* ("Right whale") and *Hyperoodon* ("Bottlenose whale"). Each is crosswalked to iNaturalist, and NCBI's lineage for them is added to `taxonomic_parent.tsv`. They are vagrants here, not residents — SalishSea.io holds 9 Whale Alert reports of them inside the Salish Sea, and those were the only identified records in its Maplify feed that reached no register entity. The two genera take a genus-level name that claims no species, as the 2026.09.4 genera do.
- **Four search names** so that SalishSea.io can resolve its Maplify feed through the register instead of through iNaturalist's taxonomy: `Gray` and `Grey` (`hidden`, on *Eschrichtius robustus*) — Whale Alert's bare category label, 141 records; `Finback whale` (`hidden`, on *Balaenoptera physalus*) — an older common name and Whale Alert's label; and `Delphinus capensis` (`historical`, on *Delphinus delphis*) — the long-beaked form's former species name, consistent with that entity's note that NCBI and iNaturalist place it within *D. delphis*. None is displayable; `hidden` and `historical` names match and are never shown.

## 2026.09.4 — 2026-09-21

One kind of thing the register could not identify, and now can: an animal reported at a rank coarser than species. Thirteen genus entities, no identifier moved or retired.

### Register
- **13 genus entities, `SSA:0000940`–`SSA:0000952`**, each a genus over a species the register already held: *Balaenoptera*, *Callorhinus*, *Delphinus*, *Enhydra*, *Eumetopias*, *Lontra*, *Megaptera*, *Mirounga*, *Orcinus*, *Phoca*, *Phocoena*, *Tursiops*, *Zalophus*. All crosswalked to iNaturalist and to NCBI.

  These exist because an observer often reports a **rank coarser than species** — "a sea lion", without separating Steller from California. Such a record reached no register entity at all, and for a consumer that is not a cosmetic gap: SalishSea.io keeps iNaturalist taxon ids on its own data purely as a fallback for records the register cannot identify, and a fallback has to exist for every record or none. Measured there, these 13 close **124 of the 182** unidentified records and take coverage from 99.71% to **99.91%**.

  **A monotypic genus shares its only species' common name** — *Orcinus* is "Killer whale", as *O. orca* is — because they denote the same animal. Five are monotypic: *Callorhinus*, *Enhydra*, *Eumetopias*, *Megaptera*, *Orcinus*. **The other eight take a genus-level name that names no species**: *Phoca* is "Seal" and not "Harbour seal", *Zalophus* is "Sea lion" and not "California sea lion", *Phocoena* is "Porpoise" and not "Harbour porpoise". A genus-level record does not support naming the species, and the register should not let a consumer imply one.
- Two `hidden` search aliases are recapitalised, `SSA:0000917` "elephant seal" and `SSA:0000927` "bottlenose dolphin", to match the new genus names exactly. Sharing an identical string is a fact about the vocabulary and [C2](docs/competency-questions.md) answers with both candidates; meeting only under the fold is the accident [ADR-0019](decisions/0019-names-are-compared-by-folding.md) forbids, and the validator caught it.

## 2026.09.3 — 2026-09-21

One name, and no identifier added, moved or retired. The *Resident* ecotype had only its label; it now has a `common` name, so a consumer that reached it through 2026.09.2's crosswalk has something to display.

### Register
- **The *Resident* ecotype has a common name: "Resident killer whale"** (`SSA:0000003`).
  It had only its label, `Resident`, which is the ecotype's designation and not a name for
  an animal. That gap was load-bearing rather than cosmetic: 2026.09.2 crosswalked
  `SSA:0000003` to *Orcinus orca ater* so a consumer could reach the entity, but a consumer
  displaying the register's `common` name reached it and found nothing to show. SalishSea.io
  had been composing the string "Resident killer whale" in a table of its own for want of
  this row — the second opinion [ADR-0012](decisions/0012-relationship-to-the-salishsea-io-catalogue.md)
  exists to prevent — and deletes that table now. The string is unchanged for a reader; what
  changes is who asserts it. Symmetric with `SSA:0000002` *Bigg's killer whale* and
  `SSA:0000010` *Southern Resident killer whale*, both of which already had theirs.

## 2026.09.2 — 2026-09-20

Two things a consumer can now ask the register that it could not before, and no identifier
added, moved or retired. **What a taxon is descended from**: NCBI's lineage for every taxon
the register points at, with `kingdom` … `genus` worked out per taxon entity — excerpted by
script, not curated, and in NCBI's own words (its kingdom is `Metazoa`). **Which entity an
iNaturalist "Resident" or "Bigg's Killer Whale" record belongs to**: the two ecotypes are
now close matches of iNaturalist's two killer-whale subspecies. A consumer that matches on
`skos:exactMatch` alone gains nothing from the second until it also admits
`skos:closeMatch`.

### Register
- **Resident and Bigg's are crosswalked to iNaturalist's two killer-whale subspecies**:
  `SSA:0000003` `skos:closeMatch` `inaturalist.taxon:1602531` (*Orcinus orca ater*), and
  `SSA:0000002` to `1602533` (*O. o. rectipinnus*). A consumer holding an iNaturalist
  record identified to subspecies could not reach either entity before, because neither
  had any iNaturalist mapping — for SalishSea.io that was about one occurrence in twelve.
  `closeMatch` and not `exactMatch`: an ecotype and a subspecies are different kinds of
  thing with the same extension, and the equation is the Society for Marine Mammalogy's.
  **A consumer that uses only `exactMatch` gains nothing until it also admits
  `closeMatch`**, and should keep excluding `broadMatch`.
- The validator now refuses an external identifier that is an exact or close match of
  more than one entity, since a consumer could not tell which to use.
- **`data/taxonomic_parent.tsv` — NCBI's lineage for every taxon the register points at**,
  126 nodes for 40 taxa, in NCBI's own identifiers, ranks and names. Until now the taxon
  entities were flat, and a consumer wanting to know that a harbour seal is a pinniped, or
  what family a killer whale is in, had to get it from somewhere the register does not
  treat as an authority. Fetched by `bin/import_taxonomy.py` and never edited; no `SSA:`
  identifier is minted for anything in it
  ([ADR-0022](decisions/0022-taxonomic-hierarchy-is-ncbis-excerpted.md)).
- **Two new views in `dist/`.** `taxon_ancestor.tsv` is the closure, with each taxon its own
  ancestor at depth 0. `classification.tsv` gives each taxon entity `kingdom`, `phylum`,
  `class`, `order`, `family` and `genus`. **NCBI's kingdom for animals is `Metazoa`, not
  `Animalia`**, and a whale's order is `Artiodactyla`; both are reported verbatim.
- `entities.taxon_id` is now a foreign key into that table. No existing row changes; a
  *new* `taxon_id` fails validation until the importer has fetched its lineage.

### Design
- **Glossary states the prefix-case rule**, which turns out to be one rule and not the two
  it looks like. `mappings.tsv` writes `NCBITaxon:` capitalised beside 40 rows of
  lowercase `inaturalist.taxon:`, which reads as a drift worth fixing. It is not: both are
  the *preferred prefix* Bioregistry publishes for that registry, as `SSA` is ours —
  exactly the distinction [ADR-0021](decisions/0021-ssa-is-a-registered-prefix.md) drew
  when it registered the lowercase key `ssa` with the preferred form `SSA`. Nothing in
  `data/` changes; the rule is written down so the apparent inconsistency stops being
  rediscovered and half-fixed.
- Glossary entry for **catalogue**, marked ⚖️. It was the last load-bearing term both
  communities use differently with no entry, and the divergence is wide: in the whale
  world "the catalogue" means CWR's photo-ID catalogue, an enumeration kept so a new
  sighting can be matched to a known animal. The register is not one and the word is
  never used for it — the catalogues sit upstream (CWR, MERS, Bay Cetology) and
  downstream (SalishSea.io) of the register, which is the relationship
  [ADR-0012](decisions/0012-relationship-to-the-salishsea-io-catalogue.md) depends on.
  *Register* is also sharpened to say what distinguishes it — the identity assignment
  rather than the description — and to note it is not a *registry*: a registry
  is the office that keeps a register, and this is a publication rather than a service
  ([ADR-0014](decisions/0014-a-publication-not-a-service.md)).
- [ADR-0022](decisions/0022-taxonomic-hierarchy-is-ncbis-excerpted.md) amends ADR-0008:
  species identity is still delegated and nothing is curated, but the register now reports
  what the authority it delegated to says about ancestry. Subsumption stays a separate
  relation from membership, so `dist/ancestor.tsv` is unchanged.

## 2026.09.1 — 2026-09-20

The second release. Two changes a consumer will notice, neither of which moves or reuses an
identifier. **The register's first deprecation**: `SSA:0000001` is merged into
`SSA:0000010`, and a consumer holding it may follow `replaced_by` without asking anyone.
**73 new groups**: the Bigg's sub-lineages, so an observer can record "the T073As" rather
than the whole T073 lineage. They are minted ahead of
[Q22](https://github.com/salish-sea/animals/issues/13) and may yet be merged away, by the
same automatic route.

### Register
- **73 Bigg's sub-lineages, `SSA:0002131`–`SSA:0002203`**, nested inside the top-level
  lineages: `T073As` (`SSA:0002172`) is T073A and her descendants, and is a member of
  `T073s`. Until now an observer who saw the T073As could only record the whole T073
  lineage. They are minted ahead of
  [Q22](https://github.com/salish-sea/animals/issues/13), which asks whether they are real
  groups; if the answer is no, each is deprecated as `merged` into its enclosing lineage
  and a consumer may follow `replaced_by` automatically. Each carries its bare designation
  as a `hidden` name, so `T073A` now resolves to two candidates — the whale and her
  lineage — as `T073` already did ([ADR-0019](decisions/0019-names-are-compared-by-folding.md)).
- 269 animals gain a membership edge to their narrowest sub-lineage and **keep** the one
  to their top-level lineage. `dist/ancestor.tsv` reports each pair once, at the shortest
  path.
- **`SSA:0000003` — the *Resident* ecotype**, which the hierarchy was missing. The
  Southern Residents now roll up through it to *Orcinus orca*.
- **`SSA:0000001` is deprecated**, `merged` into **`SSA:0000010`**. Both identifiers
  always denoted the same animals — one thing entered at two ranks — so substitution is
  automatic and a consumer may follow `replaced_by` without asking a human. This is the
  register's first deprecation, and the first row `deprecations.tsv` has ever carried.
- **`SSA:0000010` is relabelled** from *Southern Resident community* to **Southern
  Resident**, and takes over the names that were on `SSA:0000001` (*Southern Resident
  killer whale*, and the hidden *SRKW*). Its rank stays `community`; repeating the rank in
  the label was the [ADR-0011](decisions/0011-label-is-a-preferred-name.md) error of
  writing display into a name.
- Twelve entities that were unreachable from any taxon — the whole Southern Resident
  branch, J clan through J35 — now roll up to a species. `bin/validate.py` reported twelve
  before this change and none after.
- **`dist/searchable_name.tsv` gains two columns, `retired` and `replaced_by`.** Existing
  columns and their order are unchanged, so a consumer reading by name keeps working; one
  reading by position does not. The deprecation above is why they exist: a retired
  identifier keeps its names, so *Southern Resident* now matches both the withdrawn
  `SSA:0000001` and the live `SSA:0000010`, and until now nothing in the view said which.
  **A picker must filter on `retired`**; a consumer resolving old free text can follow
  `replaced_by` on the same row instead of joining to `retired.tsv`. A null `replaced_by`
  on a retired row means the substitution needs a human — never that the identifier is
  live.

### Design
- **[Q1](docs/open-questions.md#answered) is answered**: Southern Resident is a *community*
  of the *Resident* ecotype, not an ecotype itself. `definitions/ecotype.md` and
  `definitions/community.md` are updated, and `ecotype.md` now records what the Society for
  Marine Mammalogy's 2024 taxonomy review actually decided about *Orcinus ater* and
  *O. rectipinnus* — it declined species rank and adopted the names as subspecies,
  provisionally.
- `dist/structure.md`'s subtree diagram is keyed on an identifier rather than on
  `label`. It said `WHERE label = 'Southern Resident community'`, so the relabel above
  emptied the diagram without failing anything — the exact breakage
  [ADR-0011](decisions/0011-label-is-a-preferred-name.md) forbids a label lookup for. It
  is now rooted at the resident ecotype, so the rollup this change restored is visible.
- `bin/validate.py` rejects a membership edge whose container is deprecated. A merged
  entity holds no members, and enforcing that is what makes the filter below safe:
  filtering out an entity that could still have descendants would report those
  descendants with nothing named as the cause.
- `bin/validate.py` no longer reports a deprecated entity as unreachable. Being
  unreachable is the correct state for something that has been merged away, and reporting
  it would train the reader to ignore the one warning that catches a whole branch dropping
  out of the rollup.
- `bin/validate.py` pins *Southern Resident* as a C2 acceptance test, alongside the
  existing `T090s` / `J-35` / `Biggs` trio: it must return both identifiers, not one. And
  `searchable_name`'s `retired` / `replaced_by` are checked against `deprecations.tsv`
  rather than assumed, for every deprecation and not just this one — a view that lost the
  join would leave a plausible-looking pair and no way to choose between them. The check
  that two candidates describe themselves distinguishably now counts `retired` as part of
  that description.
- `dist/structure.md`'s rank counts leave out deprecated entities, as its unreachable
  count already did. It reported **three** ecotypes where two are live — on the diagram
  the README points at.
- C5 and C6 are answerable in full, and the competency-question table says so rather than
  **Partly**. The rest of the branch's stale references to Q1 are swept up with them:
  `README.md`'s outline still drew the old hierarchy (no species at the top, the community
  under an ecotype of the same name); `docs/walkthrough.md` rolled J pod up through
  `SSA:0000001` to reach a species, which is now a walk to `SSA:0000900` and not a mapping
  lookup at all; [ADR-0008](decisions/0008-species-identity-is-delegated.md) illustrated
  ecotype crosswalks with the identifier whose mapping moved; and
  [ADR-0021](decisions/0021-ssa-is-a-registered-prefix.md) offered `SSA:0000001` as the
  example on a Bioregistry submission that will outlive it. Also
  [ADR-0013](decisions/0013-distribution.md), which recorded an objection to gating
  releases on `--strict` that Q1 has retired: the warning count no longer mixes provenance
  debt with a modelling gap.
- `docs/walkthrough.md`'s traced annotation has aged into the thing it was illustrating.
  The moderator's `SSA:0000001` pick, made against edition `2026.07.1`, is now the
  register's first real C9 case — `merged`, with `replaced_by` populated, so the
  substitution is automatic. Step 4's hypothetical `split` is the contrasting case.

## 2026.08.1 — 2026-08-28

The first release. Everything below has accumulated since the first commit; from here a
consumer can pin a tag rather than a commit ([ADR-0013](decisions/0013-distribution.md)).

**Nothing in `data/` has been verified by a curator.** Every row is `SEED` or sourced but
unratified, and `bin/validate.py` reports 157 unverified rows. The register is still
proposed, and this tag is a way to consume a moving thing reproducibly, not a claim that
it is settled.

### Register
- **Twenty-one taxon entities**, `SSA:0000919`–`SSA:0000939`: fifteen species (blue, sei,
  sperm, pygmy and dwarf sperm, Baird's and Cuvier's beaked, Risso's, common bottlenose,
  common, northern right whale, striped, short-finned pilot, Guadalupe fur seal, northern
  fur seal) and six stand-ins for "sighted, but not resolvable further" — the role *Aves*
  and *Laridae* already played for audio. Coverage of the SalishSea.io corpus goes from
  97.5% to 99.6% of 61,411 occurrences.
- **`SSA:0000938` is `Pinnipedia`, not `Phocoidea`.** iNaturalist's `372843` is labelled
  "Pinnipeds" and used that way, but the name denotes the true-seal superfamily, and NCBI
  has no `Phocoidea` at all — so [ADR-0008](decisions/0008-species-identity-is-delegated.md)'s
  requirement that a taxon entity carry a `taxon_id` cannot be met by that concept.
  `Pinnipedia` is the clade meant and NCBI has it. The mapping is `skos:closeMatch`, not
  `exactMatch`: the two overlap in practice and differ in principle, which is what
  `closeMatch` says. salishsea-io decision 027 records the same misnomer from the GBIF
  side.
- **"Otter" now names two entities on purpose.** `SSA:0000939` *Lutrinae* is added because
  river otter and sea otter are both present, so a bare "otter" is genuinely ambiguous
  rather than shorthand. `validate.py` rejected the first attempt under
  [ADR-0019](decisions/0019-names-are-compared-by-folding.md) — `SSA:0000906` already
  carried a hidden `otter`, and two entities meeting *only* under the fold is an accident.
  The spelling is now declared on **both**, which is the difference between an accidental
  collision and C2's honest two-candidate answer.
- **Deliberately still uncovered:** 26 genus- and family-level stubs, 195 SalishSea.io
  occurrences. Most resolve to a single local species the register already holds, which
  raises a question rather than a gap — whether "Megaptera, species undetermined" wants an
  entity, or whether [ADR-0009](decisions/0009-uncertainty-on-the-annotation.md) means the
  consumer tags the species and carries the uncertainty on the annotation. A few
  (`Delphinidae`, `Delphinoidea`, `Phocoenidae`) are genuinely multi-species and are a
  straightforward gap.
- **Three birder alpha codes added**, all `hidden`: `UNBI` on `SSA:0000907` *Aves*,
  `OSPR` on `SSA:0000910` *Pandion haliaetus*, `HOSP` on `SSA:0000911` *Passer
  domesticus*. `UNBI` is the interesting one: the list carries group-level entries for
  exactly the case this register's *Aves* covers, and the scientific-name entry reads
  *Aves (gen, sp)* — the rank the entity already sits at. `PIGU` is unchanged but
  re-sourced from `SEED` to `IBP`, which is what actually assigns it.
- **`SSA:0000908` *Laridae* deliberately has no code**, and the `Gull` row now says so.
  The nearest entry is `UNLG`, "Unidentified Larus Gull" — *Larus*, a genus — while this
  entity is the family, which also holds terns, kittiwakes, noddies and skimmers. Adding
  it would narrow the entity through a name, and validation would not catch it, because
  nothing else in the data contradicts a name. This is the failure ADR-0019's guarantee
  is written against, arriving by a route that guarantee does not cover: not a fold
  collision, but a curator adding a name at the wrong rank. Written down so the gap is
  not "fixed" later by someone noticing it.
- **One new source, `IBP`.** Unlike `ORCASOUND`, it is an authority: an alpha code is the
  code the Institute for Bird Populations assigns to a taxon — a species, or one of the
  141 non-species entries the list also carries, which is what `UNBI` is — true whether
  or not a moderator ever types it. That is why these are `IBP` rows and not
  use-evidence rows. Not a departure from ADR-0019, which rejected variant-rows for
  *typographic* variation — `OSPR` does not fold to `osprey`; it is a name from a
  separate naming system that denotes the same animal, so a row is the right mechanism,
  and the burden is bounded at one row per bird entity the list actually covers.
- **`dist/searchable_name.tsv` gained three columns** — `entity_label`, `entity_kind`,
  `entity_rank` — closing the half of the designation-matching question that was actually
  still open. Zero-padding was already answered: ADR-0019's fold resolves `T34s`, `T38C`
  and `T65A5` against the padded labels, verified against all 94 live Orcasound tags. What
  was missing was the other half of the same promise. C2 says the honest answer is
  sometimes two candidates and a consumer should "show both", and ADR-0019 says they are
  distinguished by rank — but the file holding every name carried no rank, so a picker
  could not describe the choice it was offering. Worse for hidden names, which match in
  search and must never be displayed: a consumer matching `J` had an identifier and
  nothing to show. Same denormalisation, and the same reason, as `ancestor.tsv`. Additive,
  so existing readers keep working. C2's acceptance test grew to match: `T090` is pinned
  to *both* `SSA:0000040` and `SSA:0010290`, so a regression that quietly resolved the
  ambiguity to one candidate fails the build instead of reading as an improvement, and
  every folded form naming more than one entity is checked to describe its candidates
  distinguishably.
- **Three new individuals: `SSA:0010510` T419, `SSA:0010511` T420, `SSA:0010512` T421.**
  Designated by Bay Cetology in March 2026 after an unrecognised trio appeared in
  Vancouver Harbour and travelled into Puget Sound, and tagged on Orcasound bouts since.
  They are Bigg's by ecotype but not West Coast Transients — attributed to the Gulf of
  Alaska / Aleutian / Bering stock — which is why the Bigg's sheet does not reach them.
  Membership is recorded at the ecotype, because their matriline is not established and
  `definitions/membership.md` says not to invent an intermediate group. Sex and birth
  years are left blank: the press reports them, no citable record does yet.
- **Five names added**, all `hidden`, all sourced to use rather than to an authority:
  bare `J` / `K` / `L` on the three pods, `KW` on `SSA:0000900` *Orcinus orca*, and
  `seagull` on `SSA:0000908` *Laridae*. Every one is a tag a moderator has actually
  applied — `J` to 29 bouts — that previously resolved to nothing. `Gull` stays the
  common name for Laridae; `seagull` is hidden because it is colloquial, not because it
  is unused.
- **Two new sources.** `BAYCETOLOGY` — the body that mints T designations, maintaining
  the catalogue Michael Bigg started, which `FINWAVE` turns out to be the platform for;
  relevant to Q3. And `ORCASOUND`, which is not an authority on animals at all but
  evidence that a name is *in use* — the only claim a hidden name makes.

### Design
- **Crosswalks are checked against the authorities they point at.**
  `bin/check_crosswalks.py`, run weekly and on any pull request touching `mappings.tsv` or
  `entities.tsv`. ADR-0008 buys us out of curating taxonomy at the price of pointing at
  identifiers we do not control, and nothing here ever asked whether they still resolved.
  An audit of SalishSea.io's taxon mirror found **nine iNaturalist taxa deactivated
  upstream**, four from one genus split (*Sagmatias* → *Aethalodelphis*); every mapping in
  this register was correct throughout, but there was no way to know that without asking.
  Drift — deactivated, merged or renamed — reports and never fails, because upstream is
  allowed to change and we are only obliged to notice; each finding names the replacement
  identifier. What *does* fail is an identifier that never resolved, or a mapping added in
  a pull request that was already dead when written. A single `crosswalk-drift` issue
  holds the worklist and closes when nothing drifts.
- **Scope gained two boundaries that were being rediscovered.** `WCT01`–`WCT08` look like
  West Coast Transient catalogue designations and are Bigg's **call types** — the bout
  `Short rising WCT07 call x2` settles it — so they belong to `signals-srkw` and the
  register mints nothing for them. A consumer therefore cannot classify a tag by its
  shape: `T090s` is an animal, `WCT07` is a sound. And `fish` is deliberately outside the
  taxonomic bound, so the tag is meant to end up with no identifier.
- Q12 retired by declining it: this register never references the signals vocabulary,
  so there is no mutual convention to design. The register's half was already
  discharged — identifiers stable enough to reference (ADR-0002, ADR-0010) and editions
  to pin (ADR-0013) — and whether `signals-srkw` replaces its copied ecotype and pod
  labels with identifier references is that repository's decision, when that work is
  planned.
- **Localised preferred names are `names.tsv` rows, added when they exist** (ADR-0020),
  closing Q14 largely by rejecting its premise: `label` is not "implicitly English" but
  notation for ~650 of 668 entities, so it stays language-neutral and gains no language
  dimension. A genuinely language-bound preferred name becomes a sparse
  `type = preferred` row beside the existing `language` column, with `label` as the
  fallback; implementation is additive and deferred until the first real row. Coast
  Salish names can be recorded today as `common` + language.
- **Names are compared by folding, never rewritten** (ADR-0019), closing Q17. The
  register publishes the matching rule C2 needs — lowercase, drop apostrophes and
  hyphens, collapse whitespace, strip leading zeros per digit run — with executable test
  cases in `dist/fold_test.tsv`, so no two consumers can implement it differently. A
  trailing `s` deliberately never folds: `T090s` names the matriline and `T090` its
  matriarch, 126 such pairs exist, and merging them resolves a name to the wrong animal.
  The validator now enforces the guarantee that makes the rule safe to publish — folding
  may not merge entities that exact spelling keeps apart — and pins the C2 trio
  (`T090s` / `J-35` / `Biggs`) to permanent identifiers as an acceptance test.
- **Annotation semantics belong to the consuming systems** (ADR-0018), closing Q18 by
  relocating it. This repository had disclaimed owning the annotation shape four times
  while remaining the only place it was written down at length — a five-column table in
  ADR-0009, four rendered rows in the walkthrough, and an open question filed against this
  author. It has a home: SalishSea.io's decision 013 and the `public.identifications` table
  under it, which already ships the confidence/verification split Q18 asked for, plus an
  `is_present` flag answering the absence question ADR-0009 left open. ADR-0009 keeps its
  negative half — no hedge terms in the vocabulary — and its table is now marked
  illustrative. The register's whole claim on an annotation is two requirements: cite an
  identifier rather than a name, and record the edition anything *derived* was derived from.
- **Narrowed the edition requirement**, which several records had over-claimed. ADR-0006,
  ADR-0014, ADR-0009's sketch and the walkthrough all said or implied that an annotation
  records `register_edition` so it stays interpretable later. It does not need to: ADR-0010
  already guarantees an identifier's meaning never changes, so a stored pick is
  self-sufficient and asking for the edition beside it double-counts that guarantee. What is
  edition-dependent is a *derived* fact — an ancestor, a closure, an index — so the edition
  belongs on the materialization. ADR-0014's publication-not-a-service decision is
  unaffected; a live service offers no citable state to derive from at all.
- Dropped the walkthrough's second bout. It was carried as a hard case, and once Q7
  dissolved there was nothing left in it that the first bout does not already show.
- **The register publishes no counts of animals** (ADR-0017), resolving Q6 as "no". A
  count would read the roster's silence as data while it is knowingly incomplete, and the
  derivable count is one of descent rather than of a travelling group. Consumers may
  derive one and own the claim. Entity counts in `dist/structure.md` are unaffected —
  they describe the register, not the world.
- **The register records parentage** (ADR-0016), resolving Q16. `data/parentage.tsv`
  holds one row per child and role, as edges rather than `mother_id` columns, so a
  paternity from a genetic study and an existence from a census keep separate
  provenance. It passes ADR-0007's own test — the claim needs neither a date nor a
  place — which is the first time that rule has admitted something rather than refused
  it. Matrilines are *not* derived from parentage; the two are asserted independently
  and cross-checked, because a mother and calf share a matriline except after a fission.
- Added `docs/start-here.md` — a short entry point covering what is proposed, how it
  departs from the original service proposal in orcasound/orcasite#1001, and the domain
  questions ordered by how much they block.
- ADR-0014 records the publication-not-a-service redirect explicitly, rather than leaving
  a reviewer to infer it.
- Q18 corrected: it attributed to ADR-0009 a claim that ADR-0009 explicitly disclaims —
  that this repository owns annotation semantics — and quoted words it does not contain.
  The two documents agree; Q18 is now the work of carrying the confidence/verification
  split into the sketch, not a dispute to settle.
- Swept the repo for places where it prescribed to systems it does not own. ADR-0009 no
  longer designs Orcasound's certainty control (it states the risk and leaves the
  interface to them) and no longer reads as banning `signals-srkw`'s compound labels;
  `scope.md` and `definitions/pod.md` state the drift risk and the "J pod" ambiguity as
  facts rather than instructions; ADR-0011 keeps label non-uniqueness and drops the
  picker.
- ADR-0013 and ADR-0014 no longer disagree about release cadence. It is demand-driven —
  several a day under active development, a few times a year in steady state — and
  ADR-0014 depends only on there being editions to be stale between.
- Q5 retired by declining it: whether a consumer stores redundant ancestors or derives
  them is that consumer's annotation design. The register's part — publishing the closure
  so deriving is cheap — is already done. `dist/README.md` now warns that derived facts
  are edition-specific.
- Q7 retired by declining it: the `Humpback mimics Bigg's?` bout was never a register
  problem. A call type characteristic of Bigg's is a regularity about who produces it, not
  a property of the sound, and the walkthrough had promoted "characteristic of" to
  "belongs to". The one real finding — a signal must be taggable with no animal tag — moves
  to Q18, where the annotation schema lives.
- `schema.sql` now states the constraints declaratively and the build is the validation;
  `bin/validate.py` keeps only what SQL can't express, plus curator-facing diagnostics.
- `dist/` carries the derived views as TSV — closure, current status, searchable names,
  deprecations — so consumers don't reimplement them.
- Releases carry `register.db`, the TSVs, `schema.sql` and `SHA256SUMS`.
- ADR-0013 now states release cadence — a tag push, on demand, possibly several a day —
  and ADR-0012 states how SalishSea.io consumes the register: a released artefact at a
  pinned tag, the same way Orcasound does. Its tight coupling is about the model, not the
  transport. Who besides the author may cut a release is Q25.
- Initial scaffold: scope, competency questions, walkthrough, glossary, background,
  open questions, twelve decision records, six definitions, and a validator.
- All decision records are `Proposed`. No definition is `agreed`.

### Register
- **The marine-mammal taxon list is now PSEMP's committee list.** Seven new
  `kind = taxon` entities, `SSA:0000912`–`SSA:0000918`: harbour porpoise, Dall's
  porpoise, Pacific white-sided dolphin, minke whale, fin whale, northern elephant seal
  and sea otter. With those, the register holds all sixteen species listed by committee
  on the PSEMP
  [Marine Mammals Work Group](https://psemp-marinemammalsworkgroup-wa-psp.hub.arcgis.com/)
  site as retrieved 2026-08-13. That is a *bound*, not a guarantee of completeness: the
  work group's stated remit is "all marine mammals that inhabit or migrate through Puget
  Sound", and the committee list is the "most-common species" within it, so an animal
  they monitor may still be missing here. Adopting somebody else's published list beats
  inventing one anyway, and `docs/scope.md` now says which list and as of when. The
  dolphin's genus is contested — WoRMS says *Sagmatias*,
  NCBI and iNaturalist say *Aethalodelphis*, everyone else still says *Lagenorhynchus* —
  so the label follows WoRMS as a holding position, the other two are `names.tsv` rows,
  and a curator arbitrates in Q26.
- **An iNaturalist crosswalk**, the first new namespace in `mappings.tsv` since the
  register began: every `kind = taxon` entity now carries a `skos:exactMatch` to an
  `inaturalist.taxon:` identifier, 19 rows under a new `INAT` source. SalishSea.io
  ingests iNaturalist sightings and had no way to resolve an observation's taxon to a
  register entity; it does now. ADR-0008 had reserved this ("if a consumer needs one")
  and is updated to record that one does. `taxon_id` is untouched and stays on NCBI —
  the crosswalk records where iNaturalist puts a concept, not what the register believes.
- **Gray whale and river otter** (`SSA:0000905`, `SSA:0000906`) as `kind = taxon`
  entities, alongside the pinnipeds already there.
- **Birds enter the register at taxon level**, `SSA:0000907`–`SSA:0000911`: pigeon
  guillemot, osprey, house sparrow, `Laridae` for "gull", and `Aves` for "a bird, not
  resolved further" — the acoustic analogue of the unplaceable orca. A shore-mounted
  hydrophone hears birds and OrcaHello moderators were already tagging them
  (orcahello#550). The level follows what a moderator can actually hear; no individuals
  and no groups. *(Both entries backfilled — these shipped in 334134c without one.)*
- `parentage.tsv` added, with one row: J57's mother is J35. That fact was previously
  carried in a free-text note on `entities.tsv` that the validator ignored.
- **Imported the Bigg's designation sheet**: 510 individuals and 132 derived matrilines,
  with nicknames, Alaska/California designations, birth years, sex and deceased status.
  The register goes from 20 entities to 661. Imported, not curated — see ADR-0015, and
  Q22 for the grouping, which is the least confident part.
- Added `kind = taxon` entities for *Orcinus orca*, humpback, Steller sea lion, California
  sea lion and harbour seal, plus ecotype→species membership edges. These are what a
  moderator tags when an orca is heard too faintly to place in an ecotype — roughly 30% of
  the biophony corpus previously had nothing to tag.
- `status.tsv` gains a `recorded` column and a stated precedence rule, so a retracted
  life-status claim is resolvable. Consumers must order by `(recorded, effective)`.
- Reviewed by two independent passes (consistency, gaps); corrections applied and the
  remaining design questions filed as Q15–Q21 rather than resolved silently.
- Seed data only. Every row carries `source_id = SEED`, meaning **unverified** — the
  seed exists to make the schema concrete and to give the walkthrough something to
  point at. It must be replaced or confirmed by a curator before any consumer relies
  on it.
