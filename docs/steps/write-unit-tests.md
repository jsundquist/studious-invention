# Write Unit Tests

## What happens

This step represents writing unit tests for the service. The workflow pauses here until you mark it complete.

## What you need to do

Write unit tests covering the service's business logic. Company standard requires:

- **Minimum 80% line coverage** — measured by SonarCloud (configured in Phase 1). Coverage below this threshold will cause the SonarCloud quality gate to fail in Phase 4, blocking production deployment.
- Tests must pass in CI — the GitHub Actions pipeline runs tests on every push and pull request
- Test each endpoint's happy path and primary error cases
- Mock external service calls — unit tests must not make real network requests

Coverage is reported automatically by SonarCloud on every pull request. Check your current coverage before marking this step complete.

## Completion outcomes

| Outcome | Meaning |
|---|---|
| **Approved** | Unit tests are written and coverage meets the company standard. |
| **Skipped** | Unit testing milestone is bypassed. A reason must be provided. Note: if coverage is below threshold at Phase 4, the SonarCloud quality gate will still block production deployment regardless of this skip. |
