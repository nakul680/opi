import pytest

from examples.exmp001_scf.job import run_exmp001
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.generator_test
def test_exmp001_scf(example_input_file, tmp_path, json_files_exporter) -> None:
    """Ensure SCF example runs successfully and produces a final energy."""

    # Get input file from example folder
    input_file = example_input_file(run_exmp001)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp001(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0

    # optional export to git-tracked folder (no-op unless flag is used)
    json_files_exporter.export_jsons_from(tmp_path)
