# openfda-vet (TypeScript)

TypeScript client for the openFDA Animal & Veterinary Adverse Events API.
See the top-level [`sdk/README.md`](../README.md) for usage examples.

## Requirements

Node 18+ (uses the built-in global `fetch`). No runtime dependencies.

## Build / type-check

```bash
npm install       # installs the only dev dependency, TypeScript
npm run typecheck # tsc --noEmit, strict mode
npm run build     # emits dist/openfda-vet.js + .d.ts
```

## Tests

The Python SDK ships a full unit-test suite (`sdk/python/test_openfda_vet.py`)
that locks in the query-builder behaviour (spaced `" AND "` joins, `.exact`
count fields). The TypeScript client mirrors that logic exactly:

- `buildSearchQuery` joins filters with `" AND "` so `URLSearchParams` encodes
  the space to `+` (yielding `...+AND+...` on the wire) instead of double-encoding
  a literal `+AND+` into `%2BAND%2B`.
- `count()` appends `.exact` to the count field by default (pass `{ exact: false }`
  to opt out).

A runnable TS test suite is intentionally omitted here because it requires
installing a test runner/`typescript` from the network. To add one locally,
install dev deps and drive `buildSearchQuery`/`count` against a stubbed global
`fetch`, asserting the constructed URL contains `+AND+` (never `%2BAND%2B`) and
that count requests use the `.exact` field.
