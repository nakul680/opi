import pytest

from examples.exmp041_graph.job import run_exmp041


@pytest.mark.examples
@pytest.mark.orca
def test_exmp041_graph(cleanup_run):
    output = run_exmp041()

    assert output.terminated_normally()
