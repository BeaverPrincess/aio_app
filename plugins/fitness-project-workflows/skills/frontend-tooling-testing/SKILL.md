---
name: frontend-tooling-testing
description: Configure, build, lint, type-check, and test the Vite, TypeScript, ESLint, Vitest, and Testing Library frontend. Use for frontend tooling, environment handling, quality checks, and component tests; do not use for application feature architecture alone.
---

# Frontend tooling and testing workflow

## Vite and TypeScript

- Keep Vite configuration focused on the development server, build behavior, and official plugins. Use a development proxy for Flask requests instead of embedding a development server origin throughout application code.
- Treat every `VITE_*` variable as public build output. Never expose a secret through a Vite variable and never inspect `.env` values.
- Keep TypeScript strict. Model unknown external data as `unknown`, then validate or narrow it. Do not use `any` or broad assertions to silence an error.
- Keep direct package versions exact in `package.json`. Use package documentation matching the pinned major version before changing configuration.

## Linting and formatting

- Use the local ESLint flat configuration and installed plugins. Do not rely on global tools.
- Correct lint findings instead of disabling a rule, except for a documented and narrowly scoped incompatibility.
- Keep ESLint as the single formatting authority unless the project deliberately adopts another formatter.

## Tests

- Use Vitest as the test runner and Testing Library to exercise observable user behavior.
- Prefer queries by role, label, text, or accessible name. Use `data-testid` only when no user-facing query is suitable.
- Test user-visible success, loading, empty, validation, and failure behavior relevant to the feature. Avoid tests that assert component internals, Hook implementation, or child-component structure.
- Keep reusable test setup and providers in `frontend/src/test/`; keep feature-specific tests beside the relevant feature or page.

## Verification

- After frontend source, test, or configuration changes, run the relevant local scripts from `frontend/`: `npm run lint`, `npm run test`, and `npm run build`.
- Do not create `package-lock.json`; use `npm install --package-lock=false` when an install is required for this repository.

## References

- Vite environment variables: https://vite.dev/guide/env-and-mode
- Vite server proxy: https://vite.dev/config/server-options
- Testing Library principles: https://testing-library.com/docs/
- Testing Library queries: https://testing-library.com/docs/queries/about/
