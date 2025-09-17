import pytest

from examples.exmp018_cipsi.job import run_exmp018


@pytest.mark.examples
@pytest.mark.orca
def test_exmp018_cipsi(cleanup_run):
    output = run_exmp018()
    assert output.terminated_normally()
