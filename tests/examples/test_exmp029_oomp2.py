import pytest

from examples.exmp029_oomp2.job import run_exmp029
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp029_oomp2(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp029)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp029(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.results_properties.geometries[0].energy[1].totalenergy[0][0]
