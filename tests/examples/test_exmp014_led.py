import pytest

from examples.exmp014_led.job import run_exmp014


@pytest.mark.examples
@pytest.mark.orca
def test_exmp014_led(cleanup_run):
    output = run_exmp014()

    assert output.terminated_normally()
