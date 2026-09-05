---
name: python-development-conventions
description: Apply this repository's implementation conventions when creating, modifying, reviewing, or suggesting Python source or test code. Do not use for work that does not involve Python.
---

# Python development conventions

- Write small, cohesive units with explicit names and straightforward control
  flow. Avoid duplication, deeply nested conditionals, long parameter lists,
  and hidden side effects.
- Follow the repository's 100-character line limit and normal Ruff formatting
  conventions for new code. Do not suppress lint rules without a concrete,
  documented reason.
- Put imports at module level, grouped as standard-library, third-party, and
  local imports. Keep imports used, explicit, and alphabetically ordered.
  Use a local import only to prevent a genuine circular dependency.
- Use `is None` / `is not None`, never equality comparison with `None`; do not
  compare directly to `True` or `False`.
- Do not use bare `except`. Catch the expected exception type, preserve useful
  context, and either handle or re-raise it deliberately.
- Avoid multiple statements on one line, unnecessary semicolons, ambiguous
  names, duplicate dictionary keys, and unused variables or imports.
- Use `PascalCase` for classes, `snake_case` for functions, methods, variables,
  and modules, and `UPPER_CASE` for constants.
- Prefer a class when code owns state, represents a domain concept, coordinates
  collaborators, or has related behavior. Use a standalone function only for a
  small, stateless utility where a class would not improve clarity.
- Default to one primary, cohesive class per module. Exceptions include enums,
  constants, dataclasses, protocols, exceptions, small private helpers, and
  tightly coupled types implementing one responsibility.
- Keep comments and docstrings concise and focused on intent that the code does
  not already make clear.

# Logging

- Use `shared_logging.AppLogger` for application classes that need operational
  logs. Log significant events, recoverable problems, and failures; avoid noisy
  routine messages unless verbose mode is enabled.
- Prefix important information with `ℹ️`, warnings with `⚠️`, and errors with
  `❌` when a concise visual marker improves scanability.
- Never log secrets, credentials, environment-variable values, or personal
  data.

# Builder pattern

Use Builder when a product has several optional or nested parts, requires
ordered construction or validation, or has multiple representations sharing
similar construction steps.

- Keep the product separate from its construction process.
- Give the builder domain-level step methods and a `build()` method that returns
  only a complete, validated product.
- Use a `Protocol` or abstract base class only when multiple concrete builders
  genuinely share construction steps.
- Add a Director only when ordered construction recipes are reused in more than
  one place. Otherwise, let the client call the builder directly.
- Keep each concrete builder responsible for one product representation.
- Prefer a dataclass, normal constructor, or small factory for simple object
  creation. Do not introduce Builder merely to follow the pattern.
- Do not expose mutable, incomplete products outside the builder.
