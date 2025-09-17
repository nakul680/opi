import pytest

from examples.exmp045_existing_calc.job import run_exmp045


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp045_existing_calc(cleanup_run):
    output = run_exmp045()

    assert output.terminated_normally()