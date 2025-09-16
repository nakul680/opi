from examples.exmp040_xzyfraglib.job import run_exmp040


def test_exmp040_xyzfraglib(cleanup_run):
    output = run_exmp040()

    assert output.terminated_normally()
