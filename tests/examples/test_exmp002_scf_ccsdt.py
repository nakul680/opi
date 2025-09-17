import pytest

from examples.exmp002_scf_ccsdt.job import run_exmp002


@pytest.mark.examples
@pytest.mark.orca
def test_exmp002_scf(cleanup_run) -> None:
    output = run_exmp002()

    assert output.terminated_normally()
    assert output.get_final_energy()
    assert output.get_energies()["MDCI(SD(T))"].correnergy[0][0]
