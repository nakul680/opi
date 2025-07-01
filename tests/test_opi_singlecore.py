import pytest

from opi.core import Calculator
from opi.input.simple_keywords import Dft, Task
from opi.input.structures import Structure


@pytest.fixture(scope="session")
def tmp_path(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp(basename="temp")
    return tmp_path


def test_basename_property(tmp_path):
    calc = Calculator(basename="job")
    assert calc.basename == "job"
    with pytest.raises(ValueError):
        calc.basename = "spaced out"
    with pytest.raises(ValueError):
        calc.basename = ""

    calc.working_dir = tmp_path
    assert calc.working_dir == tmp_path.resolve()

    with pytest.raises(ValueError):
        calc.working_dir = "/path/that/doesnt/exist"

    calc.input.add_simple_keywords(Dft.R2SCAN_3C, Task.SP)

    xyz_data = """\
    3

    O      0.00000   -0.00000    0.00000
    H      0.00000    0.96899    0.00000
    H      0.93966   -0.23409    0.03434\n
    """

    formatted_xyz = """O             0.0000000000000000            -0.0000000000000000             0.0000000000000000\nH             0.0000000000000000             0.9689900000000000             0.0000000000000000\nH             0.9396600000000001            -0.2340900000000000             0.0343400000000000"""

    with open(calc.working_dir / "struc.xyz", "w") as f:
        f.write(xyz_data)

    calc.structure = Structure.from_xyz(calc.working_dir / "struc.xyz")

    calc.write_input()

    inpfile = calc.inpfile
    assert inpfile.exists()
    text = inpfile.read_text()
    assert Dft.R2SCAN_3C.format_orca() in text
    assert Task.SP.format_orca() in text
    assert "%output" in text
    assert formatted_xyz in text

    calc.run()
    outfile = calc.inpfile.with_suffix(".out")

    assert outfile.exists()

    output = calc.get_output()
    assert output.basename == calc.basename
    assert output.working_dir == calc.working_dir
    if not output.terminated_normally():
        errfile = calc.inpfile.with_suffix(".err")
        assert errfile.exists()
    else:
        assert output.terminated_normally()
