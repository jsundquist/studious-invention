# Branchline

An opinionated golden path tool that guides developers through the full lifecycle of a software artifact — from creation through to decommissioning. The golden path is the default branch; teams can branch off it knowingly, trading guardrails for autonomy. Built as a learning project to deepen skills in workflow orchestration, API design, and modern developer platform patterns.

Available as a standalone dashboard (`apps/ui`) and as a Backstage frontend plugin (`apps/backstage-plugin`).

## System Requirements

- [Docker](https://docs.docker.com/get-docker/) with Docker Compose

## Quick Start

```bash
docker compose up --detach
```

This starts the Camunda workflow stack. See [docs/local-development.md](docs/local-development.md) for port references, UI access, and troubleshooting tips.

```bash
docker compose down
```


## Documentation

- [docs/architecture.md](docs/architecture.md) — system overview and component responsibilities
- [docs/local-development.md](docs/local-development.md) — local environment reference
- [docs/adr/](docs/adr/) — architectural decision records
