import pytest

from examples.exmp038_integrals.job import run_exmp038
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp038_integrals(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp038)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp038(structure=structure, working_dir=tmp_path)
    assert output.terminated_normally()
    assert output.scf_converged()
    assert output.get_int_overlap(recreate_json=True) is not None
    assert output.get_int_hcore(recreate_json=True) is not None
    assert output.get_int_f(recreate_json=True) is not None
    assert output.get_int_j(recreate_json=True) is not None
    assert output.get_int_k(recreate_json=True) is not None
