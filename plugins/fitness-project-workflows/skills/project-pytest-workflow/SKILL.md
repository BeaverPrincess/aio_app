---
name: project-pytest-workflow
description: Create or modify pytest tests for Python applications in this repository, including fixtures, mocks, and migration-backed database tests. Do not use for non-pytest test frameworks.
---

# Project pytest workflow

Inspect the configured pytest settings and target code before changing tests. Do not add production behavior merely to make a test convenient.

## Test structure and naming

- Put shared fixtures in the application's `tests/conftest.py`. Put web-route tests in `tests/web/`, model tests in `tests/models/`, and service tests in `tests/services/`; create a directory only when its application layer exists.
- Group related behavior in classes named `Test<Feature>`. Do not use mutable class variables for application state, sessions, seed data, or cleanup.
- Name test methods `test_<function_name>__<expected_result>`, using exactly two underscores between the function and expected result.
- Use fixtures for shared setup and teardown. Each test must start clean and must not depend on execution order or another test's changes.
- When writing tests, focus on important behavior and meaningful edge cases. Avoid duplicating similar or obvious cases; group equivalent scenarios with `@pytest.mark.parametrize` or other suitable pytest decorators.

## Database test structure

Use the repository's baseline-and-transaction pattern for every test class that reads or writes ORM data, exercises migrations, or depends on PostgreSQL behavior. Reuse `src/aio_fitness_app/tests/base_test_class.py` and `src/aio_fitness_app/tests/conftest.py`; do not reproduce their fixture internals in individual test modules.

- Name a database-backed class `Test<Feature>`, inherit `BaseTestClass`, and decorate it with `@pytest.mark.usefixtures("database_baseline")`.
- Implement `_get_init_tables()` as a class method returning `BaselineRowsByModel`. Return a fresh dictionary on every call; never store baseline dictionaries, row lists, ORM instances, sessions, or cleanup state in mutable class variables.
- Map each ORM model class to a list of `BaselineRowValues` dictionaries. Each row dictionary maps mapped attribute names to their values. Use immutable `ClassVar` constants when test assertions and baseline declarations share expected values.
- Seed only rows required by that test class. Return an empty dictionary when the class requires a migrated database but no initial rows.
- Declare parent or referenced models before dependent and association-object models. Keep primary keys, foreign keys, uniqueness, singleton rules, and other database constraints valid.
- Add `database_transaction: None` to every database-backed test method. Let `database_baseline` commit the class baseline before tests run, and let `database_transaction` roll back each method's changes, including commits made by production code.
- Query baseline rows through `db.session` inside each test. Do not pass committed baseline ORM instances into tests or make assertions against detached seed instances.
- Do not request `database_baseline` as a test-method parameter merely to obtain expected values; the fixture is activated by the class marker, while expected values belong in immutable constants or explicit assertions.
- Rely on `BaseTestClass` to insert the constructed rows once per class and delete those same rows in reverse order during class teardown. Do not add model-specific insertion or cleanup SQL to the reusable base fixture.

## Assertions, mocks, and databases

- Prefer direct `assert` statements, including for mock call data. Use mock-specific assertion methods only when a direct assertion is less clear.
- Use `with patch(...)` inside the test method rather than a patch decorator.
- Mock external network boundaries; tests must not call live services.
- HTTP-only tests may use isolated in-memory SQLite configuration.
- Tests that exercise models, migrations, or PostgreSQL-specific behavior must use a disposable PostgreSQL database, never the development database. Apply the complete Alembic schema once per pytest session; do not call `db.create_all()`.
- The session-scoped infrastructure must migrate one disposable PostgreSQL database, remove each class baseline before the next class, and drop the database at session end.
