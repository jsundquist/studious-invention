# Deploy to Production

## What happens

The same container image that was running in staging is promoted to the production environment. No new build occurs — the exact artifact validated in staging is what goes to production.

- Production infrastructure is provisioned (mirrors staging sizing unless a different tier was specified)
- Container image is deployed from the company container registry
- Environment variables and secrets are injected from secrets management (production-scoped values)
- DNS record is updated to point to the production load balancer
- The service is registered in the internal service catalog as production-active

## What you need to provide

Nothing at this step — it is fully automated. Production environment configuration (secrets, environment variables) was established during infrastructure provisioning in Phase 1. No changes to application code or configuration are made at this step.

## What to expect

Production deployment uses a rolling strategy — new instances start before old ones stop, ensuring zero downtime. The load balancer health check (`GET /health`) must pass before traffic is shifted to new instances.

If the health check fails after deployment, the rollout is halted and the previous version continues serving traffic. The workflow is paused and the owning team is alerted via Grafana Cloud.
