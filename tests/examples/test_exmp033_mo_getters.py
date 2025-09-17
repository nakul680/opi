import pytest

from examples.exmp033_mo_getters.job import run_exmp033


@pytest.mark.examples
@pytest.mark.orca
def test_exmp033_mo_getters(cleanup_run):
    output = run_exmp033()

    assert output.terminated_normally()
