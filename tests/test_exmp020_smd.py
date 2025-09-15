from examples.exmp020_smd.job import run_exmp020


def test_exmp020_smd(cleanup_run):
    output = run_exmp020()

    assert output.terminated_normally()
