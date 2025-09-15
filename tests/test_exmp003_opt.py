from examples.exmp003_opt.job import run_exmp003
from opi.input.structures import Structure


def test_exmp003_opt(cleanup_run) -> None:
    output = run_exmp003()
    assert output.terminated_normally()
    assert output.scf_converged()
    assert output.geometry_optimization_converged()

    assert isinstance(len(output.results_properties.geometries), int)
    assert output.results_properties.geometries[-1].single_point_data.finalenergy
    assert output.get_structure(), Structure
