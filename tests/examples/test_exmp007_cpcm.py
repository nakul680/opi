import pytest

from examples.exmp007_cpcm.job import run_exmp007


@pytest.mark.examples
@pytest.mark.orca
def test_exmp007_cpcm(cleanup_run):
    output = run_exmp007()

    assert output.terminated_normally()
    assert output.results_properties.geometries
    assert output.results_properties.geometries[0].dft_energy.finalen
    assert output.results_properties.geometries[0].solvation_details.solvent
    assert output.results_properties.geometries[0].solvation_details.epsilon
    assert output.results_properties.geometries[0].solvation_details.npoints
    assert output.results_properties.geometries[0].solvation_details.cpcmdielenergy
