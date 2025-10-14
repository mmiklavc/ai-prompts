# Workspace Contract (Universal)

**Deliverables (strict order)**
1) Plan (3–6 bullets)
2) Changes (per-file `diff` or full files)
3) Tests (unit + param; add bench if perf-sensitive)
4) Runbook (exact format/lint/test/build commands for stacks touched)
5) Notes (short rationale; API/migration; cancellation/cleanup; security/perf)

**Global principles**
- Clarity over cleverness; small functions; isolate helpers
- Security: validate inputs; sanitize paths; never log secrets; timeouts & resource bounds
- Testing: hermetic; deterministic seeds; fakes over real I/O
- Dependencies: avoid adding; if needed, justify and pin
- CI/Make: reuse existing targets (`format|lint|test|build`). If missing, propose minimal ones.
