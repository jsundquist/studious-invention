# Workflow Orchestration Engine

## Status
Accepted

## Date
2026-06-23

## Context and Problem Statement

The golden path tool must orchestrate workflows that span automated and manual steps, external system integrations, and human approval gates — across a lifecycle of creating, updating, and decommissioning software artifacts. A workflow engine is needed that can model this as a durable, inspectable state machine where the current state, step history, and timing data are all queryable by the API layer and ultimately surfaced in the UI.

## Decision Drivers

- Human-in-the-loop steps are a first-class requirement — a manager approval gate must genuinely pause execution and resume only when an external actor signals completion, not simulate it via polling
- Async callback pattern — the workflow must be able to hand off work to an external system, suspend, and resume when that system calls back; equivalent to Step Functions' wait-for-task-token
- Phases containing steps with flexible execution order — steps within a phase must be expressible as sequential, fully parallel, or a combination
- Choice and branching logic — the workflow must support conditional paths based on state or outcomes
- Queryable workflow definition — the engine must expose an API that returns a structured representation of the workflow: its phases, steps, step types, and relationships; this data drives UI rendering of the golden path
- Queryable execution state — the engine must expose current execution state at the step level: which steps are active, waiting, or completed
- Step-level timestamps — entry and exit time per step are required as the foundation for future DORA-style metrics (phase duration, time spent waiting on human approval, total workflow duration)
- Cost — consumption-billed managed cloud services are not appropriate for a solo learning project; the engine must be usable without incurring per-execution charges
- Integration workers will be written manually — built-in connector libraries are not a deciding factor; the orchestration layer owns the workflow structure, not the integration details
- Self-hostable locally is a nice-to-have — running without an external cloud dependency simplifies local development, but it is not a hard requirement; a credible path to cloud deployment when the project is ready for it is preferred

## Considered Options

- **Camunda 8 (self-hosted)** — open source BPMN-native orchestrator with a full REST API surface
- **AWS Step Functions** — managed state machine service with full feature parity for this use case
- **GCP Workflows** — managed workflow service with similar capabilities
- **Temporal** — code-first durable workflow engine with strong execution guarantees
- **n8n** — visual automation platform with broad built-in integrations

## Decision Outcome

Chosen option: "Camunda 8 (self-hosted)", because it is the only self-hostable option that satisfies every requirement as a first-class capability: human tasks, async message-based waiting, parallel and sequential execution within sub-processes, choice gateways, a queryable process definition API, and step-level execution history with timestamps — all without a managed cloud dependency or consumption-based cost.

### Consequences

Choosing Camunda means learning BPMN as the language for defining workflows. BPMN has its own vocabulary and visual conventions that take time to become fluent in. That learning curve is accepted as part of the project's purpose. The benefit is that BPMN is an open standard — the workflow definitions are not proprietary to Camunda, and the visual diagram of the workflow is inherently documentation that any stakeholder can read.

Camunda 8 runs as a multi-component stack (Zeebe engine, Operate for monitoring and history, Tasklist for human tasks, Elasticsearch for history storage). Running this locally via Docker Compose is straightforward using Camunda's official compose configuration, but the resource footprint is heavier than a single-service workflow tool. This is a known tradeoff for local development.

Workflow definitions (BPMN files) are deployed to Camunda via its REST API and can be version-controlled and managed as infrastructure artifacts alongside the code that depends on them.

Camunda ships with a native human task UI called Tasklist, which is capable of rendering human task steps and collecting user input via Camunda Forms. In this architecture, Tasklist serves as an operator and admin tool — useful for debugging stuck workflows or inspecting execution state — rather than the developer-facing surface. Human task interactions will be routed through the custom UI and API layer instead, so that end users have no direct relationship with Camunda. This keeps licensing considerations manageable as the number of users grows, provides a unified experience that combines the catalog, workflow visualization, and task interaction in one place, and avoids splitting the developer experience across multiple products. The decision on the custom UI is addressed in ADR-004.

## Why Each Option Was Considered

### Camunda 8 (self-hosted) — chosen

Camunda is built on BPMN, a workflow modeling standard designed explicitly for the kind of processes this project requires. Human tasks are a native primitive — a workflow step that pauses execution and waits for a person to act before continuing. Async message-based waiting (the equivalent of wait-for-task-token) is also native via BPMN message events and receive tasks. Parallel gateways, exclusive gateways, and sub-processes map directly to the parallel blocks, choice blocks, and phases required by this project.

Critically, Camunda exposes two APIs that are essential to this project's architecture. The process definition API returns the full BPMN structure of a workflow — its phases, steps, step types, and connections — as queryable data that the FastAPI layer can use to drive UI rendering. The Operate API returns step-level execution state and timestamps for every flow node in a running or completed instance, providing the raw material for current-state display and future DORA metrics.

Deployment locally is via Docker Compose using Camunda's official configuration. For future cloud deployment, Terraform can provision the underlying infrastructure and Camunda can be deployed via Helm charts on a Kubernetes cluster or as Docker containers on a single VM. BPMN workflow definitions can be deployed via the Camunda REST API or managed through the Camunda Terraform provider, treating them as versionable infrastructure artifacts.

### AWS Step Functions — rejected

AWS Step Functions has feature parity for every requirement in this decision. It supports human approval patterns via wait-for-task-token, parallel and sequential execution, choice states, a DescribeStateMachine API that returns the full state machine definition as structured JSON, and GetExecutionHistory with step-level timestamps.

It is rejected on cost and cloud dependency. Step Functions is a consumption-billed managed service with no self-hosted option. Running it for a solo learning project requires an AWS account, incurs charges for every execution, and introduces a cloud dependency that is unnecessary for local development.

### GCP Workflows — rejected

GCP Workflows is Google Cloud's equivalent to Step Functions and shares the same rejection reason. It is a managed service with no self-hosted option, consumption-based pricing, and a cloud dependency that does not fit a localhost-first project. It also lacks the same breadth of human-in-the-loop support as either Step Functions or Camunda.

### Temporal — rejected

Temporal is a strong durable workflow engine with excellent support for the async callback pattern (via signals), parallel and sequential execution, and reliable long-running processes. It is self-hostable and would otherwise be a credible choice.

It is rejected because its workflow structure is defined entirely in code. There is no API to query the definition of a workflow and receive back a structured representation of its phases and steps. The workflow IS the code — to understand what it does, you read it. This means there is no native path to drive the UI rendering of the golden path from the engine itself; a separate metadata registry would have to be built and maintained alongside the workflow code. That is a meaningful gap for a tool whose primary user-facing feature is a visual representation of the workflow.

### n8n — rejected as primary orchestrator

n8n was the original technology considered for this role and has genuine strengths. Its 400+ built-in integration nodes reduce the integration work needed to connect external systems, and its visual workflow builder produces a node graph that is queryable via REST API — the workflow definition is returned as structured JSON with nodes and connections.

It is rejected as the primary orchestrator because the core requirements map poorly to its design. n8n is built for automation flows, not structured stateful orchestration. Human-in-the-loop is approximated via a Wait node that pauses until a webhook is called — functional, but not a native construct with the same semantics as a BPMN user task. The phase/step model with explicit parallel and sequential blocks is not a natural fit for n8n's node graph model. Step-level execution history with entry and exit timestamps is not cleanly exposed via its API; execution records exist at the workflow level rather than the individual node level.

The built-in integrations remain a noted advantage. If a future integration requirement benefits significantly from an n8n node, invoking n8n as a downstream service from a Camunda service task remains an option — but it is not the right engine to own the orchestration layer.
