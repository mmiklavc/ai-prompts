# Workspace Contract

Defines global structure, routing, deliverables format, and CI/Make conventions.

## Routing

| Stack | File Patterns |
|-------|----------------|
| Go | `**/*.go`, `go.mod`, `go.sum` |
| Python | `**/*.py`, `pyproject.toml`, `requirements*.txt` |
| Java | `**/*.java`, `pom.xml` |
| Bash/Shell | `**/*.sh`, executable files with shebang |
| Make | `Makefile`, `**/*.mk` |
| Helm | `charts/**`, `Chart.yaml`, `values*.yaml` |
| JSON | `**/*.json`, `**/*.schema.json` |
| gRPC/Proto | `**/*.proto` |

## Universal Rules

- Clarity > cleverness
- Validate inputs; sanitize paths; enforce timeouts; never log secrets
- Deterministic, hermetic tests
- Deliverables order: Plan → Diffs → Tests → Runbook → Notes
- Avoid new deps unless justified and pinned
- Prefer Make/CI targets: `format`, `lint`, `test`, `build`

