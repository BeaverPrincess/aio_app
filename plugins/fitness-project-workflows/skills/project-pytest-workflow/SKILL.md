---
name: project-pytest-workflow
description: Create or modify pytest tests for Python applications in this repository, including fixtures, mocks, and migration-backed database tests. Do not use for non-pytest test frameworks.
---

# Project pytest workflow

Read the applicable application `AGENTS.md`, the root guidance, and the configured pytest settings before changing tests. Preserve the user-approved implementation scope; do not add production behavior merely to make a test convenient.

## Test structure and naming

- Put shared fixtures in the application's `tests/conftest.py`. Put web-route tests in `tests/web/`, model tests in `tests/models/`, and service tests in `tests/services/`; create a directory only when its application layer exists.
- Group related behavior in classes named `Test<Feature>`. Do not use mutable class variables for application state, sessions, seed data, or cleanup.
- Name test methods `test_<function_name>__<expected_result>`, using exactly two underscores between the function and expected result.
- Use fixtures for shared setup and teardown. Each test must start clean and must not depend on execution order or another test's changes.
- When writing tests, focus on important behavior and meaningful edge cases. Avoid duplicating similar or obvious cases; group equivalent scenarios with `@pytest.mark.parametrize` or other suitable pytest decorators.

## Assertions, mocks, and databases

- Prefer direct `assert` statements, including for mock call data. Use mock-specific assertion methods only when a direct assertion is less clear.
- Use `with patch(...)` inside the test method rather than a patch decorator.
- HTTP-only tests may use isolated in-memory SQLite configuration.
- Tests that exercise models, migrations, or PostgreSQL-specific behavior must use a disposable PostgreSQL database, never the development database. Apply the complete Alembic schema once per pytest session; do not call `db.create_all()`.
- For PostgreSQL tests, seed only each test class's baseline data, roll back each test method's transaction, remove the class seed data before the next class, and drop the database at session end.

## Finish

Run the repository's configured formatter, linter, type checker, and relevant pytest command. Report the commands and their outcomes.
