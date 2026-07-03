# Develop Project

## What happens

This step represents active development of the service. The workflow pauses here until you mark development complete. There is no automated check — this is a human task that signals the platform that your implementation is ready to move forward.

## What you need to do

Implement the service according to the architecture approved in Phase 2. At a minimum, before marking this step complete:

- All planned API endpoints are implemented and functional against the staging environment
- The service integrates the Sentry SDK for error tracking (see Configure Sentry step)
- The service emits OpenTelemetry metrics, logs, and traces (see Configure Grafana Cloud step)
- All environment variables are sourced from the injected runtime environment — no hardcoded values
- The service passes local testing

## Completion outcomes

| Outcome | Meaning |
|---|---|
| **Approved** | Development is complete and the service is ready for testing. |
| **Skipped** | Development milestone is bypassed. A reason must be provided. The workflow continues but the skip is visible in the history. |

## Note

Marking this step complete does not trigger any automated validation. Unit tests and end-to-end tests are separate steps that follow. If you mark development complete and tests reveal significant issues, continue working and mark tests complete when they pass — the workflow does not need to be restarted.
