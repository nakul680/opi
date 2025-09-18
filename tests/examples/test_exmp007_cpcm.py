import pytest

from examples.exmp007_cpcm.job import run_exmp007
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp007_cpcm(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp007)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp007(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.results_properties.geometries
    assert output.results_properties.geometries[0].dft_energy.finalen
    assert output.results_properties.geometries[0].solvation_details.solvent
    assert output.results_properties.geometries[0].solvation_details.epsilon
    assert output.results_properties.geometries[0].solvation_details.npoints
    assert output.results_properties.geometries[0].solvation_details.cpcmdielenergy
