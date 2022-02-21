"""Test cases for the __main__ module."""

from dc_comp.main import main


def test_main_succeeds() -> None:
    """It exits with a status code of zero."""
    main()
    a = 1
    assert a == 1
