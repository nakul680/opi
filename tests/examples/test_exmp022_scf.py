import pytest

from examples.exmp022_scf.job import run_exmp022
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp022_scf(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp022)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp022(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.results_properties.geometries[0].dft_energy.finalen
