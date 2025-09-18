import pytest

from examples.exmp024_blocks.job import run_exmp024
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp024_blocks(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp024)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp024(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.results_properties.geometries[0].single_point_data.finalenergy
