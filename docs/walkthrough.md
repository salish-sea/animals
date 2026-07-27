# Walkthrough: one real bout, end to end

**Audience: everyone.** This is the fastest way to see whether the design is right. If
something here looks wrong to you, it probably is — say so.

Nothing exposes a modelling error faster than tracing one real record all the way
through. This traces an actual OrcaSound bout, chosen because it is hard.

## The bout

```
name:       SRKW signals at PT (J+K +L? pods)
id:         bout_031YvAeJ4O13YgkbQlc8yJ
category:   biophony
```

A real bout from the OrcaSound API. It was chosen because the moderator packed four
different kinds of claim into one string:

1. **An ecotype**, confidently: Southern Residents.
2. **Two pods**, confidently: J and K.
3. **A third pod, hedged**: `+L?`.
4. **A location shorthand**: `PT` (Port Townsend) — which is *not* animal identity and
   does not belong in this register at all.

Point 4 matters as much as the others. A shared vocabulary is as much about what it
refuses to absorb as what it holds.

## Step 1 — What the moderator does

The moderator types as they do now. Autocomplete matches against `names.tsv`, including
`hidden` names, so typing `SRKW` finds the Southern Resident ecotype even though `SRKW`
is never displayed as a label.

For the hedge, they pick `L pod` and set certainty to `possible`. They do **not** pick a
different term. There is no `L?` entity and there never will be — see
[ADR-0009](../decisions/0009-uncertainty-on-the-annotation.md).

## Step 2 — What OrcaSound stores

The original name is kept, verbatim, forever. Nothing below replaces it.

```
bout.name = "SRKW signals at PT (J+K +L? pods)"
```

Alongside it, four annotation rows:

| entity_id | certainty | evidence | asserted_by | asserted_at | register_edition |
|---|---|---|---|---|---|
| SSA:0000001 (Southern Resident) | certain | moderator-acoustic | sveirs | 2025-10-14T21:03Z | 2026.07.1 |
| SSA:0000020 (J pod) | certain | moderator-acoustic | sveirs | 2025-10-14T21:03Z | 2026.07.1 |
| SSA:0000021 (K pod) | certain | moderator-acoustic | sveirs | 2025-10-14T21:03Z | 2026.07.1 |
| SSA:0000022 (L pod) | **possible** | moderator-acoustic | sveirs | 2025-10-14T21:03Z | 2026.07.1 |

`PT` is discarded here because the bout already has a `feed_id`, which is where location
lives.

Note what each column buys:

- `certainty` is the `+L?`. Without it the moderator either drops the hedge or invents a
  term, and both corrupt the record.
- `evidence` is *how we know* — heard it, or confirmed against a photo-ID sighting, or a
  detector said so. Borrowed from the Gene Ontology's evidence codes; see
  [background.md](background.md).
- `register_edition` is what makes this row re-interpretable in 2030.

## Step 3 — What SalishSea.io ingests

It reads the four identifiers and does no string parsing.

To place this on a map as an occurrence it needs to roll `SSA:0000020` up to something
displayable. Walking `membership.tsv`:

```
SSA:0000020  J pod
  └─ SSA:0000011  J clan
       └─ SSA:0000010  Southern Resident community
```

and separately, via `mappings.tsv`, `SSA:0000001` → `NCBITaxon:9733` (*Orcinus orca*)
for anything that needs a species.

The `possible` L pod row is ingested but rendered differently — or dropped, at the
consumer's discretion. **That choice is the consumer's, and it is only available because
the certainty was preserved rather than flattened.**

## Step 4 — What happens in 2029 when something changes

Suppose L pod is reorganised, and `SSA:0000022` is deprecated in favour of two new
identifiers.

```
entity_id     reason  replaced_by  consider                    date
SSA:0000022   split                SSA:0000090 SSA:0000091     2029-03-14
```

Because the reason is `split` and not a clean rename, there is no `replaced_by` — so
OrcaSound does **not** silently rewrite the historical annotation. It surfaces the bout
for a human to re-decide, and until then the 2025 row still reads `SSA:0000022`, still
resolves to a label, and is still honest about what the moderator actually asserted.

Had this been a simple rename, `replaced_by` would have been populated and the migration
would have been mechanical.

## What this walkthrough exposed

Things that only became visible by tracing a real record:

- **The register needs no location concept at all.** Both consuming systems already have
  one. Confirms a scope boundary that was otherwise theoretical.
- **`certainty` and `evidence` are annotation columns, not register columns.** They
  describe an *act of identification*, not an animal. They belong in OrcaSound's schema
  and are documented here only so both consumers implement them the same way.
- **Ecotype and pod were both asserted on one bout**, redundantly — J pod implies
  Southern Resident. Should consumers store the redundant parent, or derive it? Open
  question [Q5](open-questions.md).

## A second, harder bout

```
name: Humpback mimics Bigg's?
id:   bout_030hfXTlTutthslHi3KfNs
```

The claim is: *a humpback produced a sound characteristic of a different species*. The
animal is a humpback; the sound belongs to Bigg's. Any model that assumes "the tag on
the bout identifies the animal that made the sound" gets this wrong.

This bout is not yet modellable and is listed as open question
[Q7](open-questions.md). It is here because it is the clearest evidence that the animal
register and the sound vocabulary have to be independently applicable to the same bout —
which is an argument for keeping them in separate repositories.
