# JSON Bootstrap Adapter

**Canonical Sources:** RFC 8259, JSON Schema Draft 2020-12, jq manual

## Rules
- Follow RFC 8259
- Define schema near producer
- Validate syntax and schema

## Runbook

```bash
jq -e . <file.json> > /dev/null
```
