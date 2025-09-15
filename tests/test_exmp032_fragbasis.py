from examples.exmp032_fragbasis.job import run_exmp032


def test_exmp032_fragbasis(cleanup_run):
    output = run_exmp032()

    assert output.terminated_normally()
