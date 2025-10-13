import pytest

from opi.core import Calculator
from opi.input import ArbitraryString, ArbitraryStringPos


@pytest.fixture
def empty_calc():
    empty_calc = Calculator("test")
    return empty_calc


@pytest.mark.parametrize(
    "string",
    [
        "test",
    ],
)
def test_add_arbitrary_strings(empty_calc: Calculator, string: str):
    """Test for Input.add_arbitrary_string()"""
    empty_calc.input.add_arbitrary_string(string)
    assert ArbitraryString(string) in empty_calc.input.arbitrary_strings


@pytest.mark.parametrize(
    "string, position",
    [
        ("toptest", ArbitraryStringPos.TOP),
        ("beforecoords", ArbitraryStringPos.BEFORE_COORDS),
        ("Bottom", ArbitraryStringPos.BOTTOM),
    ],
)
def test_add_arbitrary_strings_pos(
    empty_calc: Calculator, string: str, position: ArbitraryStringPos
):
    """Test for Input.add_arbitrary_string() with specific position."""
    empty_calc.input.add_arbitrary_string(string, pos=position)
    assert ArbitraryString(string, pos=position) in empty_calc.input.arbitrary_strings


def test_add_arbitrary_string_default_pos(empty_calc: Calculator):
    """Test for Input.add_arbitrary_string() with default position."""
    empty_calc.input.add_arbitrary_string("test")
    assert (
        ArbitraryString("test", pos=ArbitraryStringPos.BEFORE_COORDS)
        in empty_calc.input.arbitrary_strings
    )


def test_add_arbitrary_strings_not_str(empty_calc: Calculator):
    """Test for adding a non-string to arbitrary strings."""
    with pytest.raises(TypeError):
        empty_calc.input.add_arbitrary_string(1234)


def test_add_empty_string(empty_calc: Calculator):
    """Test for adding an empty string to arbitrary strings."""
    with pytest.raises(ValueError):
        empty_calc.input.add_arbitrary_string("")


@pytest.mark.parametrize(
    "add_param, remove_param", [("test", "test"), ("test1", ArbitraryString("test1"))]
)
def test_remove_string(empty_calc: Calculator, add_param: str, remove_param: str | ArbitraryString):
    """Test for removing a string from the arbitrary strings in the Input class."""
    empty_calc.input.add_arbitrary_string(add_param)
    empty_calc.input.remove_arbitrary_string(remove_param)
    assert not empty_calc.input.arbitrary_strings


def test_remove_arbitrary_string_strict(empty_calc: Calculator):
    """Test for Input.remove_arbitrary_string() with strict=True."""
    with pytest.raises(ValueError):
        empty_calc.input.remove_arbitrary_string("test", strict=True)


@pytest.mark.parametrize(
    "strings",
    [
        [
            "test_single_string",
        ],
        ["test_multi_string1", "test_multi_string2"],
    ],
)
def test_clear_arbitrary_strings(empty_calc: Calculator, strings: list[str]):
    """Test for Input.clear_arbitrary_strings()."""
    for string in strings:
        empty_calc.input.add_arbitrary_string(string)

    empty_calc.input.clear_arbitrary_strings()
    assert not empty_calc.input.arbitrary_strings


def test_clear_arbitrary_strings_strict(empty_calc: Calculator):
    """Test for Input.clear_arbitrary_strings() with strict=True."""
    with pytest.raises(ValueError):
        empty_calc.input.clear_arbitrary_strings(strict=True)
