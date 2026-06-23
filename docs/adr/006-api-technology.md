# API Technology

## Status
Accepted

## Date
2026-06-23

## Context and Problem Statement

The API layer sits between the UI and Camunda, owning all business logic, workflow operations, and communication with the Camunda stack. A framework is needed that can expose a clean HTTP interface, handle concurrent requests without blocking, and produce a well-structured, self-documenting API that is easy to work with, test, and maintain.

## Decision Drivers

- **Automatic OpenAPI generation** — the API spec must be derived directly from the code, not maintained as a separate document that can drift out of sync
- **Type safety** — strong typing must be enforced at the API boundary to catch malformed requests before they reach business logic
- **Non-blocking** — the framework must handle concurrent requests without blocking, whether through async functions, goroutines, or the runtime's native concurrency model
- **Extensible by default** — the core framework should be lean; additional capabilities should be added explicitly through libraries or configuration rather than bundled by default
- **Community momentum** — the framework must be actively maintained, show healthy issue resolution, and have growing relevance in the current industry landscape

## Considered Options

- **FastAPI** — modern async Python framework with automatic OpenAPI generation and Pydantic-based validation
- **Django REST Framework** — mature Python framework with a broad feature set built on top of Django
- **Spring Boot** — the dominant Java framework for building production-grade APIs
- **Gin** — lightweight, high-performance Go framework with growing adoption in platform engineering
- **Express** — minimal Node.js framework
- **Ruby on Rails** — full-featured web framework with strong convention over configuration
- **Rust (Actix-web / Axum)** — high-performance systems-oriented web frameworks

## Comparison Matrix

Metrics sourced from GitHub repositories as of June 23, 2026 via GitHub API. PR and issue activity covers the 30-day period May 23 – June 23, 2026. OpenAPI generation capability sourced from official documentation and independent benchmarking research.

| Framework | Auto OpenAPI | Type Safety | Non-blocking | Lean Core | Merged PRs (30d) | Open PRs | Issues Opened (30d) | Issues Closed (30d) | Latest Release |
|-----------|-------------|-------------|--------------|-----------|-----------------|----------|--------------------|--------------------|----------------|
| FastAPI | ✓ Derived from type annotations | ✓ Pydantic runtime validation | ✓ Async-native | ✓ | 64 | 100 | 8 | 9 | Jun 20, 2026 |
| Django REST | ~ Requires drf-spectacular config | ~ No native type annotations | ~ Async incomplete, ORM sync | ✗ Bundles ORM, admin, templates | 4 | 49 | 5 | 2 | Mar 24, 2026 |
| Spring Boot | ~ Annotation-driven via SpringDoc | ✓ Java compile-time | ~ Requires WebFlux for reactive | ✗ Heavy auto-configuration | 23 | 43 | 69 | 85 | Jun 10, 2026 |
| Gin | ✗ Comment-based via swaggo CLI | ✓ Go compile-time | ✓ Goroutine-based concurrency | ✓ | 12 | 100 | 13 | 6 | Feb 28, 2026 |
| Express | ✗ Fragmented, unmaintained libs | ~ Optional via TypeScript | ✓ Node.js event loop | ✓ | 8 | 100 | 13 | 12 | Dec 1, 2025 |
| Ruby on Rails | ✗ Manual via rswag | ✗ Dynamic typing | ✗ Synchronous by default | ✗ Full MVC stack | 83 | 100 | 8 | 6 | Mar 24, 2026 |
| Actix-web | ~ Derive macros via paperclip | ✓ Rust compile-time | ✓ Async-native (Tokio) | ✓ | 28 | 33 | 6 | 5 | Jun 22, 2026 |
| Axum | ~ Derive macros via utoipa | ✓ Rust compile-time | ✓ Async-native (Tokio) | ✓ | 12 | 33 | 7 | 3 | Apr 14, 2026 |

**Legend:** ✓ Fully satisfies | ~ Partially satisfies | ✗ Does not satisfy

## Decision Outcome

Chosen option: "FastAPI", because it is the only framework under consideration that fully satisfies all five decision drivers — automatic OpenAPI generation derived from code, runtime type safety via Pydantic, async-native non-blocking request handling, a lean extensible core, and strong community momentum backed by real activity data: 64 merged PRs and 9 issues closed against 8 opened in the 30 days prior to this decision, with a release on June 20, 2026. The 100 open PRs reflect active incoming contributions under review, not unresolved problems.

Notable adopters include Microsoft (ML services integrated into Windows and Office), Netflix (crisis management orchestration framework Dispatch), and Uber (REST servers for the Ludwig ML framework).

### Consequences

FastAPI generates an OpenAPI spec and interactive documentation automatically from Python type annotations and Pydantic models. The spec is always in sync with the code because it is derived from it — no separate documentation effort is required and no drift is possible. This spec is available at `/docs` (Swagger UI) and `/redoc` immediately without configuration.

FastAPI does not include an ORM or database layer. Persistence is handled separately and is the subject of its own ADR. This is intentional — the database choice should not be coupled to the framework choice.

FastAPI's raw throughput (~8,000–12,000 requests/second) is lower than Gin (~120,000 requests/second) and Rust-based frameworks in pure benchmark conditions. For an API layer whose primary operations are orchestrating calls to Camunda and a database rather than pure computation, this tradeoff is accepted. The performance gap narrows significantly under database-heavy workloads where async I/O provides meaningful parallelism.

## Why Each Option Was Considered

### FastAPI — chosen

FastAPI was built to address the gaps in older Python API frameworks. It is async-native, generates an OpenAPI spec automatically from function signatures and Pydantic models, and enforces type safety at the API boundary. It has the most active maintenance record of any framework evaluated — 64 merged PRs with 9 issues closed against 8 opened in the past 30 days, and a release on June 20, 2026 — and is seeing adoption at companies including Microsoft, Netflix, and Uber.

### Django REST Framework — rejected

Django REST Framework is mature and capable. OpenAPI generation is available via drf-spectacular but requires explicit schema configuration rather than being derived from type annotations. More significantly, Django's async support is incomplete — the ORM and much of the middleware stack remain synchronous, which creates friction for an API layer handling concurrent external calls. Django also bundles an ORM, admin panel, and templating engine that are not relevant to this use case, failing the lean core requirement.

### Spring Boot — rejected

Spring Boot has genuine strengths — Java's type system is robust, SpringDoc generates OpenAPI from annotations, and the framework has extensive enterprise adoption. It is rejected because the OpenAPI generation is annotation-driven rather than derived automatically from types, requiring explicit decoration of every endpoint and model. Spring Boot's auto-configuration and application context add significant framework weight that is better suited to large multi-team applications than a focused API layer. It fails both the lean core and automatic OpenAPI generation requirements.

### Gin — rejected

Gin is a strong and fast framework with healthy Go concurrency via goroutines and compile-time type safety. It fails the automatic OpenAPI generation requirement — documentation requires the swaggo CLI to parse comment-based annotations written alongside the code. This approach is fundamentally different from deriving the spec from the type system itself, and means the spec and the implementation can diverge. With 12 merged PRs in the past 30 days it is less actively developed than FastAPI over the same period.

### Express — rejected

Express is minimal and non-blocking via the Node.js event loop. It fails the automatic OpenAPI generation requirement — the ecosystem of OpenAPI tooling for Express has fragmented significantly, with no clear standard and several widely used packages no longer actively maintained. Type safety is optional via TypeScript rather than enforced at the framework level. The most recent release (December 2025) also lags the other options.

### Ruby on Rails — rejected

Rails fails three of the five decision drivers. OpenAPI generation requires rswag with manual maintenance rather than derivation from code. Ruby is dynamically typed, offering no enforced type safety at the API boundary. Rails is synchronous by default — async support is not a first-class concern in the framework. Rails API mode reduces the bundled features compared to a full Rails install, but the framework still carries conventions oriented toward full web applications rather than a focused API layer.

### Rust (Actix-web / Axum) — rejected

Both Actix-web and Axum are async-native, and Rust's type system is among the strongest of any language evaluated. Performance benchmarks place Rust frameworks at the top of raw throughput. OpenAPI generation is available via utoipa (Axum) and paperclip (Actix-web) using derive macros — closer to FastAPI's approach than Gin's comment-based annotations, but still requiring explicit derive annotations on every model rather than being fully automatic.

Rust is rejected on two technical grounds. First, neither Actix-web nor Axum provides truly automatic OpenAPI generation — both require explicit derive macro annotations on every model, meaning the spec is not fully derived from the type system the way FastAPI derives it from standard type annotations. Second, Axum remains at v0.8.x with v0.9 breaking changes actively in development, introducing stability uncertainty that is not present in the other options evaluated. Community activity is also modest relative to the project's maturity — Axum closed only 3 issues against 7 opened in the past 30 days.

## References

- [FastAPI GitHub Repository](https://github.com/tiangolo/fastapi) — PR activity, issue activity, release cadence, notable adopters
- [Gin GitHub Repository](https://github.com/gin-gonic/gin) — PR activity, issue activity, release cadence
- [Django REST Framework GitHub Repository](https://github.com/encode/django-rest-framework) — PR activity, issue activity, release cadence
- [Spring Boot GitHub Repository](https://github.com/spring-projects/spring-boot) — PR activity, issue activity, release cadence
- [Express GitHub Repository](https://github.com/expressjs/express) — PR activity, issue activity, release cadence
- [Ruby on Rails GitHub Repository](https://github.com/rails/rails) — PR activity, issue activity, release cadence
- [Actix-web GitHub Repository](https://github.com/actix/actix-web) — PR activity, issue activity, release cadence
- [Axum GitHub Repository](https://github.com/tokio-rs/axum) — PR activity, issue activity, release cadence
- [FastAPI vs Express vs Gin 2026 — DevTools Research](https://devtoolswatch.com/en/fastapi-vs-express-vs-gin-2026) — OpenAPI generation comparison, performance benchmarks
- [FastAPI vs Gin vs Spring Boot — amitk.io](https://www.amitk.io/rest-api-comparison-fastapi-gin-springboot/) — async support, type safety, extensibility comparison
