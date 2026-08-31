---
name: flask-app
description: Build, structure, and test Flask 3.1 application features in this repository. Use for application factories, blueprints, HTTP routes, JSON responses, error handling, and Flask test-client tests; do not use for SQLAlchemy schema-only changes.
---

# Flask application workflow

Use the Flask version pinned in `requirements.txt`. Before making a Flask design decision, consult the latest compatible official Flask documentation.

## Application structure

- Keep `create_app()` focused on configuration, extension initialization, error-handler registration, and blueprint registration.
- Put HTTP views in `src/aio_fitness_app/web/`, grouped by domain. For example, USDA routes belong in `web/usda_food_routes.py`; ingredient and dish routes each receive their own module.
- Create one blueprint per domain area, with its URL prefix defined on that blueprint.
- Do not import the Flask application instance into a route module. Register blueprints from the application factory to avoid circular imports.
- Do not load environment-based configuration or construct app-specific dependencies when a blueprint module is imported. Configure dependencies in the application factory or behind a testable request-time boundary.

## Routes and services

- Keep routes thin: validate HTTP input, call a service, and return an HTTP response.
- Keep USDA HTTP calls in `UsdaFoodClient`. Put workflows that combine multiple client calls in a dedicated service.
- Return JSON-compatible dictionaries or lists directly from Flask views when no custom response behavior is needed.
- Translate expected application and upstream-service failures to consistent JSON error responses with appropriate HTTP status codes.
- Do not add database writes, models, or migrations unless the user explicitly requests that scope.

## Testing

- Test routes with Flask's test client and pytest.
- Mock service boundaries in route tests; route tests must not make real external HTTP requests or require environment-variable values.
- Test complex orchestration separately at the service layer.
- After Python-source or test changes, run the repository's required quality checks.

## References

Use these official Flask references when relevant:

- Application factories: https://flask.palletsprojects.com/en/3.1.x/patterns/appfactories/
- Blueprints: https://flask.palletsprojects.com/en/3.1.x/blueprints/
- Testing: https://flask.palletsprojects.com/en/3.1.x/testing/