import pytest

from examples.exmp004_freq.job import run_exmp004
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp004_freq(example_input_file, tmp_path) -> None:
    """Ensure frequency example runs successfully and produces a final energy and free energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp004)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp004(structure=structure, working_dir=tmp_path)

    # Assert final energy
    assert output.get_final_energy()
    # Assert free energy
    assert output.get_free_energy()
    # Assert zero-point energy
    assert output.get_zpe()
    # Assert enthalpy
    assert output.get_enthalpy()
    # Assert entropy
    assert output.get_entropy()
    # Assert free energy difference
    assert output.get_free_energy_delta()
