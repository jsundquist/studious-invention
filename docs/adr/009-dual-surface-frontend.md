# Dual-Surface Frontend Strategy

## Status
Accepted

## Date
2026-07-10

## Context and Problem Statement

The project was originally planned around a single standalone dashboard (`apps/ui`) as the only developer-facing surface. A new opportunity has arisen to also produce a Backstage frontend plugin — a complementary deliverable that targets the large number of organizations already running Backstage as their internal developer portal. Both surfaces serve the same purpose (exposing golden path workflow status to developers) but through different distribution mechanisms.

A structural decision is needed on how to support both surfaces without duplicating the backend or fragmenting the API layer.

## Decision Drivers

- Both surfaces must show developers the same workflow data without inconsistency
- The API layer already enforces that no Camunda internals leak to any frontend — this must remain true for both surfaces
- The standalone UI is the primary development surface; the Backstage plugin is a parallel deliverable, not a replacement
- The plugin must be installable and verifiable inside a real Backstage instance without publishing to npm
- ADR-001 rejected Backstage as the *project foundation* — that decision is not revisited here; this ADR concerns adding a Backstage plugin as a *distribution target*

## Considered Options

- **Single standalone UI only** — no Backstage plugin; only `apps/ui` is produced
- **Dual surface: standalone UI + Backstage frontend plugin** — both surfaces consume `apps/api` exclusively
- **Backstage only** — replace the standalone UI with the Backstage plugin

## Decision Outcome

Chosen option: "Dual surface: standalone UI + Backstage frontend plugin", because it broadens the deliverable to cover both the standalone and enterprise portal audiences without any changes to the backend architecture. The API layer is already a clean abstraction over Camunda; both surfaces simply become two consumers of the same HTTP API.

The standalone UI (`apps/ui`) remains the primary development surface. The Backstage plugin (`apps/backstage-plugin`) is a parallel deliverable that installs into any Backstage instance. A minimal Backstage host app (`apps/backstage`) is added to the monorepo to enable end-to-end verification without publishing the plugin to npm.

The Backstage plugin targets `apps/api` via Backstage's built-in `proxy-backend` plugin rather than calling `apps/api` directly. This proxy is configured in `app-config.yaml` and is standard Backstage practice for external API integration. No custom backend plugin is required.

### Consequences

Three frontend-adjacent directories now exist: `apps/ui`, `apps/backstage-plugin`, and `apps/backstage`. The first is the application, the second is the plugin package, and the third is the host used only to verify the plugin during development.

The Backstage host app adds significant dependency weight to the monorepo. It is a development and verification tool only — it is not intended to be deployed or maintained as a production Backstage instance.

The `apps/api` surface does not change. No Backstage-specific endpoints are added. The proxy configuration in `app-config.yaml` is the only Backstage-specific artifact required outside of `apps/backstage-plugin` and `apps/backstage`.

## Why Each Option Was Considered

### Single standalone UI only — not chosen

This was the original scope. It remains a valid delivery, but it foregoes the Backstage audience entirely. Given that many organizations use Backstage as their developer portal, producing only a standalone UI limits adoption and reduces the portfolio value of the deliverable.

### Dual surface: standalone UI + Backstage frontend plugin — chosen

The API layer was already designed as an abstraction over Camunda with no Camunda internals leaking to any consumer. Adding a second consumer is architecturally free — no backend changes are required. The standalone UI continues as-is. The Backstage plugin is additive.

This option also produces two distinct portfolio artifacts: a from-scratch IDP (the standalone surface) and a Backstage plugin integration (the plugin surface). These demonstrate complementary skills.

### Backstage only — rejected

Replacing the standalone UI with a Backstage plugin would require any user of the tool to be running Backstage, which is a significant operational prerequisite. It would also mean the product has no independent identity — it would be a Backstage add-on rather than a product that can also appear in Backstage. The standalone UI is kept for this reason.

This option was also rejected by ADR-001, which established that the project would not be built on top of Backstage as its foundation.
