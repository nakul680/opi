import pytest

from examples.exmp010_uvvis.job import run_exmp010


@pytest.mark.examples
@pytest.mark.orca
def test_exmp010_uvvis(cleanup_run):
    output = run_exmp010()

    assert output.terminated_normally()
