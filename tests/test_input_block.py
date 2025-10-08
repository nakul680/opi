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


@pytest.mark.parametrize(
    "blocks",
    [
        (BlockScf(maxiter=10),),
        (BlockScf(maxiter=10), BlockMethod(d3s6=0.64, d3a1=0.3065)),
    ],
)
def test_add_block(empty_calc: Calculator, blocks: tuple):
    """Test for Input.add_blocks() with singular and multiple blocks."""
    calc = empty_calc
    calc.input.add_blocks(*blocks)
    assert calc.input.has_blocks(*blocks)


def test_add_blocks_strict(calc: Calculator):
    """Test for Input.add_blocks() with strict = True."""
    with pytest.raises(ValueError):
        calc.input.add_blocks(BlockMethod(d3s6=0.75), strict=True)


def test_add_blocks_overwrite(calc: Calculator):
    """Test for Input.add_blocks() with overwritten = True."""
    calc.input.add_blocks(BlockMethod(d3s6=0.75), overwrite=True)

    assert calc.input.blocks[BlockMethod].d3s6 == 0.75


@pytest.mark.parametrize(
    "blocks,expected",
    [
        ((BlockEprnmr(),), (False,)),
        ((BlockEprnmr(), BlockMethod()), (False, False)),
    ],
)
def test_remove_block(calc: Calculator, blocks: tuple, expected: tuple):
    """Test for Input.remove_blocks().
    Test for singular and multiple blocks."""
    calc.input.remove_blocks(*blocks)
    assert calc.input.has_blocks(*blocks) == expected


def test_remove_blocks_strict(calc: Calculator):
    """Test for Input.remove_blocks() with strict = True."""
    with pytest.raises(ValueError):
        calc.input.remove_blocks(BlockScf(), strict=True)


def test_has_block_empty_calc(empty_calc: Calculator):
    """Test for Input.has_blocks() when no blocks have been added."""
    calc = empty_calc
    assert calc.input.has_blocks(BlockScf()) == (False,)


@pytest.mark.parametrize(
    "blocks, expected",
    [
        ((BlockMethod(),), (True,)),
        ((BlockMethod(), BlockEprnmr()), (True, True)),
        ((BlockScf(),), (False,)),
    ],
)
def test_has_block(calc: Calculator, blocks: tuple, expected: tuple):
    """Test for Input.has_blocks() with different combinations of blocks and expected results"""
    assert calc.input.has_blocks(*blocks) == expected


def test_get_block_empty(empty_calc: Calculator):
    """Test for Input.get_block() when no blocks have been added."""
    returned_block = empty_calc.input.get_blocks(BlockMethod)
    assert returned_block == {}


def test_get_block(empty_calc: Calculator):
    """Test for Input.get_blocks()."""
    test_block = BlockScf()
    empty_calc.input.add_blocks(test_block)
    assert empty_calc.input.get_blocks(BlockScf) == {BlockScf: test_block}


def test_get_blocks_create_missing(empty_calc: Calculator):
    """Test for Input.get_blocks() with create_missing = True."""
    returned_blocks = empty_calc.input.get_blocks(BlockScf, create_missing=True)
    assert BlockScf in returned_blocks


def test_clear_blocks(calc: Calculator):
    """Test for Input.clear_blocks()."""
    calc.input.clear_blocks()
    assert not calc.input.blocks


def test_clear_blocks_strict(empty_calc: Calculator):
    """Test for Input.clear_blocks() with strict = True."""
    with pytest.raises(ValueError):
        empty_calc.input.clear_blocks(strict=True)
