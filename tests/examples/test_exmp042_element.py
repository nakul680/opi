import pytest

from examples.exmp042_element.job import run_exmp042
from opi.input.structures import Structure


@pytest.mark.examples
def test_exmp042_element(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp042)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    run_exmp042(structure=structure, working_dir=tmp_path)
