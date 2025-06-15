from pathlib import Path

from src import pyhunters as module
from src.target import Target

test_pyhunters = module.getPyHunters()

TEST_TARGET = "test_target"


def test_mark_no_args_no_return():
    """src.core.PyHunters.mark.

    mark a method that uses no args and has no return
    """

    @test_pyhunters.mark(TEST_TARGET)
    def test_method_no_args_no_return():
        return

    test_method_no_args_no_return()
    actual_result = test_pyhunters[TEST_TARGET]
    expected_result = Target(
        name=TEST_TARGET,
        project="DEFAULT",
        module_path=Path(__file__),
        method_name="test_method_no_args_no_return",
        line_no=18,
        args=(),
        kwargs={},
        returns=None,
        error=None,
    )
    assert actual_result == expected_result


def test_mark_no_args_w_return():
    """src.core.PyHunters.mark.

    mark a method that uses no args and has a return
    """

    @test_pyhunters.mark(TEST_TARGET)
    def test_mark_no_args_w_return():
        return "this", "that"

    test_mark_no_args_w_return()
    actual_result = test_pyhunters[TEST_TARGET]
    expected_result = Target(
        name=TEST_TARGET,
        project="DEFAULT",
        module_path=Path(__file__),
        method_name="test_mark_no_args_w_return",
        line_no=44,
        args=(),
        kwargs={},
        returns=("this", "that"),
        error=None,
    )
    assert actual_result == expected_result


def test_mark_w_args_w_return():
    """src.core.PyHunters.mark.

    mark a method that uses args and has a return
    """
    TEST_TARGET = "test_target"

    @test_pyhunters.mark(TEST_TARGET)
    def test_method_w_args_w_return(number: int):
        mulitply_by = 3
        return number * mulitply_by

    test_method_w_args_w_return(5)
    actual_result = test_pyhunters[TEST_TARGET]
    expected_result = Target(
        name=TEST_TARGET,
        project="DEFAULT",
        module_path=Path(__file__),
        method_name="test_method_w_args_w_return",
        line_no=71,
        args=(5,),
        kwargs={},
        returns=15,
        error=None,
    )
    assert actual_result == expected_result


def test_mark_w_kwargs_w_return():
    """src.core.PyHunters.mark.

    mark a method that uses kwargs and has a return
    """
    TEST_TARGET = "test_target"

    @test_pyhunters.mark(TEST_TARGET)
    def test_mark_w_kwargs_w_return(number: int):
        mulitply_by = 3
        return number * mulitply_by

    test_mark_w_kwargs_w_return(number=5)
    actual_result = test_pyhunters[TEST_TARGET]
    expected_result = Target(
        name=TEST_TARGET,
        project="DEFAULT",
        module_path=Path(__file__),
        method_name="test_mark_w_kwargs_w_return",
        line_no=99,
        args=(),
        kwargs={"number": 5},
        returns=15,
        error=None,
    )
    assert actual_result == expected_result


def test_mark_no_args_w_raise():
    """src.core.PyHunters.mark.

    mark a method that uses no args and raises an error
    """

    @test_pyhunters.mark(TEST_TARGET)
    def test_mark_no_args_w_raise():
        raise ValueError

    try:
        test_mark_no_args_w_raise()
    except Exception:
        actual_result = test_pyhunters[TEST_TARGET]
        expected_result = Target(
            name=TEST_TARGET,
            project="DEFAULT",
            module_path=Path(__file__),
            method_name="test_mark_no_args_w_raise",
            line_no=126,
            args=(),
            kwargs={},
            returns=None,
            error=ValueError(),
        )
        assert actual_result == expected_result
