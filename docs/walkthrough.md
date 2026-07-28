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

The moderator types as they do now. Autocomplete matches against preferred names in
`entities.tsv` and every alternate in `names.tsv`, including `hidden` ones — so typing
`SRKW` finds the Southern Resident ecotype even though `SRKW` is not offered as its name.

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
  Southern Resident. What a consumer stores is its own annotation design's business, not
  the register's; the register's part is to publish the closure so that deriving a parent
  is cheap (`dist/ancestor.tsv`). See [Q5](open-questions.md), resolved by declining it.

## A second, harder bout

```
name: Humpback mimics Bigg's?
id:   bout_030hfXTlTutthslHi3KfNs
```

The title is a hypothesis, question mark and all: someone heard a signal characteristic of
Bigg's and suspects a humpback produced it.

This looked at first like a modelling crisis — two species on one bout — and it was
written up here as one. It is not, and the mistake is worth keeping visible because it is
easy to make. **A call type being characteristic of Bigg's is a regularity about who
usually produces it, not a property of the sound.** Sounds do not have a species. Promote
"characteristic of" to "belongs to" and you appear to have two species attached to one
bout; undo the promotion and you have what was actually recorded: one animal, identified
with low confidence, plus a call type. The register's job on this bout is the same as on
any other, and [ADR-0009](../decisions/0009-uncertainty-on-the-annotation.md) already
covers the uncertainty.

What the bout does teach is a requirement on the annotation schema rather than on the
register: a moderator here may know the call type and genuinely not know the animal, so a
signal must be taggable with **no** animal tag. Without that, the honest answer is
unavailable and the nearest one is wrong — tagging `Bigg's` for a sound suspected to come
from a humpback asserts a species nobody meant to assert. See
[Q18](open-questions.md).

The animal register and the sound vocabulary do have to be independently applicable to
one bout. That is true because they describe different kinds of thing, though — not
because of this recording.
