# AIO Fitness App

A web-based meal tracker for recording ingredients and meals, then viewing their nutritional information. The planned stack is Flask, SQLAlchemy, PostgreSQL, and Jinja templates.

The application itself is not implemented yet. At this stage, the repository runs PostgreSQL and pgAdmin locally through Docker.

## Architecture and workflow

The browser will communicate with a Flask application. Flask will use SQLAlchemy to read and write PostgreSQL data, while Alembic records schema changes as reviewed migrations. pgAdmin is a separate browser tool for viewing and directly editing the local database when needed.

```text
Browser -> Flask -> SQLAlchemy -> PostgreSQL
                         ^
                     Alembic migrations
```

## Run

Start PostgreSQL and pgAdmin in the background:

```powershell
docker compose up -d
```

Check that both services are running:

```powershell
docker compose ps
```

Open pgAdmin at `http://localhost:5050`.

Stop the services while keeping their database data:

```powershell
docker compose down
```
