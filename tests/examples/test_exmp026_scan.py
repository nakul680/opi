import pytest

from examples.exmp026_scan.job import run_exmp026


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp026_scan(cleanup_run):
    output_bond = run_exmp026()

    assert output_bond.terminated_normally()
