import pytest

from examples.exmp010_uvvis.job import run_exmp010
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp010_uvvis(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp010)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp010(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
