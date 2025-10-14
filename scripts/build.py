#!/usr/bin/env python3
import argparse, json, shutil, time, pathlib, hashlib
from typing import Dict, List, Tuple, Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKSPACE_PREFIX = "Workspace"

def load_jsons(dirpath: pathlib.Path) -> List[Tuple[str, Dict[str, Any]]]:
    """Return list of (filename, json_obj) for all *.json in dirpath."""
    items: List[Tuple[str, Dict[str, Any]]] = []
    for p in sorted(pathlib.Path(dirpath).glob("*.json")):
        with open(p, "r", encoding="utf-8") as f:
            items.append((p.name, json.load(f)))
    return items

def index_by_name(items: List[Tuple[str, Dict[str, Any]]]) -> Dict[str, Dict[str, Any]]:
    """Index list of (filename, obj) by obj['name']."""
    return {obj["name"]: obj for _, obj in items}

def apply_overlay(rules_by_name: Dict[str, Dict[str, Any]], overlay: Dict[str, Any]) -> None:
    """Apply simple overlay operations in-place to rules_by_name dict."""
    for ov in overlay.get("overrides", []):
        target = ov["target"]
        rule = rules_by_name.get(target)
        if not rule:
            continue  # ignore unknown targets
        if "append_content" in ov:
            rule["content"] = (rule.get("content", "") + "\n" + ov["append_content"]).strip()
        if "add_matches" in ov:
            rule["matches"] = sorted(set(rule.get("matches", []) + ov["add_matches"]))

def _require_workspace(rules: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Return the workspace rule or raise a clear error."""
    for r in rules:
        if r["name"].startswith(WORKSPACE_PREFIX):
            return r
    raise SystemExit(f"ERROR: No rule found with name starting '{WORKSPACE_PREFIX}'. "
                     f"Add a workspace contract rule (e.g., 'Workspace Contract (Universal)').")

def write_cursor_rules(outdir: pathlib.Path, rules: List[Dict[str, Any]]) -> None:
    """Write Cursor rules JSON under outdir/.cursor/rules/ in deterministic order."""
    rules_dir = pathlib.Path(outdir) / ".cursor" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    for rule in sorted(rules, key=lambda r: r["name"].lower()):
        fname = rule["name"].lower().replace(" ", "-").replace("/", "-") + ".json"
        with open(rules_dir / fname, "w", encoding="utf-8") as f:
            json.dump(rule, f, indent=2, ensure_ascii=False)

def _build_system_prompt(rules: List[Dict[str, Any]]) -> str:
    """Workspace first, then each adapter as H1 sections. Adds trailing newline."""
    ws = _require_workspace(rules)
    parts: List[str] = ["# Workspace Contract", "", ws["content"].strip()]
    for r in sorted(rules, key=lambda r: r["name"].lower()):
        if r is ws:
            continue
        parts.append(f"\n\n# {r['name']}\n")
        parts.append(r["content"].strip())
    text = "\n".join(parts)
    if not text.endswith("\n"):
        text += "\n"
    return text

def write_system_prompt(outdir: pathlib.Path, rules: List[Dict[str, Any]]) -> None:
    """Write a single system-prompt.txt into flat outdir/."""
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "system-prompt.txt").write_text(_build_system_prompt(rules), encoding="utf-8")

def sha256_dir(path: pathlib.Path) -> str:
    """SHA-256 of all files under path (sorted), excluding no files; compute before manifest write."""
    h = hashlib.sha256()
    for p in sorted(pathlib.Path(path).rglob("*")):
        if p.is_file():
            h.update(p.read_bytes())
    return h.hexdigest()

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--editor", choices=["cursor", "claude", "gemini"], default="cursor")
    ap.add_argument("--org", default=None)
    ap.add_argument("--project", default=None)
    ap.add_argument("--out", default="out/default")
    args = ap.parse_args()

    # Load & index
    core = load_jsons(ROOT / "core")
    adapters = load_jsons(ROOT / "adapters")
    rules_by_name = index_by_name(core + adapters)

    # Overlays (optional)
    if args.org:
        path = ROOT / "profiles" / "org" / f"{args.org}.overlay.json"
        with open(path, "r", encoding="utf-8") as f:
            apply_overlay(rules_by_name, json.load(f))
    if args.project:
        path = ROOT / "profiles" / "project" / f"{args.project}.overlay.json"
        with open(path, "r", encoding="utf-8") as f:
            apply_overlay(rules_by_name, json.load(f))

    # Materialize list after overlays (deterministic sort by name for all emitters)
    rules: List[Dict[str, Any]] = sorted(rules_by_name.values(), key=lambda r: r["name"].lower())

    # Fresh outdir
    outdir = pathlib.Path(args.out)
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Emit artifacts + choose hash root
    if args.editor == "cursor":
        write_cursor_rules(outdir, rules)
        sha_path = outdir / ".cursor" / "rules"
    elif args.editor in ("claude", "gemini"):
        write_system_prompt(outdir, rules)
        sha_path = outdir
    else:
        raise SystemExit(f"Unknown editor: {args.editor}")

    # Manifest (hash computed before manifest write, so manifest is not part of the hash)
    manifest = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "editor": args.editor,
        "org": args.org,
        "project": args.project,
        "rule_count": len(rules),
        "sha256": sha256_dir(sha_path),
    }
    with open(outdir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
