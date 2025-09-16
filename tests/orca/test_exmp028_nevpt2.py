from examples.exmp028_nevpt2.job import run_exmp028


def test_exmp028_nevp2(cleanup_run):
    output = run_exmp028()

    assert output.terminated_normally()
    assert output.results_properties.geometries[0].energy[1].totalenergy[0][0]
