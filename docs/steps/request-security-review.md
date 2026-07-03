# Request Security Review

## What happens

An initial security review is assigned to the security team. This review runs in parallel with the architecture review and evaluates the service's security posture at the design and setup level — before development has started.

The reviewer evaluates:

- Authentication and authorization design — how will the service authenticate callers, and what access controls exist
- Data classification — what data the service handles and whether handling meets company policy
- Network exposure — whether the service is appropriately scoped to internal traffic or requires external exposure
- Threat model — known attack surfaces and mitigations planned
- Compliance considerations — whether the service touches data subject to regulatory requirements (PII, financial data, etc.)

## What you need to provide

Before this review, share with the security team:

- **Authentication approach** — how callers authenticate (API key, JWT, mTLS, etc.)
- **Data classification** — what categories of data the service stores or processes
- **Network exposure plan** — internal only, or externally accessible
- **Threat model** (if available) — a brief description of the main risks and your mitigations

A formal threat model document is not required at this stage. A written summary is sufficient.

## Approval outcomes

| Outcome | Meaning |
|---|---|
| **Approved** | Security design meets company standards. Development may proceed. |
| **Skipped** | Review was bypassed. A reason must be provided and is recorded. Development proceeds but the skip is visible in the workflow history and flagged for the final security sign-off in Phase 4. |

## Note

This is a design-level review only. Code-level security findings (dependency vulnerabilities, static analysis issues, secret detection) are addressed separately in Phase 4.
