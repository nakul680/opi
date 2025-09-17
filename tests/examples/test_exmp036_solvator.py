import pytest

from examples.exmp036_solvator.job import run_exmp036


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp036_solvator(cleanup_run):
    output = run_exmp036()

    assert output.terminated_normally()
