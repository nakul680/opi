import pytest

from examples.exmp021_basis.job import run_exmp021


@pytest.mark.examples
@pytest.mark.orca
def test_exmp021_basis(cleanup_run):
    output = run_exmp021()

    assert output.terminated_normally()
    assert output.results_properties.geometries[0].dft_energy.finalen
