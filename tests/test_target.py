from contextlib import AbstractContextManager, nullcontext
from pathlib import Path

import pytest

from src import target as module


class TestTarget:
    """src.target.Target."""

    test_cls = module.Target

    @pytest.mark.parametrize(
        "returns, error, context",
        [
            pytest.param(
                (123,),
                None,
                nullcontext(),
                id="valid-only-returns",
            ),
            pytest.param(
                None,
                None,
                nullcontext(),
                id="valid-no-returns-no-error",
            ),
            pytest.param(
                (123,),
                "ValueError()",
                pytest.raises(ValueError),
                id="invalid-both-returns-and-error",
            ),
        ],
    )
    def test_check_returns_and_error(
        self,
        returns: tuple,
        error: str,
        context: AbstractContextManager,
    ):
        """src.target.Target.check_returns_and_error."""
        with context:
            _ = self.test_cls(
                name="test_target",
                project="Test target",
                module_path=Path(),
                method_name="test_method",
                line_no=1,
                args=(),
                kwargs={},
                returns=returns,
                error=error,
            )
