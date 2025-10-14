# Prompt Rules Monorepo

A modular, profile-driven system for generating **AI coding rules and prompts** across a polyglot stack — Go, Python, Java/Maven, Shell, Make, Helm, JSON, and gRPC.

This repository produces:
- **Cursor rules** (project-local **`.mdc`** files with YAML front-matter + Markdown body)
- **Claude / Gemini system prompts** (single concatenated text)
- **Human-readable bootstrap docs** (Markdown prompt set)

---

## Structure

- `core/` – universal workspace contract  
- `adapters/` – per-language rule adapters (SoT, JSON)  
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

# Build all current emitters
make rules          # → out/cursor/.cursor/rules/*.mdc, out/claude/system-prompt.txt, out/gemini/system-prompt.txt

# Validate schemas + sanity checks
make validate
```

### Build a single editor output

```bash
make rules-cursor   # → out/cursor/.cursor/rules/*.mdc
make rules-claude   # → out/claude/system-prompt.txt
make rules-gemini   # → out/gemini/system-prompt.txt
```

You can override destinations:
```bash
make rules-cursor OUT_CURSOR=out/my-cursor
```

---

## Using in Cursor

Place the generated rules in your workspace root:

```bash
mkdir -p .cursor
cp -r out/cursor/.cursor/rules .cursor/
```

Cursor loads rules from `.cursor/rules/*.mdc` automatically (no legacy `.cursorrules` needed).

---

## Outputs

- `out/cursor/.cursor/rules/*.mdc` – Cursor rule files (MDC format)  
- `out/claude/system-prompt.txt` – Claude system prompt  
- `out/gemini/system-prompt.txt` – Gemini system prompt  
- `docs/dev/bootstrap/` – reference bootstrap docs (committed)

---

## CLI (scripts/build.py)

```text
--editor   cursor|claude|gemini   (default: cursor)
--org      optional org overlay   (profiles/org/<name>.overlay.json)
--project  optional project overlay (profiles/project/<name>.overlay.json)
--out      output dir (default: out/<editor>)
```

Example:
```bash
python scripts/build.py --editor=cursor --out out/cursor
python scripts/build.py --editor=claude --out out/claude
python scripts/build.py --editor=gemini --out out/gemini
```

---

## Notes

- **Source of truth** is JSON in `core/` and `adapters/`; build emits Cursor-native **`.mdc`** files.  
- Overlays in `profiles/` let you customize without touching `core/`/`adapters/`.  
- Builds are deterministic (stable ordering + content hashing in `manifest.json`).  
- Add new languages by dropping a JSON adapter in `adapters/` and rebuilding.  

---

> Portions of this repository (including documentation and rule scaffolding) were generated or refined with the assistance of AI tools, such as ChatGPT (GPT-5).
> All generated content has been reviewed by human maintainers.
> See [LICENSE](./LICENSE) for full licensing details.

