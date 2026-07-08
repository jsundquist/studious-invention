# UI Technology

## Status
Accepted

## Date
2026-07-08

## Context and Problem Statement

ADR-005 established that the UI is a separate application communicating exclusively over HTTP with the FastAPI layer. The technology for that application was explicitly deferred. This ADR makes that decision.

The UI has four primary responsibilities:

1. **Artifact catalog** — display all workflow instances, their lifecycle phase, and current execution status
2. **Workflow visualization** — render the steps of a golden path dynamically from data returned by the workflow definition API, not from hardcoded structure
3. **Human task interactions** — surface pending user tasks (approval gates) and allow a developer to complete them from the UI
4. **Near-real-time state** — reflect current workflow execution state without requiring a manual page refresh

This is an internal developer tool. Server-side rendering for SEO, offline support, and mobile-first design are not requirements.

## Decision Drivers

- **Component ecosystem** — the framework must have a mature ecosystem of UI components suited to data-heavy internal tooling (tables, status indicators, form dialogs, navigation)
- **TypeScript support** — first-class TypeScript integration is required; type safety at the API boundary and through the component tree catches integration errors early
- **Developer familiarity** — the framework should minimize friction on UI concerns so focus remains on the domain-specific work: workflow visualization and API integration
- **Portfolio transferability** — components and patterns should transfer to related future projects in the same problem space

## Options Considered

### React + Vite + TypeScript

The dominant single-page application framework. Vite replaces Create React App as the build tool — it provides fast HMR, native ESM, and a straightforward configuration model. TypeScript is the standard layer on top. The React ecosystem is the largest in the frontend space, which means the widest selection of compatible libraries and the highest recognizability in a portfolio context.

**Why it was chosen:** React's component model maps naturally to the UI requirements. The artifact catalog is a list of items that update independently. The workflow visualization is a tree of components driven by API data. Human task forms are isolated interactions. React's composability handles all of these without architectural friction. Vite keeps the development experience fast and the configuration minimal.

### Next.js

React-based with an opinionated routing and rendering model. Adds server-side rendering, server components, and file-based routing on top of React.

**Why it was not chosen:** SSR features are wasted on an internal tool with no SEO requirements. The added conventions (app router, server vs. client components, route handlers) introduce complexity that this project does not benefit from. Next.js is appropriate when SSR or static generation is a genuine requirement — neither applies here.

### SvelteKit

A compiler-based framework with a simpler reactivity model and smaller runtime bundle. Growing adoption, particularly for performance-sensitive applications.

**Why it was not chosen:** The workflow visualization and API integration work is the interesting part of this project. Learning a new framework at the same time adds friction without a clear payoff given the existing React familiarity. SvelteKit remains a strong candidate for future projects where the framework itself is part of the learning goal.

### Vue 3 + Vite

A component framework with a clean composition API and strong TypeScript integration. Widely used in enterprise internal tooling.

**Why it was not chosen:** Same reasoning as SvelteKit — the framework itself would become part of the learning surface at a point where the goal is to move through the UI layer and focus on the workflow visualization problem.

## Decision

**React 19 + Vite + TypeScript** for the application framework and build tooling.

**React Router v7** for client-side routing. It is the established standard for React SPAs, handles nested routes cleanly, and does not introduce the server rendering conventions that come with framework-mode usage. Routes are defined explicitly in a route configuration — not via file-based conventions.

**MUI (Material UI) v7** as the component library. MUI provides a complete set of production-quality components suited to internal tooling: data grids for the catalog view, status chips for workflow state, dialogs for human task interactions, and a navigation structure for the overall shell. The developer has existing MUI familiarity, which keeps the focus on domain problems rather than component API exploration. MUI ships its own styling engine (Emotion); Tailwind CSS is not used and would conflict.

**Raw fetch + React state** for data fetching. Each API resource has a dedicated module under `src/api/` containing typed fetch functions. Custom hooks under `src/hooks/` wrap these functions with `useState` and `useEffect` to manage loading and error state per component. For instance status — the one view that requires background refresh — a shared `usePolling` hook encapsulates the `setInterval` / cleanup / stale-response logic in a single reusable place rather than repeating it across components.

This approach keeps every data fetching call explicit and traceable, avoids adding a library whose mental model (query keys, stale time, cache invalidation) would need to be learned alongside the rest of the stack, and produces code that transfers directly to other React projects including Backstage plugins (which use their own `useApi` / `ApiRef` data fetching pattern rather than third-party libraries).

The application lives at `apps/ui/` in the monorepo. It runs on port 3000 during local development (ports 8000, 8080, 8081, and 8082 are reserved for FastAPI and the Camunda stack). It communicates exclusively with the FastAPI layer over HTTP and has no direct knowledge of Camunda internals.

## Consequences

- MUI's opinionated styling system (Emotion) is the styling layer for the entire application. Custom styles use MUI's `sx` prop or `styled()` utility rather than a separate CSS framework.
- All API calls go through typed fetch functions in `src/api/`, never inline `fetch` calls scattered through components. This keeps the FastAPI contract in one place and makes it easy to update when endpoints change.
- The `usePolling` hook is the single place where interval-based refresh logic lives. Components that need live data import it rather than implementing their own timers.
- TanStack Query (React Query) was considered for server state management. It was deferred — not rejected — because its cache invalidation and automatic refetching features add value at a scale of data complexity that this project has not yet reached. If polling logic grows beyond what `usePolling` handles cleanly, TanStack Query can be introduced for specific hooks without rewriting the whole data layer.
- No Docker container is added for the UI. It runs via `npm run dev` during local development, consistent with the principle established in ADR-004 that Docker Compose is for the Camunda stack only.
