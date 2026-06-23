# Monorepo vs Polyrepo

## Status
Accepted

## Date
2026-06-23

## Context and Problem Statement

This project may span multiple distinct apps — a workflow engine, and some combination of API and UI for interacting with it. The exact shape of those apps is not yet decided (separate services, or a single unified app). A structural decision is needed for how code, infrastructure, and workflow definitions are organized and versioned.

## Decision Drivers

- Incremental growth is expected — the structure should accommodate new components without requiring a repository reorganization
- Cross-cutting changes should be atomic — one commit, one PR, regardless of how many layers they touch
- CI should only run what changed — path filtering scopes pipelines to what was actually touched
- Solo project: polyrepo coordination overhead has no benefit at this scale

## Considered Options

- **Monorepo with path-filtered CI** — all apps, infrastructure, and workflow definitions in a single repository with CI scoped by path
- **Polyrepo** — one repository per app or concern, coordinated separately

## Decision Outcome

Chosen option: "Monorepo with path-filtered CI", because it keeps cross-cutting changes atomic, reduces operational overhead for a solo project, and makes it easier to introduce new components incrementally without restructuring.

### Consequences

A monorepo requires discipline to keep CI path filters accurate as the structure evolves — a misconfigured filter can silently skip a pipeline that should have run. The tradeoff is accepted because the alternative introduces coordination overhead that provides no value here.

The day-to-day benefit is a single source of truth for the entire system. A single `git log` tells the full story of how the project evolved — a UI change, an API change, and the infrastructure update that supported both appear as one cohesive commit or PR rather than three separate threads to mentally stitch together. Searching across layers, understanding how a change in one place rippled into another, and onboarding someone new to the project are all simpler when everything is in one place. Internal structure within the monorepo is intentionally deferred until individual app decisions are made in later ADRs.

## Why Each Option Was Considered

### Monorepo with path-filtered CI — chosen

A single repository is the natural fit when apps share infrastructure, workflow definitions, and a development lifecycle. Cross-cutting changes — for example, a contract change that touches both the API and the UI — can be made, reviewed, and reverted as a single unit. Path-filtered CI ensures that unrelated pipelines don't run on every push, preserving the speed benefit that polyrepo is often assumed to provide.

### Polyrepo — rejected

Separate repositories make sense when teams need independent release cadences, strict access boundaries, or isolated dependency graphs. None of those apply here.

In practice, a polyrepo setup for this project would mean cloning two or three repositories just to understand how the system fits together. A change to how the API communicates with the workflow engine — something that likely touches the API code, the UI that consumes it, and possibly infrastructure configuration — would require coordinated pull requests across multiple repositories, landed in the right order, with no single view of the full change. Version drift becomes a real problem too: without a shared repository enforcing consistency, it becomes easy for the UI to silently fall out of sync with the API contract it depends on.

For a solo project at this scale, that overhead is friction with no payoff. The access boundaries and release isolation that justify polyrepo in large organizations are not constraints here. A monorepo removes the coordination tax entirely.
