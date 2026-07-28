-- Salish Sea animals register — schema.
--
-- This file is the normative statement of the register's constraints. SQLite stores it
-- verbatim (comments included) in sqlite_master, so the shipped file explains itself:
--   SELECT sql FROM sqlite_master;
--
-- Every constraint below corresponds to a decision record. The ADR is the reasoning;
-- this is the enforcement.

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------------
-- Provenance
-- ---------------------------------------------------------------------------

CREATE TABLE source (
  source_id      TEXT PRIMARY KEY,
  name           TEXT NOT NULL,
  url            TEXT,
  scope          TEXT,
  license        TEXT,
  -- Redistribution permission. Data under `not-yet-requested` must not be republished.
  license_status TEXT NOT NULL CHECK (license_status IN
                   ('cleared','requested','not-yet-requested','denied','n/a')),
  retrieved_on   TEXT,
  note           TEXT
);

-- Social levels. NOT taxonomic ranks — an ecotype is not a formal taxon (ADR-0008).
-- The list is open and no ordering is implied: Bigg's have no pods (ADR-0004).
CREATE TABLE rank (
  rank            TEXT PRIMARY KEY,
  label           TEXT NOT NULL,
  applies_to      TEXT,
  definition_file TEXT NOT NULL,
  status          TEXT NOT NULL CHECK (status IN ('proposed','working','agreed')),
  note            TEXT
);

-- ---------------------------------------------------------------------------
-- Entities
-- ---------------------------------------------------------------------------

CREATE TABLE entity (
  -- Opaque and permanent. Never deleted, never reused, never reassigned (ADR-0010).
  entity_id TEXT PRIMARY KEY
            CHECK (entity_id GLOB 'SSA:[0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),

  -- individual: one animal. group: a social grouping. taxon: a taggable stand-in for
  -- "an animal of this species, not resolved further" (ADR-0003, ADR-0008).
  kind      TEXT NOT NULL CHECK (kind IN ('individual','group','taxon')),

  -- Ranks are social levels, so only groups have one (ADR-0004).
  rank      TEXT REFERENCES rank(rank),

  -- The preferred name: what the entity is canonically called. NOT a display string and
  -- NOT an integration key — it is mutable by design (ADR-0011).
  label     TEXT NOT NULL CHECK (length(trim(label)) > 0),

  -- References an external species identifier; mints none (ADR-0008).
  taxon_id  TEXT,

  -- EDTF. Qualifiers: ? uncertain, ~ approximate. Open ranges for animals first seen
  -- as adults: '../1966' means "no later than 1966".
  born      TEXT,
  sex       TEXT CHECK (sex IS NULL OR sex IN ('F','M','U')),
  source_id TEXT NOT NULL REFERENCES source(source_id),
  note      TEXT,

  CHECK (kind <> 'group'  OR rank IS NOT NULL),
  CHECK (kind =  'group'  OR rank IS NULL),
  CHECK (kind <> 'taxon'  OR taxon_id IS NOT NULL),
  -- Only animals are born or sexed.
  CHECK (kind =  'individual' OR (born IS NULL AND sex IS NULL)),
  -- Uncertainty belongs on the annotation, never in a name (ADR-0009).
  CHECK (label NOT LIKE '%?')
);

-- Lets membership constrain what kind of thing a container may be. Without this,
-- "group_id must be a group or a taxon" needs a trigger.
CREATE UNIQUE INDEX entity_id_kind ON entity (entity_id, kind);

-- Alternates only. The preferred name lives on entity.label (ADR-0011).
--   common     — a real name people use
--   historical — superseded, kept so old text still resolves ("Transient")
--   hidden     — matches in search, never offered as a name ("SRKW", "harbor seal")
CREATE TABLE name (
  entity_id TEXT NOT NULL REFERENCES entity(entity_id),
  name      TEXT NOT NULL,
  type      TEXT NOT NULL CHECK (type IN ('common','historical','hidden')),
  language  TEXT NOT NULL DEFAULT 'en',
  source_id TEXT NOT NULL REFERENCES source(source_id),
  note      TEXT,
  PRIMARY KEY (entity_id, name, language)
);

-- ---------------------------------------------------------------------------
-- Membership — genealogical only. Association is occurrence data (ADR-0005).
-- ---------------------------------------------------------------------------

CREATE TABLE membership (
  member_id  TEXT NOT NULL REFERENCES entity(entity_id),
  group_id   TEXT NOT NULL,
  -- Denormalised so the composite foreign key below can constrain it. Populated by the
  -- build, not by curators.
  group_kind TEXT NOT NULL CHECK (group_kind IN ('group','taxon')),

  -- Empty on natal edges, meaning "bounded by the individual's lifespan". A non-empty
  -- `ends` on an individual means dispersal — never death, which is status's job.
  starts     TEXT,
  ends       TEXT,
  source_id  TEXT NOT NULL REFERENCES source(source_id),
  note       TEXT,

  PRIMARY KEY (member_id, group_id),
  CHECK (member_id <> group_id),
  FOREIGN KEY (group_id, group_kind) REFERENCES entity(entity_id, kind)
);

-- ---------------------------------------------------------------------------
-- Life status — append-only, three clocks (ADR-0006)
-- ---------------------------------------------------------------------------

CREATE TABLE status (
  entity_id   TEXT NOT NULL REFERENCES entity(entity_id),
  status      TEXT NOT NULL CHECK (status IN ('alive','presumed_dead','dead','unknown')),

  effective   TEXT NOT NULL,              -- when it became true in the world
  asserted_on TEXT,                       -- when the upstream source said so
  -- When we wrote it down. The precedence key, so it must be exact: a bare year cannot
  -- order two competing claims, which is this column's only job.
  recorded    TEXT NOT NULL
              CHECK (recorded GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'),

  source_id   TEXT NOT NULL REFERENCES source(source_id),
  note        TEXT,

  -- Ties would make current status ambiguous.
  PRIMARY KEY (entity_id, recorded, effective)
);

-- ---------------------------------------------------------------------------
-- Crosswalks and deprecation
-- ---------------------------------------------------------------------------

CREATE TABLE mapping (
  subject_id            TEXT NOT NULL REFERENCES entity(entity_id),
  predicate_id          TEXT NOT NULL CHECK (predicate_id IN
                          ('skos:exactMatch','skos:closeMatch',
                           'skos:broadMatch','skos:narrowMatch')),
  object_id             TEXT NOT NULL,
  object_label          TEXT,
  mapping_justification TEXT,
  confidence            REAL CHECK (confidence IS NULL OR confidence BETWEEN 0 AND 1),
  source_id             TEXT NOT NULL REFERENCES source(source_id),
  note                  TEXT,
  PRIMARY KEY (subject_id, predicate_id, object_id)
);

CREATE TABLE deprecation (
  entity_id   TEXT PRIMARY KEY REFERENCES entity(entity_id),
  reason      TEXT NOT NULL CHECK (reason IN ('merged','split','erroneous','renamed')),
  -- replaced_by: unambiguous, a consumer MAY substitute automatically.
  -- consider:    needs human judgement, a consumer MUST NOT substitute.
  replaced_by TEXT REFERENCES entity(entity_id),
  consider    TEXT,
  date        TEXT,
  source_id   TEXT NOT NULL REFERENCES source(source_id),
  note        TEXT,
  CHECK ((replaced_by IS NULL) <> (consider IS NULL))
);

-- ---------------------------------------------------------------------------
-- Views: the intelligence a consumer would otherwise reimplement, shipped once.
-- ---------------------------------------------------------------------------

-- C4: was this individual alive on a given date?
-- The precedence rule from ADR-0006, so no consumer has to get it right themselves.
CREATE VIEW current_status AS
SELECT entity_id, status, effective, asserted_on, recorded, source_id
FROM (
  SELECT *, ROW_NUMBER() OVER (
             PARTITION BY entity_id ORDER BY recorded DESC, effective DESC) AS rn
  FROM status
)
WHERE rn = 1;

-- C5, C6: the transitive closure. Published as data so every consumer agrees.
CREATE VIEW ancestor AS
WITH RECURSIVE walk(entity_id, ancestor_id, depth) AS (
  SELECT member_id, group_id, 1 FROM membership
  UNION
  SELECT w.entity_id, m.group_id, w.depth + 1
  FROM walk w JOIN membership m ON m.member_id = w.ancestor_id
)
SELECT w.entity_id, w.ancestor_id, w.depth, e.label AS ancestor_label,
       e.kind AS ancestor_kind, e.rank AS ancestor_rank
FROM walk w JOIN entity e ON e.entity_id = w.ancestor_id;

-- C2: everything a moderator might type, in one place. Autocomplete must read the
-- preferred name AND the alternates; searching only `name` misses every label.
CREATE VIEW searchable_name AS
SELECT entity_id, label AS name, 'preferred' AS type, 'en' AS language FROM entity
UNION ALL
SELECT entity_id, name, type, language FROM name;

-- C9: what a consumer should do with an identifier it can no longer offer.
CREATE VIEW retired AS
SELECT d.entity_id, e.label, d.reason, d.replaced_by, d.consider,
       CASE WHEN d.replaced_by IS NOT NULL THEN 'automatic' ELSE 'needs-human' END
         AS migration
FROM deprecation d JOIN entity e ON e.entity_id = d.entity_id;

-- Curation surface: what still has to be verified before release.
CREATE VIEW unverified AS
SELECT 'entity' AS tbl, entity_id AS id FROM entity      WHERE source_id = 'SEED'
UNION ALL SELECT 'name',       entity_id FROM name       WHERE source_id = 'SEED'
UNION ALL SELECT 'membership', member_id FROM membership WHERE source_id = 'SEED'
UNION ALL SELECT 'status',     entity_id FROM status     WHERE source_id = 'SEED'
UNION ALL SELECT 'mapping',    subject_id FROM mapping   WHERE source_id = 'SEED';
