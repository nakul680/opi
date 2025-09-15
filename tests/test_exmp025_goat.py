from examples.exmp025_goat.job import run_exmp025


def test_exmp025_goat(cleanup_run):
    output = run_exmp025()
    assert output.terminated_normally()
