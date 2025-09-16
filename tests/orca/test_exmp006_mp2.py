import pytest

from examples.exmp006_mp2.job import run_exmp006


@pytest.mark.orca
def test_exmp006_mp2(cleanup_run):
    output = run_exmp006()

    assert output.terminated_normally()
    assert output.results_properties.geometries
    assert output.results_properties.geometries[0].energy[1].refenergy[0][0]
    assert output.results_properties.geometries[0].energy[1].correnergy[0][0]
    assert output.results_properties.geometries[0].energy[1].totalenergy[0][0]
