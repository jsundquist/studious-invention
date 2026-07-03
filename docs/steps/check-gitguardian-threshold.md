# Check GitGuardian Threshold

## What happens

The GitGuardian incident report for the repository is checked automatically. The threshold is zero tolerance — **any active secret detection blocks this step**.

If no incidents are active, this step completes automatically and the workflow continues.

If active incidents exist, **the workflow pauses here** and waits until all incidents are resolved. The workflow resumes automatically once GitGuardian reports no active incidents.

## What to do if the threshold is breached

**Treat any detected secret as compromised immediately**, regardless of whether it was pushed to a remote or is visible to others.

For each active incident:

1. **Rotate the secret** — revoke the exposed credential and generate a new one. Do this first, before anything else.
2. **Remove the secret from git history** — simply deleting the file is not enough; the secret exists in git history. Use `git filter-repo` to rewrite history, or contact the platform team if you need assistance.
3. **Store the new secret correctly** — use the secrets management system configured in Phase 1. Reference it via the appropriate environment variable at runtime.
4. **Resolve the incident in GitGuardian** — mark the incident as resolved after rotating and removing the secret.

Once all incidents are resolved, GitGuardian updates its status and the workflow continues automatically.

## Note

GitGuardian monitors all future commits. To prevent recurrence, never hardcode credentials, tokens, or keys in source code. Use environment variables backed by secrets management.
