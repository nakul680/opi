import pytest

from examples.exmp017_roci.job import run_exmp017


@pytest.mark.examples
@pytest.mark.orca
def test_exmp017_roci(cleanup_run):
    output = run_exmp017()
    assert output.terminated_normally()
