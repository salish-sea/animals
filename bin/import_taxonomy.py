#!/usr/bin/env python3
"""Cache NCBI's lineage for every taxon the register points at.

The register delegates species identity to NCBI (ADR-0008) and, until ADR-0022, held no
taxonomy at all: its taxon entities were flat. Consumers still need one -- a DarwinCore
export wants kingdom through genus, and "which of these are pinnipeds" is a question about
ancestry -- and the only tree on offer was iNaturalist's, which ADR-0008 says is not the
authority.

This script is the answer that keeps the delegation honest. It does not curate a tree and
it mints nothing. It asks NCBI for the lineage of each `taxon_id` in entities.tsv and
writes that excerpt, in NCBI's own identifiers, ranks and names, to
data/taxonomic_parent.tsv. **This script is the reviewable artefact** (ADR-0015): the rows
are its output, and anyone can reproduce them.

Judgements it makes, all deliberately small:
  - The WHOLE lineage is kept, including NCBI's unranked clades (Boreoeutheria,
    Whippomorpha...). About half of a mammal's ancestors have no rank. Dropping them
    would be editing NCBI's tree; a consumer that wants only ranked ancestors filters.
  - Names and ranks are recorded verbatim. NCBI's kingdom for animals is `Metazoa`, not
    `Animalia`, and its order for a killer whale is `Artiodactyla` with `Cetacea` an
    infraorder. Those are NCBI's positions, reported as such; a consumer that must say
    `Animalia` maps that one value on its own side and records why.
  - The root is the first node NCBI lists (`cellular organisms`). Its parent is empty.
  - No date is written per row, so an unchanged NCBI changes no row however often this
    runs. When the excerpt was last taken is `retrieved_on` on the NCBI row of
    sources.tsv, which --apply stamps with today's date -- and only --apply, because
    "we looked today and it still says this" is a claim, and a dry run makes none.

Deterministic and idempotent. Rows are sorted by identifier.

Usage:
    python3 bin/import_taxonomy.py            # dry run: report what would change
    python3 bin/import_taxonomy.py --apply    # rewrite data/taxonomic_parent.tsv
    python3 bin/import_taxonomy.py --check    # exit 1 if NCBI's lineage has moved
"""

import csv
import datetime
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "taxonomic_parent.tsv"
SOURCE = "NCBI"
PREFIX = "NCBITaxon:"
HEADER = ["taxon_id", "parent_id", "rank", "scientific_name", "source_id"]
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
# NCBI asks for a tool name and no more than three requests a second without a key. One
# request covers every taxon the register holds.
TOOL = "salish-sea-animals-register"


def wanted():
    """Every distinct NCBI identifier an entity points at."""
    with (DATA / "entities.tsv").open() as f:
        ids = {r["taxon_id"] for r in csv.DictReader(f, delimiter="\t") if r["taxon_id"]}
    # ASCII digits and nothing else. `int()` is more generous than NCBI -- it takes `+1`
    # and Unicode digits -- and this reads entities.tsv directly, before the schema has
    # had a chance to refuse anything.
    malformed = sorted(i for i in ids if not re.fullmatch(PREFIX + r"[0-9]+", i, re.ASCII))
    if malformed:
        sys.exit(f"taxon_id is not {PREFIX}<digits>, so it cannot be looked up here: {malformed}")
    return sorted(ids, key=lambda i: int(i[len(PREFIX):]))


def fetch(ids):
    query = urllib.parse.urlencode({
        "db": "taxonomy", "retmode": "xml", "tool": TOOL,
        "id": ",".join(i[len(PREFIX):] for i in ids)})
    with urllib.request.urlopen(f"{EFETCH}?{query}", timeout=60) as r:
        return ET.fromstring(r.read())


def rows_from(tree, ids):
    """One row per node on any requested taxon's path to the root."""
    nodes = {}

    def add(taxid, parent, rank, name):
        row = (PREFIX + taxid, PREFIX + parent if parent else "", rank, name, SOURCE)
        # The same ancestor arrives once per descendant. NCBI must agree with itself.
        if nodes.setdefault(row[0], row) != row:
            sys.exit(f"NCBI gave two different answers for {row[0]}: {nodes[row[0]]} / {row}")

    found = set()
    for taxon in tree.findall("Taxon"):
        taxid = taxon.findtext("TaxId")
        found.add(PREFIX + taxid)
        parent = ""
        for anc in taxon.findall("LineageEx/Taxon"):
            add(anc.findtext("TaxId"), parent, anc.findtext("Rank"), anc.findtext("ScientificName"))
            parent = anc.findtext("TaxId")
        # ParentTaxId and the last lineage entry are the same fact stated twice.
        if taxon.findtext("ParentTaxId") != parent:
            sys.exit(f"{PREFIX}{taxid}: ParentTaxId disagrees with the end of its lineage")
        add(taxid, parent, taxon.findtext("Rank"), taxon.findtext("ScientificName"))

    # An identifier NCBI has merged comes back under its NEW id, so the old one is simply
    # absent. That is drift in a taxon_id, and it must be fixed in entities.tsv by a
    # person, not papered over here.
    missing = [i for i in ids if i not in found]
    if missing:
        sys.exit(f"NCBI returned no taxon for {missing} -- merged or deleted upstream?")
    return sorted(nodes.values(), key=lambda r: int(r[0][len(PREFIX):]))


def current():
    if not OUT.exists():
        return []
    with OUT.open() as f:
        return [tuple(r) for r in list(csv.reader(f, delimiter="\t"))[1:]]


def main():
    ids = wanted()
    rows = rows_from(fetch(ids), ids)
    old = current()
    added = sorted(set(rows) - set(old))
    removed = sorted(set(old) - set(rows))
    print(f"{len(ids)} taxa, {len(rows)} nodes on their lineages; "
          f"{len(added)} row(s) new or changed, {len(removed)} gone or changed",
          file=sys.stderr)
    for r in removed:
        print("  - " + " | ".join(r), file=sys.stderr)
    for r in added:
        print("  + " + " | ".join(r), file=sys.stderr)

    if "--check" in sys.argv:
        sys.exit(1 if added or removed else 0)
    if "--apply" not in sys.argv:
        print("dry run; pass --apply to write", file=sys.stderr)
        return
    # Everything that can refuse, refuses before anything is written: a sources.tsv this
    # cannot stamp must not leave a new excerpt behind with an old date on it. Both files
    # are tracked, so a crash between the two writes is a `git checkout`, not a loss, and
    # nothing heavier than this ordering is warranted.
    today, stamped = stamped_sources()
    with OUT.open("w", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(HEADER)
        w.writerows(rows)
    (DATA / "sources.tsv").write_text(stamped)
    print(f"wrote {OUT.relative_to(ROOT)}; stamped {SOURCE}.retrieved_on = {today}",
          file=sys.stderr)


def stamped_sources():
    """sources.tsv with today on the NCBI row, as text. Exits if it cannot be produced."""
    lines = (DATA / "sources.tsv").read_text().split("\n")
    header = lines[0].split("\t")
    if "retrieved_on" not in header:
        sys.exit("sources.tsv has no retrieved_on column")
    col = header.index("retrieved_on")
    hits = [i for i, line in enumerate(lines) if line.split("\t")[0] == SOURCE]
    if len(hits) != 1:
        sys.exit(f"expected exactly one {SOURCE} row in sources.tsv, found {len(hits)}")
    cells = lines[hits[0]].split("\t")
    if len(cells) != len(header):
        sys.exit(f"the {SOURCE} row of sources.tsv has {len(cells)} fields, header has {len(header)}")
    today = datetime.date.today().isoformat()
    cells[col] = today
    lines[hits[0]] = "\t".join(cells)
    return today, "\n".join(lines)


if __name__ == "__main__":
    main()
