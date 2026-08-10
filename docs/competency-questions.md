# Competency questions

**Audience: everyone — and the best single document for a scientific reviewer to
attack.** No schema knowledge is needed to read it.

A competency question is a question the register must be able to answer. The practice
comes from ontology engineering, where it is used to decide when a model is finished:
if a question on the list can't be answered, something is missing; if a field answers no
question on the list, it probably shouldn't exist.

They are also the acceptance tests. Each one should eventually have a query in `bin/`
that answers it — **and until it does, the "answerable" column is an unverified claim.**
It was wrong for C5 and C6 on the day it was written, which is the argument for
generating this table rather than maintaining it by hand.

## Rules for this list

- A question belongs here only if a **real system** asks it. Add the asker.
- If answering a question needs data we've declared out of scope, that's a scope
  conflict — resolve it in [scope.md](scope.md), don't quietly widen the schema.

## Confirmed

| # | Question | Asked by | Answerable today |
|---|---|---|---|
| C1 | What is the current preferred label for this identifier? | Both, every display | Yes |
| C2 | A moderator typed "T090s" / "J-35" / "Biggs" — which entity is that? | OrcaSound autocomplete | Yes — fold the query and compare against `dist/searchable_name.tsv` ([ADR-0019](../decisions/0019-names-are-compared-by-folding.md)); this trio is pinned as an acceptance test in `bin/validate.py`. Sometimes the honest answer is two candidates (`T090` is a matriline's bare designation *and* its matriarch's label) — show both |
| C3 | Which individuals belonged to J pod at the time of this bout? | SalishSea.io map | Yes |
| C4 | Was this individual alive on this date? | SalishSea.io, data QA | Yes |
| C5 | Is this entity a Southern Resident? (at any depth below the ecotype) | Both, filtering | **Partly** — pods and below reach the community, not yet the ecotype, pending [Q1](open-questions.md) |
| C6 | This bout is tagged with a matriline. Which pod and ecotype does that roll up to? | SalishSea.io ingest | **Partly** — reaches the community; the ecotype level awaits [Q1](open-questions.md) |
| C7 | What did identifier X mean, given that a bout was tagged in March 2026? | Reinterpreting old annotations | Yes, via git |
| C8 | Which entities changed since the last time we synced? | Both, incremental ingest | Yes, via git |
| C9 | Identifier X is deprecated — what should we use instead, and can we substitute automatically? | Both, migration | Yes, `deprecations.tsv` |
| C10 | Who says so, and when did they say it? | Everyone, always | Yes, `source_id` |
| C11 | A moderator heard an orca but couldn't place the ecotype. What do they tag? | OrcaSound, ~30% of biophony bouts | Yes — the `Orcinus orca` taxon entity, with no ecotype alongside |
| C12 | This bout is a humpback / sea lion / harbour seal. What do they tag? | OrcaSound, SalishSea.io | Yes — `kind = taxon` entities |
| C13 | Who is this animal's mother? | SalishSea.io profile pages, curators checking a roster | Yes, `parentage.tsv` — but recorded for very few animals so far. Absent means *not recorded*, never *no mother*. It is not recoverable from membership: a matriline spans generations, so membership implies descent from the matriarch. See [ADR-0016](../decisions/0016-parentage.md) |

## Open — the model does not answer these yet

| # | Question | Asked by | Blocked on |
|---|---|---|---|
| O2 | Which hydrophone locations is this group plausibly detectable at? | OrcaSound UI hinting | Out of scope here — this is occurrence data |
| O3 | Two sources disagree about this animal's matriline. What do we publish? | Curators | [ADR pending](open-questions.md) Q3 |
| O4 | Which signal types are valid for this animal? | OrcaSound moderator UI | Cross-repo dependency on signals-srkw |

## Deliberately unanswerable

Listed so they stop being raised. Each is a question the register is *designed* not to
answer, with the reason.

| Question | Why not |
|---|---|
| Where was this animal on this date? | Occurrence data. Belongs in the consuming systems. |
| How many individuals are in this group right now? | Derivable, and deliberately not published. The roster is knowingly incomplete, and the derivable count is one of descent rather than of a travelling group. A consumer that computes one owns the claim. See [ADR-0017](../decisions/0017-no-counts.md). |
| Is this animal healthy / pregnant / emaciated? | Health data, out of scope, and sensitive. |
| What does this animal's call sound like? | The sound vocabulary's job. |
| Which animals were travelling together? | Association, not membership. See [ADR-0005](../decisions/0005-membership-is-genealogical.md). |
