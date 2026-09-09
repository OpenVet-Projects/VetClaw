---
name: vetevidence-grade
description: Grade one veterinary paper through VetEvidence (VECS). POST a PubMed ID, DOI, PMCID, or article link and report study strength, source verification, and species applicability as three separate facts. Do not invent a tier.
version: "1.0.0"
last_reviewed: "2026-09-09"
sources:
  - "https://vetevidence.com"
  - "https://vetevidence.com/llms.txt"
---

# Grade a paper via VetEvidence

## Overview

Call the public VetEvidence API to place **one clinical source** (a paper, guideline, or label) on the VECS five-tier study-strength scale. VetEvidence is built by OpenVet. This skill grades the source. It does not summarize the article and it does not answer a clinical question for a patient — that is OpenVet, not this skill.

Three facts stay separate:

- **Study strength** — how much confidence this study's design and evidence can support.
- **Source verification** — whether the cited source can be found and checked.
- **Species applicability** — whether the evidence concerns the species in question.

A real citation is not necessarily strong evidence. Strong evidence in one species is not automatically an answer for another. A lower tier means earlier-stage evidence, not lower-quality work. Most veterinary literature lives in Tiers III to V.

The tier definitions and this tool are public. The scoring weights are being calibrated and are **not published**. Never ask for them, never guess them, never display numeric dimension bars as if they were the formula.

## When to Use

- The user pastes a PubMed ID, DOI, PMCID, or article URL and asks how strong that source is
- A literature search (`veterinary-pubmed-search`) returned identifiers and you need a live grade, not a guessed level
- The user wants a guideline's reference list graded (up to 15 identifiers)
- Keywords: VECS, VetEvidence, grade this paper, how strong is this study, PMID, DOI, evidence tier, study strength

Do **not** use this skill to:

- Summarize, rewrite, or "Cliff Notes" a paper
- Recommend a drug, dose, or treatment (OpenVet)
- Grade a claim that has no resolvable identifier — use `evidence-grading` for that hierarchy

## API

No API key. Send `User-Agent: VetClaw-vetevidence-grade/1.0` so traffic is identifiable.

**One source**

```
POST https://vetevidence.com/vecs/score
Content-Type: application/json
User-Agent: VetClaw-vetevidence-grade/1.0

{"pmid":"27678080"}
```

Send exactly one of: `pmid`, `doi`, `pmcid`, `url`.

**Reference list (up to 15)**

```
POST https://vetevidence.com/vecs/batch
Content-Type: application/json
User-Agent: VetClaw-vetevidence-grade/1.0

{"ids":["27678080","30974015","10.1111/jvim.15488"]}
```

Prefer a PubMed ID or the DOI itself. Some publisher landing pages block fetching; if the API says so, report that instead of guessing. Google Scholar pages cannot be fetched — copy the DOI from Scholar's Cite popup.

## Letter → Roman tier

The JSON still uses letters. The public site uses Roman numerals. Map before you speak:

| API letter | Public tier | Label |
| --- | --- | --- |
| A | Tier I | Very strong |
| B | Tier II | Strong |
| C | Tier III | Moderate |
| D | Tier IV | Preliminary |
| E | Tier V | Signal-level |

If `label` or `why` already says "Tier II", use that wording. Do not invent a sixth tier.

## Workflow

1. Extract a PubMed ID, DOI, PMCID, or article URL. If none exists, stop and use `evidence-grading`.
2. Confirm the patient's species if the user named one. You will compare it to `source.species` after the call; do not skip the call because species is missing.
3. `POST /vecs/score` (or `/vecs/batch` for a list). Do not fabricate a tier if the request fails.
4. Read only public fields: `source`, `evidence_tier` / `label`, `verifiability`, `why`, and the **Species applicability** *detail* text inside `dimension_signals` (e.g. `canine`). Ignore numeric `value` bars — they are presentation, not weights.
5. Map the letter to the Roman tier. Report the three facts separately.
6. If the user asked what to do for a patient, stop after the grade and say OpenVet answers clinical questions; this skill does not.

On HTTP 404, say the identifier was not found. On 415, say PDFs are not accepted. On 429, wait and retry once; do not invent a grade.

## Output Format

```
**Source:** [title]. [journal] ([year]). PMID [pmid] / DOI [doi]
**Study strength:** Tier [I–V] · [label]
**Source verification:** [verifiability]
**Species applicability:** [source.species or signal detail] [— matches / does not match the named patient species]
**Why:** [why, trimmed to the grade rationale — do not add a paper summary]
**Link:** https://vetevidence.com/?pmid=[pmid]   (or the DOI if that is what you sent)
```

Worked check (live API, 2026-09-08): PMID `27678080` (EPIC, *JVIM* 2016) → Tier II · Strong study evidence; verifiability `verified`; species `canine`. If a later call disagrees, report the later call.

## Limitations

- VECS grades **this source**, not the clinical question and not the patient in front of you.
- A tier is not medical advice and does not replace reading the paper. Confirm dosing, thresholds, and species rules against the primary source.
- Abstract-only sources are capped at Tier III, because an abstract advertises strengths and rarely reports flaws.
- Retracted or unverifiable sources may be excluded before a tier is issued — report that outcome, do not substitute a guessed grade.
- Scoring weights are not public. Do not reverse-engineer them from `dimension_signals` values.
- This is not OpenVet. Do not produce a treatment plan, a SOAP, or an article summary from this skill.
