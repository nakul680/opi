import pytest

from opi.core import Calculator
from opi.input.blocks import Block, BlockEprnmr, BlockMethod, BlockScf, Nuclei, NucleiFlag
from opi.utils.element import Element

"""
This module contains tests for block-related operations including:
- Addition of blocks
- Removal of blocks
- Getting of blocks
- Checking whether block exists in a `Calculator` object
- Clearing all blocks
- Merging of blocks (`Block.__or__` and the default merge-on-add behavior of `Input.add_blocks()`)
"""


@pytest.fixture
def empty_calc():
    """An empty instance of `Calculator`."""
    return Calculator("test", version_check=False)


@pytest.fixture
def calc():
    """An instance of `Calculator` with multiple instances of `Block`."""
    calc = Calculator("test", version_check=False)
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


@pytest.fixture
def empty_test_block():
    """An empty instance of `Block`."""
    return BlockScf()


@pytest.fixture
def calc_with_test_block(empty_test_block):
    """An instance of `Calculator` with an empty test block."""
    calc = Calculator("test", version_check=False)
    calc.input.add_blocks(empty_test_block)
    return calc


@pytest.fixture(
    params=[
        (
            BlockEprnmr(
                gtensor=True,
                nuclei=Nuclei(
                    atom=Element.HYDROGEN, flags=NucleiFlag(adip=True, aiso=True, aorb=True)
                ),
            ),
        ),
        (
            BlockEprnmr(
                gtensor=True,
                nuclei=Nuclei(
                    atom=Element.HYDROGEN, flags=NucleiFlag(adip=True, aiso=True, aorb=True)
                ),
            ),
            BlockMethod(d3s6=0.64, d3a1=0.3065),
        ),
    ]
)
def blocks(request) -> tuple:
    """Provide different block combinations for parameterized testing."""
    return request.param


@pytest.mark.unit
@pytest.mark.input
def test_add_blocks(empty_calc: Calculator, blocks: tuple):
    """Test for `Input.add_blocks()` with singular and multiple blocks."""
    empty_calc.input.add_blocks(*blocks)
    assert empty_calc.input.has_blocks(*blocks)


@pytest.mark.unit
@pytest.mark.input
def test_add_blocks_strict(calc: Calculator, blocks: tuple):
    """Test for `Input.add_blocks()` with `strict=True`. When `strict=True`, a `ValueError` should be raised
    if that Block instance has already been added."""
    with pytest.raises(ValueError):
        calc.input.add_blocks(*blocks, strict=True)


@pytest.mark.unit
@pytest.mark.input
def test_add_blocks_overwrite(calc: Calculator):
    """Test for `Input.add_blocks()` with `overwritten=True`. When `overwritten=True`, the existing `Block` instance
    should be overwritten if it exists."""
    calc.input.add_blocks(BlockMethod(d3s6=0.75), overwrite=True)

    assert calc.input.blocks[BlockMethod].d3s6 == 0.75


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize(
    "blocks,expected",
    [
        ((BlockEprnmr(),), (False,)),
        ((BlockEprnmr(), BlockMethod()), (False, False)),
    ],
)
def test_remove_block(calc: Calculator, blocks: tuple, expected: tuple):
    """Test for `Input.remove_blocks()`.
    Test for singular and multiple blocks."""
    calc.input.remove_blocks(*blocks)
    assert calc.input.has_blocks(*blocks) == expected


@pytest.mark.unit
@pytest.mark.input
def test_remove_blocks_strict(calc: Calculator, empty_test_block: Block):
    """Test for `Input.remove_blocks()` with `strict = True`."""
    with pytest.raises(ValueError):
        calc.input.remove_blocks(empty_test_block, strict=True)


@pytest.mark.unit
@pytest.mark.input
def test_has_block_empty_calc(empty_calc: Calculator, empty_test_block: Block):
    """Test for `Input.has_blocks()` when no blocks have been added."""
    calc = empty_calc
    assert calc.input.has_blocks(empty_test_block) == (False,)


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize(
    "blocks, expected",
    [
        ((BlockMethod(),), (True,)),
        ((BlockMethod(), BlockEprnmr()), (True, True)),
        ((BlockScf(),), (False,)),
    ],
)
def test_has_block(calc: Calculator, blocks: tuple, expected: tuple):
    """Test for `Input.has_blocks()` with different combinations of blocks and expected results"""
    assert calc.input.has_blocks(*blocks) == expected


@pytest.mark.unit
@pytest.mark.input
def test_get_block_empty(empty_calc: Calculator):
    """Test for `Input.get_block()` when no blocks have been added."""
    returned_block = empty_calc.input.get_blocks(BlockMethod)
    assert not returned_block


@pytest.mark.unit
@pytest.mark.input
def test_get_block(calc_with_test_block: Calculator, empty_test_block: Block):
    """Test for `Input.get_blocks()`."""
    type_instance = type(empty_test_block)
    assert calc_with_test_block.input.get_blocks(type_instance) == {type_instance: empty_test_block}


@pytest.mark.unit
@pytest.mark.input
def test_get_blocks_create_missing(empty_calc: Calculator, empty_test_block: Block):
    """Test for `Input.get_blocks()` with `create_missing=True`."""
    type_instance = type(empty_test_block)
    returned_blocks = empty_calc.input.get_blocks(type_instance, create_missing=True)
    assert BlockScf in returned_blocks


@pytest.mark.unit
@pytest.mark.input
def test_clear_blocks(calc: Calculator):
    """Test for `Input.clear_blocks()`."""
    calc.input.clear_blocks()
    assert not calc.input.blocks


@pytest.mark.unit
@pytest.mark.input
def test_clear_blocks_strict(empty_calc: Calculator):
    """Test for `Input.clear_blocks()` with `strict=True`."""
    with pytest.raises(ValueError):
        empty_calc.input.clear_blocks(strict=True)


# ---------------------------------------------------------------------------
# `Block.__or__` (merging two `Block` instances directly)
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.input
def test_block_or_combines_disjoint_fields():
    """Test for `Block.__or__()`: fields set on only one side are both present in the merge."""
    left = BlockScf(maxiter=100)
    right = BlockScf(convergence="tight")

    merged = left | right

    assert merged.maxiter == 100
    assert merged.convergence == "tight"


@pytest.mark.unit
@pytest.mark.input
def test_block_or_other_takes_precedence_on_conflict():
    """Test for `Block.__or__()`: when both sides set the same field, `other`'s value wins."""
    left = BlockScf(maxiter=100)
    right = BlockScf(maxiter=200)

    merged = left | right

    assert merged.maxiter == 200


@pytest.mark.unit
@pytest.mark.input
def test_block_or_preserves_self_field_left_unset_by_other():
    """Test for `Block.__or__()`: a field left unset (`None`) on `other` does not clobber the
    value already present on `self`."""
    left = BlockScf(maxiter=100)
    right = BlockScf(convergence="tight")

    merged = left | right

    assert merged.maxiter == 100
    assert left.maxiter == 100


@pytest.mark.unit
@pytest.mark.input
def test_block_or_returns_new_instance_without_mutating_operands():
    """Test for `Block.__or__()`: the result is a new `Block` instance of the same type; neither
    operand is mutated."""
    left = BlockScf(maxiter=100)
    right = BlockScf(convergence="tight")

    merged = left | right

    assert isinstance(merged, BlockScf)
    assert merged is not left
    assert merged is not right
    assert left.convergence is None
    assert right.maxiter is None


@pytest.mark.unit
@pytest.mark.input
def test_block_or_nested_block_field_is_replaced_wholesale():
    """Test for `Block.__or__()`: a nested `BaseModel` field (e.g. `nuclei`) set on both sides is
    replaced wholesale by `other`'s value rather than being merged field-by-field."""
    left = BlockEprnmr(
        gtensor=1,
        nuclei=Nuclei(atom=Element.HYDROGEN, flags=NucleiFlag(adip=True, aiso=True)),
    )
    right = BlockEprnmr(nuclei=Nuclei(atom=Element.CARBON, flags=NucleiFlag(aorb=True)))

    merged = left | right

    assert merged.nuclei == right.nuclei
    assert merged.gtensor == 1  # preserved from `left`, untouched by `right`


@pytest.mark.unit
@pytest.mark.input
def test_block_or_arbitrary_options_are_not_preserved():
    """Test for `Block.__or__()`: arbitrary options added via `add_option()` live on a private,
    non-model attribute and are dropped by the merge (`model_dump()` does not include them), even
    if only one side ever set them."""
    left = BlockScf(maxiter=100)
    left.add_option("foo", "bar")
    right = BlockScf(convergence="tight")

    merged = left | right

    assert not merged.has_option("foo")


@pytest.mark.unit
@pytest.mark.input
def test_block_or_other_default_overrides_self_explicit_value():
    """Test for `Block.__or__()`: `aftercoord` has a non-`None` default (`False`), so it is always
    included by `model_dump(exclude_none=True)`. As a result, `other`'s default silently overrides
    an explicit value set on `self`, even though `other` never touched it."""
    left = BlockScf(maxiter=100, aftercoord=True)
    right = BlockScf(convergence="tight")  # aftercoord left at its default (False)

    merged = left | right

    assert merged.aftercoord is False


# ---------------------------------------------------------------------------
# `Input.add_blocks()` merge-on-add default behavior
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.input
def test_add_blocks_merges_existing_block_by_default(calc: Calculator):
    """Test for `Input.add_blocks()`: adding a block of a type that is already present, without
    `strict` or `overwrite`, merges it into the existing block instead of replacing it wholesale."""
    calc.input.add_blocks(BlockMethod(d3s6=0.75))

    merged = calc.input.blocks[BlockMethod]
    assert merged.d3s6 == 0.75  # new value takes precedence
    assert merged.d3a1 == 0.3065  # preserved from the previously-added block
    assert merged.d3s8 == 0.9147
    assert merged.d3a2 == 5.0570


@pytest.mark.unit
@pytest.mark.input
def test_add_blocks_merge_combines_multiple_new_blocks_of_same_type(empty_calc: Calculator):
    """Test for `Input.add_blocks()`: passing several blocks of the same type in a single call
    merges them sequentially, even when none was previously present."""
    empty_calc.input.add_blocks(BlockMethod(d3s6=0.64), BlockMethod(d3a1=0.3065))

    assert len(empty_calc.input.blocks) == 1
    merged = empty_calc.input.blocks[BlockMethod]
    assert merged.d3s6 == 0.64
    assert merged.d3a1 == 0.3065


@pytest.mark.unit
@pytest.mark.input
def test_add_blocks_merge_produces_object_distinct_from_both_inputs(empty_calc: Calculator):
    """Test for `Input.add_blocks()`: the stored, merged block is a new instance rather than
    either of the two blocks that were merged."""
    first = BlockMethod(d3s6=0.64)
    second = BlockMethod(d3a1=0.3065)
    empty_calc.input.add_blocks(first, second)

    merged = empty_calc.input.blocks[BlockMethod]
    assert merged is not first
    assert merged is not second


@pytest.mark.unit
@pytest.mark.input
def test_add_blocks_merge_does_not_mutate_previously_stored_block(calc: Calculator):
    """Test for `Input.add_blocks()`: merging on add replaces the stored block with a new
    instance; the block object that was stored before does not get its fields mutated in place."""
    previously_stored = calc.input.blocks[BlockMethod]

    calc.input.add_blocks(BlockMethod(d3s6=0.75))

    assert previously_stored.d3s6 == 0.64
    assert calc.input.blocks[BlockMethod] is not previously_stored
