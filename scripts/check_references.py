#!/usr/bin/env python3
"""Check up to 15 public citation identifiers with the hosted VetEvidence service."""

import argparse
import csv
import json
import re
import sys
from collections import defaultdict, deque
from http.client import HTTPException
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ENDPOINT = "https://vetevidence.com/vecs/batch"
IDENTIFIER = re.compile(r"(?:[1-9][0-9]*|PMC[1-9][0-9]*|10\.[0-9]{4,9}/\S+)", re.I)
TIERS = {"A": "I", "B": "II", "C": "III", "D": "IV", "E": "V"}


def validate(identifiers):
    if not isinstance(identifiers, list) or not 1 <= len(identifiers) <= 15:
        raise ValueError("Supply 1–15 identifiers per request.")
    if any(not isinstance(i, str) or not IDENTIFIER.fullmatch(i) for i in identifiers):
        raise ValueError("Use bare PMIDs, PMCIDs or DOIs, one identifier per entry.")


def assess(identifiers):
    request = Request(ENDPOINT, data=json.dumps({"ids": identifiers}).encode(),
                      headers={"Content-Type": "application/json", "Accept": "application/json",
                               "User-Agent": "VetClaw-reference-checker/1.0"})
    with urlopen(request, timeout=120) as response:
        return json.load(response)


def assessment_link(identifier):
    if identifier.isdigit():
        field = "pmid"
    elif identifier.upper().startswith("PMC"):
        field = "pmcid"
    else:
        field = "doi"
    return "https://vetevidence.com/?" + urlencode({field: identifier})


def summarize(identifiers, payload):
    if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
        raise ValueError("VetEvidence returned an unexpected response.")
    by_id = defaultdict(deque)
    for item in payload["results"]:
        if not isinstance(item, dict) or item.get("id") not in identifiers:
            raise ValueError("VetEvidence returned an unexpected result identifier.")
        by_id[item["id"]].append(item)

    results = []
    for identifier in identifiers:
        queue = by_id[identifier]
        row = queue.popleft() if queue else {"error": "No result returned"}
        error = row.get("error")
        tier = TIERS.get(row.get("effective_tier"))
        verification = row.get("verifiability")
        if verification in ("retracted", "predatory"):
            tier = None
        signals = row.get("dimension_signals") or []
        source = row.get("source") or {}
        if not isinstance(source, dict) or not isinstance(signals, list):
            raise ValueError("VetEvidence returned unexpected source metadata.")
        species = next((s.get("detail") for s in signals
                        if isinstance(s, dict) and s.get("name") == "Species applicability"), None)
        title = source.get("title")
        results.append({
            "identifier": identifier,
            "tier": tier if not error else None,
            "verification": verification,
            "species_applicability": species,
            "title": title,
            "error": error,
            "url": assessment_link(identifier),
        })
    return {"results": results, "notes": payload.get("notes", [])}


def check_references(identifiers):
    validate(identifiers)
    return summarize(identifiers, assess(identifiers))


def report(assessment, output, errors):
    writer = csv.writer(output, delimiter="\t", lineterminator="\n")
    writer.writerow(("Identifier", "VECS tier", "Source verification", "Species applicability",
                     "Title", "Status", "VetEvidence"))
    for row in assessment["results"]:
        status = row["error"] or ("Assessed" if row["tier"] else "No usable tier")
        writer.writerow((row["identifier"], row["tier"] or "—", row["verification"] or "—",
                         row["species_applicability"] or "—", row["title"] or "—", status, row["url"]))
    for note in assessment["notes"]:
        print(note, file=errors)
    return int(any(row["error"] for row in assessment["results"]))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("identifiers", metavar="ID", nargs="*", help="PMID, PMCID or DOI (or pipe one per line)")
    args = parser.parse_args(argv)
    if args.identifiers:
        ids = args.identifiers
    else:
        if sys.stdin.isatty():
            parser.error("supply identifiers as arguments or pipe a list on standard input")
        ids = [line.strip() for line in sys.stdin if line.strip()]
    try:
        validate(ids)
    except ValueError as exc:
        parser.error(str(exc))
    try:
        return report(summarize(ids, assess(ids)), sys.stdout, sys.stderr)
    except HTTPError as exc:
        retry = exc.headers.get("Retry-After")
        hint = f" Retry after {retry} seconds." if retry and retry.isdecimal() else ""
        print(f"VetEvidence returned HTTP {exc.code}.{hint}", file=sys.stderr)
    except (OSError, ValueError, HTTPException) as exc:
        print(f"Could not check this list with VetEvidence: {exc}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
