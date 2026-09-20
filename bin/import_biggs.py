#!/usr/bin/env python3
"""Import Bigg's individuals and matrilines from the community designation sheet.

Bulk import is an exception to ADR-0001's reviewable-diff premise: nobody reads five
hundred rows in a pull request. The exception is that **this script is the reviewable
artefact** — the transformation is what gets scrutinised, and the output is reproducible
from it. See ADR-0015.

Rights (salishsea-io D-21): the factual content — designations, genealogy, birth years,
sex, deceased status, naming authority — is uncopyrightable and used freely. The "Story
Behind the Nickname" column is creative prose and is **never** read by this script. The
sheet's maintainer is credited in sources.tsv.

Idempotent: an identifier already assigned to a designation is reused, so re-running
after the sheet updates only mints identifiers for genuinely new animals.

Usage:  python3 bin/import_biggs.py <path-to-biggs-ids.tsv> [--apply]
"""

import re
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SOURCE = "BIGGS-SHEET"
BIGGS_ECOTYPE = "SSA:0000002"

# Identifier blocks. Purely for legibility when scanning a file; nothing may parse them
# (ADR-0002). Bigg's gets its own range so the seed data stays readable.
MATRILINE_BLOCK = 2000
INDIVIDUAL_BLOCK = 10000

# What the sheet knows about a death is that it had happened by the time we read the
# sheet. EDTF says that exactly, rather than inventing a date.
SNAPSHOT = "2026-07"

DESIGNATION = re.compile(r"^(T\d+)([A-Z]?\d*)*$")
LINEAGE = re.compile(r"^(T\d+)")
# A designation is a T-number followed by alternating letter and number tokens, one per
# generation: T073 > T073A > T073A1. Stripping the last token gives the mother's.
TOKENS = re.compile(r"T\d+|[A-Z]+|\d+")


def enclosing(desig):
    """Every designation `desig` descends from, nearest first: T073A1 -> T073A, T073."""
    tokens = TOKENS.findall(desig)
    return ["".join(tokens[:n]) for n in range(len(tokens) - 1, 0, -1)]


def read_tsv(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    for line in lines[1:]:
        cells = line.split("\t") + [""] * len(header)
        yield dict(zip(header, cells))


def edtf_year(raw):
    """Sheet birth years into EDTF. '≤1966' and '<1969' are the common shapes."""
    v = (raw or "").strip()
    if not v or v.upper() in ("UNK", "?", "N/A"):
        return None
    if m := re.match(r"^[≤<=]+\s*(\d{4})$", v):
        year = int(m.group(1))
        # "<1969" means before 1969; "≤1966" includes it.
        return f"../{year - 1 if v.lstrip()[0] == '<' else year}"
    if m := re.match(r"^(\d{4})\s*$", v):
        return m.group(1)
    if m := re.match(r"^(\d{4})\s*[-/]\s*(\d{4})$", v):
        return f"{m.group(1)}/{m.group(2)}"
    if m := re.match(r"^(\d{4})\s*\?$", v):
        return f"{m.group(1)}?"
    if m := re.search(r"(\d{4})", v):
        return f"{m.group(1)}~"          # anything else with a year: approximate
    return None


def load_existing():
    """Designation -> entity_id, so re-running does not remint."""
    path = DATA / "entities.tsv"
    rows = [l.split("\t") for l in path.read_text().splitlines()]
    hdr = rows[0]
    by_label = {r[hdr.index("label")]: r[hdr.index("entity_id")] for r in rows[1:]}
    used = {int(r[hdr.index("entity_id")].split(":")[1]) for r in rows[1:]}
    return by_label, used, hdr, rows


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    by_label, used, hdr, existing = load_existing()

    individuals = OrderedDict()   # designation -> record
    lineage_names = {}            # lineage -> "Known as ..." label
    current_lineage = None

    for row in read_tsv(src):
        desig = row["Local ID designation (BC and WA)"].strip()
        if not desig:
            continue
        # A row carrying only a name heads a lineage: "Known as the Motley Crew",
        # "The Gretzky's". It applies to the next designation seen.
        if not desig.startswith("T") or not any(c.isdigit() for c in desig[:5]):
            current_lineage = ("PENDING", desig)
            continue

        # A trailing "?" hedges the *designation*, not the animal's existence — a 2024
        # calf not yet firmly assigned. Register the animal and record that the name is
        # provisional; when it firms up the label changes and the identifier does not
        # (ADR-0011). A hedge may never live in a label (ADR-0009).
        provisional = desig.endswith("?")
        desig = desig.rstrip("?")
        if not DESIGNATION.match(desig):
            print(f"skipped unparseable designation: {desig!r}", file=sys.stderr)
            continue
        lineage = LINEAGE.match(desig).group(1)
        if current_lineage and current_lineage[0] == "PENDING":
            name = current_lineage[1]
            lineage_names.setdefault(
                lineage, re.sub(r"^(([Kk]nown as )?[Tt]he |[Kk]nown as )", "", name))
            current_lineage = None

        sex_raw = row["Gender"].strip()
        sex = {"F": "F", "M": "M"}.get(sex_raw, "U" if sex_raw else None)
        individuals[desig] = {
            "lineage": lineage,
            "sex": sex,
            "sex_raw": sex_raw,
            "born": edtf_year(row["Birth Year"]),
            "born_raw": row["Birth Year"].strip(),
            "deceased": row["D if Deceased, PD is Presumed Deceased"].strip(),
            "nicknames": [n.strip() for n in row["Nicknames"].split("/") if n.strip()],
            "namer": row["Who Nicknamed"].strip(),
            "alt": row["Additional Designations (Alaska or California)"].strip(),
            "provisional": provisional,
            "designation_raw": desig + ("?" if provisional else ""),
        }

    lineages = OrderedDict()
    for desig, rec in individuals.items():
        lineages.setdefault(rec["lineage"], []).append(desig)

    # --- sub-lineages (Q22) ---------------------------------------------------------
    # The judgement: a letter-suffixed animal with registered descendants heads a group
    # of her own, nested inside her mother's. (The sheet sexes 71 of the 73 heads F and
    # leaves T064B1 and T075C blank; descendants named after her are the evidence.) T073A and her calves are `T073As`, inside
    # `T073s`. This is what the field reports ("the T073As were off Sooke") and what a
    # hydrophone moderator hears; the top-level lineage alone made them record less than
    # they knew, permanently, because identifiers are never reused (ADR-0010).
    #
    # Minted BEFORE Q22 is answered, deliberately, because the two ways of being wrong
    # are not symmetric. If these groups turn out not to be real, each is deprecated as
    # `merged` with `replaced_by` its enclosing lineage, and a consumer may follow that
    # without asking anyone: "the T073As" was always a true, finer statement about the
    # T073s. If they are real and were never minted, every record made against `T073s`
    # is coarser than what its author knew and nothing can refine it afterwards.
    #
    # Three narrower judgements, none obviously right:
    #  - "Descendant" is read off the designation, exactly as the top-level lineages
    #    are. No parentage is consulted; parentage.tsv does not hold the Bigg's yet.
    #  - A head must herself be a registered animal. A gap in the sheet (calves with no
    #    row for their mother) yields no group rather than a group named for nobody.
    #  - An animal with no registered descendants heads nothing: T073B is in `T073s`
    #    and no narrower group, which is not a claim that she travels with her mother.
    sub_heads = sorted(
        d for d in individuals
        if d != individuals[d]["lineage"]
        and any(d in enclosing(other) for other in individuals))

    def deepest_group(desig, include_self):
        """The narrowest lineage `desig` belongs to, as a key into mat_id."""
        candidates = ([desig] if include_self else []) + enclosing(desig)
        return next(c for c in candidates
                    if c in sub_heads or c == individuals[desig]["lineage"])

    # --- assign identifiers deterministically -------------------------------------
    def mint(block, taken):
        n = block
        while n in taken:
            n += 1
        taken.add(n)
        return f"SSA:{n:07d}"

    mat_id = {}
    for lineage in sorted(lineages):
        label = f"{lineage}s"
        mat_id[lineage] = by_label.get(label) or mint(MATRILINE_BLOCK, used)

    # Sub-lineages are minted after every top-level lineage, so adding them cannot move
    # an identifier the first import already assigned.
    for head in sub_heads:
        mat_id[head] = by_label.get(f"{head}s") or mint(MATRILINE_BLOCK, used)

    ind_id = {}
    for desig in sorted(individuals):
        ind_id[desig] = by_label.get(desig) or mint(INDIVIDUAL_BLOCK, used)

    # --- emit ---------------------------------------------------------------------
    ent, nam, mem, sta = [], [], [], []

    def add_name(row):
        key = (row[0], row[1], row[3])
        if key not in known_names:
            known_names.add(key)
            nam.append(row)

    def add_status(row):
        key = (row[0], row[4], row[2])
        if key not in known_status:
            known_status.add(key)
            sta.append(row)

    # Every emitted row is checked against what is already on disk. Without this, a
    # second run appends duplicates — the schema rejects them, but only after the fact.
    def existing_keys(stem, idx):
        return {tuple(l.split("\t")[i] for i in idx)
                for l in (DATA / f"{stem}.tsv").read_text().splitlines()[1:]}

    known_entities = {r[0] for r in existing[1:]}
    known_edges = existing_keys("membership", (0, 1))
    known_names = existing_keys("names", (0, 1, 3))
    known_status = existing_keys("status", (0, 4, 2))

    for lineage in sorted(lineages):
        eid = mat_id[lineage]
        # Reusing an existing entity must not skip its edges — an earlier version of this
        # script did, leaving the seeded T090s with no parent.
        if (eid, BIGGS_ECOTYPE) not in known_edges:
            mem.append([eid, BIGGS_ECOTYPE, "", "", SOURCE, f"{lineage}s are Bigg's."])
        if eid in known_entities:
            continue
        note = (f"Derived from the designation prefix; the sheet groups {lineage} "
                "descendants across several blocks. Grouping unconfirmed — see Q22.")
        ent.append([eid, "group", "matriline", f"{lineage}s", "NCBITaxon:9733",
                    "", "", SOURCE, note])
        if lineage in lineage_names:
            add_name([eid, lineage_names[lineage], "common", "en", SOURCE,
                      "Recorded in the sheet as a \"Known as\" heading."])
        add_name([eid, lineage, "hidden", "en", SOURCE, "Bare designation."])

    for head in sub_heads:
        eid = mat_id[head]
        parent = deepest_group(head, include_self=False)
        if (eid, mat_id[parent]) not in known_edges:
            mem.append([eid, mat_id[parent], "", "", SOURCE,
                        f"{head}s are a sub-lineage of the {parent}s."])
        if eid in known_entities:
            continue
        ent.append([eid, "group", "matriline", f"{head}s", "NCBITaxon:9733", "", "",
                    SOURCE, f"{head} and her descendants, derived from the designation. "
                    "Minted ahead of Q22; if sub-lineages prove not to be real groups "
                    f"this merges into {parent}s."])
        add_name([eid, head, "hidden", "en", SOURCE, "Bare designation."])

    for desig in sorted(individuals):
        rec = individuals[desig]
        eid = ind_id[desig]
        notes = []
        if rec["sex_raw"] and rec["sex"] == "U":
            notes.append(f"Sex recorded in the sheet as {rec['sex_raw']!r}.")
        if rec["provisional"]:
            notes.append("The sheet records this designation as provisional "
                         f"({rec['designation_raw']}); the animal is registered, the "
                         "name is not yet settled.")
        if rec["born_raw"] and not rec["born"]:
            notes.append(f"Birth year recorded as {rec['born_raw']!r}; not parseable.")
        elif rec["born_raw"] and rec["born"] != rec["born_raw"]:
            notes.append(f"Sheet records {rec['born_raw']!r}.")
        if eid not in known_entities:
            ent.append([eid, "individual", "", desig, "NCBITaxon:9733",
                        rec["born"] or "", rec["sex"] or "", SOURCE, " ".join(notes)])
        if (eid, mat_id[rec["lineage"]]) not in known_edges:
            mem.append([eid, mat_id[rec["lineage"]], "", "", SOURCE, ""])
        # The edge to the top-level lineage above is kept, not moved, although it is now
        # implied by the narrower one. An imported row is never edited by the script
        # (ADR-0015), and it keeps the sub-lineages revocable as a set: take their rows
        # out and the register is exactly what it was.
        narrowest = deepest_group(desig, include_self=True)
        if narrowest != rec["lineage"] and (eid, mat_id[narrowest]) not in known_edges:
            mem.append([eid, mat_id[narrowest], "", "", SOURCE, ""])

        for nick in rec["nicknames"]:
            note = f"Named by {rec['namer']}." if rec["namer"] else ""
            add_name([eid, nick, "common", "en", SOURCE, note])
        if rec["alt"]:
            add_name([eid, rec["alt"], "hidden", "en", SOURCE,
                        "Alaska/California catalogue designation. A proper crosswalk "
                        "needs that catalogue's namespace — see Q23."])

        d = rec["deceased"]
        if d in ("D", "PD"):
            add_status([eid, "dead" if d == "D" else "presumed_dead",
                        f"../{SNAPSHOT}", "", "2026-07-28", SOURCE,
                        "The sheet records the death but not its date; EDTF states what "
                        "is known — it had happened by the snapshot."])
        elif d == "?":
            add_status([eid, "unknown", f"../{SNAPSHOT}", "", "2026-07-28", SOURCE,
                        "Sheet marks the animal's status uncertain."])
        elif rec["born"] and not rec["born"].startswith(".."):
            add_status([eid, "alive", rec["born"], "", "2026-07-28", SOURCE, ""])

    print(f"{len(individuals)} individuals, {len(lineages)} matrilines, "
          f"{len(sub_heads)} sub-lineages in the sheet; new rows: {len(ent)} entities, "
          f"{len(mem)} membership, {len(nam)} names, {len(sta)} status", file=sys.stderr)

    if "--apply" not in sys.argv:
        print("dry run; pass --apply to write", file=sys.stderr)
        return

    for stem, rows in (("entities", ent), ("names", nam),
                       ("membership", mem), ("status", sta)):
        path = DATA / f"{stem}.tsv"
        width = len(path.read_text().splitlines()[0].split("\t"))
        with path.open("a") as f:
            for r in rows:
                assert len(r) == width, (stem, r)
                assert not any("\t" in c for c in r), (stem, r)
                f.write("\t".join(r) + "\n")
    print("written", file=sys.stderr)


if __name__ == "__main__":
    main()
