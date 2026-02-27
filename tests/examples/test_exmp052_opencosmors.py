import pytest

from examples.exmp052_opencosmors.job import run_exmp052
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp052_opencosmors(example_input_file, tmp_path) -> None:
    """Run OpenCOSMO-RS task."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp052)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output_object = run_exmp052(structure=structure, working_dir=tmp_path)

    free_solvation_energy = output_object.get_free_solvation_energy_opencosmors()

    assert isinstance(free_solvation_energy, float)
