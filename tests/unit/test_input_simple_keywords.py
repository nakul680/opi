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
    calc.input.add_simple_keywords(Method.HF, BasisSet.DEF2_SVP, SimpleKeyword("ex"))
    return calc


@pytest.fixture(params=[
    (Method.HF,),
    (Method.HF, BasisSet.DEF2_SVP),
    (SimpleKeyword("ex"),),
])
def keywords(request) -> tuple:
    """Provide different keyword combinations for parameterized testing."""
    return request.param


def test_add_simple_keyword(empty_calc: Calculator, keywords: tuple):
    """
    Test to add simple keywords to an empty Calculator object.
    """
    empty_calc.input.add_simple_keywords(*keywords)
    assert empty_calc.input.has_simple_keywords(*keywords)


def test_add_simple_keywords_strict(empty_calc: Calculator, keywords: tuple):
    """Test addition of keywords with strict = True."""
    empty_calc.input.add_simple_keywords(*keywords)

    with pytest.raises(ValueError):
        empty_calc.input.add_simple_keywords(keywords[0], strict=True)


def test_clear_simple_keywords(calc: Calculator):
    """Test for Input.clear_simple_keywords()."""
    calc.input.clear_simple_keywords()
    assert not calc.input.simple_keywords


def test_clear_simple_keywords_strict(empty_calc: Calculator):
    """Test for Input.clear_simple_keywords() with strict = True."""
    with pytest.raises(ValueError):
        empty_calc.input.clear_simple_keywords(strict=True)



def test_get_keywords(calc: Calculator, keywords: tuple):
    """Test for Input.get_simple_keywords().
    Tests for both regular and string keywords."""
    returned_keywords = calc.input.get_simple_keywords(*keywords)
    for keyword in keywords:
        assert keyword in returned_keywords


@pytest.mark.parametrize("keywords", [("ex",), ("hf",)])
def test_get_keyword_with_string(calc: Calculator, keywords: tuple):
    """Tests Input.get_simple_keywords() with a string.
    Tests for both regular and string keywords."""
    returned_keywords = calc.input.get_simple_keywords(*keywords)
    for keyword in keywords:
        assert SimpleKeyword(keyword) in returned_keywords


def test_get_keyword_create_missing(calc: Calculator, keywords: tuple):
    """Test Input.get_simple_keywords() with create_missing = True."""
    returned_keywords = calc.input.get_simple_keywords(*keywords, create_missing=True)
    assert keywords[0] in returned_keywords


def test_get_nonexistent_keyword(calc: Calculator, keywords: tuple):
    """Test Input.get_simple_keywords() with a not yet added keyword."""
    returned_keywords = calc.input.get_simple_keywords(*keywords)
    assert not returned_keywords


@pytest.mark.parametrize(
    "keywords_tuple",
    [
        pytest.param((Method.HF,), (True,), id="method_hf"),
        pytest.param((Method.HF_3C,), (False,), id="method_hf3c_missing"),
        pytest.param((Method.HF_3C, BasisSet.DEF2_SVP), (False, True), id="combo_hf3c_sv"),
        pytest.param(("hf", "ex"), (True, True), id="strings_hf_ex"),
    ],
)
def test_has_simple_keyword(calc: Calculator, keywords_tuple: tuple):
    """Test Input.has_simple_keywords() with different combinations of keywords and expected values."""
    keywords, results = keywords_tuple
    assert calc.input.has_simple_keywords(*keywords) == results
