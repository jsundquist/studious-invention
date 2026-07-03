# Request Security Sign-off

## What happens

A final security sign-off is requested from the security team. This step is reached only after all three security tool thresholds (SonarCloud, Snyk, GitGuardian) have been cleared. The security team performs a final review before production deployment is allowed.

The reviewer evaluates:

- All Phase 4 security tool thresholds are clear (confirmed automatically before this task is created)
- Any steps skipped earlier in the workflow are reviewed — skips in the initial security review (Phase 2), unit tests, or E2E tests are flagged here for the reviewer's awareness
- Any Snyk ignores added during threshold resolution are reviewed and accepted or rejected
- The overall security posture of the service is acceptable for production traffic

## What you need to provide

No action is required from the developer at this step. The security team performs the review independently using the findings dashboards from SonarCloud, Snyk, and GitGuardian.

If the security team has questions or requests changes, they will contact the owning team directly. Once satisfied, they complete this task in the workflow.

## Approval outcomes

| Outcome | Meaning |
|---|---|
| **Approved** | Security team confirms the service is ready for production deployment. |
| **Skipped** | Sign-off is bypassed. A reason must be provided. The skip is permanently recorded in the workflow history and visible in compliance reporting. |

## Note

This is the final gate before production. All prior security tool thresholds being clear is a prerequisite, not a substitute for this review. The security team's sign-off represents human judgement on the overall posture, not just automated check results.
