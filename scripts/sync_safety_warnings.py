"""Keep reviewed warnings in the standalone demo consistent with the cited matrix."""
import argparse
import html
import re

from skilllib import REPO_ROOT

MATRIX = REPO_ROOT / "assets/species-drug-safety-matrix.md"
DEMO = REPO_ROOT / "demo/safety-checker.html"


def render(matrix, demo):
    rows = [line.strip("|").split("|") for line in matrix.splitlines() if line.startswith("|")]
    species = [cell.strip().lower() for cell in rows[0]]
    records = {row[0].strip().strip("*"): row for row in rows[2:]}

    def warning(match):
        row = records[match["substance"]]
        text = row[species.index(match["species"])].strip()
        # Reviewed cells use a bold clinical headline followed by its context.
        headline, detail = re.fullmatch(r"\*\*(.+?)\*\* (.+)", text).groups()
        return f'{match["start"]}<strong>{html.escape(headline)}</strong> {html.escape(detail)}</td>'

    return re.sub(r'(?P<start><td class="cell-caution" data-substance="(?P<substance>[^"]+)" '
                  r'data-species="(?P<species>[^"]+)">).*?</td>', warning, demo)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    opts = parser.parse_args()
    current = DEMO.read_text(encoding="utf-8")
    updated = render(MATRIX.read_text(encoding="utf-8"), current)
    if opts.check and current != updated:
        raise SystemExit("Safety demo is stale. Run python3 scripts/sync_safety_warnings.py")
    if not opts.check:
        DEMO.write_text(updated, encoding="utf-8")
