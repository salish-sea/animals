# Generated artefacts

Nothing in this directory is hand-edited. It is built from `data/` and committed so that
consumers can fetch a raw URL without running a build.

Not yet implemented. Planned:

- `register.json` — the whole register in one file
- `closure.tsv` — precomputed ancestors, so a consumer tagging a matriline can filter by
  ecotype without walking the graph themselves. Published as data rather than left to
  each consumer, because otherwise every consumer implements it slightly differently.
- `register.skos.ttl` — SKOS serialisation for anyone who wants it

Each artefact should embed the commit it was built from, so an exported snapshot is
self-describing.
