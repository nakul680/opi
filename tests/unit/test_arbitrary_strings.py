import pytest

from opi.core import Calculator
from opi.input import ArbitraryString, ArbitraryStringPos


@pytest.fixture
def calc():
    calc = Calculator("test")
    return calc


@pytest.mark.parametrize(
    "string",
    [
        "test",
    ],
)
def test_add_arbitrary_strings(calc: Calculator, string: str):
    """Test for Input.add_arbitrary_string()"""
    calc.input.add_arbitrary_string(string)
    assert ArbitraryString(string) in calc.input.arbitrary_strings


@pytest.mark.parametrize(
    "string, position",
    [
        ("toptest", ArbitraryStringPos.TOP),
        ("beforecoords", ArbitraryStringPos.BEFORE_COORDS),
        ("Bottom", ArbitraryStringPos.BOTTOM),
    ],
)
def test_add_arbitrary_strings_pos(calc: Calculator, string: str, position: ArbitraryStringPos):
    """Test for Input.add_arbitrary_string() with specific position."""
    calc.input.add_arbitrary_string(string, pos=position)
    assert ArbitraryString(string, pos=position) in calc.input.arbitrary_strings


def test_add_arbitrary_string_default_pos(calc: Calculator):
    """Test for Input.add_arbitrary_string() with default position."""
    calc.input.add_arbitrary_string("test")
    assert (
        ArbitraryString("test", pos=ArbitraryStringPos.BEFORE_COORDS)
        in calc.input.arbitrary_strings
    )


def test_add_arbitrary_strings_not_str(calc: Calculator):
    """Test for adding a non-string to arbitrary strings."""
    with pytest.raises(TypeError):
        calc.input.add_arbitrary_string(1234)


def test_add_empty_string(calc: Calculator):
    """Test for adding an empty string to arbitrary strings."""
    with pytest.raises(ValueError):
        calc.input.add_arbitrary_string("")


@pytest.mark.parametrize(
    "add_param, remove_param", [("test", "test"), ("test1", ArbitraryString("test1"))]
)
def test_remove_string(calc: Calculator, add_param: str, remove_param: str | ArbitraryString):
    """Test for removing a string from an arbitrary string."""
    calc.input.add_arbitrary_string(add_param)
    calc.input.remove_arbitrary_string(remove_param)
    assert not calc.input.arbitrary_strings


def test_remove_arbitrary_string_strict(calc: Calculator):
    """Test for Input.remove_arbitrary_string() with strict=True."""
    with pytest.raises(ValueError):
        calc.input.remove_arbitrary_string("test", strict=True)


@pytest.mark.parametrize(
    "strings",
    [
        [
            "test_single_string",
        ],
        ["test_multi_string1", "test_multi_string2"],
    ],
)
def test_clear_arbitrary_strings(calc: Calculator, strings: list[str]):
    """Test for Input.clear_arbitrary_strings()."""
    for string in strings:
        calc.input.add_arbitrary_string(string)

    calc.input.clear_arbitrary_strings()
    assert not calc.input.arbitrary_strings


def test_clear_arbitrary_strings_strict(calc: Calculator):
    """Test for Input.clear_arbitrary_strings() with strict=True."""
    with pytest.raises(ValueError):
        calc.input.clear_arbitrary_strings(strict=True)
