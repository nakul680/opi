# ruff: noqa: E402
import pytest

# > example44 requires ase, which is not installed by default
# > skip test if ase is not available
pytest.importorskip("ase", reason="requires ase")
from examples.exmp044_from_ase.job import run_exmp044


@pytest.mark.ase
def test_exmp044_from_ase(cleanup_run):
    output = run_exmp044()

    assert output.terminated_normally()
    assert output.get_final_energy()
