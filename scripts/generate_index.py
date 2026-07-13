#!/usr/bin/env python3
"""Generate ``index.json`` — a machine-readable manifest of all VetClaw skills.

An agent runtime (or an installer) can read this file to enumerate skills,
filter by category, and resolve paths without walking the tree or parsing README.

Usage:
  python3 scripts/generate_index.py           # write index.json
  python3 scripts/generate_index.py --check    # exit 1 if index.json is stale (CI)
"""
from __future__ import annotations

import json
import sys

from skilllib import REPO_ROOT, iter_skills

INDEX_PATH = REPO_ROOT / "index.json"


def build_index():
    skills = []
    for path, category, fm, _body in iter_skills():
        skills.append(
            {
                "name": fm.get("name", path.parent.name),
                "category": category,
                "description": fm.get("description", ""),
                "path": str(path.relative_to(REPO_ROOT)),
            }
        )
    skills.sort(key=lambda s: (s["category"], s["name"]))

    categories = {}
    for s in skills:
        categories[s["category"]] = categories.get(s["category"], 0) + 1

    return {
        "name": "VetClaw",
        "version": "0.1.0",
        "description": "Veterinary AI skill library for OpenClaw and compatible agent frameworks.",
        "license": "MIT",
        "skill_count": len(skills),
        "categories": dict(sorted(categories.items())),
        "skills": skills,
    }


def main():
    index = build_index()
    text = json.dumps(index, indent=2, ensure_ascii=False) + "\n"

    if "--check" in sys.argv:
        current = INDEX_PATH.read_text(encoding="utf-8") if INDEX_PATH.exists() else ""
        if current != text:
            print("index.json is out of date. Run: python3 scripts/generate_index.py")
            return 1
        print(f"index.json is up to date ({index['skill_count']} skills).")
        return 0

    INDEX_PATH.write_text(text, encoding="utf-8")
    print(f"Wrote {INDEX_PATH.relative_to(REPO_ROOT)} ({index['skill_count']} skills).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
