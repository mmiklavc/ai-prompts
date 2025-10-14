import argparse, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED_KEYS = {"name","description","matches","content"}

def iter_rules():
    for folder in ["core","adapters"]:
        for p in sorted((ROOT / folder).glob("*.json")):
            yield p

def validate_schema(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = REQUIRED_KEYS - set(data.keys())
    if missing:
        return f"{path.name}: missing keys {sorted(missing)}"
    if not isinstance(data["matches"], list) or not all(isinstance(x,str) for x in data["matches"]):
        return f"{path.name}: 'matches' must be a list of strings"
    if not data["name"] or not data["content"]:
        return f"{path.name}: 'name' and 'content' must be non-empty"
    return None

def detect_collisions():
    globs = {}
    for p in iter_rules():
        data = json.loads(p.read_text(encoding="utf-8"))
        for m in data["matches"]:
            globs.setdefault(m, set()).add(data["name"])
    problems = []
    for g, names in globs.items():
        if len(names) > 3 and g != "**/*":
            problems.append(f"Glob '{g}' used by many rules: {sorted(names)}")
    return problems

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    errors = []
    for p in iter_rules():
        err = validate_schema(p)
        if err:
            errors.append(err)

    collisions = detect_collisions()
    for c in collisions:
        print(f"[routing] {c}", file=sys.stderr)

    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    else:
        print("Validation OK")
        sys.exit(0)

if __name__ == "__main__":
    main()
