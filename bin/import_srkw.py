#!/usr/bin/env python3
"""Import Southern Resident individuals, mothers and matrilines from NOAA's census file.

The source is `orca.csv` in NOAA Northwest Fisheries Science Center's
github.com/noaa-nwfsc/srkw-status, read at a pinned commit (ADR-0023). It is the census
table behind NOAA's population projections and status reviews: one row per whale
catalogued since the census began, with `animal`, `birth`, `death`, `pod`, `matriline`,
`mom` and `sexF1M2`. The observations are the Center for Whale Research's.

As with the Bigg's import, **this script is the reviewable artefact** (ADR-0015): the
judgements below are what a reviewer checks, and the rows are its output.

Rights (salishsea-io D-22): a U.S. government work, public domain under 17 U.S.C. §105,
and factual anyway. The repository's GPL-3 covers its R code, which is not used here.

Idempotent: an identifier already assigned to a label is reused, and a row already on
disk is not appended again. The five illustrative `SEED` whales and two `SEED`
matrilines are taken over on the first run (ADR-0023, judgement 7); after that, nothing
the script wrote is ever edited by it (ADR-0015).

Usage:  python3 bin/import_srkw.py <path-to-orca.csv> [--apply]
"""

import csv
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import fold  # noqa: E402  (ADR-0019: the register's one comparison form)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SOURCE = "NOAA-NWFSC"

# The commit the rows come from, and the day they were written down. A refresh bumps
# both: `recorded` is status.tsv's precedence key and must say when we learned it.
PIN = "ba0b8c40e422aa9f5afcf845a0697b4d7d15701f"
# The file at PIN, so that a different orca.csv cannot be imported under PIN's name.
SHA256 = "151f297678eab0ed95e3db35a39a51328e1ea7340f9cab16779aab5ce65a5cd5"
RECORDED = "2026-10-06"

# NOAA's `pod` column codes the three pods with the designations of their first-listed
# animals. J001, K001 and L001 are ALSO whales in the `animal` column (J1 "Ruffles",
# born 1951, is the first row of the file), so the codes are read as pods only in `pod`.
POD = {"J001": "SSA:0000020", "K001": "SSA:0000021", "L001": "SSA:0000022"}

# Identifier blocks, for legibility only; nothing may parse them (ADR-0002). The seed
# used 101-105 and Bigg's uses 2000+ and 10000+, so Southern Residents get their own.
MATRILINE_BLOCK = 3000
INDIVIDUAL_BLOCK = 20000

# Published accounts that disagree with the file. NOAA's value is written; the other
# claim rides in the row's note, with its source, and settling it is later curation
# (ADR-0023, judgement 6). Keyed by (NOAA designation, what is disputed).
DISAGREEMENTS = {
    ("K047", "mother"): (
        "The Puget Sound Institute (C. Dunagan, 27 July 2026, \"Annual census could "
        "show an increase of two killer whales among southern residents\") names K43 "
        "Saturna as the likely mother, unconfirmed; the calf has been seen travelling "
        "with both K36 and K43."),
}


# Seed notes that explain the register's modelling rather than state a fact, and that
# the docs point at. They survive the take-over; every other seed note is superseded.
KEPT_NOTES = {
    ("entity", "J17"): "The individual, distinct from matriline J17s. See ADR-0003.",
    ("entity", "J17s"): "The matriline, distinct from individual J17. See ADR-0003.",
    ("membership", "L87"): ("Genealogical membership. L87's later travel with K and J "
                            "pods is NOT recorded here; see ADR-0005."),
}


def label(code):
    """NOAA's `J035` as the Southern Resident catalogues write it, `J35`.

    ADR-0023: a label is the preferred written form as the cited catalogues (CWR, The
    Whale Museum, Orca Network) write it, and none of them pads. The fold (ADR-0019)
    already maps `J035` to `J35`, so NOAA's spelling needs no names.tsv row. The three
    `-neonate` rows are calves that died before CWR designated them; their suffix is
    NOAA's and is kept, because no catalogue has a better name for them.
    """
    m = re.fullmatch(r"([JKL])0*(\d+)(-neonate)?", code)
    if not m:
        sys.exit(f"unrecognised designation {code!r}: the label rule needs a look")
    return f"{m.group(1)}{m.group(2)}{m.group(3) or ''}"


def read_census(path):
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if digest != SHA256:
        sys.exit(f"{path} is not orca.csv at {PIN[:7]} (sha256 {digest}). Fetch it from "
                 f"https://raw.githubusercontent.com/noaa-nwfsc/srkw-status/{PIN}/orca.csv, "
                 "or, to refresh, update PIN, SHA256 and RECORDED together.")
    with open(path, newline="", encoding="utf-8") as f:
        rows = {r["animal"]: r for r in csv.DictReader(f)}
    for r in rows.values():
        # `includeFec` and `includeSurv` say whether NOAA's demographic models use the
        # animal. They are modelling choices, not facts about the whale, and are not read.
        assert r["population"] == "SRKW", r
        assert r["pod"] in POD, r
        for col in ("mom", "death"):
            if r[col] == "NA":
                r[col] = None
    for a, r in rows.items():
        if r["mom"]:
            assert r["mom"] in rows, f"{a}'s mother {r['mom']} has no row"
            # A calf is in its mother's pod. Asserted, not assumed: if it ever fails,
            # the pod membership below would contradict the parentage.
            assert rows[r["mom"]]["pod"] == r["pod"], a
    return rows


def read_tsv(stem):
    lines = (DATA / f"{stem}.tsv").read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    return header, [dict(zip(header, l.split("\t"))) for l in lines[1:]]


def write_tsv(stem, header, rows):
    with (DATA / f"{stem}.tsv").open("w", encoding="utf-8") as f:
        f.write("\t".join(header) + "\n")
        for r in rows:
            cells = [r.get(h, "") for h in header]
            assert not any("\t" in c or "\n" in c for c in cells), (stem, r)
            f.write("\t".join(cells) + "\n")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    census = read_census(sys.argv[1])

    tables = {s: read_tsv(s) for s in
              ("entities", "membership", "parentage", "status", "sources")}
    ent_hdr, entities = tables["entities"]

    children = defaultdict(list)
    for a, r in census.items():
        if r["mom"]:
            children[r["mom"]].append(a)

    # --- 1. sex --------------------------------------------------------------------
    # 1 -> F and 2 -> M; every mother in the file but one is coded 1, which confirms the
    # reading. 0 -> blank (not known) rather than `U`: the file does not say whether 0
    # means "could not be determined" or "not yet recorded" (ADR-0023, judgement 4).
    #
    # The exception: K036 is coded 2 and is also named as K047's mother. Both cannot
    # hold. Rather than choose, the sex is left blank and the conflict noted; the
    # maternity is kept because it is the claim in dispute elsewhere (DISAGREEMENTS).
    sex, sex_note = {}, {}
    for a, r in census.items():
        sex[a] = {"1": "F", "2": "M", "0": ""}[r["sexF1M2"]]
        if a in children and sex[a] == "M":
            sex[a] = ""
            kids = ", ".join(label(c) for c in sorted(children[a]))
            sex_note[a] = (f"NOAA codes this animal male (sexF1M2 = 2) but names it as "
                           f"the mother of {kids}. Both cannot hold, so sex is left "
                           "blank until a curator settles which is wrong.")

    # --- 2. matrilines (ADR-0023, judgement 2) ----------------------------------------
    # Derived from parentage, not read from NOAA's `matriline` column, which names a
    # founding lineage (it files J35 under J9, the register has her in J17s).
    #
    # Which females anchor a matriline was left open by ADR-0023's review. The answer
    # here is the one the Bigg's import already gives (ADR-0015, Q22), so the register
    # has one rule, not two: **every female with a recorded calf heads a matriline, and
    # it nests inside her mother's.** J35 heads J35s, inside J17s, inside J5s.
    #  - It is time-stable. "Females with a living descendant" would make a group appear
    #    and vanish as animals die, and identifiers are permanent (ADR-0010).
    #  - It may be too fine. If the nested groups prove not to be real, each merges into
    #    its mother's with `replaced_by`, and a record made against "J35s" was always a
    #    true, finer statement about the J17s. If they are real and never minted, every
    #    record is permanently coarser than what its author knew. Same asymmetry as the
    #    Bigg's sub-lineages.
    #  - A female with no recorded mother heads a top-level matriline in her pod. NOAA's
    #    founding lineage often groups several of these (J4 and J5 are both "J8" and
    #    "J9" lineage), but the file records no mother to join them by, so they stay
    #    separate rather than be joined on a column read as something it is not.
    heads = sorted(children)

    # NOAA's founding lineage is still used, as the check that ADR-0016's independent
    # matriline assertion would otherwise have been: a calf filed under a different
    # founding lineage from its mother's is not placed in her matriline. The parentage
    # edge is written; the membership is flagged and the calf (with any matriline she
    # heads) is placed in the pod instead. Six animals in the pinned file.
    def placed_with_mother(a):
        mom = census[a]["mom"]
        return bool(mom) and census[a]["matriline"] == census[mom]["matriline"]

    def lineage_note(a):
        mom = census[a]["mom"]
        return (f"Not placed in {label(mom)}s: NOAA files {label(a)} under the "
                f"{label(census[a]['matriline'])} founding lineage and its mother "
                f"{label(mom)} under {label(census[mom]['matriline'])}. A split, an "
                "adoption or an error in one of the two columns; a curator decides.")

    # --- 3. identifiers ---------------------------------------------------------------
    # Reuse by folded label (ADR-0023, judgement 7): the seed's `J35` and NOAA's `J035`
    # meet under the fold. Only individuals and matrilines are candidates, so the pods,
    # whose labels are prose, cannot be matched by accident.
    by_fold = {}
    for e in entities:
        if e["kind"] == "individual" or e["rank"] == "matriline":
            by_fold.setdefault(fold(e["label"]), e)
    used = {int(e["entity_id"].split(":")[1]) for e in entities}

    def mint(block):
        n = block
        while n in used:
            n += 1
        used.add(n)
        return f"SSA:{n:07d}"

    ind_id, mat_id, taken_over = {}, {}, set()
    for a in sorted(census):
        hit = by_fold.get(fold(label(a)))
        if hit and hit["kind"] == "individual":
            ind_id[a] = hit["entity_id"]
            if hit["source_id"] == "SEED":
                taken_over.add(hit["entity_id"])
        else:
            ind_id[a] = mint(INDIVIDUAL_BLOCK)
    for h in heads:
        hit = by_fold.get(fold(label(h) + "s"))
        if hit and hit["rank"] == "matriline":
            mat_id[h] = hit["entity_id"]
            if hit["source_id"] == "SEED":
                taken_over.add(hit["entity_id"])
        else:
            mat_id[h] = mint(MATRILINE_BLOCK)

    # --- 4. rows ------------------------------------------------------------------------
    ent, mem, par, sta = [], [], [], []
    taxon = "NCBITaxon:9733"

    for h in heads:
        mom = census[h]["mom"]
        note = (f"{label(h)} and her descendants, derived from NOAA's maternity "
                "records (ADR-0023). Anchoring every mother's line as a matriline is "
                "unconfirmed")
        if mom and placed_with_mother(h):
            note += f"; if these prove too fine, this merges into {label(mom)}s."
        elif mom:
            note += (f". Her mother {label(mom)} is in a different NOAA founding "
                     "lineage, so this is a top-level matriline in her pod.")
        else:
            note += (". No mother is recorded for her in the file, so this is a "
                     "top-level matriline in her pod.")
        note = " ".join(filter(None, [note, KEPT_NOTES.get(("entity", f"{label(h)}s"))]))
        ent.append({"entity_id": mat_id[h], "kind": "group", "rank": "matriline",
                    "label": f"{label(h)}s", "taxon_id": taxon, "source_id": SOURCE,
                    "note": note})
        if mom and placed_with_mother(h):
            mem.append({"member_id": mat_id[h], "group_id": mat_id[mom],
                        "source_id": SOURCE,
                        "note": f"{label(h)}s are a line within the {label(mom)}s."})
        else:
            mem.append({"member_id": mat_id[h], "group_id": POD[census[h]["pod"]],
                        "source_id": SOURCE,
                        "note": lineage_note(h) if mom else ""})

    for a in sorted(census):
        r, eid = census[a], ind_id[a]
        notes = [sex_note[a]] if a in sex_note else []
        if ("entity", label(a)) in KEPT_NOTES:
            notes.append(KEPT_NOTES[("entity", label(a))])
        if a.endswith("-neonate"):
            notes.append("A calf that died before it was given a designation; the "
                         "label is NOAA's placeholder.")
        ent.append({"entity_id": eid, "kind": "individual", "label": label(a),
                    "taxon_id": taxon, "born": r["birth"], "sex": sex[a],
                    "source_id": SOURCE, "note": " ".join(notes)})

        # Narrowest group: the matriline she heads, else her mother's, else the pod.
        if a in mat_id:
            mem.append({"member_id": eid, "group_id": mat_id[a], "source_id": SOURCE,
                        "note": ""})
        elif r["mom"] and placed_with_mother(a):
            mem.append({"member_id": eid, "group_id": mat_id[r["mom"]],
                        "source_id": SOURCE, "note": ""})
        else:
            mem.append({"member_id": eid, "group_id": POD[r["pod"]], "source_id": SOURCE,
                        "note": lineage_note(a) if r["mom"] else
                        "No mother recorded, so no matriline is derived."})
        if ("membership", label(a)) in KEPT_NOTES:
            mem[-1]["note"] = KEPT_NOTES[("membership", label(a))]

        # Parentage (ADR-0023, judgement 1). The file names no fathers.
        if r["mom"]:
            par.append({"child_id": eid, "parent_id": ind_id[r["mom"]], "role": "mother",
                        "source_id": SOURCE,
                        "note": DISAGREEMENTS.get((a, "mother"), "")})

        # Status (ADR-0023, judgement 5). A death year becomes `presumed_dead`: the file
        # does not separate whales missing from the census from those found dead, and
        # disappearance is how most Southern Resident deaths are known. `dead` waits for
        # a second source naming a carcass or necropsy.
        #
        # `alive` from the birth year is written too, so that "was J17 alive in 2010?"
        # (C4) has an answer. Except when birth and death share a year: current_status
        # breaks ties on `effective`, and a tie between `alive` and `presumed_dead` in
        # the same year would make the answer arbitrary.
        if r["birth"] != r["death"]:
            sta.append({"entity_id": eid, "status": "alive", "effective": r["birth"],
                        "recorded": RECORDED, "source_id": SOURCE, "note": ""})
        if r["death"]:
            sta.append({"entity_id": eid, "status": "presumed_dead",
                        "effective": r["death"], "recorded": RECORDED,
                        "source_id": SOURCE, "note": "NOAA gives the year only."})

    # --- 5. merge into the tables --------------------------------------------------------
    # The seed rows for the taken-over entities are replaced wholesale: their entity row
    # is rewritten under NOAA's authority, and their seed edges and statuses go. Their
    # nicknames stay `SEED` in names.tsv until a naming source is chosen (ADR-0023).
    # Everything else already on disk is kept, and nothing already present is appended.
    ent_by_id = {e["entity_id"]: e for e in ent}
    entities = [ent_by_id.pop(e["entity_id"]) if e["entity_id"] in taken_over else e
                for e in entities]
    known_ids = {e["entity_id"] for e in entities}
    new_entities = [e for e in ent if e["entity_id"] not in known_ids]
    entities += new_entities

    def merge(stem, rows, key, owner):
        header, old = tables[stem]
        kept = [r for r in old
                if not (r["source_id"] == "SEED" and r[owner] in taken_over)]
        keys = {tuple(r[k] for k in key) for r in kept}
        added = [r for r in rows if tuple(r[k] for k in key) not in keys]
        return header, kept + added, len(old) - len(kept), len(added)

    out = {
        "membership": merge("membership", mem, ("member_id", "group_id"), "member_id"),
        "parentage": merge("parentage", par, ("child_id", "role"), "child_id"),
        "status": merge("status", sta, ("entity_id", "status", "effective"),
                        "entity_id"),
    }

    # One source row, pointing at the snapshot most recently read. A refresh moves its
    # url and date forward; which snapshot an older row came from is in git history,
    # which is the register's assertion-time axis (ADR-0006), and in status.tsv's
    # `recorded`.
    src_hdr, sources = tables["sources"]
    sources = [s for s in sources if s["source_id"] != SOURCE]
    sources.append({
        "source_id": SOURCE,
        "name": "NOAA NWFSC Southern Resident census (srkw-status, orca.csv)",
        "url": f"https://github.com/noaa-nwfsc/srkw-status/blob/{PIN}/orca.csv",
        "scope": "SRKW individuals, mothers, sex, birth and death years, pods",
        "license": "public-domain",
        "license_status": "cleared",
        "retrieved_on": RECORDED,
        "note": ("The observations are the Center for Whale Research's annual "
                 "photo-identification census, made under NOAA contract; CWR is "
                 "credited as the observer and NOAA NWFSC as the publisher of the "
                 "table. U.S. government work (17 U.S.C. §105); the repository's "
                 "GPL-3 covers its code, not these facts. Assessed as D-22 in "
                 "salishsea-io/docs/rights-policy.md section 7.2. Imported by "
                 "bin/import_srkw.py (ADR-0023)."),
    })

    # Drift: a row this script wrote from an earlier snapshot that the current one no
    # longer produces. Appending would leave both the old claim and the new one, and
    # replacing would edit an imported row, which only a curator may do (ADR-0015). So
    # the run stops and lists them. A curator corrects each row by hand, changing its
    # `source_id` to whoever now stands behind it, and re-runs. A row a curator has
    # already taken over no longer carries SOURCE and is not this script's concern.
    generated = {
        "entities": {e["entity_id"]: (e["label"], e.get("born", ""), e.get("sex", ""))
                     for e in ent},
        "membership": {(m["member_id"], m["group_id"]) for m in mem},
        "parentage": {(p["child_id"], p["role"]): p["parent_id"] for p in par},
        "status": {(s["entity_id"], s["status"], s["effective"]) for s in sta},
    }
    drift = []
    for e in entities:
        if (e["source_id"] == SOURCE and e["entity_id"] in generated["entities"]
                and e["entity_id"] not in taken_over):
            was = (e["label"], e.get("born", ""), e.get("sex", ""))
            now = generated["entities"][e["entity_id"]]
            if was != now:
                drift.append(f"entities: {e['entity_id']} was {was}, census now {now}")
    for r in tables["membership"][1]:
        if r["source_id"] == SOURCE and (r["member_id"], r["group_id"]) not in \
                generated["membership"]:
            drift.append(f"membership: {r['member_id']} in {r['group_id']} is no longer "
                         "derived")
    for r in tables["parentage"][1]:
        key = (r["child_id"], r["role"])
        if r["source_id"] == SOURCE and generated["parentage"].get(key) != r["parent_id"]:
            drift.append(f"parentage: {r['child_id']}'s {r['role']} was {r['parent_id']}, "
                         f"census now {generated['parentage'].get(key) or 'none'}")
    for r in tables["status"][1]:
        if r["source_id"] == SOURCE and (r["entity_id"], r["status"], r["effective"]) \
                not in generated["status"]:
            drift.append(f"status: {r['entity_id']} {r['status']} from {r['effective']} "
                         "is no longer in the census")

    print(f"{len(census)} whales, {len(heads)} matrilines in the census; "
          f"{len(taken_over)} seed entities taken over; new: {len(new_entities)} "
          "entities, " + ", ".join(f"{n} {s} (-{d} seed)" for s, (_, _, d, n)
                                    in out.items()), file=sys.stderr)
    for d in drift:
        print(f"drift: {d}", file=sys.stderr)
    if drift:
        sys.exit(f"{len(drift)} imported rows disagree with this snapshot; correct them "
                 "by hand (ADR-0015) and re-run. Nothing written.")

    if "--apply" not in sys.argv:
        print("dry run; pass --apply to write", file=sys.stderr)
        return
    write_tsv("entities", ent_hdr, entities)
    for stem, (header, rows, _, _) in out.items():
        write_tsv(stem, header, rows)
    write_tsv("sources", src_hdr, sources)
    print("written", file=sys.stderr)


if __name__ == "__main__":
    main()
