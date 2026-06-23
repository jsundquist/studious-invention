# Frontend Architecture

## Status
Accepted

## Date
2026-06-23

## Context and Problem Statement

The golden path tool requires both a user-facing interface and an API layer that communicates with Camunda. A structural decision is needed on whether these concerns live in a single combined application or as two separate applications with distinct responsibilities.

## Decision Drivers

- The UI must be feature-rich and capable of growing as the product evolves — it needs to support workflow visualization, human task interaction, and a catalog of software artifacts
- Separate concerns map to how platform teams are structured in real organizations — a UI team and an API team owning their respective layers independently
- Each layer should be deployable and evolvable independently without requiring changes to the other

## Considered Options

- **Separate applications** — a dedicated UI application and a dedicated API application, each with their own technology stack, communicating over HTTP
- **Combined application** — a single application that owns both the UI and the API layer

## Decision Outcome

Chosen option: "Separate applications", because it allows each layer to be built with the technology best suited to its purpose, mirrors how real platform organizations structure ownership, and keeps each application independently evolvable without coupling their technology choices or deployment lifecycles.

The UI application is responsible for rendering the developer-facing surface — the catalog, workflow visualization, and human task interactions. The API application is responsible for all business logic and Camunda communication. The UI communicates with the API exclusively over HTTP. Neither application has a direct relationship with the other's internal concerns.

What each application is built with is addressed in subsequent ADRs.

### Consequences

Two separate applications means two runtimes to start locally, two directories in the monorepo, and two distinct technology stacks to maintain. For a solo project this is more moving pieces than a combined app, but the tradeoff is accepted — the separate ownership model is the point, not an accidental complexity.

The boundary between the two applications must be kept explicit. Business logic and Camunda communication belong in the API layer. The UI layer should not accumulate domain logic that belongs on the API side. As the project grows, discipline around this boundary is what keeps the architecture honest.

## Why Each Option Was Considered

### Separate applications — chosen

Separate applications allow each layer to use the technology most appropriate to its purpose without compromise. Each can be built with whatever best serves its responsibilities — the UI optimized for the developer-facing surface, the API optimized for business logic and Camunda communication.

This structure also reflects how platform engineering teams operate in practice. The UI and API are owned and deployed independently, with a clear HTTP contract between them.

### Combined application — rejected

A combined application simplifies local development and reduces the number of things to start and maintain. Frameworks that combine UI and API concerns in a single project handle this well.

The tradeoff is that a combined application couples the technology choices for the UI and API into a single decision. The best choice for a rich, flexible UI is not necessarily the best choice for business logic and Camunda communication, and vice versa. Accepting a combined application means accepting a compromise on one side or the other, which is not a tradeoff this project needs to make.
