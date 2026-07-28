# Open questions

**Audience: everyone, but sorted so you can find yours.**

This is distinct from `decisions/`. An ADR records something we have *decided*, however
provisionally. This file records things we have **not** decided and, crucially, **who
can decide them**. It is the shortest path to useful review: rather than reading a repo
and reacting, a reviewer can answer the questions addressed to them.

Every question has an owner. A question with no owner is a question that will not get
answered.

---

## For the scientific reviewers

### Q1 — Is "Southern Resident" an ecotype, or a community of the Resident ecotype?
*Owner: S. Veirs, D. Bain.*

Community is not redundant with ecotype — in the standard Northeast Pacific literature it
sits below it:

```
ecotype  ⊃  community  ⊃  clan  ⊃  pod  ⊃  matriline  ⊃  individual
```

where the ecotypes are **resident**, **Bigg's** and **offshore** (prey specialisation,
genetics, morphology, no interbreeding), a **community** is the set of pods that associate
with one another, and a **clan** is the set of pods sharing an acoustic repertoire. The
Northern Resident community contains three clans; the Southern Resident community contains
one, J clan.

**So the real problem is that the register has "Southern Resident" entered twice, once at
the wrong rank.** `SSA:0000001` calls it an ecotype and `SSA:0000010` calls it a
community. Under the reading above, the ecotype is *Resident* — which does not exist in
the register at all — and Southern Resident is a community within it.

That also explains the graph break. Bigg's connects to *Orcinus orca* because Bigg's
genuinely is an ecotype. The Southern Resident branch does not connect, because the
community's actual parent — the Resident ecotype — is missing. The break is a symptom of
the category error, not a separate problem.

**But there is a real conflict of usage, and it is yours to settle.** The #1001 comment
proposing this work says "the *Orcinus orca* species has 4 ecotypes that have occurred
within Orcasite's ecoregion (SRKW, Biggs, offshore, NRKW)" — treating SRKW and NRKW as
separate ecotypes. That is common in management and conversation (NOAA's listing unit is
the Southern Resident DPS), and it conflicts with the stricter reading, in which
SRKW-vs-NRKW is a *community* distinction inside one ecotype while Bigg's-vs-resident is
an *ecotype* distinction. Treating all four as parallel ecotypes flattens a real
difference.

Two ways to go:

**(a) Strict.** Add a `Resident` ecotype; merge `SSA:0000001` into `SSA:0000010` as a
community beneath it; Northern Residents become a sibling community. The graph connects
and the ranks mean one thing each. Costs: "SRKW" is then a community, which will read
oddly to anyone used to calling it an ecotype.

**(b) Colloquial.** Keep SRKW as an ecotype, drop `community` as a rank entirely, and
attach J clan directly to the SRKW ecotype. Simpler, matches how people talk, and gives up
the ability to say that Northern and Southern Residents are the same ecotype.

The register does not need a fixed hierarchy
([ADR-0004](../decisions/0004-rank-is-an-open-vocabulary.md)), so either works
structurally. This is a question about what the words should mean, which is why it is
yours.

*Two things to know before answering.*

**The species question does not have to be settled first.** Resident and Bigg's killer
whales have been proposed as *Orcinus ater* and *Orcinus rectipinnus*, and D. Bain holds
that keeping them as one species is not scientifically justifiable. Neither NCBI Taxonomy
nor WoRMS has adopted the split — both checked 2026-07-28; WoRMS has only *Orcinus orca*,
AphiaID 137102, `accepted` — so there is not yet an identifier to point a crosswalk at.
The register does not need an opinion:
[ADR-0008](../decisions/0008-species-identity-is-delegated.md) makes `taxon_id` a record of
where the authorities place a thing, not a belief, and the ecotype entities are
first-class regardless. Adoption later is a two-row edit, not a restructuring.

**But it is evidence for (a).** Under a species split, "resident" is the species and SRKW
and NRKW are populations within it — which is option (a)'s shape. Option (b), treating
SRKW as an ecotype parallel to Bigg's, is merely colloquial today and would be actively
wrong if the split were adopted. So (a) is robust to both outcomes and (b) is not.

### Q2 — Are the Southern Residents one acoustic clan or more?
*Owner: S. Veirs.*
Seed data asserts a single J clan containing J, K and L pods. Stated with low confidence
and needs confirmation. If clans are not useful to moderators, the rank could be dropped
entirely — a rank nobody tags with is dead weight.

### Q3 — Which source is authoritative for Bigg's?
*Owner: S. Veirs.*
MERS, finwave, DFO, and the Bigg's nickname spreadsheet have all been mentioned. Two
sub-questions: (a) who do we mirror, and (b) what happens when two of them disagree
about a matriline assignment? Until (b) has an answer, the register cannot ingest more
than one Bigg's source.

### Q4 — Should Northern Residents and offshores be populated now or later?
*Owner: S. Veirs.*
They are in scope but empty. Populating them costs curation effort; leaving them out
means a moderator who hears one has nothing to pick.

### Q9 — Are there animals or names we should *not* publish?
*Owner: S. Veirs, for the part that is still open.*
Some individual names come from naming programmes with donor relationships or cultural
significance. Some catalogues withhold detail deliberately.

**Mostly already answered.** `salishsea-io/docs/rights-policy.md` and its decision 004 are
prior work by the same author on this exact question, including the Bigg's nickname
material — naming *facts* are public, the prose "story" behind a nickname is not, and that
column is already restricted from anonymous access there. That analysis should be ported
here rather than redone.

What remains for the scientific reviewers is narrower: is there anything **in scope for
this register** — an animal, a designation, a grouping — that should not appear in a public
repository at all?

### Q22 — Is a T-number lineage the right grouping, or does the sheet group differently?
*Owner: S. Veirs, D. Bain.*
**The least confident thing in the register.** The import derives matrilines from the
designation prefix: `T023`, `T023D`, `T023D3`, `T023C`, `T023C3` all land in one group
labelled `T023s`.

The sheet groups differently. Blank rows separate sub-blocks — `T023` with the T023D line
in one, the T023C line in another — while a `Known as the Motley Crew` heading spans both.
So the sheet appears to record two levels: a lineage, and travelling sub-groups within it.
The register currently flattens them to one.

Three questions: (a) is `T023s` a matriline, or a lineage containing several? (b) if both
levels are real, which one does a moderator tag when they hear a group? (c) are the "Known
as" names attached to the right level? They are currently `common` names on the derived
group, which is a guess.

132 groups were derived this way, so getting it wrong is 132 wrong groups — though the
individuals underneath are unaffected.

### Q23 — What are the Alaska/California designations, and where do they belong?
*Owner: S. Veirs.*
The sheet's second column carries designations like `AM3`, `AM5`, `AM34` alongside the
BC/WA T-numbers. They are currently imported as `hidden` names so they resolve in search,
which is a holding position: they are really identifiers in *another catalogue*, and the
right home is `mappings.tsv` with that catalogue's namespace and a match predicate.

What is that catalogue, and does it have a citable identifier scheme?

### Q13 — Is the plural the canonical written form for a matriline?
*Owner: S. Veirs, D. Bain.*
The register records `J17s` and `T090s` as the **preferred name** for matrilines,
following ordinary usage, with the bare designation and `T090 matriline` kept as
searchable hidden names.

The question is what the community's canonical written form actually is — not what looks
best in a menu. How a consumer renders it in a pick list is that consumer's business
([ADR-0011](../decisions/0011-label-is-a-preferred-name.md)), so please answer for the
writing, not the UI. Identity does not depend on the answer
([ADR-0003](../decisions/0003-one-identifier-space.md)), so it is cheap to change now and
cheap to change later.

### Q15 — What does a curator do when a published roster is associational?
*Owner: S. Veirs, with D. Bain.*
[ADR-0005](../decisions/0005-membership-is-genealogical.md) defines membership as
genealogical: L87 (Onyx) was born to L32 and is therefore an L pod animal permanently,
regardless of his years travelling with K and then J pod.

**The question:** how does the Center for Whale Research's own published census list L87
during those years — under L pod, or under J pod? If CWR lists him under J pod, then
ADR-0005 makes this register systematically contradict the printed roster of the source
it says it mirrors, for an unknown number of animals.

That would not necessarily make ADR-0005 wrong, but it turns it from a modelling choice
into a **data-entry rule that curators need spelled out**: when a source roster records an
associational assignment, what does the curator enter, and what do they record about the
discrepancy? Without that rule, two curators transcribing the same census table will
diverge silently — the failure mode [definitions/README.md](../definitions/README.md)
calls unrepairable.

Note that SalishSea.io's catalogue took the opposite position in code, with a
`membership_basis` of `maternal` / `association` / `curated`. See
[ADR-0012](../decisions/0012-relationship-to-the-salishsea-io-catalogue.md).

---

## For the informatics reviewers

### Q8 — Who is the named editor, and who reviews the domain content?
*Owner: P. Abrahamsen, to resolve with S. Veirs.*
Partly answered: this work is funded, and the schema/tooling side has an owner. Two gaps
remain, and they are different from the one originally filed.

**A scientific reviewer of record.** `CODEOWNERS` marks `definitions/`, `entities.tsv`,
`membership.tsv` and the rest as needing domain review, then assigns them all to a software
reviewer — so domain content currently merges with no domain review at all. The obvious
candidates are S. Veirs and D. Bain. Adding either to `CODEOWNERS` would start
auto-requesting reviews, which is worth agreeing with them first rather than springing on
them; Scott is on sabbatical until 1 October.

**What happens after the funded period.** Roster maintenance is a census-cadence
obligation that outlives any particular engagement. If there is no answer, the design
should change: publish an `as_of` date on every artefact and advertise staleness loudly
rather than imply a currency the register does not have. That is a good idea regardless,
and cheap.

### Q25 — Who else can cut a release, and what makes that safe?
*Owner: P. Abrahamsen, to resolve with S. Veirs.*

A release is a CalVer tag push ([ADR-0013](../decisions/0013-distribution.md)), and today
only this repository's author can make one. During active development the register may be
tagged several times a day, so a consumer waiting on an edition is waiting on one person's
availability. S. Veirs is the obvious second.

Widening it is not merely a permissions change. The tag is what a consumer pins and what
`register_edition` records
([ADR-0006](../decisions/0006-valid-time-in-data-assertion-time-in-git.md)), so whoever
can push a tag can publish an artefact under the register's name. Making that safe is
presumably some combination of protected tags, artefacts only ever built by CI from a
reviewed commit on `main`, and an agreement about what a release *asserts* — which today
is nothing beyond "the validator passed".

Distinct from Q8, and deliberately so: the person who can publish an edition and the
person who reviews its domain content need not be the same, and probably should not be.

### Q10 — Is `SSA:` a safe prefix?
*Owner: P. Abrahamsen.*
Chosen for "Salish Sea Animals". Not checked against
[Bioregistry](https://bioregistry.io/) or any other prefix registry. Cheap to change
now, expensive after the first external system stores one.

### Q24 — Does releasing the register republish the Bigg's sheet?
*Owner: P. Abrahamsen.*
D-21 in `salishsea-io/docs/rights-policy.md` §7.1 concludes that the sheet's factual
content is uncopyrightable and freely usable, but that **the selection and arrangement is
the maintainer's compilation**, and that "we do not republish the sheet wholesale as a
product; the mirror is an internal baseline for change-detection and seeding."

That determination was made for a mirror inside an application. This register *publishes
release artefacts* — `register.db`, a TSV tarball, permanent download URLs — containing
510 individuals derived from that sheet. Whether that is a different arrangement of
uncopyrightable facts or a republication of the compilation is a genuine question, and it
is the author of both who has to answer it.

Until it is answered, [LICENSE](../LICENSE) already says the data is unlicensed and must
not be redistributed as a dataset, so importing is safe and *releasing* is the gated step.
Note also that D-21 requires the maintainer to be credited wherever nickname facts are
surfaced; `sources.tsv` does that, and any consumer displaying a nickname inherits the
obligation.

### Q17 — Whose job is designation normalization?
*Owner: P. Abrahamsen.*
[Competency question C2](competency-questions.md) ("a moderator typed `T090s` / `J-35` /
`Biggs` — which entity is that?") is marked answerable, but only by exact string match
against hand-enumerated rows in `names.tsv`. For 649 Bigg's individuals with inconsistent
zero-padding (`T065A5` vs `T65A5`), hyphenation, apostrophes and plural forms, enumerating
every spelling is unbounded.

SalishSea.io already has `normalize_designation()` doing this in SQL. OrcaSound will need
the same rule. Either the register publishes the normalization rule plus test cases (and
perhaps a `dist/` lookup of normalized form → identifier), or it states that matching is
a consumer concern and C2 is downgraded. Two implementations that disagree is precisely
the failure this register exists to prevent.

### Q18 — Adopt the confidence/verification split in the annotation shape
*Owner: P. Abrahamsen.*
[ADR-0009](../decisions/0009-uncertainty-on-the-annotation.md) sketches an annotation
carrying `certainty` and `evidence`. An earlier pass at the same problem — the
SalishSea.io catalogue, same author — shipped a different shape:
`identification_evidence`, `identification_method`, and `identification_status`
(candidate / validated / rejected).

That model separates *evidence* from *method*, and separates the **asserter's confidence**
from the **dataset's verification status**. ADR-0009's table collapses the last two, so a
moderator's `possible` that a curator later confirms has nowhere to land. The earlier
model is better on this point.

**This is agreed, not disputed.** ADR-0009 says so itself, and in the same breath declines
the ownership this question used to accuse it of: the annotation "constrains **consumers**,
not this repository", and the ADR "does **not** make this repository the owner of
annotation semantics". So what is left is not a reconciliation between two positions but a
piece of work — carrying the split into the sketch — and it should be done before either
system has data. Where the resulting shape is *implemented*, and who decides its final
form, is the consuming system's business.

**A signal must also be taggable with no animal tag** (from Q7, resolved). A moderator may
know the call type and not the producer: `Humpback mimics Bigg's?` is exactly that case.
If every signal annotation requires an animal, the honest answer is unavailable and the
nearest available one is a species claim nobody intended — tagging `Bigg's` for a sound
suspected to have come from a humpback. This is a data-quality risk to the register even
though it is not a register question, because the bad tags land in annotations that cite
register identifiers.

### Q14 — How are preferred names localised?
*Owner: P. Abrahamsen.*
`names.tsv` has a `language` column; `entities.tsv.label` does not, so the preferred name
is implicitly English. Scott has raised the possibility of Spanish-language signal labels
for a future humpback vocabulary, and the same pressure would apply here. Options: add a
language dimension to `label`, or move preferred names into `names.tsv` as a typed row
and accept the hit to diff readability. Not urgent, but it is a schema change and worth
deciding before there is much data. See
[ADR-0011](../decisions/0011-label-is-a-preferred-name.md).

### Q12 — How do the two repositories reference each other?
*Owner: P. Abrahamsen, S. Veirs.*
`signals-srkw` currently copies ecotype and pod labels rather than referencing them.
Fixing that requires a convention for cross-repository identifier references and a
decision about whether the signals vocabulary declares a dependency on a specific
edition of this register.

---

## Answered

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

### Q7 — How do we model a bout where the animal and the sound belong to different species?
**Resolved 2026-07-28, by declining it.** The question was an artefact of how the bout was
written up, not a property of the bout. `Humpback mimics Bigg's?` is a hypothesis — a
signal characteristic of Bigg's, suspected to have come from a humpback. **A call type
being characteristic of Bigg's is a regularity about who usually produces it, not a
property of the sound**; sounds carry no species. The walkthrough had promoted
"characteristic of" to "belongs to", which manufactured a second species and with it the
appearance of a modelling problem. What was recorded is one animal, identified with low
confidence — [ADR-0009](../decisions/0009-uncertainty-on-the-annotation.md) — plus a call
type, which is the signals vocabulary's business. The register was never asked to identify
sound sources, so nothing here bears on it.

One real requirement survives, and it is the annotation schema's, not the register's: a
signal must be taggable with no animal tag, so that a moderator who knows the call type
and not the producer is not forced to name an animal. Folded into Q18.

### Q19 — Is bulk import a supported operation, and how are identifiers assigned?
**Resolved 2026-07-28.** Yes, as a stated exception to ADR-0001's reviewable-diff premise:
a bulk import is reviewed as a *transformation*, with the importing script committed and
scrutinised in place of its output. It must be deterministic and idempotent, every row
carries its `source_id` so the import stays identifiable and reversible, and the script
comments every judgement it makes. Identifiers come from dedicated blocks, assigned by
sorted designation and reused on re-run. See
[ADR-0015](../decisions/0015-bulk-import.md).

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
