from examples.exmp015_pop_analysis.job import run_exmp015


def test_exmp015_pop_analysis(cleanup_run):
    output = run_exmp015()

    assert output.terminated_normally()
