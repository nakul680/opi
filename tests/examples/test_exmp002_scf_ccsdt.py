import pytest

from examples.exmp002_scf_ccsdt.job import run_exmp002
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp002_scf(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp002)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp002(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.get_final_energy()
    assert output.get_energies()["MDCI(SD(T))"].correnergy[0][0]
