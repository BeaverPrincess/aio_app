# Repository contributor guide

## Purpose and current state

This repository is a learning-focused fitness project that may contain multiple applications. Its shared learning goals are Flask, Flask-SQLAlchemy, and SQLAlchemy 2.x. Prefer clear, inspectable code that makes those concepts easy to understand. Before taking task actions, read `docs/handoffs/project-state.md` for the current repository state.

## Scope and change authority

- Do not modify project files, run schema-changing commands, or implement changes unless the user explicitly says `implement on your own` followed by the precise scope. Otherwise, provide one guided, verifiable step at a time.
- Implement only the exact change requested in the current task. Do not add anticipated features, dependencies, models, routes, configuration, files, or refactors.
- When a requested approach is materially suboptimal, explain the concern and a better design before implementing it.
- Before handoff, review the result for correctness, maintainability, scope, and a clearly better alternative.

## Agent response file links

- When linking a local file in a response, use a Markdown link with a forward-slash absolute path. On Windows, use `/C:/...`, never `C:\...`; wrap a target containing spaces in `<...>`.

## Sensitive configuration

- Never access, inspect, display, infer, or request values from `.env`.
- Treat environment-variable values as private. Refer only to variable names.
- When verification needs configuration, provide a command the user can run and describe its non-secret expected result.

## Shared engineering standards

- Keep modules small, cohesive, and explicitly named. Prefer straightforward control flow.
- Prefer object-oriented design for application code. Encapsulate related state and behavior in cohesive classes with clear public methods.
- Use standalone functions only for small, stateless utilities where a class would not improve clarity.
- For Python code, annotate function parameters, return values, and public attributes. Use precise types or `X | None`; do not use `typing.Optional` or `typing.Any` or `typing.object`.
- Validate input at an application boundary. Keep routes thin and database work in dedicated modules.
- Do not commit secrets, local databases, virtual environments, generated caches, or other local artifacts.
- Before recommending or implementing work with a dependency, consult its latest stable official documentation that is compatible with the version pinned in `requirements.txt`. Use the official documentation for Flask, Flask-SQLAlchemy, SQLAlchemy, and Alembic design guidance, and link it when explaining a design decision.

## Logging

- Use `shared_logging.AppLogger` for application classes that need operational logs. Log significant events, recoverable problems, and failures; avoid noisy routine messages unless verbose mode is enabled.
- Prefer a concise emoji prefix to make logs easy to scan: `ℹ️` for important information, `⚠️` for warnings, and `❌` for errors.
- Never write secrets, environment-variable values, credentials, or personal data to logs.

## Object construction

- Prefer the Builder pattern when constructing an object requires many optional values, staged validation, nested objects, or reusable named configurations.
- Use a builder to avoid constructors or factory functions with long lists of optional parameters.
- A builder's `build()` method must return a complete, valid product. Do not expose a partially constructed product.
- Add a director only when the same ordered construction recipe is reused across multiple callers or builder implementations; otherwise, let the caller use the builder directly.
- Do not use Builder for simple objects with a small number of required values. Prefer a direct constructor, dataclass defaults, or a clearly named class method instead.

## Flask and SQLAlchemy standards

- Use Flask-SQLAlchemy for Flask database integration.
- Use SQLAlchemy 2.x typed declarative mappings: `Mapped[...]`, `mapped_column(...)`, and annotation-inferred `relationship()` with explicit `back_populates`.
- Prefer class or column references over raw strings when they do not create an import cycle. Use strings only where SQLAlchemy requires them or where they safely avoid a cycle, such as cross-module `ForeignKey` targets and SQL `CheckConstraint` expressions.
- Represent association tables that carry domain data as association-object classes. Do not combine an association-object mapping with a `relationship(..., secondary=...)` mapping over the same table.
- Schema changes require Alembic migrations. Do not create, alter, or drop application tables at runtime.

## Verification and project guidance

- After changing Python source or tests, run `ruff check .`, `ruff format --check .`, `pyright`, and `python -m pytest`. Report the commands and their outcomes, or explain why a command could not run.
- Keep exactly one handoff file: `docs/handoffs/project-state.md`. Update it only when requested, replacing its contents with the concise current state rather than appending history.
- Keep this root file limited to cross-project requirements. Create a nested `AGENTS.md` only when an application or directory has requirements that differ from these standards.
- Before changing an application or a migration, read the nearest applicable nested `AGENTS.md` in addition to this file.
- When its workflow applies, use the installed project skill for pytest tests, SQLAlchemy schema changes, project-guidance maintenance, or guided learning.
