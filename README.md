# AIO Fitness App

A web-based meal tracker for recording ingredients and meals, then viewing their nutritional information. It uses Flask, Flask-SQLAlchemy, PostgreSQL, Alembic, and Jinja templates.

The application currently provides a health endpoint. Meal-tracker business logic and database tables have not been implemented yet.

## Architecture and workflow

```text
Browser -> Flask -> Flask-SQLAlchemy -> PostgreSQL
                                      ^
                                  Alembic migrations
```

Flask serves HTTP requests. Flask-SQLAlchemy provides Flask-aware SQLAlchemy sessions. Alembic creates and evolves the PostgreSQL schema through reviewed migrations.

## Run

Start PostgreSQL and pgAdmin:

```powershell
docker compose up -d
```

Run the Flask application:

```powershell
.\.venv\Scripts\flask.exe --app src.aio_fitness_app:create_app run --debug
```

Check the application at `http://127.0.0.1:5000/health`.

Open pgAdmin at `http://localhost:5050`.

Stop the Docker services while keeping their database data:

```powershell
docker compose down
```
