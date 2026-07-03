# Configure Grafana Cloud

## What happens

Initial Grafana Cloud resources are provisioned for the service. This step sets up the foundations; alerting rules and dashboards that require a running application are completed in Phase 4 (Finalize Grafana Cloud).

What is configured now:

- Grafana datasources created (Prometheus for metrics, Loki for logs, Tempo for traces)
- Service-specific folder created in Grafana under the company organization
- API credentials generated and stored in secrets management for SDK use

## What you need to provide

**You must instrument your application during Phase 3 (Development).** The platform creates the Grafana resources, but your code must emit metrics, logs, and traces.

Use the OpenTelemetry SDK to emit telemetry — credentials are available as environment variables injected at runtime:

- `OTEL_EXPORTER_OTLP_ENDPOINT` — the Grafana Cloud OTLP endpoint
- `OTEL_EXPORTER_OTLP_HEADERS` — authentication headers

The scaffold template includes the OpenTelemetry SDK as a dependency and a basic configuration stub. Update the stub with your service-specific metric and span names.

## What to expect

Datasources are visible in Grafana immediately after this step. No data flows until the application is deployed and instrumented. Dashboards and alert rules are created in Phase 4 once live data is available to calibrate thresholds.
