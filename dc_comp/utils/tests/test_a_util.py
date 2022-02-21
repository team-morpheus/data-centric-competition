import pytest

from dc_comp.utils.a_util import util_function


@pytest.fixture
def setup1() -> int:
    return util_function()


def test_something(setup1: int) -> None:
    print(setup1)
    assert setup1 == 3, "always right"
