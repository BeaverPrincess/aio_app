---
name: sqlalchemy-2-guidelines
description: Apply official SQLAlchemy 2.x patterns when designing, reviewing, or changing Core or ORM code, including mappings, queries, transactions, relationships, loading, and migrations.
---

# SQLAlchemy 2 Guidelines

The stable baseline is SQLAlchemy **2.0.52** and its official documentation.

Apply this snapshot for ordinary SQLAlchemy 2.x work. When a task requests the *latest* version, an upgrade, or SQLAlchemy 2.1+, verify the relevant official documentation and adapt only after confirming the target version.

## Version and project fit

- Use SQLAlchemy 2.x patterns for new code. Do not introduce 1.x-era APIs.
- Preserve the existing framework integration, session lifecycle, transaction boundaries, and migration workflow unless the requested change requires altering them.

## Declarative ORM mappings

- Prefer typed declarative mappings: `DeclarativeBase`, `Mapped[...]`, `mapped_column(...)`, and annotation-inferred `relationship(...)`.
- Model nullability accurately: `Mapped[str]` produces a non-nullable column by default, while `Mapped[str | None]` produces a nullable one by default.
- Use explicit `back_populates` on both sides of a bidirectional relationship.
- Prefer class or column expressions over strings when that does not create an import cycle. String foreign-key targets are appropriate when they avoid one.
- Enforce durable domain invariants with database constraints as well as input validation at the application boundary.
- Use an association-object class when a many-to-many table carries domain data. Do not also map that table with `relationship(..., secondary=...)`.
- Use `delete-orphan` only when a child is exclusively owned by one parent and must not outlive it.

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Parent(Base):
    __tablename__ = "parent"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[list["Child"]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan",
    )
```

## Querying and loading

- Prefer `select()` with `Session.execute()` or `Session.scalars()`.
- Use `scalars()` for one mapped entity or one selected column. Use `execute()` for rows containing multiple selected values.
- Select a result-consumption method that states the required cardinality: `one()`, `one_or_none()`, `first()`, or `all()`.
- Treat `Session.query()` and `Query` as legacy APIs. Maintain an existing use only when the task specifically requires it; do not add new uses.
- Use SQL expression constructs and bound parameters. Use `text()` only for intentional, static textual SQL with named bound parameters; never construct SQL by interpolating values into a string.
- Choose relationship loading deliberately to prevent N+1 queries. `selectinload()` is generally suitable for collections; `joinedload()` is often suitable for scalar relationships.
- A filtering `join()` does not itself replace an eager-loading option.
- When using `joinedload()` for a collection, call `Result.unique()` before consuming ORM entities.
- For extremely large collections that must be changed but not read in full, consider a SQLAlchemy 2.x write-only relationship when it matches the domain.

```python
statement = select(User).where(User.email == email)
user = session.scalars(statement).one_or_none()
```

## Sessions and transactions

- Treat a `Session` as a unit of work; do not use it as a global data-access shortcut.
- Add and modify objects through the session. Use `flush()` when database-generated values are required before the transaction commits.
- Commit at the appropriate application or service boundary, not in low-level reusable model helpers.
- Roll back a failed active transaction before the session is reused.
- Use an explicit transaction scope for grouped work.
- SQLAlchemy 2.x has no library-level autocommit and no `Session.autocommit`. Do not rely on either.
- Do not use `Engine.execute()` or connectionless execution. Execute through an explicit `Connection` or `Session`.

```python
try:
    with session.begin():
        session.add(new_dish)
except SQLAlchemyError:
    raise
```

```python
with engine.begin() as connection:
    connection.execute(
        text("UPDATE ingredient SET name = :name WHERE id = :id"),
        {"name": name, "id": ingredient_id},
    )
```

## Async SQLAlchemy

- Keep synchronous and asynchronous database stacks separate.
- Use `AsyncEngine`, `AsyncSession`, and `await` consistently.
- Avoid implicit lazy-loading IO in async code. Eager-load needed relationships or use SQLAlchemy's supported async attribute patterns.

## Schema changes

- Make persistent schema changes with Alembic and read `migrations/AGENTS.md`
  before editing a revision.

## Official baseline

- [SQLAlchemy 2.0.52 documentation](https://docs.sqlalchemy.org/en/20/)
- [Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [ORM querying guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/)
- [Session and transaction guide](https://docs.sqlalchemy.org/en/20/orm/session.html)
- [Relationship configuration](https://docs.sqlalchemy.org/en/20/orm/relationships.html)
- [SQLAlchemy 2.0 migration guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html)
