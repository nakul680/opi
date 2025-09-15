from examples.exmp019_engrad.job import run_exmp019


def test_exmp019_engrad(cleanup_run):
    output = run_exmp019()

    assert output.terminated_normally()
    assert output.results_properties.geometries[0].single_point_data.finalenergy
    assert output.results_properties.geometries[0].energy[0].totalenergy[0][0]
