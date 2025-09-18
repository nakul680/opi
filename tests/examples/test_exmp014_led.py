import pytest

from examples.exmp014_led.job import run_exmp014
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp014_led(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp014)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp014(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
