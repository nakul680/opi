from examples.exmp036_solvator.job import run_exmp036


def test_exmp036_solvator(cleanup_run):
    output = run_exmp036()

    assert output.terminated_normally()
