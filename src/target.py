from collections.abc import Callable
from pathlib import Path
from typing import Any, Self

from pydantic import (
    BaseModel,
    model_validator,
)
from pydantic_core import core_schema

from src.settings.build_root import PyHuntersConfig

__all__ = ["Target"]

config = PyHuntersConfig.initialize()


class Error:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        """Generates pydantic schema based on `Version` type in `semver`."""

        def make_str(value: Exception) -> str:
            """Convert an exception to a string representation.

            ValueError("this") -> "ValueError('this')"
            """
            return value.__repr__()

        def validate_from_str(value: str) -> Exception:
            """Evaluate a string as an exception.

            "ValueError('this')" -> ValueError("this")
            """
            return eval(value)  # noqa: S307

        return core_schema.json_or_python_schema(
            json_schema=core_schema.no_info_plain_validator_function(validate_from_str),
            python_schema=core_schema.is_instance_schema(
                Exception
            ),  # verify is Exception
            serialization=core_schema.plain_serializer_function_ser_schema(make_str),
        )


class Target(BaseModel):
    """A targetable, trackable object for comparison over time in storage."""

    name: str
    project: str = config.project
    module_path: Path
    method_name: str
    line_no: int
    args: tuple[object, ...]
    kwargs: dict[str, object]
    returns: object | None = None
    error: Error | None = None

    @model_validator(mode="after")
    def check_returns_and_error(self) -> Self:
        """Ensure wonky initialization is caught."""
        if self.returns and self.error:
            raise ValueError(
                f"A {self.__class__.__name__} object cannot have both returns and an "
                "error."
            )
        return self

    def __eq__(self, other: object) -> bool:
        """Compare two `Target` objects for equality."""
        if not isinstance(other, type(self)):
            return False

        if self.error is None != other.error is None:
            return False

        return (
            self.project == other.project
            and self.name == other.name
            and self.module_path == other.module_path
            and self.method_name == other.method_name
            and self.line_no == other.line_no
            and self.args == other.args
            and self.kwargs == other.kwargs
            and self.returns == other.returns
            and type(self.error) is type(other.error)
            if self.error is not None
            else True and self.error.args == other.error.args
            if self.error is not None
            else True
        )

    @property
    def key(self) -> str:
        """Hashable of the `Target`-able object."""
        return (
            f"{self.project}.{self.name}:"
            f"{self.module_path}.{self.method_name}.{self.line_no}"
        )

    def __hash__(self) -> int:
        """One (unique) `Target` to rule them all."""
        return hash(self.key)

    @property
    def error_raised(self) -> bool:
        """Whether the `Target` caught an error."""
        return bool(self.error)
