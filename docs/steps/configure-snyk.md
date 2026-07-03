# Configure Snyk

## What happens

The repository is imported into Snyk for continuous dependency vulnerability scanning. The following are configured automatically:

- Snyk monitors the dependency manifest (`pyproject.toml`, `package.json`, etc.) for known vulnerabilities
- GitHub pull request checks enabled — Snyk blocks merges if new critical or high vulnerabilities are introduced
- Automated fix pull requests enabled for patch-level upgrades

## What you need to provide

Nothing. This step is fully automated.

## What to expect

Snyk begins scanning immediately after import. An initial vulnerability report is generated and visible in the Snyk dashboard under the company organization. Existing vulnerabilities in the scaffold template are reviewed and accepted or remediated before this workflow reaches Phase 4.

## Relevance to later steps

During Phase 4 (Resolve Security Findings), the workflow checks whether any critical or high severity vulnerabilities exist. If they do, the workflow waits until they are resolved — either by upgrading the affected dependency or applying a Snyk-suggested fix — before allowing production deployment.
