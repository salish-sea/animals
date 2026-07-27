#!/usr/bin/env python3
"""Validate the register.

The executable form of the schema. Every check here corresponds to a rule stated in
decisions/ — the ADR is the reasoning, this is the enforcement.

Exit 1 on any error. Warnings do not fail the build: an unverified row is a normal
intermediate state (ADR-0001, "provisional entries"), not a defect.

Usage:  python3 bin/validate.py [--strict]
        --strict  treat warnings as errors (used for release tags, not for PRs)
"""

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

ID_RE = re.compile(r"^SSA:\d{7}$")
CURIE_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.]*:[A-Za-z0-9_.\-]+$")
# EDTF subset we accept: 1998 | 1998? | 1998-09 | 1998-09-13 | 1995/1998
EDTF_RE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?\??$|^\d{4}/\d{4}$")
HEDGE_RE = re.compile(r"\?\s*$|^(unconfirmed|unknown|false[- ]positive|maybe)$", re.I)

errors: list[str] = []
warnings: list[str] = []


def err(f: str, line: int, msg: str) -> None:
    errors.append(f"{f}:{line}: {msg}")


def warn(f: str, line: int, msg: str) -> None:
    warnings.append(f"{f}:{line}: {msg}")


def read(name: str) -> list[dict]:
    """Read a TSV. Rejects embedded tabs and ragged rows before parsing (ADR-0001)."""
    path = DATA / name
    if not path.exists():
        err(name, 0, "file is missing")
        return []
    raw = path.read_text(encoding="utf-8")
    if not raw.endswith("\n"):
        err(name, 0, "file does not end with a newline")
    lines = raw.splitlines()
    header = lines[0].split("\t")
    width = len(header)
    rows = []
    for i, line in enumerate(lines[1:], start=2):
        if not line.strip():
            err(name, i, "blank line")
            continue
        cells = line.split("\t")
        if len(cells) > width:
            err(name, i, f"{len(cells)} fields, header has {width}; embedded tab?")
            continue
        cells += [""] * (width - len(cells))
        row = dict(zip(header, cells))
        row["__line"] = i
        row["__file"] = name
        rows.append(row)
    return rows


def check_id(row: dict, field: str, known: set, required: bool = True) -> None:
    val = row.get(field, "").strip()
    if not val:
        if required:
            err(row["__file"], row["__line"], f"{field} is empty")
        return
    if not ID_RE.match(val):
        err(row["__file"], row["__line"], f"{field}={val!r} is not a well-formed SSA id")
    elif val not in known:
        err(row["__file"], row["__line"], f"{field}={val} does not exist in entities.tsv")


def check_source(row: dict, sources: set) -> None:
    val = row.get("source_id", "").strip()
    if not val:
        err(row["__file"], row["__line"], "source_id is empty — every claim needs a source")
    elif val not in sources:
        err(row["__file"], row["__line"], f"source_id={val} is not in sources.tsv")
    elif val == "SEED":
        warn(row["__file"], row["__line"], "unverified SEED row")


def check_edtf(row: dict, field: str) -> None:
    val = row.get(field, "").strip()
    if val and not EDTF_RE.match(val):
        err(row["__file"], row["__line"], f"{field}={val!r} is not an accepted EDTF form")


def main() -> int:
    strict = "--strict" in sys.argv

    sources = read("sources.tsv")
    ranks = read("ranks.tsv")
    entities = read("entities.tsv")
    names = read("names.tsv")
    membership = read("membership.tsv")
    status = read("status.tsv")
    mappings = read("mappings.tsv")
    deprecations = read("deprecations.tsv")

    source_ids = {r["source_id"] for r in sources}
    rank_ids = {r["rank"] for r in ranks}

    # --- ranks: every rank has a definition file that exists (ADR-0004) ---
    for r in ranks:
        f = r.get("definition_file", "").strip()
        if not f:
            err(r["__file"], r["__line"], "rank has no definition_file")
        elif not (ROOT / f).exists():
            err(r["__file"], r["__line"], f"definition_file {f} does not exist")

    # --- entities: identity, uniqueness, well-formedness (ADR-0002, 0003) ---
    entity_ids: set = set()
    groups: set = set()
    labels: dict = {}
    for e in entities:
        eid = e["entity_id"].strip()
        if not ID_RE.match(eid):
            err(e["__file"], e["__line"], f"entity_id {eid!r} is malformed")
            continue
        if eid in entity_ids:
            err(e["__file"], e["__line"], f"duplicate entity_id {eid}")
        entity_ids.add(eid)

        kind = e["kind"].strip()
        if kind not in ("individual", "group"):
            err(e["__file"], e["__line"], f"kind={kind!r} must be individual or group")
        if kind == "group":
            groups.add(eid)
            if not e["rank"].strip():
                err(e["__file"], e["__line"], "group has no rank")
            elif e["rank"].strip() not in rank_ids:
                err(e["__file"], e["__line"], f"rank={e['rank']!r} is not in ranks.tsv")
        elif e["rank"].strip():
            err(e["__file"], e["__line"], "individual must not have a rank")

        label = e["label"].strip()
        if not label:
            err(e["__file"], e["__line"], "label is empty — opaque ids need a readable neighbour")
        if HEDGE_RE.search(label):
            err(e["__file"], e["__line"],
                f"label {label!r} looks like a hedge; uncertainty belongs on the annotation (ADR-0009)")
        # Duplicate labels are legitimate across kinds (matriline vs matriarch, ADR-0003)
        key = (label, kind, e["rank"].strip())
        if key in labels:
            warn(e["__file"], e["__line"], f"label {label!r} duplicates line {labels[key]} at the same kind/rank")
        labels[key] = e["__line"]

        tid = e.get("taxon_id", "").strip()
        if tid and not CURIE_RE.match(tid):
            err(e["__file"], e["__line"], f"taxon_id={tid!r} is not a CURIE")
        check_edtf(e, "born")
        if e.get("sex", "").strip() not in ("", "F", "M", "U"):
            err(e["__file"], e["__line"], f"sex={e['sex']!r} must be F, M, U or empty")
        check_source(e, source_ids)

    # --- names: no duplication of the primary label (ADR-0002) ---
    primary = {(e["entity_id"].strip(), e["label"].strip()) for e in entities}
    for n in names:
        check_id(n, "entity_id", entity_ids)
        if n.get("type", "").strip() not in ("common", "historical", "hidden"):
            err(n["__file"], n["__line"],
                f"type={n.get('type')!r} must be common, historical or hidden")
        if (n["entity_id"].strip(), n.get("name", "").strip()) in primary:
            err(n["__file"], n["__line"],
                "duplicates the primary label from entities.tsv; names.tsv holds alternates only")
        check_source(n, source_ids)

    # --- membership: shape, direction, and the death/end rule (ADR-0005) ---
    for m in membership:
        check_id(m, "member_id", entity_ids)
        check_id(m, "group_id", entity_ids)
        gid = m["group_id"].strip()
        if gid in entity_ids and gid not in groups:
            err(m["__file"], m["__line"], f"group_id={gid} is not kind=group")
        if m["member_id"].strip() == gid:
            err(m["__file"], m["__line"], "entity cannot be a member of itself")
        check_edtf(m, "start")
        check_edtf(m, "end")
        end = m.get("end", "").strip()
        if end and re.search(r"\b(died|death|deceased|dead)\b", m.get("note", ""), re.I):
            err(m["__file"], m["__line"],
                "end must not record a death — that is status.tsv's job (ADR-0005)")
        check_source(m, source_ids)

    # --- membership graph: no cycles ---
    parents: dict = {}
    for m in membership:
        parents.setdefault(m["member_id"].strip(), []).append(m["group_id"].strip())

    def walk(node: str, seen: tuple) -> None:
        if node in seen:
            err("membership.tsv", 0, f"cycle: {' -> '.join(seen + (node,))}")
            return
        for p in parents.get(node, []):
            walk(p, seen + (node,))

    for node in list(parents):
        walk(node, ())

    # --- status: append-only enum with two clocks (ADR-0006) ---
    STATUSES = ("alive", "presumed_dead", "dead", "unknown")
    for s in status:
        check_id(s, "entity_id", entity_ids)
        eid = s["entity_id"].strip()
        if eid in groups:
            err(s["__file"], s["__line"], "status applies to individuals, not groups")
        if s.get("status", "").strip() not in STATUSES:
            err(s["__file"], s["__line"], f"status must be one of {STATUSES}")
        check_edtf(s, "effective")
        check_edtf(s, "asserted_on")
        if not s.get("effective", "").strip():
            err(s["__file"], s["__line"], "effective is required — when did this become true?")
        check_source(s, source_ids)

    # --- mappings: SSSOM-shaped crosswalks (ADR-0008) ---
    PREDICATES = ("skos:exactMatch", "skos:closeMatch", "skos:broadMatch", "skos:narrowMatch")
    for m in mappings:
        check_id(m, "subject_id", entity_ids)
        if m.get("predicate_id", "").strip() not in PREDICATES:
            err(m["__file"], m["__line"], f"predicate_id must be one of {PREDICATES}")
        obj = m.get("object_id", "").strip()
        if not CURIE_RE.match(obj):
            err(m["__file"], m["__line"], f"object_id={obj!r} is not a CURIE")
        conf = m.get("confidence", "").strip()
        if conf:
            try:
                if not 0.0 <= float(conf) <= 1.0:
                    raise ValueError
            except ValueError:
                err(m["__file"], m["__line"], f"confidence={conf!r} must be between 0 and 1")
        check_source(m, source_ids)

    # --- deprecations: exactly one pointer, no dead ends (ADR-0010) ---
    deprecated = {d["entity_id"].strip() for d in deprecations}
    for d in deprecations:
        check_id(d, "entity_id", entity_ids)
        rb = d.get("replaced_by", "").strip()
        cons = d.get("consider", "").strip().split()
        if bool(rb) == bool(cons):
            err(d["__file"], d["__line"],
                "exactly one of replaced_by / consider must be populated (ADR-0010)")
        if d.get("reason", "").strip() not in ("merged", "split", "erroneous", "renamed"):
            err(d["__file"], d["__line"], "reason must be merged, split, erroneous or renamed")
        for target in ([rb] if rb else []) + cons:
            if target not in entity_ids:
                err(d["__file"], d["__line"], f"target {target} does not exist")
            elif target in deprecated:
                err(d["__file"], d["__line"],
                    f"replaced_by/consider target {target} is itself deprecated")
        check_source(d, source_ids)

    for line in warnings:
        print(f"warning: {line}", file=sys.stderr)
    for line in errors:
        print(f"error: {line}", file=sys.stderr)

    n_seed = sum(1 for w in warnings if "SEED" in w)
    print(
        f"\n{len(entities)} entities, {len(membership)} membership edges, "
        f"{len(status)} status rows, {len(names)} alternate names, "
        f"{len(deprecations)} deprecations",
        file=sys.stderr,
    )
    print(f"{len(errors)} errors, {len(warnings)} warnings ({n_seed} unverified rows)",
          file=sys.stderr)

    if errors or (strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
