from examples.exmp022_scf.job import run_exmp022


def test_exmp022_scf(cleanup_run):
    output = run_exmp022()

    assert output.terminated_normally()
    assert output.results_properties.geometries[0].dft_energy.finalen
