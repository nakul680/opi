from examples.exmp009_rama.job import run_exmp009


def test_exmp009_rama(cleanup_run):
    output = run_exmp009()

    assert output.terminated_normally()
