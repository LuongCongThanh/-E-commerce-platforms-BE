# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- `CONTEXT.md` at the repo root
- `docs/adr/` for architecture decisions touching the relevant area

If these files don't exist, proceed silently.

## File structure

This repo is configured as single-context:

```
/
├── CONTEXT.md
├── docs/adr/
└── src/
```

## Use the glossary's vocabulary

When naming domain concepts in issues, proposals, hypotheses, and tests, use terms defined in `CONTEXT.md`.

## Flag ADR conflicts

If output contradicts an existing ADR, surface it explicitly instead of silently overriding it.
