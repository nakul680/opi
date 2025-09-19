import pytest

from examples.exmp035_moplot.job import run_exmp035
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp035_moplot(example_input_file, tmp_path) -> None:
    """Ensure MO plot example runs successfully and produces an energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp035)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp035(structure=structure, working_dir=tmp_path)

    # Assert final energy
    assert output.get_final_energy()
