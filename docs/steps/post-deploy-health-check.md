# Post-Deploy Health Check

## What happens

Automated smoke tests run against the production endpoint to confirm the service is live and behaving correctly after deployment.

The following are verified:

- `GET /health` returns HTTP 200 within the expected latency threshold
- At least one authenticated request to a primary endpoint succeeds
- Sentry is receiving events from the production instance
- Grafana Cloud is receiving metrics and traces from the production instance
- The service appears as healthy in the internal service catalog

## What you need to provide

Nothing — this step is fully automated. However, it depends on your health endpoint being correctly implemented. The health endpoint must:

- Return HTTP 200 when the service is ready to serve traffic
- Return a non-200 status (or time out) if the service is not ready
- Not require authentication
- Respond within 5 seconds

A deeper health check that verifies database connectivity or downstream service availability is recommended but not required.

## What to expect

If all checks pass, the workflow completes and your service is officially in production. A completion notification is sent to the owning team.

If any check fails, the owning team is alerted and the issue must be investigated directly. The workflow records the failure but does not automatically roll back — rollback decisions are made by the owning team.
