import pytest

from examples.exmp034_strucfile.job import run_exmp034


@pytest.mark.examples
@pytest.mark.orca
def test_exmp034_mo_setters(tmp_path) -> None:
    output = run_exmp034(working_dir=tmp_path)

    assert output.terminated_normally()
    assert output.get_final_energy()
