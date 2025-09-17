import pytest

from examples.exmp039_neb.job import run_exmp039


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp039_neb(cleanup_run):
    output = run_exmp039()

    assert output.terminated_normally()
