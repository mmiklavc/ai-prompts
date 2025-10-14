# Prompt Rules Monorepo

A modular, profile-driven system for generating **AI coding rules and prompts** across a polyglot stack — Go, Python, Java/Maven, Shell, Make, Helm, JSON, and gRPC.

This repository produces:
- **Cursor rules** (machine-readable JSON)
- **Claude / Gemini system prompts** (single concatenated text)
- **Human-readable docs** (Markdown bootstrap prompts)

---

## Structure

- `core/` – universal workspace contract  
- `adapters/` – per-language rule adapters  
- `profiles/` – optional overlays (org / project / editor)  
- `scripts/` – deterministic build + validation  
- `dev-tools/` – asdf setup + pinned tool versions  
- `docs/dev/bootstrap/` – human-readable bootstrap prompt set  
- `out/` – generated artifacts (git-ignored)

---

## Quickstart

```bash
make setup          # install asdf plugins
make tools          # install pinned tool versions
make rules          # build Cursor + Claude + Gemini outputs
make validate       # schema + routing validation
```

### Build a single editor output

```bash
make rules-cursor   # → out/default/.cursor/rules
make rules-claude   # → out/claude/system-prompt.txt
make rules-gemini   # → out/gemini/system-prompt.txt
```

---

## Using in Cursor

```bash
mkdir -p .cursor
cp -r out/default/.cursor/rules .cursor/
```

---

## Outputs

- `out/default/.cursor/rules/` – Cursor JSON rule set  
- `out/claude/system-prompt.txt` – Claude system prompt  
- `out/gemini/system-prompt.txt` – Gemini system prompt  
- `docs/dev/bootstrap/` – reference bootstrap docs (committed)

---

## Requirements

- macOS/Linux, `make`
- Python ≥ 3.10
- `asdf` (tool versions), `jq`, optional `tree`

---

## Notes

- Builds are deterministic (stable ordering + content hashing).  
- Overlays in `profiles/` let you customize without touching `core/` or `adapters/`.  
- Add new languages by dropping a JSON adapter in `adapters/` and rebuilding.  

---

> Portions of this repository (including documentation and rule scaffolding) were generated or refined with the assistance of AI tools, such as ChatGPT (GPT-5).
> All generated content has been reviewed by human maintainers.
> See [LICENSE](./LICENSE) for full licensing details.

