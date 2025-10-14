# Python Bootstrap Adapter

**Canonical Sources:** PEP 8, PEP 257, mypy, pytest

## Style & Typing
- PEP 8, docstrings per PEP 257
- Use type hints and run `mypy` strict mode
- Prefer dataclasses

## Testing
- pytest with fixtures/parametrize
- Avoid real network/disk I/O

## Runbook

```bash
ruff check .
black .
mypy .
pytest -q
```
