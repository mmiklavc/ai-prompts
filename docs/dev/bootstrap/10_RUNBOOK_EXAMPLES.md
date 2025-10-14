# Runbook Composition Examples

## Example: Go + Helm + JSON

```bash
go fmt ./...
go vet ./...
go test ./... -race -cover
helm lint ./charts/myservice
helm template ./charts/myservice --debug --dry-run
jq -e . ./deploy/config.json > /dev/null
```

## Example: Python + Shell

```bash
black .
ruff check .
pytest -q
shellcheck **/*.sh
```
