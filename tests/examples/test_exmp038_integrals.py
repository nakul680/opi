import pytest

from examples.exmp038_integrals.job import run_exmp038


@pytest.mark.examples
@pytest.mark.orca
def test_exmp038_integrals(cleanup_run):
    output = run_exmp038()
    assert output.terminated_normally()
    assert output.scf_converged()
    assert output.get_int_overlap(recreate_json=True) is not None
    assert output.get_int_hcore(recreate_json=True) is not None
    assert output.get_int_f(recreate_json=True) is not None
    assert output.get_int_j(recreate_json=True) is not None
    assert output.get_int_k(recreate_json=True) is not None
