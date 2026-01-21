import glob
from pathlib import Path

import pytest

from opi.input.structures import Structure
from opi.output.core import Output
from opi.output.mo_data import MOData
from opi.output.models.json.gbw.gbw_results import GbwResults
from opi.output.models.json.gbw.properties.mo import MO
from opi.output.models.json.property.properties.dipole_moment import DipoleMoment
from opi.output.models.json.property.properties.energy import Energy
from opi.output.models.json.property.properties.hirshfeld_population_analysis import (
    HirshfeldPopulationAnalysis,
)
from opi.output.models.json.property.properties.mayer_population_analysis import (
    MayerPopulationAnalysis,
)
from opi.output.models.json.property.properties.mbis_population_analysis import (
    MbisPopulationAnalysis,
)
from opi.output.models.json.property.properties.mp2_energy import Mp2Energy
from opi.output.models.json.property.properties.polarizability import Polarizability
from opi.output.models.json.property.properties.population_analysis import (
    ChelpgPopulationAnalysis,
    LoewdinPopulationAnalysis,
    MullikenPopulationAnalysis,
)
from opi.output.models.json.property.properties.quadrupole_moment import QuadrupoleMoment
from opi.output.models.json.property.properties.scf_energy import ScfEnergy
from opi.output.models.json.property.property_results import PropertyResults

JSON_DIR = Path(__file__).parent.parent / "fixtures/json_files"


@pytest.fixture
def output_object_aborted() -> Output:
    output_object = Output(
        "abort",
        working_dir=Path(__file__).parent.parent / "fixtures/output_files",
        version_check=False,
    )
    return output_object


@pytest.fixture
def output_object_job() -> Output:
    output_object = Output(
        "job",
        working_dir=Path(__file__).parent.parent / "fixtures/output_files",
        version_check=False,
    )
    return output_object


@pytest.fixture
def output_object_nonexistent() -> Output:
    output_object = Output("random", version_check=False)
    return output_object


@pytest.fixture
def output_object_scf_failed() -> Output:
    output_object = Output(
        "failed_scf",
        working_dir=Path(__file__).parent.parent / "fixtures/output_files",
        version_check=False,
    )
    return output_object


@pytest.fixture
def output_object_geometry_opt_failed() -> Output:
    output_object = Output(
        "failed_geometry",
        working_dir=Path(__file__).parent.parent / "fixtures/output_files",
        version_check=False,
    )
    return output_object


@pytest.fixture
def output_object_geometry_opt() -> Output:
    output_object = Output(
        "geometry",
        working_dir=Path(__file__).parent.parent / "fixtures/output_files",
        version_check=False,
    )
    return output_object


@pytest.fixture
def output_object(request) -> Output:
    return request.getfixturevalue(request.param)


def make_output_fixtures(basename: str):
    @pytest.fixture
    def _fixture() -> Output:
        output_fixture = Output(basename=basename, working_dir=JSON_DIR, version_check=False)
        gbw_file = JSON_DIR / f"{basename}.json"
        if gbw_file.exists():
            # output_fixture.parse(read_gbw_json=True)
            output_fixture.gbw_json_files = [gbw_file]
        # else:
        #     output_fixture.parse(read_gbw_json=False)

        output_fixture.parse()

        return output_fixture

    return _fixture


seen = set()
for file in JSON_DIR.glob("*.json"):
    basename = file.stem
    basename = basename.split(".", 1)[0]

    if basename in seen:
        continue

    seen.add(basename)

    fixture_name = f"output_object_{basename}"
    globals()[fixture_name] = make_output_fixtures(basename)


@pytest.mark.unit
@pytest.mark.output
def test_load_gbw_result_from_json():
    files = [f for f in glob.glob(f"{JSON_DIR}/*.json") if not f.endswith(".property.json")]
    for f in files:
        gbw_result = GbwResults.from_json_file(Path(f))
        assert gbw_result is not None


@pytest.mark.unit
@pytest.mark.output
def test_load_property_result_from_json():
    for f in JSON_DIR.glob("*.property.json"):
        print(f"{f}\n")
        property_result = PropertyResults.from_json_file(Path(f))
        assert property_result is not None


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_values",
    [
        ("output_object_aborted", False),
        ("output_object_job", True),
        ("output_object_nonexistent", False),
    ],
    indirect=["output_object"],
)
def test_terminated_normally(output_object, expected_values: bool):
    """Test if `Output.terminated_normally()` returns correct values."""
    assert output_object.terminated_normally() == expected_values


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_values",
    [
        ("output_object_scf_failed", False),
        ("output_object_job", True),
        ("output_object_nonexistent", False),
    ],
    indirect=["output_object"],
)
def test_scf_converged(output_object: Output, expected_values: bool):
    """Test if `Output.scf_converged()` returns correct values."""
    assert output_object.scf_converged() == expected_values


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_values",
    [
        ("output_object_geometry_opt_failed", False),
        ("output_object_geometry_opt", True),
        ("output_object_nonexistent", False),
    ],
    indirect=["output_object"],
)
def test_geometry_optimization_converged(output_object: Output, expected_values: bool):
    """Test if `Output.geometry_optimization_converged()` returns correct values."""
    assert output_object.geometry_optimization_converged() == expected_values


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_values",
    [
        ("output_object_opt", "rhf"),
        ("output_object_roci", "rohf"),
    ],
    indirect=["output_object"],
)
def test_get_hftype(output_object: Output, expected_values: str):
    """Test to check if `Output.get_hftype()` returns expected value."""
    assert output_object.get_hftype() == expected_values


@pytest.mark.unit
@pytest.mark.output
def test_get_hftype_nonexistent(output_object_nonexistent: Output):
    """Test to check if `Output.get_hftype()` returns None when expected."""
    assert not output_object_nonexistent.get_hftype()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_values",
    [("output_object_opt", 0), ("output_object_roci", -1)],
    indirect=["output_object"],
)
def test_get_charge(output_object: Output, expected_values: int):
    """Test to check if `Output.get_charge()` returns expected values."""
    assert output_object.get_charge() == expected_values


@pytest.mark.unit
@pytest.mark.output
def test_get_charge_nonexistent(output_object_nonexistent: Output):
    """Test to check if `Output.get_charge()` returns None when expected."""
    assert not output_object_nonexistent.get_charge()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_values",
    [("output_object_opt", 1), ("output_object_roci", 2)],
    indirect=["output_object"],
)
def test_get_mult(output_object: Output, expected_values: int):
    """Test to check if `Output.get_mult()` returns expected values."""
    assert output_object.get_mult() == expected_values


@pytest.mark.unit
@pytest.mark.output
def test_get_mult_nonexistent(output_object_nonexistent: Output):
    """Test to check if `Output.get_mult()` returns None when expected."""
    assert not output_object_nonexistent.get_mult()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_values",
    [("output_object_opt", 10), ("output_object_roci", 11)],
    indirect=["output_object"],
)
def test_get_nelectrons_not_spin_resolved(output_object: Output, expected_values: int):
    """Test to check if `Output.get_nelectrons()` returns expected values."""
    x, y = output_object.get_nelectrons()
    assert (x == expected_values) and (not y)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_values",
    [
        ("output_object_scf", (5, 5)),
        ("output_object_roci", (6, 5)),
        ("output_object_relative_corr", (80, 80)),
    ],
    indirect=["output_object"],
)
def test_get_nelectrons_spin_resolved(output_object: Output, expected_values: tuple[int, int]):
    """Test to check if `Output.get_nelectrons()` returns expected values, when `spin_resolved` is True."""
    assert output_object.get_nelectrons(spin_resolved=True) == expected_values


@pytest.mark.unit
@pytest.mark.output
def test_get_nelectrons_nonexistent(output_object_nonexistent: Output):
    """Test to check if `Output.get_nelectrons()` returns None when expected."""
    x, y = output_object_nonexistent.get_nelectrons()
    assert (not x) and (not y)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_values",
    [("output_object_relative_corr", 208), ("output_object_uvvis", 43)],
    indirect=["output_object"],
)
def test_get_nbf(output_object: Output, expected_values: int):
    """Test to check if `Output.get_nbf()` returns expected values."""
    assert output_object.get_nbf() == expected_values


@pytest.mark.unit
@pytest.mark.output
def test_get_nbf_nonexistent(output_object_nonexistent: Output):
    """Test to check if `Output.get_nbf()` returns None when expected."""
    assert not output_object_nonexistent.get_nbf()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_values",
    [
        ("output_object_opt", -76.47401149223077),
        ("output_object_scf", -75.95956918902469),
        ("output_object_neb", -7.33223897857281),
    ],
    indirect=["output_object"],
)
def test_get_final_energy_no_index(output_object: Output, expected_values: float):
    """Test to check if `Output.get_final_energy()` returns expected values."""
    assert output_object.get_final_energy() == expected_values


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "test_index, expected_value", [(0, -7.332262643705512), (2, -7.332238964312737)]
)
def test_get_final_energy_with_index(
    output_object_neb: Output, test_index: int, expected_value: float
):
    """Test to check if `Output.get_final_energy()` returns expected values when given index."""
    assert output_object_neb.get_final_energy(index=test_index) == expected_value


@pytest.mark.unit
@pytest.mark.output
def test_get_final_energy_invalid_index(output_object_neb: Output):
    """Test to check if `Output.get_final_energy()` returns None when given invalid index."""
    assert not output_object_neb.get_final_energy(
        index=len(output_object_neb.results_properties.geometries)
    )


@pytest.mark.unit
@pytest.mark.output
def test_get_final_energy_nonexistent(output_object_nonexistent: Output):
    """Test to check if `Output.get_final_energy()` returns None when expected."""
    assert not output_object_nonexistent.get_final_energy()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, key_name,expected_type",
    [("output_object_scf", "SCF", ScfEnergy), ("output_object_mp2", "MP2", Mp2Energy)],
    indirect=["output_object"],
)
def test_get_energies_type_no_index(output_object: Output, key_name: str, expected_type):
    """Test to check if `Output.get_energies()` returns expected type."""
    assert isinstance(output_object.get_energies()[key_name], expected_type)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, key_name, expected",
    [
        (
            "output_object_mp2",
            "SCF",
            ScfEnergy(method="SCF", mult=[[1]], totalenergy=[[-76.06512300578119]]),
        ),
        (
            "output_object_mp2",
            "MP2",
            Mp2Energy(
                method="MP2",
                mult=[[1]],
                correnergy=[[-0.2831817033130065]],
                refenergy=[[-76.06512300578119]],
                totalenergy=[[-76.3483047090942]],
            ),
        ),
    ],
    indirect=["output_object"],
)
def test_get_energies_no_index(output_object: Output, key_name: str, expected: Energy):
    """Test to check if `Output.get_energies()` returns expected values."""
    assert output_object.get_energies()[key_name] == expected


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    " index, expected",
    [
        (2, ScfEnergy(method="SCF", mult=[[1]], totalenergy=[[-7.332238964312737]])),
        (0, ScfEnergy(method="SCF", mult=[[1]], totalenergy=[[-7.332262643705512]])),
    ],
)
def test_get_energies_with_index(output_object_neb: Output, index, expected, key_name: str = "SCF"):
    """Test to check if `Output.get_energies()` returns expected values given index."""
    assert output_object_neb.get_energies(index=index)[key_name] == expected


@pytest.mark.unit
@pytest.mark.output
def test_get_gradient_default_index(output_object_neb: Output):
    """Test to check if `Output.get_gradient()` returns None when expected."""
    assert not output_object_neb.get_gradient()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, index",
    [("output_object_neb", -2), ("output_object_opt", 1)],
    indirect=["output_object"],
)
def test_get_gradient_with_index(output_object: Output, index: int):
    """Test to check if `Output.get_gradient()` returns expected values when given index."""
    assert isinstance(output_object.get_gradient(index=index), list)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object", [("output_object_opt"), ("output_object_neb")], indirect=["output_object"]
)
def test_get_structure_no_fragments(output_object: Output):
    """Test to check if `Output.get_structure()` returns `Structure` object."""
    assert isinstance(output_object.get_structure(), Structure)


@pytest.mark.unit
@pytest.mark.output
def test_get_structure_with_fragments(output_object_led: Output):
    """Test to check if `Output.get_structure()` returns `Structure` object with fragment ids when `with_fragments=True`."""
    structure = output_object_led.get_structure(with_fragments=True)
    for atom in structure.atoms:
        assert atom.fragment_id


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "index, expected_coordinates",
    [
        (-1, [-3.575441154384772, 1.7822964427054289, 0.011563827777798096]),
        (1, [-3.5694568743985595, 1.7784458165284545, 0.004024935055685528]),
    ],
)
def test_get_structure_with_index(
    output_object_opt: Output, index: int, expected_coordinates: list
):
    """Test to check if Output.get_structure() returns index-specific `Structure` object when index is given."""
    structure = output_object_opt.get_structure(index=index)
    assert structure.atoms[0].coordinates.to_list() == expected_coordinates


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("output_object", [("output_object_led")], indirect=["output_object"])
def test_get_mos_returns_dict(output_object: Output):
    """Test to check if `Output.get_mos()` returns `dict` object."""
    assert isinstance(output_object.get_mos(), dict)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("output_object", [("output_object_led")], indirect=["output_object"])
def test_get_mos_returns_mo(output_object: Output):
    """Test to check if `Output.get_mos()` returns `dict` with `MO` objects."""
    for value in output_object.get_mos().values():
        assert all(isinstance(mo, MO) for mo in value)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("output_object", [("output_object_led")], indirect=["output_object"])
def test_get_homo(output_object: Output):
    """Test to check if `Output.get_homo()` returns `MOData` object."""
    assert isinstance(output_object.get_homo(), MOData)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("output_object", [("output_object_led")], indirect=["output_object"])
def test_get_lumo(output_object: Output):
    """Test to check if `Output.get_lumo()` returns `MOData` object."""
    assert isinstance(output_object.get_lumo(), MOData)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected",
    [("output_object_led", 17.656923115035248), ("output_object_roci", 8.035362912976161)],
    indirect=["output_object"],
)
def test_get_hl_gap(output_object: Output, expected: float):
    """Test to check if `Output.get_hl_gap()` returns expected values."""
    assert output_object.get_hl_gap() == expected


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("output_object", ["output_object_opt"], indirect=["output_object"])
def test_get_mulliken(output_object: Output):
    """Test to check if `Output.get_mulliken()` returns `MullikenPopulationAnalysis` object."""
    for mulliken in output_object.get_mulliken():
        assert isinstance(mulliken, MullikenPopulationAnalysis)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("output_object", ["output_object_neb"], indirect=["output_object"])
def test_get_mulliken_returns_none(output_object: Output):
    """Test to check if `Output.get_mulliken()` returns `None` when expected."""
    assert not output_object.get_mulliken()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, index, expected_object",
    [
        (
            "output_object_opt",
            -1,
            MullikenPopulationAnalysis(
                natoms=3,
                atno=[[8], [1], [1]],
                method="SCF",
                level="Relaxed density",
                mult=1,
                state=-1,
                irrep=0,
                atomiccharges=[[-0.6359777531861273], [0.31798155772826897], [0.3179961954578747]],
            ),
        ),
        (
            "output_object_opt",
            0,
            MullikenPopulationAnalysis(
                natoms=3,
                atno=[[8], [1], [1]],
                method="SCF",
                level="Relaxed density",
                mult=1,
                state=-1,
                irrep=0,
                atomiccharges=[[-0.6505800051560868], [0.32528275278127494], [0.32529725237480145]],
            ),
        ),
    ],
    indirect=["output_object"],
)
def test_get_mulliken_with_index(
    output_object: Output, index: int, expected_object: MullikenPopulationAnalysis
):
    """Test to check if `Output.get_mulliken()` returns expected `MullikenPopulationAnalysis` object when index is given."""
    assert output_object.get_mulliken(index=index)[0] == expected_object


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("output_object", ["output_object_opt"], indirect=["output_object"])
def test_get_loewdin(output_object: Output):
    """Test to check if `Output.get_loewdin()` returns `LoewdinPopulationAnalysis` object."""
    for loewdin in output_object.get_loewdin():
        assert isinstance(loewdin, LoewdinPopulationAnalysis)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("output_object", ["output_object_neb"], indirect=["output_object"])
def test_get_loewdin_returns_none(output_object: Output):
    """Test if `Output.get_loewdin()` returns `None` when expected."""
    assert not output_object.get_loewdin()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, index, expected_object",
    [
        (
            "output_object_opt",
            -1,
            LoewdinPopulationAnalysis(
                natoms=3,
                atno=[[8], [1], [1]],
                method="SCF",
                level="Relaxed density",
                mult=1,
                state=-1,
                irrep=0,
                atomiccharges=[
                    [-0.30406251807199247],
                    [0.15203049288389225],
                    [0.15203202518813064],
                ],
            ),
        ),
        (
            "output_object_opt",
            0,
            LoewdinPopulationAnalysis(
                natoms=3,
                atno=[[8], [1], [1]],
                method="SCF",
                level="Relaxed density",
                mult=1,
                state=-1,
                irrep=0,
                atomiccharges=[[-0.3160029557468125], [0.15800138853952062], [0.15800156720728797]],
            ),
        ),
    ],
    indirect=["output_object"],
)
def test_get_loewdin_with_index(
    output_object: Output, index: int, expected_object: LoewdinPopulationAnalysis
):
    """Test to check if `Output.get_loewdin()` returns expected `LoewdinPopulationAnalysis` object when index is given."""
    assert output_object.get_loewdin(index=index)[0] == expected_object


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object", ["output_object_pop_analysis"], indirect=["output_object"]
)
def test_get_chelpg(output_object: Output):
    """Test to check whether `Output.get_chelpg()` returns `ChelpgPopulationAnalysis` object."""
    for chelpg in output_object.get_chelpg():
        assert isinstance(chelpg, ChelpgPopulationAnalysis)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("output_object", ["output_object_neb"], indirect=["output_object"])
def test_get_chelpg_returns_none(output_object: Output):
    """Test if `Output.get_chelpg()` returns `None` when expected."""
    assert not output_object.get_loewdin()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, index, expected_object",
    [
        (
            "output_object_pop_analysis",
            0,
            ChelpgPopulationAnalysis(
                natoms=3,
                atno=[[8], [1], [1]],
                method="SCF",
                level="Relaxed density",
                mult=1,
                state=-1,
                irrep=0,
                atomiccharges=[[-0.8520905347302165], [0.4262088004014229], [0.4258817343287936]],
            ),
        )
    ],
    indirect=["output_object"],
)
def test_get_chelpg_with_index(
    output_object: Output, index: int, expected_object: ChelpgPopulationAnalysis
):
    """Test to check whether `Output.get_chelpg()` returns expected `ChelpgPopulationAnalysis` object when index is given."""
    assert output_object.get_chelpg(index=index)[0] == expected_object


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("output_object", ["output_object_opt"], indirect=["output_object"])
def test_get_mayer(output_object: Output):
    """Test to check whether `Output.get_mayer()` returns `MayerPopulationAnalysis` object."""
    for loewdin in output_object.get_mayer():
        assert isinstance(loewdin, MayerPopulationAnalysis)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("output_object", ["output_object_neb"], indirect=["output_object"])
def test_get_mayer_returns_none(output_object: Output):
    """Test if `Output.get_mayer()` returns `None` when expected."""
    assert not output_object.get_mayer()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, index, expected_object",
    [
        (
            "output_object_opt",
            -1,
            MayerPopulationAnalysis(
                natoms=3,
                atno=[[8], [1], [1]],
                method="SCF",
                level="Relaxed density",
                mult=1,
                state=-1,
                irrep=0,
                atomiccharges=None,
                bondthresh=0.1,
                nbondordersprint=2,
                bondorders=[[0.9116931727654458], [0.91168060929033]],
                components=[(0, 8, 1, 1), (0, 8, 2, 1)],
                na=[[8.635977753186122], [0.682018442271731], [0.6820038045421255]],
                za=[[8.0], [1.0], [1.0]],
                qa=[[-0.6359777531861219], [0.31798155772826897], [0.3179961954578745]],
                va=[[1.8233737820558167], [0.9167261658022937], [0.916713602327183]],
                bva=[[1.8233737820557767], [0.9167261658022923], [0.9167136023271765]],
                fa=[[0.0], [0.0], [0.0]],
            ),
        ),
        (
            "output_object_opt",
            0,
            MayerPopulationAnalysis(
                natoms=3,
                atno=[[8], [1], [1]],
                method="SCF",
                level="Relaxed density",
                mult=1,
                state=-1,
                irrep=0,
                atomiccharges=None,
                bondthresh=0.1,
                nbondordersprint=2,
                bondorders=[[0.9044614880829198], [0.904447205838748]],
                components=[(0, 8, 1, 1), (0, 8, 2, 1)],
                na=[[8.650580005156085], [0.674717247218725], [0.6747027476251986]],
                za=[[8.0], [1.0], [1.0]],
                qa=[[-0.650580005156085], [0.32528275278127505], [0.32529725237480145]],
                va=[[1.8089086939216426], [0.9114903718801635], [0.9114760896359948]],
                bva=[[1.8089086939216674], [0.9114903718801677], [0.9114760896359959]],
                fa=[[0.0], [0.0], [0.0]],
            ),
        ),
    ],
    indirect=["output_object"],
)
def test_get_mayer_with_index(
    output_object: Output, index: int, expected_object: MayerPopulationAnalysis
):
    """Test if `Output.get_mayer()` returns expected object when given index."""
    assert output_object.get_mayer(index=index)[0] == expected_object


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object", ["output_object_pop_analysis"], indirect=["output_object"]
)
def test_get_hirshfeld(output_object: Output):
    """Test if `Output.get_hirshfeld()` returns `HirshfeldPopulationAnalysis` object."""
    for hirshfeld in output_object.get_hirshfeld():
        assert isinstance(hirshfeld, HirshfeldPopulationAnalysis)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("output_object", ["output_object_neb"], indirect=["output_object"])
def test_get_hirshfeld_returns_none(output_object: Output):
    """Test if `Output.get_hirshfeld()` returns `None` when expected."""
    assert not output_object.get_hirshfeld()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object,length", [("output_object_pop_analysis", 3)], indirect=["output_object"]
)
def test_get_hirshfeld_length_of_list(output_object: str, length: int):
    """Test if `Output.get_hirshfeld()` returns list of correct length."""
    assert len(output_object.get_hirshfeld()) == length


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, index, expected_object",
    [
        (
            "output_object_pop_analysis",
            0,
            HirshfeldPopulationAnalysis(
                natoms=3,
                atno=[[8], [1], [1]],
                method="SCF",
                level="Relaxed density",
                mult=1,
                state=-1,
                irrep=0,
                atomiccharges=[[-0.3634375969170289], [0.18171954075847874], [0.18172048615235414]],
                densa=4.999998785003111,
                densb=4.999998785003111,
                spin=[[0.0], [0.0], [0.0]],
            ),
        ),
        (
            "output_object_pop_analysis",
            1,
            HirshfeldPopulationAnalysis(
                natoms=3,
                atno=[[8], [1], [1]],
                method="MP2",
                level="Unrelaxed density",
                mult=1,
                state=-1,
                irrep=0,
                atomiccharges=[
                    [-0.35859376148576594],
                    [0.17929857560395224],
                    [0.17929766948127568],
                ],
                densa=4.999998758200266,
                densb=4.999998758200266,
                spin=[[0.0], [0.0], [0.0]],
            ),
        ),
        (
            "output_object_pop_analysis",
            2,
            HirshfeldPopulationAnalysis(
                natoms=3,
                atno=[[8], [1], [1]],
                method="MP2",
                level="Relaxed density",
                mult=1,
                state=-1,
                irrep=0,
                atomiccharges=[[-0.352158542367464], [0.1760818011203501], [0.17607925316855777]],
                densa=4.999998744039276,
                densb=4.999998744039276,
                spin=[[0.0], [0.0], [0.0]],
            ),
        ),
    ],
    indirect=["output_object"],
)
def test_get_hirshfeld_with_index(
    output_object: Output, index: int, expected_object: HirshfeldPopulationAnalysis
):
    """Test if `Output.get_hirshfeld()` returns expected `HirshfeldPopulationAnalysis` object when given index."""
    assert output_object.get_hirshfeld()[index] == expected_object


@pytest.mark.unit
@pytest.mark.output
def test_get_mbis_returns_list(output_object_mbis: Output):
    """Test if `Output.get_mbis()` returns list."""
    assert isinstance(output_object_mbis.get_mbis(), list)


@pytest.mark.unit
@pytest.mark.output
def test_get_mbis_returns_none(output_object_neb: Output):
    """Test if `Output.get_mbis()` returns `None` when expected."""
    assert not output_object_neb.get_mbis()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_object",
    [
        (
            "output_object_mbis",
            MbisPopulationAnalysis(
                natoms=3,
                atno=[[8], [1], [1]],
                method="SCF",
                level="Relaxed density",
                mult=1,
                state=-1,
                irrep=0,
                atomiccharges=[[-0.8880465516831944], [0.44402365887136586], [0.44402343711439907]],
                thresh=1e-06,
                niter=40,
                largeprint=False,
                densa=4.999999727848726,
                densb=4.999999727848726,
                spin=[[0.0], [0.0], [0.0]],
                npopval=[[7.269075842634232], [0.5559763411286341], [0.555976562885601]],
                sigmaval=[[0.40431322837699174], [0.34801696817749295], [0.3480172536216172]],
            ),
        )
    ],
    indirect=["output_object"],
)
def test_get_mbis_returned_object(output_object: Output, expected_object: MbisPopulationAnalysis):
    """Test if `Output.get_mbis()` returns expected `MbisPopulationAnalysis` object."""
    assert output_object.get_mbis()[0] == expected_object


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object", ["output_object_neb", "output_object_opt"], indirect=["output_object"]
)
def test_get_dipole_returns_list_of_dipole_moment(output_object: Output):
    """Test if `Output.get_dipole()` returns list of `DipoleMoment` objects."""
    for dipole_moment in output_object.get_dipole():
        assert isinstance(dipole_moment, DipoleMoment)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, index",
    [("output_object_opt", 0), ("output_object_neb", 1)],
    indirect=["output_object"],
)
def test_get_dipole_returns_none(output_object: str, index: int):
    """Test if `Output.get_dipole()` returns `None` when expected."""
    assert not output_object.get_dipole(index=index)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_object",
    [
        (
            "output_object_opt",
            DipoleMoment(
                method="SCF",
                level="Relaxed density",
                mult=1,
                state=-1,
                irrep=0,
                doatomicdipole=False,
                dipoleeleccontrib=[
                    [-0.09027459737314743],
                    [0.05807804194177346],
                    [0.113706070713446],
                ],
                dipolenuccontrib=[
                    [0.5611887075711595],
                    [-0.3610025526213261],
                    [-0.7067836220988835],
                ],
                dipolemagnitude=0.8156373828555052,
                dipoletotal=[[0.47091411019801205], [-0.3029245106795526], [-0.5930775513854375]],
            ),
        ),
        (
            "output_object_neb",
            DipoleMoment(
                method="SCF",
                level="Relaxed density",
                mult=1,
                state=-1,
                irrep=0,
                doatomicdipole=False,
                dipoleeleccontrib=[
                    [-4.487630629182515e-07],
                    [4.237944368918665e-05],
                    [1.9626517355565724e-05],
                ],
                dipolenuccontrib=[
                    [4.512655014110578e-07],
                    [-4.6518388876926053e-05],
                    [-2.151689626517239e-05],
                ],
                dipolemagnitude=4.550209440365934e-06,
                dipoletotal=[
                    [2.502438492806289e-09],
                    [-4.138945187739403e-06],
                    [-1.8903789096066672e-06],
                ],
            ),
        ),
    ],
    indirect=["output_object"],
)
def test_get_dipole_returns_correct_object(output_object: Output, expected_object: DipoleMoment):
    """Test if `Output.get_dipole()` returns expected `DipoleMoment` object."""
    assert output_object.get_dipole()[0] == expected_object


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object", ["output_object_pop_analysis"], indirect=["output_object"]
)
def test_get_quadrupole_returns_list_of_quadrupole_moment(output_object: Output):
    """Test if `Output.get_quadrupole()` returns list of `QuadrupoleMoment` objects."""
    for quadrupole_moment in output_object.get_quadrupole():
        assert isinstance(quadrupole_moment, QuadrupoleMoment)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object", ["output_object_pop_analysis"], indirect=["output_object"]
)
def test_get_quadrupole_returns_list_of_correct_length(output_object: Output):
    """Test if `Output.get_quadrupole()` returns list of correct length"""
    assert len(output_object.get_quadrupole()) == 3


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, index",
    [("output_object_opt", 0), ("output_object_neb", 1)],
    indirect=["output_object"],
)
def test_get_quadrupole_returns_none(output_object: Output, index: int):
    """Test if `Output.get_quadrupole()` returns `None` when expected."""
    assert not output_object.get_quadrupole(index=index)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, index, expected_object",
    [
        (
            "output_object_pop_analysis",
            0,
            QuadrupoleMoment(
                method="SCF",
                level="Relaxed density",
                mult=1,
                irrep=0,
                state=-1,
                doatomicquad=False,
                isotropicquadmoment=-4.139089762124142,
                quadeleccontrib=[
                    [-6.058543260921939],
                    [-6.565397142755049],
                    [-6.107836962748215],
                    [-0.7716104151997946],
                    [0.1852679616946788],
                    [-0.4895149684498654],
                ],
                quadnuccontrib=[
                    [1.702023843798357],
                    [2.873460224244342],
                    [1.739024012010075],
                    [1.7063686761401595],
                    [-0.3251662711247978],
                    [1.0703538057273103],
                ],
                quadtotal=[
                    [-4.356519417123582],
                    [-3.6919369185107067],
                    [-4.36881295073814],
                    [0.934758260940365],
                    [-0.139898309430119],
                    [0.5808388372774449],
                ],
                quaddiagonalized=[
                    [-5.2614837259484055],
                    [-4.238111814057211],
                    [-2.917673746366811],
                ],
            ),
        ),
        (
            "output_object_pop_analysis",
            1,
            QuadrupoleMoment(
                method="MP2",
                level="Unrelaxed density",
                mult=1,
                irrep=0,
                state=-1,
                doatomicquad=False,
                isotropicquadmoment=-4.160140674445025,
                quadeleccontrib=[
                    [-6.07825009056406],
                    [-6.589043233170835],
                    [-6.127636779652955],
                    [-0.7773062277646743],
                    [0.18631151933875473],
                    [-0.4930854296224551],
                ],
                quadnuccontrib=[
                    [1.702023843798357],
                    [2.873460224244342],
                    [1.739024012010075],
                    [1.7063686761401595],
                    [-0.3251662711247978],
                    [1.0703538057273103],
                ],
                quadtotal=[
                    [-4.376226246765703],
                    [-3.715583008926493],
                    [-4.38861276764288],
                    [0.9290624483754852],
                    [-0.13885475178604306],
                    [0.5772683761048552],
                ],
                quaddiagonalized=[
                    [-5.2755397220909614],
                    [-4.258834456089124],
                    [-2.9460478451549905],
                ],
            ),
        ),
    ],
    indirect=["output_object"],
)
def test_get_quadrupole_returns_correct_object(
    output_object: Output, index: int, expected_object: QuadrupoleMoment
):
    """Test if `Output.get_quadrupole` returns expected object when given index."""
    assert output_object.get_quadrupole()[index] == expected_object


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object",
    ["output_object_pop_analysis", "output_object_rama"],
    indirect=["output_object"],
)
def test_get_polarizability_returns_list(output_object: Output):
    """Test if `Output.get_polarizability()` returns list."""
    assert isinstance(output_object.get_polarizability(), list)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("output_object", ["output_object_neb"], indirect=True)
def test_get_polarizability_returns_none(output_object: Output):
    """Test if `Output.get_polarizability()` returns None when expected."""
    assert not output_object.get_polarizability()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object",
    ["output_object_pop_analysis", "output_object_rama"],
    indirect=["output_object"],
)
def test_get_polarizability_returns_list_of_correct_type(output_object: Output):
    """Test of Output.get_polarizability() returns list of `Polarizability` type."""
    for polarizability in output_object.get_polarizability():
        assert isinstance(polarizability, Polarizability)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, length",
    [("output_object_pop_analysis", 3), ("output_object_rama", 1)],
    indirect=["output_object"],
)
def test_get_polarizability_returns_list_of_correct_length(output_object: Output, length: int):
    """Test of Output.get_polarizability() returns list of correct length."""
    assert len(output_object.get_polarizability()) == length


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_object",
    [
        (
            "output_object_pop_analysis",
            Polarizability(
                method="SCF",
                level="Relaxed density",
                mult=1,
                state=-1,
                irrep=0,
                doatomicpolar=False,
                rawcartesian=[
                    (5.024905732862544, 1.7799831262071912, -0.3653387982981067),
                    (1.7799831262071912, 6.231120698159827, 1.121314761217183),
                    (-0.3653387982981067, 1.121314761217183, 5.087268043407156),
                ],
                diagonalizedtensor=[[3.2304502403642292], [5.401864509665477], [7.710979724399823]],
                orientation=[
                    (-0.6659195281060317, -0.5502680955214159, -0.5037422010694302),
                    (0.5733733024494435, 0.05448091103239561, -0.817480817127411),
                    (-0.47727794640571813, 0.8332087693875493, -0.2792291325962005),
                ],
                isotropicpolar=5.447764824809843,
            ),
        ),
        (
            "output_object_rama",
            Polarizability(
                method="SCF",
                level="Relaxed density",
                mult=1,
                state=-1,
                irrep=0,
                doatomicpolar=False,
                rawcartesian=[
                    (3.1038115115293277, -1.897662897230793e-08, -7.239806814925587e-10),
                    (-1.897662897230793e-08, 7.169005553207977, 7.746995026007109e-08),
                    (-7.239806814925587e-10, 7.746995026007109e-08, 4.642603341224554),
                ],
                diagonalizedtensor=[[3.1038115115293277], [4.642603341224551], [7.169005553207984]],
                orientation=[
                    (1.0, 4.704860564108599e-10, -4.668074586600124e-09),
                    (4.6680745709876126e-09, 3.066413966134831e-08, 0.9999999999999997),
                    (4.704861995533507e-10, -0.9999999999999994, 3.0664139659152044e-08),
                ],
                isotropicpolar=4.971806801987287,
            ),
        ),
    ],
    indirect=["output_object"],
)
def test_get_polarizability_returns_correct_objects(
    output_object: Output, expected_object: Polarizability
):
    """Test if `Output.get_polarizability()` returns correct objects."""
    assert output_object.get_polarizability()[0] == expected_object


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object", ["output_object_freq", "output_object_pal"], indirect=["output_object"]
)
def test_get_zpe_returns_correct_type(output_object: Output):
    """Test if `Output.get_zpe()` returns correct type."""
    assert isinstance(output_object.get_zpe(), float)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object", ["output_object_neb", "output_object_dft"], indirect=["output_object"]
)
def test_get_zpe_returns_correct_none(output_object: Output):
    """Test if `Output.get_zpe()` returns None when expected."""
    assert not output_object.get_zpe()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_value",
    [
        ("output_object_freq", 0.02062156916775446),
        ("output_object_pal", 0.021204801105653905),
    ],
    indirect=["output_object"],
)
def test_get_zpe_returns_correct_value(output_object: Output, expected_value: float):
    """Test if `Output.get_zpe()` returns correct value."""
    assert output_object.get_zpe() == expected_value


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object",
    ["output_object_relative_corr", "output_object_rama"],
    indirect=["output_object"],
)
def test_get_inner_energy_returns_float(output_object: Output):
    """Test if `Output.get_inner_energy()` returns float."""
    assert isinstance(output_object.get_inner_energy(), float)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object", ["output_object_opt", "output_object_cpcm"], indirect=["output_object"]
)
def test_get_inner_energy_returns_none(output_object: Output):
    """Test if `Output.get_inner_energy()` returns None when expected."""
    assert not output_object.get_inner_energy()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_value",
    [
        ("output_object_relative_corr", -40659.55477913393),
        ("output_object_rama", -76.29223117253484),
    ],
    indirect=["output_object"],
)
def test_get_inner_energy_returns_correct_value(output_object: Output, expected_value: float):
    """Test if `Output.get_inner_energy()` returns correct value."""
    assert output_object.get_inner_energy() == expected_value


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object",
    ["output_object_relative_corr", "output_object_rama"],
    indirect=["output_object"],
)
def test_get_enthalpy_returns_float(output_object: Output):
    """Test if `Output.get_enthalpy()` returns float."""
    assert isinstance(output_object.get_enthalpy(), float)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object", ["output_object_opt", "output_object_cpcm"], indirect=["output_object"]
)
def test_get_enthalpy_returns_none(output_object: Output):
    """Test if `Output.get_enthalpy()` returns None when expected."""
    assert not output_object.get_enthalpy()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_value",
    [
        ("output_object_relative_corr", -40659.55383492488),
        ("output_object_rama", -76.29128696349258),
    ],
    indirect=["output_object"],
)
def test_get_enthalpy_returns_correct_value(output_object: Output, expected_value: float):
    """Test if `Output.get_enthalpy()` returns correct value."""
    assert output_object.get_enthalpy() == expected_value


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object",
    ["output_object_relative_corr", "output_object_rama"],
    indirect=["output_object"],
)
def test_get_entropy_returns_float(output_object: Output):
    """Test if `Output.get_entropy()` returns float."""
    assert isinstance(output_object.get_entropy(), float)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object", ["output_object_opt", "output_object_cpcm"], indirect=["output_object"]
)
def test_get_entropy_returns_none(output_object: Output):
    """Test if `Output.get_entropy()` returns None when expected."""
    assert not output_object.get_entropy()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_value",
    [
        ("output_object_relative_corr", 0.032484726133754235),
        ("output_object_rama", 0.021312497484212576),
    ],
    indirect=["output_object"],
)
def test_get_entropy_returns_correct_value(output_object: Output, expected_value: float):
    """Test if `Output.get_entropy()` returns correct value."""
    assert output_object.get_entropy() == expected_value


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object",
    ["output_object_relative_corr", "output_object_rama"],
    indirect=["output_object"],
)
def test_get_free_energy_returns_float(output_object: Output):
    """Test if `Output.get_free_energy()` returns float."""
    assert isinstance(output_object.get_free_energy(), float)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object", ["output_object_opt", "output_object_cpcm"], indirect=["output_object"]
)
def test_get_free_energy_returns_none(output_object: Output):
    """Test if `Output.get_free_energy()` returns None when expected."""
    assert not output_object.get_free_energy()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_value",
    [
        ("output_object_relative_corr", -40659.58631965102),
        ("output_object_rama", -76.3125994609768),
    ],
    indirect=["output_object"],
)
def test_get_free_energy_returns_correct_value(output_object: Output, expected_value: float):
    """Test if `Output.get_free_energy()` returns correct value."""
    assert output_object.get_free_energy() == expected_value


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object",
    ["output_object_relative_corr", "output_object_rama"],
    indirect=["output_object"],
)
def test_get_el_energy_returns_float(output_object: Output):
    """Test if `Output.get_el_energy()` returns correct value."""
    assert isinstance(output_object.get_el_energy(), float)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object", ["output_object_opt", "output_object_cpcm"], indirect=["output_object"]
)
def test_get_el_energy_returns_none(output_object: Output):
    """Test if `Output.get_el_energy()` returns None when expected."""
    assert not output_object.get_el_energy()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_value",
    [
        ("output_object_relative_corr", -40659.558084306336),
        ("output_object_rama", -76.31703512990781),
    ],
    indirect=["output_object"],
)
def test_get_el_energy_returns_correct_value(output_object: Output, expected_value: float):
    """Test if `Output.get_el_energy()` returns correct value."""
    assert output_object.get_el_energy() == expected_value


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object",
    ["output_object_relative_corr", "output_object_rama"],
    indirect=["output_object"],
)
def test_get_free_energy_delta_returns_float(output_object: Output):
    """Test if `Output.get_free_energy()` returns correct value."""
    assert isinstance(output_object.get_free_energy_delta(), float)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object", ["output_object_opt", "output_object_cpcm"], indirect=["output_object"]
)
def test_get_free_energy_delta_returns_none(output_object: Output):
    """Test if `Output.get_free_energy_delta()` returns None when expected."""
    assert not output_object.get_free_energy_delta()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "output_object, expected_value",
    [
        ("output_object_relative_corr", -0.02823534468188882),
        ("output_object_rama", 0.004435668931009218),
    ],
    indirect=["output_object"],
)
def test_get_free_energy_delta_returns_correct_value(output_object: Output, expected_value: float):
    """Test if `Output.get_free_energy_delta()` returns correct value."""
    assert output_object.get_free_energy_delta() == expected_value
