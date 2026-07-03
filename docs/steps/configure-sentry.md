# Configure Sentry

## What happens

A Sentry project is created for the service and a DSN (Data Source Name) is generated. The DSN is stored in secrets management so your application can retrieve it at runtime.

- Sentry project created under the company organization
- DSN stored as a secret (see Secrets Management step later in this phase)
- Alert rules configured for new issue notifications routed to the owning team
- Source map support enabled for compiled languages

## What you need to provide

**You must integrate the Sentry SDK into your application during Phase 3 (Development).** The platform creates the Sentry project and stores the DSN, but your code must initialize the SDK with it.

Retrieve the DSN from the environment variable `SENTRY_DSN` (injected at runtime from secrets management) and initialize the SDK on application startup.

Example (Python):
```python
import sentry_sdk
sentry_sdk.init(dsn=os.environ["SENTRY_DSN"])
```

## What to expect

Error tracking is inactive until the SDK is integrated and the application is deployed. Once integrated, errors, performance traces, and release tracking are visible in the Sentry dashboard under the company organization.
