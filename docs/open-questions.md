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

### Q6 — Should the register publish group sizes?
*Owner: S. Veirs, D. Bain.*
A count of living members is derivable from the data. Publishing it is a claim, and a
claim that will sometimes be wrong or out of date in a way that matters publicly. Do we
derive it, publish it, or refuse to?

### Q7 — How do we model a bout where the animal and the sound belong to different species?
*Owner: S. Veirs, and whoever designs the annotation schema.*
Prompted by the real bout `Humpback mimics Bigg's?`. The animal is a humpback; the
signal is characteristic of Bigg's. Any assumption that one tag identifies both the
animal and the sound source breaks here. See [walkthrough.md](walkthrough.md).

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

### Q16 — Should the register hold parentage?
*Owner: S. Veirs, P. Abrahamsen.*
[scope.md](scope.md) and [competency-questions.md](competency-questions.md) both claim
parentage is "implied by matriline membership". **That is false** — a matriline spans
three or four generations, so membership implies descent from the matriarch, not from a
mother. J57's mother is J35, and no walk of `membership.tsv` recovers it; in the seed data
that fact survives only in a free-text `note` the validator ignores.

Two ways out: record `mother_id` on individuals (defensible — parentage is identity, not
occurrence, so [ADR-0007](../decisions/0007-no-observations.md) does not obviously forbid
it), or state plainly that parentage is out of scope and delete the false claim. The first
is what SalishSea.io does, and it *derives* matriline groups from it rather than asserting
them by hand — which is arguably the better model.

The false claim should be corrected either way, and immediately: it is the kind of error
a whale researcher notices in the first five minutes.

---

## For the informatics reviewers

### Q5 — Do consumers store redundant ancestors, or derive them?
*Owner: P. Abrahamsen.*
The walkthrough bout is tagged with both an ecotype and two pods, but the pods already
imply the ecotype. Should OrcaSound store what the moderator picked (redundant, honest,
larger) or normalise to the most specific term and derive the rest (smaller, but loses
the fact that the moderator asserted the ecotype independently)? Leaning toward storing
what was picked.

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

### Q18 — Reconcile the annotation schema with SalishSea.io's identifications model
*Owner: P. Abrahamsen.*
[ADR-0009](../decisions/0009-uncertainty-on-the-annotation.md) specifies `certainty` and
`evidence` and claims this repository is "the shared document" for the annotation shape.
An earlier pass at the same problem — the SalishSea.io catalogue, same author — shipped a
different one: `identification_evidence`, `identification_method`, and
`identification_status` (candidate / validated / rejected).

That model separates *evidence* from *method*, and separates the **asserter's confidence**
from the **dataset's verification status**. ADR-0009 collapses the last two, so a
moderator's `possible` that a curator later confirms has nowhere to land. On this point
the earlier model is better and the newer one should adopt it — the task is picking the
better of two designs, not reconciling two parties. Do it before either has data.

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
