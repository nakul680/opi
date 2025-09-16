import pytest

from examples.exmp002_scf_ccsdt.job import run_exmp002


@pytest.mark.orca
def test_exmp002_scf(cleanup_run) -> None:
    output = run_exmp002()

    assert output.terminated_normally()
    assert output.results_properties.geometries[0].single_point_data.finalenergy
    assert output.results_properties.geometries[0].energy[1].correnergy[0][0]
