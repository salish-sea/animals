#!/usr/bin/env python3
"""Write one static web page for every identifier in the register (ADR-0027).

Each identifier's global form is a w3id.org address (ADR-0026). This script writes the
page that address is meant to land on: what the entity is, what it belongs to, what
belongs to it, its mother, its names and where each claim came from. Each page also
carries, as JSON-LD, what Darwin Core can say about an Organism on its own: its
identifier, name, scope and taxon, the groups it belongs to and its mother. A program
that follows an `organismID` out of a GBIF occurrence finds a description it can read.
Sex, birth, life status and sources need the assertion and relationship tables of a
Darwin Core Data Package, which a single page has no form for, so only the HTML shows
them.

    python3 bin/build_pages.py --out build/pages

The pages are generated, like dist/, and never hand-edited. Unlike dist/ they are not
committed: a thousand HTML files would bury every data diff. They are built from one
edition of the register and say which.

Judgements this script makes, which are what a reviewer should check:
  - Individuals and groups are published as dwc:Organism. Darwin Core defines an
    Organism as "a particular organism or defined group of organisms considered to be
    taxonomically homogeneous", and its own example of an organismName is "J pod".
  - A group's organismScope is its rank (`matriline`, `pod`, ...). An individual's is
    `multicellular organism`, Darwin Core's own example value.
  - Taxon entities are NOT published as organisms, and not as taxa either: the register
    mints no taxon (ADR-0008). Their page says which NCBI taxon they stand in for, and
    gives NCBI's classification verbatim (ADR-0022).
  - Membership is genealogical (ADR-0005), so a group's page lists the members it
    descends to directly, never a count of them (ADR-0017).
  - Hidden names are not shown: a hidden name matches in search and is never displayed.
  - A retired identifier still gets a page, saying what replaced it (ADR-0010).
  - Every claim on a page names its source, because D-21 in SalishSea.io's rights policy
    requires the Bigg's sheet's maintainer to be credited wherever nicknames appear.
"""

import argparse
import html
import json
import shutil
import sqlite3
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import validate

ROOT = Path(__file__).resolve().parent.parent
GLOBAL = "https://w3id.org/salish-sea/animals/"
REPO = "https://github.com/salish-sea/animals"
NCBI = "https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id="

# Where a compact identifier from a crosswalk can be looked up. A prefix not listed here
# is shown as text.
CROSSWALK = {
    "NCBITaxon": NCBI,
    "inaturalist.taxon": "https://www.inaturalist.org/taxa/",
}

SEX = {"F": "female", "M": "male", "U": "unknown"}

e = html.escape


def digits(entity_id: str) -> str:
    return entity_id.split(":", 1)[1]


def global_id(entity_id: str) -> str:
    return GLOBAL + digits(entity_id)


def edition() -> tuple[str, str]:
    """The tag the working tree is at, if any, and its commit."""
    def git(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                              text=True).stdout.strip()
    return git("describe", "--tags", "--always", "--dirty"), git("rev-parse", "HEAD")


def load() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    validate.build(db)
    if validate.errors:
        for line in validate.errors:
            print(f"error: {line}", file=sys.stderr)
        sys.exit("the register does not validate; fix that first (bin/validate.py)")
    return db


class Register:
    """Everything a page needs, read once and indexed by entity."""

    def __init__(self, db: sqlite3.Connection):
        q = lambda sql: [dict(r) for r in db.execute(sql)]
        self.entities = {r["entity_id"]: r for r in q("SELECT * FROM entity")}
        self.sources = {r["source_id"]: r for r in q("SELECT * FROM source")}
        self.ranks = {r["rank"]: r for r in q("SELECT * FROM rank")}
        self.status = {r["entity_id"]: r for r in q("SELECT * FROM current_status")}
        self.retired = {r["entity_id"]: r for r in q("SELECT * FROM retired")}
        self.classification = {r["entity_id"]: r for r in q("SELECT * FROM classification")}
        self.taxa = {r["taxon_id"]: r for r in q("SELECT * FROM taxonomic_parent")}
        self.deprecation = {r["entity_id"]: r for r in q("SELECT * FROM deprecation")}

        self.member_of, self.members = defaultdict(list), defaultdict(list)
        for r in q("SELECT * FROM membership"):
            self.member_of[r["member_id"]].append(r)
            self.members[r["group_id"]].append(r)
        self.mothers, self.children = defaultdict(list), defaultdict(list)
        for r in q("SELECT * FROM parentage"):
            self.mothers[r["child_id"]].append(r)
            self.children[r["parent_id"]].append(r)
        self.matriarch, self.matriarch_of = {}, defaultdict(list)
        for r in q("SELECT * FROM matriarch"):
            self.matriarch[r["matriline_id"]] = r
            self.matriarch_of[r["matriarch_id"]].append(r)
        self.names, self.mappings = defaultdict(list), defaultdict(list)
        for r in q("SELECT * FROM name WHERE type <> 'hidden' ORDER BY type, name"):
            self.names[r["entity_id"]].append(r)
        for r in q("SELECT * FROM mapping"):
            self.mappings[r["subject_id"]].append(r)

    def label(self, entity_id: str) -> str:
        return self.entities[entity_id]["label"]

    def sort_key(self, entity_id: str) -> tuple:
        ent = self.entities[entity_id]
        return (ent["kind"] != "group", ent["label"].casefold(), entity_id)


# --- Darwin Core ------------------------------------------------------------------------

def organism_jsonld(reg: Register, entity_id: str) -> dict:
    """The entity as a dwc:Organism, in the terms a flat Darwin Core record would use."""
    ent = reg.entities[entity_id]
    # Only organisms: an ecotype is a member of a taxon entity, which is not one. Its
    # taxon is carried by dwc:taxonID below.
    associated = [f'"member of":"{global_id(m["group_id"])}"'
                  for m in reg.member_of[entity_id]
                  if not m["ends"] and reg.entities[m["group_id"]]["kind"] == "group"]
    associated += [f'"offspring of":"{global_id(p["parent_id"])}"'
                   for p in reg.mothers[entity_id]]
    doc = {
        "@context": {"dwc": "http://rs.tdwg.org/dwc/terms/",
                     "dcterms": "http://purl.org/dc/terms/"},
        "@id": global_id(entity_id),
        "@type": "dwc:Organism",
        "dwc:organismID": global_id(entity_id),
        "dwc:organismName": ent["label"],
        "dwc:organismScope": ent["rank"] if ent["kind"] == "group"
                             else "multicellular organism",
    }
    if associated:
        doc["dwc:associatedOrganisms"] = " | ".join(associated)
    taxon = reg.taxa.get(ent["taxon_id"])
    if taxon:
        # In Darwin Core an organism's taxon is an Identification of it. A flat record
        # carries the identification's terms beside the organism's, and so does this.
        doc["dwc:taxonID"] = taxon["taxon_id"]
        doc["dwc:scientificName"] = taxon["scientific_name"]
    if entity_id in reg.retired:
        r = reg.retired[entity_id]
        if r["replaced_by"]:
            doc["dcterms:isReplacedBy"] = {"@id": global_id(r["replaced_by"])}
    return doc


def taxon_jsonld(reg: Register, entity_id: str) -> dict:
    """A taxon entity: a register identifier standing in for an NCBI taxon. Not a taxon."""
    ent, cls = reg.entities[entity_id], reg.classification.get(entity_id, {})
    doc = {
        "@context": {"dwc": "http://rs.tdwg.org/dwc/terms/",
                     "skos": "http://www.w3.org/2004/02/skos/core#"},
        "@id": global_id(entity_id),
        "@type": "skos:Concept",
        "skos:prefLabel": ent["label"],
        "dwc:taxonID": ent["taxon_id"],
    }
    for term in ("scientific_name", "taxon_rank", "kingdom", "phylum", "class", "order",
                 "family", "genus"):
        if cls.get(term):
            key = {"scientific_name": "scientificName", "taxon_rank": "taxonRank"}.get(term, term)
            doc[f"dwc:{key}"] = cls[term]
    return doc


# --- HTML -------------------------------------------------------------------------------

STYLE = """\
:root { --bg: #fdfcfa; --fg: #1c1f22; --muted: #5d6670; --rule: #dcdfe2;
        --accent: #1f5f8b; --warn-bg: #fff4d6; --warn-fg: #6b4e00; color-scheme: light; }
@media (prefers-color-scheme: dark) {
  :root { --bg: #15181b; --fg: #e4e7ea; --muted: #9aa4ae; --rule: #2e343a;
          --accent: #7cb8e4; --warn-bg: #3a3014; --warn-fg: #f1d48a; color-scheme: dark; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg);
       font: 16px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width: 52rem; margin: 0 auto; padding: 1.5rem 16px 4rem; }
a { color: var(--accent); }
header.site { font-size: .875rem; color: var(--muted); margin-bottom: 1.5rem; }
h1 { font-size: 1.75rem; line-height: 1.2; margin: 0 0 .25rem; }
h2 { font-size: 1rem; text-transform: uppercase; letter-spacing: .04em; color: var(--muted);
     margin: 2rem 0 .5rem; border-bottom: 1px solid var(--rule); padding-bottom: .25rem; }
.kind { color: var(--muted); margin: 0 0 1rem; }
code, .id { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: .9em; }
dl { display: grid; grid-template-columns: max-content 1fr; gap: .25rem 1rem; margin: 0; }
dt { color: var(--muted); } dd { margin: 0; overflow-wrap: anywhere; }
ul { padding-left: 1.25rem; margin: .25rem 0; } li { margin: .15rem 0; }
.src { color: var(--muted); font-size: .8125rem; }
.note { color: var(--muted); font-size: .9375rem; }
.banner { background: var(--warn-bg); color: var(--warn-fg); padding: .75rem 1rem;
          border-radius: 6px; margin: 1rem 0; }
table { border-collapse: collapse; width: 100%; font-size: .9375rem; }
th, td { text-align: left; padding: .3rem .5rem .3rem 0; border-bottom: 1px solid var(--rule);
         vertical-align: top; }
th { color: var(--muted); font-weight: 600; }
input[type=search] { width: 100%; font: inherit; padding: .5rem .75rem; margin: .5rem 0 1rem;
                     border: 1px solid var(--rule); border-radius: 6px; background: var(--bg);
                     color: var(--fg); }
pre { overflow-x: auto; font-size: .8125rem; background: var(--warn-bg); background: color-mix(in srgb, var(--fg) 6%, var(--bg));
      padding: .75rem; border-radius: 6px; }
footer { margin-top: 3rem; font-size: .8125rem; color: var(--muted); }
@media (max-width: 30rem) { dl { grid-template-columns: 1fr; } dt { margin-top: .5rem; } }
"""


def page(title: str, body: str, depth: int, jsonld: dict | None, stamp: str) -> str:
    up = "../" * depth
    script = ""
    if jsonld:
        script = ('<script type="application/ld+json">\n'
                  + json.dumps(jsonld, indent=2, ensure_ascii=False).replace("<", "\\u003c")
                  + "\n</script>\n")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<link rel="stylesheet" href="{up}style.css">
{script}</head>
<body><main>
<header class="site"><a href="{up}">Salish Sea animals</a>, a register of individual
marine mammals and the groups they belong to</header>
{body}
<footer>{stamp}</footer>
</main></body>
</html>
"""


def link(reg: Register, entity_id: str, depth: int = 1) -> str:
    return (f'<a href="{"../" * depth}{digits(entity_id)}/">{e(reg.label(entity_id))}</a> '
            f'<span class="id">{e(entity_id)}</span>')


def src(reg: Register, source_id: str) -> str:
    s = reg.sources.get(source_id)
    name = s["name"] if s else source_id
    return f'<span class="src">· {e(name)}</span>'


def dates(starts: str | None, ends: str | None) -> str:
    if not starts and not ends:
        return ""
    return f' <span class="src">({e(starts or "…")}–{e(ends or "")})</span>'


def kind_line(reg: Register, ent: dict, sha: str) -> str:
    if ent["kind"] == "group":
        rank = reg.ranks.get(ent["rank"])
        word = e(rank["label"] if rank else ent["rank"])
        if rank and rank["definition_file"]:
            word = f'<a href="{REPO}/blob/{sha}/{e(rank["definition_file"])}">{word}</a>'
        return f"A group: {word}"
    if ent["kind"] == "individual":
        return "An individual animal"
    return "A taxon entity: the register's stand-in for an animal of this taxon, not resolved further"


def entity_page(reg: Register, entity_id: str, sha: str, stamp: str) -> str:
    ent = reg.entities[entity_id]
    out = [f'<h1>{e(ent["label"])}</h1>',
           f'<p class="kind">{kind_line(reg, ent, sha)}</p>']

    if entity_id in reg.retired:
        r, d = reg.retired[entity_id], reg.deprecation.get(entity_id, {})
        msg = f"This identifier is retired ({e(r['reason'])})."
        if r["replaced_by"]:
            msg += f" Use {link(reg, r['replaced_by'])} instead."
        if r["consider"]:
            msg += f" Consider {link(reg, r['consider'])}."
        out.append(f'<div class="banner">{msg}</div>')
        if d.get("note"):
            out.append(f'<p class="note">{e(d["note"])}</p>')

    facts = [("Identifier", f'<span class="id">{e(entity_id)}</span>'),
             ("Global form", f'<span class="id">{e(global_id(entity_id))}</span>')]
    taxon = reg.taxa.get(ent["taxon_id"])
    if taxon:
        facts.append(("Taxon", f'<i>{e(taxon["scientific_name"])}</i> '
                               f'<a class="id" href="{NCBI}{e(digits(taxon["taxon_id"]))}">'
                               f'{e(taxon["taxon_id"])}</a>'))
    if ent["born"]:
        facts.append(("Born", f'<code>{e(ent["born"])}</code>'))
    if ent["sex"]:
        facts.append(("Sex", SEX.get(ent["sex"], e(ent["sex"]))))
    st = reg.status.get(entity_id)
    if st:
        when = f' since <code>{e(st["effective"])}</code>' if st["effective"] else ""
        facts.append(("Status", f'{e(st["status"].replace("_", " "))}{when} {src(reg, st["source_id"])}'))
    facts.append(("Source", e(reg.sources[ent["source_id"]]["name"])))
    out.append("<dl>" + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in facts) + "</dl>")
    if ent["note"]:
        out.append(f'<p class="note">{e(ent["note"])}</p>')

    def section(title: str, items: list[str], intro: str = "") -> None:
        if items:
            out.append(f"<h2>{title}</h2>{intro}<ul>" + "".join(f"<li>{i}</li>" for i in items)
                       + "</ul>")

    section("Member of", [f'{link(reg, m["group_id"])}{dates(m["starts"], m["ends"])} '
                          f'{src(reg, m["source_id"])}'
                          for m in sorted(reg.member_of[entity_id],
                                          key=lambda m: reg.sort_key(m["group_id"]))])
    section("Members", [f'{link(reg, m["member_id"])}{dates(m["starts"], m["ends"])} '
                        f'{src(reg, m["source_id"])}'
                        for m in sorted(reg.members[entity_id],
                                        key=lambda m: reg.sort_key(m["member_id"]))],
            '<p class="note">Membership here is genealogical: who descends from whom, not '
            'who travels together. Only direct members are listed.</p>')
    if entity_id in reg.matriarch:
        m = reg.matriarch[entity_id]
        section("Named for", [f'{link(reg, m["matriarch_id"])} {src(reg, m["source_id"])}'])
    section("Matriarch of", [f'{link(reg, m["matriline_id"])} {src(reg, m["source_id"])}'
                             for m in reg.matriarch_of[entity_id]])
    section("Parents", [f'{e(p["role"])}: {link(reg, p["parent_id"])} {src(reg, p["source_id"])}'
                       for p in reg.mothers[entity_id]])
    section("Offspring", [f'{link(reg, p["child_id"])} {src(reg, p["source_id"])}'
                          for p in sorted(reg.children[entity_id],
                                          key=lambda p: reg.sort_key(p["child_id"]))])
    section("Other names", [f'{e(n["name"])} <span class="src">{e(n["type"])}, '
                            f'{e(n["language"] or "")}</span> {src(reg, n["source_id"])}'
                            for n in reg.names[entity_id]])

    maps = []
    for m in reg.mappings[entity_id]:
        prefix, _, local = m["object_id"].partition(":")
        obj = e(m["object_id"])
        if prefix in CROSSWALK:
            obj = f'<a class="id" href="{CROSSWALK[prefix]}{e(local)}">{obj}</a>'
        maps.append(f'<code>{e(m["predicate_id"])}</code> {obj} '
                    f'{e(m["object_label"] or "")} {src(reg, m["source_id"])}')
    section("Same thing elsewhere", maps)

    cls = reg.classification.get(entity_id)
    if cls:
        rows = [(r, cls[r]) for r in ("kingdom", "phylum", "class", "order", "family", "genus")
                if cls.get(r)]
        out.append("<h2>Classification, according to NCBI</h2><dl>"
                   + "".join(f"<dt>{r}</dt><dd>{e(v)}</dd>" for r, v in rows) + "</dl>")

    jsonld = (taxon_jsonld if ent["kind"] == "taxon" else organism_jsonld)(reg, entity_id)
    out.append('<h2>In Darwin Core</h2><p class="note">What Darwin Core can say about this '
               'entity on its own, for programs that follow a Darwin Core '
               '<code>organismID</code> here. It is embedded in this page as JSON-LD. Sex, '
               'birth, status and sources are not included: Darwin Core records them as '
               'separate assertions.</p><details><summary>Show</summary><pre>'
               + e(json.dumps(jsonld, indent=2, ensure_ascii=False)) + '</pre></details>')
    return page(f'{ent["label"]} ({entity_id})', "\n".join(out), 1, jsonld, stamp)


def index_page(reg: Register, stamp: str) -> str:
    rows = []
    for entity_id in sorted(reg.entities, key=reg.sort_key):
        ent = reg.entities[entity_id]
        what = ent["rank"] if ent["kind"] == "group" else ent["kind"]
        if entity_id in reg.retired:
            what += ", retired"
        rows.append(f'<tr><td><a href="{digits(entity_id)}/">{e(ent["label"])}</a></td>'
                    f'<td class="id">{e(entity_id)}</td><td>{e(what)}</td></tr>')
    body = f"""<h1>Salish Sea animals</h1>
<p>Every identifier in the register, with a page for each. An identifier's global form is
<code>{GLOBAL}</code> followed by its seven digits. See the
<a href="{REPO}">repository</a> for what the register is and how it is curated.</p>
<input type="search" id="filter" placeholder="Filter by name or identifier" aria-label="Filter">
<table><thead><tr><th>Name</th><th>Identifier</th><th>Kind</th></tr></thead>
<tbody id="rows">
{chr(10).join(rows)}
</tbody></table>
<script>
const f = document.getElementById('filter'), rows = [...document.querySelectorAll('#rows tr')];
f.addEventListener('input', () => {{
  const q = f.value.trim().toLowerCase();
  for (const r of rows) r.hidden = q && !r.textContent.toLowerCase().includes(q);
}});
</script>"""
    return page("Salish Sea animals", body, 0, None, stamp)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=ROOT / "build" / "pages",
                        help="directory to write the site into (default: build/pages)")
    args = parser.parse_args()

    reg = Register(load())
    tag, sha = edition()
    stamp = (f'Built from edition <a href="{REPO}/tree/{e(sha)}"><code>{e(tag)}</code></a>. '
             'Generated by <code>bin/build_pages.py</code>; never edited by hand. '
             'The register’s data is not yet licensed for redistribution.')

    args.out.mkdir(parents=True, exist_ok=True)
    # A directory left from a build of another edition would serve an entity this edition
    # does not have. Remove only identifier directories; leave anything else alone.
    current = {digits(i) for i in reg.entities}
    for d in args.out.iterdir():
        if d.is_dir() and len(d.name) == 7 and d.name.isdigit() and d.name not in current:
            shutil.rmtree(d)
    (args.out / "style.css").write_text(STYLE, encoding="utf-8")
    (args.out / "index.html").write_text(index_page(reg, stamp), encoding="utf-8")
    for entity_id in reg.entities:
        d = args.out / digits(entity_id)
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(entity_page(reg, entity_id, sha, stamp), encoding="utf-8")
    print(f"wrote {len(reg.entities)} pages to {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
