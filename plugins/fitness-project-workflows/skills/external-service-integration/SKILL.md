---
name: external-service-integration
description: Build or modify an HTTP client that integrates a Python application in this repository with an external service. Use for API clients, response mapping, and error translation; do not use for routes or database persistence alone.
---

# External service integration

Consult the external service's official documentation before changing protocol behavior, request parameters, or response mapping.

## Boundary design

- Keep HTTP communication in a dedicated client and keep response-to-domain mapping in a separate mapper or DTO layer.
- Read configuration through typed settings rather than accessing environment variables throughout the client.
- Set an explicit timeout for each HTTP request.
- Validate untrusted response shape before mapping it.
- Translate network, timeout, HTTP-status, rate-limit, JSON-decoding, and response-shape failures into clear integration-specific exceptions. Preserve the original exception as the cause where useful.
- Do not put route logic, database persistence, or business orchestration inside the HTTP client.

## Tests and verification

- Test successful mapping and each expected failure category.
