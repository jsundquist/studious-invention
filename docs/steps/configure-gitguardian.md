# Configure GitGuardian

## What happens

The repository is added to GitGuardian monitoring for secret detection. GitGuardian scans every commit for accidentally committed secrets including API keys, tokens, passwords, and private certificates.

- Real-time monitoring is enabled on push
- GitHub pull request checks enabled — GitGuardian flags any PR that introduces a detected secret
- Alerts are routed to the security team

## What you need to provide

Nothing. This step is fully automated.

## What to expect

GitGuardian performs a historical scan of the repository on import. Because the repository was just scaffolded, no secrets should be present. If any are detected, the security team is alerted immediately.

## Important: keep secrets out of code

GitGuardian detects secrets but cannot remove them. If a secret is committed:

1. Treat the secret as compromised immediately — rotate it regardless of whether it was pushed to a remote
2. Remove the secret from the code and all git history (git history rewrite or repo recreation may be required)
3. Use the secrets management setup (configured later in this phase) to store secrets properly

## Relevance to later steps

During Phase 4 (Resolve Security Findings), the workflow checks whether any active secret detections exist. If they do, the workflow waits until the repository is clean before allowing production deployment.
