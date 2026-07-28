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

    for eid, label, rank in db.execute(
        """SELECT entity_id, label, rank FROM entity e
           WHERE kind = 'group'
             AND NOT EXISTS (SELECT 1 FROM membership m
                             WHERE m.member_id = e.entity_id)"""
    ):
        warn(f"entities.tsv: {eid} ({label}, {rank}) has no parent — nothing rolls up "
             "from it, so ancestor queries will stop short")

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
    DIST.mkdir(exist_ok=True)
    for view in DIST_VIEWS:
        cur = db.execute(f"SELECT * FROM {view}")
        with open(DIST / f"{view}.tsv", "w", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow([d[0] for d in cur.description])
            w.writerows(cur)


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
            print(f"wrote {len(DIST_VIEWS)} views to dist/", file=sys.stderr)

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
