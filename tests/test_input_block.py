import pytest

from opi.core import Calculator
from opi.input.blocks import BlockEprnmr, BlockMethod, BlockScf, Nuclei, NucleiFlag
from opi.utils.element import Element


@pytest.fixture
def empty_calc():
    return Calculator("test")


@pytest.fixture
def calc():
    calc = Calculator("test")
    calc.input.add_blocks(
        BlockMethod(
            d3s6=0.64,
            d3a1=0.3065,
            d3s8=0.9147,
            d3a2=5.0570,
        ),
        BlockEprnmr(
            gtensor=True,
            nuclei=Nuclei(atom=Element.HYDROGEN, flags=NucleiFlag(adip=True, aiso=True, aorb=True)),
        ),
    )
    return calc


def test_add_block(empty_calc: Calculator):
    calc = empty_calc
    calc.input.add_blocks(BlockScf(maxiter=10))
    assert len(calc.input.blocks) == 1


def test_add_blocks(empty_calc: Calculator):
    calc = empty_calc
    calc.input.add_blocks(BlockScf(maxiter=10), BlockMethod(d3s6=0.64, d3a1=0.3065))
    assert len(calc.input.blocks) == 2


def test_add_blocks_strict(calc: Calculator):
    with pytest.raises(ValueError):
        calc.input.add_blocks(BlockMethod(d3s6=0.75), strict=True)


def test_add_blocks_overwrite(calc: Calculator):
    calc.input.add_blocks(BlockMethod(d3s6=0.75), overwrite=True)

    assert calc.input.blocks[BlockMethod].d3s6 == 0.75


def test_remove_block(calc: Calculator):
    calc.input.remove_blocks(BlockMethod())
    assert len(calc.input.blocks) == 1


def test_remove_blocks(calc: Calculator):
    calc.input.remove_blocks(BlockMethod(), BlockEprnmr())
    assert len(calc.input.blocks) == 0


def test_remove_blocks_strict(calc: Calculator):
    with pytest.raises(ValueError):
        calc.input.remove_blocks(BlockScf(), strict=True)


def test_has_block_empty_calc(empty_calc: Calculator):
    calc = empty_calc
    assert calc.input.has_blocks(BlockScf()) == (False,)


def test_has_block(calc: Calculator):
    assert calc.input.has_blocks(BlockMethod())


def test_has_blocks(calc: Calculator):
    assert calc.input.has_blocks(BlockMethod(), BlockEprnmr()) == (True, True)


def test_has_no_block(calc: Calculator):
    assert calc.input.has_blocks(BlockScf()) == (False,)


def test_get_block_empty(empty_calc: Calculator):
    returned_block = empty_calc.input.get_blocks(BlockMethod)
    assert returned_block == {}


def test_get_block(empty_calc: Calculator):
    test_block = BlockScf()
    empty_calc.input.add_blocks(test_block)
    assert empty_calc.input.get_blocks(BlockScf) == {BlockScf: test_block}


def test_get_blocks_create_missing(empty_calc: Calculator):
    returned_blocks = empty_calc.input.get_blocks(BlockScf, create_missing=True)
    assert BlockScf in returned_blocks


def test_clear_blocks(calc: Calculator):
    calc.input.clear_blocks()
    assert not calc.input.blocks


def test_clear_blocks_strict(empty_calc: Calculator):
    with pytest.raises(ValueError):
        empty_calc.input.clear_blocks(strict=True)
