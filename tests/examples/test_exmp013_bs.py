import pytest

from examples.exmp013_bs.job import run_exmp013
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp013_bs(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp013)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp013(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
