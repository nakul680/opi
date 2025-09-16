import pytest

from examples.exmp004_freq.job import run_exmp004


@pytest.mark.orca
def test_exmp004_freq(cleanup_run):
    output = run_exmp004()
    assert output.terminated_normally()
    assert output.results_properties.geometries
    assert output.get_final_energy()
    assert output.results_properties.geometries[0].thermochemistry_energies[0].temperature
    assert output.get_free_energy()
    assert output.get_zpe()
    assert output.get_enthalpy()
    assert output.get_entropy()
    assert output.get_free_energy_delta()
