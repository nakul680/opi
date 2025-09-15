from examples.exmp024_blocks.job import run_exmp024


def test_exmp024(cleanup_run):
    output = run_exmp024()

    assert output.terminated_normally()
    assert output.results_properties.geometries[0].single_point_data.finalenergy
