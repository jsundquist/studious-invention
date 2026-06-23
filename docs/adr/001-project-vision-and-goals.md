# Project Vision and Goals

## Status
Accepted

## Date
2026-06-23

## Context and Problem Statement

Developers lack a consistent, repeatable path for taking a software artifact from concept to production — and through its full operational lifecycle. Without a paved road, each team reinvents toolchain integration, sequencing, and standards, leading to inconsistency and cognitive overhead. The result is that "how we ship things" becomes implicit tribal knowledge rather than a documented, automatable process.

This project exists to provide opinionated, lifecycle-aware workflows that guide a developer through three phases for any software artifact:

1. **Create** — from concept to a running production service
2. **Update** — repeatable, safe path for changes to a live artifact
3. **Decommission** — structured teardown that leaves no orphaned resources or undocumented gaps

## Decision Drivers

- Developers need a single, consistent entry point for each lifecycle phase regardless of which toolchain services are in use
- Toolchain integrations (security scanning, observability, CI/CD, etc.) must be pluggable — the set of integrations is not fixed and will grow over time
- The project is also a deliberate learning vehicle: an opportunity to deepen skills with technologies intentionally different from prior work, and to produce a portfolio piece that demonstrates end-to-end system design thinking
- Must be coherent enough as a portfolio piece to stand on its own, not just as a tutorial exercise

## Considered Options

- **Build a golden path / IDP tool** — opinionated lifecycle workflows with pluggable integrations, backed by a workflow engine
- **Build a documentation site or runbook generator** — static or templated docs rather than executable workflows
- **Contribute to an existing IDP (Backstage, Port, Cortex)** — extend an established platform rather than building from scratch

## Decision Outcome

Chosen option: "Build a golden path / IDP tool", because it is the only option that produces executable, repeatable workflows (not just documentation), allows deep integration with the chosen technology stack, and results in a portfolio artifact that demonstrates end-to-end system design.

### Consequences

Committing to building from scratch means accepting higher implementation effort and no existing plugin ecosystem. The tradeoff is full architectural control and a scope that meaningfully exercises the learning goals. The primary risk is unbounded scope — the integration surface is intentionally open-ended, so discipline is required to keep each integration modular and additions deliberate rather than accumulated.

## Why Each Option Was Considered

### Build a golden path / IDP tool — chosen

This is the only option that produces executable, repeatable workflows rather than passive documentation. Building from scratch gives full control over architecture and technology choices, which directly serves the learning goals. The lifecycle model (create / update / decommission) provides natural scope boundaries.

### Build a documentation site or runbook generator — rejected

Runbooks are passive. Developers still execute steps manually and inconsistently, which does not solve the core problem. A documentation site also provides no meaningful opportunity to design or exercise the target architecture.

### Contribute to an existing IDP (Backstage, Port, Cortex) — rejected

Extending an existing platform would provide immediate access to a plugin ecosystem and existing users, but the interesting architectural decisions are already made. This option does not serve the learning goals and would produce a portfolio piece that is largely someone else's design.
