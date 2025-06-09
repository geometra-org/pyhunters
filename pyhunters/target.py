from pathlib import Path

from pydantic import BaseModel, model_validator


class Target(BaseModel):
    """A trackable, traceable object for comparison over time in storage."""

    name: str
    # `project` will likely be a partition key
    project: str = "DEFAULT"  # eventually replace with something from pyproject.toml
    module_path: Path
    method_name: str
    line_no: int
    args: tuple
    kwargs: dict
    returns: object | None = None
    error: type[Exception] | None = None

    @model_validator(mode="after")
    def check_returns_and_error(self):
        """Ensure wonky initialization is caught."""
        if self.returns and self.error:
            raise ValueError(
                f"A {self.__class__.__name__} object cannot have both returns and an "
                "error."
            )

    @property
    def key(self) -> str:
        """Hashable of the markable object."""
        return (
            f"{self.project}.{self.name}:"
            f"{self.module_path}.{self.method_name}.{self.line_no}"
        )

    def __hash__(self) -> int:
        """One (unique) mark to rule them all."""
        return hash(self.key)

    @property
    def error_raised(self) -> bool:
        """Whether the mark caught an error."""
        return bool(self.error)
