# Helm Bootstrap Adapter

**Canonical Sources:** Helm Docs, Best Practices

## Guidelines
- No hardcoded secrets
- Validate with `helm lint`
- Test templates with dry runs

## Runbook

```bash
helm lint ./charts/<name>
helm template ./charts/<name> --debug --dry-run
```
