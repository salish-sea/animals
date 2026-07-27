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
