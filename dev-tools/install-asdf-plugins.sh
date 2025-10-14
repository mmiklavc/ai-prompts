#!/usr/bin/env bash
set -euo pipefail

# Ensure asdf is available
if ! command -v asdf >/dev/null 2>&1; then
  echo "asdf not found. Install via Homebrew (macOS): brew install asdf"
  echo "Then source asdf in your shell (e.g., echo '. \"/opt/homebrew/opt/asdf/libexec/asdf.sh\"' >> ~/.zshrc)"
  exit 1
fi

add_plugin() {
  local name="$1" url="$2"
  if asdf plugin list --urls | grep -q "^${name}\b"; then
    echo "✓ plugin '${name}' already present"
  else
    echo "→ adding plugin '${name}' from ${url}"
    asdf plugin add "${name}" "${url}"
  fi
}

# Pin plugins by URL to avoid shortname drift (asdf docs recommend this approach)
# https://asdf-vm.com/manage/plugins.html
add_plugin python     https://github.com/danhper/asdf-python.git
add_plugin jq         https://github.com/AZMCode/asdf-jq.git
add_plugin shellcheck https://github.com/luizm/asdf-shellcheck.git
add_plugin shfmt      https://github.com/luizm/asdf-shfmt.git
add_plugin yamllint   https://github.com/ericcornelissen/asdf-yamllint.git

# Optional tree (plugin availability can vary; see README notes)
# add_plugin tree       https://github.com/asdf-community/asdf-tree.git

echo "→ installing tool versions from .tool-versions (this may take a bit)"
asdf install

echo "→ reshim"
asdf reshim

echo "✓ Done. Tools are pinned per-project via .tool-versions."

