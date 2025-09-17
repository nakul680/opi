import pytest

from examples.exmp016_autoci.job import run_exmp016


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp016_autoci(cleanup_run):
    output = run_exmp016()
    assert output.terminated_normally()
