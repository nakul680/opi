import pytest

from examples.exmp011_epr.job import run_exmp011


@pytest.mark.orca
def test_exmp011_epr(cleanup_run):
    output = run_exmp011()
    assert output.terminated_normally()
