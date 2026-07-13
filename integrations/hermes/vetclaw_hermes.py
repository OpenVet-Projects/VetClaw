"""VetClaw ⇄ Hermes function-calling adapter.

Hermes-family models (NousResearch Hermes 2 Pro / Hermes 3) call tools using a
ChatML system prompt that lists tool schemas inside ``<tools></tools>`` and emit
calls inside ``<tool_call></tool_call>``. Unlike OpenClaw — which auto-loads
``<workspace>/skills`` — a Hermes agent has no built-in way to see VetClaw. This
adapter bridges that gap by exposing VetClaw as ordinary function-calling tools:

  * ``list_vetclaw_skills``  — discover skills (from index.json)
  * ``get_vetclaw_skill``    — pull a skill's full SKILL.md into context on demand
  * ``search_veterinary_adverse_events`` / ``top_adverse_reactions`` — openFDA SDK

Typical flow for a Hermes agent running "in front of" OpenClaw:
  1. Build the system prompt with ``build_system_prompt()`` (embeds the tool list).
  2. Send the user turn; the model replies with one or more ``<tool_call>`` blocks.
  3. ``parse_tool_calls()`` extracts them; ``dispatch()`` runs each.
  4. Feed each result back with ``format_tool_response()`` and continue.

Stdlib-only for skill discovery. The openFDA tools lazily import the Python SDK
(``sdk/python/openfda_vet.py``) and need ``requests`` + network (API key optional
via the ``OPENFDA_API_KEY`` env var).

Run ``python3 integrations/hermes/vetclaw_hermes.py`` for an offline demo.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = REPO_ROOT / "index.json"
SDK_PATH = REPO_ROOT / "sdk" / "python"

# The canonical Hermes function-calling system prompt. ``{tools}`` is replaced
# with a newline-separated list of the tool JSON schemas.
HERMES_SYSTEM_PROMPT = (
    "You are a veterinary function calling AI model. You are provided with function "
    "signatures within <tools></tools> XML tags. You may call one or more functions "
    "to assist with the user query. VetClaw is species-first: confirm the species "
    "before giving drug or dose information, and load the relevant skill with "
    "get_vetclaw_skill before reasoning about a case. Don't make assumptions about "
    "what values to plug into functions. Here are the available tools: <tools> "
    "{tools} </tools> Use the following pydantic model json schema for each tool "
    'call you will make: {"properties": {"name": {"title": "Name", "type": '
    '"string"}, "arguments": {"title": "Arguments", "type": "object"}}, "required": '
    '["name", "arguments"], "title": "FunctionCall", "type": "object"} For each '
    "function call return a json object with function name and arguments within "
    "<tool_call></tool_call> XML tags as follows:\n"
    "<tool_call>\n"
    '{"name": <function-name>, "arguments": <args-dict>}\n'
    "</tool_call>"
)


def _load_index():
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def tool_schemas():
    """Return the VetClaw tool schemas in OpenAI/Hermes function format."""
    index = _load_index()
    categories = sorted(index.get("categories", {}).keys())
    return [
        {
            "type": "function",
            "function": {
                "name": "list_vetclaw_skills",
                "description": (
                    "List available VetClaw veterinary skills (name, category, "
                    "description). Call first to discover which skill to load."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "enum": categories,
                            "description": "Optional category filter.",
                        },
                        "query": {
                            "type": "string",
                            "description": "Optional case-insensitive substring matched against name/description.",
                        },
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_vetclaw_skill",
                "description": (
                    "Return the full markdown of a VetClaw skill by name (e.g. "
                    "'toxicology-calculator'). Load the relevant skill before "
                    "reasoning about a veterinary case."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Skill name (kebab-case) from list_vetclaw_skills.",
                        }
                    },
                    "required": ["name"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_veterinary_adverse_events",
                "description": (
                    "Search the FDA openFDA animal & veterinary adverse-event "
                    "database. Filter by species, drug, breed, and/or reaction."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "species": {"type": "string", "description": "e.g. DOG, CAT, HORSE, CATTLE, BIRD"},
                        "drug": {"type": "string"},
                        "reaction": {"type": "string"},
                        "breed": {"type": "string"},
                        "limit": {"type": "integer", "description": "Max results (default 10)."},
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "top_adverse_reactions",
                "description": "Count the most-reported adverse reactions for a species (optionally a drug).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "species": {"type": "string", "description": "e.g. DOG, CAT, HORSE"},
                        "drug": {"type": "string"},
                    },
                    "required": ["species"],
                },
            },
        },
    ]


def build_system_prompt(extra_tools=None):
    """Return the Hermes system prompt with VetClaw (and any extra) tools embedded."""
    tools = tool_schemas() + list(extra_tools or [])
    tools_json = "\n".join(json.dumps(t) for t in tools)
    # plain replace, not str.format: the template embeds literal { } (the pydantic schema)
    return HERMES_SYSTEM_PROMPT.replace("{tools}", tools_json)


# --- Tool implementations -------------------------------------------------

def _tool_list_vetclaw_skills(category=None, query=None):
    skills = _load_index()["skills"]
    if category:
        skills = [s for s in skills if s["category"] == category]
    if query:
        q = query.lower()
        skills = [s for s in skills if q in s["name"].lower() or q in s["description"].lower()]
    return [{"name": s["name"], "category": s["category"], "description": s["description"]} for s in skills]


def _tool_get_vetclaw_skill(name):
    for s in _load_index()["skills"]:
        if s["name"] == name:
            content = (REPO_ROOT / s["path"]).read_text(encoding="utf-8")
            return {"name": name, "path": s["path"], "content": content}
    return {"error": f"unknown skill '{name}'. Call list_vetclaw_skills to see valid names."}


def _openfda_client():
    if str(SDK_PATH) not in sys.path:
        sys.path.insert(0, str(SDK_PATH))
    from openfda_vet import OpenFDAVet  # lazy: needs `requests`

    return OpenFDAVet(api_key=os.environ.get("OPENFDA_API_KEY"))


def _tool_search_veterinary_adverse_events(species=None, drug=None, reaction=None, breed=None, limit=10):
    try:
        client = _openfda_client()
        return client.search(species=species, drug=drug, reaction=reaction, breed=breed, limit=limit)
    except ImportError:
        return {"error": "openFDA SDK needs `pip install requests` (see sdk/python)."}
    except Exception as exc:  # network / API errors surfaced to the agent
        return {"error": f"openFDA request failed: {exc}"}


def _tool_top_adverse_reactions(species, drug=None):
    try:
        client = _openfda_client()
        return client.top_reactions(species, drug=drug)
    except ImportError:
        return {"error": "openFDA SDK needs `pip install requests` (see sdk/python)."}
    except Exception as exc:
        return {"error": f"openFDA request failed: {exc}"}


DISPATCH = {
    "list_vetclaw_skills": _tool_list_vetclaw_skills,
    "get_vetclaw_skill": _tool_get_vetclaw_skill,
    "search_veterinary_adverse_events": _tool_search_veterinary_adverse_events,
    "top_adverse_reactions": _tool_top_adverse_reactions,
}

_TOOL_CALL_RE = re.compile(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", re.DOTALL)


def parse_tool_calls(text):
    """Extract ``[{'name': ..., 'arguments': {...}}, ...]`` from a model reply."""
    calls = []
    for match in _TOOL_CALL_RE.finditer(text):
        try:
            calls.append(json.loads(match.group(1)))
        except json.JSONDecodeError:
            continue
    return calls


def dispatch(name, arguments):
    """Run one tool call and return its raw result (dict/list)."""
    fn = DISPATCH.get(name)
    if fn is None:
        return {"error": f"unknown tool '{name}'"}
    try:
        return fn(**(arguments or {}))
    except TypeError as exc:
        return {"error": f"bad arguments for {name}: {exc}"}


def format_tool_response(name, content):
    """Wrap a tool result in the Hermes ``<tool_response>`` envelope."""
    payload = {"name": name, "content": content}
    return "<tool_response>\n" + json.dumps(payload, ensure_ascii=False) + "\n</tool_response>"


def _demo():
    print("=== Hermes system prompt (truncated) ===")
    print(build_system_prompt()[:600], "...\n")
    sample = (
        'Sure, let me look that up.\n'
        '<tool_call>\n{"name": "list_vetclaw_skills", "arguments": {"query": "toxic"}}\n</tool_call>'
    )
    for call in parse_tool_calls(sample):
        result = dispatch(call["name"], call.get("arguments"))
        print(f"=== dispatch {call['name']}({call.get('arguments')}) ===")
        print(format_tool_response(call["name"], result)[:500])


if __name__ == "__main__":
    _demo()
