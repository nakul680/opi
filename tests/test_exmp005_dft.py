from examples.exmp005_dft.job import run_exmp005


def test_exmp005_dft(cleanup_run):
    output = run_exmp005()

    assert output.terminated_normally()
    assert output.results_properties.geometries
    assert output.results_properties.geometries[0].single_point_data.finalenergy
    assert output.results_properties.geometries[0].vdw_correction.vdw
