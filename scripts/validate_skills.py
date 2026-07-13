#!/usr/bin/env python3
"""Validate every VetClaw SKILL.md against the frontmatter + structure rules.

Errors (exit 1):
  - missing YAML frontmatter
  - frontmatter `name` missing or != containing folder name
  - `description` missing or shorter than 20 chars
  - missing `## Overview` or `## Limitations` section

Warnings (exit 0):
  - overly long description (some runtimes truncate)
  - no "When to Use" section
  - no workflow-style section (content may live under an alternate heading such
    as "Diagnostic Ladder" or "The Pipeline" — accepted, but flagged)

Run:  python3 scripts/validate_skills.py
"""
from __future__ import annotations

import re
import sys

from skilllib import REPO_ROOT, iter_skills

WORKFLOW_HEADING_RE = re.compile(
    r"^##\s+.*\b(workflow|approach|ladder|pipeline|protocol|steps?|process|"
    r"selection|assessment|staging|calculation|framework|algorithm|diagnostic|"
    r"interpretation|tiers?)\b",
    re.IGNORECASE | re.MULTILINE,
)
WHENTOUSE_RE = re.compile(r"^##\s+When to (Use|Consult)\b", re.IGNORECASE | re.MULTILINE)


def has_heading(body, heading):
    """True if the body contains an H2 whose text starts with ``heading``."""
    return re.search(rf"^##\s+{re.escape(heading)}\b", body, re.MULTILINE | re.IGNORECASE) is not None


def main():
    errors = []
    warnings = []
    count = 0
    for path, _category, fm, body in iter_skills():
        count += 1
        rel = path.relative_to(REPO_ROOT)
        folder = path.parent.name

        if not fm:
            errors.append(f"{rel}: missing YAML frontmatter")
            continue

        name = fm.get("name", "")
        desc = fm.get("description", "")
        if not name:
            errors.append(f"{rel}: frontmatter missing `name`")
        elif name != folder:
            errors.append(f"{rel}: frontmatter name '{name}' != folder '{folder}'")

        if not desc:
            errors.append(f"{rel}: frontmatter missing `description`")
        elif len(desc) < 20:
            errors.append(f"{rel}: description too short ({len(desc)} chars)")
        elif len(desc) > 400:
            warnings.append(f"{rel}: description long ({len(desc)} chars); some runtimes truncate")

        if not has_heading(body, "Overview"):
            errors.append(f"{rel}: missing '## Overview' section")
        if not has_heading(body, "Limitations"):
            errors.append(f"{rel}: missing '## Limitations' section")

        if not WHENTOUSE_RE.search(body):
            warnings.append(f"{rel}: no 'When to Use' section (recommended)")
        if not WORKFLOW_HEADING_RE.search(body):
            warnings.append(f"{rel}: no workflow-style section found (recommended)")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\nChecked {count} skills: {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
