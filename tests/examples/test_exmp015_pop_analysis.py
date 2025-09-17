import pytest

from examples.exmp015_pop_analysis.job import run_exmp015


@pytest.mark.examples
@pytest.mark.orca
def test_exmp015_pop_analysis(cleanup_run):
    output = run_exmp015()

    assert output.terminated_normally()
