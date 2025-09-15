from examples.exmp042_element.job import run_exmp042


def test_exmp042_element(cleanup_run):
    output = run_exmp042()

    assert output.terminated_normally()
