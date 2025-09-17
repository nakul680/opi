import pytest

from examples.exmp042_element.job import run_exmp042


@pytest.mark.examples
def test_exmp042_element(cleanup_run):
    run_exmp042()
