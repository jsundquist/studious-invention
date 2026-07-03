# Scaffold Project

## What happens

A company-standard project template is generated and pushed to the repository created in the previous step. The scaffold includes:

- Standard directory structure for a backend API service
- `Dockerfile` and `.dockerignore` following company container standards
- CI/CD pipeline configuration (GitHub Actions workflows for build, test, lint, and deploy)
- Pre-configured linting and formatting rules
- `pyproject.toml` / `package.json` (depending on language) with standard dependencies
- A minimal health check endpoint at `GET /health`
- `README.md` pre-populated with service name, description, and local development instructions

## What you need to provide

- **Language / runtime** — selected when starting the workflow (e.g. Python, Node.js). Determines which template is used.

## What to expect

Once this step completes, the repository contains a runnable hello-world service. You can clone it immediately and begin development. The CI/CD pipeline is active — any pull request will trigger build and test checks automatically.

## Note on CI/CD

The pipeline is configured but not yet connected to a deployment target. Deployment configuration is completed during the infrastructure provisioning steps later in this phase.
