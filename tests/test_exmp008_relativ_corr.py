from examples.exmp008_relativ_corr.job import run_exmp008


def test_exmp008_relativ_corr(cleanup_run):
    output = run_exmp008()

    assert output.terminated_normally()
