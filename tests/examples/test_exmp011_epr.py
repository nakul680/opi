import pytest

from examples.exmp011_epr.job import run_exmp011
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp011_epr(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp011)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp011(structure=structure, working_dir=tmp_path)
    assert output.terminated_normally()
