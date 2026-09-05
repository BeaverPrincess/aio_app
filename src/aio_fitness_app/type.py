from typing import TypeVar

type JsonValue = str | int | float | bool | None | dict[str, "JsonValue"] | list["JsonValue"]

ViewResponse = TypeVar("ViewResponse")
