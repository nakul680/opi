import pytest

from examples.exmp013_bs.job import run_exmp013
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp013_bs(example_input_file, tmp_path) -> None:
    """Ensure broken symmetry example runs successfully and produces a final energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp013)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp013(structure=structure, working_dir=tmp_path)

    # Assert final energy
    assert output.get_final_energy()

    # Assert S²
    assert output.get_s2() is not None
