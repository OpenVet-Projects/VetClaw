# Animal Meridian

*An open field guide to veterinary evidence*

by [OpenVet](https://openvet.ai)

A dog study turns up in a search about rabbits. What did the paper establish, and what would it take to apply that finding to another species? Animal Meridian brings together literature workflows, public data clients, and species-specific review cases for questions like this.

## Check a reference list

Paste up to 15 PMIDs, PMCIDs, or DOIs into [VetEvidence’s reference-list checker](https://vetevidence.com/#batch). Each result describes one source and links evidence strength to the material the service could verify.

You can also check a journal club reading list from a checkout with Python 3:

```sh
python3 scripts/check_references.py 5061884 10.1111/jvim.15488
python3 scripts/check_references.py < references.txt > assessments.tsv
```

Use one bare identifier per line in the file. The table includes each source’s VECS tier, verification status, species note, and a link to its assessment. A failed lookup stays in its original row. If any citation fails or receives no result, the command exits with status 1. A dash marks a missing value.

## Explore a workflow

| I want to… | Start here |
| --- | --- |
| Find veterinary studies on a question | [Veterinary PubMed search](skills/literature/veterinary-pubmed-search/SKILL.md) |
| Judge how well sources support a clinical claim | [Evidence grading](skills/literature/evidence-grading/SKILL.md) |
| Examine evidence from another species | [Comparative medicine search](skills/literature/comparative-medicine-search/SKILL.md) |
| Explore animal adverse-event reports | [Python and TypeScript clients for openFDA](sdk/README.md) |
| Evaluate how an assistant handles a species-specific question | [Community review cases](evals/README.md) |

Browse the [skill folders](skills) or use the [machine-readable catalog](index.json) to find a workflow by category. Each skill is a Markdown file that can be read on its own.

## Agent integrations

The [Hermes adapter](integrations/hermes/README.md) lets a function-calling agent discover a workflow, load its text, and check citations with VetEvidence. The earlier VetClaw tool names remain available for existing callers.

For OpenClaw, copy the individual skill folders you want into your workspace. For example, from this checkout:

```sh
mkdir -p ~/.openclaw/workspace/skills
cp -R skills/literature/veterinary-pubmed-search ~/.openclaw/workspace/skills/
```

Start a new session to load the skill.

## Clinical review and contributions

Use the [cited clinical review](docs/clinical-review-2026.md) to see which values have been checked and which labels or papers support them. The catalog’s optional `review_record` field links individual skills to that documentation. Clinical decisions require a licensed veterinarian’s assessment of the individual animal. Seek veterinary care directly for a suspected poisoning or other emergency.

Clinicians can [submit a correction or review case](CONTRIBUTING.md). Developers can use the [skill template](SKILL-TEMPLATE.md), validate the catalog with `python3 scripts/validate_skills.py`, and check generated files with `python3 scripts/generate_index.py --check`.

Animal Meridian was previously published as VetClaw. The project is available under the [MIT license](LICENSE). Citation details are in [CITATION.cff](CITATION.cff).
