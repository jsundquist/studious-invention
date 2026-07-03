# Configure SonarCloud

## What happens

A SonarCloud project is created and linked to the GitHub repository. The following are configured automatically:

- GitHub integration enabled so SonarCloud analysis runs on every pull request
- Quality gate set to the company standard (no new critical or high issues, coverage must not drop below threshold)
- Pull request decoration enabled — SonarCloud posts a summary comment on each PR with findings

## What you need to provide

Nothing. This step is fully automated.

## What to expect

After this step, SonarCloud begins analyzing code on the next push or pull request. The quality gate result is visible in GitHub pull requests and at `sonarcloud.io` under the company organization.

## Relevance to later steps

The quality gate status is checked during Phase 4 (Resolve Security Findings). If your code has new critical or high issues at that point, the workflow will wait until they are resolved and the quality gate passes before allowing production deployment.
