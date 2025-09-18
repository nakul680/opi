import pytest

from examples.exmp043_dummy_atom.job import run_exmp043
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp043_dummy_atom(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp043)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp043(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.get_final_energy()
