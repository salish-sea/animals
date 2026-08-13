# Salish Sea animals

A shared register of the marine mammals that [OrcaSound](https://live.orcasound.net) and
[SalishSea.io](https://salishsea.io) both need to talk about — individuals, the groups
they belong to, and what the words for those groups mean.

**Status: proposed, and under design.** Nothing here is ratified. No row in `data/` has
been verified by a curator. Read [docs/scope.md](docs/scope.md) first, and disagree with
it — that is what this stage is for.

## The problem, in one example

A moderator listens to a hydrophone recording and types:

```
SRKW signals at PT (J+K +L? pods)
```

Everything valuable in that string — Southern Residents, J pod and K pod confidently,
L pod maybe — is locked in free text. The only way another system can use it is to
pattern-match the name, which is fragile, lossy, and discards the moderator's judgement.

This register gives both systems stable identifiers for the animals, so the moderator's
knowledge survives the trip.

## How to review this

**New here, or short on time? [docs/start-here.md](docs/start-here.md).** It covers what
is being proposed, how it departs from the original proposal in
[orcasound/orcasite#1001](https://github.com/orcasound/orcasite/issues/1001), and the nine
questions that need a domain expert — ordered by how much they block.

Otherwise: two groups are reviewing this work and they need different things. Please read
your half; you are welcome to read the other, but nothing in it should block you.

### If you're reviewing the science

Start with the two documents that need domain expertise and no software knowledge:

1. **[docs/competency-questions.md](docs/competency-questions.md)** — the questions this
   thing must be able to answer. If a question is missing or wrong, everything
   downstream is wrong. The best thirty minutes you can spend here.
2. **[definitions/](definitions/)** — what each term means. These matter more than the
   schema: a vague definition produces inconsistent data that no amount of engineering
   can repair later.

Then, if you have time: [docs/walkthrough.md](docs/walkthrough.md) traces one real bout
end to end, and the **[open questions](https://github.com/salish-sea/animals/issues?q=is%3Aissue+is%3Aopen+label%3Ascience-review)**
labelled `science-review` are addressed specifically to you — reply on the issue, no pull
request needed. Answering those questions is the single most useful thing available.
[docs/open-questions.md](docs/open-questions.md) is the index.

Decision records addressed to `Informatics reviewers` are implementation detail. Skip them.

### If you're reviewing the design

[docs/scope.md](docs/scope.md), then [decisions/](decisions/) — twenty records covering the
choices that are expensive to reverse. [docs/background.md](docs/background.md) explains
what we're borrowing from the Gene Ontology and OBO Foundry, what we're deliberately not
taking, and why most projects like this one die.

### Everyone

[docs/glossary.md](docs/glossary.md) is bilingual — terms are marked 🐋 science,
💾 informatics, or ⚖️ both. The ⚖️ ones are the dangerous ones: words both fields use
with different meanings.

## Layout

```
data/           The register. Tab-separated, normative. See ADR-0001.
schema.sql      The constraints, declaratively. Normative. See ADR-0013.
definitions/    What the terms mean. Normative.
decisions/      Architecture decision records.
docs/           Scope, competency questions, walkthrough, glossary, background,
                open questions.
bin/validate.py Loads data/ into SQLite built from schema.sql — the build is the
                validation — then runs the graph checks SQL can't state.
dist/           Generated derived views. Never hand-edited.
```

`dist/` is where the work of *consuming* the register is done once instead of per
consumer: `ancestor.tsv` is the precomputed closure, `current_status.tsv` applies the
life-status precedence rule, `searchable_name.tsv` merges preferred and alternate names.
A release also carries `register.db`, the same data as SQLite, which explains itself:

```sh
sqlite3 register.db 'SELECT sql FROM sqlite_master'
```

| File | Holds |
|---|---|
| `data/entities.tsv` | Every individual and group, with a permanent identifier |
| `data/membership.tsv` | Who belongs to what, genealogically |
| `data/parentage.tsv` | Who bore whom — not recoverable from membership, which spans generations |
| `data/status.tsv` | Life status, append-only |
| `data/names.tsv` | Alternate, historical and hidden names |
| `data/mappings.tsv` | Crosswalks to NCBI Taxonomy, finwave, and other catalogues |
| `data/deprecations.tsv` | Retired identifiers and what replaced them |
| `data/sources.tsv` | Who we got each claim from, and its licence status |
| `data/ranks.tsv` | The available group ranks and their definitions |

## The shape of it

[`dist/structure.md`](dist/structure.md) draws it, generated from the data and rendered
inline by GitHub. In outline:

```
SSA:0000001  Southern Resident (ecotype)
  └─ SSA:0000010  Southern Resident community
       └─ SSA:0000011  J clan
            ├─ SSA:0000020  J pod
            │    └─ SSA:0000030  J17s (matriline)
            │         ├─ SSA:0000105  J17   ← the whale, not the matriline
            │         ├─ SSA:0000101  J35
            │         └─ SSA:0000102  J57
            ├─ SSA:0000021  K pod
            └─ SSA:0000022  L pod
```

Identifiers are opaque on purpose — a readable identifier becomes a lie when the thing
it names changes ([ADR-0002](decisions/0002-opaque-permanent-identifiers.md)). The
preferred name sits next to the identifier, which also keeps diffs reviewable.

That name is the register's claim about what the entity is *called*, not a string to put
in a dropdown ([ADR-0011](decisions/0011-label-is-a-preferred-name.md)). Consumers
compose their own presentation from the label, the rank, and the membership context;
nothing should ever key on a label, because labels are meant to change.

## What it deliberately doesn't do

No sightings, no locations, no photographs, no health data, no genealogy beyond
membership, and no sound vocabulary — signal types live in
[orcasound/signals-srkw](https://github.com/orcasound/signals-srkw). Each boundary is
argued in [docs/scope.md](docs/scope.md); the load-bearing one is
[ADR-0007](decisions/0007-no-observations.md).

## Contributing

Four issue templates cover the common cases: a new entity, a definition question, a data
correction, and — most valuable — a **vocabulary gap**, when a moderator needed to say
something the register couldn't express. Free text is never removed from OrcaSound
bouts precisely so those gaps stay visible.

If you need an identifier today, open a pull request with `source_id = SEED`. Validation
flags it as unverified and nothing breaks. A slow process is the most likely way this
register fails.

```sh
python3 bin/validate.py               # errors fail, unverified rows warn
python3 bin/validate.py --write-dist  # regenerate dist/ (CI checks it is current)
python3 bin/validate.py --strict      # warnings fail too
```

## Versioning

A release is a CalVer tag push, cut on demand — during active development, possibly
several a day. Consumers pin a tag rather than a commit, so tagging often drags nobody
along. Released artefacts hang off permanent URLs — `releases/latest/download/register.db`
for the tip, or a tag for a pinned edition — with `SHA256SUMS` alongside, so a consumer
records the tag *and* the digest it verified
([ADR-0013](decisions/0013-distribution.md)). Releases are CalVer
(`2026.07.1`) rather than SemVer — under the rule that an identifier's meaning never
changes ([ADR-0010](decisions/0010-identifiers-are-never-reused.md)), a breaking change
essentially cannot occur, so a major-version signal has nothing to signal. What consumers
watch instead is `data/deprecations.tsv` and the changelog.

Git history is load-bearing: it is the record of *when we came to believe* each fact
([ADR-0006](decisions/0006-valid-time-in-data-assertion-time-in-git.md)). `main` must
never be force-pushed or rebased.

## Licence

Documentation, schema, and code: [CC BY 4.0](LICENSE) and MIT respectively, per
[LICENSE](LICENSE).

**The data is a separate question and is not yet settled.** Rows derived from external
catalogues carry their source in `data/sources.tsv`, where `license_status` is
`not-yet-requested` for every catalogue we mirror rows from. Redistribution permission has not been
discussed with the Center for Whale Research, MERS, or finwave. Nothing here should be
redistributed as a dataset until that is resolved.

## Origins

[orcasound/orcasite#1001](https://github.com/orcasound/orcasite/issues/1001) and the
discussion that followed.
