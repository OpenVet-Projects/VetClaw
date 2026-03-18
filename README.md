# VetClaw

**The first veterinary AI skill library for OpenClaw and compatible agent frameworks.**

[![Skills](https://img.shields.io/badge/skills-51-blue?style=flat-square)](/skills)
[![Clinical](https://img.shields.io/badge/%F0%9F%A9%BA_clinical-17-brightgreen?style=flat-square)](/skills/clinical)
[![Pharma](https://img.shields.io/badge/%F0%9F%92%8A_pharma-8-blueviolet?style=flat-square)](/skills/pharma)
[![Species](https://img.shields.io/badge/%F0%9F%90%BE_species-10-orange?style=flat-square)](/skills/species)
[![Literature](https://img.shields.io/badge/%F0%9F%93%9A_literature-7-purple?style=flat-square)](/skills/literature)
[![Safety](https://img.shields.io/badge/%F0%9F%9B%A1_safety-5-red?style=flat-square)](/skills/safety)
[![Databases](https://img.shields.io/badge/%F0%9F%97%84_databases-4-cyan?style=flat-square)](/skills/databases)
[![License](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)](/LICENSE)

**English**

> **Note**
> VetClaw is a skill library, not a monolithic application. Install the full collection or copy only the skill folders relevant to your veterinary workflows.

---

## Why VetClaw Exists

There are 869+ medical AI skills for human medicine. There are zero for veterinary medicine.

Veterinary AI is not a subset of human AI. Drug safety varies by species. A dose that saves a dog can kill a cat. Breed predispositions change differential diagnosis rankings. Evidence hierarchies differ (textbooks remain the gold standard; PubMed coverage is sparse for many species). Regulatory frameworks are distinct (FDA CVM, not FDA CDER).

VetClaw encodes this domain knowledge into structured, reusable skills that any OpenClaw-compatible agent can load immediately.

Built by [OpenVet.ai](https://openvet.ai) -- the AI hospital for every animal on earth.

---

## Important Medical & Legal Disclaimer

VetClaw skills are AI reasoning templates only. They are **not** a substitute for professional veterinary diagnosis, treatment, or clinical decision-making. All outputs must be reviewed and approved by a licensed veterinarian. The authors and OpenVet.ai assume no liability for any clinical use. In oncology or experimental cases, always work under veterinary supervision and comply with local regulations. Always contact your veterinarian or a poison control center (ASPCA 888-426-4435 / Pet Poison Helpline 855-764-7661) in emergencies.

---

## At a Glance

| Domain | Skills | Focus |
| --- | --- | --- |
| [Clinical](/skills/clinical) | **17** | Differential diagnosis, emergency triage, clinical guidelines, exam workflows, cardiology, dermatology, ophthalmology, orthopedics, pain, nutrition, dental, anesthesia, wound management, fluid therapy, personalized oncology |
| [Pharma](/skills/pharma) | **8** | Drug lookup, FDA Green Book, drug interactions, adverse event reporting, withdrawal times, compounding, precision medicine/mRNA design, neoantigen vaccine design |
| [Species](/skills/species) | **10** | Breed predisposition, species-aware reasoning, exotic/wildlife, canine, feline, equine, ruminant, avian, camelid, swine |
| [Literature](/skills/literature) | **7** | Veterinary PubMed search, evidence grading, textbook hierarchy, comparative medicine, OMIA, VBO, comparative oncology |
| [Safety](/skills/safety) | **5** | Toxicology calculator, lethal variance detection, contraindication checking, anesthesia safety, NSAID safety |
| [Databases](/skills/databases) | **4** | openFDA Animal, FARAD, OBO Foundry ontologies, NCBI Taxonomy |

## Representative Workflows

| Workflow | Example Skills |
| --- | --- |
| Emergency toxicosis | [`toxicology-calculator`](/skills/safety/toxicology-calculator/SKILL.md), [`emergency-triage`](/skills/clinical/emergency-triage/SKILL.md) |
| Drug safety check | [`veterinary-drug-lookup`](/skills/pharma/veterinary-drug-lookup/SKILL.md), [`lethal-variance-detection`](/skills/safety/lethal-variance-detection/SKILL.md) |
| Breed-aware diagnosis | [`breed-predisposition`](/skills/species/breed-predisposition/SKILL.md), [`differential-diagnosis`](/skills/clinical/differential-diagnosis/SKILL.md) |
| Literature review | [`veterinary-pubmed-search`](/skills/literature/veterinary-pubmed-search/SKILL.md), [`evidence-grading`](/skills/literature/evidence-grading/SKILL.md) |
| Exotic species case | [`exotic-wildlife-medicine`](/skills/species/exotic-wildlife-medicine/SKILL.md), [`species-aware-reasoning`](/skills/species/species-aware-reasoning/SKILL.md) |

## Tested Workflows

Try these prompts in an OpenClaw session after installing VetClaw skills:

**Toxicology triage:**
> "My 10kg dog ate 100g of dark chocolate 2 hours ago. What's the toxicity risk and what do I do?"
>
> Expected: Agent loads `toxicology-calculator` + `emergency-triage`, calculates theobromine dose (~160 mg/kg), flags as potentially severe, and recommends immediate veterinary attention with decontamination protocol.

**Breed-aware cardiology:**
> "7-year-old Cavalier King Charles Spaniel with a Grade IV murmur. Workup?"
>
> Expected: Agent loads `breed-predisposition` + `cardiology-workup`, flags CKCS MMVD predisposition, applies murmur grading and ACVIM staging criteria, recommends echocardiography to assess B1 vs B2.

**Cross-species drug safety:**
> "Can I give acetaminophen to my cat for pain?"
>
> Expected: Agent loads `lethal-variance-detection` + `contraindication-checker`, immediately flags acetaminophen as **lethal in cats** (toxic methemoglobinemia), recommends species-safe alternatives.

## Quick Start

OpenClaw loads workspace skills from `<workspace>/skills`. Setup:

```
git clone https://github.com/OpenVet-Projects/VetClaw.git
mkdir -p ~/.openclaw/workspace/skills
cp -R VetClaw/skills/* ~/.openclaw/workspace/skills/
```

Start a new OpenClaw session so skill folders are picked up. If you already keep your workspace in git, merge only the folders you want.

## Repository Layout

```
VetClaw/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
└── skills/
    ├── clinical/       # 17 skills: diagnosis, triage, guidelines, exams, specialty workups, personalized oncology
    ├── pharma/         # 8 skills: drug lookup, FDA Green Book, interactions, adverse events, withdrawal, compounding, mRNA design, neoantigen vaccine
    ├── species/        # 10 skills: breed predisposition, species reasoning, canine, feline, equine, ruminant, avian, exotic, camelid, swine
    ├── literature/     # 7 skills: PubMed search, evidence grading, textbook hierarchy, comparative medicine, OMIA, VBO, comparative oncology
    ├── safety/         # 5 skills: toxicology, lethal variance, contraindications, anesthesia safety, NSAID safety
    └── databases/      # 4 skills: openFDA, FARAD, OBO Foundry, NCBI Taxonomy
```

## Design Principles

**Species-first.** Every skill assumes the species matters. Drug skills require species before returning results. Diagnostic skills weight differentials by species and breed. This is the foundational difference from human medical AI skills.

**Evidence hierarchy matches veterinary reality.** In human medicine, PubMed systematic reviews sit at the top. In veterinary medicine, board-certified specialist textbooks (Ettinger's, Plumb's, Nelson & Couto) remain the gold standard for most clinical decisions. These skills encode that hierarchy.

**Safety is not optional.** Veterinary medicine has extreme species-dependent drug safety variance. Acetaminophen is routine in dogs, lethal in cats. Ivermectin is safe in most breeds, neurotoxic in MDR1-mutant collies. Skills in the safety category enforce species disambiguation before any drug information is returned.

**Public data, structured reasoning.** VetClaw skills reference publicly available databases and knowledge (FDA Green Book, OMIA, VBO, PubMed, openFDA). The value is in the structured veterinary reasoning patterns, not proprietary data.

## Real-World Breakthrough: The Rosie mRNA Cancer Vaccine Story

In March 2026, Australian tech entrepreneur **Paul Conyngham** (17 years in machine learning) saved his rescue dog **Rosie** from aggressive mast cell cancer using AI.

Rosie was given months to live. Paul:

- Paid for professional tumor + normal DNA sequencing at UNSW
- Used **ChatGPT** to brainstorm strategy and build analysis pipelines
- Leveraged **AlphaFold** to model neoantigens and protein structures
- Used **Grok** (and Gemini) to refine the final vaccine construct
- Collaborated with nanomedicine pioneer Prof. Thordarson at UNSW's RNA Institute

Result: A fully personalized mRNA cancer vaccine manufactured in under 2 months. Dramatic tumor shrinkage (50-75%) and Rosie back to normal life. First-ever bespoke mRNA cancer vaccine for a dog.

**This is exactly the future VetClaw was built for.**

VetClaw skills provide the veterinary-specific reasoning patterns that generic LLMs lack: species-aware safety checks, evidence hierarchy enforcement, toxicology and lethal-variance guardrails, breed predisposition and differential diagnosis structuring. Combined with OpenClaw agents and tools like ChatGPT, AlphaFold, or Grok, users can now run safe, structured workflows for personalized oncology, neoantigen identification, mRNA vaccine blueprinting, and genomics-driven therapies.

OpenVet.ai's full platform takes this further, orchestrating these skills into multi-agent clinical rooms with transparent citations and specialist oversight.

We are actively expanding the **Deep Science** category with oncology and personalized-medicine skills so every veterinarian can access this level of breakthrough safely.

## Skill Format

Every `SKILL.md` follows the AgentSkills-compatible structure:

```yaml
---
name: skill-name
description: One-line description used for agent skill matching.
---
```

```markdown
# Skill Name
## Overview        -- what this skill enables
## When to Use     -- trigger conditions for the AI agent
## Key Capabilities -- specific tools, APIs, databases
## Workflow         -- step-by-step reasoning pattern
## Output Format   -- what the agent should produce
## Limitations     -- what this skill cannot do
```

## Related Projects

| Repository | Relationship |
| --- | --- |
| [OpenClaw](https://github.com/openclaw/openclaw) | The agent runtime VetClaw skills are designed for. |
| [LabClaw](https://github.com/wu-yc/LabClaw) | Stanford/Princeton biomedical research skills. VetClaw complements LabClaw for veterinary-specific use cases. |
| [OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) | 869 human medicine skills. VetClaw fills the veterinary gap. |
| [ClawBio](https://github.com/ClawBio/ClawBio) | Bioinformatics agent skills. Relevant for veterinary genomics workflows. |

## About OpenVet

[OpenVet.ai](https://openvet.ai) is building the AI hospital for every animal on earth. VetClaw represents our commitment to open veterinary AI infrastructure. For the full clinical platform with specialist rooms, cited evidence, and species-specific decision support, visit [openvet.ai](https://openvet.ai).

## Contributing

We welcome contributions from veterinary professionals, researchers, and developers. If you work with animal health data, veterinary diagnostics, or species-specific medicine, we want your expertise encoded as skills. See [CONTRIBUTING.md](/CONTRIBUTING.md) for guidelines.

## License

[MIT License](/LICENSE)

## Credits

Skills developed by the OpenVet.ai team. Veterinary domain expertise provided by board-certified veterinary specialists.
