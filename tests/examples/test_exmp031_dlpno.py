import pytest

from examples.exmp031_dlpno.job import run_exmp031
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp031_dlpno(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp031)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp031(structure=structure, working_dir=tmp_path)
    assert output.terminated_normally()
