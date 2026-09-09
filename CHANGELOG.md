# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `vetevidence-grade` literature skill: POST a PubMed ID, DOI, PMCID, or article
  link to [VetEvidence](https://vetevidence.com) and report the live VECS tier.
  Study strength, source verification, and species applicability stay separate.
  Scoring weights are not published. `evidence-grading` is now the fallback when
  there is no identifier.
- Community and governance files: Code of Conduct, security policy, citation
  metadata, issue templates, and a pull request template.
- Schema validation for skills to enforce the SKILL-TEMPLATE format.
- Continuous integration to validate skills and the SDK on each change.
- A machine-readable skill index for programmatic discovery of the library.
- Hermes function-calling integration (`integrations/hermes/`): skill-discovery
  tools plus openFDA tools so a Hermes (or any function-calling) agent can use
  VetClaw, including when it runs in front of OpenClaw.
- `docs/clinical-review-2026.md`: an independent, literature-sourced verification
  of the clinical-accuracy corrections (PubMed citations and FDA/EMA labels).

### Changed

- Clinical values across the skills are now verified against primary literature
  and drug labels, with the sources published in `docs/clinical-review-2026.md`.
- Reliability improvements to the openFDA SDK (query handling, tests, packaging).

## [0.1.0] - 2026-03

### Added

- Initial public release of VetClaw: 51 veterinary AI skills for OpenClaw and
  compatible agent frameworks, organized into six categories — clinical, pharma,
  species, literature, safety, and databases.
- Species-first design: skills account for species differences and require or
  account for species identification before returning clinical information.
- Reference SDK clients (Python and TypeScript) for the openFDA Animal &
  Veterinary adverse-event API.
- Repository documentation: README, CONTRIBUTING guide, SKILL-TEMPLATE, and the
  MIT license.

[Unreleased]: https://github.com/openvet-projects/vetclaw/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/openvet-projects/vetclaw/releases/tag/v0.1.0
