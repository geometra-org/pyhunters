import tomllib
from dataclasses import dataclass
from functools import cached_property
from operator import itemgetter
from pathlib import Path
from typing import ClassVar

from src.type_mods.singleton import Singleton


@dataclass(frozen=True)
class BuildRoot(metaclass=Singleton):
    """Represents the global workspace build root."""

    # ordered in priority
    root_files: ClassVar[list[str]] = ["pyhunters.toml", "pyproject.toml"]

    class NotFoundError(Exception):
        """Raised when unable to find the current workspace build root."""

    @cached_property
    def path(self) -> Path:
        """Returns the build root for the current workspace."""
        root = Path.cwd().resolve()
        while not any((root / file).is_file() for file in self.root_files):
            if root != root.parent:
                root = root.parent
            else:
                raise self.NotFoundError(
                    "No build root detected. `pyhunters` detects the build root by "
                    f"looking for at least one file from {self.root_files} in the cwd "
                    "and its ancestors."
                )
        return root

    @cached_property
    def combined_toml(self):
        """Returns a combined TOML dictionary from all root files."""
        combined_toml = {}
        for file in self.root_files[::-1]:
            try:
                with open(self.path / file, "rb") as toml:
                    combined_toml |= tomllib.load(toml)
            except FileNotFoundError:
                pass
            except tomllib.TOMLDecodeError as exc:
                raise self.NotFoundError(
                    f"Invalid TOML file: {self.path / file}"
                ) from exc
        if not combined_toml:
            raise self.NotFoundError(f"No valid TOML files found in {self.path}")
        return combined_toml


@dataclass(frozen=True)
class PyHuntersConfig(metaclass=Singleton):
    """Static script configuration."""

    project: str
    team: str

    @classmethod
    def initialize(cls):
        """Init for people who can spell."""
        toml = BuildRoot().combined_toml
        keys = cls.__dict__["__match_args__"]
        attrs = itemgetter(*keys)(toml)
        kwatters = dict(zip(keys, attrs, strict=False))

        return cls(**kwatters)


def getPyHuntersConfig():
    return PyHuntersConfig.initialize()
