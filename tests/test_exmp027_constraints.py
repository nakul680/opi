from examples.exmp027_constraints.job import run_exmp027


def test_exmp027_scan(cleanup_run):
    output_bond = run_exmp027()

    assert output_bond.terminated_normally()
