import pytest

from examples.exmp035_moplot.job import run_exmp035


@pytest.mark.examples
@pytest.mark.orca
def test_exmp035_moplot():
    output = run_exmp035()

    assert output.terminated_normally()
