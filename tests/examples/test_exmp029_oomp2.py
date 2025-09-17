import pytest

from examples.exmp029_oomp2.job import run_exmp029


@pytest.mark.examples
@pytest.mark.orca
def test_exmp029_oomp2(cleanup_run):
    output = run_exmp029()

    assert output.terminated_normally()
    assert output.results_properties.geometries[0].energy[1].totalenergy[0][0]
