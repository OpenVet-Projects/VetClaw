#!/usr/bin/env python3
"""Generate ``integrations/hermes/tools.json`` — the VetClaw tool schemas in
OpenAI/Hermes function-calling format, ready to drop into a Hermes agent's
``<tools>`` block. Regenerated from index.json so the category enum stays in sync.

Usage:
  python3 scripts/generate_hermes_tools.py           # write tools.json
  python3 scripts/generate_hermes_tools.py --check     # exit 1 if stale (CI)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_PATH = REPO_ROOT / "integrations" / "hermes" / "tools.json"

sys.path.insert(0, str(REPO_ROOT / "integrations" / "hermes"))
from vetclaw_hermes import tool_schemas  # noqa: E402  (path injected above)


def main():
    text = json.dumps(tool_schemas(), indent=2, ensure_ascii=False) + "\n"

    if "--check" in sys.argv:
        current = TOOLS_PATH.read_text(encoding="utf-8") if TOOLS_PATH.exists() else ""
        if current != text:
            print("integrations/hermes/tools.json is out of date. Run: python3 scripts/generate_hermes_tools.py")
            return 1
        print("integrations/hermes/tools.json is up to date.")
        return 0

    TOOLS_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOOLS_PATH.write_text(text, encoding="utf-8")
    print(f"Wrote {TOOLS_PATH.relative_to(REPO_ROOT)} ({len(tool_schemas())} tools).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
