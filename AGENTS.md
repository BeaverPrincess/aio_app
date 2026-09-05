# Repository contributor guide

## Purpose and current state

This repository is a learning-focused fitness project that may contain multiple applications. Its shared learning goals are Flask, Flask-SQLAlchemy, and SQLAlchemy 2.x. Prefer clear, inspectable code that makes those concepts easy to understand. At the start of every Codex session, before taking task actions, read `docs/handoffs/project-state.md` for the current repository state.

## Scope and change authority

- Default to read-only guidance. Do not create, modify, rename, or delete repository files, or run schema-changing commands, unless the user's current message contains the exact phrase `implement on your own`. Requests such as "create," "add," "fix," "update," "write," or "apply" do not grant write authorization without that exact phrase.
- Write authorization applies only to the precise scope requested in the current message. Do not add anticipated features, dependencies, models, routes, configuration, files, refactors, tests, documentation, or defensive behavior outside that scope.

## Delivery mode

Without write authorization:

1. Work on one explicit implementation step at a time unless the user requests a complete roadmap.
2. Identify every file and location affected by the step.
3. Provide complete file contents or an unambiguous copyable replacement or insertion block.
4. Explain every changed construct, what it does, and why it belongs in the current architecture.
5. Explain why related components do not need changes.
6. Provide an exact verification command or action, its expected result, and the success condition.
7. Stop until the user verifies the step.

With write authorization, apply only the requested changes, verify them proportionately, and report the result.

## Critical evaluation

- Treat each request as a goal to evaluate. Before proceeding, assess whether the requested approach is correct, safe, and proportionate to the intended outcome.
- When a material correctness, security, data-integrity, billing, API-compatibility, maintainability, scope, or architectural concern exists, pause before the affected action. Explain the concern with concrete evidence, recommend the best approach, and present viable alternatives with their tradeoffs.
- Ask one focused question only when the choice materially changes the implementation or could create an irreversible or risky outcome. Do not invent objections or request confirmation for routine, low-risk, unambiguous steps.
- Follow an explicitly chosen informed tradeoff within the authorized scope unless it conflicts with higher-priority safety or repository rules.

## Response review

Before responding, silently review and revise the solution for compliance, correctness, completeness, unnecessary complexity, scope expansion, side effects, missing requirements, edge cases, verification, and the simplest correct approach. Respond only when no known material issue remains and confidence is high; otherwise state the uncertainty or ask one focused question.

## Agent response file links

- When linking a local file in a response, use a Markdown link with a forward-slash absolute path. On Windows, use `/C:/...`, never `C:\...`; wrap a target containing spaces in `<...>`.

## Sensitive configuration

- Never access, inspect, display, infer, or request values from `.env`.
- Treat environment-variable values as private. Refer only to variable names.
- When verification needs configuration, provide a command the user can run and describe its non-secret expected result.

## Repository-wide engineering standards

- Whenever generating, modifying, reviewing, or suggesting Python code, use the installed `python-development-conventions` and `python-typing-conventions` skills.
- Do not commit secrets, local databases, virtual environments, generated caches, or other local artifacts.
- Before recommending or implementing work with a dependency, consult its latest stable official documentation that is compatible with the version pinned in `requirements.txt`. Use the official documentation for Flask, Flask-SQLAlchemy, SQLAlchemy, and Alembic design guidance, and link it when explaining a design decision.

## Verification and project guidance

- After changing Python source or tests, run `ruff check .`, `ruff format --check .`, `pyright`, and `python -m pytest`. Report the commands and their outcomes, or explain why a command could not run.
- Keep exactly one handoff file: `docs/handoffs/project-state.md`. Update it only when requested, replacing its contents with the concise current state rather than appending history.
- Keep this root file limited to cross-project requirements. Create a nested `AGENTS.md` only when an application or directory has requirements that differ from these standards.
- Before changing an application or a migration, read the nearest applicable nested `AGENTS.md` in addition to this file.
- When its workflow applies, use the installed project skill for pytest tests, SQLAlchemy work, Flask application work, external-service integration, or project-guidance maintenance.
