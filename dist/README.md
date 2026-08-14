# Generated artefacts

Nothing here is hand-edited. It is generated from `data/` by:

```sh
python3 bin/validate.py --write-dist
```

and CI fails if these files differ from a fresh build.

These are the **derived facts**, published so that no consumer reimplements them and two
consumers cannot disagree. Each answers a competency question — see
[docs/competency-questions.md](../docs/competency-questions.md).

| File | Answers |
|---|---|
| `ancestor.tsv` | C5, C6 — the transitive closure of membership, precomputed |
| `current_status.tsv` | C4 — current life status, applying the `(recorded, effective)` precedence rule from ADR-0006 |
| `searchable_name.tsv` | C2 — preferred names and every alternate, in one place, each carrying the entity's label, kind and rank so two candidates can be told apart |
| `retired.tsv` | C9 — deprecated identifiers, marked `automatic` or `needs-human` |
| `fold_test.tsv` | C2 — the name-comparison fold of [ADR-0019](../decisions/0019-names-are-compared-by-folding.md), as executable test cases; a conforming implementation reproduces the `folded` column exactly |
| `structure.md` | A picture of the register's shape, as Mermaid — which GitHub renders inline |

[`structure.md`](structure.md) is the fastest way to see what the register currently
looks like. It draws every membership edge collapsed to the *level* of the things it
connects, so 661 entities become a handful of nodes — and any level with no path upward
is a break in the graph, visible at a glance.

`current_status.tsv` is the one that most earns its place: ordering by `effective` alone
is wrong, and shipping the answer means nobody has to discover that.

Everything here is derived from **one edition** of the register. Copying a derived fact
into your own tables therefore caches something that moves: resolving
[Q1](../docs/open-questions.md) will reparent every Southern Resident entity and
`ancestor.tsv` will change with it. That is not a reason to avoid copying — it is a reason
to record the tag and digest you built against
([ADR-0006](../decisions/0006-valid-time-in-data-assertion-time-in-git.md),
[ADR-0013](../decisions/0013-distribution.md)), so you can tell whether what you cached is
still what the register says.

`register.db` — the SQLite build, with the same views live — is **not** committed here. It
is a release asset, because a binary in git is heavy and unreviewable. See
[ADR-0013](../decisions/0013-distribution.md).
