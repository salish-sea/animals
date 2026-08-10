# Changelog

Started at the first commit rather than at the first release: a changelog begun late has
to be reconstructed, and this is what consumers read to find out what changed.

Entries that affect consumers — new, deprecated, or renamed identifiers — belong under
**Register**. Everything else is **Design**.

## Unreleased

### Design
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
  longer designs OrcaSound's certainty control (it states the risk and leaves the
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
  pinned tag, the same way OrcaSound does. Its tight coupling is about the model, not the
  transport. Who besides the author may cut a release is Q25.
- Initial scaffold: scope, competency questions, walkthrough, glossary, background,
  open questions, twelve decision records, six definitions, and a validator.
- All decision records are `Proposed`. No definition is `agreed`.

### Register
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
