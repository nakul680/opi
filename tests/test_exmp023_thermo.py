from examples.exmp023_thermo.job import run_exmp023


def test_exmp023_thermo(cleanup_run):
    output = run_exmp023()

    assert output.terminated_normally()
    assert output.results_properties.geometries[0].thermochemistry_energies[0].freeenergyg
    assert output.results_properties.geometries[0].thermochemistry_energies[0].temperature
    assert output.results_properties.geometries[0].dft_energy.finalen
