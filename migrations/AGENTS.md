# Alembic migration guide

## Scope

This directory contains the repository Alembic environment and revisions. Before editing it, identify the application metadata the migration environment currently imports and confirm the requested schema change belongs to that application.

## Migration rules

- Alembic is the only schema-management mechanism. Never use `db.create_all()` or runtime DDL as a substitute for a migration.
- Treat Alembic autogeneration as a candidate. Inspect every generated revision and correct its operations, constraints, names, dependencies, upgrade path, and downgrade path before it is applied.
- Update affected SQLAlchemy models and migration-backed tests together, then use the project SQLAlchemy schema workflow.
