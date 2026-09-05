---
name: react-router-spa
description: Build and review client-side routes and navigation with React Router 8 in this Vite single-page application. Use for route definitions, layouts, links, parameters, and navigation; do not use for server-state fetching or form validation alone.
---

# React Router single-page application workflow

Use React Router's Declarative Mode. TanStack Query is this application's server-state layer, so do not introduce React Router loaders, actions, or Framework Mode without a deliberate architectural decision.

## Route structure

- Define the route tree centrally in `frontend/src/app/router.tsx` and mount it once at the application root.
- Put route-screen components in `frontend/src/pages/`. A page may compose layout and features but should not contain reusable domain logic.
- Use nested routes and `Outlet` for shared layout. Give each distinct application URL a deliberate route and provide a not-found route.
- Keep route paths stable, readable, and based on user-visible resources rather than implementation details.

## Navigation and parameters

- Use `Link` or `NavLink` for internal navigation. Use an anchor only for an external URL, a download, or an in-page fragment.
- Use `useNavigate` after a successful user flow when a link cannot express the navigation.
- Treat route parameters as untrusted strings. Validate or narrow them before passing them to feature or API code.
- Preserve useful browser behavior: back/forward navigation, bookmarkable URLs, and a clear active navigation state where appropriate.

## References

- Router modes: https://reactrouter.com/start/modes
- BrowserRouter API: https://api.reactrouter.com/v8/functions/react-router.BrowserRouter.html
