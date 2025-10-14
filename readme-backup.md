# Prompt Rules Monorepo

A modular, profile-driven repository for **AI coding rules** across a polyglot stack (Go, Python, Java/Maven, Shell, Make, Helm, JSON, gRPC).
It ships with:
- **core/**: stable workspace contract
- **adapters/**: per-language Cursor rules
- **profiles/**: overlays for org/project/editor
- **scripts/**: deterministic build + validation
- **examples/**: built outputs for sanity
- **docs/**: human-readable bootstraps (Cursor prompts) per stack

## Quickstart

```bash
python scripts/build.py --editor=cursor --out out/default
python scripts/validate.py --all
tree out/default/.cursor/rules
```
