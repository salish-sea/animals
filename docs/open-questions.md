# Open questions

**Audience: everyone, but sorted so you can find yours.**

This is distinct from `decisions/`. An ADR records something we have *decided*, however
provisionally. This index records things we have **not** decided and, crucially, **who
can decide them**.

**Discussion happens in the [issue tracker](https://github.com/salish-sea/animals/issues)**,
one issue per question, so a reviewer can be notified, reply from anywhere, and never
needs to open a pull request to answer. This file is the index: it maps the stable Q
numbers used throughout the repository to their issues. When a question is resolved, the
answer lands in an ADR or a commit, the issue closes with a link to it, and the question
moves to [Answered](#answered) below.

Every question has an owner. A question with no owner is a question that will not get
answered.

## For the scientific reviewers

Filter: [`science-review`](https://github.com/salish-sea/animals/issues?q=is%3Aissue+is%3Aopen+label%3Ascience-review)

| # | Question | Owner | Discussion |
|---|----------|-------|------------|
| Q1 | Is "Southern Resident" an ecotype, or a community of the Resident ecotype? | S. Veirs, D. Bain | [#1](https://github.com/salish-sea/animals/issues/1) |
| Q2 | Are the Southern Residents one acoustic clan or more? | S. Veirs | [#2](https://github.com/salish-sea/animals/issues/2) |
| Q3 | Which source is authoritative for Bigg's? | S. Veirs | [#3](https://github.com/salish-sea/animals/issues/3) |
| Q4 | Should Northern Residents and offshores be populated now or later? | S. Veirs | [#4](https://github.com/salish-sea/animals/issues/4) |
| Q9 | Are there animals or names we should *not* publish? | S. Veirs | [#6](https://github.com/salish-sea/animals/issues/6) |
| Q13 | Is the plural the canonical written form for a matriline? | S. Veirs, D. Bain | [#9](https://github.com/salish-sea/animals/issues/9) |
| Q15 | What does a curator do when a published roster is associational? | S. Veirs, D. Bain | [#11](https://github.com/salish-sea/animals/issues/11) |
| Q22 | Is a T-number lineage the right grouping, or does the sheet group differently? | S. Veirs, D. Bain | [#13](https://github.com/salish-sea/animals/issues/13) |
| Q23 | What are the Alaska/California designations, and where do they belong? | S. Veirs | [#14](https://github.com/salish-sea/animals/issues/14) |
| Q26 | Which genus does the Pacific white-sided dolphin get labelled with? | S. Veirs, D. Bain | [#17](https://github.com/salish-sea/animals/issues/17) |

## For the informatics reviewers

Filter: [`informatics-review`](https://github.com/salish-sea/animals/issues?q=is%3Aissue+is%3Aopen+label%3Ainformatics-review)

| # | Question | Owner | Discussion |
|---|----------|-------|------------|
| Q8 | Who is the named editor, and who reviews the domain content? | P. Abrahamsen, S. Veirs | [#5](https://github.com/salish-sea/animals/issues/5) |
| Q24 | Does releasing the register republish the Bigg's sheet? | P. Abrahamsen | [#15](https://github.com/salish-sea/animals/issues/15) |

## Answered

Resolved questions stay here in full: the reasoning is part of the record, and the Q
numbers are referenced throughout the repository.

### Q5 — Do consumers store redundant ancestors, or derive them?
**Resolved 2026-07-28, by declining it.** The question named its own owner and it was not
this repository: "should *OrcaSound* store what the moderator picked". How an occurrence
records the individuals and groups a moderator tagged is that consumer's annotation
design, and there is a separate process for that work.

The register's part is already discharged. `dist/ancestor.tsv` publishes the transitive
closure precomputed ([ADR-0013](../decisions/0013-distribution.md)), so deriving a parent
costs a lookup. Having made the choice free, the register has no stake in which way it
goes.

Worth carrying into that other process: the two options were framed here as a size
trade-off, and that is the least interesting difference between them. **They promise
different things over time.** Storing what the moderator picked is a faithful record of an
act of identification and stays true as one. Deriving instead tracks the register, so the
ecotype shown against a 2026 bout will change when Q1 reparents the Southern Residents.
Neither is wrong — they answer different questions.

### Q6 — Should the register publish group sizes?
**Resolved 2026-07-28. No.** Not as a column, not as a view, not in prose. The roster is
knowingly incomplete — Northern Residents and offshores unpopulated, 510 Bigg's rows
unverified — so a count would read the register's silence as data and be wrong with no
error bar. The count that *is* derivable is a count of descent, not of a travelling
group, so it would be read as answering a question the register deliberately refuses.
And CWR publishes the census; a second figure that differs because a birth has not been
ingested sets the register against the source it depends on.

Derivability is not publication: a consumer that wants a count can compute one and own
the claim. See [ADR-0017](../decisions/0017-no-counts.md), which also draws the line
against `dist/structure.md` — counting entities in the register is a diagnostic about the
register, not a claim about how many animals exist.

Closed by P. Abrahamsen rather than by the listed owners, because every reason above is
structural rather than a domain judgement. The one part that *is* theirs is the condition
for reopening: the objection is empirical, and would weaken if a population's roster were
ever complete and verified. What would count as complete enough is recorded as the ADR's
open question.

### Q7 — How do we model a bout where the animal and the sound belong to different species?
**Resolved 2026-07-28, by declining it.** The question was an artefact of how the bout was
written up, not a property of the bout. `Humpback mimics Bigg's?` is a hypothesis — a
signal characteristic of Bigg's, suspected to have come from a humpback. **A call type
being characteristic of Bigg's is a regularity about who usually produces it, not a
property of the sound**; sounds carry no species. Promoting "characteristic of" to
"belongs to" is what manufactured a second species, and with it the appearance of a
modelling problem. What was recorded is one animal, identified with low
confidence — [ADR-0009](../decisions/0009-uncertainty-on-the-annotation.md) — plus a call
type, which is the signals vocabulary's business. The register was never asked to identify
sound sources, so nothing here bears on it.

One real requirement survives, and it is the annotation schema's, not the register's: a
signal must be taggable with no animal tag, so that a moderator who knows the call type
and not the producer is not forced to name an animal. Folded into Q18.

### Q10 — Is `SSA:` a safe prefix?
**Resolved 2026-08-13. Free, and now claimed.** Checked against four registries:
Bioregistry (2,759 prefixes — no `ssa`, and no prefix or synonym even beginning with
"ssa"), N2T (4,110), identifiers.org, and prefix.cc. Nothing collides. The only clashes
are semantic — anti-SSA/Ro is routine in biomedicine — and those cannot collide
mechanically with a CURIE prefix.

But "free" decays, so the answer is not just the check: `SSA` is being **registered in
the Bioregistry**, with no URI format, which 1,151 of its 2,759 entries also lack and
which keeps [ADR-0014](../decisions/0014-a-publication-not-a-service.md)'s
publication-not-a-service promise intact. The trigger for resolving it now was
[orcasound/orcasite#1001](https://github.com/orcasound/orcasite/issues/1001) asking
OrcaSound to store register identifiers in a new column — the first external system, which
is precisely the deadline this question set itself. See
[ADR-0021](../decisions/0021-ssa-is-a-registered-prefix.md); renaming (`ssanimals`) and
`w3id.org` IRIs are the alternatives it weighed.

### Q11 — What is the release artefact, and does it need a stable URL?
**Resolved 2026-07-28.** GitHub releases, with the permanent asset URLs GitHub already
serves:

```
https://github.com/salish-sea/animals/releases/latest/download/register.db
https://github.com/salish-sea/animals/releases/download/2026.07.1/register-tsv.tar.gz
```

That *is* the stable address, it needs no client and no API call, and it carries no
hosting commitment — which is what made the dereferenceable-identifier version of this
question look expensive. Not GitHub Packages: it has no generic file registry and no
ecosystem that serves Elixir, which is what OrcaSound's server runs. See
[ADR-0013](../decisions/0013-distribution.md).

### Q12 — How do the two repositories reference each other?
**Resolved 2026-08-09, by declining it.** The plural in the title was the error: the
reference only ever runs one way. This register will never cite the signals vocabulary,
and whether — and how — `signals-srkw` references register identifiers is that
repository's decision, to be made when that work is planned. It has not begun, and
[scope.md](scope.md) had already said as much: "whether to do that, and when, belongs to
that repository." Holding the question open here was this repo acting as owner of a
convention it had disclaimed, which is the same failure Q18's closure named.

The register's half is already discharged, which is why nothing remains to decide here:
identifiers stable enough to be worth referencing
([ADR-0002](../decisions/0002-opaque-permanent-identifiers.md),
[ADR-0010](../decisions/0010-identifiers-are-never-reused.md)) and editions to pin
([ADR-0013](../decisions/0013-distribution.md)) — "declaring a dependency on a specific
edition" is the same act for the signals vocabulary as for any consumer: pin the tag.
What carries over to the signals work when it starts: the copied ecotype and pod labels
in `labels.md` are the thing to retire, and the `JK` / `JKL` set-labels are migration
work, both stated in scope.md.

Closed by P. Abrahamsen alone though co-owned with S. Veirs, because nothing here is a
domain judgement — the question filed work against the wrong repository.

### Q14 — How are preferred names localised?
**Resolved 2026-08-09, largely by rejecting the premise.** The question assumed `label`
is implicitly English. It is not — it is *notation* for roughly 650 of 668 entities
(`J35` is the same in every language, and so, mostly, are nicknames), so a language
dimension on `label` would be empty or meaningless almost everywhere. The labels that
are genuinely language-bound are the handful of ecotypes, communities and taxa.

So: `label` stays language-neutral, and **a localised preferred name, when one exists,
is a sparse `names.tsv` row** — `type = preferred` plus the existing `language` column,
at most one per `(entity, language)`, with `label` as the fallback for every language
without a row. Consumers display the viewer's-language row if present, else the label.
Neither of the issue's two options: no language column on `label`, and no wholesale move
of preferred names into `names.tsv` (the diff-readability hit ADR-0011 already
rejected). See [ADR-0020](../decisions/0020-localised-preferred-names-are-name-rows.md).

Implementation is deferred until the first real row, which is safe *because* the shape
is decided — the change is additive, so there is no migration to get ahead of, which was
the only urgency the question claimed. Worth noting: the Spanish pressure that prompted
this attaches to humpback *signal* labels, which are the signals repository's; the
likelier demand here is Coast Salish names (qwe'lhol'mechen), and those can be recorded
today as `common` + language. Q14 only ever gated marking one *preferred*.

### Q16 — Should the register hold parentage?
**Resolved 2026-07-28.** Yes, in `data/parentage.tsv`, as edges rather than as
`mother_id` / `father_id` columns. Parentage is identity rather than encounter, and it
passes [ADR-0007](../decisions/0007-no-observations.md)'s own test — the claim needs
neither a date nor a place — so the ADR that exists to refuse new facts does not refuse
this one. Edges because provenance is per claim: maternity comes from a census and
paternity from genetics, and one `source_id` per entity row cannot carry both.

Membership is *not* derived from parentage, which is what SalishSea.io does. That model is
arguably better and was rejected on data rather than on principle — parentage is sparse
and Bigg's have effectively none, so derived matrilines would be empty exactly where the
roster is largest. Instead the two are asserted independently and checked against each
other: a mother and her calf should share a matriline, and a warning fires when they do
not. See [ADR-0016](../decisions/0016-parentage.md).

The false claim that parentage was "implied by matriline membership" is gone from
`scope.md` and `competency-questions.md`, where "who is this animal's mother?" is now C13
rather than an entry on the deliberately-unanswerable list.

### Q17 — Whose job is designation normalization?
**Resolved 2026-08-09. The register's — but as a comparison rule, not normalization.**
The word had fused two questions, and separating them was most of the answer: nothing the
register publishes is ever rewritten (`T090` keeps its zero, `Bigg's` its apostrophe);
what consumers need is a rule for when two *spellings* name the same entity. The register
now publishes that rule — the **fold**: lowercase, drop apostrophes and hyphens, collapse
whitespace, strip leading zeros in each digit run — with executable test cases in
`dist/fold_test.tsv` that a conforming implementation must reproduce exactly. See
[ADR-0019](../decisions/0019-names-are-compared-by-folding.md).

Two findings from testing the rule against the live register shaped it:

- **A trailing `s` must never fold.** `T090s` names the matriline and `T090` its
  matriarch — 126 such pairs exist — so folding the plural resolves a name to the wrong
  animal. This is the one clause SalishSea.io's `normalize_designation()` must drop when
  it reconciles (ADR-0012); its zero-and-case handling already agrees with the fold on
  every equivalence class, differing only in direction (it pads where the fold strips).
- **The safety guarantee is not uniqueness.** The vocabulary is honestly ambiguous —
  every matriline's bare designation is also its matriarch's label, and `Gull` names both
  T097 and Laridae — so the validator instead enforces that *folding may not merge what
  exact spelling keeps apart*. C2's honest answer is sometimes two candidates.

C2's "answerable: yes" is now a tested claim: the `T090s` / `J-35` / `Biggs` trio is
pinned to permanent identifiers in `bin/validate.py`, and the enumeration burden the
question complained about is gone — case, padding, hyphen and apostrophe variants need
no `names.tsv` rows.

### Q18 — Adopt the confidence/verification split in the annotation shape
**Closed 2026-07-29 by relocation, not by answer.** The work is real and still to be done;
it is not this repository's, and holding it open here was the last place this repo was
still acting as owner of a shape it disclaims owning four times over. See
[ADR-0018](../decisions/0018-annotation-semantics-belong-to-consumers.md).

The substance, carried over so nothing is lost in the move:

- SalishSea.io's `public.identifications` separates *evidence* (what the claim rests on)
  from *method* (how it was captured), and separates the **asserter's confidence** from the
  **dataset's verification status** (`candidate` / `validated` / `rejected`).
  [ADR-0009](../decisions/0009-uncertainty-on-the-annotation.md)'s sketch collapses the
  last two, so a moderator's `possible` that a curator later confirms has nowhere to land.
  The shipped model is better and the sketch now defers to it.
- **A signal must be recordable with no animal named** (from Q7). A moderator may know the
  call type and not the producer. In the shipped model that is an occurrence with zero
  identifications rather than a nullable subject — structurally available, but worth
  confirming the *interface* permits it, because a form that demands a tag produces the
  same bad data as a schema that does.
- The one genuine disagreement is `confidence`: numeric there, a three-value enum in the
  sketch. Possibly not a conflict at all — a CV match has a real score and a listening
  moderator does not.

Where it goes: an amendment to SalishSea.io's decision
[013](https://github.com/salish-sea/salishsea-io/blob/main/docs/decisions/013-orcasound-acoustic-occurrences.md),
or a successor there. ADR-0018 carries the risk that it never gets filed as its own open
question.

### Q19 — Is bulk import a supported operation, and how are identifiers assigned?
**Resolved 2026-07-28.** Yes, as a stated exception to ADR-0001's reviewable-diff premise:
a bulk import is reviewed as a *transformation*, with the importing script committed and
scrutinised in place of its output. It must be deterministic and idempotent, every row
carries its `source_id` so the import stays identifiable and reversible, and the script
comments every judgement it makes. Identifiers come from dedicated blocks, assigned by
sorted designation and reused on re-run. See
[ADR-0015](../decisions/0015-bulk-import.md).

### Q20 — `status.tsv` is append-only with no way to retract a claim
**Resolved 2026-07-27.** `status.tsv` gains a `recorded` column — when *we* wrote the row
down, distinct from `effective` (when it became true) and `asserted_on` (when the source
said so). Current status is the row with the greatest `(recorded, effective)`; ties are a
validation error; retraction without a replacement is an appended `unknown`.

Ordering by `effective` alone was the trap: a correction usually carries an *earlier*
valid-time than the claim it corrects. And `recorded` is a column rather than git history
because raw-URL consumers — which ADR-0001 explicitly supports — have no git, so a
precedence rule requiring `git log` is one most consumers cannot follow.

See [ADR-0006](../decisions/0006-valid-time-in-data-assertion-time-in-git.md), section
"Precedence".

### Q21 — Absence and false-positive claims block a consumer today
**Resolved 2026-07-27, mostly by declining it.** Reading the live bouts, the requested
`unconfirmed` / `false-positive` vocabulary turned out to be three separate problems:

- `OrcaHello FP at Bush Point` — a real bout. The detector fired on nothing. That is a
  **bout-level flag in OrcaSound**, never a tag, because it names no animal.
- `Passing boat noise`, category `biophony` — a **wrong value in an existing field**. Fix
  `bout.category`; not a vocabulary question.
- `Mystery squeaks at Port Townsend` — there is a signal, nobody knows whose. **Tag at the
  level you are sure of**, which required a species-level entity. Those now exist as
  `kind = taxon` ([ADR-0008](../decisions/0008-species-identity-is-delegated.md)).

So "unconfirmed" was never a missing modality — it was a missing *entity*. The register's
only remaining contribution is a warning, now in [scope.md](scope.md): a biophony bout may
be about no animal at all, so the absence of tags is not the absence of animals.

### Q25 — Who else can cut a release, and what makes that safe?
**Resolved 2026-08-09. No one else, for now**
([#16](https://github.com/salish-sea/animals/issues/16)). Only this repository's author
cuts releases, and the cost the question named — a consumer waiting on an edition is
waiting on one person's availability — is accepted for the moment.

That makes the "what makes that safe" half moot rather than answered. The machinery
sketched in the question — protected tags, artefacts built only by CI from a reviewed
commit on `main`, an agreement about what a release asserts — is the price of admission
for a second releaser, whenever one is wanted; it is work deferred, not work declined.
Reopen this when adding one, likely alongside Q8, which still owns the separate question
of who reviews the domain content.
