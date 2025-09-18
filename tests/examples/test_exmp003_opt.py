import pytest

from examples.exmp003_opt.job import run_exmp003
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp003_opt(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp003)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp003(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.scf_converged()
    assert output.geometry_optimization_converged()

    assert isinstance(len(output.results_properties.geometries), int)
    assert output.get_final_energy()
    assert output.get_structure(), Structure
