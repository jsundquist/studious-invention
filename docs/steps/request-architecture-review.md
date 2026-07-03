# Request Architecture Review

## What happens

An architecture review is assigned to the company's architecture team. This review must be resolved — either approved or skipped with a reason — before development begins in Phase 3.

The reviewer evaluates:

- Whether the service is appropriately scoped (does it do one thing well, or is it trying to do too much)
- API contract design — resource naming, HTTP method usage, error response structure
- Data model design and ownership boundaries
- Dependencies on other internal services and whether they are appropriate
- Non-functional requirements: expected load, latency targets, SLA

## What you need to provide

Before this step can be meaningfully reviewed, prepare the following and share them with the architecture team:

- **API specification** — an OpenAPI spec or equivalent describing your endpoints, request/response shapes, and error codes
- **Data model** — an entity diagram or description of what data the service owns and how it is structured
- **Dependency map** — which internal and external services this service depends on
- **Non-functional requirements** — expected request volume, latency targets, data retention needs

The scaffold template includes an OpenAPI spec stub generated from your health endpoint. Expand it to cover your planned API before the review.

## Approval outcomes

| Outcome | Meaning |
|---|---|
| **Approved** | Architecture meets company standards. Development may proceed. |
| **Skipped** | Review was bypassed. A reason must be provided and is recorded for audit purposes. Development proceeds but the skip is visible in the workflow history. |

## Note

This review cannot fail — it can only be approved or skipped. If the architecture needs changes, the reviewer works with the developer directly and marks the review approved once satisfied. The workflow does not loop.
