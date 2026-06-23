# Architecture

## What This System Is

A golden path tool — an Internal Developer Platform (IDP) that provides opinionated, repeatable workflows for managing software artifacts through three lifecycle phases:

- **Create** — from concept to a running production service
- **Update** — a repeatable, safe path for changes to a live artifact
- **Decommission** — structured teardown that leaves no orphaned resources

The goal is to replace implicit tribal knowledge about "how we ship things" with a documented, automatable process that every developer follows the same way.

## Components

### Workflow Engine (Camunda 8)

The orchestration layer. Owns the lifecycle state of every in-flight workflow — which phase it is in, which steps are complete, which are waiting on a human or an external system. Provides the queryable process definition that drives UI rendering and the step-level execution history that underpins operational metrics.

### Workflow Definitions (`workflows/`)

BPMN files that define the structure of each lifecycle workflow — its phases, steps, branching logic, and human task points. Deployed to Camunda on stack startup. Versioned in the repository alongside the code that depends on them.

### API (coming)

The layer between the UI and Camunda. Handles user-facing operations — starting a workflow, querying execution state, completing human tasks — and exposes no Camunda internals directly to the UI.

### Worker Service (coming)

A separate background process that polls Camunda for automated service task jobs, executes them (calling external systems, running checks, triggering integrations), and reports completion back. Distinct from the API — it has no HTTP surface of its own.

### UI (coming)

The developer-facing surface. Displays the catalog of software artifacts, renders the golden path visualization for each workflow, and surfaces human task interactions. Communicates exclusively through the API.

## Decision Records

Architectural decisions are documented as ADRs in [`docs/adr/`](adr/). Each ADR captures the context, the options considered, and the reasoning behind the choice made.

| ADR | Decision |
|-----|----------|
| [001](adr/001-project-vision-and-goals.md) | Project vision and goals |
| [002](adr/002-monorepo-vs-polyrepo.md) | Monorepo with path-filtered CI |
| [003](adr/003-workflow-orchestration-engine.md) | Camunda 8 as workflow orchestration engine |
| [004](adr/004-camunda-setup-and-workflow-storage.md) | Camunda local setup and workflow definition storage |
