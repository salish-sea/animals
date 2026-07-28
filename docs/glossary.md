# Glossary

Two communities are reviewing this work and each uses jargon the other doesn't. Terms
are marked with who is likely to need them:

- 🐋 **science** — likely unfamiliar to the software reviewers
- 💾 **informatics** — likely unfamiliar to the scientific reviewers
- ⚖️ **both** — used by both, sometimes with *different meanings*, which is the
  dangerous case

Terms with a formal definition in this register link to `definitions/`, which is
normative. This glossary is not — it is here to make the documents readable.

---

### ⚖️ Association
Animals observed travelling together. **Not** the same as membership here, and the
distinction is load-bearing: see [ADR-0005](../decisions/0005-membership-is-genealogical.md).
Association is occurrence data and lives in the consuming systems.

### 💾 ADR (Architecture Decision Record)
A short document recording one decision, why it was made, and what was given up. Kept
even after it's superseded, so future readers can see the reasoning rather than guessing
at it. In `decisions/`.

### 🐋 Bigg's
An ecotype of *Orcinus orca* that preys on marine mammals. Formerly "transient" —
retained as a `historical` name so older text still resolves. Unlike residents,
individuals do disperse from their natal group.

### 🐋 Bout
An OrcaSound concept: a human-curated stretch of hydrophone audio with a start, an end,
and a category (`biophony`, `anthrophony`, `geophony`). The unit this register is
consumed by.

### 💾 Closure (transitive closure)
The full set of ancestors of an entity, precomputed. If J35 is in matriline J17s, in J
pod, in J clan, then J35's closure includes all of them — so a search for "J pod"
finds a bout tagged only with a matriline. Generated into `dist/`, never hand-edited.

### 🐋 Clan
A group of pods sharing part of an acoustic repertoire. See
[definitions/clan.md](../definitions/clan.md).

### 💾 Competency question
A question the register must be able to answer, written down in advance and used to
decide when the model is complete. See [competency-questions.md](competency-questions.md).

### 💾 Deprecation
Marking an identifier as no longer current *without deleting it*. Deleted identifiers
break every record that ever referenced them; deprecated ones stay resolvable and point
at their replacement. See [ADR-0010](../decisions/0010-identifiers-are-never-reused.md).

### 💾 EDTF (Extended Date/Time Format)
A date notation that can express uncertainty and ranges: `1998`, `2020-09`,
`1995/1998` ("sometime between"), `../1966` ("no later than"), `1968/..` ("no earlier
than"). Two distinct qualifiers, easily confused: `1998?` is *uncertain* (we're not sure
it's 1998) and `1979~` is *approximate* (about 1979). Used for `born`, because catalogues
record most birth years as estimates or open-ended bounds for animals first seen as
adults.

### 🐋 Ecotype
A genetically and behaviourally distinct population within a species. Not a formal
taxonomic rank, which is precisely why it needs an identifier here — no external
taxonomy will give us one. See [definitions/ecotype.md](../definitions/ecotype.md).

### ⚖️ Entity
Anything in the register with an identifier: an individual animal *or* a group. Both
share one identifier space — see [ADR-0003](../decisions/0003-one-identifier-space.md).

### 💾 Evidence code
A short controlled value recording *how* a claim was arrived at: heard by a moderator,
confirmed against a photo-ID sighting, inferred from a co-occurring visual report,
produced by an automated detector. Borrowed from the Gene Ontology.

### ⚖️ Label
The register's **preferred name** for an entity — what it is canonically called. It is
input to display, not display itself: a consumer builds its own dropdown entry or map
label from this plus rank and context. Mutable by design, so nothing may key on it. See
[ADR-0011](../decisions/0011-label-is-a-preferred-name.md).

### 🐋 Matriline
A female and her surviving descendants, travelling as a unit. The only rank used by
every ecotype in scope. See [definitions/matriline.md](../definitions/matriline.md).

### ⚖️ Membership
**In this register: genealogical only.** An individual belongs to the matriline they
were born into. This is narrower than the everyday sense — L87 travelling with J pod is
not membership. See [definitions/membership.md](../definitions/membership.md).

### ⚖️ Parentage
Who bore whom, in `parentage.tsv`. **Not the same as membership and not recoverable from
it**: a matriline spans three or four generations, so a membership edge means "descended
from the matriarch", not "child of". Recorded for very few animals so far — absent means
*not recorded*, never *no mother*. See
[ADR-0016](../decisions/0016-parentage.md).

### 💾 Namespace / prefix
The `SSA:` in `SSA:0000101`. Distinguishes our identifiers from `NCBITaxon:9733` or
`finwave:T090` so they can be mixed in one column without collision.

### ⚖️ Occurrence
A record that an animal was at a place at a time. Deliberately **not** in this register.
The word is also a Darwin Core term with a precise meaning, which is roughly ours.

### 💾 Opaque identifier
An identifier that carries no meaning — `SSA:0000020` rather than `pod-j`. Meaningful
identifiers become lies when the thing they describe changes. See
[ADR-0002](../decisions/0002-opaque-permanent-identifiers.md).

### 🐋 Pod
A stable group of related matrilines that travel together, used for resident killer
whales. Bigg's do not use this rank. See [definitions/pod.md](../definitions/pod.md).

### ⚖️ Rank
The level of a group in this register: ecotype, community, clan, pod, matriline. **Not a
taxonomic rank** — an ecotype is explicitly not a formal taxon
([ADR-0008](../decisions/0008-species-identity-is-delegated.md)), and the levels are
social, not Linnaean. The list is open and not every population uses every level; Bigg's
have no pods. See [ADR-0004](../decisions/0004-rank-is-an-open-vocabulary.md).

### ⚖️ Taxon entity
An entity of `kind = taxon`: a taggable stand-in for "an animal of this species, not
resolved further". `Orcinus orca` with no ecotype alongside it *is* "an orca, ecotype
undetermined" — no separate concept needed. It references an external species identifier
rather than minting one, has no rank (ranks are social levels), and has no life status,
because it is a kind rather than an animal. See
[ADR-0008](../decisions/0008-species-identity-is-delegated.md).

### ⚖️ Register
A curated list of individually identified things, each with a permanent identifier.
Distinct from a *taxonomy* (a classification of kinds) and a *vocabulary* (an agreed set
of words). This repository is primarily a register; `definitions/` is the vocabulary
part.

### 🐋 SRKW
Southern Resident killer whale. A `hidden` name in the register — it matches in search
but is never displayed as a label.

### 💾 SKOS (Simple Knowledge Organization System)
A W3C standard for published vocabularies. We use only its label distinctions —
preferred, alternate, hidden — and its match predicates. Not the rest.

### 💾 SSSOM (Simple Standard for Sharing Ontological Mappings)
A TSV format for recording that an identifier in one system means the same as an
identifier in another, including how confident the mapping is and how it was made. Our
`mappings.tsv` follows its column names. Pronounced "sossum".

### 💾 Valid time / assertion time
Two different clocks. *Valid time* is when something was true in the world (an animal
died in September 2018). *Assertion time* is when someone recorded it (declared at the
census, some days later). Conflating them makes it impossible either to ask "who was
alive in 2017" or to reproduce what a page displayed in 2019. Here, valid time is in the
data and assertion time is in git history — see
[ADR-0006](../decisions/0006-valid-time-in-data-assertion-time-in-git.md).
