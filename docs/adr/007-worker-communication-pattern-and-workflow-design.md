# ADR-007: Worker Communication Pattern and Workflow Design

**Status:** Accepted  
**Date:** 2026-07-02

---

## Context

With the API technology (FastAPI) and workflow orchestration engine (Camunda 8) decided, the next question is how the system components communicate with each other and how the golden path workflows are structured. This ADR captures the communication architecture between the UI, the API, Camunda, and the worker service — and the design principles behind the workflow definitions themselves.

---

## Decision

### Communication Architecture

The system uses the following communication flow:

```
UI  →  FastAPI  →  Camunda (Zeebe / Operate)
                        ↕
                     Worker
```

**UI → FastAPI**: The UI communicates exclusively over HTTP with the FastAPI layer. It never talks to Camunda directly.

**FastAPI → Camunda**: FastAPI uses Camunda's REST APIs to start process instances (Zeebe REST API), query execution state and history (Operate REST API), and complete user tasks (Zeebe REST API). FastAPI translates Camunda's internal data model into clean domain objects before returning responses to the UI.

**Camunda ↔ Worker**: The worker is a separate Python process that polls Zeebe for service task jobs using Zeebe's long-polling job worker protocol. When Zeebe reaches a service task in a workflow, it creates a job of the configured type. The worker picks up the job, executes the corresponding handler, and reports completion or failure back to Zeebe. The worker does not expose an HTTP surface and does not appear in the FastAPI OpenAPI spec.

The worker communicates with Zeebe only — it does not call FastAPI. If a worker handler needs data from the artifact catalog or other application state, that data is passed as input variables on the job by FastAPI at process instantiation time.

### Why the Worker Is a Separate Process

Service task workers poll *outbound* to Zeebe — they do not receive inbound HTTP requests and have no routes to register. Embedding job workers as background threads inside FastAPI would couple two unrelated operational concerns: serving HTTP traffic and executing background automation jobs. A separate `apps/worker/` process has its own lifecycle, can be scaled independently, and keeps the FastAPI application focused on its HTTP surface.

### BPMN Represents Specific Tools, Not Generic Capabilities

Workflow definitions name specific tools explicitly (e.g. "Configure SonarCloud", "Configure Snyk") rather than generic capabilities (e.g. "Configure Security Scanning"). This is intentional: the golden path is opinionated. The UI renders workflow steps directly from the BPMN definition, so step names must be meaningful to developers. If the company's tooling changes, the BPMN is updated to reflect the new standard — this is appropriate because a tooling change represents a genuine change to the golden path itself.

### Human Task Outcome Model

Every human task gate in a workflow has exactly two valid outcomes:

- **Approved** — the reviewer confirms the work meets the standard
- **Skipped with reason** — the reviewer explicitly bypasses the gate with a recorded justification

Neither outcome causes the workflow to fail or block. The skip reason is captured as a named process variable (e.g. `architectureReviewSkipReason`) and is available via the Operate API for audit purposes. There is no "rejected" state — rejection without a path forward is not useful in a developer platform context.

### Workflow Phase Model

The Create lifecycle for a Backend API/Service is divided into five phases modeled as BPMN sub-processes:

1. **Provision Project** — automated service tasks that set up the repository, tooling, infrastructure, and staging deployment
2. **Request Initial Reviews** — human tasks for architecture review and initial security review; both must be resolved (approved or skipped) before development begins
3. **Development** — human tasks tracking development progress: implementation, unit tests, end-to-end tests
4. **Resolve Security Findings** — automated re-scan followed by human tasks to resolve findings and obtain final security sign-off
5. **Production Deployment** — automated production deploy and health check

---

## Options Considered

### Option A: Worker embedded in FastAPI as background threads

Run job workers as `asyncio` background tasks inside the FastAPI process. Rejected because: workers and HTTP handlers have different scaling profiles, failure modes, and operational concerns. A crashed worker loop would not surface clearly in FastAPI's health endpoint. A separate process fails independently and can be restarted without affecting the HTTP layer.

### Option B: Camunda calls back to FastAPI via webhooks

Configure Camunda outbound connectors to POST to FastAPI endpoints when tasks complete. Rejected because: this inverts the dependency direction, requires FastAPI to expose Camunda-specific webhook endpoints, and introduces a network dependency from Camunda to FastAPI that complicates local development and testing.

### Option C: Generic capability names in BPMN

Use generic step names ("Configure Security Scanning") and let the worker implementation decide which tools to invoke. Rejected because: the UI renders step names directly from the workflow definition. Generic names do not give developers meaningful visibility into what the platform is doing on their behalf. The workflow definition IS the golden path specification — it should be explicit.

---

## Consequences

- The worker is a third deployable unit alongside FastAPI and the UI, but it shares the same repository and deployment pipeline
- BPMN files must be updated when tooling changes — this is acceptable and expected; the ADR history documents why each tool was chosen
- The Operate REST API is used for querying execution state; this API is not officially stable in Camunda 8 and may require updates across Camunda versions
- All process input data needed by workers must be passed as variables at instantiation time or fetched by workers directly from external services — workers do not call FastAPI
