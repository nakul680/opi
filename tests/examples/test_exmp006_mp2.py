import pytest

from examples.exmp006_mp2.job import run_exmp006
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp006_mp2(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp006)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp006(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.results_properties.geometries
    assert output.results_properties.geometries[0].energy[1].refenergy[0][0]
    assert output.results_properties.geometries[0].energy[1].correnergy[0][0]
    assert output.results_properties.geometries[0].energy[1].totalenergy[0][0]
