from examples.exmp043_dummy_atom.job import run_exmp043


def test_exmp043_dummy_atom(cleanup_run):
    output = run_exmp043()

    assert output.terminated_normally()
    assert output.get_final_energy()
