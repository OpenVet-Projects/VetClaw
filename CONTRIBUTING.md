# Contributing to VetClaw

We welcome contributions from veterinary professionals, researchers, and developers.

## What We Need

- **New skills** for underserved areas: avian medicine, large animal/production, zoo/wildlife, veterinary dentistry, rehabilitation, nutrition
- **Species-specific adaptations** of existing skills (equine versions, feline-specific versions)
- **Regional adaptations** (UK/EU formulary differences, international guidelines)
- **Accuracy corrections** from practicing veterinarians and board-certified specialists
- **Evidence updates** when new guidelines or consensus statements are published

## Skill Format

Every skill must follow the AgentSkills-compatible format:

```
skills/
  [category]/
    [skill-name]/
      SKILL.md
```

The SKILL.md file must include:
1. YAML frontmatter with `name` and `description`
2. Sections: Overview, When to Use, Workflow, Limitations (at minimum)
3. Species-awareness (skills must account for species differences)
4. Source references (cite textbooks, guidelines, or databases)

## Quality Standards

- **Accuracy over speed.** Every clinical claim must be supportable by a citable veterinary reference.
- **Species-first.** Every skill must require or account for species identification.
- **Safety-first.** When in doubt, recommend the more conservative approach.
- **No hallucination.** If data is limited, say so. Do not fabricate dosing information, prevalence statistics, or clinical recommendations.

## Submission Process

1. Fork the repository
2. Create a new branch for your skill
3. Write the SKILL.md following the format above
4. Submit a pull request with:
   - Description of the skill
   - Your qualifications (veterinary degree, specialty, etc.)
   - References supporting the skill content

## Code of Conduct

Clinical accuracy is paramount. Submissions will be reviewed for veterinary accuracy before merging. We may request revisions or ask for additional references.

## Questions?

Open an issue or reach out to the OpenVet team at openvet.ai.
