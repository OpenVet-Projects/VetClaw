# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Community and governance files: Code of Conduct, security policy, citation
  metadata, issue templates, and a pull request template.
- Schema validation for skills to enforce the SKILL-TEMPLATE format.
- Continuous integration to validate skills and the SDK on each change.
- A machine-readable skill index for programmatic discovery of the library.

### Fixed

- Ongoing corrections to critical clinical-accuracy and SDK issues identified
  after the initial release. Specific clinical values are corrected in their
  respective skills and reviewed against citable veterinary references.

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
