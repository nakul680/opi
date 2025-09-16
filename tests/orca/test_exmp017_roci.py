from examples.exmp017_roci.job import run_exmp017


def test_exmp017_roci(cleanup_run):
    output = run_exmp017()
    assert output.terminated_normally()
