import pytest

from examples.exmp028_nevpt2.job import run_exmp028
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp028_nevp2(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp028)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp028(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.results_properties.geometries[0].energy[1].totalenergy[0][0]
