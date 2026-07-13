# Security Policy

VetClaw is an open-source veterinary AI skill library. This policy covers
**technical security issues** in the repository and its reference SDK. Thank you
for helping keep the project and its users safe.

## What this policy is NOT for

- **Clinical or medical-accuracy issues** (a wrong dose, value, range, or
  clinical claim) are not security issues. Please report those with the
  **Clinical Correction** issue template so a reviewer can verify and fix them.
- **Medical emergencies.** If an animal is sick or may have been poisoned,
  contact a veterinarian or a poison control center immediately
  (ASPCA 888-426-4435 / Pet Poison Helpline 855-764-7661). Do not use this
  process for emergencies.

## Reporting a vulnerability

Please report security vulnerabilities **privately**. Do not open a public
GitHub issue, pull request, or discussion for a suspected vulnerability, because
that discloses it before a fix is available.

To report:

- Preferred: use GitHub's **private vulnerability reporting** ("Report a
  vulnerability" under the repository's **Security** tab), if enabled.
- Otherwise, contact the maintainers via [OpenVet.ai](https://openvet.ai).

<!-- MAINTAINERS: set a real, monitored security contact before publishing (for
example, a security@openvet.ai address or an enabled GitHub Security Advisory /
private vulnerability reporting channel), and reference it here. -->

Please include, where possible:

- A description of the issue and its potential impact.
- Steps to reproduce or a proof of concept.
- Affected component and version/commit (e.g. `sdk/python`, `sdk/typescript`).
- Any suggested remediation.

We aim to acknowledge reports promptly, keep you informed of progress, and
credit reporters who wish to be credited once a fix is released. Please act in
good faith and give us a reasonable opportunity to remediate before any public
disclosure.

## Supported versions

VetClaw is in early development (0.x). Security fixes are applied to the latest
version on the default branch. Please verify an issue against the current `main`
before reporting.

## API keys and secrets

The reference SDK can query the openFDA Animal & Veterinary API using an
**openFDA API key**. Keep the following in mind:

- **Never commit API keys or other secrets.** Do not hard-code a key into
  source, tests, notebooks, or example snippets.
- Provide keys at runtime instead — for example via an environment variable or a
  local `.env` file. The repository's `.gitignore` already excludes `.env`, so
  keep real keys there and out of version control.
- openFDA keys are free and low-privilege (they raise rate limits and do not
  grant access to private data), but treat any leaked key as compromised:
  rotate it via <https://open.fda.gov/apis/authentication/> and remove it from
  history.
- If you find a committed secret in this repository, please report it privately
  using the process above rather than opening a public issue.
