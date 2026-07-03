# Write End-to-End Tests

## What happens

This step represents writing end-to-end tests that run against the live staging environment. The workflow pauses here until you mark it complete.

## What you need to do

Write end-to-end tests that exercise the service through its real HTTP interface against staging. At minimum, cover:

- The primary happy path for each major API endpoint
- Authentication — verify that unauthenticated requests are rejected appropriately
- Error cases that depend on real infrastructure behavior (timeouts, not-found responses, etc.)

The staging endpoint is available in your workflow details and is also accessible via the internal service catalog. Tests should run against the `STAGING_BASE_URL` environment variable so they can be pointed at different environments.

The scaffold template includes a test directory and example E2E test structure. Extend it with service-specific tests.

## Completion outcomes

| Outcome | Meaning |
|---|---|
| **Approved** | End-to-end tests are written and passing against staging. |
| **Skipped** | E2E testing is bypassed. A reason must be provided. Skipping is recorded and visible to the security team during Phase 4 sign-off. |
