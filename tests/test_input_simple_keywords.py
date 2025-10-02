import pytest

from opi.core import Calculator
from opi.input.simple_keywords import BasisSet, Method, SimpleKeyword


@pytest.fixture()
def empty_calc() -> Calculator:
    new_calc = Calculator("test")
    return new_calc

@pytest.fixture()
def calc():
    calc = Calculator("test")
    calc.input.add_simple_keywords(Method.HF, BasisSet.DHF_TZVP, SimpleKeyword("ex"))
    return calc


def test_add_simple_keyword(empty_calc: Calculator):
    empty_calc.input.add_simple_keywords(Method.HF)
    assert Method.HF in empty_calc.input.simple_keywords


def test_add_multiple_keywords(empty_calc: Calculator):
    empty_calc.input.add_simple_keywords(Method.HF, BasisSet.DHF_TZVP)
    assert Method.HF in empty_calc.input.simple_keywords
    assert BasisSet.DHF_TZVP in empty_calc.input.simple_keywords


def test_add_string_simple_keyword(empty_calc: Calculator):
    example_keyword = SimpleKeyword("example")
    empty_calc.input.add_simple_keywords(example_keyword)
    assert example_keyword in empty_calc.input.simple_keywords


def test_add_simple_keywords_strict(empty_calc: Calculator):
    empty_calc.input.add_simple_keywords(Method.HF)

    with pytest.raises(ValueError):
        empty_calc.input.add_simple_keywords(Method.HF, strict=True)


def test_add_string_and_simple_keyword(empty_calc: Calculator):
    example_keyword = SimpleKeyword("example")
    empty_calc.input.add_simple_keywords(example_keyword)
    empty_calc.input.add_simple_keywords(Method.HF)
    assert example_keyword in empty_calc.input.simple_keywords
    assert Method.HF in empty_calc.input.simple_keywords


def test_clear_keywords(calc: Calculator):
    calc.input.clear_simple_keywords()
    assert len(calc.input.simple_keywords) == 0


def test_clear_keywords_strict(empty_calc: Calculator):
    with pytest.raises(ValueError):
        empty_calc.input.clear_simple_keywords(strict=True)


def test_get_single_keyword(calc: Calculator):
    keywords = calc.input.get_simple_keywords(Method.HF)
    assert Method.HF in keywords


def test_get_multiple_keywords(calc: Calculator):
    keywords = calc.input.get_simple_keywords(Method.HF, BasisSet.DHF_TZVP)
    assert len(keywords) == 2


def test_get_keyword_with_string(calc: Calculator):
    keywords = calc.input.get_simple_keywords("hf")
    assert Method.HF in keywords


def test_get_arbitrary_keyword_with_string(calc: Calculator):
    keywords = calc.input.get_simple_keywords("ex")
    assert len(keywords) == 1


def test_get_keyword_create_missing(calc: Calculator):
    keywords = calc.input.get_simple_keywords(Method.HF_3C, create_missing=True)
    assert Method.HF_3C in keywords


def test_get_nonexistent_keyword(calc: Calculator):
    keywords = calc.input.get_simple_keywords(Method.HF_3C)
    assert len(keywords) == 0


def test_has_simple_keyword_true(calc: Calculator):
    assert calc.input.has_simple_keywords(Method.HF) == (True,)


def test_has_simple_keyword_false(calc: Calculator):
    assert calc.input.has_simple_keywords(Method.HF_3C) == (False,)


def test_multiple_keywords(calc: Calculator):
    assert calc.input.has_simple_keywords(Method.HF_3C, BasisSet.DHF_TZVP) == (False, True)


def test_has_keyword_with_string(calc: Calculator):
    assert calc.input.has_simple_keywords("hf", "ex") == (True, True)

