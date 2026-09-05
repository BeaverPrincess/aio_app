---
name: react-development
description: Build, review, and refactor React 19 components, Hooks, state, and Effects in this repository. Use for React and TSX work; do not use for routing, server-state, form-validation, styling, or test-specific decisions alone.
---

# React development

Use React 19's official guidance for component, state, and Effect decisions.

## Components and rendering

- Treat every component and custom Hook as pure: the same props, state, and context produce the same JSX.
- Never mutate props, state, context, Hook arguments, or values already passed to JSX.
- Do not cause side effects during rendering. Put user-triggered work in event handlers.
- Use components in JSX. Do not call component functions directly.
- Keep components cohesive. Extract a component when it has a distinct responsibility or is reused; do not extract trivial one-use markup merely to reduce line count.

## Hooks and state

- Call Hooks only at the top level of React function components or custom Hooks.
- Keep local state minimal. Derive values from props or existing state during render instead of synchronizing duplicate state.
- Replace objects and arrays in state; do not mutate them.
- Use an updater function when the next state depends on its previous value.
- Prefer local state. Lift state only to the nearest common owner that truly coordinates it.
- Create a custom Hook only for reusable stateful behavior, not to hide ordinary component logic.

## Effects

- Use an Effect only to synchronize React with an external system, such as a browser API, third-party widget, or subscription.
- Do not use an Effect to derive render data, respond to a click, submit a form, or fetch Flask API data. Use rendering, an event handler, or the project's TanStack Query workflow instead.
- Every subscription, timer, connection, or other external resource created in an Effect requires matching cleanup when applicable.
- Include every reactive value used by an Effect in its dependency list. Do not suppress Hook lint rules to avoid correcting the design.

## Development checks

- Keep `React.StrictMode` enabled in development.
- Let the project's ESLint React and React Hooks rules enforce these rules.
- Use the official React documentation before introducing advanced APIs or optimization hooks.

## References

- React reference: https://react.dev/reference/react
- Rules of React: https://react.dev/reference/rules
- Effects: https://react.dev/learn/you-might-not-need-an-effect
- State updates: https://react.dev/learn/updating-objects-in-state
