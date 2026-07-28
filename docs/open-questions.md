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

### Q1 — Is "community" a rank we need, and how does it relate to ecotype?
*Owner: S. Veirs, D. Bain.*
The register currently has both `ecotype` (Southern Resident) and `community` (Southern
Resident community) as separate entities, which may be redundant. Are these the same
thing at different granularity, or genuinely different concepts? If redundant, one
should go before anyone tags anything.

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
*Owner: S. Veirs.*
Some individual names come from naming programmes with donor relationships or cultural
significance. Some catalogues withhold detail deliberately. Is there anything in scope
that should not be in a public repository?

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

### Q8 — Who is the named editor?
*Owner: P. Abrahamsen, to resolve with S. Veirs.*
Per [background.md](background.md), neglect is the most likely cause of death. Someone
needs "keeps the roster current" as an explicit responsibility, and `CODEOWNERS` needs
to name them. If nobody will take it, the design should change: the register should
advertise its staleness loudly (an `as_of` date on every published artefact) rather than
imply a currency it doesn't have.

### Q10 — Is `SSA:` a safe prefix?
*Owner: P. Abrahamsen.*
Chosen for "Salish Sea Animals". Not checked against
[Bioregistry](https://bioregistry.io/) or any other prefix registry. Cheap to change
now, expensive after the first external system stores one.

### Q11 — What is the release artefact, and does it need a stable URL?
*Owner: P. Abrahamsen.*
Git tags plus generated files in `dist/` is the current plan, with consumers pinning a
tag. If identifiers should ever be dereferenceable as URLs
(`https://salishsea.io/animals/SSA:0000101`), that is a permanent hosting commitment and
should be decided before anything is published, not after.

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
SalishSea.io has already shipped a different one, governed by its own accepted decision:
`identification_evidence`, `identification_method`, and `identification_status`
(candidate / validated / rejected).

Their model separates *evidence* from *method*, and separates the **asserter's
confidence** from the **dataset's verification status**. ADR-0009 conflates the last two:
a moderator's `possible` that a curator later confirms has nowhere to land. Reconcile
before either has data.

### Q19 — Is bulk import a supported operation, and how are identifiers assigned?
*Owner: P. Abrahamsen.*
[ADR-0001](../decisions/0001-tsv-in-git-as-source-of-truth.md) rests entirely on the
reviewable diff. The first real use of this register is importing ~649 Bigg's individuals
plus the Southern Residents, with their matrilines, names and statuses — a
several-thousand-row pull request nobody will review line by line. Either the premise gets
a stated exception for imports, or the register stays empty, which is failure mode #2 in
[background.md](background.md).

Unanswered: is a scripted import an acceptable `source_id`? Who mints several hundred
identifiers, and how do two concurrent import branches avoid colliding on `SSA:0000106`?
ADR-0002's sequential blocks by kind run out at nine matrilines.

### Q20 — `status.tsv` is append-only with no way to retract a claim
*Owner: P. Abrahamsen.*
[ADR-0006](../decisions/0006-valid-time-in-data-assertion-time-in-git.md) makes
`status.tsv` strictly append-only and CI rejects any modified or removed row. There is no
`supersedes` column, no retraction, and no stated rule for which of two contradictory
rows wins.

Whales presumed dead do get resighted. Append `alive` after `presumed_dead` and no
consumer can determine current status — "latest `effective` wins" fails whenever a
correction carries an earlier valid-time than the claim it corrects, which is the normal
case for a re-dated death. That breaks [C4](competency-questions.md), asked by
SalishSea.io and by data QA.

Recommendation: a `supersedes` column naming the row being retracted, plus one sentence
of precedence rule, plus a validator check. Small, but it changes a table's semantics, so
it should be your call rather than a drive-by fix.

### Q21 — Absence and false-positive claims block a consumer today
*Owner: P. Abrahamsen, S. Veirs.*
[ADR-0009](../decisions/0009-uncertainty-on-the-annotation.md) bans `unconfirmed` and
`false-positive` as terms — correctly — and defers designing the replacement.

But SalishSea.io's accepted decision on ingesting OrcaSound acoustic occurrences needs
exactly that capability: of ~196 bouts, the tail includes OrcaHello false positives and
non-animal sounds mistagged as biophony, and their ingest must exclude them. So the
register currently says "you may not express the thing you need on day one, and we
haven't designed the alternative" — which is failure mode #2 in
[background.md](background.md), caused by us.

Likely shape: an annotation-level `presence` ∈ {present, absent} plus a bout-level
"reviewed, nothing present" marker, so that absence of a tag never has to be read as
absence of the animal. Should be finished rather than deferred.

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

*Nothing yet. When a question is resolved, move it here with the answer and, if it
warranted one, a link to the ADR it produced.*
