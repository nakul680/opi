import pytest

from examples.exmp026_scan.job import run_exmp026
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp026_scan(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp026)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp026(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
