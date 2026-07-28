#!/usr/bin/env python3
"""Validate the register, and build its distributable artefacts.

The constraints live in `schema.sql`, not here. This script loads `data/*.tsv` into a
SQLite database built from that schema — so **the build is the validation**: a row that
violates a foreign key, a CHECK, or a uniqueness rule is rejected by the database.

What remains here is the part SQL cannot state declaratively (graph reachability, cycles)
and the part a curator needs that a constraint engine does not give: which file, which
line, and what to do about it. See ADR-0013.

Usage:
    python3 bin/validate.py [--strict] [--write-dist]

    --strict      treat warnings as errors (release tags, not pull requests)
    --write-dist  regenerate dist/ — the derived views, as TSV
"""

import csv
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DIST = ROOT / "dist"

# (table, tsv stem, renames) — `start`/`end` are SQL keywords, so the columns are renamed
# on the way in rather than the data being made awkward to read.
TABLES = [
    ("source", "sources", {}),
    ("rank", "ranks", {}),
    ("entity", "entities", {}),
    ("name", "names", {}),
    ("membership", "membership", {"start": "starts", "end": "ends"}),
    ("status", "status", {}),
    ("mapping", "mappings", {}),
    ("deprecation", "deprecations", {}),
]

# Views exported to dist/ so no consumer reimplements them. Each answers a competency
# question; see docs/competency-questions.md.
DIST_VIEWS = ["ancestor", "current_status", "searchable_name", "retired"]

# GitHub renders Mermaid in Markdown; it does not render Graphviz.
MERMAID_ID = str.maketrans({":": "_", "-": "_", " ": "_", "'": ""})

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def read_tsv(stem: str) -> list[dict]:
    """Read a TSV, rejecting ragged rows in both directions.

    A short row is an error, not something to pad: a row with an embedded tab AND an
    omitted trailing column would otherwise parse cleanly with every field shifted.
    """
    path = DATA / f"{stem}.tsv"
    if not path.exists():
        err(f"{stem}.tsv:0: file is missing")
        return []
    raw = path.read_text(encoding="utf-8")
    if not raw.endswith("\n"):
        err(f"{stem}.tsv:0: file does not end with a newline")
    lines = raw.splitlines()
    header = lines[0].split("\t")
    width = len(header)
    rows = []
    for i, line in enumerate(lines[1:], start=2):
        if not line.strip():
            err(f"{stem}.tsv:{i}: blank line")
            continue
        cells = line.split("\t")
        if len(cells) != width:
            hint = "embedded tab?" if len(cells) > width else "pad the row with tabs"
            err(f"{stem}.tsv:{i}: {len(cells)} fields, header has {width}; {hint}")
            continue
        row = {k: (v if v != "" else None) for k, v in zip(header, cells)}
        row["__line"] = i
        rows.append(row)
    return rows


def build(db: sqlite3.Connection) -> None:
    """Load every TSV. The schema rejects what is malformed; we report where."""
    db.executescript((ROOT / "schema.sql").read_text())

    # `membership.group_kind` is denormalised so a composite foreign key can constrain
    # what sort of thing a container may be. Curators never maintain it; the build does.
    kinds: dict = {}

    for table, stem, rename in TABLES:
        cols = [r[1] for r in db.execute(f"PRAGMA table_info({table})")]
        for row in read_tsv(stem):
            line = row.pop("__line")
            for src, dst in rename.items():
                row[dst] = row.pop(src, None)
            if table == "entity":
                kinds[row.get("entity_id")] = row.get("kind")
            elif table == "membership":
                row["group_kind"] = kinds.get(row.get("group_id"))
            elif table == "source" and not row.get("license_status"):
                row["license_status"] = "n/a"

            unknown = set(row) - set(cols)
            if unknown:
                err(f"{stem}.tsv:{line}: column(s) {sorted(unknown)} are not in schema.sql")
                continue
            try:
                db.execute(
                    f"INSERT INTO {table} ({','.join(cols)}) "
                    f"VALUES ({','.join('?' * len(cols))})",
                    [row.get(c) for c in cols],
                )
            except sqlite3.IntegrityError as e:
                err(f"{stem}.tsv:{line}: {row.get(cols[0]) or '?'}: {e}")
            if row.get("source_id") == "SEED":
                warn(f"{stem}.tsv:{line}: unverified SEED row")
    db.commit()


def graph_checks(db: sqlite3.Connection) -> None:
    """The checks a constraint engine cannot state. Queries, not nested loops."""
    for member, _ in db.execute(
        """WITH RECURSIVE walk(a, b) AS (
             SELECT member_id, group_id FROM membership
             UNION SELECT w.a, m.group_id FROM walk w
                   JOIN membership m ON m.member_id = w.b)
           SELECT a, b FROM walk WHERE a = b"""
    ):
        err(f"membership.tsv: {member} is transitively a member of itself")

    # Reachability, not just orphanhood. Foreign keys guarantee an edge points at
    # something real; they say nothing about whether the graph has a root. A single
    # missing edge disconnects everything beneath it, so report the consequence — the
    # entities that fall out of every rollup — not only the node where the break is.
    unreachable = db.execute(
        """WITH RECURSIVE reach(id) AS (
             SELECT entity_id FROM entity WHERE kind = 'taxon'
             UNION SELECT m.member_id FROM membership m JOIN reach r
                   ON m.group_id = r.id)
           SELECT entity_id, label, kind, coalesce(rank, '') FROM entity
           WHERE entity_id NOT IN (SELECT id FROM reach)
           ORDER BY kind, rank, label"""
    ).fetchall()
    if unreachable:
        roots = [u for u in unreachable
                 if not db.execute("SELECT 1 FROM membership WHERE member_id = ?",
                                   (u[0],)).fetchone()]
        warn(f"membership.tsv: {len(unreachable)} entities are unreachable from any "
             f"taxon, so nothing rolls them up to a species. "
             f"Break{'s' if len(roots) != 1 else ''} at: "
             + ", ".join(f"{r[1]} ({r[3] or r[2]})" for r in roots))
        for eid, label, kind, rank in unreachable:
            warn(f"entities.tsv: {eid} ({label}, {rank or kind}) is unreachable")

    for eid, name in db.execute(
        """SELECT n.entity_id, n.name FROM name n
           JOIN entity e ON e.entity_id = n.entity_id AND e.label = n.name"""
    ):
        err(f"names.tsv: {eid}: {name!r} duplicates the preferred label; names.tsv "
            "holds alternates only (ADR-0011)")

    for (eid,) in db.execute(
        """SELECT entity_id FROM deprecation
           WHERE replaced_by IN (SELECT entity_id FROM deprecation)"""
    ):
        err(f"deprecations.tsv: {eid}: replaced_by points at a deprecated entity, so a "
            "consumer would have to chase a chain (ADR-0010)")

    for (f,) in db.execute("SELECT definition_file FROM rank"):
        if not (ROOT / f).exists():
            err(f"ranks.tsv: definition_file {f} does not exist")


def write_dist(db: sqlite3.Connection) -> None:
    """Export the views as TSV, deterministically.

    Rows are sorted here rather than with ORDER BY because these files are committed and
    CI compares them against a fresh build: SQLite versions may order an unordered
    recursive CTE differently, which would make the artefact spuriously dirty on some
    machines. Sorting in Python is engine-independent.
    """
    DIST.mkdir(exist_ok=True)
    for view in DIST_VIEWS:
        cur = db.execute(f"SELECT * FROM {view}")
        cols = [d[0] for d in cur.description]
        rows = sorted(cur, key=lambda r: tuple("" if v is None else str(v) for v in r))
        with open(DIST / f"{view}.tsv", "w", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(cols)
            w.writerows(rows)


def write_structure(db: sqlite3.Connection) -> None:
    """A renderable picture of the register's shape.

    661 entities will not render as one graph, so this draws the *rank-level* structure:
    which kinds of thing contain which, with counts. That collapses the whole register to
    a handful of nodes, and it makes structural differences between branches obvious —
    including any place the graph is broken.
    """
    level = "coalesce(rank, kind)"
    edges = db.execute(
        f"""SELECT {level.replace('rank', 'c.rank').replace('kind', 'c.kind')},
                   {level.replace('rank', 'p.rank').replace('kind', 'p.kind')},
                   count(*)
            FROM membership m
            JOIN entity c ON c.entity_id = m.member_id
            JOIN entity p ON p.entity_id = m.group_id
            GROUP BY 1, 2 ORDER BY 3 DESC"""
    ).fetchall()
    counts = dict(db.execute(f"SELECT {level}, count(*) FROM entity GROUP BY 1"))

    out = ["# The shape of the register",
           "",
           "Generated by `bin/validate.py --write-dist`. Not hand-edited.",
           "",
           "## Rank structure",
           "",
           "Every membership edge, collapsed to the level of the things it connects.",
           "Edge labels are edge counts; node labels are how many entities exist at that",
           "level. A level with no path upward is a break in the graph.",
           "", "```mermaid", "graph BT"]
    for lvl, n in sorted(counts.items()):
        out.append(f'  {lvl.translate(MERMAID_ID)}["{lvl}<br/>{n}"]')
    for child, parent, n in edges:
        out.append(f"  {child.translate(MERMAID_ID)} -->|{n}| "
                   f"{parent.translate(MERMAID_ID)}")
    out += ["```", ""]

    unreachable = db.execute(
        """WITH RECURSIVE reach(id) AS (
             SELECT entity_id FROM entity WHERE kind = 'taxon'
             UNION SELECT m.member_id FROM membership m JOIN reach r ON m.group_id = r.id)
           SELECT count(*) FROM entity WHERE entity_id NOT IN (SELECT id FROM reach)"""
    ).fetchone()[0]
    if unreachable:
        out += [f"> **{unreachable} entities are unreachable from any species.** Follow the",
                "> arrows up: a level with no outgoing edge is where the graph breaks, and",
                "> everything below it falls out of every rollup.", ""]

    # One real subtree, small enough to read.
    out += ["## Southern Residents", "",
            "The seeded branch in full — small enough to render whole.", "",
            "```mermaid", "graph BT"]
    rows = db.execute(
        """WITH RECURSIVE sub(id) AS (
             SELECT entity_id FROM entity WHERE label = 'Southern Resident community'
             UNION SELECT m.member_id FROM membership m JOIN sub s ON m.group_id = s.id)
           SELECT e.entity_id, e.label, coalesce(e.rank, e.kind) FROM entity e
           JOIN sub ON sub.id = e.entity_id ORDER BY e.entity_id"""
    ).fetchall()
    ids = {r[0] for r in rows}
    for eid, label, lvl in rows:
        out.append(f'  {eid.translate(MERMAID_ID)}["{label}<br/>({lvl})"]')
    for a, b in db.execute("SELECT member_id, group_id FROM membership"):
        if a in ids and b in ids:
            out.append(f"  {a.translate(MERMAID_ID)} --> {b.translate(MERMAID_ID)}")
    out += ["```", ""]
    (DIST / "structure.md").write_text("\n".join(out))


def main() -> int:
    strict = "--strict" in sys.argv
    db = sqlite3.connect(sys.argv[sys.argv.index("--db") + 1]
                         if "--db" in sys.argv else ":memory:")
    db.execute("PRAGMA foreign_keys = ON")
    build(db)
    if not errors:
        graph_checks(db)
        if "--write-dist" in sys.argv:
            write_dist(db)
            write_structure(db)
            print(f"wrote {len(DIST_VIEWS)} views and structure.md to dist/",
                  file=sys.stderr)

    for line in warnings:
        print(f"warning: {line}", file=sys.stderr)
    for line in errors:
        print(f"error: {line}", file=sys.stderr)

    counts = ", ".join(
        f"{db.execute(f'SELECT count(*) FROM {t}').fetchone()[0]} {t}"
        for t, _, _ in TABLES
    )
    seed = sum(1 for w in warnings if "SEED" in w)
    print(f"\n{counts}", file=sys.stderr)
    print(f"{len(errors)} errors, {len(warnings)} warnings ({seed} unverified)",
          file=sys.stderr)
    return 1 if errors or (strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
