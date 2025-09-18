import pytest

from examples.exmp021_basis.job import run_exmp021
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp021_basis(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp021)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp021(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.results_properties.geometries[0].dft_energy.finalen
