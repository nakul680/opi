import pytest

from examples.exmp005_dft.job import run_exmp005
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp005_dft(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp005)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp005(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.results_properties.geometries
    assert output.results_properties.geometries[0].single_point_data.finalenergy
    assert output.results_properties.geometries[0].vdw_correction.vdw
