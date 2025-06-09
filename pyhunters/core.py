import atexit
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from tracer.mark import Mark
from tracer.type_mods.singleton import Singleton

__all__ = ["mark"]


@dataclass
class Tracer(metaclass=Singleton):
    """Class for adding and managing marks."""

    name: str

    def __post_init__(self):
        """Ensure that the exit handler is registered."""
        self._marks: list[Mark] = []
        self._register_exit()

    def __iter__(self):
        """Iterate through all the marks."""
        return iter(self._marks)

    def __getitem__(self, key: str) -> Mark:
        """Get a mark by name."""
        return self._map[key]

    def get(self, name: str) -> Mark | None:
        """Get a mark by name, or None if not found."""
        try:
            return self._map[name]
        except KeyError:
            return None

    def _register_exit(self):
        atexit.register(self.summarize)

    @property
    def _map(self):
        """Get a dictionary mapping mark names to marks."""
        return {mark.name: mark for mark in self._marks}

    def add(self, mark: Mark) -> Self:
        if not isinstance(mark, Mark):
            raise TypeError(f"Expected Mark, got {type(mark)}.")
        self._marks += [mark]
        return self

    def summarize(self):
        """Summarize all traces."""
        pass


def getTracer(name: str = __name__) -> Tracer:
    """Create or get the singleton `Tracer` instance."""
    return Tracer(name=name)


def mark(name: str, *, project: str = "DEFAULT"):
    """Simple interface for adding a marker."""
    tracer = Tracer(project)
    caller = inspect.stack()[1]
    module_path = Path(caller.filename)
    line_no = caller.lineno + 1
    mark_kwargs = {"name": name, "module_path": module_path, "line_no": line_no}

    def inner(func):
        method_name = func.__name__
        mark_kwargs["method_name"] = method_name
        mark_kwargs["name"] = name

        def wrapper(*args, **kwargs):
            """Inner actions within the method."""
            mark_kwargs["args"] = args
            mark_kwargs["kwargs"] = kwargs
            try:
                global returns
                returns = func(*args, **kwargs)
            except Exception as exc:
                mark_kwargs["error"] = exc
                tracer.add(Mark(**mark_kwargs))
                raise exc
            mark_kwargs["returns"] = returns
            tracer.add(Mark.model_validate(**mark_kwargs))
            return returns

        return wrapper

    return inner
