# VetClaw + Hermes

Use VetClaw skills with a [NousResearch Hermes](https://huggingface.co/NousResearch)
function-calling agent (Hermes 2 Pro / Hermes 3), including agents that run **in
front of** OpenClaw.

## Why this exists

OpenClaw auto-loads every skill in `<workspace>/skills`. A Hermes agent has no
such mechanism — it discovers capabilities through **function calling**. So the way
to give a Hermes agent VetClaw is to expose the library as tools it can call:

| Tool | What it does |
| --- | --- |
| `list_vetclaw_skills(category?, query?)` | Discover skills (from [`index.json`](../../index.json)) |
| `get_vetclaw_skill(name)` | Pull a skill's full `SKILL.md` into context on demand |
| `search_veterinary_adverse_events(...)` | Query the openFDA animal/vet adverse-event DB |
| `top_adverse_reactions(species, drug?)` | Aggregate top reactions |

The tool schemas (OpenAI/Hermes function format) are generated to
[`tools.json`](tools.json); the reference dispatcher is
[`vetclaw_hermes.py`](vetclaw_hermes.py).

## Three ways to integrate (simplest → most capable)

### 1. Static injection
If you already know which skills a case needs, concatenate those `SKILL.md` files
into the Hermes agent's system prompt. Zero code; best when your agent is narrow.

### 2. Manifest + on-demand retrieval
Put the skill list (name + description from `index.json`) in the system prompt so
the model knows what exists, then let it call `get_vetclaw_skill(name)` to pull the
one it needs. Keeps the context small while covering all 52 skills.

### 3. Full function-calling (recommended)
Register all four tools and run the standard Hermes tool loop. The model discovers,
loads, and applies skills itself, and can hit openFDA for live data.

## Quickstart (pattern 3)

`vetclaw_hermes.py` is stdlib-only for skill discovery (the openFDA tools lazily
import the Python SDK and need `requests` + an optional `OPENFDA_API_KEY`).

```python
from vetclaw_hermes import build_system_prompt, parse_tool_calls, dispatch, format_tool_response

# 1. Build the Hermes system prompt (embeds the <tools> block)
system = build_system_prompt()

# 2. Send to your Hermes endpoint (any OpenAI-compatible server: vLLM, Ollama, TGI…)
#    messages = [{"role": "system", "content": system}, {"role": "user", "content": question}]
#    reply = call_your_hermes_model(messages)

# 3. Run any tool calls the model emitted, feed results back, and continue
for call in parse_tool_calls(reply):
    result = dispatch(call["name"], call.get("arguments"))
    tool_msg = format_tool_response(call["name"], result)   # <tool_response>…</tool_response>
    # append tool_msg as the next turn, then call the model again
```

Run the offline demo (no model or network needed):

```
python3 integrations/hermes/vetclaw_hermes.py
```

### Serving Hermes with a native tool parser
Most OpenAI-compatible servers can parse Hermes tool calls for you, so you can pass
`tools.json` as the `tools` argument instead of hand-building the prompt:

- **vLLM:** `--enable-auto-tool-choice --tool-call-parser hermes`
- **Ollama / llama.cpp:** use a Hermes model with a tool-enabled chat template and
  pass the tools through the `/api/chat` or OpenAI-compatible `tools` field.

Either way, `dispatch()` and `format_tool_response()` remain your execution layer.

## Hermes in front of OpenClaw

If your Hermes agent triages before handing off to OpenClaw, you get two clean
options — and they compose:

- **Hermes pulls skills directly** via these tools (good for quick, single-skill
  answers — toxicity checks, dose lookups).
- **Hermes hands off to OpenClaw**, which auto-loads the same `skills/` for deeper,
  multi-step workflows.

Because both read the *same* `SKILL.md` files, the veterinary reasoning is identical
on either side of the hand-off.

## Keeping tools in sync

`tools.json` is generated from `index.json` (the category enum tracks the skills):

```
python3 scripts/generate_hermes_tools.py           # regenerate
python3 scripts/generate_hermes_tools.py --check     # CI freshness check
```

## Note on models

The Hermes function-calling format is what this integration targets. The same
tools work with any function-calling-capable open model served through an
OpenAI-compatible endpoint; Hermes is simply the one with a matching native
tool-call parser. Nothing here requires a proprietary model.
