# Scaffold Repository

## What happens

A GitHub repository is created under the company organization using the service name you provided when starting this workflow. The following are applied automatically:

- Branch protection on `main`: requires pull request reviews, passing CI checks, and no direct pushes
- Standard repository labels (bug, enhancement, security, dependencies)
- Default `.gitignore` appropriate for the service type
- `CODEOWNERS` file assigning the owning team

## What you need to provide

The following inputs are required when starting the Create workflow:

- **Service name** — used as the repository name (kebab-case, e.g. `payments-api`)
- **Service description** — a one-sentence description written to the repository About field
- **Owning team** — the GitHub team that will be assigned as code owner

## What to expect

Once this step completes, the repository is available at `github.com/<org>/<service-name>`. You will have write access immediately. The `main` branch exists but is empty — code is added in the Scaffold Project step.
