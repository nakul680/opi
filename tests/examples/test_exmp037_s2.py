import pytest

from examples.exmp037_s2.job import run_exmp037
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp037_s2(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp037)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp037(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
