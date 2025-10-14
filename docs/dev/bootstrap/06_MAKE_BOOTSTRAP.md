# Makefile Bootstrap Adapter

**Canonical Source:** GNU Make Manual

## Principles
- `.PHONY` for non-file targets
- Accurate dependencies, minimal hidden state
- Parallel-safe targets

## Runbook

```bash
make format
make lint
make test
make build
```
