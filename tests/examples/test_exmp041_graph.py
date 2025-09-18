import pytest

from examples.exmp041_graph.job import run_exmp041
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp041_graph(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp041)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp041(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
