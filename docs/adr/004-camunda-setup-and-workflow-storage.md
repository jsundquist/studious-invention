# Camunda Setup and Workflow Definition Storage

## Status
Accepted

## Date
2026-06-23

## Context and Problem Statement

With Camunda 8 selected as the workflow orchestration engine, two setup decisions are needed before any workflow development can begin: how to run the Camunda stack locally, and where to store the BPMN workflow definition files in the repository.

Camunda 8 is a multi-component stack — Zeebe (the workflow engine), Operate (monitoring and execution history), Tasklist (human task management), and Elasticsearch (history storage for Operate). A local development strategy must bring all of these components up reliably in a way that is reproducible across environments and does not diverge significantly from how the stack would run in production.

## Decision Drivers

- Local environment must be reproducible — cloning the repository and running a single command should bring up the full Camunda stack without manual steps
- The local topology should reflect how Camunda actually runs — a simplified single-binary distribution that hides component relationships would obscure how the system behaves in production
- BPMN workflow definitions are versioned artifacts that belong in the repository alongside the code that deploys and depends on them
- Workflow definitions are distinct from application code and infrastructure configuration — they deserve a dedicated location that makes their purpose immediately clear
- Structure should stay minimal — no directories created beyond what this decision actually requires

## Considered Options

- **Docker Compose with official Camunda configuration** — run the full Camunda 8 stack locally using Camunda's provided compose file
- **Camunda 8 Run** — Camunda's lightweight single-JAR distribution for local development
- **Direct local installation** — install each Camunda component natively on the developer machine

## Decision Outcome

Chosen option: "Docker Compose with official Camunda configuration", because it runs the full Camunda 8 stack as it is actually composed, is reproducible with a single command, and is the approach Camunda themselves recommend for local development.

BPMN workflow definition files will be stored in a `workflows/` directory at the repository root. This is the only directory introduced by this decision.

### Consequences

Running the full Camunda 8 stack locally via Docker Compose carries a heavier resource footprint than a single-service tool. Zeebe, Operate, Tasklist, and Elasticsearch together require meaningful memory allocation. This is a known and accepted tradeoff — the resource cost buys a local environment that behaves like production and exposes the full Camunda API surface, including Operate's step-level execution history that was a key requirement in ADR-003.

The `docker-compose.yml` file at the repository root starts the Camunda stack only. Any additional services introduced by later ADRs will run independently via their own native runtimes rather than being added to this compose file.

BPMN files in `workflows/` are automatically deployed to Zeebe on startup. The Docker Compose setup will include a mechanism — a startup script or dedicated compose service — that waits for Zeebe to be healthy and then deploys all workflow definitions via the Camunda REST API. This ensures the stack is always in a known state after `docker compose up`, regardless of whether volumes were preserved from a previous run. It also means any automated or E2E tests can rely on workflow definitions being present without a manual deploy step preceding them.

The job worker service — the separate process that polls Zeebe for automated service task jobs — is not part of this setup decision. It is an application-layer concern that will be addressed when the applications ADR is written.

## Why Each Option Was Considered

### Docker Compose with official Camunda configuration — chosen

Camunda publishes and maintains an official Docker Compose configuration for local development. Using it means running exactly the stack Camunda designs and tests against — Zeebe, Operate, Tasklist, and Elasticsearch together, wired correctly. This removes the risk of a hand-rolled compose configuration that diverges from supported topology. It also means that documentation, troubleshooting resources, and community answers are directly applicable to the local environment without translation.

Docker Compose also fits the project's future shape naturally. Additional services — the FastAPI application, the UI, the worker service — can be added to the same compose file incrementally, keeping a single command as the way to start the full stack regardless of how many components eventually exist.

### Camunda 8 Run — rejected

Camunda 8 Run is a single-JAR distribution designed to simplify local development by packaging the core components into one process. It starts faster and uses fewer resources than the full Docker Compose stack.

It is rejected because it does not include Operate. Operate is Camunda's monitoring component and the source of the step-level execution history and timestamps that were identified as requirements in [ADR-003](003-workflow-orchestration-engine.md) — the foundation for current-state display and future DORA-style metrics. Running without Operate during local development would mean developing and testing against a runtime that is missing a capability the production system depends on.

### Direct local installation — rejected

Installing Zeebe, Operate, Tasklist, and Elasticsearch natively on a developer machine is brittle and not reproducible. Version management becomes a manual concern, and the setup cannot be expressed as code that another environment can replicate. There is no meaningful advantage over Docker Compose that would justify this approach.
