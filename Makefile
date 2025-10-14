# Root Makefile — dev tools + rule builds (no SoT, no prompts generator)
# Usage:
#   make help
#   make setup | tools | update-tools | doctor
#   make rules                 # builds cursor+claude+gemini
#   make rules-cursor          # cursor only
#   make rules-claude          # claude only
#   make rules-gemini          # gemini only
#   make validate | clean | clean-all

SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.ONESHELL:
.DEFAULT_GOAL := help

# -----------------------
# Variables (override via CLI)
# -----------------------
PY          ?= python
ORG         ?=
PROJECT     ?=
OUT_CURSOR  ?= out/cursor
OUT_CLAUDE  ?= out/claude
OUT_GEMINI  ?= out/gemini

# -----------------------
# Helper macros
# -----------------------
define _assert_cmd
	@command -v $(1) >/dev/null 2>&1 || { echo "❌ missing '$(1)'. Install it and retry."; exit 1; }
endef
define _assert_file
	@[ -f "$(1)" ] || { echo "❌ missing file: $(1)"; exit 1; }
endef

# -----------------------
# Help
# -----------------------
.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS=":.*?## " ; print "Targets:"} /^[a-zA-Z0-9_\-]+:.*?## / {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort
	@echo
	@echo "Vars: ORG=$(ORG) PROJECT=$(PROJECT) OUT_CURSOR=$(OUT_CURSOR) OUT_CLAUDE=$(OUT_CLAUDE) OUT_GEMINI=$(OUT_GEMINI) PY=$(PY)"

# -----------------------
# Tooling
# -----------------------
.PHONY: setup tools update-tools doctor
setup: ## One-time: install asdf plugins & pinned tool versions
	$(call _assert_cmd,asdf)
	@bash dev-tools/install-asdf-plugins.sh

tools: ## Ensure pinned tool versions are installed (asdf install + reshim)
	$(call _assert_cmd,asdf)
	@asdf install
	@asdf reshim

update-tools: ## Reinstall/upgrade tools after editing .tool-versions
	$(call _assert_cmd,asdf)
	@asdf install
	@asdf reshim

doctor: ## Print current asdf tool versions and key binaries
	@echo "→ asdf current (if available)"
	@if command -v asdf >/dev/null 2>&1; then asdf current || true; else echo "(asdf not installed)"; fi
	@for cmd in jq shellcheck shfmt yamllint tree; do \
		if command -v $$cmd >/dev/null 2>&1; then \
			echo "✓ $$cmd: $$($$cmd --version 2>/dev/null | head -n1)"; \
		else \
			echo "✗ $$cmd: not found"; \
		fi; \
	done

# -----------------------
# Rule builds (Cursor / Claude / Gemini)
# -----------------------
.PHONY: rules rules-cursor rules-claude rules-gemini
rules: ## Build ALL: Cursor rules + Claude + Gemini
	$(call _assert_cmd,$(PY))
	$(call _assert_file,scripts/build.py)
	@echo "→ Building ALL editors (org=$(ORG) project=$(PROJECT))"
	@$(PY) scripts/build.py --editor=cursor $(if $(ORG),--org $(ORG),) $(if $(PROJECT),--project $(PROJECT),) --out $(OUT_CURSOR)
	@$(PY) scripts/build.py --editor=claude $(if $(ORG),--org $(ORG),) $(if $(PROJECT),--project $(PROJECT),) --out $(OUT_CLAUDE)
	@$(PY) scripts/build.py --editor=gemini $(if $(ORG),--org $(ORG),) $(if $(PROJECT),--project $(PROJECT),) --out $(OUT_GEMINI)
	@echo "✅ Built:"
	@echo "   • Cursor rules → $(OUT_CURSOR)/.cursor/rules"
	@echo "   • Claude prompt → $(OUT_CLAUDE)/system-prompt.txt"
	@echo "   • Gemini prompt → $(OUT_GEMINI)/system-prompt.txt"

rules-cursor: ## Build Cursor rules only → $(OUT_CURSOR)/.cursor/rules
	$(call _assert_cmd,$(PY))
	$(call _assert_file,scripts/build.py)
	@$(PY) scripts/build.py --editor=cursor $(if $(ORG),--org $(ORG),) $(if $(PROJECT),--project $(PROJECT),) --out $(OUT_CURSOR)
	@echo "✅ Built Cursor rules to $(OUT_CURSOR)/.cursor/rules"

rules-claude: ## Build Claude system prompt only → $(OUT_CLAUDE)/system-prompt.txt
	$(call _assert_cmd,$(PY))
	$(call _assert_file,scripts/build.py)
	@$(PY) scripts/build.py --editor=claude $(if $(ORG),--org $(ORG),) $(if $(PROJECT),--project $(PROJECT),) --out $(OUT_CLAUDE)
	@echo "✅ Wrote Claude prompt to $(OUT_CLAUDE)/system-prompt.txt"

rules-gemini: ## Build Gemini system prompt only → $(OUT_GEMINI)/system-prompt.txt
	$(call _assert_cmd,$(PY))
	$(call _assert_file,scripts/build.py)
	@$(PY) scripts/build.py --editor=gemini $(if $(ORG),--org $(ORG),) $(if $(PROJECT),--project $(PROJECT),) --out $(OUT_GEMINI)
	@echo "✅ Wrote Gemini prompt to $(OUT_GEMINI)/system-prompt.txt"

# -----------------------
# Validation / housekeeping
# -----------------------
.PHONY: validate clean clean-all
validate: ## Validate rule schemas + routing hints
	$(call _assert_cmd,$(PY))
	$(call _assert_file,scripts/validate.py)
	@$(PY) scripts/validate.py --all

clean: ## Remove common build outputs
	@rm -rf $(OUT_CURSOR) $(OUT_CLAUDE) $(OUT_GEMINI)
	@echo "🧹 Cleaned build outputs: $(OUT_CURSOR) $(OUT_CLAUDE) $(OUT_GEMINI)"

clean-all: ## Nuke entire out/ directory
	@rm -rf out
	@echo "🧨 Removed out/"

