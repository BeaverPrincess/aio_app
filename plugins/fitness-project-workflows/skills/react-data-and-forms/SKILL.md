---
name: react-data-and-forms
description: Build and review Flask API access, TanStack Query 5 server state, React Hook Form 7 forms, and Zod 4 validation in this frontend. Use for queries, mutations, API clients, form schemas, and validation boundaries; do not use for purely local visual state or routing alone.
---

# React data and forms workflow

## API boundary

- Keep HTTP request functions in `frontend/src/api/`; do not call `fetch` from components.
- Check unsuccessful HTTP responses and translate them into a clear application error before returning data.
- Accept JSON responses as `unknown` and validate their runtime shape with a Zod schema. Export inferred types from schemas instead of duplicating API data interfaces.
- Keep API functions small and resource-focused. Do not mix request transport, React Hooks, and rendering in one module.

## TanStack Query

- Create one `QueryClient` in the application providers layer.
- Use `useQuery` and `useMutation` for Flask data. Do not duplicate their loading, error, or cached data in React state.
- Give every query a stable array key. Include every query-function input that changes the returned data in that key.
- Organize query keys by feature and invalidate the narrowest affected query family after a successful mutation.
- Choose `staleTime`, retries, polling, and refetch settings intentionally. TanStack Query's defaults are active behavior, not neutral configuration.

## Forms and validation

- Let React Hook Form manage field registration, submission state, and field errors. Use a Zod schema through `zodResolver` as the client-side validation source of truth.
- Use Zod input and output types when a schema transforms values. Do not force mismatched form types with assertions.
- Show both field-level validation feedback and a clear form-level error for a rejected server request.
- Client validation does not trust the browser or replace Flask-side validation.

## References

- TanStack Query quick start: https://tanstack.com/query/latest/docs/framework/react/quick-start
- Query keys: https://tanstack.com/query/latest/docs/framework/react/guides/query-keys
- Query invalidation: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
- Zod basics: https://zod.dev/basics
- React Hook Form resolver typing: https://github.com/react-hook-form/resolvers
