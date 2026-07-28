# Start here

**For a first read, especially a short one.** Everything else in this repository is
elaboration.

## What is being proposed

A shared list of the animals and groups that OrcaSound and SalishSea.io both need to name
— Southern Residents, Bigg's, pods, matrilines, individuals — each with a permanent
identifier, so that what a moderator knows survives the trip between systems.

Right now a bout is named `SRKW signals at PT (J+K +L? pods)` and everything in that
string is locked in free text. A downstream system can only guess at it by pattern
matching, which throws away the judgement that was expensive to produce.

## What changed from the original proposal

[orcasound/orcasite#1001](https://github.com/orcasound/orcasite/issues/1001) proposed
SalishSea.io as a service that apps query for current taxonomy. This is **published
instead of served**: dated editions that consumers hold, rather than an endpoint.

The content is the same; the timing moves. Reconciling CWR, MERS, finwave and DFO happens
when a curator prepares an edition, not inside a request. The main reason is that a bout
tagged in 2025 has to still mean what it meant in 2025, which a live service cannot
promise. [ADR-0014](../decisions/0014-a-publication-not-a-service.md) has the full
argument, and it is the one design departure worth disagreeing with early if you are
going to.

## If you read three things

1. **[definitions/](../definitions/)** — six terms: ecotype, community, clan, pod,
   matriline, membership. Ten minutes. These matter more than anything technical here,
   because two curators applying a term differently produces inconsistent data that no
   amount of engineering repairs later.
2. **[docs/competency-questions.md](competency-questions.md)** — the questions the
   register must be able to answer. If one is missing or wrong, everything downstream is
   wrong.
3. **[docs/open-questions.md](open-questions.md)** — the questions *for you*, below.

## The questions only a domain expert can answer

Ordered by how much they block. The first four should be settled before anything is
tagged, because tagging against them and then changing our minds means re-tagging.

| | Question | Why it blocks |
|---|---|---|
| **[Q1](open-questions.md)** | Is "community" a rank we need, or is it the same thing as ecotype? | Both are in the data now and may be redundant. Until it is settled, nothing rolls up from a pod to an ecotype — a gap the validator currently reports as a warning. |
| **[Q2](open-questions.md)** | Are the Southern Residents one acoustic clan, or more? | Asserted with low confidence. If moderators would never tag at clan level, the rank should be dropped rather than maintained. |
| **[Q3](open-questions.md)** | Which source is authoritative for Bigg's — MERS, finwave, DFO? And what happens when two disagree? | Until the second half has an answer, the register cannot take in more than one Bigg's source. |
| **[Q15](open-questions.md)** | How does CWR's published census list L87 during the years he travelled with J pod? | The register defines membership as genealogical, so L87 is L pod permanently. If CWR prints him under J pod, curators need a stated rule for transcribing an associational roster — otherwise two curators will diverge silently. |
| [Q4](open-questions.md) | Populate Northern Residents and offshores now, or later? | Curation effort against moderator coverage. |
| [Q6](open-questions.md) | Should the register publish group sizes? | A count is derivable; publishing it is a public claim that will sometimes be wrong. |
| [Q7](open-questions.md) | How do we model `Humpback mimics Bigg's?` — a real bout where the animal and the sound belong to different species? | Breaks any assumption that one tag identifies both. |
| [Q9](open-questions.md) | Is there anything in scope that should not be in a public repository? | Naming programmes, cultural significance, catalogues that withhold detail. |
| **[Q22](open-questions.md)** | Is a T-number lineage the right grouping? The sheet seems to record two levels — a lineage, and travelling sub-groups within it — and the import flattens them to one. | 132 derived groups depend on the answer. |
| [Q13](open-questions.md) | Is `J17s` the canonical written form for a matriline, or would a catalogue write `T090 matriline`? | Display is the consumer's business; this is asking what the community actually writes. |
| [Q23](open-questions.md) | What are the `AM3`-style Alaska/California designations, and what catalogue are they from? | They are searchable names now; they belong in `mappings.tsv` as a crosswalk. |

## Things to know before you judge the data

- **The Bigg's data is imported, not curated.** 510 individuals and 132 matrilines came
  from the community designation sheet by script
  ([ADR-0015](../decisions/0015-bulk-import.md)). Nobody has checked them against a
  catalogue. The individuals are a fairly direct transcription; **the groupings are
  derived and are the least confident thing here** — see [Q22](open-questions.md).
- **The Southern Resident data is illustrative.** Those rows are marked `SEED` and exist
  so the schema is concrete and the walkthrough has something to point at. Errors in them
  are expected; errors in the *shape* are what to look for.
- **Nothing is ratified.** All fifteen decision records are `Proposed`. They are written
  as arguments to disagree with, not as conclusions.
- **Identifiers look unfriendly on purpose.** `SSA:0000101` rather than `J35`, because a
  meaningful identifier becomes a lie when the thing it names changes. The name sits right
  next to it and can be changed freely.

## What this deliberately refuses to hold

No sightings, no locations, no photographs, no health data, no parentage (yet — see
[Q16](open-questions.md)), and no sound vocabulary. Signal types stay in
[signals-srkw](https://github.com/orcasound/signals-srkw). The boundaries are argued in
[docs/scope.md](scope.md); the load-bearing one is
[ADR-0007](../decisions/0007-no-observations.md).
