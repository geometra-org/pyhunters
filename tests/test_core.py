from pathlib import Path

from pyhunters import core as module

test_pyhunters = module.getPyHunters()


def test_mark():
    """Just a super basic test that calls the mark method."""
    TEST_TARGET = "test_target"

    @test_pyhunters.mark(TEST_TARGET)
    def test_method_no_args():
        return "this"

    test_method_no_args()
    target = test_pyhunters[TEST_TARGET]
    assert target.name == TEST_TARGET
    assert target.project == "DEFAULT"
    assert target.module_path == Path(__file__)
    assert target.method_name == "test_method_no_args"
    assert target.line_no == 13
    assert target.args == ()
    assert target.kwargs == {}
    assert target.returns == "this"
    assert target.error is None
