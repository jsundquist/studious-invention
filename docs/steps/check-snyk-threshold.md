# Check Snyk Threshold

## What happens

The Snyk vulnerability report for the service is checked automatically. The company threshold requires:

- Zero critical severity vulnerabilities
- Zero high severity vulnerabilities

Medium and low severity vulnerabilities do not block this step.

If the threshold is met, this step completes automatically and the workflow continues.

If the threshold is breached, **the workflow pauses here** and waits until Snyk reports no critical or high vulnerabilities. The workflow resumes automatically once the threshold is met.

## What to do if the threshold is breached

1. Open Snyk and review the specific vulnerabilities blocking the threshold
2. For each critical or high finding, choose one of:
   - **Upgrade the dependency** — Snyk shows the minimum version that fixes the vulnerability
   - **Apply a Snyk fix PR** — Snyk can open a pull request automatically for many vulnerabilities
   - **Add a Snyk ignore** — only if the vulnerability is a false positive or genuinely not exploitable in your context; requires a written justification reviewed by the security team
3. Merge the fix and push to `main`
4. Snyk re-scans automatically on push
5. Once the threshold is met, the platform detects the change and the workflow continues

## Note

You do not need to take any action in this workflow UI. Fix the dependencies, push the changes, and the workflow resumes on its own.
