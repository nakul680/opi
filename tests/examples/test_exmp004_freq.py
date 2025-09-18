import pytest

from examples.exmp004_freq.job import run_exmp004
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp004_freq(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp004)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp004(structure=structure, working_dir=tmp_path)
    assert output.terminated_normally()
    assert output.results_properties.geometries
    assert output.get_final_energy()
    assert output.results_properties.geometries[0].thermochemistry_energies[0].temperature
    assert output.get_free_energy()
    assert output.get_zpe()
    assert output.get_enthalpy()
    assert output.get_entropy()
    assert output.get_free_energy_delta()
