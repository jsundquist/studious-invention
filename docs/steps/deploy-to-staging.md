# Deploy to Staging

## What happens

The latest build from the `main` branch is deployed to the staging environment provisioned in the previous step.

- Container image is pulled from the company container registry
- Environment variables and secrets are injected from secrets management
- Service is started and the load balancer health check is verified (`GET /health` must return HTTP 200)
- Staging endpoint is registered in the internal service catalog

## What you need to provide

**The scaffold project must build successfully before this step can complete.** The CI/CD pipeline (configured in Phase 1) must produce a passing build and push a container image to the registry.

If the build is failing at this point, check:

- The CI/CD pipeline logs in GitHub Actions
- That all required environment variables are referenced correctly in your application (they will be injected at runtime — do not hardcode values)
- That `GET /health` returns HTTP 200 with no dependencies on external services that may not be available yet

## What to expect

Once this step completes, the service is running and reachable at its staging endpoint. This endpoint is used by end-to-end tests in Phase 3 and by Grafana Cloud for dashboard calibration in Phase 4. The staging environment remains live for the duration of the workflow.
