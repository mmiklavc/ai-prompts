# Java (Maven) Bootstrap Adapter

**Canonical Sources:** [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html), JUnit 5, Maven docs

## Style
- Google Java Style; use `google-java-format`
- Avoid static singletons, prefer dependency injection

## Testing
- JUnit 5 (Jupiter)
- Parameterized tests, Mockito for fakes

## Runbook

```bash
mvn -q -DskipTests=false test
mvn -q -T1C verify
mvn -q spotbugs:check checkstyle:check pmd:check
```
