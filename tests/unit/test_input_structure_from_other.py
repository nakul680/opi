# import pytest
#
# from opi.core import Calculator
# from opi.input.structures import structure, Structure
# from opi.utils.element import Element
#
#
# @pytest.fixture
# def symbol_list_str():
#     symbol_list = ["O","H","H"]
#     return symbol_list
#
# @pytest.fixture
# def symbol_list_int():
#     symbol_list = [8,1,1]
#     return symbol_list
#
# @pytest.fixture
# def coord_list():
#     coord_list = [(-3.56626,1.77639,0.00000),(-2.59626,1.77639,0.00000),(-3.88959,1.36040,-0.81444)]
#     return coord_list
#
# # @pytest.fixture
# # def empty_calc():
# #     empty_calc = Calculator("test", version_check=False)
# #     return empty_calc
#
# @pytest.mark.parametrize(
#
# )
# def test_structure_from_lists(symbol_list_str, coord_list):
#     test_structure = Structure.from_lists(symbol_list_str, coord_list)
#     assert isinstance(test_structure, Structure)
#
#
# def test_structure_from_lists_int_symbols(symbol_list_int, coord_list):
#     test_structure = Structure.from_lists(symbol_list_int, coord_list)
#     assert isinstance(test_structure, Structure)
#
#
# @pytest.mark.parametrize(
#     "symbol_lists",
#     [
#         symbol_list_int,
#         symbol_list_str,
#
#     ]
# )
# def test_structure_from_lists_correct_num_atoms(symbol_lists, coord_list):
#     test_structure = Structure.from_lists(symbol_lists,coord_list)
#     assert len(test_structure.atoms) == 3
#
#
#
# def test_structure_from_list_mismatched_length(symbol_list_str, coord_list, empty_calc):
#     symbol_list = symbol_list_str[:-1]
#     with pytest.raises(ValueError):
#         Structure.from_lists(symbol_list, coord_list)
#
#
#
#
#
#
#
#
#
#
