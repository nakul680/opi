import pytest

from examples.exmp023_thermo.job import run_exmp023
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp023_thermo(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp023)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp023(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.results_properties.geometries[0].thermochemistry_energies[0].freeenergyg
    assert output.results_properties.geometries[0].thermochemistry_energies[0].temperature
    assert output.results_properties.geometries[0].dft_energy.finalen
