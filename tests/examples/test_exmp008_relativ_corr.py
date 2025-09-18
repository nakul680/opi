import pytest

from examples.exmp008_relativ_corr.job import run_exmp008
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp008_relativ_corr(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp008)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp008(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
