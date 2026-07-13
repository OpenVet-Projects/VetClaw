"""Shared helpers for VetClaw skill tooling (dependency-free, stdlib only).

Used by validate_skills.py and generate_index.py. Deliberately avoids PyYAML so
the tooling runs anywhere with a bare Python 3 interpreter.
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"


def parse_frontmatter(text):
    """Parse a minimal YAML frontmatter block (``--- ... ---``) into a dict.

    Only supports simple ``key: value`` scalars, which is all a SKILL.md needs.
    Returns ``(frontmatter_dict, body_str)``; frontmatter is ``{}`` if absent.
    """
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    fm = {}
    for line in lines[1:end]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip()
    body = "\n".join(lines[end + 1:])
    return fm, body


def iter_skills():
    """Yield ``(path, category, frontmatter, body)`` for each ``skills/*/*/SKILL.md``."""
    for skill_file in sorted(SKILLS_DIR.glob("*/*/SKILL.md")):
        category = skill_file.parent.parent.name
        text = skill_file.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        yield skill_file, category, fm, body
