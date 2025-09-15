from examples.exmp012_nmr.job import run_exmp012


def test_exmp012_nmr(cleanup_run):
    output = run_exmp012()

    assert output.terminated_normally()
