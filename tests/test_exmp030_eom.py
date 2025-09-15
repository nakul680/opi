from examples.exmp030_eom.job import run_exmp030


def test_exmp030_eom(cleanup_run):
    output = run_exmp030()
    assert output.terminated_normally()
