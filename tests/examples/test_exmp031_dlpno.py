import pytest

from examples.exmp031_dlpno.job import run_exmp031


@pytest.mark.examples
@pytest.mark.orca
def test_exmp031_dlpno(cleanup_run):
    output = run_exmp031()
    assert output.terminated_normally()
