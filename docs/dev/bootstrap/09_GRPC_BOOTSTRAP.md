# gRPC / Protobuf Bootstrap Adapter

**Canonical Sources:** gRPC Concepts, Performance Best Practices, Proto Style Guide

## Design
- Follow proto3 style (names, packages, field numbering)
- Unary vs streaming: explicit choice
- Include deadlines/timeouts

## Versioning
- Additive changes preferred
- Reserve/avoid field reuse
- Document version bumps

## Runbook

```bash
protoc --proto_path=. --go_out=. --go-grpc_out=. path/to/*.proto
```
