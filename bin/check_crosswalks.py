#!/usr/bin/env python3
"""Check the register's crosswalks against the authorities they point at.

`bin/validate.py` proves the register is internally consistent. It cannot prove that
`inaturalist.taxon:1368491` still names a live concept, because that fact lives on
someone else's server. This script asks.

Two kinds of finding, and the difference matters:

  DRIFT      an object we point at has moved — deactivated, merged, or renamed.
             Not our error. Upstream is allowed to change; we are only obliged to
             notice. Reported, and non-fatal unless --strict.

  BAD        a mapping that was wrong when it was written — an identifier that does
             not resolve at all, or one added in this pull request that already
             points at an inactive taxon. That is a defect, caught cheaply at review
             time, and fails.

Why this exists: on 2026-08-27 an audit of SalishSea.io's taxon mirror found nine
iNaturalist taxa deactivated upstream, four of them from a single genus split
(Sagmatias -> Aethalodelphis). The register's own mapping was correct throughout —
but there was no way to know that without asking the API, and no process that would
ever have asked. See ADR-0008 on why species identity is delegated, which is
precisely what makes these crosswalks load-bearing.

Scope: this checks crosswalks only. Coverage — "which taxa does a consumer hold that
the register has no entity for?" — needs a consumer's corpus, which the register does
not have and should not acquire. That check belongs to the consumer.

Usage:
    python3 bin/check_crosswalks.py [--strict] [--github] [--offline]

    --strict   treat drift as an error too (scheduled runs that should shout)
    --github   emit ::warning:: / ::error:: annotations for GitHub Actions
    --offline  skip every network call; only check that identifiers are well-formed
"""

import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

USER_AGENT = "salish-sea/animals crosswalk check (+https://github.com/salish-sea/animals)"

# iNaturalist accepts a comma-separated list of ids and asks for courtesy: no more
# than ~60 requests/minute, and they prefer far fewer. 30 ids per call keeps the whole
# register inside a handful of requests.
INAT_BATCH = 30
INAT_PAUSE_S = 1.1
INAT_URL = "https://api.inaturalist.org/v1/taxa/{ids}"

# EBI's Ontology Lookup Service resolves NCBITaxon, which is what ADR-0008 chose over
# WoRMS on tooling grounds. One request per term; there is no batch endpoint, and the
# register holds few enough taxon entities for that to be fine.
OLS_URL = "https://www.ebi.ac.uk/ols4/api/ontologies/ncbitaxon/terms"


class Finding:
    """A single problem, with enough context for a curator to fix it in one edit."""

    def __init__(self, kind: str, subject: str, message: str, fix: str = "") -> None:
        self.kind = kind  # "drift" | "bad"
        self.subject = subject
        self.message = message
        self.fix = fix

    def __str__(self) -> str:
        line = f"{self.subject}: {self.message}"
        return f"{line}\n    fix: {self.fix}" if self.fix else line


def read_tsv(name: str) -> list[dict[str, str]]:
    with (DATA / f"{name}.tsv").open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def check_inaturalist(offline: bool) -> list[Finding]:
    """Every `inaturalist.taxon:` object in mappings.tsv, against the iNaturalist API.

    Three things can be wrong: the id does not resolve; it resolves but is inactive
    (iNaturalist then names its replacement in `current_synonymous_taxon_ids`, so the
    fix is a one-line edit); or it resolves and is active but no longer carries the
    name we recorded in `object_label`, which makes our TSV misleading to read even
    though nothing is broken.
    """
    findings: list[Finding] = []
    wanted: dict[str, dict[str, str]] = {}

    for row in read_tsv("mappings"):
        obj = row["object_id"]
        if not obj.startswith("inaturalist.taxon:"):
            continue
        taxon_id = obj.split(":", 1)[1]
        if not taxon_id.isdigit():
            findings.append(Finding(
                "bad", row["subject_id"],
                f"{obj} is not a numeric iNaturalist taxon id",
                "iNaturalist taxon identifiers are integers.",
            ))
            continue
        wanted[taxon_id] = row

    if offline or not wanted:
        return findings

    ids = sorted(wanted)
    seen: set[str] = set()
    for i in range(0, len(ids), INAT_BATCH):
        batch = ids[i:i + INAT_BATCH]
        try:
            payload = fetch_json(INAT_URL.format(ids=",".join(batch)))
        except (urllib.error.URLError, TimeoutError) as exc:
            # A network failure is not a data problem. Say so and stop, rather than
            # reporting every unchecked mapping as if it were broken.
            findings.append(Finding(
                "bad", "iNaturalist",
                f"could not be reached: {exc}",
                "Re-run when the API is available; this is not a register defect.",
            ))
            return findings

        for taxon in payload.get("results", []):
            tid = str(taxon["id"])
            seen.add(tid)
            row = wanted[tid]
            subject = f"{row['subject_id']} -> inaturalist.taxon:{tid}"

            if not taxon.get("is_active"):
                replacements = taxon.get("current_synonymous_taxon_ids") or []
                target = (
                    f"inaturalist.taxon:{replacements[0]}" if len(replacements) == 1
                    else f"one of {replacements}" if replacements
                    else "no replacement offered by iNaturalist"
                )
                findings.append(Finding(
                    "drift", subject,
                    f"'{taxon.get('name')}' is INACTIVE upstream",
                    f"Repoint mappings.tsv at {target}, and check whether names.tsv "
                    f"should keep the old name as type=historical.",
                ))
            elif taxon.get("name") != row["object_label"]:
                findings.append(Finding(
                    "drift", subject,
                    f"renamed upstream: object_label says '{row['object_label']}', "
                    f"iNaturalist now says '{taxon.get('name')}'",
                    "Update object_label. The id is still correct, so nothing else "
                    "changes.",
                ))

        time.sleep(INAT_PAUSE_S)

    for missing in sorted(set(ids) - seen):
        row = wanted[missing]
        findings.append(Finding(
            "bad", f"{row['subject_id']} -> inaturalist.taxon:{missing}",
            "does not resolve at iNaturalist",
            "Check the identifier. iNaturalist does not reuse taxon ids, so a "
            "non-resolving one was probably never right.",
        ))

    return findings


def check_ncbi(offline: bool) -> list[Finding]:
    """Every `NCBITaxon:` id in entities.tsv, against the Ontology Lookup Service.

    ADR-0008 delegates species identity to NCBI, so a `taxon_id` that has been merged
    or withdrawn silently detaches an entity from the authority it claims to reference.
    OLS reports obsolete terms explicitly.
    """
    findings: list[Finding] = []
    wanted: list[tuple[str, str, str]] = []

    for row in read_tsv("entities"):
        raw = (row.get("taxon_id") or "").strip()
        if not raw:
            continue
        if not raw.startswith("NCBITaxon:"):
            findings.append(Finding(
                "bad", row["entity_id"],
                f"taxon_id '{raw}' is not an NCBITaxon CURIE",
                "ADR-0008 fixes the authority as NCBI; use NCBITaxon:<id>.",
            ))
            continue
        wanted.append((row["entity_id"], raw, row.get("label", "")))

    if offline:
        return findings

    # Several entities legitimately share a taxon_id — every ecotype of Orcinus orca
    # points at NCBITaxon:9733 — so ask once per distinct id and report per entity.
    by_curie: dict[str, list[tuple[str, str]]] = {}
    for entity_id, curie, label in wanted:
        by_curie.setdefault(curie, []).append((entity_id, label))

    for curie, holders in sorted(by_curie.items()):
        iri = f"http://purl.obolibrary.org/obo/NCBITaxon_{curie.split(':', 1)[1]}"
        url = f"{OLS_URL}?iri={urllib.parse.quote(iri, safe='')}"
        try:
            payload = fetch_json(url)
        except (urllib.error.URLError, TimeoutError) as exc:
            findings.append(Finding(
                "bad", "OLS",
                f"could not be reached: {exc}",
                "Re-run when the service is available; not a register defect.",
            ))
            return findings

        terms = payload.get("_embedded", {}).get("terms", [])
        subjects = ", ".join(e for e, _ in holders)
        if not terms:
            findings.append(Finding(
                "drift", f"{subjects} -> {curie}",
                "does not resolve at the Ontology Lookup Service",
                "NCBI may have merged the taxon. Check "
                f"https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id="
                f"{curie.split(':', 1)[1]}",
            ))
            continue
        term = terms[0]
        if term.get("is_obsolete"):
            findings.append(Finding(
                "drift", f"{subjects} -> {curie}",
                f"is marked OBSOLETE in NCBITaxon ('{term.get('label')}')",
                "Repoint taxon_id at the current NCBI taxon.",
            ))

    return findings


def check_new_mappings(base_file: Path) -> list[Finding]:
    """Mappings added since `base_file` must not already be inactive.

    Drift is forgiven because upstream moved after we wrote the row. A mapping that is
    stale on the day it is added is a different thing, and a pull request is the
    cheapest place to catch it. Callers pass the base branch's mappings.tsv; anything
    here that is also in the drift findings is upgraded from drift to bad.
    """
    with base_file.open(newline="", encoding="utf-8") as fh:
        base = {(r["subject_id"], r["object_id"]) for r in csv.DictReader(fh, delimiter="\t")}
    added = {
        (r["subject_id"], r["object_id"])
        for r in read_tsv("mappings")
        if (r["subject_id"], r["object_id"]) not in base
    }
    return [Finding("added", f"{s} -> {o}", "added in this change") for s, o in sorted(added)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true",
                        help="treat drift as an error, not a warning")
    parser.add_argument("--github", action="store_true",
                        help="emit GitHub Actions annotations")
    parser.add_argument("--offline", action="store_true",
                        help="skip network calls; check identifier syntax only")
    parser.add_argument("--added-since", type=Path, metavar="FILE",
                        help="path to the base revision's mappings.tsv; drift on a "
                             "mapping added since then is an error rather than a warning")
    args = parser.parse_args()

    findings = check_inaturalist(args.offline) + check_ncbi(args.offline)

    if args.added_since and args.added_since.exists():
        added = {f.subject for f in check_new_mappings(args.added_since)}
        for finding in findings:
            if finding.kind == "drift" and finding.subject in added:
                finding.kind = "bad"
                finding.message += " — and this mapping is new in this change"

    drift = [f for f in findings if f.kind == "drift"]
    bad = [f for f in findings if f.kind == "bad"]

    for finding in drift:
        prefix = "::warning::" if args.github else "warning: "
        print(f"{prefix}{finding}", file=sys.stderr)
    for finding in bad:
        prefix = "::error::" if args.github else "error: "
        print(f"{prefix}{finding}", file=sys.stderr)

    checked = "syntax only (offline)" if args.offline else "iNaturalist and NCBITaxon"
    print(f"\nchecked {checked}: {len(drift)} drifted, {len(bad)} broken",
          file=sys.stderr)

    if bad or (drift and args.strict):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
