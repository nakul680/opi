import pytest

from examples.exmp013_bs.job import run_exmp013


@pytest.mark.examples
@pytest.mark.orca
def test_exmp013_bs(cleanup_run):
    output = run_exmp013()

    assert output.terminated_normally()
