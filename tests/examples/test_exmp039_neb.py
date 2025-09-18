import pytest

from examples.exmp039_neb.job import run_exmp039


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp039_neb(example_input_file, tmp_path) -> None:
    # > Run the example with the structure
    output = run_exmp039(working_dir=tmp_path)

    assert output.terminated_normally()
