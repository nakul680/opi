# ruff: noqa: E402
import pytest

from opi.input.structures import Structure

# > example44 requires ase, which is not installed by default
# > skip test if ase is not available
pytest.importorskip("ase", reason="requires ase")
from examples.exmp044_from_ase.job import run_exmp044


@pytest.mark.ase
@pytest.mark.examples
@pytest.mark.orca
def test_exmp044_from_ase(example_input_file, tmp_path) -> None:
    # > Get example input file
    input_file = example_input_file(run_exmp044)
    # > Read structure
    structure = Structure.from_xyz(input_file)
    # > Run the example with the structure
    output = run_exmp044(structure=structure, working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.get_final_energy()
