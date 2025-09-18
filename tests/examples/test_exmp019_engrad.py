import pytest

from examples.exmp019_engrad.job import run_exmp019
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp019_engrad(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp019)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp019(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.results_properties.geometries[0].single_point_data.finalenergy
    assert output.results_properties.geometries[0].energy[0].totalenergy[0][0]
