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


@pytest.mark.parametrize(
    "keywords",
    [
        (Method.HF,),
        (Method.HF,BasisSet.DEF2_SVP),
        (SimpleKeyword("ex"),),
    ]
)
def test_add_simple_keyword(empty_calc: Calculator, keywords: tuple):
    """
    Test for Input.add_simple_keywords with a singular and multiple keywords.
    Also tests adding an arbitrary keyword.
    """
    empty_calc.input.add_simple_keywords(*keywords)
    assert empty_calc.input.has_simple_keywords(*keywords)


@pytest.mark.parametrize(
    "keywords",
    [
        (Method.HF,),
        (Method.HF,BasisSet.DEF2_SVP),
    ]
)
def test_add_simple_keywords_strict(empty_calc: Calculator,keywords: tuple):
    """Test addition of keywords with strict = True."""
    empty_calc.input.add_simple_keywords(*keywords)

    with pytest.raises(ValueError):
        empty_calc.input.add_simple_keywords(Method.HF, strict=True)


def test_clear_keywords(calc: Calculator):
    """Test for Input.clear_simple_keywords()."""
    calc.input.clear_simple_keywords()
    assert not calc.input.simple_keywords


def test_clear_keywords_strict(empty_calc: Calculator):
    """Test for Input.clear_simple_keywords() with strict = True."""
    with pytest.raises(ValueError):
        empty_calc.input.clear_simple_keywords(strict=True)

@pytest.mark.parametrize(
    "keywords",
    [
        (Method.HF,),
        (Method.HF,BasisSet.DEF2_SVP),
        (SimpleKeyword("ex"),),

    ]
)
def test_get_keywords(calc: Calculator, keywords: tuple):
    """Test for Input.get_simple_keywords().
    Tests for both regular and arbitrary keywords."""
    returned_keywords = calc.input.get_simple_keywords(*keywords)
    for keyword in keywords:
        assert keyword in returned_keywords


@pytest.mark.parametrize(
    "keywords",
    [
        ("ex",),
        ("hf",)
    ]
)
def test_get_keyword_with_string(calc: Calculator, keywords: tuple):
    """Tests Input.get_simple_keywords() with a string.
    Tests for both regular and arbitrary keywords."""
    returned_keywords = calc.input.get_simple_keywords(*keywords)
    for keyword in keywords:
        assert SimpleKeyword(keyword) in returned_keywords


def test_get_keyword_create_missing(calc: Calculator):
    """Test Input.get_simple_keywords() with create_missing = True."""
    keywords = calc.input.get_simple_keywords(Method.HF_3C, create_missing=True)
    assert Method.HF_3C in keywords


def test_get_nonexistent_keyword(calc: Calculator):
    """Test Input.get_simple_keywords() with a not yet added keyword."""
    keywords = calc.input.get_simple_keywords(Method.HF_3C)
    assert len(keywords) == 0


@pytest.mark.parametrize(
    "keywords, results",
    [
        ((Method.HF,) , (True,)),
        ((Method.HF_3C,) , (False,)),
        ((Method.HF_3C,BasisSet.DEF2_SVP) , (False,True)),
        (("hf", "ex") , (True, True))
    ]
)
def test_has_simple_keyword(calc: Calculator, keywords: tuple, results: tuple):
    """Test Input.has_simple_keywords() with different combinations of keywords and expected values."""
    assert calc.input.has_simple_keywords(*keywords) == results


