import argparse, json, os, shutil, hashlib, time, glob, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

def load_jsons(dirpath):
    items = []
    for p in sorted(pathlib.Path(dirpath).glob("*.json")):
        with open(p, "r", encoding="utf-8") as f:
            items.append((p.name, json.load(f)))
    return items

def index_by_name(items):
    return {item['name']: item for _, item in items}

def apply_overlay(rules_by_name, overlay):
    for ov in overlay.get("overrides", []):
        target = ov["target"]
        if target not in rules_by_name:
            continue
        rule = rules_by_name[target]
        if "append_content" in ov:
            rule["content"] = (rule.get("content","") + "\n" + ov["append_content"]).strip()
        if "add_matches" in ov:
            rule["matches"] = sorted(set(rule.get("matches", []) + ov["add_matches"]))

def write_cursor_rules(outdir, rules):
    rules_dir = pathlib.Path(outdir) / ".cursor" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    for rule in rules:
        fname = rule["name"].lower().replace(" ", "-").replace("/", "-") + ".json"
        with open(rules_dir / fname, "w", encoding="utf-8") as f:
            json.dump(rule, f, indent=2)
    return rules_dir

def write_claude_prompt(outdir, rules):
    prompt = []
    prompt.append("# Workspace Contract\n")
    prompt.append(next(r for r in rules if r["name"].startswith("Workspace"))["content"])
    for r in rules:
        if r["name"].startswith("Workspace"):
            continue
        prompt.append(f"\n\n# {r['name']}\n")
        prompt.append(r["content"])
    outp = pathlib.Path(outdir) / "out" / "claude"
    outp.mkdir(parents=True, exist_ok=True)
    with open(outp / "system-prompt.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(prompt))

def write_gemini_prompt(outdir, rules):
    prompt = []
    ws = next(r for r in rules if r["name"].startswith("Workspace"))
    prompt.append("# Workspace Contract\n")
    prompt.append(ws["content"].strip())
    for r in rules:
        if r is ws:
            continue
        prompt.append(f"\n\n# {r['name']}\n")
        prompt.append(r["content"].strip())
    outp = pathlib.Path(outdir) / "out" / "gemini"
    outp.mkdir(parents=True, exist_ok=True)
    with open(outp / "system-prompt.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(prompt))

def sha256_dir(path):
    import hashlib
    h = hashlib.sha256()
    for p in sorted(pathlib.Path(path).rglob("*")):
        if p.is_file():
            h.update(p.read_bytes())
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--editor", choices=["cursor","claude","gemini"], default="cursor")
    ap.add_argument("--org", default=None)
    ap.add_argument("--project", default=None)
    ap.add_argument("--out", default="out/default")
    args = ap.parse_args()

    core = load_jsons(ROOT / "core")
    adapters = load_jsons(ROOT / "adapters")

    items = core + adapters
    rules_by_name = index_by_name(items)
    rules = list(rules_by_name.values())

    if args.org:
        path = ROOT / "profiles" / "org" / f"{args.org}.overlay.json"
        with open(path, "r", encoding="utf-8") as f:
            apply_overlay(rules_by_name, json.load(f))
    if args.project:
        path = ROOT / "profiles" / "project" / f"{args.project}.overlay.json"
        with open(path, "r", encoding="utf-8") as f:
            apply_overlay(rules_by_name, json.load(f))

    rules = list(rules_by_name.values())

    outdir = pathlib.Path(args.out)
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    if args.editor == "cursor":
        write_cursor_rules(outdir, rules)
        sha_path = outdir / ".cursor" / "rules"
    elif args.editor == "claude":
        write_claude_prompt(outdir, rules)
        sha_path = outdir / "out" / "claude"
    elif args.editor == "gemini":
        write_gemini_prompt(outdir, rules)
        sha_path = outdir / "out" / "gemini"

    manifest = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "editor": args.editor,
        "org": args.org,
        "project": args.project,
        "rule_count": len(rules),
    }
    manifest["sha256"] = sha256_dir(sha_path)
    with open(outdir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    main()
