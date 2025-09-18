import pytest

from examples.exmp009_rama.job import run_exmp009
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp009_rama(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp009)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp009(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
