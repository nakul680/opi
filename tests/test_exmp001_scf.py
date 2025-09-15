from examples.exmp001_scf.job import run_exmp001


def test_exmp001_scf(cleanup_run) -> None:
    output = run_exmp001()

    assert output.terminated_normally()
    assert output.scf_converged()
    assert output.get_final_energy()  # assert final energy is not None
    assert (
        output.get_final_energy()
        == output.results_properties.geometries[0].single_point_data.finalenergy
        == (
            output.results_properties.geometries[0].energy[0].totalenergy[0][0]
            + output.results_properties.geometries[0].vdw_correction.vdw
        )
    )
