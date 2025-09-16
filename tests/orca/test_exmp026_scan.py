from examples.exmp026_scan.job import run_exmp026


def test_exmp026_scan(cleanup_run):
    output_bond = run_exmp026()

    assert output_bond.terminated_normally()
