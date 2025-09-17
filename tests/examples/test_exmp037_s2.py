import pytest

from examples.exmp037_s2.job import run_exmp037


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp037_s2(cleanup_run):
    output = run_exmp037()

    assert output.terminated_normally()
