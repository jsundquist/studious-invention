# Finalize Grafana Cloud

## What happens

Now that the service has been running in staging and emitting real telemetry, Grafana Cloud setup is completed with live-data-backed configuration:

- Service-specific dashboards are created using actual metric and trace names emitted by the service
- Alerting rules are configured using real baseline values observed from staging traffic
- On-call routing is configured to notify the owning team for critical alerts
- SLO (Service Level Objective) targets are registered based on the non-functional requirements provided at workflow start

## What you need to provide

This step is automated, but it depends on your application having been instrumented and deployed to staging. If the service is not emitting telemetry, dashboards will be empty and alert thresholds cannot be calibrated.

Before this step completes successfully:

- Confirm the service is running in staging and has received traffic (run your E2E tests to generate signal)
- Confirm OpenTelemetry is initialized and emitting data (check Grafana Explore for recent traces and metrics from your service)

If no telemetry data is found, this step will complete with a warning and dashboards will use default placeholder thresholds — these should be reviewed and updated before production deployment.

## What to expect

After this step, the service has a Grafana dashboard accessible to the owning team and alert rules active against staging. The same dashboards and alerts are promoted to monitor the production deployment in Phase 5.
