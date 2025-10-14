# Shell/Bash Bootstrap Adapter

**Canonical Sources:** ShellCheck, shfmt, Bash strict mode

## Best Practices
- Shebang: `#!/usr/bin/env bash`
- `set -euo pipefail`
- Quote variables; trap cleanup
- Avoid UUOC, ensure portability

## Runbook

```bash
shellcheck **/*.sh
shfmt -w .
```
