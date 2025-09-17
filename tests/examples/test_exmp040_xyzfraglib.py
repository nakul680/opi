import pytest

from examples.exmp040_xzyfraglib.job import run_exmp040


@pytest.mark.examples
@pytest.mark.orca
def test_exmp040_xyzfraglib(cleanup_run):
    output = run_exmp040()

    assert output.terminated_normally()
