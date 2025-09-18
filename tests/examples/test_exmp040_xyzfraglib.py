import pytest

from examples.exmp040_xzyfraglib.job import run_exmp040


@pytest.mark.examples
@pytest.mark.orca
def test_exmp040_xyzfraglib(example_input_file, tmp_path) -> None:
    output = run_exmp040(working_dir=tmp_path)

    assert output.terminated_normally()
