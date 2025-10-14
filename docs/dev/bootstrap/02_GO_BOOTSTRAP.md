# Go Bootstrap Adapter

**Canonical Sources:** [Effective Go](https://go.dev/doc/effective_go), [Best Practices (2013 Talk)](https://go.dev/talks/2013/bestpractices.slide)

## Idioms

- Effective Go naming & structuring
- Early returns, zero-value types, minimal interfaces
- Synchronous public APIs, concurrency internal
- Document exported symbols

## Errors

- Return/wrap with `%w`
- Use `errors.Is/As`
- Include actionable context

## Concurrency

- Use `context.Context` boundaries
- Avoid goroutine leaks
- Verify with `go test -race`

## Testing

- Table-driven, small, deterministic
- Benchmarks for performance-sensitive code

## Runbook

```bash
go fmt ./...
go vet ./...
go test ./... -race -cover
staticcheck ./...      # optional
govulncheck ./...      # optional
```
