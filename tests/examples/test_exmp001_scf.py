import pytest

from examples.exmp001_scf.job import run_exmp001
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp001_scf(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp001)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp001(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.scf_converged()
    assert output.get_final_energy()
    assert (
        output.get_final_energy()
        == output.results_properties.geometries[-1].single_point_data.finalenergy
    )
