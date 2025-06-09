import atexit
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from pyhunters.target import Target
from pyhunters.type_mods.singleton import Singleton

__all__ = ["PyHunters"]


@dataclass
class PyHunters(metaclass=Singleton):
    """Class for adding and managing marks."""

    project: str

    def __post_init__(self):
        """Ensure that the exit handler is registered."""
        self._targets: list[Target] = []
        self._register_exit()

    def __iter__(self):
        """Iterate through all the marks."""
        return iter(self._targets)

    def __getitem__(self, key: str) -> Target:
        """Get a mark by name."""
        return self._map[key]

    def get(self, name: str) -> Target | None:
        """Get a mark by name, or None if not found."""
        try:
            return self._map[name]
        except KeyError:
            return None

    def _register_exit(self):
        """Register the exit handler to summarize all targets."""
        atexit.register(self.summarize)

    @property
    def _map(self):
        """Get a dictionary mapping target names to targets."""
        return {target.name: target for target in self._targets}

    def add(self, target: Target) -> Self:
        """Add a target to the collection."""
        if not isinstance(target, Target):
            raise TypeError(f"Expected Target, got {type(target)}.")
        self._targets += [target]
        return self

    def summarize(self):
        """Summarize all traces."""
        pass

    def mark(self, name: str):
        """Simple interface for adding a marker."""
        caller = inspect.stack()[1]
        module_path = Path(caller.filename)
        line_no = caller.lineno + 1
        mark_kwargs = {"name": name, "module_path": module_path, "line_no": line_no}

        def inner(func):
            method_name = func.__name__
            mark_kwargs["method_name"] = method_name

            def wrapper(*args, **kwargs):
                """Inner actions within the method."""
                mark_kwargs["args"] = args
                mark_kwargs["kwargs"] = kwargs
                try:
                    returns = func(*args, **kwargs)
                except Exception as exc:
                    mark_kwargs["error"] = exc
                    self.add(Target(**mark_kwargs))
                    raise exc
                mark_kwargs["returns"] = returns
                target = Target.model_validate(mark_kwargs)
                self.add(target)
                return returns

            return wrapper

        return inner


def getPyHunters(project: str = __name__) -> PyHunters:
    """Create or get the singleton `PyHunters` instance."""
    return PyHunters(project=project)
