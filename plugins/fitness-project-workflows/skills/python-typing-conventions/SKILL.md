---
name: python-typing-conventions
description: Apply this repository's strict typing conventions when creating, modifying, reviewing, or suggesting Python source or test code. Do not use for work that does not involve Python.
---

# Python typing conventions

- Give every new or changed function and method precise parameter and return
  annotations. Annotate public attributes and class-level state explicitly.
- Use built-in generic types (`list[str]`, `dict[str, int]`) and PEP 604 unions.
  Include `None` only when it is a valid runtime value; never use
  `typing.Optional`.
- Avoid `Any`, `object`, and overly broad annotations when the possible values
  can be expressed precisely. Model dynamic boundaries with an exact union,
  protocol, generic type parameter, typed mapping, or boundary-specific type.
- Use `...` only where it has defined typing syntax, such as a variable-length
  tuple, an overload body, or a protocol or stub method body.
- Use `TypedDict` for dictionary-shaped data at serialization or external-data
  boundaries. Prefer an existing domain type or a `@dataclass` when the value
  has domain identity, validation, defaults, or behavior.
- Keep type aliases, protocols, enums, and dataclasses next to the narrowest
  layer that owns them. Do not create a generic `constants.py` solely to hold
  unrelated type declarations.
