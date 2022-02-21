import pytest

from dc_comp.utils.example_util import util_function2


@pytest.fixture
def setup1() -> int:
    return util_function2()


def test_something(setup1: int) -> None:
    print(setup1)
    assert setup1 == 3, "always right"
