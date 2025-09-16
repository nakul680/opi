from examples.exmp034_strucfile.job import run_exmp034


def test_exmp034_mo_setters(cleanup_run):
    output = run_exmp034()

    assert output.terminated_normally()
    assert output.get_final_energy()
